# DevSecOps Pipeline — Overview

An agentic four-act pipeline that takes a system architecture from description to threat model, security requirements, and hardened code — fully automated.

---

## The Four Acts

### Act 1 — Design Phase
> *"Architects think in diagrams."*

The agent takes a plain-English architecture description and builds a STRIDE threat model in Devici — trust boundary zones, color-coded risk nodes, STRIDE-annotated components, and sticky note advisories on high-risk areas.

---

### Act 2 — Code Phase
> *"The code tells a different story."*

The agent scans the actual codebase and creates an enriched threat model showing the delta between the original design and what was implemented. New threats found in code are highlighted; components that drifted from the design are flagged.

---

### Act 3 — Security Phase
> *"Your team used to spend two days on this."*

The agent reads the threat model, creates a project in SD Elements, and auto-fills the security survey directly from the architecture and threat data. Every answered question receives an evidence-backed comment citing the specific threat, component, or code pattern that drove it.

---

### Act 4 — Remediation Phase
> *"Close the loop."*

The agent implements the highest-priority security countermeasures in the codebase and updates each countermeasure status with a rationale note — connecting every code change back to a specific security requirement.

---

## Key Results (DVRAG)

| Metric | Value |
|---|---|
| Threat model creation | Seconds vs. 2-hour whiteboard session |
| Security survey completion | Minutes vs. 2 days manual effort |
| Requirements generated | 79 |
| Survey answers matched | 69 — all exact match to SDE taxonomy |
| Questions with evidence comments | 34 / 34 (100%) |

---

## Known Limitations

- Arrowhead markers do not render on imported diagram edges in Devici; data flow direction is indicated via labels instead
- Act 4 (automated code remediation) is optional and can be scoped based on team readiness
