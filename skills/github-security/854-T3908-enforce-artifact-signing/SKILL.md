---
name: 854-t3908-enforce-artifact-signing
description: Sign Docker container images and Python build artifacts to enable provenance verification. Use Sigstore/Cosign for container signing.
---

# 854-T3908: Enforce Artifact Signing (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3908](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Required Actions:**

1. **Sign Docker images with Cosign** in the CI pipeline:

```yaml
# .github/workflows/build-and-sign.yml
name: Build and Sign Image

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write        # needed for keyless Sigstore signing
  packages: write        # needed to push to GHCR

jobs:
  build-sign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      - name: Build image
        run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Push image
        run: docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Sign image (keyless via Sigstore)
        run: |
          cosign sign --yes ghcr.io/${{ github.repository }}@$(
            docker inspect --format='{{index .RepoDigests 0}}' \
              ghcr.io/${{ github.repository }}:${{ github.sha }}
          )
```

2. **Generate SBOM** alongside signed image:

```yaml
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json
```

3. **Verify signatures before deployment:**

```bash
cosign verify ghcr.io/{owner}/{repo}:{tag} \
  --certificate-identity-regexp="https://github.com/{owner}/{repo}/.github/workflows/.*" \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com
```

**Success Criteria:**

- Docker images signed with Cosign (keyless, via OIDC)
- SBOM generated and attached to image
- Deployment pipeline verifies signature before deploying

**Status:** Pending
