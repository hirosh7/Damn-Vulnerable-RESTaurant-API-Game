---
name: 854-t43-avoid-unsafe-os-interaction
description: Fix OS command injection in get_disk_usage() in app/apis/admin/utils.py. This is the Level 5 vulnerability allowing RCE via the /admin/stats/disk endpoint.
---

# 854-T43: Avoid Unsafe Operating System Interaction

**Category:** CODE_FIX
**SD Elements:** [854-T43](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 10

**Vulnerability (Level 5 — Remote Code Execution):**

```python
# app/tests/vulns/level_5_remote_code_execution.py
# /admin/stats/disk?parameters=%26%26echo%20vulnerable!
# Passes because parameters are appended to shell command

# Original vulnerable code (before fixes):
# subprocess.run(f"df -h {parameters}", shell=True)
```

**Current (partially fixed) code:**

```python
# app/apis/admin/utils.py:17-34
ALLOWED_PATHS = {"/", "/tmp", "/var", "/home", "/app", "/data"}

def get_disk_usage(parameters: str):
    path = parameters.strip() if parameters else "/"
    if path not in ALLOWED_PATHS:
        raise ValueError(...)
    result = subprocess.run(
        ["df", "-h", path],  # GOOD — no shell=True, list args
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,  # GOOD
    )
```

The current code appears to be already partially fixed (uses allowlist + list args + shell=False). 

**Verification Tasks:**

1. Confirm the Level 5 test in `app/tests/vulns/level_5_remote_code_execution.py` now FAILS (meaning the exploit is fixed).
2. Verify `shell=False` is present in the subprocess call.
3. Verify the path validation is in place.
4. Audit `app/game.py:30` subprocess.Popen — ensure test runner cannot be exploited.

**Additional Hardening:**

```python
# app/apis/admin/utils.py — add timeout to prevent DoS
result = subprocess.run(
    ["df", "-h", path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=False,
    timeout=5,  # prevent hanging subprocess
)
```

**Dockerfile:** Remove the `sudo find` permission:

```dockerfile
# Dockerfile — REMOVE this line:
# RUN echo 'ALL ALL=(ALL) NOPASSWD: /usr/bin/find' | sudo tee /etc/sudoers.d/find_nopasswd
```

**Success Criteria:**

- Level 5 RCE test no longer passes
- `shell=False` confirmed in all subprocess calls
- `sudo find` permission removed from Dockerfile
- Subprocess calls have timeouts

**Status:** Pending
