"""
Initialize Database Schema
"""

import logging
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

def init_db():
    """Initialize database schema"""
    
    try:
        # For SQLite, database is created automatically
        db_path = Path("astra.db")
        
        if not db_path.exists():
            logger.info("📁 Creating SQLite database...")
            
            # Create empty database
            import sqlite3
            conn = sqlite3.connect("astra.db")
            cursor = conn.cursor()
            
            # Videos table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    file_size_mb REAL,
                    status TEXT DEFAULT 'pending',
                    uploaded_at TEXT,
                    completed_at TEXT,
                    path TEXT,
                    roi_config JSON,
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Detections table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detections (
                    id TEXT PRIMARY KEY,
                    video_id TEXT,
                    frame_number INTEGER,
                    timestamp REAL,
                    motorcycle_id TEXT,
                    occupants INTEGER,
                    helmets_detected INTEGER,
                    confidence_score REAL,
                    bounding_boxes JSON,
                    is_unique_crossing BOOLEAN,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id TEXT PRIMARY KEY,
                    video_id TEXT,
                    total_motorcycles INTEGER,
                    total_occupants INTEGER,
                    helmets_worn INTEGER,
                    compliance_rate REAL,
                    processed_at TEXT,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
            logger.info("✅ Database initialized successfully")
        else:
            logger.info("✅ Database already exists")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        return False

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    init_db()
