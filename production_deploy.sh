#!/bin/bash
# Production deployment script for Telegram File Storage Bot

echo "🚀 Telegram File Storage Bot - Production Deployment"
echo "=================================================="

# Check environment
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN environment variable not set"
    exit 1
fi

echo "✅ Environment variables configured"

# Install dependencies if needed
echo "📦 Installing dependencies..."
uv add flask gunicorn requests python-telegram-bot

# Run in production mode with Gunicorn
echo "🔧 Starting production server with Gunicorn..."
echo "Server will be available at: http://0.0.0.0:5000"
echo "Health check: http://0.0.0.0:5000/health"
echo ""
echo "To set webhook after deployment:"
echo "  python deploy_webhook.py setup https://your-domain.com"
echo ""

# Start server
exec gunicorn -c gunicorn_config.py webhook_server:app