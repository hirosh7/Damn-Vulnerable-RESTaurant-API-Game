---
name: 854-t156-validate-certificate-chain
description: Ensure certificate validation is enabled for all external HTTP requests. The app uses requests.get() to download menu images from user-supplied URLs without explicit certificate validation.
---

# 854-T156: Validate Certificate and Its Chain of Trust Properly

**Category:** CODE_FIX
**SD Elements:** [854-T156](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Relevant Code:**

```python
# app/apis/menu/utils.py:9-13
def _image_url_to_base64(image_url: str):
    response = requests.get(image_url, stream=True)  # VERIFY not explicit
    encoded_image = base64.b64encode(response.content).decode()
    return encoded_image
```

The `requests` library verifies SSL certificates by default (`verify=True`), but this should be explicitly enforced and documented.

**Required Fix:**

1. Explicitly set `verify=True` in all `requests.get()` calls.
2. Set a timeout to prevent SSRF-induced hangs (cross-reference T1365).
3. Validate the URL is HTTPS before making the request.

```python
# app/apis/menu/utils.py — secure image fetching
import certifi
from urllib.parse import urlparse

ALLOWED_IMAGE_DOMAINS = {"cdn.example.com", "images.restaurant.com"}
IMAGE_FETCH_TIMEOUT = 5  # seconds

def _image_url_to_base64(image_url: str):
    parsed = urlparse(image_url)
    if parsed.scheme != "https":
        raise ValueError("Only HTTPS URLs are allowed for images")
    if parsed.netloc not in ALLOWED_IMAGE_DOMAINS:
        raise ValueError(f"Domain '{parsed.netloc}' is not in the allowed list")
    response = requests.get(
        image_url,
        stream=True,
        verify=certifi.where(),  # explicit cert validation
        timeout=IMAGE_FETCH_TIMEOUT,
    )
    response.raise_for_status()
    return base64.b64encode(response.content).decode()
```

**Note:** The domain allowlist should also address SSRF (T1365) — coordinate these fixes.

**Success Criteria:**

- All external HTTP requests use `verify=True` with certifi
- Timeout is set on all external requests
- Only HTTPS URLs are accepted

**Status:** Pending
