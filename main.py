#!/usr/bin/env python3
"""
Main entry point for Health Tracker Telegram Bot
Optimized for Replit deployment with continuous operation
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from aiohttp import web

from bot import create_bot, dp
from config import BOT_TOKEN, DATABASE_PATH
from database import init_database
from scheduler import start_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ---------- aiohttp /ping endpoint ----------
async def ping(request):
    return web.Response(text="pong")

async def start_web_app():
    app = web.Application()
    app.router.add_get("/ping", ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 3000)  # Replit uchun port 3000
    await site.start()
    logger.info("Web server started at http://0.0.0.0:3000")

async def run_bot():
    """Main function to run the Health Tracker bot"""
    try:
        logger.info("Starting Health Tracker Bot...")
        
        # Initialize database
        await init_database()
        logger.info("Database initialized successfully")
        
        # Create bot instance
        bot = create_bot()
        
        # Start scheduler for daily reminders
        await start_scheduler(bot)
        logger.info("Scheduler started for daily reminders")
        
        # Start polling
        logger.info("Bot is starting polling...")
        await dp.start_polling(bot, skip_updates=True)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        logger.info("Bot stopped")

async def main():
    await asyncio.gather(
        run_bot(),
        start_web_app()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
