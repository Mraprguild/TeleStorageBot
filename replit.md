# Telegram File Storage Bot

**Project Owner:** Mraprguild

## Overview

This is a Telegram bot application that enables users to upload, store, download, and manage files using Telegram's servers as a storage backend. The bot provides a simple interface for file operations with configurable size limits and user quotas.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Bot Layer**: Handles Telegram API interactions and user commands
- **Database Layer**: Manages file metadata using SQLite
- **File Management Layer**: Provides utilities for file operations and validation
- **Configuration Layer**: Centralizes application settings and limits

The architecture is designed for simplicity and maintainability, avoiding complex frameworks in favor of straightforward Python modules.

## Key Components

### 1. Bot Handlers (`bot_handlers.py`)
- **Purpose**: Manages all Telegram bot interactions and command processing
- **Key Features**: 
  - Command handlers for /start, /help, /upload, /list, /details, /stats, /download, /delete
  - Comprehensive file metadata display with full details
  - Storage statistics and analytics
  - Message handlers for all file types (documents, photos, videos, audio, voice notes)
  - User interaction through Markdown-formatted messages with proper escaping
  - Advanced file management capabilities
- **Dependencies**: python-telegram-bot library, database module, file manager

### 2. Database Management (`database.py`)
- **Purpose**: Handles file metadata storage and retrieval
- **Technology**: SQLite with direct SQL queries
- **Schema**: Single `files` table storing user_id, file_id, file_name, file_size, mime_type, upload_date, file_unique_id
- **Features**: Automatic table creation, indexing for performance, error handling

### 3. File Manager (`file_manager.py`)
- **Purpose**: Provides file operation utilities and validation
- **Key Functions**:
  - File size formatting for human-readable display
  - Upload/download size validation against configured limits
  - File operation helpers
- **Validation**: Enforces Telegram's 2GB upload limit and configurable 10GB download limit

### 4. Configuration (`config.py`)
- **Purpose**: Centralizes all application settings
- **Key Settings**:
  - File size limits (4GB upload, 10GB download, 2GB Telegram limit)
  - Database file location
  - Bot token from environment variables
  - User quotas (100 files per user)
  - Chunk size for large file operations (1MB)

### 5. Main Application (`main.py`)
- **Purpose**: Application entry point and initialization
- **Features**:
  - Logging configuration (file + console output)
  - Bot token validation
  - Application setup and polling start
  - Error handling and graceful startup

## Data Flow

1. **File Upload**: User sends any file type → Bot validates size/limits → Stores complete metadata in SQLite → Confirms upload with details
2. **File List**: User requests list → Bot queries database by user_id → Returns formatted list with sizes, types, dates, total storage
3. **File Details**: User requests details → Bot retrieves complete file metadata → Returns comprehensive information including IDs, dates, actions
4. **Storage Stats**: User requests stats → Bot calculates usage statistics → Returns file counts, total storage, type distribution, largest files  
5. **File Download**: User requests file → Bot validates permissions and size limits → Retrieves file_id from database → Downloads from Telegram servers
6. **File Delete**: User requests deletion → Bot validates ownership → Removes metadata from database → Confirms deletion with details

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Telegram Bot API wrapper for handling bot interactions
- **sqlite3**: Built-in Python module for database operations
- **asyncio**: For asynchronous operations required by telegram bot

### Environment Variables
- **TELEGRAM_BOT_TOKEN**: Required bot token from BotFather

### Third-party Services
- **Telegram Bot API**: Primary integration for bot functionality and file storage
- **Telegram File Servers**: Used as the actual file storage backend

## Deployment Strategy

### Local Development
- SQLite database stored locally (`file_storage.db`)
- Environment variable for bot token
- File logging to `bot.log`
- Direct Python execution via `main.py`

### Production Considerations
- **Database**: Currently uses SQLite; may need migration to PostgreSQL for scalability
- **Environment**: Requires `TELEGRAM_BOT_TOKEN` environment variable
- **Logging**: Configured for both file and console output
- **Error Handling**: Basic error logging and graceful failure handling
- **Scalability**: Single-instance design; would need modification for horizontal scaling

### Configuration Management
- All limits and settings centralized in `Config` class
- Easy modification of file size limits and user quotas
- Environment-based bot token configuration for security

The application is designed for simplicity and ease of deployment, with minimal external dependencies and straightforward configuration management.

## Recent Updates (Version 2.0)

**Latest Changes (July 26, 2025):**
- ✅ Fixed all Markdown parsing errors with comprehensive character escaping
- ✅ Enhanced file listing with detailed metadata display
- ✅ Added /details command for complete file information
- ✅ Added /stats command with storage analytics and file distribution
- ✅ Improved error handling for all file operations
- ✅ Support for all file types with proper metadata tracking
- ✅ Fixed special character handling in filenames across all commands
- ✅ Added utility functions for consistent Markdown escaping
- ✅ Enhanced upload/download confirmations with proper formatting
- ✅ Project ownership properly assigned to Mraprguild
- ✅ **WEBHOOK DEPLOYMENT SUPPORT**: Added complete webhook infrastructure for production deployment
- ✅ Added Flask-based webhook server with comprehensive API endpoints
- ✅ Created deployment scripts and Gunicorn configuration for production
- ✅ Added dual-mode support: polling (development) and webhook (production)

**Features Working Perfectly:**
- File uploads with size validation and metadata storage
- Comprehensive file listings with sizes, types, and dates
- Detailed file information display with all metadata
- Storage statistics with usage analytics
- File downloads with proper validation
- File deletion with confirmation
- All Markdown formatting working without errors
- Support for files with special characters in names
- **Production webhook deployment with health monitoring**
- **Complete webhook management API with setup/status/removal endpoints**