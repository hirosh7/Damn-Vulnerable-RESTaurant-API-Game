# DVRAG — Security Requirements Project Summary

**Date:** March 15, 2026
**Application:** Damn Vulnerable RESTaurant API Game (DVRAG)
**SDE Project:** Damn Vulnerable Restaurant API Game - From Devici Diagram (Mar 2026)
**SDE Project ID:** 828
**Project URL:** https://sde-ent-onyxdrift.sdelab.net/bunits/corporate-security-bu/secapp-assessment-application/damn-vulnerable-restaurant-api-game-from-devici-diagram-mar-2026/
**Code branch:** `feature/sde-countermeasures-828-mar2026`

---

## Overview

A STRIDE threat model was generated from the DVRAG architecture, imported into SD Elements to produce a set of security requirements, and all requirements were evaluated and implemented (where applicable) in the codebase. This document captures the full scope of what was assessed and what was built.

---

## Architecture Input

The threat model captures the DVRAG deployment topology:

| Artifact | Count |
|---|---|
| Architecture components | 14 |
| Trust boundary zones | 3 (Internet · Application/Docker · Database) |
| Data flows | 10 |
| STRIDE threats | 11 |
| Mitigations | 9 |

**Stack:** FastAPI hub-and-spoke REST API · PostgreSQL · JWT Bearer (HS256) · Docker Compose · Python 3.10

---

## Act 3 — SDE Project + Exhaustive Survey

### Project Setup

An SD Elements project was created with the architecture description extracted directly from the OTM threat model. Profile P1 (Blank) was selected to maximise the question surface; Risk Policy 1 was applied.

### Survey Completion

The survey was completed in **dependency order** — base answers unlock downstream questions. A final reconciliation pass compared `getDraft` (section-visible questions) against `getProjectSurvey` (authoritative flat list) to surface hidden and profile-pre-populated answers that do not appear in the visible question tree.

| Survey Metric | Value |
|---|---|
| Total answers selected (`getProjectSurvey`) | **65** |
| Visible questions answered (`getDraft`) | 29 |
| Hidden / auto-selected answers | 18 |
| Survey status | **Published** |

Key dependency chain applied:
```
Web application
  → Uses a database
    → Stand-alone database that supports SQL
      → PostgreSQL
Authorizes Subjects → authorization / session management questions
Handles Personal Data → GAPP / GDPR privacy questions
Docker → container platform questions
```

### Evidence Comments

Every answered question received an evidence-backed comment citing the specific threat, code file, or architectural component that justified the answer.

| Question Topic | Evidence |
|---|---|
| Components In Development | Hub-and-spoke FastAPI; Auth, Order, Menu, Admin, Debug services |
| Components In Use | PostgreSQL, SQLAlchemy ORM, Pydantic, passlib/bcrypt, python-jose |
| Architectural Features | Docker bridge network; internet-facing trust boundary; CORS middleware |
| Architecture | Microservices topology with single API gateway routing to 5 service components |
| Application Context | Security training application; intentional OWASP API Top 10 vulnerabilities |
| Target Platform | Python 3.10 Docker containers on Linux |
| Programming Language | Python 3 backend; no JavaScript frontend |
| Web Client Technologies | CORSMiddleware in init_app.py for cross-origin REST API clients |
| Database | PostgreSQL standalone container; SQLAlchemy ORM |
| Database Management System | PostgreSQL; credentials from environment variables |
| Data Formats | JSON REST API payloads via pydantic serialization |
| Interfaces & APIs | FastAPI OpenAPI gateway routing to 5 service components |
| Authentication Features | JWT Bearer HS256; algorithm confusion + brute force vulnerabilities |
| Server-to-Server Auth | Docker internal network; JWT claim-based service identity |
| Password Management | Change/reset password endpoints; 8-digit PIN code; rate-limited |
| Authorization | CUSTOMER / CHEF / EMPLOYEE roles; IDOR and role-bypass vulnerabilities |
| Session Management | JWT 30-min expiry; no server-side revocation mechanism |
| External Code/Data | FastAPI dependency injection; third-party libraries |
| Input Validation | Pydantic models on all endpoints; SQL injection in order status update |
| Encryption | bcrypt password hashing; env-var JWT secret; HSTS response header |
| Miscellaneous | Async workers; Chef-auth debug endpoint; audit logging gap |
| Application Layer Protocols | HTTP REST; JSON; Docker port mapping |
| Authentication Method | Username/password form → JWT token issuance |
| HTTP-Based Protocols | RESTful web services; JSON responses only |
| Handles Personal Data | Username, phone number, password hash, order history in PostgreSQL |
| OWASP Development Tools | passlib/bcrypt, python-jose, slowapi |
| Privacy Regulations | GAPP; PII exposed via debug endpoint (intentional vulnerability) |
| Version Control | GitHub repository |
| Security Code Analysis | DAST (Burp Suite) + SAST on Python codebase |
| Open Source Libraries | python-jose, passlib/bcrypt, slowapi, SQLAlchemy |
| Test Tools | Burp Suite for OWASP API Top 10; pytest suite in `app/tests/vulns/` |
| Containerization | Docker Compose; 3 containers (api, db, delivery); bridge network |
| Changes Since Last Release | Full initial scope captured |
| Changes to User I/O | All API input/output endpoints captured as new |

### Requirements Generated

| Metric | Value |
|---|---|
| Risk-relevant countermeasures | **59** |
| Requirements phase (X1) | 33 |
| Development phase (X3) | 26 |

---

## Act 4 — Countermeasure Implementation

### Status Summary

| Status | Count | Requirements (X1) | Development (X3) |
|---|---|---|---|
| ✅ Complete | **22** | 8 | 14 |
| ➖ Not Applicable | **21** | 14 | 7 |
| ⚠️ Incomplete | **16** | 11 | 5 |
| **Total** | **59** | **33** | **26** |

### Code Fixes Applied

| File | Vulnerability | Countermeasures |
|---|---|---|
| `app/apis/orders/services/get_order_service.py` | **IDOR / BOLA** — customers could retrieve any order by ID | T338, T378, T184, T2598 |
| `app/apis/auth/services/update_profile_service.py` | **IDOR** — any authenticated user could update another user's profile | T378, T184 |
| `app/apis/users/services/update_user_role_service.py` | **Privilege escalation** — any authenticated user could promote other accounts | T184, T338 |
| `app/apis/orders/services/get_order_status.py` | **SQL injection** — raw f-string SQL in order status update | T38 |
| `app/apis/auth/services/reset_password_service.py` | **Account enumeration** — distinct error message for unknown usernames | T2139 |
| `app/apis/menu/utils.py` | **SSRF** — image fetch made requests to any attacker-supplied URL | T1365 |
| `app/audit_log.py` *(new)* | **Missing audit logging** — structured JSON audit records to stdout | T2602 |
| `app/apis/auth/services/get_token_service.py` | Audit wired in — login success/failure logged with actor and IP | T2602 |
| `app/config.py` | **Weak default secret** — `POSTGRES_PASSWORD` now warns at startup when not set | T76 |

### Fix Details

**IDOR — get_order_service.py**
```python
if current_user.role == UserRole.CUSTOMER and db_order.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Access denied")
```

**SQL injection — get_order_status.py**
```python
# Replaced: db.execute(f"UPDATE orders SET status = '{status_value}' WHERE id = {order_id}")
validated_status = OrderStatus(raw_status)   # raises ValueError if enum value unknown
db_order.status = validated_status
db.add(db_order)
db.commit()
```

**Privilege escalation — update_user_role_service.py**
```python
if current_user.role != models.UserRole.CHEF:
    raise HTTPException(status_code=403, detail="Only Chef is authorized to update user roles.")
```

**Account enumeration — reset_password_service.py**
```python
if not user or user.role != UserRole.CUSTOMER:
    return {"detail": "If the account exists, a PIN code will be sent to the registered phone number."}
```

**SSRF — menu/utils.py**
```python
_ALLOWED_IMAGE_HOSTS = {"restaurant.com", "cdn.restaurant.com", "images.restaurant.com", ...}

def _validate_image_url(image_url: str) -> None:
    parsed = urlparse(image_url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Image URL must use http or https.")
    if (parsed.hostname or "") not in _ALLOWED_IMAGE_HOSTS:
        raise HTTPException(status_code=400, detail="Image host is not trusted.")
```

### Notable Incomplete Countermeasures

| Countermeasure | What exists | Remaining gap |
|---|---|---|
| T70 — Account lockout | Rate limiting at 10/min on `/token` | No per-account failed-login counter or lockout |
| T20 — Session ID rotation | JWT tokens are unique per issuance | No server-side revocation; logout is client-side only |
| T60 — Algorithm enforcement | `algorithms=["HS256"]` prevents `none` attack | HS256 is symmetric; RS256/ES256 asymmetric not implemented |
| T21 — TLS enforcement | HSTS header set (max-age=63072000; includeSubDomains) | Full TLS termination requires reverse proxy (infra layer) |
| T536 — Message size limits | — | No explicit request body size limit in FastAPI/uvicorn |
| T1362 — API throttling | `/token`, `/register`, `/reset-password` throttled | Data endpoints (`/orders`, `/menu`) not rate-limited |
| T19 — DB least privilege | — | Single DB user for all operations; no read-only role |
| T2 — Password reset security | Rate-limited; 8-digit cryptographic PIN; 10-min expiry | No brute-force lockout on wrong PIN attempts |
| T349 — Protect audit logs | Logs to stdout → Docker log driver (append-only) | RBAC on log aggregator is an infrastructure concern |

### Not Applicable Rationale

| Countermeasure | Reason |
|---|---|
| T29 — Anti-CSRF | JWT Bearer auth in `Authorization` header; no cookies transmitted |
| T37 — DOM XSS | Pure REST API; no HTML rendering or JavaScript frontend |
| T1144 — SSTI | FastAPI returns JSON via pydantic; no server-side template engine |
| T166 — JSON hijacking | Bearer token auth; no JSONP or script-tag loading surface |
| T1539 — Clear browser data on logout | No browser storage (localStorage, sessionStorage, cookies) |
| T1468 — Encrypt browser storage | No browser storage used by the application |
| T178, T604, T754, T755, T2170 — GDPR controls | Process/legal obligations; training application with no real users |
| T2348 — Code reviews | Process activity; not a code artefact |
| T2256 — Registry authentication | Application does not access container or credential registries at runtime |
| T2599 — Connection string pollution | DB URL constructed entirely from environment variables; no user input |
| T50 — Indirect file object references | No file-based object access in the application |

---

## Threat-to-Countermeasure Traceability

| STRIDE Threat | Countermeasure(s) | Status |
|---|---|---|
| Spoofing — JWT Algorithm Confusion | T60 — Algorithm enforcement | ⚠️ Incomplete (HS256; RS256 not implemented) |
| Spoofing — Brute Force / Weak Password | T70 — Account lockout | ⚠️ Incomplete (rate limiting only) |
| Spoofing — Account Enumeration | T2139 — No info exposure via APIs | ✅ Complete |
| Tampering — SQL Injection (order status) | T38 — Bind SQL variables | ✅ Complete |
| Tampering — IDOR / Mass Assignment | T184, T338, T378, T2598 | ✅ Complete |
| Repudiation — No Audit Logging | T2602 — Log DB/server activities | ✅ Complete |
| Information Disclosure — Debug Endpoint | T49 — Remove debug capabilities | ✅ Complete |
| Denial of Service — No Rate Limiting | T1362 — Message throttling | ⚠️ Incomplete (auth only) |
| Elevation of Privilege — IDOR Orders | T338, T378, T2598 | ✅ Complete |
| Elevation of Privilege — Role Bypass | T184 — REST auth checks | ✅ Complete |
| SSRF — Image URL Fetching | T1365 — Mitigate SSRF | ✅ Complete |

---

## Source Artifacts

| Artifact | Location |
|---|---|
| Threat model generator | `docs/threat-model/generate_otm.py` |
| Architecture description | `docs/threat-model/PROMPT.md` |
| Audit logging module | `app/audit_log.py` |
| SDE project | https://sde-ent-onyxdrift.sdelab.net/…/damn-vulnerable-restaurant-api-game-from-devici-diagram-mar-2026/ |
| Code branch | `feature/sde-countermeasures-828-mar2026` |
