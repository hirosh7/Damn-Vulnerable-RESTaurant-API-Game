# DevSecOps Pipeline — Demo Guide

Quick reference for running and narrating the Devici + SDE pipeline demo.

---

## How to Invoke

| What you want | Say this |
|---|---|
| Full pipeline (all 4 acts) | `"run the devici-sde pipeline for DVRAG"` |
| Design + Code only (Acts 1–2) | `"run acts 1 and 2 only"` |
| Skip to security requirements (Act 3+) using existing OTM | `"bring your own OTM — run from Act 3"` |
| Skip to Act 3 using a specific file | `"bring your own diagram — use docs/threat-model/generate_otm.py"` |

---

## The Four Acts

### Act 1 — Design Phase *(~2–3 min)*
> *"Architects think in diagrams."*

The agent takes a plain-English architecture description and builds a STRIDE threat model in Devici — trust boundary zones, color-coded risk nodes, STRIDE-annotated components, and sticky note advisories.

**Check after:** Canvas loads in Devici with 3 zones, colored nodes, edges with `→` labels, and 3 annotation stickers.

---

### Act 2 — Code Phase *(~3–4 min)*
> *"The code tells a different story."*

The agent scans the actual codebase using Code Genius and creates a REPOSITORY-type threat model showing the design vs. code delta.

**Check after:** Pipeline view in Devici shows green (new threats found in code), orange (changed), white (unchanged).

---

### Act 3 — Security Phase *(~2–3 min)*
> *"Your team used to spend two days on this."*

The agent reads the threat model, creates an SDE project, auto-fills the survey in dependency order using `mutateByText`, commits it, and adds an evidence-backed comment to every answered question.

**Check after:** SDE project published, requirements count shown, every question has a comment.

> **Key demo moment:** `mutateByText` — every answer filled from the architecture description at similarity = 1.0. No clicking.

---

### Act 4 — Remediation Phase *(~2–3 min)*  *(read the room — skip if audience isn't ready)*
> *"Close the loop."*

The agent implements the highest-priority SDE countermeasures in the codebase and updates each countermeasure status with a rationale note.

**Check after:** Code changes made in repo, countermeasure statuses updated to Complete/N/A/Incomplete.

---

## Key Metrics to Quote

| Before | After |
|---|---|
| Threat model: 2-hour whiteboard | 30 seconds |
| Survey fill: 2 days | < 3 minutes |
| Requirements generated | 79 (DVRAG) |
| Survey answers | 69 — all exact match |
| Questions with evidence comments | 34 / 34 |

---

## Known Limitations (be upfront)

- SVG arrowheads don't render on OTM-imported Devici edges — direction shown via `→` in label text instead
- Act 4 is optional — flag it as "fully agentic" and let the audience decide if they're ready for that step
- `getProjectSurvey` (not `getDraft`) is the authoritative answer list — the agent handles this internally

---

## DVRAG Known IDs

| Resource | Value |
|---|---|
| Devici Demo Collection | `e39684a2-e0d1-4ebf-9e9b-e4eafad6892e` |
| SDE Application ID | 568 |
| OTM generator | `docs/threat-model/generate_otm.py` |
| SDE project URL pattern | `https://sde-ent-onyxdrift.sdelab.net/bunits/corporate-security-bu/secapp-assessment-application/<slug>/` |
