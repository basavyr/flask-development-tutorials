"""
Database management for the SPS Auth Workflow application.

Handles SQLite connection and schema initialization.
Includes failsafe mechanism to recreate database if deleted while server is running.
"""

import sqlite3
import os
from backend.config import Config
from backend.utils.logger import log_info, log_error, log_warning


# SQL schema for users table
USERS_TABLE_SCHEMA = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        password_salt TEXT NOT NULL,
        hashing_algorithm TEXT DEFAULT 'md5',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """
    Ensure the database schema exists.
    
    This is called on every connection to handle the case where
    the database file was deleted while the server was running.
    """
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='users'
    """)
    
    if cursor.fetchone() is None:
        # Table doesn't exist - recreate it
        log_warning("Database table 'users' not found - recreating schema")
        cursor.execute(USERS_TABLE_SCHEMA)
        conn.commit()
        log_info("Database schema recreated successfully")


def get_db_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.
    
    Returns a connection with row factory set to sqlite3.Row
    for dictionary-like access to columns.
    
    Includes failsafe: if database was deleted, it will be recreated.
    """
    db_path = Config.DATABASE_PATH
    
    # Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        log_warning(f"Database directory recreated: {db_dir}")
    
    # Check if database file exists (for logging purposes)
    db_existed = os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    if not db_existed:
        log_warning(f"Database file was missing - created new: {db_path}")
    
    # Failsafe: ensure schema exists on every connection
    _ensure_schema(conn)
    
    return conn


def init_db() -> None:
    """
    Initialize the database schema.
    
    Creates the users table if it does not exist.
    Should be called when the application starts.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(USERS_TABLE_SCHEMA)
        conn.commit()
        log_info("Database initialized successfully")
    except sqlite3.Error as e:
        log_error(f"Database initialization failed: {e}")
        raise
    finally:
        conn.close()


def close_db(conn: sqlite3.Connection) -> None:
    """Close the database connection."""
    if conn:
        conn.close()
