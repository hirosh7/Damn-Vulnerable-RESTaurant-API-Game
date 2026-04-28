---
name: 854-t3907-pipeline-definition-security
description: Harden the pipeline YAML definition against injection attacks, especially when using untrusted inputs in run steps. Use environment variables for user-supplied values.
---

# 854-T3907: Ensure Pipeline Definition and Security (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3907](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current Workflow:**

```yaml
# .github/workflows/test.yml — check for injection vectors
on:
  pull_request:
    branches: [main]
```

**Risk: Script Injection** — when pipeline steps use `${{ github.event.pull_request.title }}` or other user-controlled inputs in `run:` blocks, attackers can inject shell commands through PR titles/branch names.

**Required Actions:**

1. **Never interpolate `github.event.*` directly into `run:` scripts:**

```yaml
# UNSAFE — injection risk
- run: echo "PR title: ${{ github.event.pull_request.title }}"

# SAFE — use environment variable intermediary
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "PR title: $PR_TITLE"
```

2. **Scope workflow triggers carefully:**

```yaml
# Only trigger on push and PRs to protected branches
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
  # Do NOT add: workflow_dispatch with untrusted inputs
```

3. **Validate `workflow_dispatch` inputs** if used:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        type: choice    # Constrained input, not free-form
        options: [staging, production]
```

4. **No `pull_request_target`** triggers with write permissions (classic attack vector).

**Success Criteria:**

- No untrusted input interpolated directly into `run:` steps
- Workflow triggers do not use `pull_request_target`
- Any `workflow_dispatch` inputs are constrained (type: choice, not free-form)

**Status:** Pending
