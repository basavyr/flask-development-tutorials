"""
Authentication routes for the SPS Auth Workflow application.

Handles login, signup, and logout functionality.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from backend.models import User
from backend.utils.password import validate_password
from backend.utils.logger import log_info, log_debug, log_error

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    """Redirect to dashboard if logged in, otherwise to login."""
    if "user_id" in session:
        return redirect(url_for("account.dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if "user_id" in session:
        return redirect(url_for("account.dashboard"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        if not email or not password:
            flash("Please enter both email and password", "error")
            return render_template("login.html")
        
        user = User.authenticate(email, password)
        
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["full_name"] = user.full_name
            log_info(f"User logged in: {user.username}")
            return redirect(url_for("account.dashboard"))
        else:
            flash("Invalid email or password", "error")
            log_debug(f"Failed login attempt for: {email}")
    
    return render_template("login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user registration."""
    if "user_id" in session:
        return redirect(url_for("account.dashboard"))
    
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validate required fields
        if not all([full_name, email, username, password, confirm_password]):
            flash("All fields are required", "error")
            return render_template("signup.html")
        
        # Check password confirmation
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template("signup.html")
        
        # Validate password requirements
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            flash(error_msg, "error")
            return render_template("signup.html")
        
        # Attempt to create user
        try:
            user = User.create(full_name, email, username, password)
            
            # Auto-login after registration
            session["user_id"] = user.id
            session["username"] = user.username
            session["full_name"] = user.full_name
            
            log_info(f"New user registered and logged in: {username}")
            flash(f"Welcome, {full_name}! Your account has been created.", "success")
            return redirect(url_for("account.dashboard"))
            
        except ValueError as e:
            flash(str(e), "error")
            log_debug(f"Registration failed: {e}")
        except Exception as e:
            flash("An error occurred during registration. Please try again.", "error")
            log_error(f"Registration error: {e}")
    
    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    """Handle user logout."""
    username = session.get("username", "Unknown")
    session.clear()
    log_info(f"User logged out: {username}")
    flash("You have been logged out successfully", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/api/singularization-log", methods=["POST"])
def singularization_log():
    """Log when singularization toggle is activated."""
    data = request.get_json() or {}
    page = data.get("page", "unknown")
    log_info(f"Singularization mode activated on {page}")
    return jsonify({"status": "logged", "message": "Singularization activation logged"})
