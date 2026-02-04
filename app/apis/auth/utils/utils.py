import logging
from datetime import datetime, timedelta, timezone
from typing import Union

from apis.auth.exceptions import UserAlreadyExistsException
from config import Settings
from db.models import User, UserRole
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = Settings.JWT_SECRET_KEY
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_username(db, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    return user


def get_user_by_id(db, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    return user


def update_user_password(db, username: str, password: str) -> User:
    db_user = get_user_by_username(db, username)
    db_user.password = get_password_hash(password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_phone_number(db, phone_number: str) -> User:
    user = db.query(User).filter(User.phone_number == phone_number).first()
    return user


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_user(
    db,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    phone_number: str,
    role: str = UserRole.CUSTOMER,
):
    if get_user_by_phone_number(db, phone_number) or get_user_by_username(db, username):
        raise UserAlreadyExistsException()

    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_user_if_not_exists(
    db,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    phone_number: str,
    role: str = UserRole.CUSTOMER,
):
    try:
        return create_user(
            db, username, password, first_name, last_name, phone_number, role
        )
    except UserAlreadyExistsException:
        return None


def update_user(db, username: str, user):
    db_user = get_user_by_username(db, username)

    for var, value in vars(user).items():
        if value:
            setattr(db_user, var, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def send_code_to_phone_number(phone_number: str, code: str):
    """
    Send password reset code via SMS.
    In production, integrate with SMS provider (Twilio, AWS SNS, etc.).
    
    Args:
        phone_number: Recipient phone number
        code: Password reset code (sensitive - never log)
    
    Returns:
        bool: True if successful
    """
    # Mask phone number for secure logging (show only last 4 digits)
    if phone_number and len(phone_number) >= 4:
        masked_phone = '*' * (len(phone_number) - 4) + phone_number[-4:]
    else:
        masked_phone = '****'
    
    # Log the event without sensitive data
    logger = logging.getLogger("security")
    logger.info(f"Password reset code sent to phone ending in {masked_phone[-4:]}")
    
    # TODO: In production, integrate with actual SMS provider
    # Example: twilio_client.messages.create(to=phone_number, body=f"Your code: {code}")
    
    # For development/testing only - remove in production
    # DO NOT print sensitive codes to stdout/logs in production
    print(f"[DEV ONLY] Code sent to {masked_phone}")
    
    return True
