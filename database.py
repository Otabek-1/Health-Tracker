"""
Database operations for Health Tracker Bot
"""

import aiosqlite
import logging
from datetime import datetime
from typing import Optional, List, Tuple
from config import DATABASE_PATH

logger = logging.getLogger(__name__)

async def init_database():
    """Initialize SQLite database with required tables"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Create users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create health_data table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS health_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                sleep_time REAL NOT NULL,
                activity_time REAL NOT NULL,
                aggression_level INTEGER NOT NULL,
                mood_level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, date)
            )
        """)
        
        await db.commit()
        logger.info("Database tables created successfully")

async def create_user(telegram_id: int, full_name: str, age: int) -> bool:
    """Create a new user in the database"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute(
                "INSERT INTO users (telegram_id, full_name, age) VALUES (?, ?, ?)",
                (telegram_id, full_name, age)
            )
            await db.commit()
            logger.info(f"User created: {telegram_id}")
            return True
    except aiosqlite.IntegrityError:
        logger.warning(f"User already exists: {telegram_id}")
        return False
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return False

async def get_user(telegram_id: int) -> Optional[dict]:
    """Get user information by telegram_id"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT id, telegram_id, full_name, age FROM users WHERE telegram_id = ?",
                (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "telegram_id": row[1],
                        "full_name": row[2],
                        "age": row[3]
                    }
        return None
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        return None

async def save_health_data(user_id: int, date: str, sleep_time: float, 
                          activity_time: float, aggression_level: int, mood_level: int) -> bool:
    """Save daily health data for a user"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            await db.execute("""
                INSERT OR REPLACE INTO health_data 
                (user_id, date, sleep_time, activity_time, aggression_level, mood_level)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, date, sleep_time, activity_time, aggression_level, mood_level))
            await db.commit()
            logger.info(f"Health data saved for user {user_id} on {date}")
            return True
    except Exception as e:
        logger.error(f"Error saving health data: {e}")
        return False

async def get_user_health_data(user_id: int, limit: int = 30) -> List[dict]:
    """Get recent health data for a user"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute("""
                SELECT date, sleep_time, activity_time, aggression_level, mood_level, created_at
                FROM health_data 
                WHERE user_id = ?
                ORDER BY date DESC
                LIMIT ?
            """, (user_id, limit)) as cursor:
                rows = await cursor.fetchall()
                return [
                    {
                        "date": row[0],
                        "sleep_time": row[1],
                        "activity_time": row[2],
                        "aggression_level": row[3],
                        "mood_level": row[4],
                        "created_at": row[5]
                    }
                    for row in rows
                ]
    except Exception as e:
        logger.error(f"Error getting health data: {e}")
        return []

async def check_today_data_exists(user_id: int, date: str) -> bool:
    """Check if user has already submitted data for today"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT COUNT(*) FROM health_data WHERE user_id = ? AND date = ?",
                (user_id, date)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] > 0
    except Exception as e:
        logger.error(f"Error checking today's data: {e}")
        return False

async def get_all_users() -> List[dict]:
    """Get all users for sending reminders"""
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute(
                "SELECT id, telegram_id, full_name FROM users"
            ) as cursor:
                rows = await cursor.fetchall()
                return [
                    {
                        "id": row[0],
                        "telegram_id": row[1],
                        "full_name": row[2]
                    }
                    for row in rows
                ]
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []
