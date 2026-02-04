from typing import List

from apis.orders import schemas
from db.models import Order
from db.session import get_db
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

router = APIRouter()

# In production, this should be stored securely (e.g., in environment variables)
# and use proper API key management
VALID_API_KEYS = set([
    # These would be issued to authorized delivery service partners
    # In real implementation, store these in a database with proper management
])


def verify_delivery_service_api_key(x_api_key: str = Header(None)):
    """
    Verify that the request includes a valid API key from an authorized delivery service.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Include X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    # Validate against the set of valid API keys
    # In production, validate against database of registered delivery services
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key. Access denied.",
        )
    
    return x_api_key


@router.get(
    "/delivery/orders",
    response_model=List[schemas.Order],
    # Exclude from public API docs but keep internal documentation
    include_in_schema=False,
)
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_delivery_service_api_key),
):
    """
    This is a dedicated endpoint for AUTHENTICATED delivery services to integrate with
    the Restaurant. Requires a valid API key in X-API-Key header.
    
    Only authorized delivery service partners can access this endpoint.
    """
    # Enforce reasonable limits to prevent data exposure
    if limit > 100:
        limit = 100
    
    orders = (
        db.query(Order)
        .order_by(Order.date_ordered.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return orders
