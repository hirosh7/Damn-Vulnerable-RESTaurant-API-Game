import secrets
from datetime import datetime, timedelta

from db.models import User
from sqlalchemy.orm import Session

from .utils import send_code_to_phone_number


def generate_and_send_code_to_user(user: User, db: Session):
    # 8-digit PIN (100,000,000 combinations) with a 10-minute expiry window.
    user.reset_password_code = "".join([str(secrets.randbelow(10)) for _ in range(8)])
    user.reset_password_code_expiry_date = datetime.now() + timedelta(minutes=10)
    db.add(user)
    db.commit()

    success = send_code_to_phone_number(user.phone_number, user.reset_password_code)
    return success
