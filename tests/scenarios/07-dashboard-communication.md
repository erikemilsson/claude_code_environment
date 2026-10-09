# Scenario 07: Dashboard Communication and Feedback

Verify that the dashboard functions as a complete communication loop: Claude surfaces what it needs, the user acts, Claude picks up the result. Tests that feedback persists, decisions are detected, and stale state is caught.

## Context

The user runs Claude Code CLI in one pane and has `dashboard.html` open in a browser in the other. Their workflow: check dashboard, do what it says, run `/work`, check dashboard again. If any step breaks silently, the user loses trust in the system.

---

## Trace A: Complete attention-to-resolution loop

### State

- Task 7: "Awaiting Verification" — verify-agent will find issues
- Dashboard was last regenerated while Task 7 was "In Progress" (it counts under "In Progress" in the status legend; the HTML has no per-task status row)

### Expected sequence

1. Claude runs verify-agent, finds issues; Task 7 goes back to "In Progress" with a `[VERIFICATION FAIL #1]` note (a per-task fail creates no fix task: `work-procedures.md § "State Persistence Protocol"`, "After verify-agent returns (per-task mode)" step 4), regenerates dashboard
2. Dashboard updates: Task 7 still counts under "In Progress"; it has no Verification Debt row, because a task under rework is not debt (debt is a task Awaiting Verification, or Finished without a pass)
3. Claude implements fix, re-verifies, passes
4. Dashboard updates: Task 7 counts under "Finished" and is listed in "Recent — last 7 days"; verification debt 0; footer `spec aligned · 0 drift deferrals, 0 verification debt`

### Pass criteria

- [ ] Each state transition produces a dashboard regeneration
- [ ] Dashboard accurately reflects the current state at every step
- [ ] No "phantom" items remain from previous states
- [ ] The user can follow the lifecycle from the dashboard's counts (status legend, verification debt, Recent)

### Fail indicators

- Dashboard shows stale status while work is happening
- A Verification Debt row for Task 7 while it is being reworked
- Verification debt persists after task passes verification

---

## Trace B: Feedback given at `/work complete` survives regeneration

- **Path:** `/work complete 11` → `work-procedures.md § "Task Completion (/work complete)"` step 3c

### State

- Task 11 (owner: both) is Finished with `user_review_pending: true`; its `user_feedback` already holds one dated entry from an earlier guided-testing round
- The dashboard is read-only generated HTML (DEC-024): it has no feedback area and no `FEEDBACK:{id}` markers
- `template_inbox_path` is not configured

### Scenario

The user has a remark about Task 11. A parallel agent finishes and the dashboard is regenerated before the user runs `/work complete 11`.

### Expected

- Nothing the user wrote lived in the dashboard, so the regeneration loses nothing
- `/work complete 11` asks the project-notes prompt (always shown); the template-notes prompt is not shown, because there is no inbox to send it to
- The answer is prepended to the task's `user_feedback` as a dated entry; the earlier entry stays below it
- No step reads the dashboard for feedback
- The dashboard regenerated at the end of `/work complete` no longer shows Task 11's review row

Variant, inbox configured: both prompts are shown, each skippable with Enter; a template note becomes an `FB-NNN` entry through `/feedback template:`.

### Pass criteria

- [ ] The two prompts are the only feedback path in `/work complete`
- [ ] Feedback is stored in the task JSON (`user_feedback`), dated, newest first
- [ ] An earlier `user_feedback` entry is not overwritten
- [ ] A dashboard regeneration at any point changes nothing the user said

### Fail indicators

- `/work complete` looking for feedback markers in `dashboard.html`
- The new entry replacing the earlier guided-testing entry
- The template-notes prompt shown with no `template_inbox_path`
- Feedback kept only in the conversation

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
5. Dashboard updated — DEC-002's row leaves the Needs-you card's Decisions sub-section; the Decisions card shows it as "Decided" with the selected option; Phase 3 no longer reads `Blocked (DEC-002)`

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
- The page has no staleness banner: a reader viewing it without running `/work` has the footer's `generated {timestamp}` and `state of record = task JSON`
- An edit that only sets or clears `user_review_pending` also counts: the hash rows carry a `review` field

### Pass criteria

- [ ] Dashboard META block hash enables staleness detection
- [ ] `/work` catches mismatch and regenerates
- [ ] After regeneration, dashboard matches actual file state
- [ ] Clearing a review flag by hand removes the task's review row on the next `/work`

### Fail indicators

- Dashboard shows stale data indefinitely
- `/work` doesn't regenerate despite mismatch
- Manual edits to task JSON lost on regeneration (dashboard is NOT source of truth)

---

## Trace E: Multi-session feedback continuity

### State

- Session 1: User gives feedback for a task in a durable location: at `/work complete` (the task's `user_feedback`), as a note they ask Claude to add (sidecar `user_notes`, shown on the read-only Notes card), or in a decision doc
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

- Dashboard lists each pending recommendation under Needs you → Reviews: `{id} {title} — out-of-spec task awaiting your approval → run /work` (task id, title and command; no file link)
- `/work` presents them with `[A]` Accept / `[R]` Reject / `[D]` Defer / `[AA]` Accept all (`work-user-flows.md § "Out-of-Spec Task Approval"`); the choice is made in the CLI, not in the dashboard
- User's choice is recorded in the task JSON: `out_of_spec_approved: true`, or `out_of_spec_rejected: true` with the optional `rejection_reason`; a deferred task keeps its Reviews row
- Rejected recommendations leave a trace (archived to `.claude/tasks/archive/`, not silently deleted)

### Pass criteria

- [ ] Each pending recommendation has a Reviews row naming the task and the command
- [ ] An accepted or rejected recommendation has no Reviews row after the next regeneration
- [ ] User's choice is recorded
- [ ] Rejected items leave a record (not silently deleted)

### Fail indicators

- A pending recommendation missing from Reviews
- Rejected tasks deleted with no record
- An accepted or rejected recommendation still listed under Reviews
