from typing import List

from apis.auth.utils import RolesBasedAuthChecker, get_current_user
from apis.orders import schemas
from db.models import Order, User, UserRole
from db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

router = APIRouter()


@router.get("/orders", response_model=List[schemas.Order])
def get_orders(
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    auth=Depends(RolesBasedAuthChecker([UserRole.CUSTOMER])),
):
    # Enforce maximum result set size to prevent resource exhaustion
    MAX_LIMIT = 100
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    
    # Validate skip parameter
    if skip < 0:
        skip = 0
    
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.date_ordered.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders
