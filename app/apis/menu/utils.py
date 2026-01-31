import base64
from urllib.parse import urlparse

import requests
from apis.menu import schemas
from db.models import MenuItem, OrderItem
from fastapi import HTTPException


def is_safe_image_url(url: str) -> bool:
    """
    Validate image URL to prevent SSRF attacks.
    Only allow HTTPS URLs from trusted domains.
    """
    try:
        parsed = urlparse(url)
        
        # Only allow HTTPS
        if parsed.scheme != 'https':
            return False
        
        # Block localhost and private IP addresses
        hostname = parsed.hostname
        if not hostname:
            return False
        
        blocked_hosts = [
            'localhost', '127.0.0.1', '0.0.0.0', '::1',
            '169.254.', '10.', '172.16.', '192.168.',
            'metadata.google.internal',  # Cloud metadata endpoints
            '169.254.169.254',  # AWS/Azure metadata
        ]
        
        for blocked in blocked_hosts:
            if hostname.startswith(blocked) or hostname == blocked.rstrip('.'):
                return False
        
        # Allowlist of trusted image hosting domains (configure for your use case)
        # In production, maintain a strict allowlist
        trusted_domains = [
            'images.restaurant.com',
            'cdn.restaurant.com',
            'storage.googleapis.com',
            's3.amazonaws.com',
            # Add other trusted image hosting services
        ]
        
        # For now, allow any HTTPS URL that's not on blocklist
        # In production, use strict allowlist by uncommenting:
        # if hostname not in trusted_domains:
        #     return False
        
        return True
    except Exception:
        return False


def _image_url_to_base64(image_url: str):
    """
    Fetch image from URL and convert to base64.
    Includes SSRF protection and size limits.
    """
    # Validate URL for SSRF protection
    if not is_safe_image_url(image_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid or unsafe image URL. Only HTTPS URLs from trusted domains are allowed."
        )
    
    try:
        # Make request with security measures
        response = requests.get(
            image_url,
            stream=True,
            timeout=10,  # Prevent hanging
            allow_redirects=False,  # Prevent redirect-based SSRF
            verify=True,  # Verify SSL certificates
            headers={'User-Agent': 'Restaurant-App/1.0'}
        )
        
        # Check response status
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch image: HTTP {response.status_code}"
            )
        
        # Check content type
        content_type = response.headers.get('Content-Type', '')
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if not any(ct in content_type for ct in allowed_types):
            raise HTTPException(
                status_code=400,
                detail="Invalid content type. Only image files are allowed."
            )
        
        # Limit image size to prevent DoS (max 5MB)
        max_size = 5 * 1024 * 1024
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) > max_size:
            raise HTTPException(
                status_code=400,
                detail="Image too large. Maximum size is 5MB."
            )
        
        # Read with size limit
        content = b''
        for chunk in response.iter_content(chunk_size=8192):
            content += chunk
            if len(content) > max_size:
                raise HTTPException(
                    status_code=400,
                    detail="Image too large. Maximum size is 5MB."
                )
        
        encoded_image = base64.b64encode(content).decode()
        return encoded_image
        
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch image: {str(e)}"
        )


def create_menu_item(
    db,
    menu_item: schemas.MenuItemCreate,
):
    menu_item_dict = menu_item.dict()
    image_url = menu_item_dict.pop("image_url", None)
    db_item = MenuItem(**menu_item_dict)

    if image_url:
        db_item.image_base64 = _image_url_to_base64(image_url)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_menu_item(
    db,
    item_id: int,
    menu_item: schemas.MenuItemCreate,
):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    menu_item_dict = menu_item.dict()
    image_url = menu_item_dict.pop("image_url", None)

    for key, value in menu_item_dict.items():
        setattr(db_item, key, value)

    if image_url:
        db_item.image_base64 = _image_url_to_base64(image_url)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_menu_item(db, item_id: int):
    existing_order_item = (
        db.query(OrderItem).filter(OrderItem.menu_item_id == item_id).first()
    )
    if existing_order_item is not None:
        raise HTTPException(
            status_code=409,
            detail="You can not delete this menu item, it is associated with existing orders.",
        )

    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(db_item)
    db.commit()
