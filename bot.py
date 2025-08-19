"""
Health Tracker Telegram Bot
Complete health tracking functionality with database persistence
"""

import asyncio
import logging
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config
from database import Database
from handlers import HealthHandlers

logger = logging.getLogger(__name__)

class HealthTrackerBot:
    def __init__(self):
        """Initialize the Health Tracker Bot"""
        self.config = Config()
        self.db = Database()
        self.handlers = HealthHandlers(self.db)
        
        # Initialize the bot application
        self.application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        # Setup handlers
        self._setup_handlers()
        
        logger.info("Health Tracker Bot initialized successfully")
    
    def _setup_handlers(self):
        """Setup all command and message handlers"""
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("profile", self.handlers.profile_command))
        self.application.add_handler(CommandHandler("stats", self.handlers.stats_command))
        self.application.add_handler(CommandHandler("reminder", self.handlers.reminder_command))
        self.application.add_handler(CommandHandler("export", self.handlers.export_command))
        
        # Health tracking commands
        self.application.add_handler(CommandHandler("weight", self.handlers.weight_command))
        self.application.add_handler(CommandHandler("steps", self.handlers.steps_command))
        self.application.add_handler(CommandHandler("water", self.handlers.water_command))
        self.application.add_handler(CommandHandler("exercise", self.handlers.exercise_command))
        self.application.add_handler(CommandHandler("sleep", self.handlers.sleep_command))
        self.application.add_handler(CommandHandler("mood", self.handlers.mood_command))
        
        # Message handlers for interactive input
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handlers.handle_message
        ))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
        
        logger.info("All handlers registered successfully")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors that occur during bot operation"""
        logger.error(f"Update {update} caused error: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. Please try again later."
            )
    
