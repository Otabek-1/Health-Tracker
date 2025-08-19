"""
Data models for Health Tracker Bot
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

@dataclass
class User:
    """User data model"""
    id: Optional[int] = None
    telegram_id: int = 0
    full_name: str = ""
    age: int = 0
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert user object to dictionary"""
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "full_name": self.full_name,
            "age": self.age,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user object from dictionary"""
        user = cls(
            id=data.get("id"),
            telegram_id=data.get("telegram_id", 0),
            full_name=data.get("full_name", ""),
            age=data.get("age", 0)
        )
        
        if data.get("created_at"):
            try:
                user.created_at = datetime.fromisoformat(data["created_at"])
            except ValueError:
                logger.warning(f"Invalid created_at format: {data['created_at']}")
        
        return user

@dataclass
class HealthData:
    """Health data model for daily tracking"""
    id: Optional[int] = None
    user_id: int = 0
    date: str = ""
    sleep_time: float = 0.0
    activity_time: float = 0.0
    aggression_level: int = 1
    mood_level: int = 3
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Validate data ranges
        self.sleep_time = max(0, min(24, self.sleep_time))
        self.activity_time = max(0, min(24, self.activity_time))
        self.aggression_level = max(1, min(3, self.aggression_level))
        self.mood_level = max(1, min(5, self.mood_level))
    
    def to_dict(self) -> dict:
        """Convert health data object to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date,
            "sleep_time": self.sleep_time,
            "activity_time": self.activity_time,
            "aggression_level": self.aggression_level,
            "mood_level": self.mood_level,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HealthData':
        """Create health data object from dictionary"""
        health_data = cls(
            id=data.get("id"),
            user_id=data.get("user_id", 0),
            date=data.get("date", ""),
            sleep_time=float(data.get("sleep_time", 0)),
            activity_time=float(data.get("activity_time", 0)),
            aggression_level=int(data.get("aggression_level", 1)),
            mood_level=int(data.get("mood_level", 3))
        )
        
        if data.get("created_at"):
            try:
                health_data.created_at = datetime.fromisoformat(data["created_at"])
            except ValueError:
                logger.warning(f"Invalid created_at format: {data['created_at']}")
        
        return health_data
    
    def get_sleep_status(self) -> str:
        """Get sleep status description"""
        if self.sleep_time >= 8:
            return "Yaxshi"
        elif self.sleep_time >= 6:
            return "Qoniqarli"
        else:
            return "Kam"
    
    def get_activity_status(self) -> str:
        """Get activity status description"""
        if self.activity_time >= 1.5:
            return "Yaxshi"
        elif self.activity_time >= 0.5:
            return "O'rtacha"
        else:
            return "Kam"
    
    def get_mood_description(self) -> str:
        """Get mood description"""
        mood_descriptions = {
            1: "Juda yomon",
            2: "Yomon", 
            3: "Normal",
            4: "Yaxshi",
            5: "Ajoyib"
        }
        return mood_descriptions.get(self.mood_level, "Noma'lum")
    
    def get_aggression_description(self) -> str:
        """Get aggression level description"""
        aggression_descriptions = {
            1: "Past",
            2: "O'rtacha",
            3: "Yuqori"
        }
        return aggression_descriptions.get(self.aggression_level, "Noma'lum")

@dataclass
class HealthAnalysis:
    """Health analysis result model"""
    user_id: int
    analysis_date: str
    overall_score: float = 0.0
    sleep_analysis: str = ""
    activity_analysis: str = ""
    mood_analysis: str = ""
    aggression_analysis: str = ""
    correlations: str = ""
    recommendations: List[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert analysis object to dictionary"""
        return {
            "user_id": self.user_id,
            "analysis_date": self.analysis_date,
            "overall_score": self.overall_score,
            "sleep_analysis": self.sleep_analysis,
            "activity_analysis": self.activity_analysis,
            "mood_analysis": self.mood_analysis,
            "aggression_analysis": self.aggression_analysis,
            "correlations": self.correlations,
            "recommendations": self.recommendations,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HealthAnalysis':
        """Create analysis object from dictionary"""
        analysis = cls(
            user_id=data.get("user_id", 0),
            analysis_date=data.get("analysis_date", ""),
            overall_score=float(data.get("overall_score", 0)),
            sleep_analysis=data.get("sleep_analysis", ""),
            activity_analysis=data.get("activity_analysis", ""),
            mood_analysis=data.get("mood_analysis", ""),
            aggression_analysis=data.get("aggression_analysis", ""),
            correlations=data.get("correlations", ""),
            recommendations=data.get("recommendations", [])
        )
        
        if data.get("created_at"):
            try:
                analysis.created_at = datetime.fromisoformat(data["created_at"])
            except ValueError:
                logger.warning(f"Invalid created_at format: {data['created_at']}")
        
        return analysis
    
    def calculate_overall_score(self, health_data: HealthData) -> float:
        """Calculate overall health score based on metrics"""
        # Sleep score (0-25 points)
        if health_data.sleep_time >= 7.5:
            sleep_score = 25
        elif health_data.sleep_time >= 6:
            sleep_score = 15
        else:
            sleep_score = 5
        
        # Activity score (0-25 points)
        if health_data.activity_time >= 1.5:
            activity_score = 25
        elif health_data.activity_time >= 0.5:
            activity_score = 15
        else:
            activity_score = 5
        
        # Mood score (0-25 points)
        mood_score = (health_data.mood_level / 5) * 25
        
        # Aggression score (0-25 points, inverted)
        aggression_score = ((4 - health_data.aggression_level) / 3) * 25
        
        self.overall_score = sleep_score + activity_score + mood_score + aggression_score
        return self.overall_score
    
    def get_score_description(self) -> str:
        """Get description of overall score"""
        if self.overall_score >= 80:
            return "Ajoyib! Sog'ligingiz juda yaxshi holatda."
        elif self.overall_score >= 60:
            return "Yaxshi! Sog'ligingiz qoniqarli darajada."
        elif self.overall_score >= 40:
            return "O'rtacha. Ba'zi joylarni yaxshilash kerak."
        else:
            return "E'tiborli! Sog'ligingizga ko'proq g'amxo'rlik qiling."

@dataclass
class UserSession:
    """User session model for tracking input state"""
    telegram_id: int
    current_state: str = ""
    temp_data: dict = None
    last_activity: Optional[datetime] = None
    
    def __post_init__(self):
        if self.temp_data is None:
            self.temp_data = {}
        if self.last_activity is None:
            self.last_activity = datetime.now()
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def clear_temp_data(self):
        """Clear temporary data"""
        self.temp_data = {}
        self.current_state = ""
        self.update_activity()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session is expired"""
        if self.last_activity is None:
            return True
        
        time_diff = datetime.now() - self.last_activity
        return time_diff.total_seconds() > (timeout_minutes * 60)

# Health metrics validation functions
def validate_sleep_time(sleep_time: str) -> tuple[bool, float]:
    """Validate sleep time input"""
    try:
        value = float(sleep_time)
        if 0 <= value <= 24:
            return True, value
        else:
            return False, 0.0
    except ValueError:
        return False, 0.0

def validate_activity_time(activity_time: str) -> tuple[bool, float]:
    """Validate activity time input"""
    try:
        value = float(activity_time)
        if 0 <= value <= 24:
            return True, value
        else:
            return False, 0.0
    except ValueError:
        return False, 0.0

def validate_age(age: str) -> tuple[bool, int]:
    """Validate age input"""
    try:
        value = int(age)
        if 1 <= value <= 120:
            return True, value
        else:
            return False, 0
    except ValueError:
        return False, 0

# Constants for health metrics
OPTIMAL_SLEEP_HOURS = 8.0
MIN_SLEEP_HOURS = 6.0
OPTIMAL_ACTIVITY_HOURS = 1.5
MIN_ACTIVITY_HOURS = 0.5

# Mood and aggression mapping
MOOD_EMOJIS = ["😡", "😐", "🙂", "😃", "🤩"]
AGGRESSION_LEVELS = ["Past", "O'rtacha", "Baland"]

def get_health_recommendations(health_data: HealthData) -> List[str]:
    """Generate health recommendations based on data"""
    recommendations = []
    
    # Sleep recommendations
    if health_data.sleep_time < MIN_SLEEP_HOURS:
        recommendations.append("🛏 Kamida 6-8 soat uxlashga harakat qiling.")
    elif health_data.sleep_time > 10:
        recommendations.append("🛏 Haddan tashqari uyqu ham foydali emas, 7-8 soat yetarli.")
    
    # Activity recommendations
    if health_data.activity_time < MIN_ACTIVITY_HOURS:
        recommendations.append("🏃‍♂️ Kuniga kamida 30 daqiqa jismoniy mashq qiling.")
    
    # Mood recommendations
    if health_data.mood_level <= 2:
        recommendations.append("😊 Kayfiyatni yaxshilash uchun: do'stlar bilan vaqt o'tkazing, sevimli mashg'ulot bilan shug'ullaning.")
    
    # Aggression recommendations
    if health_data.aggression_level >= 3:
        recommendations.append("😤 Stressni kamaytirish uchun: meditatsiya, chuqur nafas olish, yengil mashqlar.")
    
    return recommendations

logger.info("Health Tracker models loaded successfully")
