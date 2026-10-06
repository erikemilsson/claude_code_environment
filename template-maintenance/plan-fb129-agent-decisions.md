# Plan: FB-129, agent-recorded decisions reach the user (v5.11.0)

**Status:** COMPLETE — shipped v5.11.0 (2026-10-06). Design approved by the maintainer (decisions 1–8, 2026-10-06).

## Measured first (read-only, 8 downstream projects, 2026-10-06)

- 52 of 239 decision records carry `decided_by: implement-agent`; 51 `approved`, 1 `superseded`, none ever `proposed`.
- 24 were provably created before their task's first verify pass (file birth time vs pass timestamp; lower bound).
- 26 of 52 sit in same-task clusters (largest: 5 records for styler task 677). About 15 are trivial by title.
- 5 use `## Selected`, 4 have neither `## Selected` nor `## Decision` (8 of the 9 in PortfolioWebsite); 40 lack `## Options Comparison`.
- 24 have a ticked `## Select an Option` box the user never ticked.
- 4 agent records are in a task's `decision_dependencies` (all four tasks Finished).
- 77 of 239 project record ids equal a template-cited DEC id. Unavoidable (projects start at 001), so the remedy is disambiguated citation.

## Build contract

**C1. Status `recorded`.** New decision status: an agent made the choice during implementation, the work is verified, the user has not ratified it. Lifecycle: `recorded → approved` (ratified) or `recorded → proposed` (reconsidered). `recorded` counts as **resolved** for `decision_dependencies` (it never blocks a task, Step 1d, or a phase gate) but is **not** "Decided".

Frontmatter of an agent-recorded record:
```yaml
status: recorded
decided: <date of the verify pass>
decided_by: implement-agent        # or `orchestrator` for inline work
related:
  tasks: [<task id>]
```
After ratification: `status: approved` plus a new key `ratified: YYYY-MM-DD`; `decided_by` is unchanged (provenance). Legacy records (status `approved`/`implemented`, `decided_by: implement-agent`, no `ratified`) are only surfaced by `/health-check` (C7), never by the renderer.

**C2. Renderer (`dashboard-render.py`).** `recorded` is not in `UNRESOLVED_DECISION`. Display label `Recorded`; not counted in "decided". The summary block gains `decisions_recorded: N`. When N ≥ 1 the Needs-you card gets exactly **one** row for the whole project: `N agent decision(s) await ratification: DEC-031, DEC-032 … — run /work ratify all (or /work ratify DEC-NNN)`, ids linked to their files, at most 8 ids then `+K more`. The row lives with the other decision rows. Whatever staleness signal existing decision rows rely on must also cover it.

**C3. Task field `decisions_pending`.** Optional array on a task; each element has the shape of an implement-agent `decisions_to_record[]` entry. `validate-tasks.py` accepts it (array of objects) and does not otherwise change.

**C4. Flow (`work-procedures.md` § State Persistence Protocol).**
- *After implement-agent returns*, step 3 becomes **Hold decisions**: drop entries that meet `decisions.md` § "Skip Records For" (prepend each to task `notes` as `[CHOICE] …`); set the task's `decisions_pending` to the remaining entries, **replacing** any previous value (an empty set removes the field). No decision file is written here.
- *After verify-agent returns, pass branch* (also any other path that sets a task Finished, e.g. `/work complete`): **Persist decisions**: if `decisions_pending` is non-empty, write **one** record for the task (`decision-NNN-{slug}.md`, next free project id) with C1 frontmatter, `## Background`, `## Options Comparison`, `## Decision` (a `**Selected:**` line and rationale per choice), `## Trade-offs`, `## Impact`; **no** `## Select an Option` section. Then remove the field. Never add the new id to any task's `decision_dependencies`. Tier-1 dashboard regen. The step names the template's `## Decision` (`**Selected:**`) and `## Options Comparison` and links `support/reference/decisions.md` § "Numbering namespace".
- Fail branch: the field stays; the next implement report replaces it.
- Inline work by the orchestrator (FB-119) uses the same two steps.

**C5. Ratifying (`commands/work.md`).** New sub-mode `/work ratify [all | DEC-NNN …]`: for each named `recorded` record set `status: approved` and add `ratified: <today>` (frontmatter only), then regenerate the dashboard. `/work reconsider DEC-NNN`: set `status: proposed` and point at `/research DEC-NNN`; the task stays Finished, follow-up work is a new task after the user selects. Both are frontmatter-only edits: DEC-016's infrastructure carve-out (the `permissions.ask` prompt still fires once per session).

**C6. Phase gates.** Unratified records do not block. The phase-gate summary shows the count.

**C7. `/health-check` Part 3.** `recorded` is a valid status. New rows (Fix Queue Protocol, excluded from bare `[A]`): legacy agent-approved records, one row per project, offering "mark ratified" (adds `ratified: <today>`) or "flip to `recorded`"; default is leave. A row to rename `## Selected` to `## Decision`.

**C8. `support/reference/decisions.md`.** Lifecycle with `recorded`; a section on agent-recorded decisions (shape, timing, ratification); the numbering-namespace rule gains "cite a template record as `template DEC-NNN` in project files".

**C9. `agents/implement-agent.md`.** `decisions_to_record[]`: one entry per coupled set of choices, normally one per task; the full current set is restated on every return (fix rounds included); trivial choices go to `notes`. The agent never claims approval.

**C10. `rules/spec-workflow.md`.** The infrastructure-operations list names ratification frontmatter (`status`, `ratified`).

**C11. `commands/research.md`.** `/research DEC-NNN` on a `recorded` record confirms, then treats it as reconsider (C5).

## File ownership

| Agent | Files (inside its mirror) |
|---|---|
| A (scripts) | `dot-claude/scripts/dashboard-render.py`, `validate-tasks.py`, `scripts/tests/*`, `scripts/README.md` |
| B (work flow) | `dot-claude/support/reference/work-procedures.md`, `commands/work.md`, `agents/implement-agent.md`, `support/reference/task-schema.md`, `phase-decision-gates.md`, `work-user-flows.md`, `work-recovery.md`, `session-recovery.md`, `parallel-execution.md` |
| C (decisions, health, docs, scenarios) | `dot-claude/support/reference/decisions.md`, `rules/decisions.md`, `rules/spec-workflow.md`, `rules/dashboard.md`, `commands/health-check.md`, `commands/research.md`, `commands/status.md`, `support/reference/dashboard-regeneration.md`, `shared-definitions.md`, `dot-claude/README.md`, `agents/research-agent.md`, `agents/verify-agent.md`, `tests/scenarios/*`, `tests/README.md` |

## Amendments

- **A1 (row wording).** The renderer pluralises: `1 agent decision awaits ratification: …`, `N agent decisions await ratification: …`; no trailing ellipsis. Docs and scenario 49 follow the script.
- **A2 (META).** `decisions_recorded` is a META key directly after `decisions_approved` (15 keys). Decisions are not a `task_hash` input; the count lines are their staleness signal, so C4's regen after persist and C5's regen after ratify are required.
- **A3 (persist is a named paragraph).** "Persist decisions (when a task becomes Finished)" sits beside "Friction entries a task fixes" and is invoked from the pass branch, parent auto-completion and `/work complete`; step numbers are unchanged. A pending user review does not delay it.
- **A4 (inline provenance).** Inline Hold adds `"decided_by": "orchestrator"` to each held entry; Persist reads it.
- **A5 (fix rounds).** A fix round runs in a fresh agent, so the dispatch passes the task's `decisions_pending` and the agent restates the current set.
- **A6 (`decision_made` removed).** The `issues_discovered` type `decision_made` had no consumer; `decisions_to_record` is the signal.
- **A7 (checkbox auto-approve).** `phase-decision-gates.md` and `extension-patterns.md`: a checked box auto-approves only a `draft`/`proposed` record. 24 legacy agent records carry a self-ticked box; without this, a legacy record flipped to `recorded` would be auto-approved on the next `/work` with no `ratified`.
- **A8 (reconsidered records).** `/work reconsider` sets only `status: proposed`. `/research DEC-NNN` inserts the missing `## Select an Option`, `## Option Details` and `## Your Notes & Constraints` sections so the user's tick has somewhere to land.
- **A9 (health-check rows).** The legacy row is `needs-input` with replies `ratified / recorded / keep` (default keep). The `## Selected` rename row carries a new risk flag, `⚠ edits decision record`.
- **A10 (gate checks).** "Unresolved" in the gate checks is now "record missing, or `draft`/`proposed` with no checked box" (it was "no checked box", which would have read every `recorded` record as unresolved). The Late Decision Check skips agent and orchestrator records.
- **A11 (unowned files, edited by the orchestrator).** `context-transitions.md` (7-case scan), `rules/agents.md` (inline contract holds choices), `.claude/CLAUDE.md` (command table row), `extension-patterns.md` (A7).

## Review fixes (independent review: 1 blocker, 6 should-fix, 6 nits; all applied by a fixer agent on a fresh mirror)

- **F1 (blocker).** `/work reconsider` (and `/research` on a `recorded` record) unticks a `## Select an Option` box the agent ticked; otherwise the next `/work` or `/iterate` approved the reopened record. This is the sub-mode's only body edit.
- **F2.** A user tick on a record with `decided_by: implement-agent`/`orchestrator` also adds `ratified`.
- **F3.** The follow-up-task offer for a reconsidered decision lives in `phase-decision-gates.md` § "Post-Decision Check" (both `/work` Step 2b and `/iterate` Step 1a run it).
- **F4.** Persist handles a task that already has an agent record (rework after Finished): repeat → nothing; changed → new record linked by `related.decisions`, an old `recorded` one becomes `superseded`.
- **F5.** `/work` Step 0g persists an interrupted write (a Finished task with `decisions_pending`); `session-recovery.md` case 7 points there.
- **F6.** Legacy `implemented` records are offered `ratified / keep` only; never flipped to `recorded`.
- **F7.** Scenario 37 updated. **F8–F13 (nits).** "approved this run"; empty case for `/work ratify`; one regen per pass; `draft`/`proposed` at both tick-scan sites; parallel fix rounds restate held decisions; escaping test for the ratify row.
