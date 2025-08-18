import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from datetime import datetime
from dbmanager import DBManager
from models import Analyzer

db = DBManager(connection="sqlite", dbname="HealtTracker")

# Har bir user uchun state dict
user_monitoring_dict = {}

db.create_table("users")
db.add_col("users", "id").integer().primary_key().commit()
db.add_col("users", "telegram_id").integer().commit()
db.add_col("users", "full_name").text().commit()
db.add_col("users", "age").integer().commit()

TOKEN = "6632372434:AAFx3RVs66F7IZdJfVk7_NyZi15THnjblcg"
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def analyze(user_dict):
    """
    user_dict: {telegram_id: {"monitoring_time": True/False, "data": [...], "agression": ..., "mood": ...}}
    """
    for user_id, info in user_dict.items():
        if not info.get("monitoring_time", False) and "data" in info and len(info["data"]) >= 4:
            sleep_time = info["data"][1]
            action_time = info["data"][2]
            agression = info.get("agression", "normal")
            mood = info.get("mood", 3)
            analyzer = Analyzer(
                telegram_id=user_id,
                sleep_time=sleep_time,
                action_time=action_time,
                agression=agression,
                mood=mood
            )
            await bot.send_message(user_id, analyzer.get_conclusion(), parse_mode="HTML")
            # Clear data after analysis
            info["data"] = []


def check_time():
    hour = datetime.now().hour
    minute = datetime.now().minute
    return (21 <= hour <= 23) or (hour == 0 and minute == 0)


async def send_reminder(bot, db):
    if check_time():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Boshlash", callback_data="start_monitoring")],
                [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_monitoring")]
            ]
        )
        users = db.get_table("users")
        if not users:
            print("❌ users jadvalidan ma'lumot olinmadi")
            return

        for user in users[:]:
            await bot.send_message(user[2], "Xayrli kech! Kunlik monitoring vaqti!", reply_markup=keyboard)
            users.remove(user)


@dp.callback_query(lambda c: c.data == "start_monitoring")
async def start_monitoring(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("Ajoyib! Unda boshlaymiz!")
    await callback.message.answer(
        "Kun hisobida umumiy uyqu vaqtingiz va jismoniy harakat vaqtingizni yozing "
        "(soatlarda, bo'sh joy bilan ajratgan holda):"
    )

    # Foydalanuvchi state yaratish yoki yangilash
    state = user_monitoring_dict.setdefault(user_id, {
        "input_age": False,
        "input_name": False,
        "monitoring_time": False,
        "data": [],
        "agression": None,
        "mood": None
    })
    state["monitoring_time"] = True
    state["data"] = [user_id]  # telegram_id birinchi element


@dp.callback_query(lambda c: c.data == "cancel_monitoring")
async def cancel_monitoring(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Monitoring bekor qilindi.")
    user_id = callback.from_user.id
    if user_id in user_monitoring_dict:
        user_monitoring_dict[user_id]["monitoring_time"] = False
        user_monitoring_dict[user_id]["data"] = []


@dp.callback_query(lambda c: c.data.startswith("ag_"))
async def handle_aggression(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ag_value = callback.data[3:]  # low / normal / high
    state = user_monitoring_dict.get(user_id)
    if state and state.get("monitoring_time"):
        state["agression"] = ag_value
        state["data"].append(ag_value)

    # Kayfiyat inline keyboard
    keyboard_mood = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="😡", callback_data="mood_1"),
            InlineKeyboardButton(text="😐", callback_data="mood_2"),
            InlineKeyboardButton(text="🙂", callback_data="mood_3"),
            InlineKeyboardButton(text="😃", callback_data="mood_4"),
            InlineKeyboardButton(text="🤩", callback_data="mood_5")
        ]]
    )
    await callback.message.answer("Endi kayfiyat darajangizni tanlang:", reply_markup=keyboard_mood)


@dp.callback_query(lambda c: c.data.startswith("mood_"))
async def handle_mood(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    mood_value = int(callback.data[5:])
    state = user_monitoring_dict.get(user_id)
    if state and state.get("monitoring_time"):
        state["mood"] = mood_value
        state["data"].append(mood_value)

        # Analyzer uchun dictdagi ma’lumotlarni yuborish
        analyzer = Analyzer(
            telegram_id=user_id,
            sleep_time=state["data"][1],
            action_time=state["data"][2],
            agression=state["agression"],
            mood=state["mood"]
        )
        await bot.send_message(user_id, analyzer.get_conclusion(), parse_mode="HTML")

        # Monitoringni tugatish
        state["monitoring_time"] = False
        state["data"] = []


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user = message.from_user
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Sozlamalar")],
            [KeyboardButton(text="Bot haqida")]
        ],
        resize_keyboard=True
    )

    exists = db.filter("users", f"telegram_id = {user.id}")
    state = user_monitoring_dict.setdefault(user.id, {
        "input_age": False,
        "input_name": False,
        "monitoring_time": False,
        "data": [],
        "agression": None,
        "mood": None
    })

    if not exists:
        await message.answer(
            "👋 Assalomu alaykum!\n\n"
            "<b>Health Tracker</b> botiga xush kelibsiz! 🌿\n\n"
            "Bu yerda siz har kungi <i>uyqu, mashq va kayfiyat</i> haqida "
            "ma'lumotlaringizni yozib borasiz. Bot esa sizga oddiy "
            "tahlillar va foydali maslahatlarni beradi. 📊✨\n\n"
            "🔧 Ma'lumotlaringizni keyinchalik <b>Sozlamalar</b> bo'limidan "
            "o'zgartirishingiz mumkin.\n\n"
            "ℹ️ Batafsil ma'lumotni <b>Bot haqida</b> bo'limida olasiz.\n\n"
            "Kunlik monitoring va analiz funksiyalari ro'yxatdan o'tgan yoki botni ishga tushirgan kundan 1 kun keyindan boshlanadi.\n\n"
            "Botni ishlatishni boshlashdan oldin yoshingizni kiriting:",
            parse_mode="HTML", reply_markup=keyboard
        )
        state["input_age"] = True
        db.insert_row("users", {"telegram_id": user.id, "full_name": user.full_name})
    else:
        age_exists = exists[0][4]
        if not age_exists:
            await message.answer(
                "Qayta xush kelibsiz! Botni ishlatishdan oldin yoshingizni kiriting: ",
                reply_markup=keyboard
            )
            state["input_age"] = True
        else:
            await message.answer(
                "Qayta xush kelibsiz!\n\nBotni ishlatishda davom etishingiz mumkin.",
                reply_markup=keyboard
            )


@dp.message()
async def message_handlers(message: types.Message):
    user_id = message.from_user.id
    state = user_monitoring_dict.setdefault(user_id, {
        "input_age": False,
        "input_name": False,
        "monitoring_time": False,
        "data": [],
        "agression": None,
        "mood": None
    })

    text = message.text
    user = message.from_user

    if state["input_age"]:
        try:
            age = int(text)
            db.update_row("users", {"age": age}, f"telegram_id = {user.id}")
            await message.answer(f"✅ Yoshingiz {age} deb qabul qilindi!")
            state["input_age"] = False
        except ValueError:
            await message.answer("❌ Iltimos, faqat son kiriting (masalan: 25).")
        return

    if state["input_name"]:
        db.update_row("users", {"full_name": text}, f"telegram_id = {user.id}")
        await message.answer("Ma'lumotlar o'zgartirildi!")
        state["input_name"] = False
        return

    if state["monitoring_time"]:
        try:
            sleep_hours, action_hours = map(int, text.split())
            state["data"].extend([sleep_hours, action_hours])
            # Step 2: agressiya
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Past", callback_data="ag_low")],
                    [InlineKeyboardButton(text="O'rtacha", callback_data="ag_normal")],
                    [InlineKeyboardButton(text="Baland", callback_data="ag_high")]
                ]
            )
            await message.answer(
                "Ajoyib! Endi bugungi kunlik agressiya darajangizni tanlang "
                "(kun bo'yi asabiy holatingiz qanday bo'ldi?)",
                reply_markup=keyboard
            )
        except ValueError:
            await message.answer("❌ Iltimos to'g'ri formatda yuboring (Masalan: 10 7).")
        return

    # Sozlamalar yoki bot haqida
    if text == "Sozlamalar":
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Ismni o'zgartirish")],
                [KeyboardButton(text="Yoshni o'zgartirish")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        user_info = db.filter("users", f"telegram_id = {user.id}")[0]
        await message.answer(
            "Sizning ma'lumotlaringiz:\n\n"
            f"<b>ID:</b> {user_info[0]}\n"
            f"<b>To'liq ism familya:</b> <i>{user_info[3]}</i>\n"
            f"<b>Yosh:</b> {user_info[4]}\n",
            parse_mode="HTML",
            reply_markup=keyboard
        )
    elif text == "Bot haqida":
        await message.answer(
            "<b>Health Tracker</b> — jismoniy va ruhiy holatingizni monitoring qilishga "
            "yordam beruvchi sun’iy intellekt asosidagi bot. 🌿📊\n\n"
            "<b>📌 Ishlatish qoidalari va yo‘riqnoma:</b>\n"
            "• Botdan foydalanish uchun yoshingizni kiritishingiz shart.\n"
            "• Har kuni soat <b>21:00</b> da kunlik <i>uyqu, mashq va kayfiyat</i> "
            "haqida ma’lumot kiritasiz va monitoring natijalarini olasiz.\n"
            "• Bot sizga avtomatik eslatadi. ⏰ 21:00 dan erta ma’lumot kiritish mumkin emas.\n"
            "• Kun davomida foydali maslahatlar, takliflar va e’lonlardan xabardor bo‘lib borasiz.\n\n"
            "👉 Botni to‘liq ishlatish uchun <b>/start</b> tugmasini bosing.",
            parse_mode="HTML"
        )
    elif text == "Ismni o'zgartirish":
        state["input_name"] = True
        await message.answer("Iltimos to'liq ism- familyangizni to'g'ri formatda yozing:")
    elif text == "Yoshni o'zgartirish":
        state["input_age"] = True
        await message.answer("Iltimos, yoshingizni to'g'ri formatda yozing:")


async def main():
    asyncio.create_task(send_reminder(bot, db))
    print("Bot ishga tushdi.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
