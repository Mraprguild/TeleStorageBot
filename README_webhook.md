# Telegram File Storage Bot - Webhook Deployment Guide

## Overview

This bot now supports both **polling mode** (for development) and **webhook mode** (for production deployment). The webhook implementation enables efficient, scalable deployment on platforms like Replit Deployments.

## Deployment Modes

### 1. Polling Mode (Development)
- **File**: `main.py`
- **Usage**: Local development and testing
- **Command**: `python main.py`
- **Advantages**: Simple setup, works behind firewalls

### 2. Webhook Mode (Production)
- **File**: `webhook_server.py`
- **Usage**: Production deployment with better performance
- **Command**: `python webhook_server.py`
- **Advantages**: Better resource usage, instant response to messages

## Quick Start

### Development (Polling)
```bash
# Start the bot in polling mode
python main.py
```

### Production (Webhook)
```bash
# Start webhook server
python webhook_server.py

# Or with Gunicorn for production
gunicorn -c gunicorn_config.py webhook_server:app
```

## Webhook Endpoints

The webhook server provides several management endpoints:

- `POST /webhook` - Receives Telegram updates
- `GET /health` - Health check endpoint  
- `POST /set_webhook` - Configure webhook URL
- `GET /webhook_info` - Get webhook status
- `POST /delete_webhook` - Remove webhook (switch to polling)

## Deployment Script

Use the deployment helper script for easy webhook management:

```bash
# Check server health
python deploy_webhook.py info

# Setup webhook (replace with your domain)
python deploy_webhook.py setup https://yourapp.replit.app

# Remove webhook 
python deploy_webhook.py delete
```

## Replit Deployment

### Step 1: Deploy to Replit
1. Use the "Deploy" button in Replit
2. The app will be available at `https://yourproject.username.replit.app`

### Step 2: Configure Webhook
```bash
# Set webhook to your deployment URL
python deploy_webhook.py setup https://yourproject.username.replit.app
```

### Step 3: Verify Deployment
```bash
# Check that everything is working
curl https://yourproject.username.replit.app/health
```

## Environment Variables

Required environment variable:
- `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather

## Production Configuration

The webhook server includes production-ready features:

- **Gunicorn Support**: Use `gunicorn_config.py` for production WSGI server
- **Logging**: Comprehensive logging to files and console
- **Error Handling**: Robust error handling for all webhook operations  
- **Health Checks**: Built-in health monitoring endpoint
- **Security**: Webhook URL validation and secure update processing

## File Structure

```
├── main.py              # Polling mode bot
├── webhook_server.py    # Webhook server
├── bot_handlers.py      # Shared bot handlers
├── deploy_webhook.py    # Deployment helper
├── gunicorn_config.py   # Production server config
├── config.py            # Configuration settings
├── database.py          # SQLite database management
└── file_manager.py      # File operation utilities
```

## Switching Between Modes

### To Webhook Mode:
1. Stop polling bot if running
2. Start webhook server: `python webhook_server.py`
3. Configure webhook: `python deploy_webhook.py setup <URL>`

### To Polling Mode:
1. Remove webhook: `python deploy_webhook.py delete`
2. Stop webhook server
3. Start polling bot: `python main.py`

## Troubleshooting

### Webhook Issues
- Ensure your deployment URL is HTTPS
- Check that port 5000 is accessible
- Verify TELEGRAM_BOT_TOKEN is set correctly
- Use `/webhook_info` endpoint to check status

### Performance
- Use Gunicorn for production deployments
- Monitor webhook response times (should be < 10 seconds)
- Check logs for any processing errors

The bot automatically handles all file operations in both modes with identical functionality.