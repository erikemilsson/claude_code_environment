# Scenario 27: Verification Failure and Rework Cycle

Verify that per-task verification failure correctly routes back to implement-agent for fixes, and that the fail → fix → re-verify loop operates correctly including the 2-attempt re-verification limit.

## Context

Verification is not a rubber stamp. When verify-agent finds issues, the task must go back to implement-agent for fixes, then re-verify. This cycle is mandatory — a task cannot reach "Finished" without passing verification. After 2 failed re-verification attempts, the task escalates to human review. This scenario tests the full rework loop.

## State (Base)

- Phase 1: 3 tasks
  - Task 5: "Implement data pipeline" (owner: claude, status: "Awaiting Verification")
    - `files_affected: ["src/pipeline/extract.py", "src/pipeline/transform.py", "src/pipeline/load.py"]`
    - `notes: "Implemented ETL pipeline for 4 bronze tables"`
    - NO `task_verification` field yet
  - Task 6: "Build API layer" (owner: claude, status: "Pending", depends on [5])
  - Task 7: "Write pipeline tests" (owner: claude, status: "Pending", depends on [5])

---

## Trace 27A: First verification failure

- **Path:** verify-agent → Steps T1-T8; work.md → Step 3 routing algorithm

### Scenario

`/work` detects Task 5 in "Awaiting Verification" → routes to verify-agent per-task mode. verify-agent discovers that only 3 of 4 required bronze tables have upsert logic (spec requires 4).

### Expected

1. verify-agent Step T1: Reads task, spec section, completion notes
2. Steps T2-T5: Verifies files, spec alignment, quality, integration
3. Step T3 fails: spec says "upsert for 4 bronze tables", only 3 implemented
4. Step T6: Writes `task_verification` to task JSON:
   ```json
   {
     "task_verification": {
       "result": "fail",
       "checks": {
         "files_exist": "pass",
         "spec_alignment": "fail",
         "output_quality": "pass",
         "integration_ready": "pass"
       },
       "issues": [{
         "severity": "major",
         "description": "Missing upsert for raw_game_designers table"
       }]
     }
   }
   ```
5. Step T7: Task status set back to "In Progress"
   - `[VERIFICATION FAIL]` prepended to notes
   - `completion_date` cleared
6. Dashboard regenerated showing Task 5 back to "In Progress"

### Pass criteria

- [ ] verify-agent actually reads and evaluates files (not rubber-stamp)
- [ ] Spec alignment check catches the missing table
- [ ] `task_verification.result` is "fail" with specific issues
- [ ] Task status reverts to "In Progress" (not "Pending" or "Finished")
- [ ] `[VERIFICATION FAIL]` notes document what's wrong
- [ ] `completion_date` cleared
- [ ] Dashboard regenerated to reflect status change

### Fail indicators

- verify-agent passes the task despite missing implementation
- Task stays "Awaiting Verification" after failure (stuck state)
- Task goes to "Finished" despite spec_alignment fail
- Verification notes don't explain what to fix
- Dashboard not regenerated

---

## Trace 27B: Fix and re-verify (pass on second attempt)

- **Path:** `/work` → implement-agent (fix) → verify-agent (re-verify)

### Scenario

After 27A, `/work` detects Task 5 "In Progress" with `[VERIFICATION FAIL]` notes. Routes to implement-agent. implement-agent reads the failure notes, adds the missing 4th table upsert, then triggers re-verification.

### Expected

1. implement-agent reads `[VERIFICATION FAIL]` notes → understands what to fix
2. Step 4: Implements missing `raw_game_designers` upsert
3. Step 5: Self-review confirms all 4 tables now have upserts
4. Step 6a: Sets "Awaiting Verification" again
5. Step 6b: Triggers verify-agent
6. verify-agent re-verifies:
   - All 4 tables present → spec_alignment: pass
   - All checks pass
   - `task_verification.result: "pass"`
7. Step T7: Task status → "Finished"
8. Tasks 6 and 7 (which depend on Task 5) become eligible

### Pass criteria

- [ ] implement-agent reads and uses verification failure notes to guide fix
- [ ] Fix addresses the specific issue identified by verify-agent
- [ ] Task goes through full cycle: In Progress → Awaiting Verification → Finished
- [ ] verify-agent re-verifies with fresh eyes (not just checking the fix in isolation)
- [ ] Dependent tasks (6, 7) unblock after Task 5 passes verification
- [ ] Dashboard shows Task 5 as "Finished" and Tasks 6, 7 as eligible

### Fail indicators

- implement-agent ignores verification failure notes
- Task skips re-verification and goes directly to "Finished"
- verify-agent only checks the new file, not the full task scope
- Dependent tasks don't unblock

---

## Trace 27C: Re-verification limit (2 failures → escalate)

- **Path:** verify-agent → Step T7 re-verification limit

### Scenario

Task 5 has now failed verification twice. implement-agent attempts a fix and triggers a third verification attempt. verify-agent detects this is the 3rd attempt.

### Expected

1. verify-agent counts previous `[VERIFICATION FAIL]` entries in task notes
2. Detects this is attempt 3 (after 2 prior failures)
3. Per Step T7: "Maximum 2 re-verification attempts per task"
4. Task status set to "Blocked"
5. Notes explain the repeated failures
6. Task escalated to human review
7. Dashboard surfaces Task 5 in "Action Required" as blocked/needing human attention

### Pass criteria

- [ ] Re-verification limit enforced after 2 failures
- [ ] Task set to "Blocked" (not "In Progress" for another attempt)
- [ ] Notes document the history of failures
- [ ] Human review is explicitly requested
- [ ] Dashboard surfaces the blocked task prominently
- [ ] Dependent tasks (6, 7) remain blocked

### Fail indicators

- Infinite retry loop with no escalation
- Task silently stays "In Progress" after 3rd failure
- No human escalation mechanism
- Verification history not tracked in notes

---

## Trace 27D: Phase-level verification creates fix tasks

- **Path:** verify-agent phase-level → Steps 5-6; work.md § "If Verifying (Phase-Level)"

### Scenario

All spec tasks are "Finished" with passing per-task verification. Phase-level verification runs and discovers a cross-task integration issue: the API layer (Task 6) doesn't correctly consume the pipeline output format (Task 5). This is a spec requirement ("API must serve pipeline data").

### Expected

1. verify-agent Step 3: Per-criterion table shows "API serves pipeline data" as FAIL
2. Step 5: Categorized as "Major" (core functionality broken)
3. Step 6: Creates a new fix task:
   - Regular task (NOT `out_of_spec: true`) — this is an in-spec bug
   - `source: "verify-agent"`
   - Describes the integration mismatch
4. Step 7: `verification-result.json` written with `result: "fail"`
5. `/work` reads result → routes back to implement-agent for the fix task
6. After fix: `/work` routes to phase-level re-verification

### Pass criteria

- [ ] Phase-level verification catches cross-task integration issues
- [ ] Fix task created as regular task (in-spec), not out-of-spec
- [ ] `verification-result.json` written with `result: "fail"`
- [ ] `/work` correctly routes to implement-agent for the fix task
- [ ] After fix completes, phase-level verification re-runs
- [ ] Dashboard shows fix task and verification debt

### Fail indicators

- Integration issue missed (per-task verification passed each task individually)
- Fix task created as `out_of_spec: true` (this IS in the spec)
- `/work` treats the project as complete despite `result: "fail"`
- No re-verification after fix
- verify-agent implements the fix itself (violates separation of concerns)

---

## Trace 27E: Out-of-spec recommendations require user approval

- **Path:** verify-agent phase-level → Step 6; work.md § out-of-spec consent flow

### Scenario

During phase-level verification, verify-agent also notices that adding request caching would improve API performance. This is NOT in the spec — it's a recommendation.

### Expected

1. verify-agent Step 6: Creates recommendation task:
   - `out_of_spec: true`
   - `source: "verify-agent"`
   - `status: "Pending"`
2. Result is `"pass_with_issues"` (all spec criteria pass, but recommendation exists)
3. `/work` presents the recommendation to the user:
   - `[A]` Accept, `[R]` Reject, `[D]` Defer
4. User must explicitly approve before `/work` will execute it

### Pass criteria

- [ ] Recommendation created with `out_of_spec: true`
- [ ] Phase result is `"pass_with_issues"` (not "fail" — spec criteria all passed)
- [ ] User presented with accept/reject/defer options
- [ ] Task not auto-executed without user approval
- [ ] Dashboard shows recommendation with warning prefix

### Fail indicators

- Recommendation treated as in-spec fix (blocks completion)
- Auto-executed without user consent
- Phase result is "fail" for a beyond-spec suggestion
- No user-facing choice presented
