"""
Bot message handlers for Health Tracker
"""

import logging
from datetime import datetime, time, timedelta
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import (
    WELCOME_MESSAGE, START_MONITORING_MESSAGE, UserStates,
    MOOD_SCALE, AGGRESSION_SCALE, REMINDER_TIME, DEFAULT_TIMEZONE_OFFSET
)
from database import (
    create_user, get_user, save_health_data, 
    check_today_data_exists, get_user_health_data
)
from ml_analysis import analyze_health_data, generate_recommendations

logger = logging.getLogger(__name__)

class RegistrationStates(StatesGroup):
    waiting_name = State()
    waiting_age = State()

class DataInputStates(StatesGroup):
    waiting_sleep = State()
    waiting_activity = State()
    waiting_aggression = State()
    waiting_mood = State()

router = Router()

# Temporary storage for user data during input
user_temp_data = {}

def create_mood_keyboard():
    """Create keyboard for mood selection"""
    keyboard = [
        [KeyboardButton(text="😡"), KeyboardButton(text="😐"), KeyboardButton(text="🙂")],
        [KeyboardButton(text="😃"), KeyboardButton(text="🤩")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

def create_aggression_keyboard():
    """Create keyboard for aggression level selection"""
    keyboard = [
        [KeyboardButton(text="Past"), KeyboardButton(text="O'rtacha"), KeyboardButton(text="Baland")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """Handle /start command"""
    user = await get_user(message.from_user.id)
    
    if user:
        await message.answer(
            f"Salom {user['full_name']}! Siz allaqachon ro'yxatdan o'tgansiz.\n\n"
            f"Bugungi ma'lumotlar uchun /today buyrug'ini ishlating."
        )
    else:
        await message.answer(WELCOME_MESSAGE)
        await state.set_state(RegistrationStates.waiting_name)

@router.message(StateFilter(RegistrationStates.waiting_name))
async def process_name(message: Message, state: FSMContext):
    """Process user's name input"""
    await state.update_data(name=message.text)
    await message.answer("Yoshingizni kiriting (faqat raqam):")
    await state.set_state(RegistrationStates.waiting_age)

@router.message(StateFilter(RegistrationStates.waiting_age))
async def process_age(message: Message, state: FSMContext):
    """Process user's age input"""
    try:
        age = int(message.text)
        if age < 1 or age > 120:
            await message.answer("Iltimos, to'g'ri yosh kiriting (1-120 oralig'ida):")
            return
        
        data = await state.get_data()
        name = data.get('name')
        
        # Create user in database
        success = await create_user(message.from_user.id, name, age)
        
        if success:
            await message.answer(START_MONITORING_MESSAGE)
            await state.clear()
        else:
            await message.answer("Xatolik yuz berdi. Qaytadan urinib ko'ring.")
            await state.clear()
    
    except ValueError:
        await message.answer("Iltimos, faqat raqam kiriting:")

@router.message(Command("today"))
async def today_command(message: Message, state: FSMContext):
    """Handle /today command for data input"""
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("Avval ro'yxatdan o'ting. /start buyrug'ini ishlating.")
        return
    
    # Get local time (UTC + user timezone offset)
    utc_now = datetime.now()
    local_time = utc_now + timedelta(hours=DEFAULT_TIMEZONE_OFFSET)
    current_time = local_time.time()
    reminder_time = time(21, 0)  # 21:00
    today_date = local_time.strftime("%Y-%m-%d")
    
    # Allow data input only after 21:00 local time
    if current_time < reminder_time:
        await message.answer(
            f"Ma'lumotlarni faqat soat {REMINDER_TIME} dan keyin kiritish mumkin. "
            f"Hozir mahalliy vaqt bo'yicha soat {current_time.strftime('%H:%M')}"
        )
        return
    
    # Check if data already exists for today
    data_exists = await check_today_data_exists(user['id'], today_date)
    if data_exists:
        await message.answer("Siz bugun allaqachon ma'lumot kiritgansiz!")
        return
    
    # Initialize temporary data storage
    user_temp_data[message.from_user.id] = {"user_id": user['id'], "date": today_date}
    
    await message.answer("Bugun necha soat uxladingiz? (masalan: 7.5)")
    await state.set_state(DataInputStates.waiting_sleep)

@router.message(StateFilter(DataInputStates.waiting_sleep))
async def process_sleep_time(message: Message, state: FSMContext):
    """Process sleep time input"""
    try:
        sleep_time = float(message.text)
        if sleep_time < 0 or sleep_time > 24:
            await message.answer("Iltimos, to'g'ri uyqu vaqtini kiriting (0-24 soat):")
            return
        
        user_temp_data[message.from_user.id]['sleep_time'] = sleep_time
        await message.answer("Bugun jami necha soat jismoniy mashq qildingiz? (masalan: 1.5)")
        await state.set_state(DataInputStates.waiting_activity)
    
    except ValueError:
        await message.answer("Iltimos, to'g'ri format kiriting (masalan: 7.5):")

@router.message(StateFilter(DataInputStates.waiting_activity))
async def process_activity_time(message: Message, state: FSMContext):
    """Process activity time input"""
    try:
        activity_time = float(message.text)
        if activity_time < 0 or activity_time > 24:
            await message.answer("Iltimos, to'g'ri vaqt kiriting (0-24 soat):")
            return
        
        user_temp_data[message.from_user.id]['activity_time'] = activity_time
        await message.answer(
            "Bugungi agressiya darajangizni tanlang:",
            reply_markup=create_aggression_keyboard()
        )
        await state.set_state(DataInputStates.waiting_aggression)
    
    except ValueError:
        await message.answer("Iltimos, to'g'ri format kiriting (masalan: 1.5):")

@router.message(StateFilter(DataInputStates.waiting_aggression))
async def process_aggression(message: Message, state: FSMContext):
    """Process aggression level input"""
    if message.text not in AGGRESSION_SCALE:
        await message.answer(
            "Iltimos, tugmalardan birini tanlang:",
            reply_markup=create_aggression_keyboard()
        )
        return
    
    user_temp_data[message.from_user.id]['aggression_level'] = AGGRESSION_SCALE[message.text]
    await message.answer(
        "Bugungi kayfiyatingizni tanlang:",
        reply_markup=create_mood_keyboard()
    )
    await state.set_state(DataInputStates.waiting_mood)

@router.message(StateFilter(DataInputStates.waiting_mood))
async def process_mood(message: Message, state: FSMContext):
    """Process mood level input and complete data collection"""
    if message.text not in MOOD_SCALE:
        await message.answer(
            "Iltimos, tugmalardan birini tanlang:",
            reply_markup=create_mood_keyboard()
        )
        return
    
    user_data = user_temp_data.get(message.from_user.id)
    if not user_data:
        await message.answer("Xatolik yuz berdi. Qaytadan /today buyrug'ini ishlating.")
        await state.clear()
        return
    
    user_data['mood_level'] = MOOD_SCALE[message.text]
    
    # Save data to database
    success = await save_health_data(
        user_data['user_id'],
        user_data['date'],
        user_data['sleep_time'],
        user_data['activity_time'],
        user_data['aggression_level'],
        user_data['mood_level']
    )
    
    if success:
        await message.answer("✅ Ma'lumotlar saqlandi! Tahlil qilinmoqda...")
        
        # Get user's recent data for analysis
        recent_data = await get_user_health_data(user_data['user_id'], 30)
        
        # Generate analysis and recommendations
        analysis = await analyze_health_data(recent_data)
        recommendations = await generate_recommendations(recent_data, user_data)
        
        # Send analysis results
        response = "📊 **Bugungi tahlil:**\n\n"
        response += analysis + "\n\n"
        response += "💡 **Tavsiyalar:**\n\n" 
        response += recommendations
        
        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("❌ Ma'lumotlarni saqlashda xatolik yuz berdi.")
    
    # Clean up
    if message.from_user.id in user_temp_data:
        del user_temp_data[message.from_user.id]
    await state.clear()

@router.message(Command("stats"))
async def stats_command(message: Message):
    """Show user statistics"""
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("Avval ro'yxatdan o'ting. /start buyrug'ini ishlating.")
        return
    
    recent_data = await get_user_health_data(user['id'], 7)
    
    if not recent_data:
        await message.answer("Hali ma'lumotlar yo'q. /today buyrug'i bilan ma'lumot kiriting.")
        return
    
    # Calculate averages
    avg_sleep = sum(d['sleep_time'] for d in recent_data) / len(recent_data)
    avg_activity = sum(d['activity_time'] for d in recent_data) / len(recent_data)
    avg_mood = sum(d['mood_level'] for d in recent_data) / len(recent_data)
    avg_aggression = sum(d['aggression_level'] for d in recent_data) / len(recent_data)
    
    stats_message = f"""
📈 **So'nggi {len(recent_data)} kunlik statistika:**

🛏 O'rtacha uyqu: {avg_sleep:.1f} soat
🏃‍♂️ O'rtacha faollik: {avg_activity:.1f} soat  
😊 O'rtacha kayfiyat: {avg_mood:.1f}/5
😤 O'rtacha agressiya: {avg_aggression:.1f}/3

Jami kirdirilgan kunlar: {len(recent_data)}
"""
    
    await message.answer(stats_message, parse_mode="Markdown")

@router.message(Command("help"))
async def help_command(message: Message):
    """Show help information"""
    help_text = """
🤖 **HealthTracker Bot yordam**

**Buyruqlar:**
/start - Botni ishga tushirish va ro'yxatdan o'tish
/today - Bugungi ma'lumotlarni kiritish (21:00 dan keyin)
/stats - So'nggi 7 kunlik statistika
/help - Bu yordam xabari

**Bot qanday ishlaydi:**
1. Har kuni soat 21:00 da eslatma yuboramiz
2. Siz 4 ta ma'lumot kiritasiz: uyqu, faollik, agressiya, kayfiyat
3. Bot AI yordamida tahlil qiladi va maslahat beradi

**Texnik yordam:** @YourSupportUsername
    """
    await message.answer(help_text, parse_mode="Markdown")

def register_handlers(dp):
    """Register all handlers with the dispatcher"""
    dp.include_router(router)
    logger.info("All handlers registered successfully")
