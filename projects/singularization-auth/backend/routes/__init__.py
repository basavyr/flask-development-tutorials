"""
Route blueprints for the SPS Auth Workflow application.
"""

from backend.routes.auth import auth_bp
from backend.routes.account import account_bp

__all__ = ["auth_bp", "account_bp"]
