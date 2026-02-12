# Scenario 07: Dashboard Communication and Feedback

Verify that the dashboard functions as a complete communication loop: Claude surfaces what it needs, the user acts, Claude picks up the result. Tests that feedback persists, decisions are detected, and stale state is caught.

## Context

The user runs Claude Code CLI in one pane and has `dashboard.md` open in the other. Their workflow: check dashboard, do what it says, run `/work`, check dashboard again. If any step breaks silently, the user loses trust in the system.

---

## Trace A: Complete attention-to-resolution loop

### State

- Task 7: "Awaiting Verification" — verify-agent will find issues
- Dashboard currently shows Task 7 as "In Progress"

### Expected sequence

1. Claude runs verify-agent, finds issues, creates fix tasks, regenerates dashboard
2. Dashboard updates: Task 7 back to "In Progress" (failed verification), new fix task appears, verification debt shown
3. Claude implements fix, re-verifies, passes
4. Dashboard updates: Task 7 "Finished", fix task "Finished", verification debt cleared

### Pass criteria

- [ ] Each state transition produces a dashboard regeneration
- [ ] Dashboard accurately reflects the current state at every step
- [ ] No "phantom" items remain from previous states
- [ ] The user can follow the entire lifecycle from the dashboard alone

### Fail indicators

- Dashboard shows stale status while work is happening
- Fix task appears before it exists
- Verification debt persists after task passes verification

---

## Trace B: Feedback written in dashboard survives regeneration

### State

- Task 11 (owner: both) needs user feedback
- Dashboard has an inline feedback area for Task 11
- User writes feedback in the dashboard

### Scenario

Before the user runs `/work complete`, something triggers a dashboard regeneration (e.g., a parallel agent finishes).

### Expected

- Feedback written in the dashboard is preserved across regeneration
- When `/work complete` runs, it captures the feedback before clearing the area
- Feedback is durably stored in the task JSON after completion

### Pass criteria

- [ ] Feedback areas in the dashboard have a preservation mechanism
- [ ] `/work complete` captures inline feedback before regenerating
- [ ] Feedback persists in task JSON after completion
- [ ] User is never silently losing feedback they wrote

### Fail indicators

- User writes feedback, dashboard regenerates, feedback disappears
- No mechanism exists to capture inline feedback before regeneration
- Feedback written but never captured in any durable location

---

## Trace C: Decision resolution detection

### State

- DEC-002: proposed, blocks tasks 8-9
- User opens decision doc, reviews options, checks a selection box

### Expected

1. Next `/work` run detects the checked box in the decision doc
2. Decision frontmatter auto-updated (status, decided date)
3. If inflection point: `/work` pauses and directs to `/iterate`
4. If pick-and-go: dependent tasks unblocked immediately
5. Dashboard updated — decision moves from Action Required to resolved

### Pass criteria

- [ ] Checking a box in the decision doc is sufficient to resolve it
- [ ] Next `/work` run detects and acts on the change
- [ ] Dashboard reflects the resolution
- [ ] Decision frontmatter status updated (not left permanently stale)

### Fail indicators

- User checks box but `/work` doesn't detect it
- Decision shown as resolved but dependent tasks still blocked
- Frontmatter status stays "proposed" permanently

---

## Trace D: Stale dashboard detection

### State

- User manually edits a task JSON file without running `/work`
- Dashboard META block hash is now stale

### Expected

- Next `/work` run detects hash mismatch and regenerates the dashboard
- Dashboard now reflects the manual edit
- Dashboard header includes a staleness note for when viewed without running `/work`

### Pass criteria

- [ ] Dashboard META block hash enables staleness detection
- [ ] `/work` catches mismatch and regenerates
- [ ] After regeneration, dashboard matches actual file state

### Fail indicators

- Dashboard shows stale data indefinitely
- `/work` doesn't regenerate despite mismatch
- Manual edits to task JSON lost on regeneration (dashboard is NOT source of truth)

---

## Trace E: Multi-session feedback continuity

### State

- Session 1: User writes feedback for a task in a durable location (dashboard notes, questions.md, decision doc)
- Session ends
- Session 2: User runs `/work`

### Expected

- Feedback persists across sessions (file-based, not conversation memory)
- `/work` or `/work complete` reads feedback from its durable location
- Claude incorporates feedback when continuing work
- No conversation-state dependency for feedback

### Pass criteria

- [ ] Feedback mechanism is file-based (survives session boundaries)
- [ ] Feedback written in Session 1 is available in Session 2
- [ ] No conversation-state dependency for feedback

### Fail indicators

- Feedback relies on conversation context (lost between sessions)
- User has to re-state feedback in the new session

---

## Trace F: Out-of-spec recommendation feedback

### State

- Task 15 finished, verify-agent created 2 out-of-spec recommendations
- User needs to Accept, Reject, or Defer each

### Expected

- Dashboard presents recommendations with enough context to decide
- Each recommendation links to relevant files
- User's choice (Accept/Reject/Defer) is recorded
- Rejected recommendations leave a trace (not silently deleted)

### Pass criteria

- [ ] Recommendations presented with context in the dashboard
- [ ] Each links to the source file
- [ ] User's choice is recorded
- [ ] Rejected items leave a record (not silently deleted)

### Fail indicators

- Recommendations presented without context
- Rejected tasks deleted with no record
- Accept/Reject is CLI-only with no dashboard trace
