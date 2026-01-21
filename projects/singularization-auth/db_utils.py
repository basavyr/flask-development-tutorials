#!/usr/bin/env python3
"""
Database utility script for SPS Auth Workflow.

Usage:
    python db_utils.py list              - List all users (basic info)
    python db_utils.py list full         - List all users with hash/salt columns
    python db_utils.py get <email>       - Get user by email
    python db_utils.py delete <email>    - Delete user by email
    python db_utils.py count             - Count total users
    python db_utils.py schema            - Show database schema
    python db_utils.py raw "<SQL>"       - Execute raw SQL query
"""

import sys
from backend.database import get_db_connection, init_db
from backend.models import User


def list_users(full: bool = False):
    """List all users in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if full:
        cursor.execute("SELECT id, uuid, full_name, email, username, password_hash, password_salt, hashing_algorithm, created_at FROM users ORDER BY id")
    else:
        cursor.execute("SELECT id, uuid, full_name, email, username, created_at FROM users ORDER BY id")
    
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        print("No users found in database.")
        return
    
    if full:
        print(f"\n{'ID':<4} {'Username':<15} {'Email':<30} {'Hash':<32} {'Salt':<32} {'Algo':<6} {'Created'}")
        print("-" * 160)
        for user in users:
            print(f"{user['id']:<4} {user['username']:<15} {user['email']:<30} {user['password_hash']:<32} {user['password_salt']:<32} {user['hashing_algorithm']:<6} {user['created_at']}")
    else:
        print(f"\n{'ID':<4} {'UUID':<36} {'Full Name':<20} {'Email':<30} {'Username':<15} {'Created'}")
        print("-" * 130)
        for user in users:
            print(f"{user['id']:<4} {user['uuid']:<36} {user['full_name']:<20} {user['email']:<30} {user['username']:<15} {user['created_at']}")
    
    print(f"\nTotal: {len(users)} user(s)")


def get_user(email: str):
    """Get detailed info for a specific user."""
    user = User.get_by_email(email)
    if user:
        print("\nUser Details:")
        print("-" * 40)
        for key, value in user.to_dict().items():
            print(f"  {key}: {value}")
        print(f"  hashing_algorithm: {user.hashing_algorithm}")
    else:
        print(f"No user found with email: {email}")


def delete_user(email: str):
    """Delete a user by email."""
    user = User.get_by_email(email)
    if user:
        confirm = input(f"Are you sure you want to delete user '{user.username}' ({email})? [y/N]: ")
        if confirm.lower() == 'y':
            user.delete()
            print(f"User '{user.username}' deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print(f"No user found with email: {email}")


def count_users():
    """Count total users in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    result = cursor.fetchone()
    conn.close()
    print(f"Total users: {result['count']}")


def show_schema():
    """Show the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print("\nUsers Table Schema:")
        print("-" * 40)
        print(result['sql'])
    else:
        print("Users table not found.")


def execute_raw(sql: str):
    """Execute a raw SQL query."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        
        if sql.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            if results:
                # Print column headers
                columns = results[0].keys()
                print("\n" + " | ".join(columns))
                print("-" * (len(" | ".join(columns)) + 10))
                for row in results:
                    print(" | ".join(str(row[col]) for col in columns))
                print(f"\n{len(results)} row(s) returned.")
            else:
                print("No results.")
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()


def print_usage():
    """Print usage instructions."""
    print(__doc__)


def main():
    # Ensure database exists
    init_db()
    
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        full_flag = len(sys.argv) >= 3 and sys.argv[2].lower() == "full"
        list_users(full=full_flag)
    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: python db_utils.py get <email>")
        else:
            get_user(sys.argv[2])
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python db_utils.py delete <email>")
        else:
            delete_user(sys.argv[2])
    elif command == "count":
        count_users()
    elif command == "schema":
        show_schema()
    elif command == "raw":
        if len(sys.argv) < 3:
            print("Usage: python db_utils.py raw \"<SQL>\"")
        else:
            execute_raw(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()
