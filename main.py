#!/usr/bin/env python3
"""
Telegram File Storage Bot
Main entry point for the bot application
"""

import logging
import asyncio
import os
from telegram.ext import Application
from config import Config
from bot_handlers import setup_handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    try:
        # Get bot token from environment
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
            return

        # Create application
        application = Application.builder().token(bot_token).build()
        
        # Setup handlers
        setup_handlers(application)
        
        logger.info("Starting Telegram File Storage Bot...")
        
        # Start the bot using run_polling which handles the event loop internally
        application.run_polling(allowed_updates=["message"])
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()
