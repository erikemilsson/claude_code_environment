# Scenario 06: Late Decision Detection

Verify that the template catches decisions created *after* dependent work has already started or completed.

This is the anti-pattern that motivated the test suite: work proceeds on unresolved assumptions, forcing a rebuild when decisions are finally made.

## State

- Phase 1: 3 tasks, all "Finished"
- Phase 2: 3 tasks — Task 4: "Finished", Task 5: "In Progress", Task 6: "Pending"
  - **None have `decision_dependencies`** — created without the decision
- DEC-001 just created: `status: draft`, `inflection_point: true`, `related.tasks: ["4", "5", "6"]`

## Trace: `/health-check` Part 3, Check 6 — Cross-Reference

- **Path:** health-check.md → Part 3 → Check 6 (Decision-Task Cross-Reference)
- Read DEC-001 `related.tasks` → ["4", "5", "6"]
- For each: check if "DEC-001" in task's `decision_dependencies` → NO for all three
- Task 4 "Finished" → ERROR (work completed without decision)
- Task 5 "In Progress" → ERROR (work ongoing without decision)
- Task 6 "Pending" → WARNING (still fixable)

### Expected report

```
[ERROR] Late decision detected — work proceeded without decision gating

  DEC-001 (Analysis Method) references tasks [4, 5, 6]
  But these tasks have no decision_dependencies for DEC-001:

  - Task 4: Finished — may need rework
  - Task 5: In Progress — building without decision
  - Task 6: Pending — can be fixed

  Recommendations:
  1. Add decision_dependencies to tasks 4, 5, 6
  2. Review task 4's implementation
  3. Pause task 5 until DEC-001 resolved
```

## Trace: `/work` Step 2b item 5 — Late Decision Check

- **Path:** work.md → Step 2b → item 5 (LATE DECISION CHECK)
- Same reverse cross-reference as health-check
- Surfaces warning with options: [1] Add deps + pause, [2] Proceed as-is, [3] Review first
- Task 6 (Pending) silently fixed — `decision_dependencies: ["DEC-001"]` added

### If user picks [1]

- Task 4: dependency added, note: "Review after DEC-001 resolved — may need rework"
- Task 5: dependency added, status → "Pending" (blocked)
- Task 6: already fixed
- Dashboard regenerated showing new blocking state

## Trace: Post-resolution (after adding deps and resolving DEC-001)

- DEC-001 resolved → Step 2b-post → `inflection_point: true`, `spec_revised` absent → pause
- Standard Scenario 03 flow takes over
- Task 4's rework note surfaced during `/iterate`

## Pass criteria

- [ ] `/health-check` detects mismatch between `related.tasks` and `decision_dependencies`
- [ ] Finished tasks flagged as ERROR (work done without decision)
- [ ] In-progress tasks flagged as ERROR (ongoing without decision)
- [ ] Pending tasks flagged as WARNING (fixable)
- [ ] `/work` detects the same mismatch at Step 2b item 5
- [ ] User gets options (add deps / proceed / review)
- [ ] Completed work flagged for review, NOT automatically reverted
- [ ] After fix, standard inflection point flow (Scenario 03) takes over

## Fail indicators

- No cross-reference check (only checks task→decision, not decision→task)
- Finished tasks silently ignored
- Work automatically reverted (too aggressive)
- No options — just blocks or just continues
