---
name: 854-t3914-artifact-origin-policy
description: Implement build provenance attestation and a policy for verifying where built artifacts originated. Use GitHub's artifact attestation feature.
---

# 854-T3914: Implement Artifact Origin Information Policy (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3914](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Required Actions:**

1. **Generate provenance attestation** using GitHub's native attestation action:

```yaml
# .github/workflows/build.yml
name: Build and Attest

on:
  push:
    branches: [main]

permissions:
  id-token: write        # for OIDC token
  attestations: write    # for attestation creation
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        id: build
        run: |
          docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
          echo "digest=$(docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/${{ github.repository }}:${{ github.sha }} | cut -d@ -f2)" >> "$GITHUB_OUTPUT"

      - name: Generate artifact attestation
        uses: actions/attest-build-provenance@v1
        with:
          subject-name: ghcr.io/${{ github.repository }}
          subject-digest: ${{ steps.build.outputs.digest }}
          push-to-registry: true
```

2. **Verify artifact origin** before deployment:

```bash
# Verify image attestation
gh attestation verify ghcr.io/{owner}/{repo}:{tag} \
  --owner {owner} \
  --format json
```

3. **SLSA provenance level** — the above approach achieves SLSA Build L2:
   - Build instructions from source (not user-provided)
   - Provenance is signed and non-forgeable
   - Build environment is ephemeral (GitHub-hosted runner)

4. **Document the artifact origin policy** in the repository:

```markdown
# SUPPLY_CHAIN.md
## Artifact Origin Policy

All production Docker images are built exclusively from:
- GitHub Actions workflows on the `main` branch
- Authenticated via GitHub OIDC (not static secrets)
- Attested using GitHub Build Provenance

To verify an image:
  gh attestation verify ghcr.io/{owner}/dvrag:{sha} --owner {owner}
```

**Success Criteria:**

- Build provenance attestation generated for each release image
- Attestation published to GHCR alongside the image
- Deployment runbook includes verification step

**Status:** Pending
