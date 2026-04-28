---
name: 854-t19-restrict-db-access
description: Apply principle of least privilege to the PostgreSQL database account. The app uses "admin" user with likely superuser privileges. Create a dedicated limited-privilege account.
---

# 854-T19: Restrict Application's Access to Database

**Category:** CODE_FIX
**SD Elements:** [854-T19](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Issue:**

```yaml
# docker-compose.yml lines 27-28
environment:
  - POSTGRES_USER=admin  # likely SUPERUSER — too privileged
```

The `admin` PostgreSQL user is the database owner (created by `POSTGRES_USER` env var), giving the app superuser-level access.

**Required Fix:**

Create a dedicated application user with minimal permissions:

```sql
-- init.sql — run during database initialization
CREATE USER dvrag_app WITH PASSWORD 'your-secure-password';
GRANT CONNECT ON DATABASE restaurant TO dvrag_app;
GRANT USAGE ON SCHEMA public TO dvrag_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dvrag_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO dvrag_app;
-- Do NOT grant: CREATE, DROP, ALTER, SUPERUSER
```

```yaml
# docker-compose.yml — separate admin (for schema creation) from app user
services:
  web:
    environment:
      - POSTGRES_USER=dvrag_app
      - POSTGRES_PASSWORD=${APP_DB_PASSWORD}
  db:
    environment:
      - POSTGRES_USER=admin  # only used for initial setup
      - POSTGRES_PASSWORD=${ADMIN_DB_PASSWORD}
```

Update Alembic to use the admin credentials for migrations, and the app to use the restricted `dvrag_app` credentials for runtime.

**Success Criteria:**

- Application connects to database with a non-superuser account
- App account has only SELECT/INSERT/UPDATE/DELETE permissions
- Schema creation/migrations use a separate admin account

**Status:** Pending
