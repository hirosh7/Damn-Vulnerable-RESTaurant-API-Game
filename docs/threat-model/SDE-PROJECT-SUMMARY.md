# DVRAG — Security Requirements Project Summary
## From Threat Model to SD Elements

**Date:** March 15, 2026
**Application:** Damn Vulnerable RESTaurant API Game (DVRAG)
**SDE Project:** DVRAG - From Devici OTM (Mar 2026)
**Project URL:** https://sde-ent-onyxdrift.sdelab.net/bunits/corporate-security-bu/secapp-assessment-application/dvrag-from-devici-otm-mar-2026/

---

## What Was Done

### Step 1 — Threat Model Generation

A STRIDE threat model was generated programmatically from the DVRAG architecture description. The model encodes:

| Artifact | Count |
|---|---|
| Architecture components | 14 |
| Data flows | 10 |
| STRIDE threats | 11 |
| Mitigations | 9 |

The model covers 3 trust boundary zones (Internet, Application/Docker, Database), 7 functional components (FastAPI hub, Auth, Order, Menu, Admin, Debug Endpoint, PostgreSQL), and 11 STRIDE-annotated threats with corresponding mitigations.

### Step 2 — SD Elements Project Creation

An SD Elements project was created using the architecture description extracted directly from the threat model, eliminating any manual data re-entry between tools.

### Step 3 — Automated Survey Completion

The security survey was populated automatically in dependency order — base answers unlock downstream questions, which are then evaluated and answered in sequence. The survey was completed across three passes to ensure all dependent questions were captured and answered.

**Final state:** 69 answers selected across 34 questions. Survey published.

### Step 4 — Evidence Comments on Every Question

An evidence-backed comment was added to every answered survey question, each citing the specific threat, architectural component, or code pattern that justified the answer.

| Question Topic | Evidence Source |
|---|---|
| Components In Development | Hub-and-spoke architecture, 5 service components |
| Components In Use | PostgreSQL + FastAPI/SQLAlchemy/Pydantic libraries |
| Architectural Features | Docker bridge network, internet-facing trust boundary |
| Architecture | Microservices topology from threat model |
| Application Context | Security training application (OWASP-based) |
| Target Platform | Python Docker containers on Linux |
| Programming Language | Python 3 backend |
| Web Client Technologies | CORS middleware for cross-origin API clients |
| Database | PostgreSQL standalone container |
| Database Management System | PostgreSQL; credentials stored in environment config |
| Data Formats | JSON REST API payloads |
| Interfaces & APIs | FastAPI gateway routing to 5 service components |
| Authentication Features | JWT auth; known algorithm confusion vulnerability |
| Server-to-Server Auth | Docker network; JWT claim-based internal auth |
| Password Management | Change/reset password; known brute force vulnerability |
| Authorization | Admin/customer roles; known role bypass vulnerability |
| Session Management | JWT token lifecycle; no revocation mechanism |
| External Code/Data | Dynamic library loading via FastAPI dependency injection |
| Input Validation | Menu search SQL injection; Pydantic model validation |
| Encryption | Environment-stored credentials; JWT token signing |
| Miscellaneous | Async workers; debug endpoint exposure; repudiation gap |
| Application Layer Protocols | HTTP/HTTPS REST API traffic |
| Authentication Method | Password auth + JWT token issuance |
| HTTP-Based Protocols | RESTful web services |
| Handles Personal Data | Email, passwords, order history in PostgreSQL |
| OWASP Development Tools | Python-equivalent OWASP security libraries |
| Privacy Regulations | GAPP; PII stored and exposed via debug endpoint |
| Version Control | GitHub repository |
| Security Code Analysis | DAST (Burp Suite) + SAST on Python codebase |
| Open Source Libraries | PyJWT, Passlib/Bcrypt, Cryptography |
| Test Tools | Burp Suite for OWASP API Top 10 testing |
| Containerization | Docker Compose, 2 containers, bridge network |
| Changes Since Last Release | Full initial scope captured |
| Changes to User I/O | All API input/output endpoints captured as new |

---

## Results

| Metric | Value |
|---|---|
| Survey answers selected | 69 |
| Questions answered | 34 |
| Questions with evidence comments | 34 / 34 (100%) |
| Risk-relevant requirements generated | **79** |
| Survey status | Published |

### Requirements Breakdown

79 risk-relevant security requirements generated across all SD Elements phases:

- **Requirements** — security requirements driven by STRIDE threats (JWT, SQL injection, IDOR, mass assignment)
- **Development** — secure coding tasks for Python/FastAPI (input validation, parameterized queries, auth enforcement)
- **Testing** — verification tasks linked to DAST/SAST tooling
- **Deployment** — containerization hardening from Docker and Linux platform configuration

### Threat-to-Requirements Traceability

| STRIDE Threat | Survey Answers That Generated Requirements |
|---|---|
| Spoofing — JWT Algorithm Confusion | Authentication features; Session management |
| Spoofing — Brute Force / Weak Password Policy | Password management features |
| Spoofing — Account Enumeration | Authentication features |
| Tampering — SQL Injection via Menu Search | Receives text input; SQL database |
| Tampering — Mass Assignment | Input validation; Web application |
| Repudiation — No Audit Logging | Requires non-repudiation |
| Information Disclosure — Debug Endpoint | Diagnostic/debug logging |
| Denial of Service — No Rate Limiting | Internet Facing; Web service |
| Elevation of Privilege — IDOR (Order Retrieval) | Authorizes Subjects; Provides APIs |
| Elevation of Privilege — Admin Role Bypass | Authorizes Subjects; Authentication |

---

## Source Artifacts

| Artifact | Location |
|---|---|
| Threat model generator | `docs/threat-model/generate_otm.py` |
| Architecture description | `docs/threat-model/PROMPT.md` |
| SD Elements project | https://sde-ent-onyxdrift.sdelab.net/…/dvrag-from-devici-otm-mar-2026/ |
