---
name: 854-t2602-log-db-activities
description: Add structured logging for database operations and API access events. The application currently has no centralized logging — add Python logging for auth events, data access, and errors.
---

# 854-T2602: Log Typical Database and Server Activities and Related Metadata

**Category:** CODE_FIX
**SD Elements:** [854-T2602](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 8

**Issue:**

The application has no structured logging. Security-relevant events (login failures, authorization denials, data access) are not recorded.

**Required Fix:**

Add a centralized logging module:

```python
# app/logging_config.py — new file
import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "user"):
            log_obj["user"] = record.user
        if hasattr(record, "action"):
            log_obj["action"] = record.action
        return json.dumps(log_obj)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

```python
# app/apis/auth/services/get_token_service.py — log auth events
from logging_config import get_logger
logger = get_logger("auth")

@router.post("/token")
async def get_token(request: Request, form_data, db):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning("Login failed", extra={"user": form_data.username, "action": "login_fail", "ip": request.client.host})
        raise HTTPException(...)
    logger.info("Login success", extra={"user": user.username, "action": "login_success"})
    ...
```

**Key Events to Log:**
- Authentication success/failure
- Authorization denials (403)
- Admin operations (password reset, role changes)
- Data access for sensitive endpoints

**Success Criteria:**

- Structured JSON logs for auth events
- Login failures logged with username and IP
- Authorization denials logged
- Logs written to stdout for container log aggregation

**Status:** Pending
