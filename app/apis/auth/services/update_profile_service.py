from typing import Union

from apis.auth.utils import get_current_user, get_user_by_username
from db.models import User
from db.session import get_db
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Annotated

router = APIRouter()


class UserUpdate(BaseModel):
    # Remove username from update fields - users can only update their own profile
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone_number: Union[str, None] = None

    class Config:
        # Prevent extra fields to avoid mass assignment
        extra = "forbid"


@router.put("/profile", response_model=UserUpdate, status_code=status.HTTP_200_OK)
def update_profile(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    # CRITICAL: Update only the current user's profile (fix IDOR vulnerability)
    # Users cannot update other users' profiles
    db_user = get_user_by_username(db, current_user.username)
    
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Only update allowed fields explicitly
    allowed_fields = {'first_name', 'last_name', 'phone_number'}
    for var, value in user.dict(exclude_unset=True).items():
        if var in allowed_fields and value is not None:
            setattr(db_user, var, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
