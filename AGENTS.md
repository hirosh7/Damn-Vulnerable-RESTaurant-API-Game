# AGENTS.md — DVRAG Security Assessment

## Survey Traceability — 2026-04-20

- **Project ID:** 852
- **Project Name:** DVRAG Survey Traceability - Apr 2026
- **Project URL:** https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-survey-traceability-apr-2026/
- **Application:** Damn Vulnerable RESTaurant API Game (ID 585)
- **Branch:** demo-test
- **Profile:** P1 (Blank)
- **SDE MCP Server:** user-kj-partner-sde-mcp

### Survey Metrics

| Metric | Value |
|---|---|
| Total answers selected | **49** |
| Manually answered (agent) | 25 |
| Auto-answered (dependencies/defaults) | 24 |
| Questions with traceability notes | **27** |
| Auto-answered questions flagged for human review | **6** |
| Risk-relevant countermeasures generated | **62** |
| Spec generation | **confirmed** |

### Manually Answered Questions (codebase-grounded)

| Question | Answer(s) | Key Evidence |
|---|---|---|
| Components In Development | Web service | app/init_app.py, app/apis/router.py |
| Components In Use | Uses a database; Uses third-party libraries | app/db/session.py, pyproject.toml |
| Architectural Features | Network communication; Internet Facing | docker-compose.yml |
| Application Target Platform | Linux/Unix | Dockerfile (python:3.10-slim) |
| Programming Language | Python | pyproject.toml |
| Database | Stand-alone SQL database | docker-compose.yml (postgres:15.4-alpine) |
| DBMS | PostgreSQL | app/config.py (DATABASE_URL) |
| Data Formats | JSON | app/apis/ (Pydantic serialization) |
| Authentication Features | Direct end-user authentication | app/apis/auth/services/get_token_service.py |
| Authentication Method | Passwords; API tokens; Database auth | app/apis/auth/utils/utils.py |
| Server-to-Server Auth | Yes | app/config.py (DB credentials) |
| Password Management | Forgot password function | app/apis/auth/services/reset_password_service.py |
| Authorizes Subjects | Yes (RBAC) | app/apis/auth/utils/roles_based_auth_checker.py |
| Session Management | Yes (JWT 30-min expiry) | app/apis/auth/utils/jwt_auth.py |
| Application Layer Protocols | HTTP-based | app/main.py (Uvicorn port 8091) |
| HTTP-Based Protocols | RESTful web services | app/apis/router.py |
| Containerization | Docker | Dockerfile, docker-compose.yml |
| Version Control | GitHub | README.md, .pre-commit-config.yaml |
| Open Source Security Libraries | Yes (passlib, python-jose, slowapi) | pyproject.toml |
| Handles Personal Data | Yes (PII: usernames, phone, orders) | app/db/models.py |
| Privacy Regulations | GAPP | app/db/models.py (PII fields) |

### Auto-Answered Questions (flagged for human review)

| Question | Answer(s) | Derivation |
|---|---|---|
| Test Tools Permitted | Burp Suite | System default for web service |
| OWASP Development Tools | ESAPI | Dependency of OSS permitted |
| More Features | Multi-threaded; Debug logging; Random numbers | Web service + auth dependencies |
| Internal Hidden Properties | 7 hidden properties (auth, server, logging, data, software, services, containers) | Derived from visible answers |
| Changes Since Last Release | 10 change categories | P1 Blank profile defaults |
| Changes to User I/O | Output changes; Input changes | Dependency chain from Changes section |

<!-- SDE-SECURITY-HARDENING-START -->
## Security Hardening Execution Contract

## Project Overview

| Property | Value |
|----------|-------|
| Application | Damn Vulnerable RESTaurant API Game |
| SD Elements Project | [DVRAG Security Hardening - Apr 2026](https://sde-ent-onyxdrift.sdelab.net/bunits/dvrag-security/damn-vulnerable-restaurant-api-game/dvrag-security-hardening-apr-2026/) |
| Project ID | 854 |
| Total Countermeasures | 65 |
| Branch | security-hardening/dvrag-security-hardening-apr-2026-20260427 |

## Countermeasure Summary by Category

| Category | Count | Description |
|----------|-------|-------------|
| CODE_FIX | 48 | Code/config changes in repo |
| ML_CODE | 0 | ML security with code to fix |
| ML_DOC | 0 | ML guidance (no ML code) |
| INFRA | 3 | External infrastructure |
| **FILE-TRACKED TOTAL** | **51** | Countermeasures with local skill files |

> **PROCESS countermeasures (14) are noted in SD Elements only — not tracked locally.**

## Skill Files

| Domain | Countermeasures |
|--------|----------------|
| authentication | 10 |
| authorization | 4 |
| api-security | 7 |
| database | 4 |
| os-security | 3 |
| privacy | 5 |
| container-security | 3 |
| github-security | 12 |
| infra | 3 |

### authentication

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T2 | Secure the password reset mechanism | [skills/authentication/854-T2-secure-password-reset/SKILL.md](./skills/authentication/854-T2-secure-password-reset/SKILL.md) | 9 | CODE_FIX | Pending |
| 854-T20 | Generate unique session IDs and reset old IDs after authentication | [skills/authentication/854-T20-generate-unique-session-ids/SKILL.md](./skills/authentication/854-T20-generate-unique-session-ids/SKILL.md) | 9 | CODE_FIX | Pending |
| 854-T59 | Use standard libraries for cryptography | [skills/authentication/854-T59-use-standard-crypto-libraries/SKILL.md](./skills/authentication/854-T59-use-standard-crypto-libraries/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T60 | Use correct and approved cryptographic algorithms | [skills/authentication/854-T60-approved-crypto-algorithms/SKILL.md](./skills/authentication/854-T60-approved-crypto-algorithms/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T69 | Strong password requirements for server-to-server accounts | [skills/authentication/854-T69-strong-s2s-password-requirements/SKILL.md](./skills/authentication/854-T69-strong-s2s-password-requirements/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T70 | Implement account lockout or authentication throttling | [skills/authentication/854-T70-account-lockout-throttling/SKILL.md](./skills/authentication/854-T70-account-lockout-throttling/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T76 | Do not hardcode passwords | [skills/authentication/854-T76-no-hardcoded-passwords/SKILL.md](./skills/authentication/854-T76-no-hardcoded-passwords/SKILL.md) | 10 | CODE_FIX | Pending |
| 854-T151 | Use cryptographically secure random numbers | [skills/authentication/854-T151-cryptographically-secure-random/SKILL.md](./skills/authentication/854-T151-cryptographically-secure-random/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T156 | Validate certificate and its chain of trust properly | [skills/authentication/854-T156-validate-certificate-chain/SKILL.md](./skills/authentication/854-T156-validate-certificate-chain/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T1889 | Secure the configuration of the authorization server | [skills/authentication/854-T1889-secure-authorization-server-config/SKILL.md](./skills/authentication/854-T1889-secure-authorization-server-config/SKILL.md) | 7 | CODE_FIX | Pending |

### authorization

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T338 | Control access to resources through user authentication and authorization | [skills/authorization/854-T338-control-access-resources/SKILL.md](./skills/authorization/854-T338-control-access-resources/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T378 | Authorize every request for data objects | [skills/authorization/854-T378-authorize-every-data-request/SKILL.md](./skills/authorization/854-T378-authorize-every-data-request/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T2598 | Implement query-level access control | [skills/authorization/854-T2598-query-level-access-control/SKILL.md](./skills/authorization/854-T2598-query-level-access-control/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T2600 | Control the result set size returned by a query | [skills/authorization/854-T2600-control-result-set-size/SKILL.md](./skills/authorization/854-T2600-control-result-set-size/SKILL.md) | 7 | CODE_FIX | Pending |

### api-security

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T35 | Fine-tune HTTP server settings | [skills/api-security/854-T35-fine-tune-http-settings/SKILL.md](./skills/api-security/854-T35-fine-tune-http-settings/SKILL.md) | 9 | CODE_FIX | Pending |
| 854-T49 | Disable and remove debug capabilities | [skills/api-security/854-T49-disable-debug-capabilities/SKILL.md](./skills/api-security/854-T49-disable-debug-capabilities/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T50 | Use indirect object reference maps | [skills/api-security/854-T50-indirect-object-reference/SKILL.md](./skills/api-security/854-T50-indirect-object-reference/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T536 | Restrict the size of incoming messages | [skills/api-security/854-T536-restrict-message-size/SKILL.md](./skills/api-security/854-T536-restrict-message-size/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T1362 | Perform message throttling in Web APIs | [skills/api-security/854-T1362-message-throttling-web-apis/SKILL.md](./skills/api-security/854-T1362-message-throttling-web-apis/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T1365 | Mitigate Server Side Request Forgery | [skills/api-security/854-T1365-mitigate-ssrf/SKILL.md](./skills/api-security/854-T1365-mitigate-ssrf/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T2139 | Prevent information exposure through APIs | [skills/api-security/854-T2139-prevent-api-info-exposure/SKILL.md](./skills/api-security/854-T2139-prevent-api-info-exposure/SKILL.md) | 7 | CODE_FIX | Pending |

### database

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T19 | Restrict Application's Access to Database | [skills/database/854-T19-restrict-db-access/SKILL.md](./skills/database/854-T19-restrict-db-access/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T38 | Bind variables in SQL statements | [skills/database/854-T38-bind-sql-variables/SKILL.md](./skills/database/854-T38-bind-sql-variables/SKILL.md) | 10 | CODE_FIX | Pending |
| 854-T2599 | Protect against connection string parameter pollution | [skills/database/854-T2599-connection-string-pollution/SKILL.md](./skills/database/854-T2599-connection-string-pollution/SKILL.md) | 9 | CODE_FIX | Pending |
| 854-T2602 | Log typical database and server activities | [skills/database/854-T2602-log-db-activities/SKILL.md](./skills/database/854-T2602-log-db-activities/SKILL.md) | 8 | CODE_FIX | Pending |

### os-security

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T43 | Avoid unsafe operating system interaction | [skills/os-security/854-T43-avoid-unsafe-os-interaction/SKILL.md](./skills/os-security/854-T43-avoid-unsafe-os-interaction/SKILL.md) | 10 | CODE_FIX | Pending |
| 854-T214 | Protect confidential files on OS or server | [skills/os-security/854-T214-protect-confidential-files/SKILL.md](./skills/os-security/854-T214-protect-confidential-files/SKILL.md) | 9 | CODE_FIX | Pending |
| 854-T295 | Avoid storing unencrypted confidential data | [skills/os-security/854-T295-no-unencrypted-confidential-data/SKILL.md](./skills/os-security/854-T295-no-unencrypted-confidential-data/SKILL.md) | 7 | CODE_FIX | Pending |

### privacy

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T349 | Protect audit information and logs | [skills/privacy/854-T349-protect-audit-logs/SKILL.md](./skills/privacy/854-T349-protect-audit-logs/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T558 | Authenticate all components before network communication | [skills/privacy/854-T558-authenticate-all-components/SKILL.md](./skills/privacy/854-T558-authenticate-all-components/SKILL.md) | 9 | CODE_FIX | Pending |
| 854-T622 | Assign a random revocable token to actions in the game | [skills/privacy/854-T622-random-revocable-token-game/SKILL.md](./skills/privacy/854-T622-random-revocable-token-game/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T627 | Follow best practices for secure transactional processing | [skills/privacy/854-T627-secure-transactional-processing/SKILL.md](./skills/privacy/854-T627-secure-transactional-processing/SKILL.md) | 7 | CODE_FIX | Pending |
| 854-T742 | Implement technical measures for accuracy of personal information | [skills/privacy/854-T742-personal-info-accuracy/SKILL.md](./skills/privacy/854-T742-personal-info-accuracy/SKILL.md) | 7 | CODE_FIX | Pending |

### container-security

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T1917 | Perform container security assessment | [skills/container-security/854-T1917-container-security-assessment/SKILL.md](./skills/container-security/854-T1917-container-security-assessment/SKILL.md) | 10 | CODE_FIX | Pending |
| 854-T4746 | Ensure container images are secure | [skills/container-security/854-T4746-ensure-container-images-secure/SKILL.md](./skills/container-security/854-T4746-ensure-container-images-secure/SKILL.md) | 10 | CODE_FIX | Pending |
| 854-T4751 | Reduce the attack surface of container images | [skills/container-security/854-T4751-reduce-container-attack-surface/SKILL.md](./skills/container-security/854-T4751-reduce-container-attack-surface/SKILL.md) | 10 | CODE_FIX | Pending |

### github-security

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T186 | Use recommended settings and latest patches for third-party libraries | [skills/github-security/854-T186-update-third-party-libraries/SKILL.md](./skills/github-security/854-T186-update-third-party-libraries/SKILL.md) | 10 | CODE_FIX | Pending |
| 854-T3900 | Implement and use code change management strategy (GitHub) | [skills/github-security/854-T3900-code-change-management/SKILL.md](./skills/github-security/854-T3900-code-change-management/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3901 | Enforce repository management and security strategies (GitHub) | [skills/github-security/854-T3901-repository-management-security/SKILL.md](./skills/github-security/854-T3901-repository-management-security/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3903 | Implement application and webhook security strategies (GitHub) | [skills/github-security/854-T3903-app-webhook-security/SKILL.md](./skills/github-security/854-T3903-app-webhook-security/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3905 | Ensure pipeline efficiency and security (GitHub) | [skills/github-security/854-T3905-pipeline-efficiency-security/SKILL.md](./skills/github-security/854-T3905-pipeline-efficiency-security/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3906 | Implement secure build worker management (GitHub) | [skills/github-security/854-T3906-secure-build-worker-management/SKILL.md](./skills/github-security/854-T3906-secure-build-worker-management/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3907 | Ensure pipeline definition and security (GitHub) | [skills/github-security/854-T3907-pipeline-definition-security/SKILL.md](./skills/github-security/854-T3907-pipeline-definition-security/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3908 | Enforce artifact signing (GitHub) | [skills/github-security/854-T3908-enforce-artifact-signing/SKILL.md](./skills/github-security/854-T3908-enforce-artifact-signing/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3909 | Ensure third-party artifact security (GitHub) | [skills/github-security/854-T3909-third-party-artifact-security/SKILL.md](./skills/github-security/854-T3909-third-party-artifact-security/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3910 | Implement dependency management strategy (GitHub) | [skills/github-security/854-T3910-dependency-management/SKILL.md](./skills/github-security/854-T3910-dependency-management/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3913 | Implement package registry security (GitHub) | [skills/github-security/854-T3913-package-registry-security/SKILL.md](./skills/github-security/854-T3913-package-registry-security/SKILL.md) | 8 | CODE_FIX | Pending |
| 854-T3914 | Implement artifact origin information policy (GitHub) | [skills/github-security/854-T3914-artifact-origin-policy/SKILL.md](./skills/github-security/854-T3914-artifact-origin-policy/SKILL.md) | 8 | CODE_FIX | Pending |

### infra

| ID | Title | Skill File | Priority | Category | Status |
|----|-------|-----------|----------|----------|--------|
| 854-T21 | Ensure all data in transit is encrypted using a secure TLS channel | [skills/infra/854-T21-tls-encryption/SKILL.md](./skills/infra/854-T21-tls-encryption/SKILL.md) | 9 | INFRA | Pending |
| 854-T374 | Offload HTTP request handling to dedicated modules | [skills/infra/854-T374-offload-http-handling/SKILL.md](./skills/infra/854-T374-offload-http-handling/SKILL.md) | 7 | INFRA | Pending |
| 854-T2256 | Authenticate and log all access to registries | [skills/infra/854-T2256-authenticate-registry-access/SKILL.md](./skills/infra/854-T2256-authenticate-registry-access/SKILL.md) | 8 | INFRA | Pending |

## Completion Requirements

**ALL 51 file-tracked countermeasures must be addressed. No exceptions.**

### Progress Tracking

| Domain | Total | Applied | Documented | Remaining |
|--------|-------|---------|------------|-----------|
| authentication | 10 | 0 | 0 | 10 |
| authorization | 4 | 0 | 0 | 4 |
| api-security | 7 | 0 | 0 | 7 |
| database | 4 | 0 | 0 | 4 |
| os-security | 3 | 0 | 0 | 3 |
| privacy | 5 | 0 | 0 | 5 |
| container-security | 3 | 0 | 0 | 3 |
| github-security | 12 | 0 | 0 | 12 |
| infra | 3 | 0 | 0 | 3 |
| **TOTAL** | **51** | **0** | **0** | **51** |

**Remaining MUST reach 0 before completion.**

## Verification Checklist

- [ ] All CODE_FIX countermeasures have fixes applied
- [ ] All fixes are in ORIGINAL files (no *_secure.* alternatives)
- [ ] All non-code items documented with justification
- [ ] Total addressed = 51
<!-- SDE-SECURITY-HARDENING-END -->
