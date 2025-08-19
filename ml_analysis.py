"""
Machine Learning analysis and recommendations for health data
"""

import logging
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

async def analyze_health_data(recent_data: List[Dict]) -> str:
    """
    Analyze user's recent health data and provide insights
    """
    if len(recent_data) < 2:
        return "Tahlil uchun kam ma'lumot. Yana bir necha kun ma'lumot kiriting."
    
    # Get today's data (first item since data is ordered DESC)
    today = recent_data[0]
    
    analysis_parts = []
    
    # Sleep analysis
    sleep_analysis = analyze_sleep_pattern(recent_data)
    analysis_parts.append(f"🛏 **Uyqu:** {sleep_analysis}")
    
    # Activity analysis
    activity_analysis = analyze_activity_pattern(recent_data)
    analysis_parts.append(f"🏃‍♂️ **Faollik:** {activity_analysis}")
    
    # Mood analysis
    mood_analysis = analyze_mood_pattern(recent_data)
    analysis_parts.append(f"😊 **Kayfiyat:** {mood_analysis}")
    
    # Aggression analysis
    aggression_analysis = analyze_aggression_pattern(recent_data)
    analysis_parts.append(f"😤 **Agressiya:** {aggression_analysis}")
    
    # Overall correlation analysis
    correlation_analysis = analyze_correlations(recent_data)
    if correlation_analysis:
        analysis_parts.append(f"🔍 **Bog'liqlik:** {correlation_analysis}")
    
    return "\n\n".join(analysis_parts)

def analyze_sleep_pattern(data: List[Dict]) -> str:
    """Analyze sleep patterns"""
    sleep_times = [d['sleep_time'] for d in data]
    avg_sleep = sum(sleep_times) / len(sleep_times)
    today_sleep = sleep_times[0]
    
    if today_sleep >= 7.5:
        sleep_status = "yaxshi"
    elif today_sleep >= 6:
        sleep_status = "qoniqarli"
    else:
        sleep_status = "kam"
    
    trend = ""
    if len(data) >= 3:
        recent_avg = sum(sleep_times[:3]) / 3
        if recent_avg > avg_sleep + 0.5:
            trend = " So'nggi kunlarda uyqu vaqti yaxshilandi."
        elif recent_avg < avg_sleep - 0.5:
            trend = " So'nggi kunlarda uyqu vaqti kamaydi."
    
    return f"Bugun {today_sleep} soat uxladingiz ({sleep_status}). O'rtacha: {avg_sleep:.1f} soat.{trend}"

def analyze_activity_pattern(data: List[Dict]) -> str:
    """Analyze physical activity patterns"""
    activity_times = [d['activity_time'] for d in data]
    avg_activity = sum(activity_times) / len(activity_times)
    today_activity = activity_times[0]
    
    if today_activity >= 1.5:
        activity_status = "yaxshi"
    elif today_activity >= 0.5:
        activity_status = "o'rtacha"
    else:
        activity_status = "kam"
    
    comparison = ""
    if today_activity > avg_activity:
        comparison = f" Bu odatdagidan {today_activity - avg_activity:.1f} soat ko'p."
    elif today_activity < avg_activity:
        comparison = f" Bu odatdagidan {avg_activity - today_activity:.1f} soat kam."
    
    return f"Bugun {today_activity} soat faol bo'ldingiz ({activity_status}).{comparison}"

def analyze_mood_pattern(data: List[Dict]) -> str:
    """Analyze mood patterns"""
    mood_levels = [d['mood_level'] for d in data]
    avg_mood = sum(mood_levels) / len(mood_levels)
    today_mood = mood_levels[0]
    
    mood_names = {1: "juda yomon", 2: "yomon", 3: "normal", 4: "yaxshi", 5: "ajoyib"}
    
    trend = ""
    if len(data) >= 3:
        if mood_levels[0] > mood_levels[1] > mood_levels[2]:
            trend = " Kayfiyat tobora yaxshilanmoqda!"
        elif mood_levels[0] < mood_levels[1] < mood_levels[2]:
            trend = " Kayfiyat pasayib bormoqda, e'tibor bering."
    
    return f"Bugungi kayfiyat: {mood_names[today_mood]} ({today_mood}/5). O'rtacha: {avg_mood:.1f}/5.{trend}"

def analyze_aggression_pattern(data: List[Dict]) -> str:
    """Analyze aggression patterns"""
    aggression_levels = [d['aggression_level'] for d in data]
    avg_aggression = sum(aggression_levels) / len(aggression_levels)
    today_aggression = aggression_levels[0]
    
    aggression_names = {1: "past", 2: "o'rtacha", 3: "yuqori"}
    
    if today_aggression <= avg_aggression:
        comparison = "Bu odatdagi darajada yoki undan kam."
    else:
        comparison = "Bu odatdagidan yuqori, sabablarini tahlil qiling."
    
    return f"Bugungi agressiya: {aggression_names[today_aggression]} ({today_aggression}/3). {comparison}"

def analyze_correlations(data: List[Dict]) -> str:
    """Analyze correlations between different health metrics"""
    if len(data) < 5:
        return ""
    
    insights = []
    
    # Sleep-Mood correlation
    sleep_mood_corr = calculate_correlation([d['sleep_time'] for d in data], 
                                          [d['mood_level'] for d in data])
    if abs(sleep_mood_corr) > 0.6:
        if sleep_mood_corr > 0:
            insights.append("Ko'p uxlagan kunlarda kayfiyatingiz yaxshi bo'ladi.")
        else:
            insights.append("Uyqu va kayfiyat o'rtasida teskari bog'liqlik bor.")
    
    # Activity-Mood correlation
    activity_mood_corr = calculate_correlation([d['activity_time'] for d in data],
                                             [d['mood_level'] for d in data])
    if abs(activity_mood_corr) > 0.6:
        if activity_mood_corr > 0:
            insights.append("Faol bo'lgan kunlarda kayfiyatingiz yaxshi.")
        else:
            insights.append("Jismoniy faollik kayfiyatingizga salbiy ta'sir qilayotganga o'xshaydi.")
    
    # Sleep-Aggression correlation
    sleep_aggr_corr = calculate_correlation([d['sleep_time'] for d in data],
                                          [d['aggression_level'] for d in data])
    if abs(sleep_aggr_corr) > 0.6:
        if sleep_aggr_corr < 0:
            insights.append("Kam uxlagan kunlarda agressivroq bo'lasiz.")
    
    return " ".join(insights) if insights else ""

def calculate_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    try:
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    except:
        return 0

async def generate_recommendations(recent_data: List[Dict], today_data: Dict) -> str:
    """
    Generate personalized recommendations based on health data
    """
    recommendations = []
    
    # Sleep recommendations
    if today_data['sleep_time'] < 7:
        recommendations.append("🛏 Ertaga kamida 7-8 soat uxlashga harakat qiling. Yaxshi uyqu kayfiyatni yaxshilaydi.")
    elif today_data['sleep_time'] > 9:
        recommendations.append("🛏 Juda ko'p uxlash ham yomon. 7-8 soat uxlash optimal.")
    
    # Activity recommendations  
    if today_data['activity_time'] < 0.5:
        recommendations.append("🏃‍♂️ Ertaga kamida 30 daqiqa jismoniy mashq qiling. Yurish ham yetarli.")
    elif today_data['activity_time'] < 1:
        recommendations.append("🏃‍♂️ Jismoniy faolligingizni oshiring. Kuniga 1 soat faollik ideal.")
    
    # Mood recommendations
    if today_data['mood_level'] <= 2:
        recommendations.append("😊 Kayfiyat pastligini bartaraf etish uchun: do'stlar bilan suhbat, qiziqarli faoliyat, tabiatda yurish.")
        
        # Check sleep correlation
        if today_data['sleep_time'] < 7:
            recommendations.append("😴 Kam uyqu kayfiyatga salbiy ta'sir qilishi mumkin.")
    
    # Aggression recommendations
    if today_data['aggression_level'] >= 3:
        recommendations.append("😤 Agressiyani kamaytirishga yordam beradi: chuqur nafas olish, meditatsiya, jismoniy mashqlar.")
        
        # Check recent pattern
        if len(recent_data) >= 3:
            recent_aggression = [d['aggression_level'] for d in recent_data[:3]]
            if all(level >= 2 for level in recent_aggression):
                recommendations.append("⚠️ So'nggi kunlarda agressiya yuqori. Stress manbalarini aniqlashga harakat qiling.")
    
    # Weekly pattern recommendations
    if len(recent_data) >= 7:
        weekly_recommendations = analyze_weekly_patterns(recent_data)
        recommendations.extend(weekly_recommendations)
    
    # General health tips
    recommendations.append("💡 Muntazam rejim: bir xil vaqtda uxlash va turish, muntazam ovqatlanish.")
    recommendations.append("🥗 Sog'lom ovqatlanish: ko'proq meva-sabzavot, kam qayta ishlangan mahsulotlar.")
    
    return "\n\n".join(recommendations)

def analyze_weekly_patterns(data: List[Dict]) -> List[str]:
    """Analyze weekly patterns and provide insights"""
    recommendations = []
    
    # Check consistency
    sleep_times = [d['sleep_time'] for d in data[:7]]
    sleep_std = np.std(sleep_times) if len(sleep_times) > 1 else 0
    
    if sleep_std > 2:
        recommendations.append("📅 Uyqu rejimi notekis. Muntazam uyqu grafigini shakllantiring.")
    
    # Check weekend patterns (assuming last entry is most recent)
    # This is a simplified approach - in real implementation, you'd use actual date checking
    if len(data) >= 7:
        weekday_mood = sum(d['mood_level'] for d in data[2:7]) / 5  # Mon-Fri approximation
        weekend_mood = sum(d['mood_level'] for d in data[:2]) / 2   # Sat-Sun approximation
        
        if weekend_mood > weekday_mood + 0.5:
            recommendations.append("📊 Dam olish kunlari kayfiyatingiz yaxshi. Ish kunlarida ham faolroq bo'ling.")
    
    return recommendations
