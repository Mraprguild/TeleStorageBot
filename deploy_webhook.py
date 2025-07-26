#!/usr/bin/env python3
"""
Deployment script for webhook setup
Configures webhook URL and manages deployment
"""

import os
import requests
import json
import asyncio
from telegram.ext import Application

async def setup_webhook(webhook_url):
    """Setup webhook for the bot"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found")
        return False
    
    # Create bot application
    app = Application.builder().token(bot_token).build()
    
    try:
        # Set webhook
        success = await app.bot.set_webhook(
            url=f"{webhook_url}/webhook",
            drop_pending_updates=True,
            allowed_updates=["message"]
        )
        
        if success:
            print(f"✅ Webhook set successfully: {webhook_url}/webhook")
            
            # Get webhook info to verify
            info = await app.bot.get_webhook_info()
            print(f"📋 Webhook URL: {info.url}")
            print(f"📊 Pending updates: {info.pending_update_count}")
            return True
        else:
            print("❌ Failed to set webhook")
            return False
            
    except Exception as e:
        print(f"❌ Error setting webhook: {e}")
        return False

async def delete_webhook():
    """Delete webhook and return to polling"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN not found")
        return False
    
    app = Application.builder().token(bot_token).build()
    
    try:
        success = await app.bot.delete_webhook(drop_pending_updates=True)
        if success:
            print("✅ Webhook deleted successfully")
            return True
        else:
            print("❌ Failed to delete webhook")
            return False
    except Exception as e:
        print(f"❌ Error deleting webhook: {e}")
        return False

def main():
    """Main deployment function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python deploy_webhook.py setup <webhook_url>")
        print("  python deploy_webhook.py delete")
        print("  python deploy_webhook.py info")
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        if len(sys.argv) < 3:
            print("❌ Please provide webhook URL")
            print("Example: python deploy_webhook.py setup https://yourapp.replit.app")
            return
        
        webhook_url = sys.argv[2]
        success = asyncio.run(setup_webhook(webhook_url))
        if success:
            print("\n🚀 Webhook deployment successful!")
            print("Your bot is now ready for production deployment.")
        else:
            print("\n❌ Webhook deployment failed!")
    
    elif command == "delete":
        success = asyncio.run(delete_webhook())
        if success:
            print("\n✅ Webhook removed - bot will use polling mode")
    
    elif command == "info":
        # Test webhook server health
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Webhook server is running")
                data = response.json()
                print(f"📋 Status: {data.get('status')}")
                print(f"🤖 Bot: {data.get('bot')}")
            else:
                print("❌ Webhook server not responding properly")
        except Exception as e:
            print(f"❌ Cannot connect to webhook server: {e}")
    
    else:
        print("❌ Unknown command")

if __name__ == "__main__":
    main()