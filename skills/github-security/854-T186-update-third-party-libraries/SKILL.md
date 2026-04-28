---
name: 854-t186-update-third-party-libraries
description: Update all third-party Python dependencies to their latest patched versions. Enable Dependabot or pip-audit in CI to automate ongoing monitoring.
---

# 854-T186: Use Recommended Settings and Latest Patches for Third-Party Libraries

**Category:** CODE_FIX
**SD Elements:** [854-T186](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 10

**Current State:**

```toml
# pyproject.toml — pinned versions may be outdated
[tool.poetry.dependencies]
fastapi = "^0.101.1"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
slowapi = "^0.1.8"
SQLAlchemy = "^2.0.20"
```

**Required Actions:**

1. **Run pip-audit to identify vulnerable packages:**

```bash
pip install pip-audit
pip-audit -r requirements.txt --strict
```

2. **Enable GitHub Dependabot** — create `.github/dependabot.yml`:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "security"
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

3. **Add pip-audit to CI pipeline** (`/.github/workflows/test.yml`):

```yaml
# .github/workflows/test.yml — add security audit step
  security-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install pip-audit
      - run: pip-audit -r requirements.txt
```

4. **Known vulnerabilities to address:**
   - `python-jose` 3.x: JOSE library vulnerabilities — consider migrating to `python-jwt` or `authlib`

**Success Criteria:**

- `pip-audit` passes with 0 critical/high vulnerabilities
- Dependabot enabled for Python dependencies
- CI fails on new critical/high vulnerabilities

**Status:** Pending
