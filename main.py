"""
Health Tracker Telegram Bot - Main Entry Point
Designed for deployment on Replit with keep-alive functionality
"""

import asyncio
import logging
import os
from threading import Thread
from keep_alive import keep_alive
from bot import HealthTrackerBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot with keep-alive functionality"""
    try:
        # Start the keep-alive server in a separate thread
        logger.info("Starting keep-alive server...")
        keep_alive_thread = Thread(target=keep_alive)
        keep_alive_thread.daemon = True
        keep_alive_thread.start()
        
        # Initialize and start the bot
        logger.info("Initializing Health Tracker Bot...")
        bot = HealthTrackerBot()
        
        # Run the bot
        logger.info("Starting bot polling...")
        bot.application.run_polling(drop_pending_updates=True)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise

if __name__ == "__main__":
    main()
