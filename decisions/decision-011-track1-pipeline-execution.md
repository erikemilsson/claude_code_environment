---
id: DEC-011
title: Track 1 / Track 2 pipeline execution — fix tier for marker-append + session-export reliability
status: draft
category: architecture
created: 2026-05-13
decided:
related:
  tasks: []
  decisions: [DEC-001]
  feedback: [FB-057]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Track 1 / Track 2 pipeline execution — fix tier for marker-append + session-export reliability

## Select an Option

*(populated after research completes; final selection gated on real downstream telemetry availability)*

---

## Context

DEC-001 Option C (Track 1 friction markers + Track 2 retrospective + Phase 3 ingest) is documented end-to-end across `implement-agent.md`, `verify-agent.md`, `work.md`, `pre-compact-handoff.sh`, and `health-check.md`. But empirical evidence (styler Phase 20 observation 2026-04-27 + DEC-001 Option C audit 2026-05-13) suggests the pipeline isn't reliably executed:

- **Cause 1 (resolved 2026-05-13 by FB-040 Part 5d):** downstream `template_inbox_path` discoverability gap. Closed.
- **Cause 2 (open):** orchestrator-side marker append (`work.md:543`) documented but not reliably executed during `/work` runs. Styler Phase 20: 8 markers batch-appended at pause; abrupt termination would have lost all.
- **Cause 3 (open):** `/work pause` Track 2 + Session Export step not reliably run.

FB-057's tiered fix path:

- **A. Behavioral nudge:** tighter protocol — "append marker via single bash call immediately after agent return; do not batch."
- **B. Idempotent catchup:** orchestrator (or PreCompact hook) auto-appends missing markers detected from task notes.
- **C. Structural hook:** PostAgentReturn / PostToolUse hook gated on Task subagent (un-skippable by the orchestrator).
- **D. Deterministic script:** extract marker-append into a `.claude/scripts/` script (FB-011 Family D/E candidate).

These tiers are not mutually exclusive — a final ship could combine, e.g., B (idempotent catchup) + lightweight A (behavioral nudge). The decision is the right combination.

**Telemetry gate:** currently no downstream project has `template_inbox_path` set, so there's no Track-1 telemetry to inspect yet. (FB-040 Part 5d will surface this in the next downstream `/health-check`.) Research can prepare the option analysis but the final selection waits for empirical evidence from real downstream sessions.

## Questions to Research

*(Answers in `## Research Findings` below.)*

1. What's the current orchestrator-side marker append mechanic in `commands/work.md:543` (and parallel-execution.md mirror)? Is it specified as inline or batched, and does the prose match a reliable execution pattern?
2. Hook-based approaches in Claude Code: does PostToolUse fire after Task subagent completion? Can a hook gate be set on `subagent_type` or model? How would such a hook compose with the existing PreCompact handoff hook in `.claude/hooks/pre-compact-handoff.sh`?
3. Deterministic script approach (FB-011 Family D/E): what would the script's invocation contract be? Pure stdlib? Read-only or write? Idempotent given multiple invocations? Where would it live in the orchestrator's workflow?
4. What's the cost of each tier — how much template-side change, how much downstream-side change, what new failure modes does each introduce?
5. Is there a way to detect that markers are *missing* (the canonical state — what *should* be in `.session-log.jsonl` — derived from agent reports) so an idempotent catchup is even possible?
6. Could the lightweight tier (behavioral nudge) succeed under Opus 4.7's stronger instruction following alone? Is there a way to A/B-test this against current behavior without burning real downstream sessions?
7. What does the styler Phase 20 evidence specifically reveal about WHY the orchestrator skipped the append step? Was it Claude prioritizing user-facing communication, was it a misread of the procedure, or a context-pressure forgetting?
8. Are there other Track 1 / Track 2 pipeline parts that have the same execution-skip risk (e.g., `/work pause` Session Export step), or is the marker-append step a uniquely-skippable case?

## Options Comparison

*(populated after research completes; final selection gated on downstream telemetry)*

## Option Details

*(populated after research completes)*

## Recommendation

*(populated after research completes; gated on downstream telemetry availability)*

## Research Findings

*(populated by research-agent)*

## Your Notes & Constraints

*(user notes go here)*

---

## Decision

*(populated after user selects an option, post-telemetry)*
