# Session Recovery

Procedure for detecting and recovering tasks left in inconsistent states by a previous session. Run as `/work` Step 0.

---

## Session Sentinel

A lightweight file at `.claude/tasks/.last-clean-exit.json` tracks whether the previous `/work` session ended cleanly.

**Schema:**
```json
{
  "timestamp": "2026-01-28T14:30:00Z",
  "task_count": 15,
  "in_progress_tasks": ["5", "8"]
}
```

**Written by:** `/work` at the end of a successful run (after Step 5).
**Read by:** `/work` at the start of Step 0.

### Fast-Path: Skip Recovery Scan

```
1. Read .claude/tasks/.last-clean-exit.json
2. IF file exists AND timestamp is within last 24 hours:
   → Skip full recovery scan
   → Only check the specific tasks listed in in_progress_tasks
     (verify they're still in expected states)
   → Proceed to Step 1
3. IF file missing OR stale (>24h):
   → Run full recovery scan below
```

---

## Full Recovery Scan

Scan all non-archived `task-*.json` files and check for recoverable states.

**Newest state tag.** Cases 2–5 match on a task's newest state tag: the first of `[BLOCKED]`, `[AGENT TIMEOUT]`, `[VERIFICATION TIMEOUT]`, `[VERIFICATION ESCALATED]`, `[VERIFICATION FAIL #N]`, `[PARTIAL]` and `[PARTIAL_RESUME_PENDING]` found in `notes`, reading from the start. Notes are newest first and keep old tags, so a tag further down is history, not the task's current state.

```
1. STATUS: "Awaiting Verification"
   (Agent crashed after implementation, before verification completed)

   → Auto-recover: spawn verify-agent for this task. If the task carries
     drift_reverify, the brief adds the line "Re-verification after a spec edit:
     the implementation is unchanged; check it against the current section text."
   → Log: "⚡ Recovering task {id} — spawning verification (previous session incomplete)"
   → Continue to Step 1 after recovery spawns complete

2. STATUS: "Blocked" WITH newest state tag "[VERIFICATION TIMEOUT]"
   AND verification_attempts < 3
   (Verify-agent twice returned no valid report — implementation is done, verification needs retry)

   → Auto-recover: set status to "Awaiting Verification", spawn verify-agent with an extended turn budget (up from 30) in its dispatch prompt: `Turn budget: about 40 tool calls. If you get close, follow verify-agent.md § Turn Budget Protocol (result "fail", unfinished checks "skipped").` A task carrying drift_reverify also gets Case 1's re-verification line.
   → Log: "⚡ Retrying verification for task {id} with extended turn limit"

3. STATUS: "Blocked" WITH newest state tag "[VERIFICATION TIMEOUT]"
   AND verification_attempts >= 3
   (Verify-agent failed 3 times — needs human review)

   → Prepend note: "[VERIFICATION ESCALATED] 3 verification attempts exhausted — requires human review"
   → Log: "Task {id} escalated to human review after 3 failed verification attempts"

4. STATUS: "Blocked" WITH newest state tag "[AGENT TIMEOUT]"
   (Parallel agent timed out — task may be too complex or need breakdown)

   → Present to user:
   │  Task {id} "{title}" timed out in a previous session.
   │  [R] Retry (set to Pending for next dispatch)
   │  [B] Break down (run /breakdown {id})
   │  [S] Skip (stays Blocked)

5. STATUS: "Blocked" WITH newest state tag "[VERIFICATION ESCALATED]"
   (Intentional escalation — already surfaced, no auto-action)

   → Report only: "Task {id} awaiting human review (3 verification attempts exhausted)"

6. STATUS: "In Progress" WITH updated_date older than 24 hours
   AND no agent currently running for this task
   (Abandoned by a crashed implement-agent)

   → Present to user:
   │  Task {id} "{title}" has been In Progress for {N} days without activity.
   │  [C] Continue (keep In Progress, /work will route to implement-agent)
   │  [P] Reset to Pending (start fresh)
   │  [H] Put On Hold

7. STATUS: "Finished" WITH non-empty decisions_pending
   (Crashed between the verify pass and the decision-record write)

   → Handled by work.md Step 0g item 1, which runs on every /work (this scan
     is skipped after a clean exit). Nothing more to do here.
```

**After recovery actions complete, proceed to Step 1.**

**Recovery verifications take turns.** Cases 1 and 2 can match several tasks at once. Dispatch their verify-agents as `parallel-execution.md § "Single-Instance Resources"` says: a verification that needs the browser or runs the build goes one at a time, each after the previous one's after-return steps; the others may run together. Every dispatch follows `work.md § "Before Any Dispatch"`, and two or more at once also get the pre-flight checks of `parallel-execution.md § "Pre-Dispatch Confirmation"`.

**Note:** Cases 1 and 2 are auto-recovered because the implementation is already done — we only need to run verification. Cases 4 and 6 present options because the implementation state is uncertain.

## Residue From a Previous Session

An agent the previous session lost (a limit cutoff, a crash, a closed terminal) stopped nothing and removed nothing. Only on the full-scan path (the sentinel is missing or stale, so the session did not end cleanly), when the scan matches case 1, 2, 4 or 6, run the Residue check once, before any recovery dispatch (`work-procedures.md § "Residue check"`). No baseline survives from that session, so it only reports, as "When the check only reports" there defines: evidence-shaped files in the project root and listeners whose working directory is inside the project, left to the user. Nothing is moved or stopped. The fast path skips this: after a clean exit, In Progress tasks are a normal pause, not a lost agent.

**Malformed files during scan:** If a task file fails to parse during Step 0, skip it and continue scanning other files. The malformed file will be reported in Step 1 (see work.md "Malformed task file handling").
