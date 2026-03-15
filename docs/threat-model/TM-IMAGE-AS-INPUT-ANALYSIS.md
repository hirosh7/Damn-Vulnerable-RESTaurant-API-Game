# TM Diagram Image as Act 1 Input — Analysis

**Date:** March 15, 2026  
**Context:** Can a threat model diagram image substitute for a text-based architectural description to kick off Act 1 of the Devici + SDE DevSecOps pipeline?

---

## Summary

Yes — with important caveats. A vision-capable AI model can read the diagram image and derive enough information to construct an architectural description comparable to a hand-written one. The image is a valid Act 1 entry point, but it produces shallower STRIDE threats than a purpose-written text description.

---

## What Can Be Extracted from the Image

| Element | Extractable? | Notes |
|---|---|---|
| Component names | ✅ Yes | FastAPI REST API, Auth Service, Order Service, Menu Service, Admin Service, Debug Endpoint, PostgreSQL |
| Trust boundaries | ✅ Yes | Internet Zone, Application Zone (Docker), Database Zone |
| Data flows | ✅ Yes | API Request, Authenticate/Register, Admin Request, DB Query, Debug Request |
| Risk levels | ✅ Yes | Via node color coding — Critical (Debug Endpoint), High (Order Service), Medium (Auth/Menu/Admin) |
| Attack surface | ✅ Yes | From Internet Zone sticker: no auth on public endpoints, no rate limiting, account enumeration via error messages, HTTPS not enforced in dev config |
| DB context | ✅ Yes | From DB Zone sticker: Auth = user lookup + sessions, Order = order lifecycle, Menu = item catalog |

This is sufficient to write a text architectural description covering components, roles, trust zones, data flows, and high-level threats — the core inputs to Act 1.

---

## What the Image Is Missing vs. a Text Description

| Missing Element | Why It Matters for the Pipeline |
|---|---|
| Stack/tech specifics (FastAPI, SQLAlchemy, Python 3.10, JWT HS256) | SDE survey answers depend on these — e.g. "PostgreSQL" vs generic DB, "JWT Bearer" auth method |
| Specific vulnerability details (algorithm confusion, BOLA/IDOR mechanics, SQL injection location) | STRIDE threat descriptions in the generated OTM will be less precise |
| Explicit STRIDE category mapping | Act 1 OTM generation needs `"Spoofing - ..."`, `"Tampering - ..."` prefixes on threats |
| CVE-relevant library names (python-jose, passlib, slowapi) | Act 4 CVE dependency audit is blind without declared library names |

---

## Impact on Each Act

| Act | Impact |
|---|---|
| **Act 1** (Devici TM from description) | Image is sufficient for correct topology — nodes, zones, flows, color coding, stickers. Threat descriptions will be shallower. |
| **Act 2** (Code Genius enrichment) | Code scan compensates for what the image couldn't provide — tech stack, library names, and code-level vulnerability specifics are discovered here. |
| **Act 3** (SDE project + survey) | Slightly reduced survey evidence quality; comments will be less code-specific. Act 2 enrichment partially closes this gap. |
| **Act 4** (Countermeasure implementation) | Requires the codebase regardless — the image alone is never sufficient for Act 4. |

---

## Practical Conclusion

The image **can replace** a text architectural description for Act 1 topology construction. The gap is in **threat depth**, not structure. For the manual-workflow scenario — architect produces a diagram, developer derives requirements and implements code — the image is a reasonable entry point. The Act 2 Code Genius scan is designed to enrich the design-time model with code-derived detail, which is exactly the compensation needed for the information gaps in an image-only input.

**Recommended approach if starting from an image:**
1. Use the image as the primary source for Act 1 (components, zones, flows, attack surface)
2. Supplement with any known stack/library details if available (even informally)
3. Let Act 2 Code Genius fill in the code-level gaps before Act 3 survey completion
