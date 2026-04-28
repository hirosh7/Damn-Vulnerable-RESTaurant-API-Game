---
name: 854-t2256-authenticate-registry-access
description: Ensure all access to container and package registries is authenticated and logged. Anonymous registry pulls must be prohibited for production deployments.
---

# 854-T2256: Authenticate and Log All Access to Registries

**Category:** INFRA
**SD Elements:** [854-T2256](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

The `Dockerfile` and `docker-compose.yml` pull from Docker Hub using anonymous access. Docker Hub imposes rate limits on anonymous pulls and provides no audit trail.

**Required Infrastructure Changes:**

1. **Authenticate all registry pulls** in production via GitHub OIDC:

```yaml
# .github/workflows/build.yml
- name: Log in to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}

- name: Log in to Docker Hub (for pulling base images)
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

2. **Mirror base images to GHCR** to avoid anonymous Docker Hub dependency:

```bash
# Mirror python:3.10-slim to your own GHCR namespace
docker pull python:3.10-slim
docker tag python:3.10-slim ghcr.io/{owner}/base-images/python:3.10-slim
docker push ghcr.io/{owner}/base-images/python:3.10-slim

# Update Dockerfile
FROM ghcr.io/{owner}/base-images/python:3.10-slim@sha256:<digest>
```

3. **Log all registry access** — GHCR provides audit logs via the GitHub Organization Audit Log:
   - Navigate to Organization → Settings → Audit Log → Filter by "packages"
   - Retain audit logs for 90+ days

4. **For production deployments** — use a Kubernetes secret or Docker credential store:

```bash
# Kubernetes imagePullSecret
kubectl create secret docker-registry ghcr-creds \
  --docker-server=ghcr.io \
  --docker-username=$GITHUB_ACTOR \
  --docker-password=$GITHUB_TOKEN
```

5. **Revoke and rotate registry credentials** on team member departure.

**Success Criteria:**

- No anonymous registry pulls in production
- Registry access authenticated via short-lived OIDC tokens (not static PATs)
- Audit log enabled for registry push/pull events
- Base images mirrored to organization-controlled registry

**Status:** Pending — requires infrastructure deployment
