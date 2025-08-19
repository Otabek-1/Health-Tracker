"""
Main bot initialization and dispatcher setup
"""

import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import register_handlers

logger = logging.getLogger(__name__)

def create_bot():
    """Create and configure bot instance"""
    bot = Bot(token=BOT_TOKEN)
    return bot

# Create dispatcher with memory storage for FSM
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register all handlers
register_handlers(dp)

logger.info("Bot and dispatcher configured successfully")
