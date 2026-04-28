---
name: 854-t169-minimal-container-image
description: The Docker image contains unnecessary packages. Use a minimal base image and remove unrequired tools to reduce attack surface.
---

# 854-T169: Keep the Container Image Minimal and Remove Unnecessary Components

**Category:** CODE_FIX
**SD Elements:** [854-T169](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 9

**Current Dockerfile Issues:**

```dockerfile
# Dockerfile:6-16 — installs gcc, python-dev, sudo
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    sudo \          # ← NEVER include sudo in production container
    && rm -rf /var/lib/apt/lists/*

# Dockerfile:36 — EXTREMELY dangerous sudo rule
RUN echo "app ALL=(ALL) NOPASSWD: /usr/bin/find" >> /etc/sudoers
```

**Required Fix:**

```dockerfile
# Dockerfile — multi-stage build to eliminate build tools from final image
FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


FROM python:3.10-slim AS runtime

# Only libpq needed at runtime (no build tools, no gcc, no sudo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

RUN useradd -m -u 1000 -s /sbin/nologin app
WORKDIR /app
COPY --chown=app:app . .
USER app

EXPOSE 8091
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8091"]
```

**Key changes:**
- Remove `sudo` from container
- Remove `gcc`, `python3-dev` from final image (build-time only)
- Remove the `NOPASSWD: /usr/bin/find` sudoers entry
- Multi-stage build to reduce final image size

**Success Criteria:**

- `sudo` not installed in final container
- No `NOPASSWD` sudoers rules
- Final image size reduced (no gcc/python3-dev)
- App runs as non-root user `app`

**Status:** Pending
