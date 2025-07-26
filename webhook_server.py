#!/usr/bin/env python3
"""
Webhook server for Telegram File Storage Bot
Enables webhook-based updates for production deployment
"""

import logging
import os
import asyncio
import json
from flask import Flask, request, Response, jsonify, render_template
from telegram import Update
from telegram.ext import Application
from bot_handlers import setup_handlers
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('webhook.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Global application instance
telegram_app = None

def create_telegram_application():
    """Create and configure Telegram application"""
    global telegram_app
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    # Create application
    telegram_app = Application.builder().token(bot_token).build()
    
    # Setup handlers
    setup_handlers(telegram_app)
    
    logger.info("Telegram application created and configured")
    return telegram_app

def run_async(coro):
    """Helper to run async code in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

@app.route('/', methods=['GET'])
def index():
    """Dashboard homepage"""
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'bot': 'telegram-file-storage'}, 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    try:
        # Get update data
        update_data = request.get_json()
        
        if not update_data:
            logger.warning("Received empty webhook data")
            return Response(status=400)
        
        # Create Update object
        update = Update.de_json(update_data, telegram_app.bot)
        
        if update:
            # Process the update asynchronously
            run_async(telegram_app.process_update(update))
            logger.debug(f"Processed update: {update.update_id}")
        else:
            logger.warning("Failed to parse update from webhook data")
            return Response(status=400)
        
        return Response(status=200)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return Response(status=500)

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    """Set webhook URL for the bot"""
    try:
        webhook_url = request.json.get('url')
        if not webhook_url:
            return jsonify({'error': 'No webhook URL provided'}), 400
        
        # Set webhook
        success = run_async(telegram_app.bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True
        ))
        
        if success:
            logger.info(f"Webhook set successfully: {webhook_url}")
            return jsonify({'status': 'success', 'webhook_url': webhook_url}), 200
        else:
            logger.error("Failed to set webhook")
            return jsonify({'error': 'Failed to set webhook'}), 500
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    """Get current webhook information"""
    try:
        webhook_info = run_async(telegram_app.bot.get_webhook_info())
        
        return jsonify({
            'url': webhook_info.url,
            'has_custom_certificate': webhook_info.has_custom_certificate,
            'pending_update_count': webhook_info.pending_update_count,
            'last_error_date': webhook_info.last_error_date.isoformat() if webhook_info.last_error_date else None,
            'last_error_message': webhook_info.last_error_message,
            'max_connections': webhook_info.max_connections,
            'allowed_updates': webhook_info.allowed_updates
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_webhook', methods=['POST'])
def delete_webhook():
    """Delete webhook and switch back to polling"""
    try:
        success = run_async(telegram_app.bot.delete_webhook(drop_pending_updates=True))
        
        if success:
            logger.info("Webhook deleted successfully")
            return jsonify({'status': 'success', 'message': 'Webhook deleted'}), 200
        else:
            logger.error("Failed to delete webhook")
            return jsonify({'error': 'Failed to delete webhook'}), 500
            
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        return jsonify({'error': str(e)}), 500

def main():
    """Main function to run webhook server"""
    try:
        # Create Telegram application
        create_telegram_application()
        
        # Get port from environment or use default
        port = int(os.getenv('PORT', 5000))
        
        logger.info(f"Starting webhook server on port {port}")
        logger.info("Available endpoints:")
        logger.info("  POST /webhook - Receive Telegram updates")
        logger.info("  POST /set_webhook - Set webhook URL")
        logger.info("  GET /webhook_info - Get webhook information")
        logger.info("  POST /delete_webhook - Delete webhook")
        logger.info("  GET /health - Health check")
        
        # Run Flask app
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False
        )
        
    except Exception as e:
        logger.error(f"Error starting webhook server: {e}")
        return False

if __name__ == "__main__":
    main()