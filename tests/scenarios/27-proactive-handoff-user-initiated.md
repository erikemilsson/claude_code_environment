# Scenario 27: Proactive Context Handoff (User-Initiated)

Verify that `/work pause` performs a graceful wind-down: reaches the nearest clean boundary, updates task JSON with partial notes, writes a handoff file, and that the next `/work` run detects and uses the handoff for smarter resumption.

## State

- Phase 2: 4 tasks
  - Task 5: "Finished" (completed this session)
  - Task 6: "Finished" (completed this session)
  - Task 7: "Build transformation engine" (status: "In Progress", owner: "claude")
    - implement-agent is at Step 4 (implementation), mid-work
    - `files_affected: ["src/transform/mapper.py", "src/transform/coerce.py", "src/transform/aggregate.py"]`
    - mapper.py and coerce.py are written; aggregate.py is not started
  - Task 8: "Pending", depends on [7]
- DEC-002: `status: approved`, selected: "pandas"
- User said earlier in conversation: "Error messages matter more than performance for this prototype"

---

## Trace 27A: `/work pause` — graceful wind-down

- **Path:** `/work pause` triggered while implement-agent is mid-Step 4

### Expected

1. Claude recognizes the pause signal
2. Attempts to reach nearest clean boundary:
   - Step 4 (implementation) is in progress — cannot cleanly finish the full step
   - Writes what it has so far as partial completion notes
3. Updates task 7 JSON:
   - Status stays "In Progress"
   - Notes updated: `[PARTIAL] Completed column mapping logic (mapper.py) and type coercion module (coerce.py). Aggregation pipeline (aggregate.py) not started. User prioritizes clear error messages over performance.`
   - `updated_date` set to today
4. Writes `.claude/tasks/.handoff.json` with:
   - `trigger: "user_pause"`
   - `position.phase: "2"`, `position.recently_completed: ["5", "6"]`, `position.next_planned: "7"`
   - `active_work[0].task_id: "7"`, `agent: "implement"`, `agent_step: "Step 4 (implementation)"`, `partial: true`, `ready_for_verify: false`
   - `session_knowledge` captures the user's error message preference and DEC-002 context
   - `recovery_action` explains: continue task 7 implementation, aggregation pipeline remains
5. Writes `.claude/tasks/.last-clean-exit.json` (clean exit — pause is intentional)

### Pass criteria

- [ ] Task 7 status remains "In Progress" (not changed to Blocked, On Hold, or any other status)
- [ ] Task 7 notes contain `[PARTIAL]` prefix with meaningful progress summary
- [ ] Handoff file written with all required top-level fields (`version`, `trigger`, `timestamp`, `spec_version`)
- [ ] `active_work` entry has `partial: true` and `ready_for_verify: false`
- [ ] `session_knowledge` captures the error-message preference (not in spec or CLAUDE.md — only stated in conversation)
- [ ] Session sentinel written (this was a clean exit)
- [ ] No new work started after pause signal

### Fail indicators

- Task 7 status changed to something other than "In Progress"
- Handoff file missing or missing critical fields
- Claude starts working on the next task after receiving pause signal
- Partial notes are empty or generic ("work in progress")
- User's conversation preferences not captured in `session_knowledge`

---

## Trace 27B: Next session `/work` detects handoff

- **Path:** `/work` Step 0, handoff file exists from Trace 27A

### State (at session start)

- `.claude/tasks/.handoff.json` exists (from 27A)
- `.claude/tasks/.last-clean-exit.json` exists (clean exit)
- Task 7: "In Progress" with `[PARTIAL]` notes

### Expected

1. `/work` Step 0 detects `.handoff.json` before session recovery scan
2. Presents brief summary to user:
   ```
   Resuming from previous session (paused 2026-03-05T14:30:00Z):
   Task 7 "Build transformation engine" — implementation ~60% done
   (mapper.py and coerce.py complete, aggregate.py remaining)
   ```
3. Loads `session_knowledge` into working context (error message preference, DEC-002 context)
4. Uses `recovery_action` to inform routing: routes to implement-agent for task 7, not task 8
5. Deletes `.handoff.json` after successful restoration
6. Proceeds to normal Step 0 session recovery (fast-path: sentinel is clean, only checks task 7)
7. Routes to implement-agent for task 7 with enriched context from handoff

### Pass criteria

- [ ] Handoff detected and summary presented before any other work
- [ ] Summary includes task title and progress indication (not just "task 7 in progress")
- [ ] Routes to task 7 (not task 8 or re-decomposition)
- [ ] `session_knowledge` content available to inform implementation (e.g., error message preference)
- [ ] Handoff file deleted after restoration
- [ ] Normal session recovery still runs after handoff restoration

### Fail indicators

- Handoff file ignored — `/work` routes based only on task status
- Summary is too verbose (full handoff dump) or missing (no summary at all)
- Routes to wrong task or re-decomposes
- Handoff file left on disk after restoration (risks stale handoff next session)
- Session recovery scan skipped because handoff was found
