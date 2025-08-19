"""
Message and command handlers for Health Tracker Bot
"""

import logging
import json
from datetime import datetime, date
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from database import Database

logger = logging.getLogger(__name__)

class HealthHandlers:
    """Handler class for all bot commands and messages"""
    
    def __init__(self, database: Database):
        self.db = database
        self.user_states = {}  # Track user conversation states
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        # Register user in database
        self.db.register_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        welcome_text = f"""
🏥 **Welcome to Health Tracker Bot!** 🏥

Hi {user.first_name}! I'm here to help you track your daily health metrics.

**Available Commands:**
📊 /stats - View your health statistics
👤 /profile - Manage your profile
⚖️ /weight - Log your weight
👣 /steps - Log daily steps
💧 /water - Log water intake
🏃 /exercise - Log exercise time
😴 /sleep - Log sleep hours
😊 /mood - Log your mood
🔔 /reminder - Set daily reminders
📤 /export - Export your data
❓ /help - Show detailed help

Start tracking your health journey today! 🌟
        """
        
        keyboard = [
            [KeyboardButton("📊 Stats"), KeyboardButton("👤 Profile")],
            [KeyboardButton("⚖️ Weight"), KeyboardButton("👣 Steps")],
            [KeyboardButton("💧 Water"), KeyboardButton("🏃 Exercise")],
            [KeyboardButton("❓ Help")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🔍 **Detailed Help Guide**

**Health Tracking Commands:**
⚖️ `/weight [value]` - Log weight (kg)
   Example: /weight 70.5

👣 `/steps [value]` - Log daily steps
   Example: /steps 8500

💧 `/water [value]` - Log water intake (ml)
   Example: /water 2000

🏃 `/exercise [minutes]` - Log exercise time
   Example: /exercise 45

😴 `/sleep [hours]` - Log sleep duration
   Example: /sleep 8

😊 `/mood [1-10]` - Rate your mood (1=sad, 10=happy)
   Example: /mood 8

**Data Management:**
📊 `/stats` - View your statistics
👤 `/profile` - Manage profile settings
📤 `/export` - Export your data as CSV
🔔 `/reminder` - Set daily reminders

**Tips:**
• You can use the keyboard buttons for quick access
• Data is automatically saved with timestamp
• Use /stats to track your progress over time
• Set reminders to maintain consistency

Need more help? Just type your question! 🤔
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def weight_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /weight command"""
        user_id = update.effective_user.id
        
        if context.args:
            try:
                weight = float(context.args[0])
                if 20 <= weight <= 500:  # Reasonable weight range
                    success = self.db.record_health_data(
                        user_id=user_id,
                        record_type='weight',
                        value=weight,
                        unit='kg'
                    )
                    
                    if success:
                        await update.message.reply_text(
                            f"✅ Weight recorded: {weight} kg\n"
                            f"📅 Date: {date.today().strftime('%Y-%m-%d')}"
                        )
                    else:
                        await update.message.reply_text("❌ Failed to record weight. Please try again.")
                else:
                    await update.message.reply_text("❌ Please enter a realistic weight between 20-500 kg")
            except ValueError:
                await update.message.reply_text("❌ Please enter a valid number for weight")
        else:
            self.user_states[user_id] = 'waiting_weight'
            await update.message.reply_text(
                "⚖️ Please send your current weight in kg:\n"
                "Example: 70.5"
            )
    
    async def steps_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /steps command"""
        user_id = update.effective_user.id
        
        if context.args:
            try:
                steps = int(context.args[0])
                if 0 <= steps <= 100000:  # Reasonable steps range
                    success = self.db.record_health_data(
                        user_id=user_id,
                        record_type='steps',
                        value=steps,
                        unit='steps'
                    )
                    
                    if success:
                        await update.message.reply_text(
                            f"✅ Steps recorded: {steps:,} steps\n"
                            f"📅 Date: {date.today().strftime('%Y-%m-%d')}"
                        )
                    else:
                        await update.message.reply_text("❌ Failed to record steps. Please try again.")
                else:
                    await update.message.reply_text("❌ Please enter a realistic step count (0-100,000)")
            except ValueError:
                await update.message.reply_text("❌ Please enter a valid number for steps")
        else:
            self.user_states[user_id] = 'waiting_steps'
            await update.message.reply_text(
                "👣 Please send your daily step count:\n"
                "Example: 8500"
            )
    
    async def water_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /water command"""
        user_id = update.effective_user.id
        
        if context.args:
            try:
                water = float(context.args[0])
                if 0 <= water <= 10000:  # Reasonable water intake range
                    success = self.db.record_health_data(
                        user_id=user_id,
                        record_type='water',
                        value=water,
                        unit='ml'
                    )
                    
                    if success:
                        await update.message.reply_text(
                            f"✅ Water intake recorded: {water} ml\n"
                            f"📅 Date: {date.today().strftime('%Y-%m-%d')}"
                        )
                    else:
                        await update.message.reply_text("❌ Failed to record water intake. Please try again.")
                else:
                    await update.message.reply_text("❌ Please enter a realistic water amount (0-10,000 ml)")
            except ValueError:
                await update.message.reply_text("❌ Please enter a valid number for water intake")
        else:
            self.user_states[user_id] = 'waiting_water'
            await update.message.reply_text(
                "💧 Please send your water intake in ml:\n"
                "Example: 2000"
            )
    
    async def exercise_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /exercise command"""
        user_id = update.effective_user.id
        
        if context.args:
            try:
                exercise = int(context.args[0])
                if 0 <= exercise <= 1440:  # Max 24 hours
                    success = self.db.record_health_data(
                        user_id=user_id,
                        record_type='exercise',
                        value=exercise,
                        unit='minutes'
                    )
                    
                    if success:
                        hours, minutes = divmod(exercise, 60)
                        time_str = f"{hours}h {minutes}m" if hours else f"{minutes}m"
                        await update.message.reply_text(
                            f"✅ Exercise recorded: {time_str}\n"
                            f"📅 Date: {date.today().strftime('%Y-%m-%d')}"
                        )
                    else:
                        await update.message.reply_text("❌ Failed to record exercise. Please try again.")
                else:
                    await update.message.reply_text("❌ Please enter exercise time between 0-1440 minutes")
            except ValueError:
                await update.message.reply_text("❌ Please enter a valid number for exercise minutes")
        else:
            self.user_states[user_id] = 'waiting_exercise'
            await update.message.reply_text(
                "🏃 Please send your exercise time in minutes:\n"
                "Example: 45"
            )
    
    async def sleep_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sleep command"""
        user_id = update.effective_user.id
        
        if context.args:
            try:
                sleep = float(context.args[0])
                if 0 <= sleep <= 24:  # Reasonable sleep range
                    success = self.db.record_health_data(
                        user_id=user_id,
                        record_type='sleep',
                        value=sleep,
                        unit='hours'
                    )
                    
                    if success:
                        await update.message.reply_text(
                            f"✅ Sleep recorded: {sleep} hours\n"
                            f"📅 Date: {date.today().strftime('%Y-%m-%d')}"
                        )
                    else:
                        await update.message.reply_text("❌ Failed to record sleep. Please try again.")
                else:
                    await update.message.reply_text("❌ Please enter sleep hours between 0-24")
            except ValueError:
                await update.message.reply_text("❌ Please enter a valid number for sleep hours")
        else:
            self.user_states[user_id] = 'waiting_sleep'
            await update.message.reply_text(
                "😴 Please send your sleep duration in hours:\n"
                "Example: 8"
            )
    
    async def mood_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /mood command"""
        user_id = update.effective_user.id
        
        if context.args:
            try:
                mood = int(context.args[0])
                if 1 <= mood <= 10:
                    success = self.db.record_health_data(
                        user_id=user_id,
                        record_type='mood',
                        value=mood,
                        unit='scale'
                    )
                    
                    if success:
                        mood_emoji = "😢" if mood <= 3 else "😐" if mood <= 6 else "😊"
                        await update.message.reply_text(
                            f"✅ Mood recorded: {mood}/10 {mood_emoji}\n"
                            f"📅 Date: {date.today().strftime('%Y-%m-%d')}"
                        )
                    else:
                        await update.message.reply_text("❌ Failed to record mood. Please try again.")
                else:
                    await update.message.reply_text("❌ Please rate your mood from 1 to 10")
            except ValueError:
                await update.message.reply_text("❌ Please enter a valid number from 1 to 10")
        else:
            self.user_states[user_id] = 'waiting_mood'
            keyboard = [
                [KeyboardButton("1😢"), KeyboardButton("2"), KeyboardButton("3")],
                [KeyboardButton("4"), KeyboardButton("5😐"), KeyboardButton("6")],
                [KeyboardButton("7"), KeyboardButton("8😊"), KeyboardButton("9")],
                [KeyboardButton("10🎉")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                "😊 Please rate your mood from 1 (sad) to 10 (happy):",
                reply_markup=reply_markup
            )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        
        # Get statistics for last 30 days
        stats = self.db.get_stats(user_id, days=30)
        
        if not stats or stats.get('total_records', 0) == 0:
            await update.message.reply_text(
                "📊 No health data found!\n\n"
                "Start tracking your health with commands like:\n"
                "⚖️ /weight\n👣 /steps\n💧 /water\n🏃 /exercise"
            )
            return
        
        # Format statistics message
        stats_text = f"📊 **Your Health Statistics (Last 30 days)**\n\n"
        
        for record_type, data in stats.items():
            if record_type in ['total_records', 'days_period']:
                continue
                
            icon = {
                'weight': '⚖️',
                'steps': '👣',
                'water': '💧',
                'exercise': '🏃',
                'sleep': '😴',
                'mood': '😊'
            }.get(record_type, '📝')
            
            unit = {
                'weight': 'kg',
                'steps': 'steps',
                'water': 'ml',
                'exercise': 'min',
                'sleep': 'hours',
                'mood': '/10'
            }.get(record_type, '')
            
            stats_text += f"{icon} **{record_type.title()}**: {data['count']} entries, avg {data['average']} {unit}\n"
        
        stats_text += f"\n📈 Total records: {stats['total_records']}"
        
        # Get today's summary
        today_summary = self.db.get_daily_summary(user_id)
        if today_summary:
            stats_text += "\n\n**Today's Data:**\n"
            for record_type, data in today_summary.items():
                icon = {
                    'weight': '⚖️',
                    'steps': '👣',
                    'water': '💧',
                    'exercise': '🏃',
                    'sleep': '😴',
                    'mood': '😊'
                }.get(record_type, '📝')
                
                stats_text += f"{icon} {data['value']} {data['unit'] or ''}\n"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        user_id = update.effective_user.id
        user = update.effective_user
        
        # Get user preferences
        prefs = self.db.get_user_preferences(user_id)
        
        profile_text = f"👤 **Profile: {user.first_name}**\n\n"
        profile_text += f"🆔 User ID: {user_id}\n"
        profile_text += f"👥 Username: @{user.username or 'Not set'}\n"
        profile_text += f"🔔 Reminders: {'Enabled' if prefs.get('reminder_enabled', True) else 'Disabled'}\n"
        profile_text += f"⏰ Reminder time: {prefs.get('reminder_time', '20:00')}\n"
        profile_text += f"⚖️ Weight unit: {prefs.get('weight_unit', 'kg')}\n"
        
        if prefs.get('height_cm'):
            profile_text += f"📏 Height: {prefs['height_cm']} cm\n"
        if prefs.get('age'):
            profile_text += f"🎂 Age: {prefs['age']} years\n"
        if prefs.get('gender'):
            profile_text += f"👤 Gender: {prefs['gender']}\n"
        
        keyboard = [
            [KeyboardButton("Set Height"), KeyboardButton("Set Age")],
            [KeyboardButton("Toggle Reminders"), KeyboardButton("Set Reminder Time")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(profile_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def reminder_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reminder command"""
        user_id = update.effective_user.id
        
        if context.args:
            time_str = context.args[0]
            try:
                # Validate time format (HH:MM)
                datetime.strptime(time_str, '%H:%M')
                
                success = self.db.update_user_preferences(
                    user_id=user_id,
                    reminder_time=time_str,
                    reminder_enabled=True
                )
                
                if success:
                    await update.message.reply_text(
                        f"✅ Daily reminder set for {time_str}\n"
                        "You'll receive a daily health tracking reminder at this time."
                    )
                else:
                    await update.message.reply_text("❌ Failed to set reminder. Please try again.")
            except ValueError:
                await update.message.reply_text("❌ Please use HH:MM format (24-hour)\nExample: /reminder 20:00")
        else:
            await update.message.reply_text(
                "🔔 **Daily Reminder Setup**\n\n"
                "Send your preferred reminder time in HH:MM format (24-hour)\n"
                "Example: /reminder 20:00 (8:00 PM)\n\n"
                "Or use buttons below:",
                reply_markup=ReplyKeyboardMarkup([
                    [KeyboardButton("08:00"), KeyboardButton("12:00")],
                    [KeyboardButton("18:00"), KeyboardButton("20:00")],
                    [KeyboardButton("Disable Reminders")]
                ], resize_keyboard=True, one_time_keyboard=True)
            )
    
    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /export command"""
        user_id = update.effective_user.id
        
        # Get all user records
        records = self.db.get_user_records(user_id, days=365)  # Last year
        
        if not records:
            await update.message.reply_text(
                "📤 No data to export!\n\n"
                "Start tracking your health first, then you can export your data."
            )
            return
        
        # Create CSV content
        csv_content = "Date,Type,Value,Unit,Notes,Recorded At\n"
        
        for record in records:
            csv_content += f"{record['date_for']},{record['record_type']},{record['value']},"
            csv_content += f"{record['unit'] or ''},{record['notes'] or ''},{record['recorded_at']}\n"
        
        # Send as document
        from io import BytesIO
        csv_file = BytesIO(csv_content.encode('utf-8'))
        csv_file.name = f"health_data_{user_id}_{date.today().strftime('%Y%m%d')}.csv"
        
        await update.message.reply_document(
            document=csv_file,
            caption=f"📤 Your health data export\n📅 Records: {len(records)}\n🗓️ Generated: {date.today()}"
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages based on user state"""
        user_id = update.effective_user.id
        text = update.message.text.strip()
        
        # Handle keyboard button presses
        if text in ["📊 Stats", "Stats"]:
            await self.stats_command(update, context)
            return
        elif text in ["👤 Profile", "Profile"]:
            await self.profile_command(update, context)
            return
        elif text in ["❓ Help", "Help"]:
            await self.help_command(update, context)
            return
        elif text in ["⚖️ Weight", "Weight"]:
            await self.weight_command(update, context)
            return
        elif text in ["👣 Steps", "Steps"]:
            await self.steps_command(update, context)
            return
        elif text in ["💧 Water", "Water"]:
            await self.water_command(update, context)
            return
        elif text in ["🏃 Exercise", "Exercise"]:
            await self.exercise_command(update, context)
            return
        
        # Handle state-based input
        if user_id not in self.user_states:
            await update.message.reply_text(
                "I didn't understand that. Use /help to see available commands or use the keyboard buttons below."
            )
            return
        
        state = self.user_states[user_id]
        
        try:
            if state == 'waiting_weight':
                weight = float(text)
                if 20 <= weight <= 500:
                    success = self.db.record_health_data(user_id, 'weight', weight, 'kg')
                    if success:
                        await update.message.reply_text(f"✅ Weight recorded: {weight} kg")
                    else:
                        await update.message.reply_text("❌ Failed to record weight")
                else:
                    await update.message.reply_text("❌ Please enter a weight between 20-500 kg")
                    return
                
            elif state == 'waiting_steps':
                steps = int(text)
                if 0 <= steps <= 100000:
                    success = self.db.record_health_data(user_id, 'steps', steps, 'steps')
                    if success:
                        await update.message.reply_text(f"✅ Steps recorded: {steps:,}")
                    else:
                        await update.message.reply_text("❌ Failed to record steps")
                else:
                    await update.message.reply_text("❌ Please enter steps between 0-100,000")
                    return
                
            elif state == 'waiting_water':
                water = float(text)
                if 0 <= water <= 10000:
                    success = self.db.record_health_data(user_id, 'water', water, 'ml')
                    if success:
                        await update.message.reply_text(f"✅ Water intake recorded: {water} ml")
                    else:
                        await update.message.reply_text("❌ Failed to record water intake")
                else:
                    await update.message.reply_text("❌ Please enter water amount between 0-10,000 ml")
                    return
                
            elif state == 'waiting_exercise':
                exercise = int(text)
                if 0 <= exercise <= 1440:
                    success = self.db.record_health_data(user_id, 'exercise', exercise, 'minutes')
                    if success:
                        hours, minutes = divmod(exercise, 60)
                        time_str = f"{hours}h {minutes}m" if hours else f"{minutes}m"
                        await update.message.reply_text(f"✅ Exercise recorded: {time_str}")
                    else:
                        await update.message.reply_text("❌ Failed to record exercise")
                else:
                    await update.message.reply_text("❌ Please enter exercise time between 0-1440 minutes")
                    return
                
            elif state == 'waiting_sleep':
                sleep = float(text)
                if 0 <= sleep <= 24:
                    success = self.db.record_health_data(user_id, 'sleep', sleep, 'hours')
                    if success:
                        await update.message.reply_text(f"✅ Sleep recorded: {sleep} hours")
                    else:
                        await update.message.reply_text("❌ Failed to record sleep")
                else:
                    await update.message.reply_text("❌ Please enter sleep hours between 0-24")
                    return
                
            elif state == 'waiting_mood':
                # Handle both number and emoji button format
                if text.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')) and text[0].isdigit():
                    mood = int(text[0])
                else:
                    mood = int(text)
                
                if 1 <= mood <= 10:
                    success = self.db.record_health_data(user_id, 'mood', mood, 'scale')
                    if success:
                        mood_emoji = "😢" if mood <= 3 else "😐" if mood <= 6 else "😊"
                        await update.message.reply_text(f"✅ Mood recorded: {mood}/10 {mood_emoji}")
                    else:
                        await update.message.reply_text("❌ Failed to record mood")
                else:
                    await update.message.reply_text("❌ Please rate your mood from 1 to 10")
                    return
            
            # Clear state after successful input
            del self.user_states[user_id]
            
            # Show main keyboard
            keyboard = [
                [KeyboardButton("📊 Stats"), KeyboardButton("👤 Profile")],
                [KeyboardButton("⚖️ Weight"), KeyboardButton("👣 Steps")],
                [KeyboardButton("💧 Water"), KeyboardButton("🏃 Exercise")],
                [KeyboardButton("❓ Help")]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("What would you like to track next?", reply_markup=reply_markup)
            
        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")
