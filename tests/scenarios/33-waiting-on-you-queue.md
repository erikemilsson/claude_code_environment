# Scenario 33: Waiting-on-You Queue (human-gated coverage invariant)

Verify that `/work` Step 0g and the `/work pause` open-question sweep (shipped v4.14.0) keep every user-gated item visible as a dashboard Action Required row — never buried solely in handoff prose.

## Context

Observed failure mode (styler, 2026-06-10 analysis): two decisions sat "paused mid-decision (unanswered)" inside a 7.8KB handoff blob and 5 On Hold tasks awaited the user with no consolidated surface. The invariant: anything blocked on the user must have a 🚨 Action Required row with the concrete question inline; `/work` prints the queue at session start (Step 0g) and sweeps it at pause.

## State (Base)

- Task 12: `owner: "human"`, Pending, all dependencies Finished ("Provide production API key")
- Task 15: `owner: "both"`, Finished, `user_review_pending: true` (UI review outstanding)
- Task 18: On Hold (user paused it two sessions ago)
- DEC-007: status `proposed` (two options populated, none selected)
- Mid-session, Claude asked "Should increment 2 use approach A or B?" — the user never answered
- User runs `/work pause`

---

## Trace 33A: Pause sweep writes Action Required rows before the handoff

- **Path:** `/work pause` → Context Transition key rules → open-question sweep

### Expected

- Before the handoff file is written, the sweep enumerates: Task 12, Task 15, Task 18, DEC-007, and the unanswered A-or-B question
- Each gets a 🚨 Action Required row with the concrete question/action inline (targeted-edit path allowed; `pending_full_regen` sentinel set)
- The handoff references those rows; the A-or-B question does NOT exist only in handoff prose

### Pass criteria

- [ ] All 5 items have Action Required rows with inline questions/actions
- [ ] Rows satisfy the Action Item Contract (actionable, linked, completable)
- [ ] Sentinel set if targeted edits were used
- [ ] Handoff points at rows rather than being the sole carrier

### Fail indicators

- The unanswered question appears only in `session_knowledge` / handoff prose
- On Hold task or proposed decision missing from Action Required
- Full dashboard regen forced when a targeted edit would do

---

## Trace 33B: Next session start prints the queue

- **Path:** next `/work` → Step 0g (always runs)

### Expected

- Output contains `Waiting on you (5):` with one line per item — concrete question/action + file link
- Printed before any routing (Step 1 onward); merged with Step 0c output on a clean start
- Dashboard cross-check finds the rows from 33A present — no additions needed

### Pass criteria

- [ ] Queue printed before routing, N == 5
- [ ] Each line carries the question/action, not just a title
- [ ] Cross-check is a no-op when rows already exist

### Fail indicators

- Routing begins (agent dispatched) before the queue is shown
- Queue lists titles without the concrete questions
- Items found in scan but missing dashboard rows are left missing

---

## Trace 33C: Empty queue stays silent

- **Path:** `/work` Step 0g with no user-gated items

### State (delta)

All tasks `owner: "claude"`, no On Hold, all decisions resolved, no handoff.

### Expected

- Step 0g produces NO output block (skip entirely when N == 0) — no "Waiting on you (0)" noise

### Pass criteria

- [ ] No queue block in session-start output
- [ ] No dashboard edits made by the cross-check

### Fail indicators

- "Waiting on you (0):" or an empty section printed
- Action Required rows invented for non-gated items
