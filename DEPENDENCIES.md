# Project Dependencies

## Core Dependencies

### Telegram Bot Framework
- **python-telegram-bot** (>=20.8) - Main bot framework for Telegram API interaction

### Web Framework (Webhook Server)
- **Flask** (>=3.1.1) - Web framework for webhook server
- **gunicorn** (>=23.0.0) - Production WSGI server
- **Jinja2** (>=3.1.6) - Template engine for web interface
- **Werkzeug** (>=3.1.3) - WSGI utilities
- **MarkupSafe** (>=3.0.2) - HTML escaping utilities
- **itsdangerous** (>=2.2.0) - Secure token generation
- **click** (>=8.2.1) - Command-line interface utilities
- **blinker** (>=1.9.0) - Signal dispatching

### HTTP & Networking
- **requests** (>=2.32.4) - HTTP library for API calls
- **urllib3** (>=2.5.0) - HTTP client (dependency of requests)
- **charset-normalizer** (>=3.4.2) - Character encoding detection

### Async Support
- **asyncio** - Built-in Python async library (used by telegram bot)
- **httpx** - Async HTTP client (used by python-telegram-bot)

### Utilities
- **packaging** (>=25.0) - Version handling utilities

## Installation Commands

### Using UV (Replit's package manager)
```bash
uv add python-telegram-bot flask gunicorn requests
```

### Using Pip (Alternative)
```bash
pip install python-telegram-bot>=20.8 flask>=3.1.1 gunicorn>=23.0.0 requests>=2.32.4
```

## Development Dependencies (Optional)

### Testing
```bash
uv add pytest pytest-asyncio
```

### Code Quality
```bash
uv add black flake8
```

## Environment Variables Required

- **TELEGRAM_BOT_TOKEN** - Bot token from @BotFather (required)

## Current Project Structure

```
├── main.py              # Polling mode bot
├── webhook_server.py    # Webhook server with web dashboard
├── bot_handlers.py      # Shared bot message handlers
├── database.py          # SQLite database management
├── file_manager.py      # File operation utilities
├── config.py           # Configuration settings
├── deploy_webhook.py   # Webhook deployment helper
├── gunicorn_config.py  # Production server configuration
├── templates/
│   └── index.html      # Web dashboard interface
└── DEPENDENCIES.md     # This file
```

## Deployment Notes

- All dependencies are managed through UV in Replit environment
- The project uses SQLite (built-in) for database storage
- No external database dependencies required
- Flask serves both API endpoints and web dashboard
- Gunicorn provides production-ready WSGI server