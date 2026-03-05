# Scenario 31: Handoff at Phase Boundary

Verify that context transitions at phase boundaries preserve the strategic knowledge that bridges phases — what Phase N established that Phase N+1 depends on. This is the moment where the "why" context matters most, because the next session starts a new body of work that builds on assumptions from the completed phase.

## State

- Phase 1: all 4 tasks "Finished" with passing verification
  - Phase 1 established: CSV and JSON parsers, data validation layer, schema registry
  - Key patterns discovered: the user's data has inconsistent date formats across vendors
  - DEC-001 (data format): resolved, chose ISO 8601 normalization
- Phase 2: 4 tasks "Pending" (analysis pipeline — depends on Phase 1's data layer)
  - DEC-002 (analysis library): resolved, chose pandas
- Phase gate 1->2: approved by user
- Tier 2 (phase-level) verification: passed
- `/work` is about to dispatch Phase 2's first task

---

## Trace 31A: `/work pause` between phases

- **Path:** `/work pause` triggered after Phase 1 completion, before Phase 2 work begins

### Expected

1. No active agent work to wind down (between dispatches)
2. Handoff file written:
   ```json
   {
     "trigger": "user_pause",
     "position": {
       "phase": "2",
       "recently_completed": ["1", "2", "3", "4"],
       "next_planned": "5",
       "phase_context": "Phase 1 built the data ingestion layer. Key outcome: all vendor data normalized to ISO 8601 dates via DEC-001. Phase 2 builds the analysis pipeline on top of this — pandas chosen via DEC-002. Date format inconsistency across vendors was a recurring issue in Phase 1; the normalization layer handles it but downstream tasks should not assume consistent input formats before normalization."
     },
     "active_work": [],
     "parallel_state": null,
     "session_knowledge": "User's data has inconsistent date formats across vendors — this drove several implementation decisions in Phase 1. The normalization layer is the critical dependency for Phase 2. User prefers explicit error messages for data quality issues. Performance is secondary to correctness for the prototype.",
     "recovery_action": "Begin Phase 2 execution. First eligible task is task 5. Phase 1's data layer is complete and verified. No special handling needed — normal /work routing will dispatch Phase 2 tasks."
   }
   ```
3. `active_work` is empty (no task in flight)
4. `session_knowledge` captures cross-phase insights (date format issue, user preferences)
5. `recovery_action` is straightforward (normal routing)

### Pass criteria

- [ ] `phase_context` captures what Phase 1 established and why it matters for Phase 2
- [ ] `session_knowledge` includes cross-phase patterns (date inconsistency, error message preference)
- [ ] `active_work` is empty array (not null — no work in flight, but the field should be present)
- [ ] `recovery_action` indicates normal Phase 2 start (no special recovery needed)
- [ ] Handoff does NOT duplicate information already in decision records or task completion notes

### Fail indicators

- `phase_context` is empty or generic ("Phase 1 is done")
- Cross-phase knowledge lost (date format issue not captured anywhere)
- `session_knowledge` duplicates task completion notes verbatim (should add what notes don't capture)
- `recovery_action` suggests re-verifying Phase 1 (already verified and gate-approved)

---

## Trace 31B: Next session starts Phase 2 with context

- **Path:** `/work` Step 0, handoff from phase boundary exists

### State (at session start)

- `.claude/tasks/.handoff.json` exists (from 31A)
- Phase 1: all "Finished", gate approved
- Phase 2: all "Pending"

### Expected

1. `/work` Step 0 detects handoff, presents summary:
   ```
   Resuming from previous session (paused at phase boundary):
   Phase 1 complete. Starting Phase 2 (analysis pipeline).
   Key context: data normalized to ISO 8601 (DEC-001), pandas selected (DEC-002).
   ```
2. Handoff deleted
3. No session recovery needed (no stuck tasks)
4. `/work` routes to Phase 2 task 5 via normal Step 3 logic
5. `session_knowledge` available to `/work` coordinator — when dispatching implement-agent for task 5, the coordinator can include relevant phase context in the agent handoff

### Pass criteria

- [ ] Summary is concise — highlights phase transition and key decisions, not full handoff dump
- [ ] Phase 2 work begins normally (no re-verification of Phase 1)
- [ ] Phase gate not re-presented (already approved — handoff doesn't reset gates)
- [ ] `session_knowledge` informs implement-agent context (date format patterns relevant to analysis tasks)
- [ ] `phase_context` enriches the "Provides: current phase, spec summary, recent activity" handoff to implement-agent (per workflow.md Handoff Protocol)

### Fail indicators

- Phase 1 re-verified or gate re-presented
- Phase context lost — implement-agent for task 5 has no awareness of Phase 1 patterns
- `/work` re-decomposes Phase 2 (tasks already exist)
- Handoff treated as if active work was in flight (it wasn't — clean phase boundary)

---

## Why Phase Boundaries Matter Most

Phase boundaries are where the handoff's `session_knowledge` and `phase_context` fields provide the most value. Within a phase, implement-agent can usually infer context from task dependencies and completion notes. But at a phase boundary:

- The tasks change (Phase 2 tasks don't depend on Phase 1 tasks directly — phases are sequential barriers, not dependency chains)
- The completion notes are in Phase 1's task JSONs, which Phase 2's implement-agent doesn't naturally read
- Patterns discovered in Phase 1 (like the date format inconsistency) affect Phase 2 design but aren't in any spec section or decision record

The handoff bridges this gap. Without it, the next session's implement-agent starts Phase 2 "cold" — technically correct (it reads the spec) but missing the experiential knowledge from Phase 1.
