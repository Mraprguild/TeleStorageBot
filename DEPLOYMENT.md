# Telegram File Storage Bot - Deployment Guide

## Quick Start

### 1. Replit Deployment (Recommended)
```bash
# Already configured - just click Deploy in Replit!
# The project is ready for immediate deployment
```

### 2. Local Development
```bash
# Clone and install dependencies
git clone <your-repo>
cd telegram-file-storage-bot
pip install -r requirements-standalone.txt

# Set environment variable
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Run in polling mode (development)
python main.py

# Or run webhook server (production)
python webhook_server.py
```

### 3. Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t telegram-file-bot .
docker run -d -p 5000:5000 -e TELEGRAM_BOT_TOKEN="your_token" telegram-file-bot
```

## Dependencies

### Current Project Dependencies (pyproject.toml)
- `python-telegram-bot==20.8` - Main bot framework
- `flask>=3.1.1` - Web server for webhook
- `gunicorn>=23.0.0` - Production WSGI server  
- `requests>=2.32.4` - HTTP client
- `telegram>=0.0.1` - Additional Telegram utilities

### Installation Commands

**Replit (UV package manager):**
```bash
uv add python-telegram-bot flask gunicorn requests
```

**Standard Python environments:**
```bash
pip install -r requirements-standalone.txt
```

## Environment Variables

### Required
- `TELEGRAM_BOT_TOKEN` - Your bot token from @BotFather

### Optional
- `PORT` - Server port (default: 5000)

## Deployment Modes

### Polling Mode (Development)
- **File**: `main.py`
- **Best for**: Local development, testing, environments behind firewalls
- **Command**: `python main.py`

### Webhook Mode (Production)
- **File**: `webhook_server.py`  
- **Best for**: Production deployment, better performance, cloud hosting
- **Command**: `python webhook_server.py`
- **Web Dashboard**: Available at `http://your-domain.com/`

## Production Deployment

### Replit Deployments
1. Click "Deploy" button in Replit
2. Your app will be available at `https://yourproject.username.replit.app`
3. Visit the web dashboard to configure webhook
4. Or use: `python deploy_webhook.py setup https://yourproject.username.replit.app`

### Other Cloud Platforms

**Heroku:**
```bash
# Procfile is included
git push heroku main
heroku config:set TELEGRAM_BOT_TOKEN="your_token"
```

**DigitalOcean/AWS/GCP:**
```bash
# Use Docker deployment
docker-compose up -d
```

## File Structure

```
telegram-file-storage-bot/
├── main.py                    # Polling mode bot
├── webhook_server.py          # Webhook server + web dashboard
├── bot_handlers.py           # Shared message handlers
├── database.py               # SQLite database management
├── file_manager.py           # File utilities
├── config.py                 # Configuration
├── deploy_webhook.py         # Webhook helper script
├── gunicorn_config.py        # Production server config
├── templates/
│   └── index.html           # Web dashboard
├── requirements-standalone.txt # Dependencies for external deployment
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-container setup
├── pyproject.toml          # Replit dependencies
└── file_storage.db         # SQLite database (created automatically)
```

## Webhook Management

### Web Dashboard
- Visit your deployment URL for the management interface
- Real-time status monitoring
- Set/delete webhook directly from browser
- Health checks and error monitoring

### Command Line
```bash
# Check webhook status
python deploy_webhook.py info

# Set webhook URL
python deploy_webhook.py setup https://your-domain.com

# Remove webhook (switch to polling)
python deploy_webhook.py delete
```

### API Endpoints
- `GET /` - Web dashboard
- `GET /health` - Health check
- `POST /webhook` - Telegram webhook endpoint
- `GET /webhook_info` - Webhook status
- `POST /set_webhook` - Configure webhook
- `POST /delete_webhook` - Remove webhook

## Database

- **Type**: SQLite (file-based)
- **File**: `file_storage.db` (created automatically)
- **Schema**: Single `files` table with metadata
- **Backup**: Simply copy the `.db` file

## Security Notes

- Bot token is stored in environment variables only
- Webhook endpoints validate Telegram signatures
- File access is user-isolated
- No sensitive data stored in logs

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check `TELEGRAM_BOT_TOKEN` is set correctly
- Verify bot is not running in multiple places
- Check logs for error messages

**Webhook errors:**
- Ensure deployment URL uses HTTPS
- Check that port 5000 is accessible
- Verify webhook URL is set correctly

**File upload/download issues:**
- Check file size limits (4GB upload, 10GB download)
- Verify database permissions
- Check available disk space

### Logs
- **Development**: Console output
- **Production**: `bot.log` and `webhook.log` files
- **Docker**: Use `docker logs container_name`

## Performance

- **File limits**: 4GB upload, 10GB download
- **User limits**: 100 files per user (configurable)
- **Concurrent users**: Supports multiple users simultaneously
- **Database**: SQLite suitable for moderate usage
- **Scaling**: For high load, consider PostgreSQL migration