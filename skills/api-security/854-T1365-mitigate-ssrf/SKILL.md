---
name: 854-t1365-mitigate-ssrf
description: Fix the SSRF vulnerability in _image_url_to_base64() in app/apis/menu/utils.py. This is the Level 4 vulnerability allowing attackers to make the server fetch internal endpoints.
---

# 854-T1365: Mitigate Server Side Request Forgery

**Category:** CODE_FIX
**SD Elements:** [854-T1365](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Vulnerability (Level 4 — SSRF):**

```python
# app/apis/menu/utils.py:9-13
def _image_url_to_base64(image_url: str):
    response = requests.get(image_url, stream=True)  # SSRF vulnerability
    encoded_image = base64.b64encode(response.content).decode()
    return encoded_image
```

An attacker can submit `image_url = "http://localhost:8091/admin/reset-chef-password"` to make the server fetch internal endpoints.

**Required Fix:**

Implement strict URL validation with an allowlist of trusted domains:

```python
# app/apis/menu/utils.py — SSRF fix
import ipaddress
import socket
from urllib.parse import urlparse
import certifi

ALLOWED_IMAGE_DOMAINS = frozenset({
    "cdn.restaurant.com",
    "images.restaurant.com",
    "static.restaurant.com",
})
PRIVATE_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
]

def _validate_image_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP/HTTPS URLs are allowed")
    if parsed.netloc not in ALLOWED_IMAGE_DOMAINS:
        raise ValueError(f"Domain '{parsed.netloc}' is not in the allowlist")
    # Resolve IP and check for private ranges
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
        for private_range in PRIVATE_RANGES:
            if ip in private_range:
                raise ValueError("URL resolves to a private/internal IP address")
    except socket.gaierror:
        raise ValueError("Cannot resolve domain")

def _image_url_to_base64(image_url: str):
    _validate_image_url(image_url)
    response = requests.get(
        image_url,
        stream=True,
        verify=certifi.where(),
        timeout=5,
        allow_redirects=False,  # prevent redirect-based SSRF
    )
    response.raise_for_status()
    # Validate content type
    content_type = response.headers.get("content-type", "")
    if not content_type.startswith("image/"):
        raise ValueError("URL does not point to an image")
    return base64.b64encode(response.content).decode()
```

**Success Criteria:**

- Level 4 SSRF vulnerability test no longer passes
- Only allowlisted domains accepted
- Private IP addresses rejected
- Redirects disabled

**Status:** Pending
