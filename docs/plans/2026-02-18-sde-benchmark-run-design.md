# sde-benchmark-run Skill Design

**Date**: February 18, 2026  
**Status**: Approved  
**Author**: Brainstormed via Cursor AI session

---

## Purpose

A new Cursor skill (`sde-benchmark-run`) that orchestrates and measures a full two-phase SDE evaluation run — project modeling followed by countermeasure implementation — then generates an enriched comparison report extending the existing `sde-project-comparison` format with timing, cost, model, and prompt metadata.

---

## Problem Statement

The existing `sde-project-comparison` skill compares SDE project metrics (survey answers, countermeasure status) but has no awareness of *how* a project was created — which model was used, how long it took, which prompts drove it, or what it cost. This makes it impossible to benchmark model quality vs. cost vs. speed across runs.

---

## Approach: Option B — Accumulator (Separate Sessions)

The skill is invoked separately for each phase. State is persisted to a JSON run-file on disk between invocations. This approach was chosen because:

- Each prompt run benefits from a fresh, focused context window
- Long-running sessions (30–90 min each) risk context exhaustion in a single session
- Run-files provide a resilient, reusable historical record
- Phase 1 data is preserved even if Phase 2 fails or needs to be retried with a different model

---

## Workflow

### Invocation 1 — Start Run / Phase 1 (Project Creation)

1. Skill lists prompt files from `prompts/` matching `model-*.txt`
2. Asks user to select the project creation prompt (or enter a path)
3. Asks which model is being used (if not determinable from context)
4. Asks which SDE MCP server to use (defaults to `user-sdelements-gitlab`)
5. Records `phase1.start_time`
6. Reads and injects the selected prompt, executes it (creates SDE project, answers survey, publishes, adds comments)
7. Records `phase1.end_time`, calculates `phase1.duration_seconds`
8. Estimates token usage (see Token Estimation section)
9. Writes run-file to `~/projects/docs/demo-analysis/runs/benchmark-run-YYYY-MM-DD-HH-MM.json`
10. Prints run-file path and instructs user to invoke skill again for Phase 2

### Invocation 2 — Phase 2 (Countermeasure Implementation)

1. Skill detects existing run-file(s) in `~/projects/docs/demo-analysis/runs/`
2. Asks user to confirm which run to continue (if multiple in-progress)
3. Lists prompt files from `prompts/` matching `implement-*.txt`
4. Asks user to select the countermeasure prompt
5. Records `phase2.start_time`
6. Reads and injects the selected prompt, executes it (implements countermeasures, updates statuses, adds notes)
7. Records `phase2.end_time`, calculates `phase2.duration_seconds`
8. Estimates token usage for Phase 2
9. Updates run-file with Phase 2 data + cumulative totals
10. Fetches final SDE project metrics via MCP (survey answers, countermeasure status)
11. Generates the benchmark comparison report (see Report Format section)
12. Saves report to Obsidian: `AI Generated/SDE Benchmarks/benchmark-run-YYYY-MM-DD.md`

### Compare Mode — Multi-Run Comparison

Invoked as: *"Run sde-benchmark-run compare"*

1. Lists all completed run-files in `~/projects/docs/demo-analysis/runs/`
2. Asks user which runs to include in the comparison
3. Reads cached data from selected run-files (no live MCP re-fetch)
4. Generates side-by-side comparison report
5. Saves to Obsidian: `AI Generated/SDE Benchmarks/benchmark-comparison-YYYY-MM-DD.md`

---

## Run-File Schema

**Location**: `~/projects/docs/demo-analysis/runs/benchmark-run-YYYY-MM-DD-HH-MM.json`

```json
{
  "run_id": "benchmark-run-2026-02-18-14-30",
  "status": "complete",
  "phase1": {
    "prompt_file": "prompts/model-in-sde-v2.txt",
    "prompt_name": "model-in-sde-v2",
    "model": "claude-4-6-sonnet",
    "sde_mcp_server": "user-sdelements-gitlab",
    "project_id": 812,
    "project_name": "Damn Vulnerable RESTaurant API",
    "start_time": "2026-02-18T14:30:00",
    "end_time": "2026-02-18T14:58:42",
    "duration_seconds": 1722,
    "estimated_input_tokens": 85000,
    "estimated_output_tokens": 18000,
    "estimated_cost_usd": 0.54
  },
  "phase2": {
    "prompt_file": "prompts/implement-countermeasures-v2.txt",
    "prompt_name": "implement-countermeasures-v2",
    "model": "claude-4-6-sonnet",
    "sde_mcp_server": "user-sdelements-gitlab",
    "start_time": "2026-02-18T15:10:00",
    "end_time": "2026-02-18T16:02:15",
    "duration_seconds": 3135,
    "estimated_input_tokens": 280000,
    "estimated_output_tokens": 62000,
    "estimated_cost_usd": 1.77
  },
  "sde_metrics": {
    "total_survey_answers": 45,
    "questions_answered": 23,
    "questions_with_comments": 23,
    "questions_without_comments": 0,
    "comment_coverage_pct": 100.0,
    "total_countermeasures": 40,
    "complete_done": 33,
    "incomplete_todo": 5,
    "not_applicable_na": 2,
    "cms_with_notes": 40,
    "cms_without_notes": 0,
    "pct_complete": 82.5
  },
  "cumulative": {
    "duration_seconds": 4857,
    "duration_human": "1h 20m 57s",
    "estimated_input_tokens": 365000,
    "estimated_output_tokens": 80000,
    "estimated_cost_usd": 2.31
  }
}
```

---

## Token Estimation Logic

Token counts are estimated at the end of each phase using character-based heuristics (approximately 4 characters per token):

| Component | Estimation Method |
|---|---|
| Prompt file text | `len(file_contents) / 4` |
| Codebase context scanned | ~50 tokens per file touched × estimated files scanned |
| MCP tool call responses | ~2,000 tokens per SDE API call × number of calls made |
| Conversation/system overhead | Fixed ~5,000 tokens |
| **Output tokens** | `len(all_generated_response_text) / 4` |

These are clearly labeled as estimates in all output. The skill will note: *"Token counts are estimated; verify via Cursor Settings → Usage for exact figures."*

---

## Pricing Lookup Table

All prices in USD per 1 million tokens. Used to calculate `estimated_cost_usd`.

| Model | Input | Cache Write | Cache Read | Output |
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

**Cost formula**: `(input_tokens / 1_000_000 × input_rate) + (output_tokens / 1_000_000 × output_rate)`

If the model is not in the table, the skill will prompt: *"Model `[name]` not found in pricing table. Please provide input $/MTok and output $/MTok."*

---

## Report Format

### Markdown Report Output
**Location**: `AI Generated/SDE Benchmarks/benchmark-run-YYYY-MM-DD.md` (Obsidian vault)  
**Written via**: `obsidian_append_content` using `user-MCP_DOCKER` MCP server

### Benchmark Summary Table (top of report)

```markdown
## 🏎️ Benchmark Summary

| Run | Model | Phase 1 Prompt | Phase 2 Prompt | MCP Server |
|-----|-------|----------------|----------------|------------|
| Run A | claude-4-6-sonnet | model-in-sde-v2 | implement-countermeasures-v2 | user-sdelements-gitlab |

| Run | P1 Time | P2 Time | Total Time | Est. Input Tok | Est. Output Tok | Est. Cost |
|-----|---------|---------|------------|----------------|-----------------|-----------|
| Run A | 28m 42s | 52m 15s | 1h 20m 57s | ~365K | ~80K | ~$2.31 |
```

### Quick Status Dashboard (from sde-project-comparison)
Unchanged — same format as the existing skill.

### Detailed Comparison Table
All existing `sde-project-comparison` columns **plus**:
- Model
- Phase 1 Prompt
- Phase 2 Prompt
- MCP Server
- Phase 1 Duration
- Phase 2 Duration
- Total Duration
- Est. Input Tokens
- Est. Output Tokens
- Est. Cost (USD)

### Multi-Run Comparison (compare mode)

```markdown
## 🏎️ Benchmark Summary

| Run | Model | Total Time | Est. Cost | CM Complete % | Grade |
|-----|-------|-----------|-----------|---------------|-------|
| Run A | claude-4-6-sonnet | 1h 20m | ~$2.31 | 82.5% | A+ |
| Run B | gpt-5 | 58m | ~$1.45 | 70.0% | B |
```

---

## File & Directory Structure

```
~/projects/
  docs/
    demo-analysis/
      runs/
        benchmark-run-2026-02-18-14-30.json   ← run-files (JSON)
        benchmark-run-2026-02-19-09-15.json
Obsidian Vault (C:\Users\kjohnson\Documents\Obsidian Vaults\Tech_Notes_Vault_v2)
  AI Generated/
    SDE Benchmarks/
      benchmark-run-2026-02-18.md             ← single-run reports
      benchmark-comparison-2026-02-20.md      ← multi-run comparisons
~/.cursor/skills/
  sde-benchmark-run/
    SKILL.md                                  ← the new skill
```

---

## Skill Location

`/home/hirosh7/.cursor/skills/sde-benchmark-run/SKILL.md`

---

## Related Skills & Dependencies

- **`sde-project-comparison`**: This skill extends that format. The report sections for survey metrics and countermeasure status are generated following the same rules.
- **`obsidian-notes`**: Used for writing the final markdown report to the vault.
- **`user-sdelements-gitlab` MCP server**: Used for fetching SDE project metrics after Phase 2.
- **`user-MCP_DOCKER` MCP server**: Used for writing to the Obsidian vault.

---

## Constraints & Notes

- Token counts are estimates only — users should verify via Cursor Settings → Usage
- The `auto` model's actual underlying model cannot be determined programmatically; cost estimate uses auto's own rates ($1.25 input / $6.00 output)
- Run-files use cached SDE metrics for compare mode (no live MCP re-fetch), preserving a snapshot of project state at run completion time
- If a model name is not in the pricing table, the skill will prompt the user before proceeding with cost calculation
- Prompt files are expected in `prompts/` relative to the workspace root; the skill will list available files and ask the user to select
