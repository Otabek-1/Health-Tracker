"""
Scheduler for daily reminders and automated tasks
"""

import asyncio
import logging
from datetime import datetime, time, timedelta
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNotFound

from database import get_all_users, check_today_data_exists
from config import REMINDER_TIME, DEFAULT_TIMEZONE_OFFSET

logger = logging.getLogger(__name__)

async def send_daily_reminder(bot: Bot, user_telegram_id: int, user_name: str, user_id: int):
    """Send daily reminder to a specific user"""
    try:
        # Use local time for date calculation
        utc_now = datetime.now()
        local_time = utc_now + timedelta(hours=DEFAULT_TIMEZONE_OFFSET)
        today_date = local_time.strftime("%Y-%m-%d")
        
        # Check if user already submitted data today
        data_exists = await check_today_data_exists(user_id, today_date)
        if data_exists:
            return  # Don't send reminder if data already exists
        
        reminder_message = f"""
🔔 **Kunlik eslatma!**

Salom {user_name}! Bugungi sog'lik ma'lumotlaringizni kiritish vaqti keldi.

Quyidagi ma'lumotlarni kiriting:
🛏 Uyqu vaqti
🏃‍♂️ Jismoniy faollik vaqti
😤 Agressiya darajasi
😊 Kayfiyat

Ma'lumot kiritish uchun /today buyrug'ini ishlating.
        """
        
        await bot.send_message(user_telegram_id, reminder_message, parse_mode="Markdown")
        logger.info(f"Reminder sent to user {user_telegram_id}")
        
    except TelegramForbiddenError:
        logger.warning(f"User {user_telegram_id} blocked the bot")
    except TelegramNotFound:
        logger.warning(f"User {user_telegram_id} not found")
    except Exception as e:
        logger.error(f"Error sending reminder to {user_telegram_id}: {e}")

async def daily_reminder_task(bot: Bot):
    """Task to send daily reminders to all users"""
    logger.info("Starting daily reminder task")
    
    try:
        users = await get_all_users()
        logger.info(f"Sending reminders to {len(users)} users")
        
        for user in users:
            await send_daily_reminder(
                bot, 
                user['telegram_id'], 
                user['full_name'], 
                user['id']
            )
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.1)
        
        logger.info("Daily reminders sent successfully")
    
    except Exception as e:
        logger.error(f"Error in daily reminder task: {e}")

async def schedule_daily_reminders(bot: Bot):
    """Schedule daily reminders at specified time"""
    while True:
        try:
            # Use local time for scheduling
            utc_now = datetime.now()
            local_now = utc_now + timedelta(hours=DEFAULT_TIMEZONE_OFFSET)
            target_time = time(21, 0)  # 21:00 local time
            
            # Calculate next reminder time in local timezone
            today_reminder_local = datetime.combine(local_now.date(), target_time)
            if local_now.time() > target_time:
                # If it's already past today's reminder time, schedule for tomorrow
                today_reminder_local += timedelta(days=1)
            
            # Convert back to UTC for scheduling
            today_reminder_utc = today_reminder_local - timedelta(hours=DEFAULT_TIMEZONE_OFFSET)
            
            # Calculate sleep duration
            sleep_seconds = (today_reminder_utc - utc_now).total_seconds()
            logger.info(f"Next reminder scheduled for: {today_reminder_local} local time ({today_reminder_utc} UTC)")
            
            # Sleep until reminder time
            await asyncio.sleep(sleep_seconds)
            
            # Send reminders
            await daily_reminder_task(bot)
            
            # Sleep a bit to avoid multiple executions in the same minute
            await asyncio.sleep(60)
            
        except Exception as e:
            logger.error(f"Error in reminder scheduler: {e}")
            # Wait 5 minutes before retrying
            await asyncio.sleep(300)

async def start_scheduler(bot: Bot):
    """Start the reminder scheduler"""
    logger.info("Starting reminder scheduler")
    
    # Create background task for daily reminders
    asyncio.create_task(schedule_daily_reminders(bot))
    
    logger.info("Reminder scheduler started successfully")
