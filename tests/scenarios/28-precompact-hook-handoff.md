# Scenario 28: Auto-Compaction Handoff (PreCompact Hook)

Verify that the PreCompact hook writes a valid handoff file when auto-compaction triggers, and that the result is equivalent to the user-initiated path for restoration purposes — even though the hook path is lighter-touch (handoff only, no task JSON updates).

## Context

The PreCompact hook is the safety net. Unlike `/work pause` (where Claude has full conversation context and can gracefully wind down), the hook fires in a constrained environment. It must produce a useful handoff without modifying task JSON files (risk of corruption from a shell hook).

## State

- Same as Scenario 27: Task 7 "In Progress", implement-agent mid-Step 4
- Auto-compaction threshold reached (~95% context capacity)
- User did NOT run `/work pause` — compaction is automatic

---

## Trace 28A: PreCompact hook fires

- **Path:** Claude Code auto-compaction triggers PreCompact hook

### Expected

1. PreCompact hook fires before compaction begins
2. Hook writes `.claude/tasks/.handoff.json` with:
   - `trigger: "pre_compact"` (distinguishes from user-initiated)
   - All required fields populated from available context
   - `active_work` reflects current state as best as possible
3. Hook does NOT modify task JSON files (task 7 stays as-is, no `[PARTIAL]` prefix in notes)
4. Compaction proceeds normally after hook completes

### Pass criteria

- [ ] Handoff file written before compaction clears context
- [ ] `trigger` field is `"pre_compact"` (not `"user_pause"`)
- [ ] Task JSON files are untouched by the hook
- [ ] Handoff file has valid JSON structure with all required top-level fields
- [ ] Hook completes within execution time constraints (does not block compaction)

### Fail indicators

- Hook fails silently and no handoff file is written
- Hook modifies task JSON (risk of corruption)
- Hook blocks or significantly delays compaction
- Handoff file has invalid JSON (partially written due to timeout)

---

## Trace 28B: Restoration from hook-generated handoff

- **Path:** `/work` Step 0, handoff from PreCompact hook exists

### State (at session start)

- `.claude/tasks/.handoff.json` exists with `trigger: "pre_compact"`
- Task 7: "In Progress" but notes do NOT have `[PARTIAL]` prefix (hook didn't update task JSON)
- `.claude/tasks/.last-clean-exit.json` may or may not exist (compaction isn't a clean `/work` exit)

### Expected

1. `/work` Step 0 detects handoff — same flow as Scenario 27B
2. Summary presented to user (may be slightly less detailed than user-initiated handoff since partial notes weren't written to task JSON)
3. `session_knowledge` and `recovery_action` still available from handoff
4. Routes to implement-agent for task 7
5. Handoff deleted after restoration
6. Session recovery scan runs normally (sentinel may be stale — full scan)

### Pass criteria

- [ ] Hook-generated handoff treated identically to user-initiated handoff for restoration
- [ ] Missing `[PARTIAL]` notes in task JSON doesn't break restoration (handoff's `partial_notes` field provides the context)
- [ ] Routing decision is correct (task 7, not task 8)
- [ ] Full session recovery scan runs if sentinel is stale (hook path doesn't guarantee clean exit)

### Fail indicators

- Restoration fails because task JSON doesn't have partial notes (over-reliance on task JSON vs handoff)
- Different code path for hook-generated vs user-initiated handoffs (should be unified)
- Session recovery scan skipped despite no clean exit sentinel

---

## Contrast with Scenario 27

| Aspect | User-initiated (Scenario 27) | PreCompact hook (this) |
|--------|------------------------------|----------------------|
| Trigger | `/work pause` command | Auto-compaction threshold |
| Task JSON updated | Yes (`[PARTIAL]` notes) | No (too risky from hook) |
| Clean boundary reached | Yes (finishes current sub-step) | No (interrupted wherever context was) |
| Session sentinel | Written (clean exit) | May not be written (compaction isn't `/work` exit) |
| Handoff quality | Higher (full Claude context available) | Lower (constrained hook environment) |
| Restoration path | Identical | Identical |
| Safety guarantee | Graceful | Best-effort |
