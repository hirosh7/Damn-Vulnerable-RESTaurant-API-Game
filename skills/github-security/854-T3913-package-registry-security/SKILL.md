---
name: 854-t3913-package-registry-security
description: Secure the container image registry (GHCR or Docker Hub). Implement registry authentication, image scanning, and access control.
---

# 854-T3913: Implement Package Registry Security (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3913](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Required Actions:**

1. **Use GitHub Container Registry (GHCR)** instead of anonymous Docker Hub pulls:

```dockerfile
# Dockerfile — use explicit registry reference
FROM ghcr.io/library/python:3.10-slim@sha256:<digest>
# or use Docker Official Images with explicit registry
FROM docker.io/library/python:3.10-slim@sha256:<digest>
```

2. **Authenticate to registry in CI** using GitHub's OIDC token:

```yaml
# .github/workflows/build.yml
- name: Log in to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}  # Short-lived OIDC token
```

3. **Configure GHCR visibility** appropriately:
   - For public repos: packages can be public, but push access must require auth
   - For private repos: set package visibility to `private`

4. **Vulnerability scanning on push to registry:**

```yaml
# .github/workflows/publish.yml — scan before marking as "latest"
- name: Scan before tagging latest
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'ghcr.io/${{ github.repository }}:${{ github.sha }}'
    exit-code: '1'
    severity: 'CRITICAL'

- name: Tag as latest only if scan passes
  run: |
    docker tag ghcr.io/${{ github.repository }}:${{ github.sha }} \
      ghcr.io/${{ github.repository }}:latest
    docker push ghcr.io/${{ github.repository }}:latest
```

5. **Immutable tags** — never reuse non-`latest` version tags.

**Success Criteria:**

- Images pushed to GHCR with authenticated pipeline
- Vulnerability scan gate before `latest` tag promotion
- Registry credentials use short-lived OIDC tokens (not long-lived PATs)

**Status:** Pending
