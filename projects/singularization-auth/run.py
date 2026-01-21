"""
SPS Auth Workflow - Application Entry Point

Run this file to start the Flask development server.
Usage: python run.py
"""

from backend.app import create_app
from backend.config import Config

app = create_app()

if __name__ == "__main__":
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
