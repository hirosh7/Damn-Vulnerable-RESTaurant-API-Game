---
name: 854-t214-protect-confidential-files
description: Protect sensitive files (.env, database files, migration scripts) from unauthorized access. Review Dockerfile and docker-compose.yml for file permission issues.
---

# 854-T214: Protect Confidential Files on Operating System or Server

**Category:** CODE_FIX
**SD Elements:** [854-T214](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current Issues:**

```dockerfile
# Dockerfile — issues with file access
RUN echo 'ALL ALL=(ALL) NOPASSWD: /usr/bin/find' | sudo tee /etc/sudoers.d/find_nopasswd
# Any app user can run find as root — allows filesystem traversal
RUN chown app .
USER app
```

```yaml
# docker-compose.yml
privileged: true    # container has elevated OS privileges
cap_add:
  - SYS_ADMIN       # grants almost root-level access
```

**Required Fixes:**

```dockerfile
# Dockerfile — remove sudo find permission, tighten permissions
# REMOVE:
# RUN echo 'ALL ALL=(ALL) NOPASSWD: /usr/bin/find' | sudo tee /etc/sudoers.d/find_nopasswd

# Set proper file permissions
COPY --chown=app:app app ./app
RUN chmod -R 750 /app
```

```yaml
# docker-compose.yml — remove privileged mode and SYS_ADMIN
services:
  web:
    # REMOVE these lines:
    # privileged: true
    # cap_add:
    #   - SYS_ADMIN
    read_only: true  # optional: make filesystem read-only
    tmpfs:
      - /tmp  # allow writes only in /tmp
```

Also add a `.dockerignore` file to prevent sensitive files from being copied:

```text
# .dockerignore
.env
.env.*
*.key
*.pem
postgres_data/
```

**Success Criteria:**

- No `privileged: true` in docker-compose.yml
- No `SYS_ADMIN` capability
- No sudo NOPASSWD rules in Dockerfile
- `.dockerignore` excludes sensitive files

**Status:** Pending
