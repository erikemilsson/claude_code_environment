# /work User-Interaction Flows

<!-- Loaded on demand by commands/work.md: read only when the trigger line in /work points here. -->

Flows `/work` runs when a task needs the user: choosing the channel, guided testing, CLI-direct review, and approving out-of-spec tasks.

## Interaction Mode Selection

When a task involves human action (owner `"human"` or `"both"`, or `user_review_pending`), Claude should select the interaction channel that minimizes friction. This is a judgment call, not a rigid rule.

| Factor | Dashboard-mediated | CLI-direct |
|--------|-------------------|------------|
| Timing | User will do it later (async) | User should do it now (synchronous) |
| Duration | Extended (reading docs, thinking through decisions) | Quick (run a command, confirm output, yes/no) |
| Terminal needed? | No | Yes — commands to run, output to check |
| Multiple items | Batch of unrelated items | Single focused task |
| Interaction type | Passive review (read, think, decide) | Active testing (run, observe, respond) |

**Scenario examples:**
- Test a CLI/TUI → `cli_direct` (run commands, observe output)
- Test a web UI → `cli_direct` (Playwright screenshots, visual confirmation)
- Review a long document → `dashboard` (user needs reading time)
- Make a design decision → `dashboard` (user weighs options)
- Configure API keys → `cli_direct` (Claude guides step by step)
- Phase gate approval → `dashboard` (user reviews overall progress)
- Quick confirmation → `cli_direct` (2-second yes/no)

The `interaction_hint` is set by verify-agent during Step T4b/T7. `/work` respects the hint but users can always override by using `/work complete {id}` from the dashboard flow.

## After a Per-Task Pass with `user_review_pending`

**Interaction mode routing (after per-task verification pass):**

When a task passes verification and has `user_review_pending: true` (set for `owner: "both"` tasks AND any task with a `test_protocol`), check for an `interaction_hint` field:

| `interaction_hint` | Routing |
|--------------------|---------|
| `"cli_direct"` | Present the task for guided testing or confirmation directly in the CLI conversation (see Guided Testing Flow below). Do NOT wait for the user to discover it in the dashboard. |
| `"dashboard"` or absent | Existing flow — task appears in dashboard "Your Tasks" / "Action Required". User reviews asynchronously. |

**Guided Testing Flow (CLI-direct with test_protocol):**

When a task has `interaction_hint: "cli_direct"` AND a `test_protocol`, present the testing flow immediately:

```
Task {id}: "{title}" — guided testing ({estimated_time})

{automated_results}

Step 1/{N}: {instruction}
  Expected: {expected}
  [R] Run command  [S] Skip  [P] Pass  [F] Fail
  (Available options depend on step type — "command" shows [R], others show [P]/[F])

Step 2/{N}: {instruction}
  Expected: {expected}
  [P] Pass  [S] Skip  [F] Fail

Guided testing complete: {passed}/{total} passed
```

**Step type handling:**
- `"command"` steps: Offer `[R]` Run — execute the command via Bash and show output. Then ask `[P]` Pass / `[F]` Fail based on the output.
- `"interactive"` steps: Show instruction and expected result. User tests manually, then signals `[P]` Pass / `[F]` Fail.
- `"visual"` steps: If a screenshot is available (e.g., from Playwright), show it. Otherwise, show instruction. User confirms `[P]` Pass / `[F]` Fail.

**After guided testing:**
- All steps passed or skipped → clear `user_review_pending`, continue auto-continuation
- Any step failed → write the round to the task's `user_feedback` as one entry, `Guided testing: step {n} failed: {what the user reported}` for each failed step, clear `user_review_pending` (a leftover flag on reworked work would let `/work complete` accept it as verified; re-verification sets the flag again), set task back to "In Progress" for fixes with `verification_attempts: 0` in the same write (`work-procedures.md § "State Persistence Protocol"`, "Reopening resets the counter"), route to implement-agent
- User can also provide freeform feedback at the end of the guided testing flow; it goes in the same entry (an entry of its own when no step failed)
- One entry per guided-testing round, written as `work-procedures.md § "State Persistence Protocol"` ("`user_feedback` is history too") defines: dated, prepended, never replacing earlier rounds, which the implement-agent fixing the task needs too.

**CLI-direct without test_protocol:**

When a task has `interaction_hint: "cli_direct"` but NO `test_protocol` (e.g., a quick confirmation), present the task inline:

```
Task {id}: "{title}" — ready for your review

{task description / notes summary}

[C] Complete  [F] Needs fixes (provide feedback)
```

`[F]` takes the failed-step path under "After guided testing": the feedback as one dated `user_feedback` entry, `user_review_pending` cleared, back to "In Progress" with the counter reset, then implement-agent.

## Out-of-Spec Task Approval

**Out-of-spec task handling:** After phase routing completes (or at phase boundaries), check for pending out-of-spec tasks: `[A]` Accept (sets `out_of_spec_approved: true`), `[R]` Reject, `[D]` Defer, `[AA]` Accept all. Never auto-execute out-of-spec tasks. Accepted out-of-spec tasks are routed to implement-agent → verify-agent like any other task.

**Reject behavior (`[R]`):**
1. Prompt for optional rejection reason
2. Set `out_of_spec_rejected: true` and `rejection_reason` (if provided) on task JSON
3. Move task file to `.claude/tasks/archive/`
4. Task preserved for audit trail but excluded from active processing and dashboard
