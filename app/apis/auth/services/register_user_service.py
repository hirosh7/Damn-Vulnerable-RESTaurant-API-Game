import secrets
from datetime import datetime, timedelta

from apis.auth.exceptions import UserAlreadyExistsException
from apis.auth.password_validator import validate_password_strength
from apis.auth.schemas import UserCreate, UserRead
from apis.auth.utils import create_user
from apis.auth.utils.utils import send_code_to_phone_number
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from rate_limiting import limiter
from sqlalchemy.orm import Session

ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 1 week

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/hour")  # Rate limit registration to prevent abuse
async def register_user(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    auth = request.headers.get("Authorization")

    if auth:
        raise HTTPException(
            status_code=400,
            detail="You're already logged in. You can not register an account.",
        )

    # Validate password strength
    is_valid, error_message = validate_password_strength(user.password)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=error_message,
        )

    try:
        db_user = create_user(
            db,
            user.username,
            user.password,
            user.first_name,
            user.last_name,
            user.phone_number,
        )
        
        # Generate and send phone verification code
        verification_code = "".join(
            secrets.choice("0123456789") for _ in range(6)
        )
        db_user.phone_verification_code = verification_code
        db_user.phone_verification_code_expiry = datetime.now() + timedelta(minutes=10)
        db_user.phone_verified = False
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send verification code via SMS
        send_code_to_phone_number(db_user.phone_number, verification_code)
        
    except UserAlreadyExistsException:
        # Use generic message to prevent user enumeration
        raise HTTPException(
            status_code=400,
            detail="Registration failed. Please check your information.",
        )
    except Exception as e:
        # Log the actual error for debugging but don't expose to user
        # logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Registration failed. Please try again later.",
        )

    return db_user
