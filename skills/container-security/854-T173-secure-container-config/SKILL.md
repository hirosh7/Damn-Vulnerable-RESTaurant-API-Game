---
name: 854-t173-secure-container-config
description: The docker-compose.yml uses privileged:true and cap_add:SYS_ADMIN which grants root-equivalent container capabilities. Remove all unnecessary capabilities.
---

# 854-T173: Use a Secure Configuration for Containers

**Category:** CODE_FIX
**SD Elements:** [854-T173](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 10

**Current Vulnerable Configuration:**

```yaml
# docker-compose.yml:24-28 — CRITICAL: root-equivalent container
services:
  web:
    privileged: true      # EXTREMELY DANGEROUS — grants all capabilities
    cap_add:
      - SYS_ADMIN         # Allows: mount, chroot, namespace manipulation
```

These settings are intentionally vulnerable (it's DVRAG), but must be removed for hardening.

**Required Fix:**

```yaml
# docker-compose.yml — hardened configuration
services:
  web:
    image: ${COMPOSE_IMAGE_NAME:-dvrag-api}
    build:
      context: .
      dockerfile: Dockerfile
    # REMOVED: privileged: true
    # REMOVED: cap_add: [SYS_ADMIN]
    security_opt:
      - no-new-privileges:true        # prevent privilege escalation
    read_only: false                   # set true once app is verified
    cap_drop:
      - ALL                            # drop ALL capabilities
    cap_add:
      - NET_BIND_SERVICE               # only if binding ports < 1024 (not needed here)
    user: "1000:1000"                  # run as non-root user
    environment:
      - POSTGRES_USER
      - POSTGRES_PASSWORD
      - POSTGRES_SERVER
      - POSTGRES_PORT
      - POSTGRES_DB
      - JWT_SECRET_KEY
    ports:
      - "${API_PORT:-8091}:8091"
```

**Additional changes:**
- Remove `privileged: true` 
- Remove `cap_add: SYS_ADMIN`
- Add `cap_drop: ALL`
- Add `security_opt: no-new-privileges:true`

**Note:** The `get_disk_usage()` function in admin/utils.py that relied on these privileges must also be fixed (see T43).

**Success Criteria:**

- No `privileged: true` in docker-compose.yml
- No `SYS_ADMIN` capability
- `cap_drop: ALL` applied
- `no-new-privileges:true` security option set

**Status:** Pending
