"""
Account management routes for the SPS Auth Workflow application.

Handles dashboard, settings, and account deletion.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from backend.models import User
from backend.utils.logger import log_info, log_debug, log_error

account_bp = Blueprint("account", __name__)


def login_required(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


@account_bp.route("/dashboard")
@login_required
def dashboard():
    """Display the user dashboard."""
    user = User.get_by_id(session["user_id"])
    
    if not user:
        session.clear()
        flash("Session expired. Please log in again.", "error")
        return redirect(url_for("auth.login"))
    
    log_debug(f"Dashboard accessed by: {user.username}")
    return render_template("dashboard.html", user=user)


@account_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Handle account settings."""
    user = User.get_by_id(session["user_id"])
    
    if not user:
        session.clear()
        flash("Session expired. Please log in again.", "error")
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        new_name = request.form.get("full_name", "").strip()
        
        if not new_name:
            flash("Full name cannot be empty", "error")
        elif new_name != user.full_name:
            if user.update_full_name(new_name):
                session["full_name"] = new_name
                flash("Your name has been updated successfully", "success")
            else:
                flash("Failed to update your name. Please try again.", "error")
        else:
            flash("No changes were made", "info")
    
    # Refresh user data
    user = User.get_by_id(session["user_id"])
    return render_template("settings.html", user=user)


@account_bp.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    """Handle account deletion."""
    user = User.get_by_id(session["user_id"])
    
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))
    
    username = user.username
    
    if user.delete():
        session.clear()
        log_info(f"Account deleted by user: {username}")
        flash("Your account has been deleted successfully", "info")
        return redirect(url_for("auth.login"))
    else:
        flash("Failed to delete account. Please try again.", "error")
        return redirect(url_for("account.settings"))
