from datetime import datetime, timedelta

from apis.auth.schemas import Token
from apis.auth.utils import authenticate_user, create_access_token
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from rate_limiting import limiter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Track failed login attempts per username
# In production, use Redis or database for distributed systems
failed_login_attempts = {}
LOCKOUT_THRESHOLD = 5
LOCKOUT_DURATION_MINUTES = 15


@router.post("/token")
@limiter.limit("10/minute")  # Rate limit login attempts
async def get_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    username = form_data.username
    
    # Check if account is locked out
    if username in failed_login_attempts:
        attempt_data = failed_login_attempts[username]
        if attempt_data['count'] >= LOCKOUT_THRESHOLD:
            lockout_until = attempt_data['locked_until']
            if datetime.now() < lockout_until:
                remaining = int((lockout_until - datetime.now()).total_seconds() / 60)
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Account temporarily locked due to too many failed attempts. Try again in {remaining} minutes.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                # Lockout expired, reset counter
                del failed_login_attempts[username]
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Track failed attempt
        if username not in failed_login_attempts:
            failed_login_attempts[username] = {'count': 0, 'locked_until': None}
        
        failed_login_attempts[username]['count'] += 1
        
        # Lock account after threshold reached
        if failed_login_attempts[username]['count'] >= LOCKOUT_THRESHOLD:
            failed_login_attempts[username]['locked_until'] = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
        
        # Use generic error message to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Successful login - reset failed attempts
    if username in failed_login_attempts:
        del failed_login_attempts[username]
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
