from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    ON_THE_WAY = "OnTheWay"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderItem(BaseModel):
    menu_item_id: int = Field(..., gt=0, description="Menu item ID must be positive")
    quantity: int = Field(..., gt=0, le=100, description="Quantity must be between 1 and 100")


class OrderBase(BaseModel):
    delivery_address: str = Field(..., min_length=5, max_length=500, description="Delivery address")
    phone_number: str = Field(..., min_length=10, max_length=20, description="Phone number")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        """Validate phone number format"""
        # Remove common separators
        cleaned = v.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if not cleaned.isdigit():
            raise ValueError('Phone number must contain only digits and separators')
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise ValueError('Phone number length must be between 10 and 15 digits')
        return v
    
    @validator('delivery_address')
    def validate_address(cls, v):
        """Validate address doesn't contain suspicious content"""
        if not v or not v.strip():
            raise ValueError('Delivery address is required')
        # Check for suspicious patterns
        suspicious = ['<script', 'javascript:', 'onerror=']
        v_lower = v.lower()
        for pattern in suspicious:
            if pattern in v_lower:
                raise ValueError('Address contains invalid characters')
        return v.strip()


class OrderCreate(OrderBase):
    items: List[OrderItem] = Field(..., min_items=1, max_items=50, description="Order items (1-50)")
    coupon_id: Optional[int] = Field(None, gt=0, description="Discount coupon ID")
    
    @validator('items')
    def validate_items(cls, v):
        """Validate items list is not empty"""
        if not v:
            raise ValueError('Order must contain at least one item')
        return v


class Order(OrderBase):
    id: int
    user_id: int
    items: List[OrderItem] = []
    status: OrderStatus
    final_price: float

    class Config:
        from_attributes = True
