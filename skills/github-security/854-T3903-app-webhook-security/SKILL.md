---
name: 854-t3903-app-webhook-security
description: Secure any GitHub App integrations and webhooks with proper secrets validation and minimal permissions.
---

# 854-T3903: Implement Application and Webhook Security Strategies (GitHub)

**Category:** CODE_FIX
**SD Elements:** [854-T3903](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Current State:**

The repository uses GitHub Actions CI/CD via `.github/workflows/test.yml`. No webhooks or GitHub Apps are currently configured, but any future integrations must follow these guidelines.

**Required Actions:**

1. **Validate webhook signatures** for any webhooks receiving GitHub events:

```python
# If implementing a webhook receiver endpoint
import hashlib
import hmac

def verify_github_webhook_signature(payload_body: bytes, signature_header: str, secret: str) -> bool:
    """Verify GitHub webhook HMAC-SHA256 signature."""
    if not signature_header:
        return False
    if not signature_header.startswith("sha256="):
        return False
    expected_sig = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_sig, signature_header)
```

2. **GitHub Apps: minimal permissions** — if adding a GitHub App:
   - Request only necessary repository permissions (read-only where possible)
   - Never request admin:org permissions

3. **Secrets in Actions** — all GitHub Actions secrets must be:
   - Stored as GitHub Secrets (not in YAML files)
   - Scoped to minimum required repositories/environments

4. **Audit GitHub App installations:**

```bash
# Review installed apps via API
gh api /repos/{owner}/{repo}/installations
```

**Success Criteria:**

- No webhook endpoints without signature validation
- GitHub Apps limited to minimum permissions
- All external service tokens stored in GitHub Secrets

**Status:** Pending
