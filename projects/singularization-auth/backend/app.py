"""
Flask application factory for the SPS Auth Workflow application.

Creates and configures the Flask application with all blueprints registered.
"""

import os
from flask import Flask
from backend.config import Config
from backend.database import init_db
from backend.routes import auth_bp, account_bp
from backend.utils.logger import log_info


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Configured Flask application instance.
    """
    # Determine paths for templates and static files
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "frontend", "templates")
    static_dir = os.path.join(base_dir, "frontend", "static")
    
    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )
    
    # Configure the application
    app.secret_key = Config.FLASK_SECRET_KEY
    
    # Initialize the database
    init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)
    
    log_info("SPS Auth Workflow application started")
    log_info(f"Debug mode: {Config.FLASK_DEBUG}")
    log_info(f"Database: {Config.DATABASE_PATH}")
    
    return app
