"""
Secure logging configuration for the application.
Implements T2602 and T349 countermeasures.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import ENVIRONMENT, ENV


def setup_secure_logging():
    """
    Configure secure logging with:
    - Separate log files for different log levels
    - Log rotation to prevent disk exhaustion
    - Restricted file permissions
    - Structured logging format
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Set restrictive permissions on log directory (owner read/write only)
    try:
        os.chmod(log_dir, 0o700)
    except Exception:
        pass  # May not have permission in some environments
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if ENVIRONMENT == ENV.PRODUCTION else logging.DEBUG)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters with structured logging
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Security events log (authentication, authorization, access control)
    security_handler = RotatingFileHandler(
        'logs/security.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    security_handler.setLevel(logging.INFO)
    security_handler.setFormatter(detailed_formatter)
    
    # Application log (general application events)
    app_handler = RotatingFileHandler(
        'logs/application.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(detailed_formatter)
    
    # Error log (errors and exceptions)
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Console handler for development
    if ENVIRONMENT == ENV.DEVELOPMENT:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(console_handler)
    
    # Add all handlers
    root_logger.addHandler(security_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    
    # Set restrictive permissions on log files
    for log_file in ['logs/security.log', 'logs/application.log', 'logs/error.log']:
        if os.path.exists(log_file):
            try:
                os.chmod(log_file, 0o600)  # Owner read/write only
            except Exception:
                pass
    
    return root_logger


def log_security_event(event_type: str, username: str, details: str, success: bool = True):
    """
    Log security-relevant events (authentication, authorization, access control).
    
    Args:
        event_type: Type of security event (LOGIN, LOGOUT, ACCESS_DENIED, etc.)
        username: Username involved in the event
        details: Additional details about the event
        success: Whether the operation succeeded
    """
    logger = logging.getLogger("security")
    status = "SUCCESS" if success else "FAILURE"
    logger.info(f"[{event_type}] [{status}] User: {username} - {details}")


def sanitize_for_logging(data: str, max_length: int = 100) -> str:
    """
    Sanitize data before logging to prevent log injection and limit size.
    
    Args:
        data: Data to sanitize
        max_length: Maximum length to log
        
    Returns:
        Sanitized string safe for logging
    """
    if not data:
        return ""
    
    # Remove newlines and carriage returns to prevent log injection
    sanitized = data.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # Truncate to max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized
