"""
User model and database operations for the SPS Auth Workflow application.

Provides CRUD operations for user management.
"""

import uuid
from datetime import datetime
from backend.database import get_db_connection
from backend.utils.password import hash_password, verify_password
from backend.utils.logger import log_info, log_error, log_debug


class User:
    """Represents a user in the system with associated database operations."""
    
    def __init__(self, id: int | None = None, user_uuid: str | None = None, 
                 full_name: str | None = None, email: str | None = None, 
                 username: str | None = None, password_hash: str | None = None,
                 password_salt: str | None = None, hashing_algorithm: str = "md5",
                 created_at: str | None = None, updated_at: str | None = None):
        self.id = id
        self.uuid = user_uuid
        self.full_name = full_name
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.hashing_algorithm = hashing_algorithm
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def create(full_name: str, email: str, username: str, password: str) -> "User":
        """
        Create a new user in the database.
        
        Args:
            full_name: The user's full name.
            email: The user's email address.
            username: The user's chosen username.
            password: The plaintext password (will be hashed).
        
        Returns:
            The created User object.
        
        Raises:
            ValueError: If email or username already exists.
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Check for existing email
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                raise ValueError("Email address already registered")
            
            # Check for existing username
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                raise ValueError("Username already taken")
            
            # Generate UUID and hash password
            user_uuid = str(uuid.uuid4())
            password_hash, password_salt = hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (uuid, full_name, email, username, password_hash, 
                                   password_salt, hashing_algorithm)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_uuid, full_name, email, username, password_hash, 
                  password_salt, "md5"))
            
            conn.commit()
            user_id = cursor.lastrowid
            
            log_info(f"New user created: {username} (ID: {user_id})")
            
            return User.get_by_id(user_id)
            
        except Exception as e:
            conn.rollback()
            log_error(f"Failed to create user: {e}")
            raise
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(user_id: int) -> "User | None":
        """Retrieve a user by their ID."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User._from_row(row)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_email(email: str) -> "User | None":
        """Retrieve a user by their email address."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            if row:
                return User._from_row(row)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_username(username: str) -> "User | None":
        """Retrieve a user by their username."""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                return User._from_row(row)
            return None
        finally:
            conn.close()
    
    @staticmethod
    def authenticate(email: str, password: str) -> "User | None":
        """
        Authenticate a user with email and password.
        
        Args:
            email: The user's email address.
            password: The plaintext password to verify.
        
        Returns:
            The User object if authentication succeeds, None otherwise.
        """
        user = User.get_by_email(email)
        
        if user is None:
            log_debug(f"Authentication failed: no user with email {email}")
            return None
        
        if verify_password(password, user.password_hash, user.password_salt):
            log_info(f"User authenticated: {user.username}")
            return user
        
        log_debug(f"Authentication failed: invalid password for {email}")
        return None
    
    def update_full_name(self, new_name: str) -> bool:
        """
        Update the user's full name.
        
        Args:
            new_name: The new full name.
        
        Returns:
            True if update succeeded, False otherwise.
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET full_name = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_name, self.id))
            conn.commit()
            
            self.full_name = new_name
            log_info(f"Updated full name for user {self.username}")
            return True
        except Exception as e:
            conn.rollback()
            log_error(f"Failed to update full name: {e}")
            return False
        finally:
            conn.close()
    
    def delete(self) -> bool:
        """
        Delete the user from the database.
        
        Returns:
            True if deletion succeeded, False otherwise.
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.id,))
            conn.commit()
            
            log_info(f"User deleted: {self.username} (ID: {self.id})")
            return True
        except Exception as e:
            conn.rollback()
            log_error(f"Failed to delete user: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def _from_row(row) -> "User":
        """Create a User object from a database row."""
        return User(
            id=row["id"],
            user_uuid=row["uuid"],
            full_name=row["full_name"],
            email=row["email"],
            username=row["username"],
            password_hash=row["password_hash"],
            password_salt=row["password_salt"],
            hashing_algorithm=row["hashing_algorithm"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    def to_dict(self) -> dict:
        """Convert user to a dictionary (excludes sensitive fields)."""
        return {
            "id": self.id,
            "uuid": self.uuid,
            "full_name": self.full_name,
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
