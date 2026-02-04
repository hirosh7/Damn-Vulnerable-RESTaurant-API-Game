from apis.auth.utils import RolesBasedAuthChecker, get_current_user, update_user
from apis.users.schemas import UserRoleUpdate
from db import models
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing_extensions import Annotated

router = APIRouter()


@router.put("/users/update_role", response_model=UserRoleUpdate)
async def update_user_role(
    user: UserRoleUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    auth=Depends(RolesBasedAuthChecker([models.UserRole.CHEF, models.UserRole.EMPLOYEE])),
):
    # This method allows authorized staff (CHEF and EMPLOYEE) to manage user roles
    
    # Prevent users from updating their own role
    if current_user.username == user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot modify your own role!",
        )
    
    # Get the target user to check their current role
    from apis.auth.utils import get_user_by_username
    target_user = get_user_by_username(db, user.username)
    
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Only Chef can assign Chef role
    if user.role == models.UserRole.CHEF.value:
        if current_user.role != models.UserRole.CHEF.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Chef is authorized to assign Chef role!",
            )
    
    # Only Chef can modify Chef accounts (prevent role demotion)
    if target_user.role == models.UserRole.CHEF:
        if current_user.role != models.UserRole.CHEF.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Chef is authorized to modify Chef accounts!",
            )

    db_user = update_user(db, user.username, user)
    return current_user
