---
name: 854-t3905-pipeline-efficiency-security
description: Harden the GitHub Actions pipeline by pinning action versions, using least-privilege permissions, and adding security scanning steps.
---

# 854-T3905: Ensure Pipeline Efficiency and Security (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3905](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current Workflow Issues:**

```yaml
# .github/workflows/test.yml — current issues
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3   # ← Should be pinned to commit SHA
      - uses: pre-commit/action@v3.0.1  # ← Pin to SHA
```

**Required Fix:**

```yaml
# .github/workflows/test.yml — hardened version
name: Build and Test

on:
  push:
    branches: [main, "security-hardening/**"]
  pull_request:
    branches: [main]

permissions:
  contents: read              # least-privilege: only read code
  security-events: write      # needed only for code scanning

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1 pinned SHA
        with:
          fetch-depth: 0
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - uses: pre-commit/action@2c7b3805fd2a0fd8c1884dcaebf91fc102a13ecd  # v3.0.1 pinned SHA

  build-and-test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    needs: pre-commit
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
      - name: Run security audit
        run: |
          pip install pip-audit
          pip-audit -r requirements.txt
      - name: Build and test
        run: docker compose up --build -d && docker compose run --rm web pytest
      - name: Tear down
        if: always()
        run: docker compose down
```

**Key changes:**
- Add `permissions:` block (least privilege — no write unless needed)
- Pin actions to commit SHAs (not floating version tags)
- Add `pip-audit` security scan step
- Fail build on critical vulnerabilities

**Success Criteria:**

- All `uses:` statements pinned to full commit SHA
- Workflow has explicit `permissions:` blocks with minimal grants
- Pipeline fails on detected vulnerabilities

**Status:** Pending
