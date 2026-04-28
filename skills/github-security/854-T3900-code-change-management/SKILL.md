---
name: 854-t3900-code-change-management
description: Implement branch protection rules, required code reviews, and signed commits to enforce secure code change management in GitHub.
---

# 854-T3900: Implement and Use Code Change Management Strategy (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3900](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Required Actions:**

1. **Enable branch protection rules** for `main` via GitHub repository settings or via API:

```bash
# Configure via GitHub CLI
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["build-and-test"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null
```

2. **Require signed commits** (CODEOWNERS + branch protection):

```bash
# Enable via GitHub UI: Settings → Branches → Edit rule → Require signed commits
```

3. **Add CODEOWNERS** file for sensitive paths:

```
# .github/CODEOWNERS
# Security-sensitive paths require security team review
app/apis/auth/         @security-team
app/apis/admin/        @security-team
docker-compose.yml     @devops-team
Dockerfile             @devops-team
```

4. **Pre-commit hooks** (already present via `.pre-commit-config.yaml`):

```yaml
# .pre-commit-config.yaml — add security hooks
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "app/", "-ll"]
```

**Success Criteria:**

- `main` branch requires PR review before merge
- Direct pushes to `main` blocked
- Pre-commit hooks include security scanning (bandit)
- CODEOWNERS file defines security-sensitive paths

**Status:** Pending
