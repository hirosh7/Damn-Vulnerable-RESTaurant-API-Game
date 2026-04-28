---
name: 854-t3909-third-party-artifact-security
description: Ensure third-party Docker base images and Python packages are verified before use. Pin to specific digest hashes and enable vulnerability scanning.
---

# 854-T3909: Ensure Third-Party Artifact Security (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3909](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current Issues:**

```dockerfile
# Dockerfile:1 — floating tag, no digest pin
FROM python:3.10-slim
```

```yaml
# docker-compose.yml:19 — floating tag
image: postgres:15.4-alpine
```

**Required Fix:**

1. **Pin Docker base images to digest:**

```dockerfile
# Dockerfile — pin to specific digest
FROM python:3.10-slim@sha256:<digest>
# Obtain digest: docker pull python:3.10-slim && docker inspect python:3.10-slim | grep RepoDigests
```

2. **Pin PostgreSQL image to digest** in `docker-compose.yml`:

```yaml
db:
  image: postgres:15.4-alpine@sha256:<digest>
```

3. **Run Trivy/Grype vulnerability scan** in CI:

```yaml
# .github/workflows/test.yml — add image scanning
  - name: Scan image with Trivy
    uses: aquasecurity/trivy-action@master
    with:
      image-ref: 'dvrag-api:latest'
      format: 'sarif'
      output: 'trivy-results.sarif'
      severity: 'CRITICAL,HIGH'
      exit-code: '1'        # fail build on HIGH/CRITICAL

  - name: Upload Trivy results
    uses: github/codeql-action/upload-sarif@v3
    if: always()
    with:
      sarif_file: 'trivy-results.sarif'
```

4. **Lock Python dependencies** with hash verification:

```bash
# Generate requirements.txt with hashes
pip-compile --generate-hashes pyproject.toml -o requirements.txt
```

```bash
# Install only verified hashes
pip install --require-hashes -r requirements.txt
```

**Success Criteria:**

- Base Docker images pinned to digest (not floating tags)
- Container vulnerability scan in CI (Trivy/Grype)
- Python packages installed with hash verification

**Status:** Pending
