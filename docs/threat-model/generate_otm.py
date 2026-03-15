#!/usr/bin/env python3
"""
DVRAG Devici OTM Generator — v8
Generates a Devici-compatible OTM JSON for the Damn Vulnerable RESTaurant API Game.

v8 improvements over v7:
  1. Color-coded edges — each flow colored to match its destination node
     so overlapping/crossing lines are visually distinguishable
  2. Arrowhead colors match their line for clear directional indication

Usage:
  python3 generate_otm.py [--output /tmp/otm.json]
  python3 generate_otm.py --validate-only

The output JSON is ready for import via:
  threat_model_import_otm(collection_id="...", otm_file_path="/tmp/otm_v8.json")
"""

import json
import uuid
import argparse
import sys

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
CANVAS_W = 1450
CANVAS_H = 700

# Trust boundary zones (absolute canvas coords)
TZ_INTERNET = dict(x=20,   y=20, w=270, h=650)
TZ_APP      = dict(x=350,  y=20, w=750, h=650)
TZ_DB       = dict(x=1120, y=20, w=310, h=650)  # v7: moved left, slightly wider

# Node sizes
SZ_HUB   = dict(w=180, h=120)   # FastAPI — tall hub
SZ_SVC   = dict(w=160, h=80)    # service leaf nodes
SZ_STORE = dict(w=180, h=80)    # datastore
SZ_EXT   = dict(w=180, h=80)    # external entity

# Node positions (absolute canvas coords)
# Client — vertically aligned with FastAPI hub
# FastAPI — horizontally centered in App Zone, top row
# Col-1 services (left side of App Zone)
# Col-2 services (right side of App Zone)
# Postgres — vertically centered relative to service y-midpoints
NODE_POS = {
    "client":    dict(x=55,   y=120),   # v7: moved up to align horizontally with FastAPI
    "fastapi":   dict(x=635,  y=40),    # App Zone center (635+90=725=350+375)
    "auth":      dict(x=385,  y=200),   # Col-1
    "order":     dict(x=385,  y=310),   # Col-1
    "menu":      dict(x=385,  y=430),   # Col-1
    "admin":     dict(x=870,  y=255),   # Col-2
    "debug":     dict(x=870,  y=365),   # Col-2
    "postgres":  dict(x=1155, y=290),   # v7: shifted left with DB Zone
}

# Sticker positions
STICKER_INTERNET = dict(x=40,  y=360, w=230, h=260)
STICKER_LEGEND   = dict(x=868, y=490, w=210, h=155)
STICKER_DB_NOTE  = dict(x=1135, y=420, w=270, h=130)  # v7: near Postgres

# Color palette
COLOR_ZONE_INTERNET = "#FF6B6B1A"
COLOR_ZONE_APP      = "#3B82F61A"
COLOR_ZONE_DB       = "#14B8A61A"

COLOR_FASTAPI   = "#3B82F699"   # blue — info
COLOR_AUTH      = "#8B5CF699"   # purple — medium
COLOR_ORDER     = "#EF444499"   # red — high (BOLA/IDOR)
COLOR_MENU      = "#F9731699"   # orange — medium (SQLi)
COLOR_ADMIN     = "#F59E0B99"   # amber — medium
COLOR_DEBUG     = "#DC262699"   # dark red — critical
COLOR_POSTGRES  = "#14B8A699"   # teal — datastore

EDGE_COLOR   = "#6F767ECC"   # default fallback (unused in v8)
EDGE_COLOR_B = "#6F767E"

# v8: per-edge colors — each edge matches its destination node for traceability.
# Format: (line color with alpha CC, arrowhead color without alpha)
EDGE_INBOUND   = ("#2563EBCC", "#2563EB")   # blue — Client → FastAPI
EDGE_TO_AUTH   = ("#8B5CF6CC", "#8B5CF6")   # purple — to Auth
EDGE_TO_ORDER  = ("#EF4444CC", "#EF4444")   # red — to Order
EDGE_TO_MENU   = ("#F97316CC", "#F97316")   # orange — to Menu
EDGE_TO_ADMIN  = ("#F59E0BCC", "#F59E0B")   # amber — to Admin
EDGE_TO_DEBUG  = ("#DC2626CC", "#DC2626")   # dark red — to Debug
EDGE_TO_DB     = ("#0D9488CC", "#0D9488")   # teal — any flow → Postgres
EDGE_AUTH_DB   = ("#8B5CF680", "#8B5CF6")   # purple faded — Auth → DB
EDGE_ORDER_DB  = ("#EF444480", "#EF4444")   # red faded — Order → DB
EDGE_MENU_DB   = ("#F9731680", "#F97316")   # orange faded — Menu → DB


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def uid() -> str:
    return str(uuid.uuid4())


def canvas_rep(canvas_id: str, x: int, y: int, w: int, h: int) -> dict:
    return {
        "representation": canvas_id,
        "id": canvas_id,
        "position": {"x": x, "y": y},
        "positionAbsolute": {"x": x, "y": y},
        "size": {"width": w, "height": h},
    }


def sticker_rep(canvas_id: str, x: int, y: int, w: int, h: int) -> dict:
    """Sticker representation — skill says height-only, but explicit width
    fixes ultra-narrow rendering in Devici UI."""
    return {
        "representation": canvas_id,
        "id": canvas_id,
        "position": {"x": x, "y": y},
        "positionAbsolute": {"x": x, "y": y},
        "size": {"width": w, "height": h},
    }


def node_meta(canvas_id: str, label: str, color: str | None = None) -> dict:
    m = {
        "label": label,
        "selectedBy": [],
        "representation": canvas_id,
        "fontSize": 12,
        "textStyle": {"isBold": False},
        "autoFontSize": True,
    }
    if color:
        m["color"] = color
    return m


def tz_meta(canvas_id: str, label: str, color: str) -> dict:
    return {
        "label": label,
        "selectedBy": [],
        "representation": canvas_id,
        "color": color,
        "fontSize": 14,
        "textStyle": {"isBold": True},
    }


def make_component(
    comp_id: str,
    name: str,
    comp_type: str,
    canvas_id: str,
    x: int,
    y: int,
    w: int,
    h: int,
    color: str | None = None,
    threat_ids: list[str] | None = None,
) -> dict:
    return {
        "id": comp_id,
        "name": name,
        "type": comp_type,
        "representationId": canvas_id,
        "metaData": node_meta(canvas_id, name, color),
        "representations": [canvas_rep(canvas_id, x, y, w, h)],
        "parent": {"trustZone": comp_id},  # SELF-REFERENCING
        "attributes": {},
        "threats": [{"ref": t} for t in (threat_ids or [])],
        "description": None,
        "assets": None,
    }


def make_trust_boundary(
    comp_id: str,
    name: str,
    canvas_id: str,
    x: int,
    y: int,
    w: int,
    h: int,
    color: str,
) -> dict:
    return {
        "id": comp_id,
        "name": name,
        "type": "trustBoundaryNode",
        "representationId": canvas_id,
        "metaData": tz_meta(canvas_id, name, color),
        "representations": [canvas_rep(canvas_id, x, y, w, h)],
        "parent": {"trustZone": comp_id},  # SELF-REFERENCING
        "attributes": {},
        "threats": [],
        "description": None,
        "assets": None,
    }


def make_sticker(
    comp_id: str,
    text: str,
    canvas_id: str,
    x: int,
    y: int,
    w: int,
    h: int,
) -> dict:
    return {
        "id": comp_id,
        "name": text,
        "type": "stickerNode",
        "representationId": canvas_id,
        "metaData": {
            "label": text,
            "selectedBy": [],
            "representation": canvas_id,
        },
        "representations": [sticker_rep(canvas_id, x, y, w, h)],
        "parent": {"trustZone": comp_id},  # SELF-REFERENCING
        "attributes": None,
        "threats": [],
        "description": None,
        "assets": None,
    }


def make_dataflow(
    flow_id: str,
    name: str,
    canvas_id: str,
    src_id: str,
    dst_id: str,
    src_handle: str,
    tgt_handle: str,
    hidden_label: bool = False,
    flow_type: str = "default",
    waypoints: list[dict] | None = None,
    edge_color: tuple[str, str] | None = None,
) -> dict:
    points = waypoints or []
    line_color, arrow_color = edge_color or (EDGE_COLOR, EDGE_COLOR_B)
    return {
        "id": flow_id,
        "name": name,
        "source": src_id,
        "destination": dst_id,
        "sourceHandle": src_handle,
        "targetHandle": tgt_handle,
        "type": flow_type,
        "markerEnd": {"type": "arrowclosed", "color": arrow_color},
        "metaData": {
            "color": line_color,
            "label": name,
            "fontSize": 10,
            "algorithm": "bezier-catmull-rom",
            "fontColor": "#000000",
            "textStyle": {"isBold": False},
            "markerType": "arrow",
            "hiddenLabel": hidden_label,
            "representation": canvas_id,
            "points": points,
            "autoFontSize": False,
            "floatingDisable": False,
        },
        "attributes": {},
    }


def wp(x: int, y: int) -> dict:
    """Create a waypoint dict."""
    return {"x": x, "y": y, "id": uid(), "active": True}


# ---------------------------------------------------------------------------
# Bounds checker
# ---------------------------------------------------------------------------

def check_bounds(components: list[dict], zones: dict[str, dict]) -> list[str]:
    """Return list of violations (component name + zone it's supposed to be in)."""
    errors = []
    zone_map = {
        "tz-internet": zones["internet"],
        "tz-app":      zones["app"],
        "tz-db":       zones["db"],
    }

    def in_zone(cx, cy, cw, ch, zone):
        zx, zy, zw, zh = zone["x"], zone["y"], zone["w"], zone["h"]
        return (
            cx >= zx and cy >= zy
            and cx + cw <= zx + zw
            and cy + ch <= zy + zh
        )

    for comp in components:
        if comp["type"] == "trustBoundaryNode":
            continue
        if comp["type"] == "stickerNode":
            continue
        rep = comp["representations"][0]
        pos  = rep["position"]
        size = rep["size"]
        cx, cy, cw, ch = pos["x"], pos["y"], size["width"], size["height"]
        # Find which zone this should be in by name hints
        name = comp["name"]
        if "Client" in name or "API Consumer" in name:
            target_zone = zone_map["tz-internet"]
            zone_name = "Internet"
        elif "PostgreSQL" in name:
            target_zone = zone_map["tz-db"]
            zone_name = "DB"
        else:
            target_zone = zone_map["tz-app"]
            zone_name = "App"
        if not in_zone(cx, cy, cw, ch, target_zone):
            errors.append(
                f"  ✗ {name}: ({cx},{cy},{cw}×{ch}) overflows {zone_name} zone "
                f"({target_zone['x']},{target_zone['y']},{target_zone['w']}×{target_zone['h']})"
            )
    return errors


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def build_otm(canvas_id: str) -> dict:
    # Component IDs
    tz_internet_id = "tz-internet"
    tz_app_id      = "tz-app"
    tz_db_id       = "tz-db"

    client_id   = "c-client"
    fastapi_id  = "c-fastapi"
    auth_id     = "c-auth"
    order_id    = "c-order"
    menu_id     = "c-menu"
    admin_id    = "c-admin"
    debug_id    = "c-debug"
    postgres_id = "c-postgres"

    sticker_internet_id = "s-internet"
    sticker_legend_id   = "s-legend"
    sticker_db_note_id  = "s-db-note"

    # --------------- THREATS ---------------
    t_jwt    = uid()
    t_sqli   = uid()
    t_repud  = uid()
    t_debug  = uid()
    t_dos    = uid()
    t_idor   = uid()
    t_massas = uid()
    t_brute  = uid()
    t_enum   = uid()
    t_scrape = uid()
    t_admin  = uid()

    threats = [
        {
            "id": t_jwt,
            "name": "Spoofing - JWT Algorithm Confusion Attack",
            "description": (
                "The API accepts JWTs without enforcing the algorithm (alg) header. "
                "An attacker can forge tokens using 'none' algorithm or switch to HS256 "
                "with the public key, bypassing authentication entirely."
            ),
            "categories": ["Spoofing"],
            "risk": {"likelihood": 3, "impact": 5},
        },
        {
            "id": t_sqli,
            "name": "Tampering - SQL Injection via Menu Search",
            "description": (
                "The menu search endpoint constructs SQL queries using unsanitized "
                "user input. An attacker can exfiltrate the entire database, modify "
                "data, or execute OS commands via stacked queries."
            ),
            "categories": ["Tampering"],
            "risk": {"likelihood": 4, "impact": 5},
        },
        {
            "id": t_repud,
            "name": "Repudiation - No Audit Logging for Sensitive Operations",
            "description": (
                "Admin actions (role changes, resets), order modifications, and "
                "authentication events are not logged. Attackers can perform "
                "malicious actions without forensic evidence."
            ),
            "categories": ["Repudiation"],
            "risk": {"likelihood": 2, "impact": 4},
        },
        {
            "id": t_debug,
            "name": "Information Disclosure - Debug Endpoint Exposes Internals",
            "description": (
                "The /api/v1/debug endpoint is accessible without authentication "
                "and exposes stack traces, environment variables, DB connection strings, "
                "and internal service configuration."
            ),
            "categories": ["Information Disclosure"],
            "risk": {"likelihood": 5, "impact": 5},
        },
        {
            "id": t_dos,
            "name": "Denial of Service - No Rate Limiting on API",
            "description": (
                "No rate limiting exists on any endpoint. Attackers can flood the "
                "auth endpoint with credential stuffing or exhaust DB connections "
                "via heavy menu search queries."
            ),
            "categories": ["Denial of Service"],
            "risk": {"likelihood": 3, "impact": 3},
        },
        {
            "id": t_idor,
            "name": "Elevation of Privilege - IDOR in Order Retrieval",
            "description": (
                "GET /api/v1/orders/{order_id} does not verify the requesting user "
                "owns the order. Any authenticated user can retrieve another user's "
                "order details by iterating integer IDs (BOLA/IDOR)."
            ),
            "categories": ["Elevation of Privilege"],
            "risk": {"likelihood": 4, "impact": 4},
        },
        {
            "id": t_massas,
            "name": "Tampering - Mass Assignment via Unfiltered User Input",
            "description": (
                "User registration and profile update endpoints pass raw request body "
                "directly to ORM constructors. Attackers can set privileged fields "
                "(is_admin, role) by including them in the request payload."
            ),
            "categories": ["Tampering"],
            "risk": {"likelihood": 4, "impact": 5},
        },
        {
            "id": t_brute,
            "name": "Spoofing - Brute Force via Weak Password Policy",
            "description": (
                "The authentication endpoint has no account lockout, no CAPTCHA, "
                "and accepts passwords as short as 1 character. Enables automated "
                "credential brute-force and stuffing attacks."
            ),
            "categories": ["Spoofing"],
            "risk": {"likelihood": 4, "impact": 4},
        },
        {
            "id": t_enum,
            "name": "Spoofing - Account Enumeration via Error Differentiation",
            "description": (
                "Login and password-reset endpoints return different error messages "
                "for unknown email vs. wrong password, allowing attackers to enumerate "
                "valid accounts at scale."
            ),
            "categories": ["Spoofing"],
            "risk": {"likelihood": 3, "impact": 2},
        },
        {
            "id": t_scrape,
            "name": "Denial of Service - Public Endpoint Scraping",
            "description": (
                "The menu listing endpoint is publicly accessible with no authentication "
                "or throttling. Automated scrapers can hammer the endpoint, causing "
                "elevated DB load and degraded service for legitimate users."
            ),
            "categories": ["Denial of Service"],
            "risk": {"likelihood": 2, "impact": 2},
        },
        {
            "id": t_admin,
            "name": "Elevation of Privilege - Admin Role Bypass via Insecure Direct Reference",
            "description": (
                "The admin endpoints do not re-validate the caller's role on each "
                "request. A stale or forged token with an elevated role claim can "
                "invoke privileged operations (user role changes, chef password reset)."
            ),
            "categories": ["Elevation of Privilege"],
            "risk": {"likelihood": 3, "impact": 5},
        },
    ]

    # --------------- MITIGATIONS ---------------
    m_jwt    = uid()
    m_sqli   = uid()
    m_repud  = uid()
    m_debug  = uid()
    m_dos    = uid()
    m_idor   = uid()
    m_massas = uid()
    m_brute  = uid()
    m_enum   = uid()

    mitigations = [
        {"id": m_jwt,    "name": "Enforce RS256/ES256 algorithm; reject 'none'"},
        {"id": m_sqli,   "name": "Use parameterized queries / ORM filters; input validation"},
        {"id": m_repud,  "name": "Implement structured audit log for all state-changing operations"},
        {"id": m_debug,  "name": "Remove debug endpoint in production; gate behind auth + role"},
        {"id": m_dos,    "name": "Apply rate limiting (slowapi/redis) on auth + search endpoints"},
        {"id": m_idor,   "name": "Add ownership check: verify order.user_id == current_user.id"},
        {"id": m_massas, "name": "Use explicit Pydantic schema fields; never pass **kwargs to ORM"},
        {"id": m_brute,  "name": "Account lockout after N failures; enforce password complexity"},
        {"id": m_enum,   "name": "Return uniform error message for unknown user / wrong password"},
    ]

    # Attach mitigations to threats
    for t in threats:
        t["mitigations"] = []
    threat_map = {t["id"]: t for t in threats}
    threat_map[t_jwt]["mitigations"]    = [{"ref": m_jwt}]
    threat_map[t_sqli]["mitigations"]   = [{"ref": m_sqli}]
    threat_map[t_repud]["mitigations"]  = [{"ref": m_repud}]
    threat_map[t_debug]["mitigations"]  = [{"ref": m_debug}]
    threat_map[t_dos]["mitigations"]    = [{"ref": m_dos}]
    threat_map[t_idor]["mitigations"]   = [{"ref": m_idor}]
    threat_map[t_massas]["mitigations"] = [{"ref": m_massas}]
    threat_map[t_brute]["mitigations"]  = [{"ref": m_brute}]
    threat_map[t_enum]["mitigations"]   = [{"ref": m_enum}]

    # --------------- COMPONENTS ---------------
    p = NODE_POS
    components = [
        # Trust boundaries
        make_trust_boundary(
            tz_internet_id, "Internet Zone", canvas_id,
            TZ_INTERNET["x"], TZ_INTERNET["y"], TZ_INTERNET["w"], TZ_INTERNET["h"],
            COLOR_ZONE_INTERNET,
        ),
        make_trust_boundary(
            tz_app_id, "Application Zone (Docker)", canvas_id,
            TZ_APP["x"], TZ_APP["y"], TZ_APP["w"], TZ_APP["h"],
            COLOR_ZONE_APP,
        ),
        make_trust_boundary(
            tz_db_id, "Database Zone", canvas_id,
            TZ_DB["x"], TZ_DB["y"], TZ_DB["w"], TZ_DB["h"],
            COLOR_ZONE_DB,
        ),

        # Stickers
        make_sticker(
            sticker_internet_id,
            (
                "Attack Surface:\n"
                "• No authentication on public endpoints\n"
                "• No rate limiting or CAPTCHA\n"
                "• Account enumeration via error messages\n"
                "• HTTPS not enforced in dev config"
            ),
            canvas_id,
            STICKER_INTERNET["x"], STICKER_INTERNET["y"],
            STICKER_INTERNET["w"], STICKER_INTERNET["h"],
        ),
        make_sticker(
            sticker_legend_id,
            (
                "Node Color Key:\n"
                "[C] Critical — Debug Endpoint\n"
                "[H] High — Order (IDOR/BOLA)\n"
                "[M] Medium — Auth / Menu / Admin\n"
                "[L] Low/Info — FastAPI hub / DB"
            ),
            canvas_id,
            STICKER_LEGEND["x"], STICKER_LEGEND["y"],
            STICKER_LEGEND["w"], STICKER_LEGEND["h"],
        ),
        make_sticker(
            sticker_db_note_id,
            (
                "All services query PostgreSQL\n"
                "for CRUD operations.\n"
                "Auth: user lookup + sessions\n"
                "Order: order lifecycle\n"
                "Menu: item catalog"
            ),
            canvas_id,
            STICKER_DB_NOTE["x"], STICKER_DB_NOTE["y"],
            STICKER_DB_NOTE["w"], STICKER_DB_NOTE["h"],
        ),

        # External entity
        make_component(
            client_id, "Client / API Consumer", "externalEntityNode",
            canvas_id,
            p["client"]["x"], p["client"]["y"],
            SZ_EXT["w"], SZ_EXT["h"],
            color=None,
            threat_ids=[t_enum, t_scrape],
        ),

        # Process nodes
        make_component(
            fastapi_id, "FastAPI REST API", "processNode",
            canvas_id,
            p["fastapi"]["x"], p["fastapi"]["y"],
            SZ_HUB["w"], SZ_HUB["h"],
            COLOR_FASTAPI,
            threat_ids=[t_dos, t_massas],
        ),
        make_component(
            auth_id, "Auth Service", "processNode",
            canvas_id,
            p["auth"]["x"], p["auth"]["y"],
            SZ_SVC["w"], SZ_SVC["h"],
            COLOR_AUTH,
            threat_ids=[t_jwt, t_brute],
        ),
        make_component(
            order_id, "Order Service", "processNode",
            canvas_id,
            p["order"]["x"], p["order"]["y"],
            SZ_SVC["w"], SZ_SVC["h"],
            COLOR_ORDER,
            threat_ids=[t_idor, t_repud],
        ),
        make_component(
            menu_id, "Menu Service", "processNode",
            canvas_id,
            p["menu"]["x"], p["menu"]["y"],
            SZ_SVC["w"], SZ_SVC["h"],
            COLOR_MENU,
            threat_ids=[t_sqli],
        ),
        make_component(
            admin_id, "Admin Service", "processNode",
            canvas_id,
            p["admin"]["x"], p["admin"]["y"],
            SZ_SVC["w"], SZ_SVC["h"],
            COLOR_ADMIN,
            threat_ids=[t_admin],
        ),
        make_component(
            debug_id, "Debug Endpoint", "processNode",
            canvas_id,
            p["debug"]["x"], p["debug"]["y"],
            SZ_SVC["w"], SZ_SVC["h"],
            COLOR_DEBUG,
            threat_ids=[t_debug],
        ),

        # Datastore
        make_component(
            postgres_id, "PostgreSQL Database", "datastoreNode",
            canvas_id,
            p["postgres"]["x"], p["postgres"]["y"],
            SZ_STORE["w"], SZ_STORE["h"],
            COLOR_POSTGRES,
        ),
    ]

    # --------------- DATAFLOWS ---------------
    # Waypoint x just inside right edge of App Zone before entering DB Zone
    WP_X = 1100

    dataflows = [
        # 1. Client → FastAPI (blue — inbound)
        make_dataflow(
            uid(), "API Request →", canvas_id,
            client_id, fastapi_id,
            "sourceRight", "targetLeft",
            edge_color=EDGE_INBOUND,
        ),
        # 2. FastAPI → Auth (purple — matches Auth node)
        make_dataflow(
            uid(), "→ Authenticate / Register", canvas_id,
            fastapi_id, auth_id,
            "sourceLeft", "targetRight",
            edge_color=EDGE_TO_AUTH,
        ),
        # 3. FastAPI → Order (red — matches Order node; label hidden)
        make_dataflow(
            uid(), "→ Order Request", canvas_id,
            fastapi_id, order_id,
            "sourceLeft", "targetRight",
            hidden_label=True,
            edge_color=EDGE_TO_ORDER,
        ),
        # 4. FastAPI → Menu (orange — matches Menu node; label hidden)
        make_dataflow(
            uid(), "→ Menu Request", canvas_id,
            fastapi_id, menu_id,
            "sourceLeft", "targetRight",
            hidden_label=True,
            edge_color=EDGE_TO_MENU,
        ),
        # 5. FastAPI → Admin (amber — matches Admin node)
        make_dataflow(
            uid(), "→ Admin Request", canvas_id,
            fastapi_id, admin_id,
            "sourceRight", "targetLeft",
            edge_color=EDGE_TO_ADMIN,
        ),
        # 6. FastAPI → Debug (dark red — matches Debug node)
        make_dataflow(
            uid(), "→ Debug Request", canvas_id,
            fastapi_id, debug_id,
            "sourceRight", "targetLeft",
            edge_color=EDGE_TO_DEBUG,
        ),
        # 7. FastAPI → Postgres (teal — DB flow; routed via sourceTop)
        make_dataflow(
            uid(), "→ DB Query", canvas_id,
            fastapi_id, postgres_id,
            "sourceTop", "targetTop",
            hidden_label=False,
            waypoints=[wp(725, 25), wp(1310, 25)],
            edge_color=EDGE_TO_DB,
        ),
        # 8. Auth → Postgres (purple faded; staggered waypoint y=245)
        make_dataflow(
            uid(), "User Lookup", canvas_id,
            auth_id, postgres_id,
            "sourceRight", "targetLeft",
            hidden_label=True,
            waypoints=[wp(WP_X, 245)],
            edge_color=EDGE_AUTH_DB,
        ),
        # 9. Order → Postgres (red faded; staggered waypoint y=355)
        make_dataflow(
            uid(), "Order CRUD", canvas_id,
            order_id, postgres_id,
            "sourceRight", "targetLeft",
            hidden_label=True,
            waypoints=[wp(WP_X, 355)],
            edge_color=EDGE_ORDER_DB,
        ),
        # 10. Menu → Postgres (orange faded; staggered waypoint y=470)
        make_dataflow(
            uid(), "Menu CRUD", canvas_id,
            menu_id, postgres_id,
            "sourceRight", "targetLeft",
            hidden_label=True,
            waypoints=[wp(WP_X, 470)],
            edge_color=EDGE_MENU_DB,
        ),
    ]

    # --------------- CANVAS REPRESENTATION ---------------
    representations = [
        {
            "type": "diagram",
            "id": canvas_id,
            "name": "DVRAG Architecture Diagram",
            "attributes": {
                "width": CANVAS_W,
                "height": CANVAS_H,
            },
        }
    ]

    return {
        "otmVersion": "0.2.0",
        "project": {
            "name": "DVRAG STRIDE (Mar 2026) v8",
            "id": uid(),
            "description": (
                "STRIDE threat model for the Damn Vulnerable RESTaurant API Game. "
                "Generated by docs/threat-model/generate_otm.py. "
                "v8: color-coded edges matching destination nodes, "
                "faded service→DB flows, matching arrowhead colors."
            ),
            "owner": "Security Team",
            "ownerContact": "security@demo.local",
            "attributes": {
                "ref": "dvrag-stride-v8",
            },
        },
        "representations": representations,
        "trustZones": [],
        "components": components,
        "dataflows": dataflows,
        "threats": threats,
        "mitigations": mitigations,
    }


# ---------------------------------------------------------------------------
# Bounds validation
# ---------------------------------------------------------------------------

def validate_bounds(otm: dict) -> bool:
    zones = {
        "internet": TZ_INTERNET,
        "app":      TZ_APP,
        "db":       TZ_DB,
    }
    errors = check_bounds(otm["components"], zones)
    if errors:
        print("❌ Bounds check FAILED:")
        for e in errors:
            print(e)
        return False
    print(f"✅ Bounds check passed — all {len(otm['components'])} components verified")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate DVRAG Devici OTM v8")
    parser.add_argument(
        "--output", default="/tmp/otm_v8.json",
        help="Output path for the OTM JSON (default: /tmp/otm_v8.json)",
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Validate JSON only, do not write output file",
    )
    args = parser.parse_args()

    canvas_id = str(uuid.uuid4())
    print(f"Canvas ID: {canvas_id}")

    otm = build_otm(canvas_id)

    # Validate JSON serialisability
    try:
        json_str = json.dumps(otm, indent=2)
    except Exception as e:
        print(f"❌ JSON serialization error: {e}")
        sys.exit(1)

    # Validate bounds
    if not validate_bounds(otm):
        sys.exit(1)

    if args.validate_only:
        print(f"✅ Validate-only mode — OTM is {len(json_str):,} bytes, not written to disk")
        return

    with open(args.output, "w") as f:
        f.write(json_str)

    size_kb = len(json_str) / 1024
    print(f"✅ OTM written to {args.output} ({size_kb:.1f} KB)")
    if size_kb > 30:
        print("ℹ️  Payload >30KB — use otm_file_path= in threat_model_import_otm (not otm_content)")
    print(f"   Components : {len(otm['components'])}")
    print(f"   Dataflows  : {len(otm['dataflows'])}")
    print(f"   Threats    : {len(otm['threats'])}")
    print(f"   Mitigations: {len(otm['mitigations'])}")


if __name__ == "__main__":
    main()
