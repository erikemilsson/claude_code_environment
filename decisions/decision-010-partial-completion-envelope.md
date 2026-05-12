---
id: DEC-010
title: partial_completion envelope — schema and threshold for usage-limit graceful resume
status: draft
category: architecture
created: 2026-05-13
decided:
related:
  tasks: []
  decisions: [DEC-004]
  feedback: [FB-049]
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# partial_completion envelope — schema and threshold for usage-limit graceful resume

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Minimal envelope — three fields, implement-only, in-handoff
- [ ] Option B: Full envelope — five fields + integrity hash, implement-only, dedicated sidecar
- [ ] Option C: Middle path — four fields, implement-only, in-handoff (recommended)
- [ ] Option D: Symmetric envelope — Option C + matching verify-agent contract
- [ ] Option E: Defer — rely on SDK `error_max_turns` + existing `[PARTIAL]` notes; do nothing template-side

*Check one box above, then fill in the Decision section below.*

---

## Context

Anthropic usage-limit cuts mid-implement-agent or mid-verify-agent are recurring. Two cases in a single styler Phase 20 session (2026-04-27): T433's first dispatch was cut at 41 tool uses with no structured report; T454's verify-agent dispatch never even started before the limit hit. Current handoff is via free-form task notes + dashboard prose + `.last-clean-exit.json` — entirely manual. Subsequent invocations have to audit partial work by reading git diff + task notes, costing ~10-15 minutes of audit overhead per case.

FB-049 proposes a `partial_completion` envelope that implement-agent fills when sensing usage-limit approach with unfinished sub-targets. Orchestrator persists to task JSON; next dispatch brokers a "resume from where you stopped" prompt instead of re-deriving context from git diff.

Multiple design questions remain unresolved:

1. **Envelope minimality:** What fields are strictly necessary vs nice-to-have? Token budget for the envelope matters — every field the agent fills costs context.
2. **Detection threshold:** FB-049 proposes "tool_uses > 75% of typical session budget AND remaining sub-targets > 0." But 75% is arbitrary and depends on `max_turns` (40 default for implement, 25-30 for verify). Per-agent threshold or unified?
3. **verify-agent symmetry:** Should verify-agent get a matching envelope (`partial_verification_pending`), or is its work atomic enough that a graceful-cut behavior would be more confusing than useful?
4. **.handoff.json schema impact:** Should the existing handoff schema absorb task-level partial state, or should a separate per-task `task-{id}.partial.json` file hold it?
5. **Re-dispatch context contract:** When the orchestrator re-dispatches a task with a `partial_completion` envelope, what's the exact prompt shape? "Resume from {completed_subtargets}" — but how does the implement-agent verify the previous attempt's edits didn't corrupt state?

## Questions to Research

*(Answers in `## Research Findings` below.)*

1. What does the Anthropic API signal when approaching usage limits? Is there an in-band hint the agent can use, or does the agent have to estimate from `tool_uses` count alone?
2. What does the current implement-agent return schema (`.claude/agents/implement-agent.md` § Step 6) cost in tokens? Adding a `partial_completion` envelope with N fields adds how much?
3. Are there existing precedents in the template (or other agent frameworks the user has integrated) for partial-completion / structured-resume contracts? What fields proved necessary vs decorative?
4. How does a `partial_completion` flow interact with verify-agent? If implement-agent returns `partial_resume_pending`, does verify-agent never run, or does it run on the partial state?
5. What's the right unit for "remaining work" — sub-targets (named work items within the task), file-level (which files still need edits), or step-level (Step 4 done, Step 5 partial)?
6. How does the orchestrator detect that a re-dispatched task's prior edits are still intact (not rolled back, no merge conflicts)? Does the envelope need a `prior_attempt_files_hash` field?
7. What's the failure mode if the partial envelope is wrong (e.g., agent says `completed_subtargets: [A, B]` but B was actually only half-done)? How is this guarded?
8. Should the envelope have a `confidence` field (high/moderate/low) like research-agent's recommendation, to surface uncertainty to the next dispatch?

## Options Comparison

*(populated after research completes)*

## Option Details

*(populated after research completes)*

## Recommendation

*(populated after research completes)*

## Research Findings

*(populated by research-agent)*

## Your Notes & Constraints

*(user notes go here)*

---

## Decision

*(populated after user selects an option)*
