# SDE MCP Live Demo — Opening Segment (`setup-security-plan-from-repo`, Steps 0–1.5)

**Purpose:** Show a live audience the real agentic flow — MCP connection check, then genuine
interactive questions for project/BU/application — then stop, before the long-running
survey/classification/library-lookup work. The full step-by-step breakdown of all three SDE
prompts (`setup-security-plan-from-repo`, `create-security-plan-from-specs`, `apply-security-fixes`)
is covered separately in slides/notes — this file is NOT that summary.

**When to use:** Read this file instead of fetching/following the full skill contract when running
this opening segment of the demo. It intentionally executes only Steps 0–1.5 of
`setup-security-plan-from-repo` and then halts. To run the real, complete workflow later, fetch
the actual prompt via `prompts op=get prompt=setup-security-plan-from-repo` and follow it in
full — this opening segment is not a substitute for that contract on a real engagement.

**Important — fresh data only:** A prior full run against this repo already exists in SD Elements
(project 770, per `EXECUTIVE_SUMMARY.md`). Ignore it. This segment creates a **new** project from
a clean survey — do not reuse or reference project 770's answers/countermeasures. Delete the
project this segment creates once the live portion of the demo has run (it's a throwaway used
only to show the interactive flow).

---

## Step 0: Verify MCP Connection

Call `test_connection` (or `business_unit` `op: "list"`). On success:

```
[CHECKPOINT] MCP connection successful
```

## Step 1: Gather User Inputs (LIVE — this is the demo moment)

Ask ONE AT A TIME via `ask_question` / AskUserQuestion, wait for a real answer each time, and
echo back the selection before moving on:

1. **Repository** — "Which repository would you like to harden?" Offer the current repo path plus
   a manual-entry option. Store `repository_path`.
2. **Project mode** — "SD Elements project setup:" → `create_new` / `use_existing`. For this
   segment, steer toward `create_new` (see fresh-data note above).
3. **Business Unit** (if create_new) — call `business_unit op=list`, ask the user to pick one or
   create a new one. Store `business_unit_id`.
4. **Application** — call `application op=list` for that BU, ask the user to pick or create new
   (suggest the repo name as a default, but let them confirm/edit). Store `application_id`.
5. **Project name** — suggest the repo name as default; ask the user to confirm or enter a
   different name. Check for duplicates via `project op=list`; if a duplicate exists, offer
   use-existing / name-with-date-suffix / enter-custom. Store `project_name`.
   **Naming rule — do NOT expose internal-only wording:** the project name is client-visible
   in SD Elements, so never include "teaser," "demo-only," or similar internal labels in it.
   Suggest a clean, professional name instead (e.g. `{Application} Security Assessment -
   {date}`). Track internally/verbally that this run is the abbreviated opening segment — do
   not put that label in any client-facing SDE artifact (project name, description, tags).
6. **Risk policy** — call `library_search query=all types=[risk_policies]` and `business_unit
   op=get` (for the BU's default policy); offer the BU default + other policies + custom ID
   + skip. Store `risk_policy_id` (or `SKIPPED`).

## Step 1.5: Create the Project

Call `project op=create` with `application_id`, `name` (project_name), and `risk_policy`
(if set). Then validate by calling `project op=get` on the returned id and confirming the name
matches.

Output:
```
[CHECKPOINT] Inputs: repo={repository_path}, project={project_name} (ID: {project_id}), risk_policy={risk_policy_id or SKIPPED}
[CHECKPOINT] Project ID: {project_id} (validated via get_project name-match)
```

## STOP HERE — Opening Segment Complete

Tell the audience the real skill would continue:

`1.7 (security branch) → 1.8 (archive AI config) → 2 (survey: 100+ questions, code-evidence-driven)
→ 3–4 (countermeasure retrieval + classification) → 4.5–4.6 (PROCESS notes + library-skill lookup)
→ 5–9 (AGENTS.md + per-countermeasure SKILL.md generation)`, then the second and third prompts
(`create-security-plan-from-specs`, `apply-security-fixes`) apply and verify the actual fixes.

Do not continue further in this session — switch to slides/notes for the rest.

## Cleanup After the Live Segment

The project created in Step 1.5 is throwaway — it exists only to demonstrate the interactive
flow. Once the live portion of the demo wraps, delete it: `api_request DELETE
/api/v2/projects/{project_id}/` (confirm with the presenter first — this is irreversible).
Do not leave demo-run projects accumulating in SD Elements.
