---
name: 854-t175-container-resource-limits
description: The docker-compose.yml has no resource limits. Add CPU and memory limits to prevent DoS and resource exhaustion attacks.
---

# 854-T175: Apply Resource Limits to Containers

**Category:** CODE_FIX
**SD Elements:** [854-T175](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

```yaml
# docker-compose.yml — no resource limits defined
services:
  web:
    ...  # unlimited CPU and memory
  db:
    ...  # unlimited CPU and memory
```

Without limits, a compromised container or bug can consume all host resources (DoS).

**Required Fix:**

```yaml
# docker-compose.yml — add resource limits
services:
  web:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    # For docker-compose v3 without swarm, use:
    mem_limit: 512m
    cpus: 1.0
    mem_reservation: 128m

  db:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
    mem_limit: 512m
    cpus: 1.0
```

**Note:** `deploy.resources` is respected by Docker Compose in standalone mode with Docker Compose v2.x. For compatibility, also add `mem_limit` and `cpus` at the service level.

**Recommended Values (development):**

| Service | CPU Limit | Memory Limit |
|---------|-----------|-------------|
| web (FastAPI) | 1.0 | 512MB |
| db (PostgreSQL) | 1.0 | 512MB |

**Success Criteria:**

- Both web and db services have CPU and memory limits defined
- Container cannot OOM-kill the host
- `docker stats` shows cgroup limits applied

**Status:** Pending
