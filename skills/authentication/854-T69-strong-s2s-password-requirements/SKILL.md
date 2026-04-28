---
name: 854-t69-strong-s2s-password-requirements
description: Replace hardcoded weak PostgreSQL credentials in docker-compose.yml. The current password is "password" — enforce strong credentials for server-to-server auth.
---

# 854-T69: Strong Password Requirements for Server-to-Server System Accounts

**Category:** CODE_FIX
**SD Elements:** [854-T69](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Vulnerable Code:**

```yaml
# docker-compose.yml lines 16-20
environment:
  - POSTGRES_USER=admin
  - POSTGRES_PASSWORD=password   # WEAK: default/trivial password
  - POSTGRES_SERVER=db
  - POSTGRES_PORT=5432
  - POSTGRES_DB=restaurant
```

```python
# app/config.py lines 44-49
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")  # WEAK default
```

**Required Fix:**

1. Remove hardcoded `password` defaults from config.py.
2. In docker-compose.yml, use a Docker secret or at minimum a stronger placeholder.
3. Document that `POSTGRES_PASSWORD` must be set from environment in production.

```python
# app/config.py — remove weak defaults
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "dbuser")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
if not POSTGRES_PASSWORD:
    raise RuntimeError("POSTGRES_PASSWORD environment variable is required")
```

**For docker-compose.yml (development):**

```yaml
environment:
  - POSTGRES_USER=${POSTGRES_USER:-dbuser}
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}  # must be set in .env
```

Add a `.env.example` with instructions.

**Success Criteria:**

- No hardcoded credentials in source code or docker-compose
- `POSTGRES_PASSWORD` required at startup
- Minimum 20-character password in deployment docs

**Status:** Pending
