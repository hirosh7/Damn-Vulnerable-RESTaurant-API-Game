---
name: configure-survey-with-traceability
description: >
  Configures the SD Elements project survey and generates security specs, then
  ensures every answered survey question (including auto-answered questions) has
  a note for full traceability. Use this instead of the built-in
  configure-survey-and-generate-specs skill when audit trails and traceability
  notes are required.
---

# Configure Survey with Full Traceability

This skill extends the built-in `configure-survey-and-generate-specs` MCP skill by adding a
mandatory post-survey step that adds notes to every answered question — including those
answered automatically — so that reviewers and auditors can understand the basis for each
answer.

## Step 1 — Run the built-in skill

Invoke `/user-sdelements-gitlab/configure-survey-and-generate-specs` and follow it completely:
gather project context, answer all survey questions, and confirm that specs have been generated.
Do not proceed to Step 2 until the spec generation step is confirmed complete.

## Step 2 — Retrieve all survey questions

Use the `user-sdelements-gitlab` MCP server to retrieve every survey question for the project:

```
survey_questions op=list project_id=<id> page_size=100
```

Also retrieve the current answers:

```
survey_answers op=list project_id=<id> page_size=100
```

Get the project ID from `.sde-handoff.json` before it is deleted, or from `AGENTS.md`.

## Step 3 — Add a traceability note to every answered question

For **every question that has an answer** — including questions answered automatically by the
built-in skill, pre-populated default answers, and any inherited answers — add a note that
explains the basis for the answer.

### Mandatory note contents

Each note MUST include:

1. **Answer value recorded** — the exact answer text or option selected (e.g. `Yes`, `No`, `N/A`, `Custom value`).
2. **Basis for the answer** — why this answer was chosen:
   - Auto-answered: state which rule or system default triggered it (e.g. `Auto-answered: SD Elements default for web applications`, `Auto-answered: inferred from technology tag "Python/FastAPI"`).
   - Manually answered: state the rationale (e.g. `Based on code review: JWT tokens issued from /auth/token endpoint`).
   - Inherited: state the source (e.g. `Inherited from parent project survey`).
3. **Evidence or file reference** (if applicable) — the specific file, config key, or external document that supports the answer (e.g. `See app/apis/auth/utils/jwt_auth.py`, `See docker-compose.yml line 12`).
4. **Reviewer** — note that the answer was set by the AI agent in this session and the branch/date context (e.g. `Set by agent on branch demo-test, 2026-03-17`).

### Note format

```
Answer: <value>
Basis: <auto-answered / manually answered / inherited> — <reason>
Evidence: <file or config reference, or "None">
Reviewer: AI agent — branch <branch>, <date>
```

### Auto-answered questions

If a question was answered automatically by the built-in skill without explicit human review,
the note MUST also include:

```
⚠ Auto-answered — human review recommended before finalizing survey.
```

This flags questions for a human to verify without blocking progress.

## Step 4 — Verify coverage

After adding notes, call `survey_answers op=list` again and confirm:

- Every answered question has a non-empty note.
- No answered question is missing a basis or evidence field.
- Auto-answered questions are flagged with the `⚠ Auto-answered` marker.

Report a final summary:
- Total questions in survey
- Total answered
- Total with notes added this session
- Count of auto-answered questions flagged for human review

## Step 5 — Commit traceability artifacts (optional)

If the project uses an `AGENTS.md` or similar tracking file, append a survey traceability
summary block recording:

```markdown
## Survey Traceability — <date>

- Project ID: <id>
- Branch: <branch>
- Total questions answered: <n>
- Auto-answered (flagged): <n>
- Notes added: <n>
- Spec generation: confirmed
```

## Notes

- Add notes in parallel batches of 4–5 to reduce total time.
- Do not skip questions that were answered with default values — defaults still require a
  documented rationale.
- Do not modify any answers that were already set; this step is note-only.
- If a question is unanswered/skipped, no note is required (but record its ID in the
  traceability summary as "unanswered").
