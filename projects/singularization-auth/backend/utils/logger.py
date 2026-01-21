"""
Simple logging utilities for the SPS Auth Workflow application.

Uses print-based logging with prefixes for easy console tracking.
"""

from datetime import datetime


def _log(level: str, message: str) -> None:
    """Internal logging function with timestamp and level prefix."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {level} - {message}")


def log_info(message: str) -> None:
    """Log an informational message."""
    _log("INFO", message)


def log_debug(message: str) -> None:
    """Log a debug message."""
    _log("DEBUG", message)


def log_error(message: str) -> None:
    """Log an error message."""
    _log("ERROR", message)


def log_warning(message: str) -> None:
    """Log a warning message."""
    _log("WARNING", message)
