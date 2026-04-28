---
name: 854-t3901-repository-management-security
description: Enforce repository security settings including private visibility controls, secret scanning, and access management to reduce the repository attack surface.
---

# 854-T3901: Enforce Repository Management and Security Strategies (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3901](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Required Actions:**

1. **Enable GitHub Advanced Security features** via repository settings:
   - Secret scanning: **enabled** — detects committed secrets
   - Push protection: **enabled** — blocks commits with secrets
   - Code scanning (CodeQL): **enabled** — SAST analysis

2. **Create `.github/workflows/codeql.yml`** for automated code scanning:

```yaml
# .github/workflows/codeql.yml
name: CodeQL Security Analysis

on:
  push:
    branches: [main, security-hardening/**]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6AM UTC

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-extended

      - uses: github/codeql-action/autobuild@v3

      - uses: github/codeql-action/analyze@v3
        with:
          category: "/language:python"
```

3. **Repository access hygiene:**
   - Minimum outside collaborators
   - No public write access
   - Regular access reviews
   - Require 2FA for all contributors

4. **Add `.gitignore` entries** to prevent accidental secret commits:

```
# .gitignore additions
.env
.env.local
*.pem
*.key
secrets/
```

**Success Criteria:**

- Secret scanning enabled with push protection
- CodeQL workflow running on PRs to `main`
- `.gitignore` covers all credential file patterns

**Status:** Pending
