"""
Configuration settings for the Telegram File Storage Bot
"""

import os

class Config:
    """Configuration class for bot settings"""
    
    # File size limits (in bytes)
    MAX_UPLOAD_SIZE = 4 * 1024 * 1024 * 1024  # 4GB
    MAX_DOWNLOAD_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
    
    # Telegram API limits
    TELEGRAM_FILE_SIZE_LIMIT = 2 * 1024 * 1024 * 1024  # 2GB (Telegram's actual limit)
    
    # Database file
    DATABASE_FILE = "file_storage.db"
    
    # Bot settings
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Chunk size for large file operations
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks
    
    # Maximum files per user
    MAX_FILES_PER_USER = 100
    
    @classmethod
    def get_max_upload_size_mb(cls):
        """Get max upload size in MB"""
        return cls.MAX_UPLOAD_SIZE // (1024 * 1024)
    
    @classmethod
    def get_max_download_size_mb(cls):
        """Get max download size in MB"""
        return cls.MAX_DOWNLOAD_SIZE // (1024 * 1024)
