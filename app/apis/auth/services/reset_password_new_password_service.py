from datetime import datetime

from apis.auth.schemas import NewPasswordData
from apis.auth.utils import update_user_password
from db.models import User
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from rate_limiting import limiter
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/reset-password/new-password",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
def set_new_password(
    request: Request,
    data: NewPasswordData,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or phone number",
        )

    if not user.reset_password_code:
        raise HTTPException(
            status_code=400,
            detail="Reset password process was not initiated via /reset-password!",
        )

    if datetime.now() > user.reset_password_code_expiry_date:
        raise HTTPException(
            status_code=400,
            detail="Reset password code expired!",
        )

    if user.reset_password_code != data.reset_password_code:
        raise HTTPException(
            status_code=400,
            detail="Invalid reset password code",
        )

    update_user_password(db, user.username, data.new_password)
    user.reset_password_code = None
    user.reset_password_code_expiry_date = None
    db.add(user)
    db.commit()

    return {"detail": "Password updated successfully!"}
