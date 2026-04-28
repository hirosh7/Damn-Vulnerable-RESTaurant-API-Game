---
name: 854-t76-no-hardcoded-passwords
description: Remove hardcoded credentials from docker-compose.yml and config.py. The PostgreSQL password "password" and default usernames must not be hardcoded.
---

# 854-T76: Do Not Hardcode Passwords

**Category:** CODE_FIX
**SD Elements:** [854-T76](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 10

**Vulnerable Locations:**

1. `docker-compose.yml` lines 16-19: `POSTGRES_PASSWORD=password`
2. `app/config.py` line 47: `os.getenv("POSTGRES_PASSWORD", "password")`
3. `app/config.py` line 43: `CHEF_USERNAME = os.getenv("CHEF_USERNAME", "chef")`

**Required Fix:**

```python
# app/config.py — remove default values for secrets
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
if not POSTGRES_PASSWORD:
    if ENVIRONMENT == ENV.PRODUCTION:
        raise RuntimeError("POSTGRES_PASSWORD must be set in production")
    POSTGRES_PASSWORD = "dev-password-not-for-prod"  # dev-only fallback
```

```yaml
# docker-compose.yml — use .env file or Docker secrets
services:
  web:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}  # must be set in .env
  db:
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

Create a `.env.example` file:

```bash
# .env.example
POSTGRES_USER=dvrag_user
POSTGRES_PASSWORD=<generate-strong-password-here>
JWT_SECRET_KEY=<generate-with: python3 -c "import secrets; print(secrets.token_hex(32))">
```

Add `.env` to `.gitignore`.

**Success Criteria:**

- No hardcoded passwords in any tracked source file
- `.env.example` exists with documentation
- `.env` is in `.gitignore`

**Status:** Pending
