# Scenario 29: Handoff During Verify-Agent Execution

Verify that context transitions work correctly when verify-agent is mid-verification. The Turn Budget Protocol already handles graceful wind-down for turn exhaustion — this tests that the handoff captures verification state and that the next session correctly spawns a fresh verify-agent rather than trying to resume partial verification.

## State

- Phase 2: 4 tasks
  - Task 5, 6: "Finished"
  - Task 7: "Awaiting Verification" (implement-agent completed, verify-agent spawned)
    - `verification_attempts: 1`
    - verify-agent is at Step T3 (spec alignment check), mid-verification
    - `files_affected: ["src/transform/mapper.py", "src/transform/coerce.py", "src/transform/aggregate.py"]`
  - Task 8: "Pending", depends on [7]

---

## Trace 29A: `/work pause` during verification

- **Path:** `/work pause` triggered while verify-agent is mid-Step T3

### Expected

1. Claude recognizes the pause signal
2. Verify-agent does NOT write partial `task_verification` (verification is binary — pass or fail, not partial)
3. Task 7 status stays "Awaiting Verification" (no change)
4. Handoff file written:
   - `active_work[0].task_id: "7"`, `agent: "verify"`, `agent_step: "Step T3 (spec alignment)"`, `partial: true`
   - `ready_for_verify: false` is irrelevant here (already in verification) — field should indicate verification was in progress
   - `recovery_action`: "Task 7 verification was interrupted. Spawn a fresh verify-agent — do not attempt to resume partial verification."
5. Session sentinel written (clean exit)

### Pass criteria

- [ ] Task 7 remains "Awaiting Verification" (not set back to "In Progress" or "Blocked")
- [ ] No partial `task_verification` written (incomplete verification must not look like a result)
- [ ] `verification_attempts` NOT incremented (this wasn't a failed attempt — it was interrupted)
- [ ] Handoff `agent` field is `"verify"` (distinguishes from implement handoff)
- [ ] `recovery_action` explicitly says to spawn fresh verify-agent

### Fail indicators

- Task 7 set to "Blocked" with timeout note (wrong — this is intentional pause, not timeout)
- Partial verification result written (violates binary pass/fail invariant)
- `verification_attempts` incremented (would bring task closer to escalation unfairly)
- Handoff says to continue verification where it left off (verify-agent must start fresh for context separation)

---

## Trace 29B: Next session resumes — merges with session recovery

- **Path:** `/work` Step 0, handoff exists + task in "Awaiting Verification"

### State (at session start)

- `.claude/tasks/.handoff.json` exists (from 29A, `agent: "verify"`)
- Task 7: "Awaiting Verification", `verification_attempts: 1`
- `.claude/tasks/.last-clean-exit.json` exists (clean exit)

### Expected

1. `/work` Step 0 detects handoff, presents summary:
   ```
   Resuming from previous session (paused):
   Task 7 "Build transformation engine" — verification was in progress, will restart
   ```
2. Handoff deleted
3. Session recovery runs: detects task 7 "Awaiting Verification" (recovery Case 1)
4. Session recovery spawns verify-agent for task 7 (auto-recover)
5. verify-agent starts fresh — full Steps T1-T8, no partial state carried over

### Pass criteria

- [ ] Handoff summary mentions verification was interrupted (not just "task 7 in progress")
- [ ] Session recovery Case 1 handles the actual re-spawn (handoff informs context, recovery handles mechanics)
- [ ] verify-agent gets fresh context (no partial verification state leaked)
- [ ] `verification_attempts` stays at 1 until verify-agent runs and increments it normally
- [ ] `session_knowledge` from handoff is available to `/work` coordinator (but NOT passed to verify-agent — context separation)

### Fail indicators

- Handoff restoration tries to spawn verify-agent itself (duplicating session recovery logic)
- Partial verification state from handoff passed to verify-agent (violates fresh-eyes principle)
- Session recovery skipped because handoff already "handled" verification
- `session_knowledge` leaked into verify-agent's context (should only inform `/work` coordinator)

---

## Key Design Constraint

**Handoff informs the coordinator; session recovery handles the mechanics.** The handoff tells `/work` "verification was in progress and was interrupted." Session recovery detects "Awaiting Verification" and spawns verify-agent. These are complementary, not competing — the handoff provides richer context (what step, why interrupted) while session recovery provides the actual re-spawn logic that already works.

**`session_knowledge` stays with the coordinator.** The user's conversation preferences (captured in `session_knowledge`) inform `/work`'s decisions but are NOT passed to verify-agent. Verify-agent must remain independent — it receives only task JSON, spec section, and files_affected. This preserves context separation.
