"""
Database module for Health Tracker Bot
Handles all data persistence operations
"""

import sqlite3
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class Database:
    """Database handler for health tracking data"""
    
    def __init__(self, db_path: str = "health_tracker.db"):
        """Initialize database with proper schema"""
        self.db_path = db_path
        self._init_database()
        logger.info(f"Database initialized at {db_path}")
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    timezone TEXT DEFAULT 'UTC'
                )
            """)
            
            # Health records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS health_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    record_type TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT,
                    notes TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_for DATE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id INTEGER PRIMARY KEY,
                    reminder_enabled BOOLEAN DEFAULT TRUE,
                    reminder_time TEXT DEFAULT '20:00',
                    weight_unit TEXT DEFAULT 'kg',
                    height_cm INTEGER,
                    age INTEGER,
                    gender TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_health_records_user_date 
                ON health_records (user_id, date_for)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_health_records_type 
                ON health_records (record_type)
            """)
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def register_user(self, user_id: int, username: str = None, 
                     first_name: str = None, last_name: str = None) -> bool:
        """Register a new user or update existing user info"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_name) 
                    VALUES (?, ?, ?, ?)
                """, (user_id, username, first_name, last_name))
                
                # Create default preferences
                cursor.execute("""
                    INSERT OR IGNORE INTO user_preferences (user_id) 
                    VALUES (?)
                """, (user_id,))
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error registering user {user_id}: {e}")
            return False
    
    def record_health_data(self, user_id: int, record_type: str, value: float,
                          unit: str = None, notes: str = None, date_for: date = None) -> bool:
        """Record health data for a user"""
        if date_for is None:
            date_for = date.today()
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO health_records 
                    (user_id, record_type, value, unit, notes, date_for)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, record_type, value, unit, notes, date_for))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error recording health data for user {user_id}: {e}")
            return False
    
    def get_user_records(self, user_id: int, record_type: str = None, 
                        days: int = 30) -> List[Dict[str, Any]]:
        """Get health records for a user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                if record_type:
                    query = """
                        SELECT * FROM health_records 
                        WHERE user_id = ? AND record_type = ? 
                        AND date_for >= date('now', '-{} days')
                        ORDER BY date_for DESC, recorded_at DESC
                    """.format(days)
                    cursor.execute(query, (user_id, record_type))
                else:
                    query = """
                        SELECT * FROM health_records 
                        WHERE user_id = ? 
                        AND date_for >= date('now', '-{} days')
                        ORDER BY date_for DESC, recorded_at DESC
                    """.format(days)
                    cursor.execute(query, (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting user records: {e}")
            return []
    
    def get_daily_summary(self, user_id: int, target_date: date = None) -> Dict[str, Any]:
        """Get daily summary of health data"""
        if target_date is None:
            target_date = date.today()
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT record_type, value, unit, notes, recorded_at
                    FROM health_records 
                    WHERE user_id = ? AND date_for = ?
                    ORDER BY recorded_at DESC
                """, (user_id, target_date))
                
                records = cursor.fetchall()
                summary = {}
                
                for record in records:
                    record_type = record['record_type']
                    if record_type not in summary:
                        summary[record_type] = {
                            'value': record['value'],
                            'unit': record['unit'],
                            'notes': record['notes'],
                            'recorded_at': record['recorded_at']
                        }
                
                return summary
        except Exception as e:
            logger.error(f"Error getting daily summary: {e}")
            return {}
    
    def update_user_preferences(self, user_id: int, **preferences) -> bool:
        """Update user preferences"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                valid_fields = ['reminder_enabled', 'reminder_time', 'weight_unit', 
                               'height_cm', 'age', 'gender']
                
                updates = []
                values = []
                
                for field, value in preferences.items():
                    if field in valid_fields:
                        updates.append(f"{field} = ?")
                        values.append(value)
                
                if updates:
                    query = f"UPDATE user_preferences SET {', '.join(updates)} WHERE user_id = ?"
                    values.append(user_id)
                    cursor.execute(query, values)
                    conn.commit()
                    return True
                
                return False
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM user_preferences WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                return dict(row) if row else {}
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {}
    
    def get_stats(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get health statistics for a user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get record counts by type
                cursor.execute("""
                    SELECT record_type, COUNT(*) as count, AVG(value) as avg_value
                    FROM health_records 
                    WHERE user_id = ? AND date_for >= date('now', '-{} days')
                    GROUP BY record_type
                """.format(days), (user_id,))
                
                stats = {}
                for row in cursor.fetchall():
                    stats[row['record_type']] = {
                        'count': row['count'],
                        'average': round(row['avg_value'], 2) if row['avg_value'] else 0
                    }
                
                # Get total records
                cursor.execute("""
                    SELECT COUNT(*) as total_records 
                    FROM health_records 
                    WHERE user_id = ? AND date_for >= date('now', '-{} days')
                """.format(days), (user_id,))
                
                total = cursor.fetchone()['total_records']
                stats['total_records'] = total
                stats['days_period'] = days
                
                return stats
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
