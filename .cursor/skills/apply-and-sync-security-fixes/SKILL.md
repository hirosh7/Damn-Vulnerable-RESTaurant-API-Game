---
name: apply-and-sync-security-fixes
description: >
  Applies all security hardening fixes from generated specs (AGENTS.md + skill guidance),
  then syncs countermeasure statuses to SD Elements. Use this instead of the built-in
  apply-fixes-from-security-specs skill when you want SD Elements status tracking included.
---

# Apply Security Fixes and Sync to SD Elements

This skill extends the built-in `apply-fixes-from-security-specs` MCP skill by adding a
mandatory SD Elements status sync step after all code changes are committed.

## Step 1 — Run the built-in skill

Invoke `/user-sdelements-gitlab/apply-fixes-from-security-specs` and follow it completely:
confirm the handoff, apply all countermeasures, update local skill files, clean up generated
artifacts, and commit all changes to the security branch. Do not proceed to Step 2 until the
git commit is confirmed.

## Step 2 — Retrieve project countermeasures from SD Elements

Use the `user-sdelements-gitlab` MCP server to list all countermeasures for the project:

```
project_countermeasures op=list project_id=<id> page_size=100
```

Get the project ID from `.sde-handoff.json` before it is deleted, or from `AGENTS.md`.

## Step 3 — Update each countermeasure status

For every countermeasure, set the status based on **actual implementation state** — not
documentation state:

### Complete (`DONE`)

Mark as Complete only if one of the following is true:
- Code was written and committed addressing the countermeasure directly
- A config file (Dockerfile, docker-compose.yml, GitHub Actions workflow, etc.) was modified
- A new file was created that directly implements the control

Include a note with: what was changed, which file(s), and the branch name.

### Incomplete (`TODO`)

Mark as Incomplete if the countermeasure requires any action that was NOT taken in the
codebase, including:
- Organizational process adoption (code review policies, incident response plans)
- Legal or compliance team decisions (consent forms, data registers, DPA agreements)
- GitHub admin settings that must be configured in the GitHub UI (branch protection, MFA
  enforcement, secret scanning, artifact signing, package registry controls)
- UI features not yet built (consent management pages, DSAR interfaces)
- Recurring operational tasks (periodic security assessments, audits)

Include a note starting with `PENDING:` that specifies:
1. What action is required
2. Who is responsible (GitHub admin / Privacy Officer / Legal team / Development team)
3. Any prerequisite steps

### Typical split

| Category | Expected status |
|---|---|
| CODE_FIX — applied to source code | Complete |
| INFRA — applied to config files in repo | Complete |
| INFRA — GitHub org/repo admin settings | Incomplete |
| PROCESS — organizational or team procedures | Incomplete |
| PROCESS — legal/compliance decisions | Incomplete |

## Step 4 — Verify the final count

After all updates, call `project_countermeasures op=list` again and confirm:
- Complete count matches the number of code/config fixes applied
- Incomplete count matches the number of process/external items
- No countermeasure was left at its prior status without a note

## Notes

- Update countermeasures in parallel batches of 4–5 to reduce total time.
- Each note should be specific enough for a human to act on without needing to read the
  code — name the file, the setting, or the team responsible.
- Do not mark anything Complete solely because guidance was written in a skill.md file.
  Documented ≠ Implemented.
