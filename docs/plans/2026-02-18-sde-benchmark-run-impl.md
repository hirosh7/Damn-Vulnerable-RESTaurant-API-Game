# sde-benchmark-run Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a Cursor skill (`sde-benchmark-run`) that orchestrates two-phase SDE evaluation runs, tracks timing and estimated token/cost data, and generates an enriched comparison report in Obsidian.

**Architecture:** A single SKILL.md file at `~/.cursor/skills/sde-benchmark-run/SKILL.md`. The skill uses a JSON run-file on disk to persist state between Phase 1 and Phase 2 invocations. On Phase 2 completion it writes a Markdown report to the user's Obsidian vault via the `user-MCP_DOCKER` MCP server. All token counts are estimated via character-count heuristics.

**Tech Stack:** Markdown skill file, JSON run-files, Obsidian MCP (`user-MCP_DOCKER`), SDE MCP (`user-sdelements-gitlab`), shell commands for timestamps and file I/O.

**Design Doc:** `docs/plans/2026-02-18-sde-benchmark-run-design.md`

---

## Task 1: Create Skill Directory and Scaffold

**Files:**
- Create: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Create the directory**

```bash
mkdir -p ~/.cursor/skills/sde-benchmark-run
```

**Step 2: Write the initial SKILL.md scaffold** with YAML frontmatter, purpose, and section headings (no content yet):

```markdown
---
name: sde-benchmark-run
description: >
  Orchestrate and measure a two-phase SDE evaluation run (project modeling +
  countermeasure implementation). Tracks wall-clock timing, estimates token
  usage and cost, captures SDE project metrics, and writes an enriched
  comparison report to Obsidian. Use when benchmarking model quality, speed,
  or cost across SDE prompt runs.
---

# SDE Benchmark Run

## Purpose
## When to Use
## How to Use
### Phase 1 — Project Creation
### Phase 2 — Countermeasure Implementation
### Compare Mode
## Token Estimation
## Pricing Lookup Table
## Run-File Schema
## Report Format
## MCP Tools Used
## Common Pitfalls
```

**Step 3: Verify the file exists**

```bash
ls -la ~/.cursor/skills/sde-benchmark-run/SKILL.md
```
Expected: file exists, non-zero size

**Step 4: Commit**

```bash
cd ~/.cursor
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: scaffold sde-benchmark-run skill"
```

---

## Task 2: Write Purpose, When to Use, and Startup Behavior

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Fill in the Purpose and When to Use sections:**

```markdown
## Purpose
Compare SDE project modeling runs across models, prompts, and sessions by
tracking: wall-clock time per phase, estimated input/output tokens, estimated
cost (USD), model used, prompts used, SDE MCP server, and all standard SDE
project metrics (survey answers, countermeasure status).

## When to Use
- Benchmarking a new prompt version against a previous run
- Comparing model quality (e.g. claude-4-6-sonnet vs gpt-5) on the same task
- Tracking cost-efficiency across runs
- Generating a reproducible record of an SDE modeling session
```

**Step 2: Write the startup detection logic** — the first thing the skill does when invoked is detect context:

```markdown
## Startup: Detecting Invocation Mode

When this skill is invoked, first determine which mode to enter:

1. If user says "compare" → enter **Compare Mode** (see section below)
2. If a run-file exists in `~/projects/docs/demo-analysis/runs/` with `"status": "phase1_complete"` → offer to continue with **Phase 2**
3. Otherwise → start a new run with **Phase 1**

To check for in-progress run-files:
```bash
ls ~/projects/docs/demo-analysis/runs/*.json 2>/dev/null | head -20
```
Read each file and check the `"status"` field. A status of `"phase1_complete"` means Phase 2 is pending.
```

**Step 3: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: add purpose, when-to-use, startup detection"
```

---

## Task 3: Write Phase 1 — Project Creation Workflow

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Write the Phase 1 section.** This must cover: prompt selection, gathering run metadata, timing, execution, token estimation, run-file write.

```markdown
## Phase 1 — Project Creation

### Step 1: Gather Run Metadata

Ask the user the following questions (prompt for each if not already known from context):

**a) Which project creation prompt?**
List available prompts:
```bash
ls ~/projects/Damn-Vulnerable-RESTaurant-API-Game/prompts/model-*.txt 2>/dev/null
ls ~/projects/*/prompts/model-*.txt 2>/dev/null
```
Display the list and ask: "Which project creation prompt should I use? (enter filename or number)"

**b) Which model are you using?**
If the current Cursor model is determinable from context, confirm it. Otherwise ask:
"Which model are you using for this run? (e.g. claude-4-6-sonnet, gpt-5, auto)"

**c) Which SDE MCP server?**
Default: `user-sdelements-gitlab`
Ask only if default is not appropriate: "Which SDE MCP server should I use? (default: user-sdelements-gitlab)"

**d) Create the runs directory if needed:**
```bash
mkdir -p ~/projects/docs/demo-analysis/runs
```

### Step 2: Record Phase 1 Start Time

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```
Store this as `phase1.start_time`. Also note the human-readable form for display.

### Step 3: Execute Phase 1 Prompt

Read the selected prompt file:
```bash
cat <prompt_file_path>
```

Inject the prompt content into the conversation and execute it fully:
- Create a new SDE project
- Answer all survey questions with comments
- Publish the survey
- Do NOT proceed to Phase 2 yet

### Step 4: Record Phase 1 End Time and Calculate Duration

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```
`phase1.duration_seconds = end_time - start_time`

### Step 5: Capture Phase 1 SDE Data

After the prompt completes, record:
- `project_id` — the ID of the newly created SDE project
- `project_name` — the project name as returned by the SDE API

### Step 6: Estimate Phase 1 Token Usage

See **Token Estimation** section for formulas. Calculate:
- `estimated_input_tokens`
- `estimated_output_tokens`
- `estimated_cost_usd` (using Pricing Lookup Table)

### Step 7: Write Run-File

Generate a run ID: `benchmark-run-YYYY-MM-DD-HH-MM` (using phase1 start time)

Write JSON to `~/projects/docs/demo-analysis/runs/<run_id>.json`:
```json
{
  "run_id": "<run_id>",
  "status": "phase1_complete",
  "phase1": {
    "prompt_file": "<path>",
    "prompt_name": "<filename without extension>",
    "model": "<model>",
    "sde_mcp_server": "<server>",
    "project_id": <id>,
    "project_name": "<name>",
    "start_time": "<ISO>",
    "end_time": "<ISO>",
    "duration_seconds": <n>,
    "estimated_input_tokens": <n>,
    "estimated_output_tokens": <n>,
    "estimated_cost_usd": <n>
  }
}
```

### Step 8: Notify User

Display:
```
✅ Phase 1 complete!
   Run ID:    <run_id>
   Project:   <project_name> (ID: <project_id>)
   Duration:  <HH>h <MM>m <SS>s
   Est. cost: ~$<X.XX>
   Run-file:  ~/projects/docs/demo-analysis/runs/<run_id>.json

▶ To continue: invoke sde-benchmark-run again and I will detect Phase 2 is pending.
```
```

**Step 2: Verify the section is complete and well-formed**

Read the file and check it renders cleanly as Markdown (no broken code fences, etc.)

**Step 3: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: write Phase 1 workflow section"
```

---

## Task 4: Write Phase 2 — Countermeasure Implementation Workflow

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Write the Phase 2 section.** Must cover: run-file detection, prompt selection, timing, execution, SDE metric collection, token estimation, run-file update.

```markdown
## Phase 2 — Countermeasure Implementation

### Step 1: Select In-Progress Run

List run-files with status `phase1_complete`:
```bash
ls ~/projects/docs/demo-analysis/runs/*.json
```
Read each and display runs with `phase1_complete` status:
```
In-progress runs found:
  [1] benchmark-run-2026-02-18-14-30  (Project: <name>, Phase 1: 28m 42s)
  [2] benchmark-run-2026-02-18-09-10  (Project: <name>, Phase 1: 31m 15s)
Which run should I continue? (enter number)
```

### Step 2: Select Countermeasure Prompt

List available prompts:
```bash
ls ~/projects/Damn-Vulnerable-RESTaurant-API-Game/prompts/implement-*.txt 2>/dev/null
ls ~/projects/*/prompts/implement-*.txt 2>/dev/null
```
Ask: "Which countermeasure prompt should I use? (enter filename or number)"

### Step 3: Confirm Model

Ask user to confirm or change the model for Phase 2. It may differ from Phase 1.

### Step 4: Record Phase 2 Start Time

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

### Step 5: Execute Phase 2 Prompt

Read the selected prompt file:
```bash
cat <prompt_file_path>
```

Inject and execute fully:
- Fetch risk-relevant countermeasures from the Phase 1 project
- Implement countermeasures in the codebase
- Update every countermeasure status (complete / not applicable / incomplete)
- Add a note to every countermeasure

### Step 6: Record Phase 2 End Time and Duration

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

### Step 7: Fetch Final SDE Project Metrics

Using the SDE MCP server, collect the following for the Phase 1 project:

```javascript
// Survey answers and comments
const survey = callMcpTool("project_survey", { op: "getAnswersForProject", project_id: PROJECT_ID });
const comments = callMcpTool("project_survey", { op: "listComments", project_id: PROJECT_ID });
// Countermeasures
const cms = callMcpTool("project_countermeasures", { op: "list", project_id: PROJECT_ID });
```

Calculate (following sde-project-comparison skill rules exactly):
- `total_survey_answers` — count of answer IDs
- `questions_answered` — count of unique question IDs from answers
- `questions_with_comments` — count of unique question IDs from `listComments`
- `questions_without_comments` — questions_answered - questions_with_comments
- `comment_coverage_pct` — (questions_with_comments / questions_answered) × 100
- `total_countermeasures` — total CM count
- `complete_done` — count where `"meaning": "DONE"`
- `incomplete_todo` — count where `"meaning": "TODO"`
- `not_applicable_na` — count where `"meaning": "NA"`
- `cms_with_notes` — count where `note_count > 0`
- `cms_without_notes` — count where `note_count == 0`
- `pct_complete` — (complete_done / total_countermeasures) × 100

### Step 8: Estimate Phase 2 Token Usage

Apply Token Estimation formulas. Calculate `estimated_cost_usd` for Phase 2.

### Step 9: Update Run-File

Update the JSON run-file with Phase 2 data and cumulative totals:

```json
{
  "status": "complete",
  "phase2": { "...all fields..." },
  "sde_metrics": { "...all metrics..." },
  "cumulative": {
    "duration_seconds": <phase1 + phase2>,
    "duration_human": "<H>h <M>m <S>s",
    "estimated_input_tokens": <sum>,
    "estimated_output_tokens": <sum>,
    "estimated_cost_usd": <sum>
  }
}
```

### Step 10: Generate Report

See **Report Format** section. Write the completed report to Obsidian.
```

**Step 2: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: write Phase 2 workflow section"
```

---

## Task 5: Write Token Estimation and Pricing Table Sections

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Write the Token Estimation section:**

```markdown
## Token Estimation

Token counts are estimated at the end of each phase. All estimates use the
~4 characters-per-token heuristic standard for English/code text.

**Always label estimates clearly in output**: "~X tokens (estimated)"

### Input Token Components

| Component | How to Estimate |
|---|---|
| Prompt file text | `len(file_contents_chars) / 4` |
| Files scanned in codebase | ~50 tokens × number of files read/analyzed |
| MCP tool call responses | ~2,000 tokens × number of SDE API calls made |
| Conversation/system overhead | Fixed: 5,000 tokens |
| **Total estimated input** | Sum of above |

### Output Token Components

| Component | How to Estimate |
|---|---|
| All generated text in session | `len(all_response_text_chars) / 4` |
| **Total estimated output** | Above value |

### Cost Formula

```
cost = (input_tokens / 1_000_000 × input_$/MTok)
     + (output_tokens / 1_000_000 × output_$/MTok)
```

Round to 2 decimal places. Prefix with `~` in all displays.

> Note: For models that support prompt caching (Anthropic), subsequent
> tool calls within a session may use cache reads at 0.1x input rate.
> This estimation does not account for caching; actual costs may be lower.

### Verification Note

Always include in the report:
> ⚠️ Token counts are estimates only. Verify exact usage via
> Cursor Settings → Usage.
```

**Step 2: Write the Pricing Lookup Table section:**

```markdown
## Pricing Lookup Table

All prices in USD per 1 million tokens. Source: cursor.com/docs/models (Feb 2026).

| Model Key | Input $/MTok | Cache Write | Cache Read | Output $/MTok |
|---|---|---|---|---|
| auto | $1.25 | $1.25 | $0.25 | $6.00 |
| claude-4-sonnet | $3.00 | $3.75 | $0.30 | $15.00 |
| claude-4-sonnet-1m | $6.00 | $7.50 | $0.60 | $22.50 |
| claude-4-5-haiku | $1.00 | $1.25 | $0.10 | $5.00 |
| claude-4-5-opus | $5.00 | $6.25 | $0.50 | $25.00 |
| claude-4-5-sonnet | $3.00 | $3.75 | $0.30 | $15.00 |
| claude-4-6-opus | $5.00 | $6.25 | $0.50 | $25.00 |
| claude-4-6-opus-fast | $30.00 | $37.50 | $3.00 | $150.00 |
| claude-4-6-sonnet | $3.00 | $3.75 | $0.30 | $15.00 |
| composer-1 | $1.25 | — | $0.13 | $10.00 |
| composer-1-5 | $3.50 | — | $0.35 | $17.50 |
| gemini-2-5-flash | $0.30 | — | $0.03 | $2.50 |
| gemini-3-flash | $0.50 | — | $0.05 | $3.00 |
| gemini-3-pro | $2.00 | — | $0.20 | $12.00 |
| gpt-5 | $1.25 | — | $0.13 | $10.00 |
| gpt-5-fast | $2.50 | — | $0.25 | $20.00 |
| gpt-5-mini | $0.25 | — | $0.03 | $2.00 |
| gpt-5-codex | $1.25 | — | $0.13 | $10.00 |
| gpt-5-1-codex | $1.25 | — | $0.13 | $10.00 |
| gpt-5-1-codex-max | $1.25 | — | $0.13 | $10.00 |
| gpt-5-1-codex-mini | $0.25 | — | $0.03 | $2.00 |
| gpt-5-2 | $1.75 | — | $0.18 | $14.00 |
| gpt-5-2-codex | $1.75 | — | $0.18 | $14.00 |
| gpt-5-3-codex | $1.75 | — | $0.18 | $14.00 |
| grok-code | $0.20 | — | $0.02 | $1.50 |

**If model is not in table:** Prompt the user:
> "Model `[name]` is not in the pricing table. Please provide:
> - Input $/MTok:
> - Output $/MTok:"
> Do not proceed with cost estimation until values are provided.
```

**Step 3: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: write token estimation and pricing table sections"
```

---

## Task 6: Write Compare Mode Section

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Write the Compare Mode section:**

```markdown
## Compare Mode

Invoked when user says "compare", "run sde-benchmark-run compare", or similar.

### Step 1: List Completed Runs

```bash
ls ~/projects/docs/demo-analysis/runs/*.json
```

Read each file, filter to `"status": "complete"`. Display:

```
Completed benchmark runs:
  [1] benchmark-run-2026-02-18-14-30  Project: <name>  Model: <model>  Cost: ~$2.31  CM: 82.5%
  [2] benchmark-run-2026-02-19-09-15  Project: <name>  Model: <model>  Cost: ~$1.45  CM: 70.0%
  [3] benchmark-run-2026-02-20-11-00  Project: <name>  Model: <model>  Cost: ~$3.10  CM: 88.0%

Which runs should I compare? (enter numbers, e.g. "1 2" or "all")
```

### Step 2: Generate Comparison Report

Use run-file data only (no live MCP calls). The oldest selected run is the baseline.

Follow all formatting rules from the sde-project-comparison skill for survey/CM sections.

### Step 3: Save to Obsidian

Use `obsidian_append_content` (via `user-MCP_DOCKER` MCP server):
- Path: `AI Generated/SDE Benchmarks/benchmark-comparison-YYYY-MM-DD.md`
```

**Step 2: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: write compare mode section"
```

---

## Task 7: Write Report Format Section

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Write the Report Format section** with exact Markdown templates for both single-run and comparison reports:

```markdown
## Report Format

### Output Destinations
- **Single-run report**: `AI Generated/SDE Benchmarks/benchmark-run-YYYY-MM-DD.md`
- **Comparison report**: `AI Generated/SDE Benchmarks/benchmark-comparison-YYYY-MM-DD.md`
- Written via `obsidian_append_content` using `user-MCP_DOCKER` MCP server

### Report Header

```markdown
# SDE Benchmark Run Report

**Run ID**: <run_id>
**Report Date**: <Month DD, YYYY at H:MM AM/PM PST/PDT>
**Model (Phase 1)**: <model>
**Model (Phase 2)**: <model>
**Phase 1 Prompt**: `<prompt_name>`
**Phase 2 Prompt**: `<prompt_name>`
**SDE MCP Server**: `<server>`
**Project**: <project_name> (ID: <project_id>)
```

### Benchmark Summary Table

```markdown
## 🏎️ Benchmark Summary

| Metric | Phase 1 | Phase 2 | Total |
|--------|---------|---------|-------|
| Duration | <HH>h <MM>m | <HH>h <MM>m | <HH>h <MM>m |
| Est. Input Tokens | ~<N>K | ~<N>K | ~<N>K |
| Est. Output Tokens | ~<N>K | ~<N>K | ~<N>K |
| Est. Cost (USD) | ~$<X.XX> | ~$<X.XX> | ~$<X.XX> |

> ⚠️ Token counts are estimates only. Verify via Cursor Settings → Usage.
```

### Quick Status Dashboard

Follow the sde-project-comparison skill format exactly:

```markdown
## 📊 Quick Status Dashboard

| Project | Status | Survey | CMs | Grade | Notes |
|---------|--------|--------|-----|-------|-------|
| **<name>** (<date>) | 🟢/🔴 | ✅/⚠️/❌ <pct>% | ✅/⚠️/❌ <pct>% (<n>/<total>) | **<grade>** | <model> |
```

### Detailed Comparison Table (Multi-Run)

For compare mode, include ALL columns:

```markdown
## Detailed Comparison Table

| Metric | Run A | Run B |
|--------|-------|-------|
| Run ID | ... | ... |
| Project Name | ... | ... |
| Project ID | ... | ... |
| Model (P1) | ... | ... |
| Model (P2) | ... | ... |
| Phase 1 Prompt | ... | ... |
| Phase 2 Prompt | ... | ... |
| MCP Server | ... | ... |
| Project Created | ... | ... |
| Phase 1 Duration | ... | ... |
| Phase 2 Duration | ... | ... |
| **Total Duration** | ... | ... |
| **Est. Input Tokens** | ... | ... |
| **Est. Output Tokens** | ... | ... |
| **Est. Cost (USD)** | ... | ... |
| Survey Answers | ... | ... |
| Questions Answered | ... | ... |
| Questions with Comments | ... | ... |
| Questions without Comments | ... | ... |
| Comment Coverage % | ... | ... |
| Total Countermeasures | ... | ... |
| Complete (DONE) | ... | ... |
| Incomplete (TODO) | ... | ... |
| Not Applicable (N/A) | ... | ... |
| CMs with Notes | ... | ... |
| CMs without Notes | ... | ... |
| % Complete | ... | ... |
```

Then include all standard sde-project-comparison sections:
- Key Findings (Survey Documentation, Survey Modeling, CM Status, Documentation Quality)
- Survey Answer Differences vs Baseline
- Recommendations
- Technical Details (MCP tools used, data sources)
```

**Step 2: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: write report format section"
```

---

## Task 8: Write Common Pitfalls and MCP Tools Sections

**Files:**
- Modify: `~/.cursor/skills/sde-benchmark-run/SKILL.md`

**Step 1: Write Common Pitfalls section:**

```markdown
## Common Pitfalls

- **Do NOT count comments from the survey draft** — always use `listComments` (inherits from sde-project-comparison)
- **Do NOT forget N/A countermeasures** — check `"meaning": "NA"` explicitly
- **Do NOT use placeholders** for model name or prompt name — always prompt the user if unknown
- **Do NOT proceed with cost estimation** if model is not in the pricing table — ask for rates first
- **If run-file already exists for today**, generate a new run ID with a unique HH-MM suffix to avoid overwriting
- **Validate run-file JSON** before writing — malformed JSON will break compare mode
```

**Step 2: Write MCP Tools Used section:**

```markdown
## MCP Tools Used

| Tool | Server | Purpose |
|------|--------|---------|
| `project` (op: list, get) | `user-sdelements-gitlab` | Get project metadata and creation timestamp |
| `project_survey` (op: getAnswersForProject) | `user-sdelements-gitlab` | Survey answer counts |
| `project_survey` (op: listComments) | `user-sdelements-gitlab` | Comment counts (ALWAYS use this, not getDraft) |
| `project_countermeasures` (op: list) | `user-sdelements-gitlab` | Countermeasure status and notes |
| `obsidian_append_content` | `user-MCP_DOCKER` | Write report to Obsidian vault |

**Obsidian vault path**: `C:\Users\kjohnson\Documents\Obsidian Vaults\Tech_Notes_Vault_v2`
**Report subfolder**: `AI Generated/SDE Benchmarks/`
```

**Step 3: Commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: write pitfalls and MCP tools sections"
```

---

## Task 9: Final Review and Validation

**Files:**
- Read: `~/.cursor/skills/sde-benchmark-run/SKILL.md`
- Read: `docs/plans/2026-02-18-sde-benchmark-run-design.md`

**Step 1: Verify all design requirements are covered**

Check each item from the design doc against the skill:

- [ ] Phase 1 and Phase 2 invocations with run-file persistence
- [ ] Prompt discovery from `prompts/` directory
- [ ] Model name prompt if unknown
- [ ] SDE MCP server field (default: `user-sdelements-gitlab`)
- [ ] Wall-clock timing per phase + cumulative
- [ ] Token estimation with formulas
- [ ] Full pricing lookup table (all 24 models including `auto` and `composer-1-5`)
- [ ] Cost calculation formula
- [ ] Unknown model prompts user for rates
- [ ] Run-file schema (JSON, correct path)
- [ ] SDE metrics collection following sde-project-comparison rules
- [ ] Compare mode lists runs and generates side-by-side report
- [ ] Report written to Obsidian `AI Generated/SDE Benchmarks/`
- [ ] Benchmark Summary table in report
- [ ] Detailed Comparison table with all new columns
- [ ] Estimation disclaimer in all reports
- [ ] Common pitfalls documented

**Step 2: Fix any gaps found**

Address any missing items from the checklist above.

**Step 3: Final commit**

```bash
git add skills/sde-benchmark-run/SKILL.md
git commit -m "feat: finalize sde-benchmark-run skill — all sections complete"
```

**Step 4: Verify skill is discoverable**

```bash
ls -la ~/.cursor/skills/sde-benchmark-run/SKILL.md
head -5 ~/.cursor/skills/sde-benchmark-run/SKILL.md
```
Expected: file exists, YAML frontmatter present with `name: sde-benchmark-run`
