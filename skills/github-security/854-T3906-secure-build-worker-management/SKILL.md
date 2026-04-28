---
name: 854-t3906-secure-build-worker-management
description: Ensure GitHub Actions runners are secure. Avoid self-hosted runners for public repos and isolate build environments to prevent runner compromise.
---

# 854-T3906: Implement Secure Build Worker Management (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3906](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

```yaml
# .github/workflows/test.yml
runs-on: ubuntu-latest   # GitHub-hosted runner — GOOD for public repos
```

The project uses GitHub-hosted runners which are ephemeral and isolated. This is the correct approach for a public/open-source repository.

**Required Actions:**

1. **Never use self-hosted runners** for public repositories (arbitrary code execution risk).

2. **Isolate build steps** using separate jobs:

```yaml
# Separate security scan from build to isolate permissions
jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    steps: [...]

  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read  # read-only — cannot write to repo
    steps: [...]
```

3. **Restrict `GITHUB_TOKEN` permissions** at workflow level:

```yaml
# .github/workflows/test.yml — top level
permissions:
  contents: read       # default read-only for GITHUB_TOKEN
```

4. **Use ephemeral environments** — GitHub-hosted runners destroy the VM after each job.

5. **No secrets in workflow logs** — ensure no `echo $SECRET` in run steps.

**Success Criteria:**

- Workflow uses only GitHub-hosted (`ubuntu-latest`) runners
- `permissions:` is explicitly set to `read-only` at workflow level
- No self-hosted runners configured

**Status:** Pending
