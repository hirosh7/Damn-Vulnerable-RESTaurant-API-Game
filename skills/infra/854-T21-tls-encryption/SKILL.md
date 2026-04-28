---
name: 854-t21-tls-encryption
description: Ensure all data in transit is encrypted with TLS. Currently the app listens on HTTP (no TLS termination). A reverse proxy (nginx/Traefik) with TLS must be added in front of the FastAPI app.
---

# 854-T21: Ensure All Data in Transit Is Encrypted Using a Secure TLS Channel

**Category:** INFRA
**SD Elements:** [854-T21](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current State:**

The FastAPI app serves on HTTP port 8091 with no TLS. All authentication tokens, PII, and API traffic are sent in plaintext.

**Required Infrastructure Change:**

This is an INFRA-level fix. The application code change is to enforce HTTPS redirects and set HSTS headers:

**Code-side changes (app/init_app.py):**

```python
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

def create_app() -> FastAPI:
    app = FastAPI(...)
    
    # HTTPS redirect (only in production where TLS is terminated)
    if settings.ENVIRONMENT == "production":
        app.add_middleware(HTTPSRedirectMiddleware)
    
    # HSTS header (already present, verify it's set correctly)
    # Strict-Transport-Security: max-age=31536000; includeSubDomains
    return app
```

**Infrastructure-side changes (nginx reverse proxy):**

```nginx
# nginx.conf
server {
    listen 80;
    server_name api.example.com;
    return 301 https://$server_name$request_uri;  # Force HTTPS
}

server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    add_header Strict-Transport-Security "max-age=63072000" always;
    
    location / {
        proxy_pass http://web:8091;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Success Criteria:**

- All production traffic uses TLS 1.2+
- HSTS header is present with `max-age >= 31536000`
- HTTP traffic redirected to HTTPS
- TLS certificate from a trusted CA (Let's Encrypt acceptable)

**Status:** Pending — requires infrastructure deployment
