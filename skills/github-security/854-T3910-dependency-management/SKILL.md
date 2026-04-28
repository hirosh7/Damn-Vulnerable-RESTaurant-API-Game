---
name: 854-t3910-dependency-management
description: Implement a dependency management strategy with lockfiles, Dependabot, and automated vulnerability scanning for Python packages.
---

# 854-T3910: Implement Dependency Management Strategy (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3910](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

The project uses `pyproject.toml` with Poetry. A `poetry.lock` file should be checked into version control to ensure reproducible builds.

**Required Actions:**

1. **Commit `poetry.lock`** to version control (if not already):

```bash
git add poetry.lock
git commit -m "chore: lock Python dependencies for reproducible builds"
```

2. **Enable Dependabot** for automated dependency updates (see T186):

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    allow:
      - dependency-type: "all"
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]  # manual major version reviews
```

3. **Automated vulnerability scanning** on every PR:

```yaml
# .github/workflows/security.yml
name: Dependency Security

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install pip-audit
      - run: pip-audit --requirement requirements.txt --strict
```

4. **Separate dev from production dependencies:**

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.101.1"
# ... production deps only

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.2"
pre-commit = "^3.4.0"
# ... dev-only deps
```

**Success Criteria:**

- `poetry.lock` is committed and kept current
- Dependabot opens PRs for outdated dependencies weekly
- `pip-audit` runs in CI and blocks on HIGH/CRITICAL
- Dev dependencies separated from production

**Status:** Pending
