# DVRAG — SDE Project Creation from Devici OTM
## Executive Summary

**Date:** March 15, 2026
**Workflow:** Bring Your Own OTM → Act 3 entry point (Demo Workflow B)
**SDE Project:** DVRAG - From Devici OTM (Mar 2026)
**Project URL:** https://sde-ent-onyxdrift.sdelab.net/bunits/corporate-security-bu/secapp-assessment-application/dvrag-from-devici-otm-mar-2026/
**SDE Project ID:** 827

---

## What Was Done

### Step 1 — OTM Generation

The Devici-format OTM was generated programmatically using `docs/threat-model/generate_otm.py` (v8):

```
python3 docs/threat-model/generate_otm.py --output /tmp/otm_v8.json
```

Output: `/tmp/otm_v8.json` (32.6 KB)

| Artifact | Count |
|---|---|
| Components | 14 |
| Dataflows | 10 |
| STRIDE Threats | 11 |
| Mitigations | 9 |

The OTM encodes the full DVRAG architecture: 3 trust boundary zones (Internet, Application/Docker, Database), 7 functional nodes (FastAPI hub, Auth, Order, Menu, Admin, Debug, PostgreSQL), 2 external entities (Client, stickers), and 11 STRIDE-annotated threats with mitigations.

### Step 2 — SDE Project Creation

An SDE project was created via the SDE MCP (`user-sdelements-gitlab`) using the architecture description extracted directly from the OTM:

- **Application ID:** 568 (SecApp Assessment Application)
- **Business Unit ID:** 544 (Corporate Security BU)
- **Profile:** P1 (Blank)
- **Risk Policy:** 1

### Step 3 — Survey Auto-Fill (Dependency-Ordered)

The survey was populated in three dependency-ordered batches to ensure parent answers unlocked child answers before they were selected:

**Batch 1 — Base answers via `mutateByText` (exact match, similarity = 1.0):**
Web application, Web service, Uses a database, Contains components that communicate through a network, Linux/Unix, Python, JSON, Has direct or third party authentication for end users, devices or nodes, Uses encryption functions (not including SSL), Docker, Receives text input from users, CORS

**Batch 2 — Dependency chain via `updateByIds`:**
Stand-alone database that supports SQL (A11) → unlocks PostgreSQL (A1252); Authorizes Subjects (A23); Handles Personal Data (A130)

**Batch 3 — Additional applicable answers:**
Internet Facing (CA1), Microservice backend (A1264), Microservices ecosystem (A1262), Uses API gateway (A1593), Uses third-party software libraries (A1084), Passwords stored in configuration files (A21), Requires non-repudiation (A1122), GitHub (A1390), Uses passwords (A19), Performs diagnostic/debug logging (A90), RESTful web services (A731), Generates API tokens (A1062), Provides web services or external APIs (A754), This is a game application (A1150), Uses regular expressions on end-user input (A174), Uses Static or Dynamic Security Code Analysis (A777)

**Final survey state:** 56 answers selected across 30 questions. Survey committed (published).

### Step 4 — Comments on Every Answered Question

A comment was added to all 30 answered questions, each citing specific evidence from the OTM architecture, STRIDE threats, or codebase. No answered question was left without justification.

| Question | Topic | Comment Evidence Source |
|---|---|---|
| Q101 | Components In Development | OTM hub-and-spoke architecture, 5 service nodes |
| Q253 | Components In Use | PostgreSQL + FastAPI/SQLAlchemy/Pydantic libraries |
| Q500 | Architectural Features | Docker bridge network, Internet Zone trust boundary |
| Q322 | Architecture | Microservices topology from OTM canvas |
| Q252 | App Context | DVRAG is a security training game/CTF |
| Q294 | Target Platform | Python slim Docker images, Linux base |
| Q109 | Programming Language | Python 3 backend, JavaScript for web clients |
| Q191 | Web Client Technologies | FastAPI CORS middleware, cross-origin API clients |
| Q103 | Database | PostgreSQL standalone container, Database Zone |
| Q305 | DBMS | PostgreSQL in docker-compose, plaintext credentials (OTM threat) |
| Q115 | Data Formats | REST API JSON payloads, FastAPI default serialization |
| Q270 | Interfaces & APIs | FastAPI gateway → 5 service dataflows in OTM |
| Q120 | Authentication Features | JWT auth, OTM threat: JWT Algorithm Confusion (L:3, I:5) |
| Q129 | Server-to-Server Auth | Docker bridge network, JWT claim-based internal auth |
| Q213 | Password Management | Change/reset password functions, OTM brute force threat |
| Q127 | Authorizes Subjects | Admin/customer roles, OTM EoP: Admin Role Bypass |
| Q126 | Session Management | JWT token lifecycle, no revocation mechanism |
| Q259 | External Code/Data | FastAPI DI, SQLAlchemy ORM, dynamic library loading |
| Q215 | Input Validation | Menu search SQLi (OTM Tampering, L:4, I:5), Pydantic |
| Q131 | Encryption | Plaintext DB creds in docker-compose, JWT HS256 signing |
| Q214 | Miscellaneous | Async workers, debug endpoint (OTM critical: L:5, I:5), repudiation gap |
| Q186 | Application Layer Protocols | HTTP/HTTPS, OTM Client→FastAPI API Request dataflow |
| Q160 | Handles Personal Data | Email, passwords, order history in PostgreSQL |
| Q364 | Version Control | OWASP/Damn-Vulnerable-RESTaurant-API-Game on GitHub |
| Q235 | Security Code Analysis | DAST with Burp Suite, SAST on Python codebase |
| Q105 | Open Source Libraries | PyJWT, Passlib/Bcrypt, Cryptography packages |
| Q212 | Test Tools | Burp Suite for OWASP API Top 10 testing |
| Q308 | Containerization | Docker Compose, 2 containers, bridge network |
| Q220 | Changes Since Last Release | Initial creation — all scope is new |
| Q222 | Changes to User I/O | All API input/output endpoints captured as new |

---

## Results

| Metric | Value |
|---|---|
| Survey answers selected | 69 |
| Questions answered | 34 |
| Questions with comments | 34 / 34 (100%) |
| Risk-relevant requirements generated | **79** |
| Survey status | Published (committed) |

### Post-Commit Comment Gap — Root Cause

After the initial commit, a review found **4 questions with no comments**. The root cause: the `getDraft` with `include=survey` response only surfaces sections-visible questions (30 of 34). Four additional questions had answers selected through two mechanisms not reflected in the sections structure:

1. **Auto-selected by the P1 (Blank) profile at project creation** — Q106 (OWASP Development Tools Used: ESAPI) and Q224 (Privacy Regulations: GAPP) were pre-populated by the profile before any manual survey work.
2. **Auto-selected as dependency side-effects** — Q121 (Authentication Method: Uses passwords + Generates API tokens) and Q216 (HTTP-Based Protocols Used: RESTful web services) were unlocked and selected as downstream effects of other answers (Q120: Has direct authentication; Q186: Uses HTTP-based protocol), but did not appear in the sections tree.

**Fix applied:** All 4 questions were identified by comparing `getProjectSurvey` (which returns the full flat answer list of 69) against the sections-based view (which only showed 56). Comments were added to all 4.

**Lesson:** Always use `getProjectSurvey` as the authoritative source for selected answers, not `getDraft include=survey`, when verifying comment coverage.

#### The 4 recovered questions

| Question | ID | Answers | Comment Added |
|---|---|---|---|
| Authentication Method | Q121 | Uses passwords (A19), Generates API tokens (A1062) | Password auth + JWT token issuance; known brute force + algorithm confusion vulnerabilities |
| HTTP-Based Protocols Used | Q216 | RESTful web services (A731) | REST API over HTTP/HTTPS; OTM API Request dataflow |
| OWASP Development Tools Used | Q106 | ESAPI (A58) | Auto-selected; DVRAG is Python-based; Python equivalents noted (PyJWT, Passlib) |
| Privacy Regulations | Q224 | GAPP (A747) | Auto-selected; DVRAG stores PII (email, passwords, orders); debug endpoint exposes PII without auth |

### Requirements Breakdown

79 risk-relevant security requirements were generated, spanning all SDE phases:
- **Requirements phase** — security requirements driven by STRIDE threats (JWT, SQLi, IDOR, mass assignment)
- **Development phase** — secure coding tasks for Python/FastAPI (input validation, parameterized queries, auth enforcement)
- **Testing phase** — verification tasks linked to the DAST/SAST tooling answers
- **Deployment phase** — containerization hardening from the Docker + Linux platform answers

### Key Survey-to-Threat Mappings

| OTM STRIDE Threat | Survey Answer(s) That Unlocked Requirements |
|---|---|
| Spoofing — JWT Algorithm Confusion | Q120: Has direct authentication; Q126: Session management |
| Spoofing — Brute Force / Weak Password Policy | Q213: Password management features |
| Spoofing — Account Enumeration | Q120: Authentication features |
| Tampering — SQL Injection via Menu Search | Q215: Receives text input; Q103: SQL database |
| Tampering — Mass Assignment | Q215: Input validation; Q101: Web application |
| Repudiation — No Audit Logging | Q214: Requires non-repudiation |
| Information Disclosure — Debug Endpoint | Q214: Performs diagnostic/debug logging |
| Denial of Service — No Rate Limiting | Q500: Internet Facing; Q101: Web service |
| Elevation of Privilege — IDOR (Order) | Q127: Authorizes Subjects; Q270: Provides APIs |
| Elevation of Privilege — Admin Role Bypass | Q127: Authorizes Subjects; Q120: Authentication |

---

## Source Artifacts

| Artifact | Location |
|---|---|
| OTM generator script | `docs/threat-model/generate_otm.py` |
| OTM prompt and iteration history | `docs/threat-model/PROMPT.md` |
| Generated OTM (v8) | `/tmp/otm_v8.json` (32.6 KB, not committed) |
| SDE project | https://sde-ent-onyxdrift.sdelab.net/…/dvrag-from-devici-otm-mar-2026/ |

---

## Notes

- The OTM was used as the **sole architecture source** for Act 3 — no live Devici connection was required. This validates the "Bring Your Own OTM" flow documented in `AI Generated/Demo Workflows/dvrag-devici-sde-demo-runbook.md`.
- The `mutateByText` API matched all base answers at **similarity = 1.0** (exact match), confirming that the OTM architecture language maps directly to SDE's survey taxonomy.
- The `generate_otm.py` script can be re-run at any time to regenerate a fresh OTM. Re-running Act 3 from the new OTM (with a versioned project name) would allow before/after requirement comparisons as the vulnerability profile changes.
