"""
Password utilities for the SPS Auth Workflow application.

Provides password hashing (MD5 + salt), verification, and validation.
"""

import hashlib
import secrets
import re


def generate_salt(length: int = 32) -> str:
    """
    Generate a cryptographically secure random salt.
    
    Args:
        length: Number of hex characters in the salt (default 32).
    
    Returns:
        A hex-encoded random string.
    """
    return secrets.token_hex(length // 2)


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """
    Hash a password using MD5 with a salt.
    
    Args:
        password: The plaintext password to hash.
        salt: Optional salt to use. If not provided, a new salt is generated.
    
    Returns:
        A tuple of (password_hash, salt).
    """
    if salt is None:
        salt = generate_salt()
    
    salted_password = salt + password
    password_hash = hashlib.md5(salted_password.encode()).hexdigest()
    
    return password_hash, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """
    Verify a password against a stored hash.
    
    Args:
        password: The plaintext password to verify.
        stored_hash: The stored MD5 hash.
        salt: The salt used when hashing.
    
    Returns:
        True if the password matches, False otherwise.
    """
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == stored_hash


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate a password against security requirements.
    
    Requirements:
        - Length between 12 and 32 characters
        - At least one uppercase letter
        - At least one digit
        - At least one special character
    
    Args:
        password: The password to validate.
    
    Returns:
        A tuple of (is_valid, error_message).
        If valid, error_message is an empty string.
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    
    if len(password) > 32:
        return False, "Password must not exceed 32 characters"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    
    special_chars = r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`'\"]"
    if not re.search(special_chars, password):
        return False, "Password must contain at least one special character"
    
    return True, ""
