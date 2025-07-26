#!/usr/bin/env python3
"""
Enhanced Telegram File Storage Bot v2.0
Complete update with full error handling and enhanced features
"""

import logging
import asyncio
import os
from telegram.ext import Application
from config import Config
from bot_handlers_v2 import setup_handlers

# Configure enhanced logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot_v2.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Enhanced main function with better error handling"""
    try:
        # Validate environment
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
            return False

        # Create application with enhanced configuration
        application = Application.builder().token(bot_token).build()
        
        # Setup all handlers
        setup_handlers(application)
        
        logger.info("Starting Enhanced Telegram File Storage Bot v2.0...")
        logger.info(f"Max upload size: {Config.get_max_upload_size_mb()}MB")
        logger.info(f"Max download size: {Config.get_max_download_size_mb()}MB")
        logger.info(f"Max files per user: {Config.MAX_FILES_PER_USER}")
        
        # Start the bot with enhanced polling
        application.run_polling(
            allowed_updates=["message"],
            drop_pending_updates=True
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Critical error starting bot: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("Bot started successfully")
    else:
        logger.error("Bot failed to start")
        exit(1)