"""
File management utilities for the Telegram bot
"""

import logging
import os
import asyncio
from typing import Optional, Dict
from telegram.ext import ContextTypes
from config import Config

logger = logging.getLogger(__name__)

class FileManager:
    """Manages file operations for the bot"""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes = size_bytes / 1024.0
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    @staticmethod
    def validate_upload_size(file_size: int) -> tuple[bool, str]:
        """Validate if file size is within upload limits"""
        if file_size > Config.TELEGRAM_FILE_SIZE_LIMIT:
            max_size = FileManager.format_file_size(Config.TELEGRAM_FILE_SIZE_LIMIT)
            return False, f"File too large. Maximum upload size is {max_size}"
        
        return True, ""
    
    @staticmethod
    def validate_download_size(file_size: int) -> tuple[bool, str]:
        """Validate if file size is within download limits"""
        if file_size > Config.MAX_DOWNLOAD_SIZE:
            max_size = FileManager.format_file_size(Config.MAX_DOWNLOAD_SIZE)
            return False, f"File too large for download. Maximum download size is {max_size}"
        
        return True, ""
    
    @staticmethod
    async def get_file_info(context: ContextTypes.DEFAULT_TYPE, file_id: str):
        """Get file information from Telegram"""
        try:
            file = await context.bot.get_file(file_id)
            return file
        except Exception as e:
            logger.error(f"Error getting file info for {file_id}: {e}")
            return None
    
    @staticmethod
    async def download_file_bytes(context: ContextTypes.DEFAULT_TYPE, file_id: str) -> Optional[bytes]:
        """Download file as bytes from Telegram"""
        try:
            file = await context.bot.get_file(file_id)
            if not file:
                return None
            
            # Validate download size
            is_valid, error_msg = FileManager.validate_download_size(file.file_size)
            if not is_valid:
                logger.warning(f"Download size validation failed: {error_msg}")
                return None
            
            # Download file
            file_bytes = await file.download_as_bytearray()
            return bytes(file_bytes)
            
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {e}")
            return None
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Get file extension from filename"""
        return os.path.splitext(filename)[1].lower()
    
    @staticmethod
    def is_supported_file_type(filename: str) -> bool:
        """Check if file type is supported (for now, all types are supported)"""
        # You can add restrictions here if needed
        return True
    
    @staticmethod
    def generate_file_info_text(file_info: Dict) -> str:
        """Generate formatted text for file information"""
        upload_date = file_info.get('upload_date', 'Unknown')
        file_size = FileManager.format_file_size(file_info.get('file_size', 0))
        mime_type = file_info.get('mime_type', 'Unknown')
        
        return (
            f"📁 **{file_info['file_name']}**\n"
            f"📊 Size: {file_size}\n"
            f"📅 Uploaded: {upload_date}\n"
            f"🎯 Type: {mime_type}"
        )
    
    @staticmethod
    def generate_file_list_text(files: list) -> str:
        """Generate formatted text for file list with comprehensive details"""
        if not files:
            return "📂 No files found.\n\nUse /upload to upload your first file!"
        
        # Calculate total storage used
        total_size = sum(file['file_size'] for file in files)
        total_size_str = FileManager.format_file_size(total_size)
        
        text = f"📂 **Your Files** ({len(files)} files, {total_size_str} total):\n\n"
        
        for i, file_info in enumerate(files, 1):
            size = FileManager.format_file_size(file_info['file_size'])
            mime_type = file_info.get('mime_type', 'Unknown')
            upload_date = file_info.get('upload_date', 'Unknown')
            
            # Format upload date to show just date part
            if upload_date != 'Unknown' and ' ' in upload_date:
                upload_date = upload_date.split(' ')[0]
            
            # Escape filename for Markdown
            safe_filename = file_info['file_name'].replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)')
            
            text += f"{i}. **{safe_filename}**\n"
            text += f"   📊 Size: {size} | 🎯 Type: {mime_type}\n"
            text += f"   📅 Uploaded: {upload_date}\n\n"
        
        text += f"**Commands:**\n"
        text += f"💡 `/download filename` - Download a file\n"
        text += f"💡 `/details filename` - View complete file info\n"
        text += f"💡 `/stats` - View storage statistics\n"
        text += f"💡 `/delete filename` - Delete a file"
        
        return text
