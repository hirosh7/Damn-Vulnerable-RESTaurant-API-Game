import secrets
from datetime import datetime, timedelta

from apis.auth.utils import get_user_by_username
from apis.auth.utils.utils import send_code_to_phone_number
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from rate_limiting import limiter
from sqlalchemy.orm import Session

router = APIRouter()


class PhoneVerificationRequest(BaseModel):
    username: str


class PhoneVerificationConfirm(BaseModel):
    username: str
    code: str


@router.post(
    "/verify-phone/request",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("3/hour")  # Rate limit to prevent abuse
def request_phone_verification(
    request: Request,
    data: PhoneVerificationRequest,
    db: Session = Depends(get_db),
):
    """
    Request a phone verification code.
    This should be called after registration or when updating phone number.
    """
    user = get_user_by_username(db, data.username)
    if not user:
        # Use generic message to prevent user enumeration
        raise HTTPException(
            status_code=400,
            detail="Invalid request",
        )
    
    if user.phone_verified:
        raise HTTPException(
            status_code=400,
            detail="Phone number is already verified",
        )
    
    # Generate a cryptographically secure 6-digit code
    user.phone_verification_code = "".join(
        secrets.choice("0123456789") for _ in range(6)
    )
    
    # Set expiration to 10 minutes
    user.phone_verification_code_expiry = datetime.now() + timedelta(minutes=10)
    
    db.add(user)
    db.commit()
    
    # Send the verification code via SMS
    send_code_to_phone_number(user.phone_number, user.phone_verification_code)
    
    return {"detail": "Verification code sent to your phone number"}


@router.post(
    "/verify-phone/confirm",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/hour")  # Rate limit to prevent brute force
def confirm_phone_verification(
    request: Request,
    data: PhoneVerificationConfirm,
    db: Session = Depends(get_db),
):
    """
    Confirm phone verification with the code sent via SMS.
    """
    user = get_user_by_username(db, data.username)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code",
        )
    
    if user.phone_verified:
        raise HTTPException(
            status_code=400,
            detail="Phone number is already verified",
        )
    
    # Check if code exists and matches
    if not user.phone_verification_code or user.phone_verification_code != data.code:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code",
        )
    
    # Check if code is expired
    if not user.phone_verification_code_expiry or user.phone_verification_code_expiry < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Verification code has expired. Please request a new one.",
        )
    
    # Mark phone as verified and clear verification code
    user.phone_verified = True
    user.phone_verification_code = None
    user.phone_verification_code_expiry = None
    
    db.add(user)
    db.commit()
    
    return {"detail": "Phone number verified successfully"}
