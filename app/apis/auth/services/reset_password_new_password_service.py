from datetime import datetime

from apis.auth.schemas import NewPasswordData
from apis.auth.utils import update_user_password
from db.models import User
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from rate_limiting import limiter
from sqlalchemy.orm import Session

ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 1 week

router = APIRouter()

# Track failed attempts per username to prevent brute force
failed_attempts = {}
MAX_FAILED_ATTEMPTS = 5


@router.post(
    "/reset-password/new-password",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")  # Rate limit to 5 attempts per minute
def set_new_password(
    request: Request,
    data: NewPasswordData,
    db: Session = Depends(get_db),
):
    # Check for too many failed attempts
    if data.username in failed_attempts and failed_attempts[data.username] >= MAX_FAILED_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Please request a new reset code.",
        )
    
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        # Use generic error message to prevent user enumeration
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials or reset code",
        )

    if not user.reset_password_code:
        raise HTTPException(
            status_code=400,
            detail="Reset password process was not initiated via /reset-password!",
        )

    if datetime.now() > user.reset_password_code_expiry_date:
        # Clear expired code
        user.reset_password_code = None
        user.reset_password_code_expiry_date = None
        db.add(user)
        db.commit()
        raise HTTPException(
            status_code=400,
            detail="Reset password code expired! Please request a new code.",
        )

    if user.reset_password_code != data.reset_password_code:
        # Track failed attempts
        failed_attempts[data.username] = failed_attempts.get(data.username, 0) + 1
        raise HTTPException(
            status_code=400,
            detail="Invalid reset password code",
        )

    # Success - reset counters
    if data.username in failed_attempts:
        del failed_attempts[data.username]
    
    update_user_password(db, user.username, data.new_password)
    user.reset_password_code = None
    user.reset_password_code_expiry_date = None
    db.add(user)
    db.commit()

    return {"detail": "Password updated successfully!"}
