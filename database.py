"""
Database operations for file metadata storage
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Union

logger = logging.getLogger(__name__)

class FileDatabase:
    """Database manager for file metadata"""
    
    def __init__(self, db_file: str = "file_storage.db"):
        self.db_file = db_file
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Create files table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        file_id TEXT NOT NULL,
                        file_name TEXT NOT NULL,
                        file_size INTEGER NOT NULL,
                        mime_type TEXT,
                        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_unique_id TEXT UNIQUE
                    )
                """)
                
                # Create index for faster queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_user_id ON files(user_id)
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def add_file(self, user_id: int, file_id: str, file_name: str, 
                 file_size: int, mime_type: Optional[str] = None, file_unique_id: Optional[str] = None) -> bool:
        """Add a new file record to the database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO files (user_id, file_id, file_name, file_size, mime_type, file_unique_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, file_id, file_name, file_size, mime_type, file_unique_id))
                
                conn.commit()
                logger.info(f"Added file record: {file_name} for user {user_id}")
                return True
                
        except sqlite3.IntegrityError:
            logger.warning(f"File with unique_id {file_unique_id} already exists")
            return False
        except Exception as e:
            logger.error(f"Error adding file record: {e}")
            return False
    
    def get_user_files(self, user_id: int) -> List[Dict]:
        """Get all files for a specific user"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, file_id, file_name, file_size, mime_type, upload_date, file_unique_id
                    FROM files 
                    WHERE user_id = ?
                    ORDER BY upload_date DESC
                """, (user_id,))
                
                files = []
                for row in cursor.fetchall():
                    files.append({
                        'id': row[0],
                        'file_id': row[1],
                        'file_name': row[2],
                        'file_size': row[3],
                        'mime_type': row[4],
                        'upload_date': row[5],
                        'file_unique_id': row[6]
                    })
                
                return files
                
        except Exception as e:
            logger.error(f"Error getting user files: {e}")
            return []
    
    def get_file_by_name(self, user_id: int, file_name: str) -> Optional[Dict]:
        """Get a specific file by name for a user"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, file_id, file_name, file_size, mime_type, upload_date, file_unique_id
                    FROM files 
                    WHERE user_id = ? AND file_name = ?
                """, (user_id, file_name))
                
                row = cursor.fetchone()
                if row:
                    return {
                        'id': row[0],
                        'file_id': row[1],
                        'file_name': row[2],
                        'file_size': row[3],
                        'mime_type': row[4],
                        'upload_date': row[5],
                        'file_unique_id': row[6]
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting file by name: {e}")
            return None
    
    def delete_file(self, user_id: int, file_name: str) -> bool:
        """Delete a file record from the database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM files 
                    WHERE user_id = ? AND file_name = ?
                """, (user_id, file_name))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Deleted file record: {file_name} for user {user_id}")
                    return True
                else:
                    logger.warning(f"File {file_name} not found for user {user_id}")
                    return False
                
        except Exception as e:
            logger.error(f"Error deleting file record: {e}")
            return False
    
    def get_user_file_count(self, user_id: int) -> int:
        """Get the number of files for a user"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT COUNT(*) FROM files WHERE user_id = ?
                """, (user_id,))
                
                return cursor.fetchone()[0]
                
        except Exception as e:
            logger.error(f"Error getting user file count: {e}")
            return 0
