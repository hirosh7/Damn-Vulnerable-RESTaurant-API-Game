---
name: 854-t374-offload-http-handling
description: Place a dedicated reverse proxy (nginx, Traefik, or AWS ALB) in front of the FastAPI/Uvicorn server to handle TLS, request filtering, rate limiting, and connection management at the infrastructure layer.
---

# 854-T374: Offload HTTP Request Handling to Dedicated Modules

**Category:** INFRA
**SD Elements:** [854-T374](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Current State:**

Uvicorn directly handles all HTTP connections. There is no reverse proxy layer. Uvicorn is an ASGI server, not designed to be a public-facing edge server.

**Required Infrastructure Change:**

Add nginx as a reverse proxy in `docker-compose.yml`:

```yaml
# docker-compose.yml — add nginx service
services:
  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      - web
    networks:
      - frontend

  web:
    # Remove external port exposure — only accessible via nginx
    # ports:
    #  - "8091:8091"   # REMOVE — expose only through nginx
    expose:
      - "8091"         # Internal-only port
    networks:
      - frontend
      - backend

  db:
    # No external port exposure for DB
    expose:
      - "5432"
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true     # DB network not reachable from outside
```

**nginx configuration:**

```nginx
# nginx/nginx.conf
upstream api {
    server web:8091;
    keepalive 32;
}

server {
    listen 80;
    client_max_body_size 10M;     # Request size limit (see T536)
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Strip server header
    server_tokens off;
    
    location / {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
}
```

**Success Criteria:**

- nginx reverse proxy in front of Uvicorn
- Database port not exposed externally
- TLS terminated at nginx (see T21)
- `server_tokens off` to hide nginx version

**Status:** Pending — requires infrastructure deployment
