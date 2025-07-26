"""
Telegram bot handlers for file upload/download operations
"""

import logging
from telegram import Update
from telegram.ext import (
    ContextTypes, CommandHandler, MessageHandler, 
    filters
)
from database import FileDatabase
from file_manager import FileManager
from config import Config

logger = logging.getLogger(__name__)

# Initialize database
db = FileDatabase()

def escape_markdown(text: str) -> str:
    """Escape special characters for Telegram Markdown"""
    return text.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    welcome_text = (
        "🚀 **Welcome to File Storage Bot!**\n\n"
        "I can help you store and manage files using Telegram's servers.\n\n"
        "**Available Commands:**\n"
        "/upload - Upload a file (send any document)\n"
        "/list - List your uploaded files\n"
        "/details <filename> - Get detailed file information\n"
        "/stats - Show your storage statistics\n"
        "/download <filename> - Download a specific file\n"
        "/delete <filename> - Delete a file\n"
        "/help - Show this help message\n\n"
        f"**Limits:**\n"
        f"📤 Max upload: {FileManager.format_file_size(Config.TELEGRAM_FILE_SIZE_LIMIT)}\n"
        f"📥 Max download: {FileManager.format_file_size(Config.MAX_DOWNLOAD_SIZE)}\n"
        f"📁 Max files per user: {Config.MAX_FILES_PER_USER}"
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = (
        "🤖 **File Storage Bot Help**\n\n"
        "**How to use:**\n"
        "1. Send any document to upload it\n"
        "2. Use /list to see your files\n"
        "3. Use /details filename for complete file info\n"
        "4. Use /stats to see your storage usage\n"
        "5. Use /download filename to get a file back\n"
        "6. Use /delete filename to remove a file\n\n"
        "**Features:**\n"
        "✅ Store files up to 2GB each\n"
        "✅ Download files up to 10GB\n"
        "✅ Complete file metadata tracking\n"
        "✅ Storage statistics\n"
        "✅ Simple file management\n\n"
        "**Tips:**\n"
        "• File names are case-sensitive\n"
        "• Use quotes for filenames with spaces\n"
        "• Files are stored on Telegram's servers\n"
        "• Check /stats to monitor your usage"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /upload command"""
    upload_text = (
        "📤 **Upload a File**\n\n"
        "To upload a file, simply send any document to this chat.\n\n"
        "**Supported:**\n"
        "• Documents\n"
        "• Images\n"
        "• Videos\n"
        "• Audio files\n"
        "• Any other file type\n\n"
        f"**Maximum size:** {FileManager.format_file_size(Config.TELEGRAM_FILE_SIZE_LIMIT)}"
    )
    
    await update.message.reply_text(upload_text, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document uploads"""
    try:
        user_id = update.effective_user.id
        document = update.message.document
        
        if not document:
            await update.message.reply_text("❌ No document found in the message.")
            return
        
        # Check file count limit
        file_count = db.get_user_file_count(user_id)
        if file_count >= Config.MAX_FILES_PER_USER:
            await update.message.reply_text(
                f"❌ You have reached the maximum file limit ({Config.MAX_FILES_PER_USER} files).\n"
                "Please delete some files before uploading new ones."
            )
            return
        
        # Validate file size
        is_valid, error_msg = FileManager.validate_upload_size(document.file_size)
        if not is_valid:
            await update.message.reply_text(f"❌ {error_msg}")
            return
        
        # Check if file already exists
        existing_file = db.get_file_by_name(user_id, document.file_name)
        if existing_file:
            await update.message.reply_text(
                f"❌ A file named '{document.file_name}' already exists.\n"
                "Please rename the file or delete the existing one first."
            )
            return
        
        # Escape filename for Markdown
        safe_filename = escape_markdown(document.file_name)
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            f"⏳ Processing upload: **{safe_filename}**\n"
            f"Size: {FileManager.format_file_size(document.file_size)}",
            parse_mode='Markdown'
        )
        
        # Add file to database
        success = db.add_file(
            user_id=user_id,
            file_id=document.file_id,
            file_name=document.file_name,
            file_size=document.file_size,
            mime_type=document.mime_type,
            file_unique_id=document.file_unique_id
        )
        
        if success:
            await processing_msg.edit_text(
                f"✅ **Upload Successful!**\n\n"
                f"📁 File: {safe_filename}\n"
                f"📊 Size: {FileManager.format_file_size(document.file_size)}\n"
                f"🎯 Type: {document.mime_type or 'Unknown'}\n\n"
                f"Use /download command to download it later.",
                parse_mode='Markdown'
            )
            logger.info(f"File uploaded successfully: {document.file_name} by user {user_id}")
        else:
            await processing_msg.edit_text(
                "❌ Failed to save file information. The file might already exist."
            )
            
    except Exception as e:
        logger.error(f"Error handling document upload: {e}")
        await update.message.reply_text(
            "❌ An error occurred while processing your upload. Please try again."
        )

async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /list command"""
    try:
        user_id = update.effective_user.id
        files = db.get_user_files(user_id)
        
        list_text = FileManager.generate_file_list_text(files)
        await update.message.reply_text(list_text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        await update.message.reply_text(
            "❌ An error occurred while retrieving your files."
        )

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /download command"""
    try:
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Please specify a filename.\n"
                "Usage: `/download filename`\n"
                "Use `/list` to see your files.",
                parse_mode='Markdown'
            )
            return
        
        filename = ' '.join(context.args)
        file_info = db.get_file_by_name(user_id, filename)
        
        if not file_info:
            await update.message.reply_text(
                f"❌ File '{filename}' not found.\n"
                "Use `/list` to see your available files.",
                parse_mode='Markdown'
            )
            return
        
        # Validate download size
        is_valid, error_msg = FileManager.validate_download_size(file_info['file_size'])
        if not is_valid:
            await update.message.reply_text(f"❌ {error_msg}")
            return
        
        # Send processing message
        safe_filename = escape_markdown(filename)
        processing_msg = await update.message.reply_text(
            f"⏳ Preparing download: **{safe_filename}**\n"
            f"Size: {FileManager.format_file_size(file_info['file_size'])}",
            parse_mode='Markdown'
        )
        
        # Send the file
        try:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_info['file_id'],
                caption=f"📁 {filename}\n📊 {FileManager.format_file_size(file_info['file_size'])}"
            )
            
            await processing_msg.edit_text(
                f"✅ **Download Complete!**\n\n"
                f"📁 File: {safe_filename}\n"
                f"📊 Size: {FileManager.format_file_size(file_info['file_size'])}",
                parse_mode='Markdown'
            )
            
            logger.info(f"File downloaded successfully: {filename} by user {user_id}")
            
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            await processing_msg.edit_text(
                "❌ Failed to send the file. The file might be corrupted or too large."
            )
            
    except Exception as e:
        logger.error(f"Error in download command: {e}")
        await update.message.reply_text(
            "❌ An error occurred while processing the download."
        )

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /delete command"""
    try:
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Please specify a filename.\n"
                "Usage: `/delete filename`\n"
                "Use `/list` to see your files.",
                parse_mode='Markdown'
            )
            return
        
        filename = ' '.join(context.args)
        file_info = db.get_file_by_name(user_id, filename)
        
        if not file_info:
            await update.message.reply_text(
                f"❌ File '{filename}' not found.\n"
                "Use `/list` to see your available files.",
                parse_mode='Markdown'
            )
            return
        
        # Delete from database
        success = db.delete_file(user_id, filename)
        
        if success:
            safe_filename = escape_markdown(filename)
            await update.message.reply_text(
                f"✅ **File Deleted!**\n\n"
                f"📁 File: {safe_filename}\n"
                f"📊 Size: {FileManager.format_file_size(file_info['file_size'])}\n\n"
                f"Note: The file is removed from your list but may still exist on Telegram's servers.",
                parse_mode='Markdown'
            )
            logger.info(f"File deleted successfully: {filename} by user {user_id}")
        else:
            await update.message.reply_text(
                "❌ Failed to delete the file. Please try again."
            )
            
    except Exception as e:
        logger.error(f"Error in delete command: {e}")
        await update.message.reply_text(
            "❌ An error occurred while deleting the file."
        )

async def file_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /details command"""
    try:
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text(
                "❌ Please specify a filename.\n"
                "Usage: `/details filename`\n"
                "Use `/list` to see your files.",
                parse_mode='Markdown'
            )
            return
        
        filename = ' '.join(context.args)
        file_info = db.get_file_by_name(user_id, filename)
        
        if not file_info:
            await update.message.reply_text(
                f"❌ File '{filename}' not found.\n"
                "Use `/list` to see your available files.",
                parse_mode='Markdown'
            )
            return
        
        # Escape special characters in filename for Markdown
        safe_filename = escape_markdown(file_info['file_name'])
        
        # Generate detailed file information
        details_text = (
            f"📁 **File Details: {safe_filename}**\n\n"
            f"📊 **Size:** {FileManager.format_file_size(file_info['file_size'])}\n"
            f"🎯 **Type:** {file_info['mime_type'] or 'Unknown'}\n"
            f"📅 **Upload Date:** {file_info['upload_date']}\n"
            f"🆔 **File ID:** `{file_info['file_id']}`\n"
            f"🔑 **Unique ID:** `{file_info['file_unique_id']}`\n"
            f"📋 **Database ID:** {file_info['id']}\n\n"
            f"**File Actions:**\n"
            f"• Use /download to get this file\n"
            f"• Use /delete to remove this file"
        )
        
        await update.message.reply_text(details_text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error in details command: {e}")
        await update.message.reply_text(
            "❌ An error occurred while retrieving file details."
        )

async def storage_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /stats command"""
    try:
        user_id = update.effective_user.id
        files = db.get_user_files(user_id)
        
        if not files:
            await update.message.reply_text(
                "📊 **Your Storage Statistics**\n\n"
                "📂 No files stored yet\n"
                "💾 Total storage used: 0 B\n"
                f"📁 Files remaining: {Config.MAX_FILES_PER_USER}\n\n"
                "Use /upload to start storing files!"
            )
            return
        
        # Calculate statistics
        total_size = sum(file['file_size'] for file in files)
        file_count = len(files)
        remaining_files = Config.MAX_FILES_PER_USER - file_count
        
        # File type distribution
        type_counts = {}
        for file in files:
            mime_type = file['mime_type'] or 'Unknown'
            type_counts[mime_type] = type_counts.get(mime_type, 0) + 1
        
        # Largest files (top 3)
        largest_files = sorted(files, key=lambda x: x['file_size'], reverse=True)[:3]
        
        stats_text = (
            f"📊 **Your Storage Statistics**\n\n"
            f"📂 **Total Files:** {file_count}/{Config.MAX_FILES_PER_USER}\n"
            f"💾 **Total Storage Used:** {FileManager.format_file_size(total_size)}\n"
            f"📁 **Files Remaining:** {remaining_files}\n\n"
            f"**File Types:**\n"
        )
        
        for mime_type, count in sorted(type_counts.items()):
            stats_text += f"• {mime_type}: {count} files\n"
        
        if largest_files:
            stats_text += f"\n**Largest Files:**\n"
            for i, file in enumerate(largest_files, 1):
                size = FileManager.format_file_size(file['file_size'])
                safe_filename = escape_markdown(file['file_name'])
                stats_text += f"{i}. {safe_filename} ({size})\n"
        
        stats_text += f"\n💡 Use `/list` to see all files\n💡 Use `/details filename` for file info"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error in stats command: {e}")
        await update.message.reply_text(
            "❌ An error occurred while retrieving storage statistics."
        )

async def handle_other_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle other file types (photos, videos, audio)"""
    try:
        user_id = update.effective_user.id
        file_obj = None
        file_name = None
        
        # Determine file type and get file object
        if update.message.photo:
            # Get the largest photo
            file_obj = update.message.photo[-1]
            file_name = f"photo_{file_obj.file_unique_id}.jpg"
        elif update.message.video:
            file_obj = update.message.video
            file_name = file_obj.file_name or f"video_{file_obj.file_unique_id}.mp4"
        elif update.message.audio:
            file_obj = update.message.audio
            file_name = file_obj.file_name or f"audio_{file_obj.file_unique_id}.mp3"
        elif update.message.voice:
            file_obj = update.message.voice
            file_name = f"voice_{file_obj.file_unique_id}.ogg"
        elif update.message.video_note:
            file_obj = update.message.video_note
            file_name = f"video_note_{file_obj.file_unique_id}.mp4"
        else:
            return  # Not a supported file type
        
        # Check file count limit
        file_count = db.get_user_file_count(user_id)
        if file_count >= Config.MAX_FILES_PER_USER:
            await update.message.reply_text(
                f"❌ You have reached the maximum file limit ({Config.MAX_FILES_PER_USER} files).\n"
                "Please delete some files before uploading new ones."
            )
            return
        
        # Validate file size
        is_valid, error_msg = FileManager.validate_upload_size(file_obj.file_size)
        if not is_valid:
            await update.message.reply_text(f"❌ {error_msg}")
            return
        
        # Check if file already exists
        existing_file = db.get_file_by_name(user_id, file_name)
        if existing_file:
            await update.message.reply_text(
                f"❌ A file named '{file_name}' already exists.\n"
                "Please send a different file or delete the existing one first."
            )
            return
        
        # Send processing message
        safe_filename = escape_markdown(file_name)
        processing_msg = await update.message.reply_text(
            f"⏳ Processing upload: **{safe_filename}**\n"
            f"Size: {FileManager.format_file_size(file_obj.file_size)}",
            parse_mode='Markdown'
        )
        
        # Add file to database
        mime_type = getattr(file_obj, 'mime_type', None) or 'Unknown'
        success = db.add_file(
            user_id=user_id,
            file_id=file_obj.file_id,
            file_name=file_name,
            file_size=file_obj.file_size,
            mime_type=mime_type,
            file_unique_id=file_obj.file_unique_id
        )
        
        if success:
            await processing_msg.edit_text(
                f"✅ **Upload Successful!**\n\n"
                f"📁 File: {safe_filename}\n"
                f"📊 Size: {FileManager.format_file_size(file_obj.file_size)}\n"
                f"🎯 Type: {mime_type or 'Unknown'}\n\n"
                f"Use /download command to download it later.",
                parse_mode='Markdown'
            )
            logger.info(f"File uploaded successfully: {file_name} by user {user_id}")
        else:
            await processing_msg.edit_text(
                "❌ Failed to save file information. The file might already exist."
            )
            
    except Exception as e:
        logger.error(f"Error handling file upload: {e}")
        await update.message.reply_text(
            "❌ An error occurred while processing your upload. Please try again."
        )

def setup_handlers(application):
    """Setup all bot handlers"""
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload", upload_command))
    application.add_handler(CommandHandler("list", list_files))
    application.add_handler(CommandHandler("details", file_details))
    application.add_handler(CommandHandler("stats", storage_stats))
    application.add_handler(CommandHandler("download", download_file))
    application.add_handler(CommandHandler("delete", delete_file))
    
    # File handlers
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.PHOTO, handle_other_files))
    application.add_handler(MessageHandler(filters.VIDEO, handle_other_files))
    application.add_handler(MessageHandler(filters.AUDIO, handle_other_files))
    application.add_handler(MessageHandler(filters.VOICE, handle_other_files))
    application.add_handler(MessageHandler(filters.VIDEO_NOTE, handle_other_files))
    
    logger.info("Bot handlers setup complete")
