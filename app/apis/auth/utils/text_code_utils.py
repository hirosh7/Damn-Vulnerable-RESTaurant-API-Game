import secrets
from datetime import datetime, timedelta

from db.models import User
from sqlalchemy.orm import Session

from .utils import send_code_to_phone_number


def generate_and_send_code_to_user(user: User, db: Session):
    """
    Generate a secure password reset code.
    Uses 8-digit alphanumeric code with 15 minutes expiration.
    """
    # Generate a cryptographically secure 8-character code (alphanumeric)
    # This provides significantly more entropy than 4 digits
    # 8 alphanumeric chars = 62^8 = 218 trillion possibilities vs 4 digits = 10,000
    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    user.reset_password_code = "".join(secrets.choice(characters) for _ in range(8))
    
    # Use shorter expiration window for security - 10 minutes instead of 15
    user.reset_password_code_expiry_date = datetime.now() + timedelta(minutes=10)
    db.add(user)
    db.commit()

    success = send_code_to_phone_number(user.phone_number, user.reset_password_code)
    return success
