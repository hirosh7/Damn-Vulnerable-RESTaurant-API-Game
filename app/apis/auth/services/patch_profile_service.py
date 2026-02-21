from typing import Union

from apis.auth.utils import get_current_user, get_user_by_username
from db.models import User
from db.session import get_db
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing_extensions import Annotated

router = APIRouter()

# Explicit allowlist of fields a user is permitted to update on their own
# profile. Extra.allow is intentionally NOT used here; any unknown field in
# the request body is silently ignored, preventing mass-assignment attacks
# that could allow a user to elevate their own role or tamper with other
# protected attributes.
UPDATABLE_FIELDS = {"first_name", "last_name", "phone_number"}


class UserRead(BaseModel):
    username: str
    phone_number: str
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    role: str


class UserUpdate(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone_number: Union[str, None] = None


@router.patch("/profile", response_model=UserRead, status_code=status.HTTP_200_OK)
def patch_profile(
    user: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_username(db, current_user.username)

    for field in UPDATABLE_FIELDS:
        value = getattr(user, field, None)
        if value is not None:
            setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
