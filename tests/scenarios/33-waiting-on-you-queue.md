# Scenario 33: Waiting-on-You Queue (human-gated coverage invariant)

Verify that `/work` Step 0g and the `/work pause` open-question sweep (shipped v4.14.0) keep every user-gated item visible as a dashboard Action Required row — never buried solely in handoff prose. Since FB-118 the script derives review rows for any owner and Blocked rows for human/both-owned or escalated tasks, and judgment rows persist in sidecar `augment_rows[]`.

## Context

Observed failure mode (styler, 2026-06-10 analysis): two decisions sat "paused mid-decision (unanswered)" inside a 7.8KB handoff blob and 5 On Hold tasks awaited the user with no consolidated surface. The invariant: anything blocked on the user must have a 🚨 Action Required row with the concrete question inline; `/work` prints the queue at session start (Step 0g) and sweeps it at pause.

FB-118 (three projects): review flags on Finished or claude-owned tasks, and Blocked tasks waiting on a user choice, got no row; the hand-inserted rows covering them were wiped by every regen.

## State (Base)

- Task 12: `owner: "human"`, Pending, all dependencies Finished ("Provide production API key")
- Task 15: `owner: "both"`, Finished, `user_review_pending: true` (UI review outstanding)
- Task 18: On Hold (user paused it two sessions ago)
- Task 20: `owner: "claude"`, Finished, `user_review_pending: true` (runtime validation was partial; a `test_protocol` awaits the user)
- Task 21: `owner: "both"`, Blocked — Claude needs the user's export-format choice (X or Y)
- DEC-007: status `proposed` (two options populated, none selected)
- Mid-session, Claude asked "Should increment 2 use approach A or B?" — the user never answered
- User runs `/work pause`

---

## Trace 33A: Pause sweep puts every item on the card before the handoff

- **Path:** `/work pause` → Context Transition key rules → open-question sweep → `dashboard-regeneration.md § "Augment Rows"`

### Expected

- Before the handoff file is written, the sweep enumerates 7 items: Task 12, Task 15, Task 18, Task 20, Task 21, DEC-007, and the unanswered A-or-B question
- Script-derived, no LLM writing: Your Tasks — Task 12 (yours to do), Task 15 and Task 20 (review, `/work complete {id}`; Finished status and `owner: "claude"` don't hide them), Task 18 (On Hold), Task 21 (Blocked, owner `both`); Decisions — DEC-007
- Judgment rows go to sidecar `augment_rows[]`: the A-or-B question, and Task 21's X-or-Y choice (`task_id: "21"`, text naming task 21). Each carries the concrete question and a command (e.g. "answer at the next `/work`")
- One full regen after the sidecar write; the card ends with "Also Needs You" holding both rows
- The handoff's `open_question_refs` point at those rows; the A-or-B question does NOT exist only in handoff prose

### Pass criteria

- [ ] All 7 items have Action Required rows with inline questions/actions
- [ ] Rows satisfy the Action Item Contract (actionable, linked, completable)
- [ ] Judgment rows written to `augment_rows[]` before the regen; `dashboard.html` not edited after the script's output is written
- [ ] Handoff points at rows rather than being the sole carrier

### Fail indicators

- The unanswered question appears only in `session_knowledge` / handoff prose
- Task 20 or Task 21 missing from Your Tasks (the FB-118 derivation gaps)
- On Hold task or proposed decision missing from Action Required
- An `<li>` hand-inserted into `dashboard.html` (the next regen wipes it)
- A script-derived row restated in `augment_rows[]`

---

## Trace 33B: Next session start prints the queue

- **Path:** next `/work` → Step 0g (always runs)

### Expected

- Output contains `Waiting on you (7):` with one line per item — concrete question/action + file link (Task 21's line carries the X-or-Y question)
- Printed before any routing (Step 1 onward); merged with Step 0c output on a clean start
- Dashboard cross-check finds the rows from 33A present, including both `augment_rows[]` entries — no additions needed

### Pass criteria

- [ ] Queue printed before routing, N == 7
- [ ] Each line carries the question/action, not just a title
- [ ] Cross-check is a no-op when rows already exist (no sidecar write, no regen)

### Fail indicators

- Routing begins (agent dispatched) before the queue is shown
- Queue lists titles without the concrete questions
- Items found in scan but missing dashboard rows are left missing

---

## Trace 33C: Empty queue stays silent

- **Path:** `/work` Step 0g with no user-gated items

### State (delta)

All tasks `owner: "claude"`, none Blocked, On Hold or flagged `user_review_pending`; all decisions resolved; sidecar `augment_rows` empty; no handoff.

### Expected

- Step 0g produces NO output block (skip entirely when N == 0) — no "Waiting on you (0)" noise

### Pass criteria

- [ ] No queue block in session-start output
- [ ] The cross-check writes nothing (no `augment_rows` change, no regen)

### Fail indicators

- "Waiting on you (0):" or an empty section printed
- Action Required rows invented for non-gated items

---

## Trace 33D: Judgment rows survive regens and expire with their task

- **Path:** Tier-1 regen → `dashboard-regeneration.md` Step 2 → `dashboard-render.py --html`; § "Augment Rows"

### State (delta)

Continuing from 33B. A parallel batch ends (Tier-1 regen). The user then answers both questions (approach A; format X); the orchestrator prunes the A-or-B row but misses the Task 21 row. Task 21 is unblocked, implemented and verified (Finished; as a `both` task it gets the review flag), and the user closes its review with `/work complete 21` (Finished, flag cleared).

### Expected

- The batch-end regen re-renders both "Also Needs You" rows unchanged; nobody re-authors them
- The pruned A-or-B row is gone after the next regen
- The Task 21 row still renders while Task 21's review is open, then expires: once `/work complete 21` leaves it Finished without `user_review_pending`, the renderer skips it, with no HTML edit

### Pass criteria

- [ ] Rows identical before and after the intervening regen
- [ ] Answered row pruned from the sidecar
- [ ] Expired row absent from the card even though it is still in the sidecar

### Fail indicators

- Rows re-extracted from the previous HTML and re-injected (the FB-118 failure)
- The answered Task 21 choice still listed after Task 21's review closed

---

## Trace 33E: An open review holds back Verification Pending

- **Path:** `dashboard-render.py --html` → Verification Pending gate (`dashboard-regeneration.md § "Section Display Rules"`)

### State (delta)

Every task Finished with passing per-task verification; Task 15 still `user_review_pending: true`; no `verification-result.json`.

### Expected

- Your Tasks lists Task 15's review row (`/work complete 15`); no Verification Pending row
- `/work complete 15` clears the flag and regenerates: Verification Pending appears. Clearing the flag by hand instead changes `task_hash` (its `review` field), so the next freshness check regenerates

### Pass criteria

- [ ] Verification Pending absent while any review flag is set
- [ ] Clearing only the flag makes the dashboard read stale

### Fail indicators

- The card says phase-level verification will run on next `/work` while the user's review is still open
- Task 15's review row missing because its status is Finished
