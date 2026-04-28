---
name: 854-t349-protect-audit-logs
description: Implement structured audit logging and protect logs from unauthorized access. The app currently has no audit trail for security-sensitive operations.
---

# 854-T349: Protect Audit Information and Logs Against Unauthorized Access

**Category:** CODE_FIX
**SD Elements:** [854-T349](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/)
**Priority:** 7

**Issue:**

No audit trail exists for security-sensitive operations. There is no logging for:
- Authentication events
- Authorization failures
- Admin operations
- Data access/modifications

**Required Fix:**

Add a structured audit log model and middleware:

```python
# app/db/models.py — add AuditLog model
class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String, nullable=False, index=True)  # e.g., "login", "delete_order"
    resource = Column(String, nullable=True)             # e.g., "order:42"
    ip_address = Column(String, nullable=True)
    success = Column(Boolean, nullable=False, default=True)
    details = Column(String, nullable=True)
```

```python
# app/init_app.py — add audit middleware for all requests
@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code in (401, 403):
        # Log all auth/authz failures to stdout (to container log aggregator)
        import logging
        logging.getLogger("audit").warning(
            f"Auth failure: {request.method} {request.url.path} "
            f"from {request.client.host} -> {response.status_code}"
        )
    return response
```

**Success Criteria:**

- Auth/authz failures logged with user, IP, endpoint, and status
- Logs go to stdout (container-friendly, aggregated by infrastructure)
- Log entries are not deletable by application users (write-once)

**Status:** Pending
