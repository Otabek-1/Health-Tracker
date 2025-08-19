"""
Configuration settings for Health Tracker Bot
"""

import os
from pathlib import Path

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "6632372434:AAFx3RVs66F7IZdJfVk7_NyZi15THnjblcg")

# Database Configuration
DATABASE_PATH = "HealtTracker.db"

# Reminder Configuration
REMINDER_TIME = "21:00"  # Daily reminder time
TIMEZONE = "Asia/Tashkent"  # Default timezone for Uzbekistan (UTC+5)
DEFAULT_TIMEZONE_OFFSET = 5  # Default UTC offset in hours

# ML Model Configuration
MIN_DATA_POINTS = 3  # Minimum data points required for analysis

# Message Templates
WELCOME_MESSAGE = """
🌟 Salom! HealthTracker botiga xush kelibsiz!

Bu bot sizning kunlik sog'ligingizni kuzatadi va AI yordamida tahlil qiladi.

Quyidagi ma'lumotlarni har kuni kiritishingiz kerak:
🛏 Uyqu vaqti
🏃‍♂️ Jismoniy faollik vaqti  
😤 Agressiya darajasi
😊 Kayfiyat darajasi

Har kuni soat 21:00 da eslatma yuboramiz!

Boshlash uchun ismingizni kiriting:
"""

START_MONITORING_MESSAGE = """
✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!

Endi har kuni soat 21:00 dan keyin kunlik ma'lumotlaringizni kiritishingiz mumkin.

Bugun ma'lumot kiritish uchun /today buyrug'ini ishlating.
"""

# Data Collection States
class UserStates:
    WAITING_NAME = "waiting_name"
    WAITING_AGE = "waiting_age"
    WAITING_SLEEP = "waiting_sleep"
    WAITING_ACTIVITY = "waiting_activity"
    WAITING_AGGRESSION = "waiting_aggression"
    WAITING_MOOD = "waiting_mood"
    COMPLETED = "completed"

# Mood and Aggression Scales
MOOD_SCALE = {
    "😡": 1,
    "😐": 2, 
    "🙂": 3,
    "😃": 4,
    "🤩": 5
}

AGGRESSION_SCALE = {
    "Past": 1,
    "O'rtacha": 2,
    "Baland": 3
}
