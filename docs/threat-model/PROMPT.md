# Threat Model Generation Prompt

This document captures the prompt and context used to drive `generate_otm.py` — the script that builds the Devici OTM for the Damn Vulnerable RESTaurant API Game.

---

## Architecture Description (input to the agent)

The Damn Vulnerable RESTaurant API Game is a deliberately vulnerable FastAPI application designed for learning API security testing. The architecture consists of:

**Stack**: Python 3 / FastAPI / SQLAlchemy ORM / PostgreSQL, containerized with Docker Compose.

**Components**:

| Component | Role | Notes |
|---|---|---|
| FastAPI REST API | Central API gateway | All requests route through here; no middleware filtering |
| Auth Service | Authentication + registration | JWT-based; no algorithm enforcement; weak password policy |
| Order Service | Order CRUD | No ownership checks on retrieval (BOLA/IDOR) |
| Menu Service | Menu item listing + search | Raw SQL in search endpoint (SQL injection) |
| Admin Service | User role management, chef password reset | Role checked via JWT claim only; no re-validation |
| Debug Endpoint | Exposes internal state | No authentication; leaks env vars, DB strings, stack traces |
| PostgreSQL Database | Persistent data store | Credentials in plaintext docker-compose env vars |

**Trust boundaries**:
- Internet Zone — external clients (browsers, API consumers)
- Application Zone (Docker) — all FastAPI services in a single container
- Database Zone — PostgreSQL in a separate container on the Docker network

**Known vulnerability classes** (STRIDE):
- **Spoofing**: JWT algorithm confusion (`none`/HS256 swap), brute force (no lockout, 1-char passwords), account enumeration (differential error messages)
- **Tampering**: SQL injection in menu search, mass assignment in registration/profile update
- **Repudiation**: No audit logging on any state-changing operation
- **Information Disclosure**: Debug endpoint exposes internals without auth
- **Denial of Service**: No rate limiting on any endpoint; public menu endpoint scrapable
- **Elevation of Privilege**: IDOR on order retrieval, admin role bypass via stale/forged token claims

---

## Agent Instructions

Generate a STRIDE threat model for the DVRAG application and import it into Devici. Follow the `devici-sde-devsecops-pipeline` skill's Act 1 OTM authoring rules.

### Layout requirements

1. Three trust boundary zones arranged left-to-right: Internet → Application → Database, with ~20-30px gaps between zone edges.
2. FastAPI REST API positioned as a centered hub at the top of the Application Zone — not in the same column as leaf services.
3. Two service columns in the App Zone:
   - **Col-1 (left)**: Auth, Order, Menu — stacked vertically with ~110px spacing
   - **Col-2 (right)**: Admin, Debug — stacked vertically with ~110px spacing
4. PostgreSQL in the Database Zone, vertically centered relative to the service connection span.
5. Client / API Consumer in the Internet Zone, vertically aligned so the API Request flow to FastAPI is roughly horizontal.

### Flow routing

- FastAPI ← → Col-1 services: `sourceLeft` / `targetRight` (flows go left from the hub)
- FastAPI → Col-2 services: `sourceRight` / `targetLeft` (flows go right from the hub)
- FastAPI → Postgres: route via `sourceTop` / `targetTop` with waypoints above all nodes to separate from the Admin/Debug right-side flows
- Service → Postgres (Auth, Order, Menu): `sourceRight` / `targetLeft` with `smoothstep` type and staggered y-waypoints (e.g. 245, 355, 470) to prevent convergence
- Hide labels on obvious flows: Order Request, Menu Request, and all three service→DB flows (`hiddenLabel: true`)

### Annotations

- **Attack Surface sticker** in the Internet Zone listing the key external-facing risks
- **Color legend sticker** in the App Zone (bottom-right) using plain text markers `[C]`, `[H]`, `[M]`, `[L]` — no emoji (Devici renders them poorly)
- **DB context sticker** in the Database Zone explaining what each service→DB flow carries

### Node colors (risk-coded)

| Node | Color | Hex | Risk level |
|---|---|---|---|
| FastAPI REST API | Blue | `#3B82F699` | Info (hub) |
| Auth Service | Purple | `#8B5CF699` | Medium |
| Order Service | Red | `#EF444499` | High (BOLA/IDOR) |
| Menu Service | Orange | `#F9731699` | Medium (SQLi) |
| Admin Service | Amber | `#F59E0B99` | Medium |
| Debug Endpoint | Dark red | `#DC262699` | Critical |
| PostgreSQL | Teal | `#14B8A699` | Datastore |

### Trust boundary zone tints

| Zone | Hex |
|---|---|
| Internet | `#FF6B6B1A` (red tint) |
| Application | `#3B82F61A` (blue tint) |
| Database | `#14B8A61A` (teal tint) |

### Threats

Attach 11 STRIDE threats across components:

- **Client**: Account enumeration (Spoofing), public endpoint scraping (DoS)
- **FastAPI**: No rate limiting (DoS), mass assignment (Tampering)
- **Auth**: JWT algorithm confusion (Spoofing), brute force (Spoofing)
- **Order**: IDOR in order retrieval (EoP), no audit logging (Repudiation)
- **Menu**: SQL injection via search (Tampering)
- **Admin**: Role bypass via insecure direct reference (EoP)
- **Debug**: Exposes internals without auth (Information Disclosure)

Each threat should have a corresponding mitigation.

### Output

Write the OTM JSON to `/tmp/otm_v7.json`, validate bounds, then import via:

```
threat_model_import_otm(
    collection_id="e39684a2-e0d1-4ebf-9e9b-e4eafad6892e",
    otm_file_path="/tmp/otm_v7.json"
)
```

Verify the canvas via `GET /api/v1/canvases/<canvas_id>` to confirm positions, colors, and edge routing are correct.

---

## Iteration History

| Version | Key changes |
|---|---|
| v1 | Initial OTM — nodes appeared in wrong zones (absolute vs relative positioning confusion) |
| v2 | Fixed: child positions made relative to parent zone — still wrong approach |
| v3 | Fixed: all positions absolute, self-referencing `parent.trustZone`, `arrowclosed` markers, `destination` field |
| v4 | Added: zone tint colors, node risk colors, hidden DB flow labels, smoothstep routing, staggered waypoints, taller FastAPI hub, client threats, sticker clipping fix |
| v5 | Clean regeneration from updated skill — validated all rules are repeatable |
| v6 | FastAPI centered as hub, Postgres vertically centered, color legend sticker, explicit sticker widths, FastAPI→DB routed high |
| v7 | Decluttered labels (hidden Order/Menu Request), FastAPI→DB via sourceTop, tighter DB zone gap, plain-text legend (no emoji), client aligned with FastAPI, DB context sticker |
| v8 | Color-coded edges matching destination nodes (primary=full alpha, secondary service→DB=50% alpha faded); `→` arrow chars in labels as arrowhead workaround; confirmed `"editable"` type causes spaghetti (reverted to `"default"`); confirmed neither `"arrowclosed"` nor `"end"` renders SVG markers — Devici limitation |
