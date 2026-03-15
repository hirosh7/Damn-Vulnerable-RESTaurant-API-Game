# DVRAG — Architecture & Threat Model Description

This document describes the architecture and known vulnerability profile of the Damn Vulnerable RESTaurant API Game, used as the input for STRIDE threat model generation.

---

## Architecture Description

The Damn Vulnerable RESTaurant API Game is a deliberately vulnerable FastAPI application designed for learning API security testing.

**Stack**: Python 3 / FastAPI / SQLAlchemy ORM / PostgreSQL, containerized with Docker Compose.

**Components**:

| Component | Role | Security Notes |
|---|---|---|
| FastAPI REST API | Central API gateway | All requests route through here; no middleware filtering |
| Auth Service | Authentication + registration | JWT-based; no algorithm enforcement; weak password policy |
| Order Service | Order CRUD | No ownership checks on retrieval (BOLA/IDOR) |
| Menu Service | Menu item listing + search | Raw SQL in search endpoint (SQL injection) |
| Admin Service | User role management, chef password reset | Role checked via JWT claim only; no re-validation |
| Debug Endpoint | Exposes internal state | No authentication; leaks env vars, DB strings, stack traces |
| PostgreSQL Database | Persistent data store | Credentials in plaintext environment configuration |

**Trust boundaries**:
- Internet Zone — external clients (browsers, API consumers)
- Application Zone (Docker) — all FastAPI services in a single container
- Database Zone — PostgreSQL in a separate container on the Docker network

---

## STRIDE Threat Coverage

| Category | Threats |
|---|---|
| **Spoofing** | JWT algorithm confusion (`none`/HS256 swap), brute force (no lockout, 1-character passwords), account enumeration via differential error messages |
| **Tampering** | SQL injection in menu search endpoint, mass assignment in registration and profile update |
| **Repudiation** | No audit logging on any state-changing operation |
| **Information Disclosure** | Debug endpoint exposes internals without authentication |
| **Denial of Service** | No rate limiting on any endpoint; public menu endpoint freely scrapable |
| **Elevation of Privilege** | IDOR on order retrieval (BOLA), admin role bypass via stale or forged token claims |

---

## Visual Design

### Node Risk Coding

| Component | Risk Level | Color |
|---|---|---|
| FastAPI REST API | Info (hub) | Blue |
| Auth Service | Medium | Purple |
| Order Service | High — BOLA/IDOR | Red |
| Menu Service | Medium — SQL injection | Orange |
| Admin Service | Medium | Amber |
| Debug Endpoint | **Critical** | Dark red |
| PostgreSQL | Datastore | Teal |

### Trust Boundary Zones

| Zone | Tint |
|---|---|
| Internet | Red |
| Application (Docker) | Blue |
| Database | Teal |
