from typing import Optional

from pydantic import BaseModel, Field, validator


class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Menu item name")
    price: float = Field(..., gt=0, lt=10000, description="Price must be positive and reasonable")
    category: str = Field(..., min_length=1, max_length=100, description="Menu item category")
    image_url: Optional[str] = Field(None, max_length=2048, description="HTTPS URL to menu item image")
    description: Optional[str] = Field(None, max_length=1000, description="Menu item description")
    
    @validator('name', 'category', 'description')
    def validate_text_fields(cls, v, field):
        """Validate text fields for XSS and injection attempts"""
        if v is None:
            return v
        
        # Check for suspicious patterns
        suspicious_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=']
        v_lower = v.lower()
        for pattern in suspicious_patterns:
            if pattern in v_lower:
                raise ValueError(f'{field.name} contains invalid characters')
        
        return v.strip()
    
    @validator('price')
    def validate_price(cls, v):
        """Validate price is reasonable"""
        if v <= 0:
            raise ValueError('Price must be positive')
        if v > 10000:
            raise ValueError('Price seems unreasonably high')
        # Limit to 2 decimal places
        return round(v, 2)
    
    @validator('image_url')
    def validate_image_url(cls, v):
        """Validate image URL is HTTPS"""
        if v is None:
            return v
        if not v.startswith('https://'):
            raise ValueError('Image URL must use HTTPS protocol')
        if len(v) > 2048:
            raise ValueError('Image URL is too long')
        return v


class MenuItem(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: Optional[str] = None
    image_base64: Optional[str] = None
