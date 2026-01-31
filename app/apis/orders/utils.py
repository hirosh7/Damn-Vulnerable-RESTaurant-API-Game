from urllib.parse import urlparse

from fastapi import HTTPException


def is_safe_url(url: str) -> bool:
    """
    Validate URL to prevent Server-Side Request Forgery (SSRF) attacks.
    Only allow requests to trusted delivery service domains.
    """
    try:
        parsed = urlparse(url)
        
        # Only allow HTTPS
        if parsed.scheme != 'https':
            return False
        
        # Allowlist of trusted delivery service domains
        trusted_domains = [
            'delivery.service',
            'api.deliverypartner.com',
            # Add other trusted delivery service domains here
        ]
        
        # Check if hostname is in trusted list
        if parsed.hostname not in trusted_domains:
            return False
        
        # Prevent requests to private IP ranges
        # Additional check: ensure hostname doesn't resolve to private IP
        import socket
        try:
            ip = socket.gethostbyname(parsed.hostname)
            # Check for private IP ranges
            if ip.startswith(('127.', '10.', '192.168.', '172.')):
                return False
            if ip.startswith('169.254.'):  # Link-local
                return False
        except socket.gaierror:
            return False
        
        return True
    except Exception:
        return False


def fetch_order_status_from_delivery_service(order_id: int):
    """
    Fetches order status from an external delivery service with SSRF protection.
    
    Security measures:
    - URL validation against allowlist of trusted domains
    - HTTPS-only connections
    - Timeout protection
    - Response validation
    """
    
    # Simulate external API call
    # In a real implementation, uncomment and use proper SSRF protection:
    #
    # import requests
    # 
    # delivery_url = f"https://delivery.service/api/orders/{order_id}"
    # 
    # # Validate URL before making request
    # if not is_safe_url(delivery_url):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Invalid delivery service URL"
    #     )
    # 
    # try:
    #     response = requests.get(
    #         delivery_url,
    #         timeout=5,  # Prevent hanging
    #         verify=True,  # Verify SSL certificates
    #         allow_redirects=False  # Prevent redirect-based SSRF
    #     )
    #     response.raise_for_status()
    #     delivery_data = response.json()
    #     
    #     # Validate response structure
    #     required_fields = ['order_id', 'status']
    #     if not all(field in delivery_data for field in required_fields):
    #         raise HTTPException(status_code=502, detail="Invalid response from delivery service")
    #     
    #     return delivery_data
    # except requests.RequestException as e:
    #     raise HTTPException(status_code=502, detail="Failed to contact delivery service")

    # Simulated response for educational purposes
    return {
        "order_id": order_id,
        "status": "ON_THE_WAY",
        "delivery_notes": "Your order is on the way!",
    }
