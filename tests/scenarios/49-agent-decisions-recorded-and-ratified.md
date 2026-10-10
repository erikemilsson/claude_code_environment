# Scenario 49 — Agent decisions are held, recorded after verification, and ratified by the user (FB-129)

Conceptual trace test for v5.11.0. A non-trivial choice an agent makes while implementing a task is held on the task (`decisions_pending`) until verification passes, then written as **one** decision record per task with status `recorded`. A `recorded` decision never blocks anything, is not shown as Decided, and reaches the user as one Needs-you row; the user ratifies it (`/work ratify`) or reopens it (`/work reconsider`). Trivial choices become `[CHOICE]` notes. `/health-check` surfaces records that older versions wrote straight to `approved`.

## Setup / State

- `.claude/support/decisions/` holds DEC-001 … DEC-005, none `recorded`. The next free project id is DEC-006.
- A held entry has the shape of an implement-agent `decisions_to_record[]` entry (`title`, `summary`, `options_considered`, `selected_option`, `rationale`, `related_task_ids`).
- "Hold decisions" and "Persist decisions" are the steps of those names in `work-procedures.md § "State Persistence Protocol"` (after implement-agent returns; after verify-agent returns, pass branch). The traces name steps, not step numbers.
- Trivial means it meets `decisions.md § "Skip Records For"`.
- Traces A → C follow one task. Each later trace lists the state it starts from.

## Trace A — implement-agent returns choices: held on the task, no file

Command path: `commands/work.md § "If Executing"` → `work-procedures.md § "State Persistence Protocol"`: "After implement-agent returns", step "Hold decisions".

State: Task 14 "Add outlier filtering to the cleaning step" (`owner: claude`, In Progress, no `decisions_pending`, `notes: ""`).

1. implement-agent returns `completed` with two `decisions_to_record[]` entries:
   - "Outlier rule for the cleaning step": one entry covering two coupled choices (IQR fences over z-scores; the fence multiplier lives in `config.yaml`, default 1.5).
   - "Helper name": the bounds helper is called `_iqr_bounds`. A trivial implementation detail.
2. "Hold decisions": the helper-name entry meets "Skip Records For", so it is dropped from the set and prepended to `notes` as `[CHOICE] …`. The remaining entry becomes the task's `decisions_pending` (one element).
3. No file is written under `.claude/support/decisions/`. The highest record is still DEC-005.
4. Task 14 → Awaiting Verification; verify-agent is dispatched as usual.

Variant, agent already filtered: the report carries only the outlier entry and mentions the helper name in its `notes`. `decisions_pending` is the same one element; the orchestrator adds no `[CHOICE]` note of its own.

Variant, nothing to hold: the report has no entries, or only trivial ones. The task gets no `decisions_pending` field (an empty set removes it).

Variant, inline work: the orchestrator implemented Task 14 itself (`[INLINE]`, `rules/agents.md § "Dispatch Invariants vs Efficiency Defaults"`). It holds its own choices the same way.

**Expected:** before v5.11.0 the orchestrator wrote `decision-006-….md` at this point with `status: approved`, before any verification and without the user. Now nothing the user hasn't seen is called approved, and unverified work leaves no decision record behind.

**Pass criteria:** `decisions_pending` holds exactly one entry (the coupled pair as one); `notes` begins with a `[CHOICE]` note for the helper name; no decision file is created; the entry keeps the `decisions_to_record[]` shape; an empty set leaves no field.

## Trace B — verification fails, the fix changes the choices: field replaced, still no file

Command path: `work-procedures.md § "State Persistence Protocol"`: "After verify-agent returns (per-task mode)", fail branch → "After implement-agent returns", step "Hold decisions".

State: Task 14 from Trace A (Awaiting Verification, `decisions_pending` with the IQR entry).

1. verify-agent returns `fail`: the IQR fences drop valid readings from a skewed sensor column. Task 14 → In Progress with a `[VERIFICATION FAIL #1]` note. `decisions_pending` is untouched.
2. implement-agent fixes it and returns `completed`. Its report restates the full current set: one entry, "Outlier rule for the cleaning step", now selecting median absolute deviation (MAD) over IQR and z-scores, threshold still in `config.yaml`.
3. "Hold decisions" **replaces** `decisions_pending` with the report's set. The field holds one entry (MAD); the IQR entry is gone, not appended to.
4. Still no file under `.claude/support/decisions/`.

Variant, fix round with no choices left: the fix removes the need for the choice and the report carries no entries. The field is removed.

**Expected:** the record written later describes what was verified, not a first attempt that failed. A choice abandoned in a fix round never becomes a record.

**Pass criteria:** after the fail, the field is unchanged; after the fix round, it equals the new report's set (replaced, never merged); `notes` keeps the `[VERIFICATION FAIL #1]` entry and the `[CHOICE]` note (prepend-only, scenario 46); no decision file exists.

## Trace C — verification passes: one `recorded` record, one ratify row

Command path: `work-procedures.md § "State Persistence Protocol"`: "After verify-agent returns (per-task mode)", pass branch, step "Persist decisions" → `decisions.md § "Agent-recorded decisions"` → `dashboard-regeneration.md § "When to Regenerate"` (Tier 1).

State: Task 14 from Trace B (Awaiting Verification, `decisions_pending` with the MAD entry). Task 15 (Pending) depends on Task 14. The verify pass is dated 2026-10-06.

1. verify-agent returns `pass`. Task 14 → Finished.
2. "Persist decisions": `decisions_pending` is non-empty, so the orchestrator writes `decision-006-outlier-rule-for-the-cleaning-step.md`, one record for the task, with frontmatter:
   ```yaml
   id: DEC-006
   status: recorded
   decided: 2026-10-06
   decided_by: implement-agent
   related:
     tasks: [14]
   ```
   and the headings `## Background`, `## Options Comparison`, `## Decision`, `## Trade-offs`, `## Impact`. `## Decision` has a `**Selected:**` line and rationale for each choice (MAD; threshold in `config.yaml`). There is no `## Select an Option` section and no ticked box.
3. `decisions_pending` is removed from Task 14.
4. DEC-006 is added to no task's `decision_dependencies`: not Task 14's, not Task 15's.
5. The dashboard is regenerated. The Needs-you card has exactly one row for agent decisions, with the other decision rows:
   `1 agent decision awaits ratification: DEC-006 — run /work ratify all (or /work ratify DEC-NNN)`
   with `DEC-006` linked to its file. The Decisions card shows DEC-006 as "Recorded". META has `decisions_recorded: 1`; `decisions_approved` did not change.
6. `/work` continues to Task 15 without a prompt.

Variant, a task with three held entries: still one record, DEC-006, whose `## Decision` carries three `**Selected:**` lines.

Variant, inline work: `decided_by: orchestrator`.

Variant, `/work complete 14` finishes the task instead of a verifier pass: the same step runs.

Variant, a second task (Task 16) passes with held choices: DEC-007 is written the same way. The card still has **one** row: `2 agent decisions await ratification: DEC-006, DEC-007 — run /work ratify all (or /work ratify DEC-NNN)`. With ten `recorded` records the row lists eight ids, then `+2 more`.

Variant, numbering: the next record takes the number after the project's own highest existing record (`decisions.md`, "Numbering namespace"). Shipped instruction files cite no template decision ids, so a bare `DEC-006` in them or in project files is the project's record.

**Expected:** the record exists only once the work is verified, says who decided, and waits for the user without stopping anything.

**Pass criteria:** exactly one new file for the task; `status: recorded`, `decided` = the pass date, `decided_by` set, `related.tasks` names the task; the five headings, `**Selected:**` per choice, no `## Select an Option`; the task no longer has `decisions_pending`; no `decision_dependencies` gained the id; one ratify row whatever the count, capped at eight ids; DEC-006 is not counted as decided.

## Trace D — `recorded` never blocks a task or a phase gate

Command path: `commands/work.md § "Step 1d: Non-Actionable State Fast Path"` and `§ "Step 2b: Phase and Decision Gate"` → `phase-decision-gates.md` (decision dependency check; phase-gate summary).

State: DEC-003 was written by an older version as agent-approved, and `/health-check` flipped it to `recorded` (Trace G). Task 20 "Wire the cleaning config into the CLI" (Pending, `owner: claude`, dependencies met) has `decision_dependencies: ["DEC-003"]`, added by hand before the upgrade. DEC-003 has no `## Select an Option` section. Task 20 is the only unfinished task of Phase 1; Phase 2 tasks exist.

1. Step 1d: DEC-003 is `recorded`, which counts as resolved. Task 20 is actionable: no fast exit, no `Waiting on decisions:` line for it.
2. Step 2b's decision dependency check does not treat DEC-003 as unresolved, although no box is ticked: no `[R] Research / [S] Skip` prompt.
3. Task 20 is implemented and verified. All Phase 1 tasks are Finished.
4. The Phase 1 → 2 gate is presented. Its summary shows the count of unratified agent decisions; the gate's conditions don't include them, and the user can approve the gate with DEC-003 and DEC-006 still `recorded`.
5. The dependency graph and critical path show no `❗ Resolve DEC-003` node.

**Expected:** ratification is a review the user does when they choose. It is not a gate.

**Pass criteria:** a task whose `decision_dependencies` names a `recorded` record routes normally; the phase gate is offered and can be approved with records unratified; the gate summary states how many there are; the ratify row is the only place the user is asked to act on them.

## Trace E — `/work ratify all`

Command path: `commands/work.md` (sub-mode `/work ratify`) → `rules/spec-workflow.md § "Direct edits to spec, decision, and vision files"` (infrastructure operations) → dashboard regen.

State: DEC-006 and DEC-007 are `recorded` (`decided_by: implement-agent`, `decided: 2026-10-06`). Today is 2026-10-07.

1. The user runs `/work ratify all`.
2. For each `recorded` record the orchestrator edits frontmatter only: `status: approved`, new key `ratified: 2026-10-07`. `decided_by` and `decided` are unchanged, and the body is untouched. The DEC-016 `permissions.ask` prompt fires on the first edit (once per session with "Yes, don't ask again").
3. The dashboard is regenerated: the ratify row is gone, both records show as "Decided", META has `decisions_recorded: 0` and `decisions_approved` two higher.

Variant, `/work ratify DEC-006`: only DEC-006 changes. The row now reads `1 agent decision awaits ratification: DEC-007 — run /work ratify all (or /work ratify DEC-NNN)`.

Variant, a named record that is not `recorded` (`/work ratify DEC-002`, already `approved`): it is not changed and gets no `ratified` key.

**Expected:** `approved` on an agent's decision now means the user said so, on a known date, and the record still says who made the choice.

**Pass criteria:** `status: approved` and `ratified: <today>` on every ratified record; `decided_by` unchanged; no body edit; no `## Select an Option` section added; the row disappears at zero and shrinks otherwise; only `recorded` records are affected.

## Trace F — `/work reconsider DEC-NNN`

Command path: `commands/work.md` (sub-mode `/work reconsider`) → `commands/research.md` Step 1 (decision ID provided).

State: DEC-007 "Cache layer for the stats job" is `recorded` (Task 16, Finished). DEC-006 is `recorded` too.

1. The user runs `/work reconsider DEC-007`.
2. Frontmatter only: `status: proposed`. DEC-007 was written by v5.11.0, so it has no `## Select an Option` section and nothing else is edited. Task 16 stays Finished and its verification stands.
3. The dashboard is regenerated. DEC-007 is now an unresolved decision: it has its own Decisions row on the Needs-you card and shows as "Pending". The ratify row lists DEC-006 only.
4. `/work` points the user at `/research DEC-007`.
5. `/research DEC-007`: the record is `proposed` and has no `## Select an Option` section, so `/research` inserts the template sections it lacks (`## Select an Option` under the title with one unchecked box per option the record names; empty `## Option Details` and `## Your Notes & Constraints`), leaves `## Decision` as written, and dispatches research-agent.
6. The user later ticks a box; `/work` Step 2b (or `/iterate` Step 1a) approves the decision as for any other and, because the record has `decided_by: implement-agent`, also adds `ratified: <today>`; `decided_by` stays. The Post-Decision Check then compares the selection with what was built: if it differs, a new task is offered and, when created, its id is appended to DEC-007's `related.tasks` after 16; Task 16 is not reopened. `/review` then flags DEC-007 while the new task is unfinished and stops when it is Finished; DEC-006 is never flagged, whether still `recorded` or ratified with `/work ratify`. If the new task finishes with held choices, "Persist decisions" writes a new record for it: DEC-007's first id is 16, so it is not a match.

Variant, `/research DEC-006` while it is still `recorded`: `/research` says it is an agent-recorded decision that is already built and verified, and asks `[Y] Reconsider and research | [N] Leave as recorded`. `[Y]` sets `status: proposed` and continues as steps 5–6; `[N]` changes nothing.

Variant, legacy record with a self-ticked box: DEC-003 was written by an older version with a `## Select an Option` section whose box the agent ticked, and `/health-check` flipped it to `recorded` (Trace G). `/work reconsider DEC-003` sets `status: proposed` and, in the same edit, unticks that box and says so. The next `/work` Step 2b and `/iterate` Step 1a find no ticked box, so DEC-003 stays `proposed` until the user ticks one. Without the untick it would become `approved` on the next run with no user selection. `/research DEC-003` → `[Y]` does the same.

Variant, `/research` with no argument: auto-detect still scans `draft`/`proposed` only. DEC-006 (`recorded`) is not offered; DEC-007 (`proposed`) is.

**Expected:** reconsidering turns an agent's choice into an ordinary open decision with the usual research and selection path, without undoing verified work.

**Pass criteria:** `status: proposed` after reconsider; a box the agent ticked is unticked in the same edit and reported, and no run approves the record before the user ticks one; the user's tick gives `approved` plus `ratified`, with `decided_by` unchanged; the follow-up-task offer is made from `/work` and from `/iterate`, and a created follow-up task's id is appended to the record's `related.tasks`; `/review` flags the reconsidered record only until the follow-up is Finished; the follow-up's own choices get their own record; the task stays Finished; the record is listed as unresolved and leaves the ratify row; `/research DEC-NNN` is suggested; `/research` on a `recorded` record confirms before changing anything; auto-detect ignores `recorded`.

## Trace G — `/health-check` Part 3 on a project with legacy agent-approved records

Command path: `commands/health-check.md § "Part 3: Decision System Validation"` (checks 1, 4, 7; Decision Auto-Fixes) → `§ "Fix Queue Protocol"` → Step 4 (Batch Fix Triage).

State: a project upgraded to v5.11.0. Its records:
- DEC-002, DEC-003, DEC-005: `status: approved`, `decided_by: implement-agent`, no `ratified` key.
- DEC-004: `status: implemented`, `decided_by: implement-agent`, no `ratified` key, anchors present.
- DEC-005's body has a `## Selected` heading and no `## Decision`.
- DEC-001: `status: approved`, no `decided_by` (the user ticked its box).
- DEC-006: `status: recorded`, written by v5.11.0 (headings as in Trace C).
- The dashboard is fresh and nothing else is wrong.

1. Check 1: `recorded` is a valid status. DEC-006 raises nothing.
2. Check 4: DEC-006 has a non-empty `## Decision` and an option in `## Options Comparison`, so it passes; its missing `## Select an Option` is not a finding. DEC-005 has `## Selected` and no `## Decision`: the rename row is queued instead of an "incomplete" report.
3. Check 7: four records match (DEC-002, DEC-003, DEC-004, DEC-005). DEC-001 doesn't (no `decided_by`), nor does DEC-006 (`recorded`: the dashboard's ratify row covers it). One row is queued for the project.
4. Step 4 shows one table and takes one response:
   ```
   | # | Part | File | Proposed fix | Risk |
   |---|------|------|--------------|------|
   | 1 | 3 | .claude/support/decisions/ | 4 decisions were approved by an agent, never ratified: DEC-002, DEC-003, DEC-004, DEC-005 — reply "1: ratified / recorded / keep" (`recorded` skips the 1 `implemented`) | needs-input |
   | 2 | 3 | decision-005-*.md | Rename heading `## Selected` → `## Decision` | ⚠ edits decision record |
   ```
5. The user replies `A`. Neither row applies: both are listed back as still open. No decision file changes.

Variant, `1: ratified`: each of the four gains `ratified: <today>`; statuses are unchanged (DEC-004 stays `implemented`). The row doesn't return on the next run.

Variant, `1: recorded`: DEC-002, DEC-003 and DEC-005 (`approved`) get `status: recorded`; the dashboard is regenerated and its ratify row lists them with DEC-006 (four ids). `/work ratify all` then finishes the job (Trace E). DEC-004 is `implemented` and is not flipped: ratifying it from `recorded` would leave it `approved`, a downgrade. On the next run the row returns for DEC-004 alone, offering `ratified / keep`.

Variant, `1: keep`, or no answer: nothing changes, and the row returns on the next run.

Variant, `A include 2`: DEC-005's heading line becomes `## Decision`; the text under it is untouched.

Applying either row edits a decision record, so the DEC-016 `permissions.ask` prompt fires.

**Expected:** decisions the user never saw are put in front of them once per run, as one row, with the choice left to them. Nothing is ratified or relabelled by default.

**Pass criteria:** `recorded` passes checks 1 and 4 without `## Select an Option`; exactly one legacy row per project, with the count and ids; the legacy row is `needs-input` with `ratified / recorded / keep`, and unanswered means keep; `recorded` never changes an `implemented` record, which is offered `ratified / keep` only and keeps its status either way; one rename row per affected record, flagged `⚠ edits decision record`; bare `[A]` applies neither; a user-approved record and a `recorded` record are not counted as legacy.

## Invariant checks

- No decision file is written for an agent's choice before the task's verification passes. Between implementation and the pass, the choices live only in the task's `decisions_pending`.
- `decisions_pending` always equals the latest implement report's non-trivial set: each report replaces it, an empty set removes it, and the pass removes it.
- One record per task per pass, however many choices it made. A reworked task whose choices are unchanged gets no second record; changed choices get a new record that links the old one and supersedes it while it is still `recorded`. Trivial choices are `[CHOICE]` notes and never records.
- An agent's record is born `recorded`. It becomes `approved` only by the user's `/work ratify`, or by the user ticking a box after it was reconsidered (`/work` Step 2b or `/iterate` Step 1a); both add `ratified`. A box the agent ticked never approves it: reconsider unticks it. `decided_by` never changes.
- An agent-recorded record has no `## Select an Option` section unless it has been reconsidered.
- `recorded` is resolved for `decision_dependencies`, Step 1d and phase gates, and is not counted as decided. A new record's id is never added to any task's `decision_dependencies`.
- The dashboard carries exactly one ratify row for the whole project while any record is `recorded`, and none otherwise. It is script-derived: never restated in `augment_rows[]`.
- Ratify and reconsider edit frontmatter only, except that reconsider unticks a box the agent ticked on an older record. Neither changes a task's status.
- `/health-check` never ratifies, flips or renames without an explicit answer or inclusion.
