# Scenario 26: /review Command — Implementation Quality Assessment

Verify that `/review` correctly assesses quality across completed tasks and produces purely advisory suggestions without modifying any project state. Also verify that `/iterate` stays in spec review mode regardless of task completion count.

## State

- Spec v1: status `active`
- 12 tasks total across Phase 1:
  - Tasks 1-8: status `Finished` with passing `task_verification`
  - Task 9: status `In Progress`
  - Tasks 10-12: status `Pending`
- Task 3 and Task 7 both modify `src/api/routes.ts` (noted in `files_affected`)
- Task 3 uses try/catch error handling pattern
- Task 7 uses `.catch()` promise chain pattern
- DEC-001: status `implemented`, `implementation_anchors: [{ file: "src/auth/oauth.ts", line: 45 }]`
- DEC-002: status `approved`, no `implementation_anchors` (not yet implemented)
- `.claude/support/learnings/` contains `patterns.md` with "Use async/await with try/catch for error handling"

## Trace A: `/review` enters review mode

- review.md Step 1: gather context
- Reads all task files, spec, decisions, learnings
- 8 tasks Finished (≥ 3 threshold) → proceeds

### Expected

- Shows implementation review report (not spec readiness checklist)
- Proceeds to Step 2 focus area assessment

## Trace A2: `/iterate` stays in spec mode despite many finished tasks

- Same state (spec `active`, 8 tasks Finished)
- User runs `/iterate` (bare, no arguments)

### Expected

- Does NOT enter implementation review mode
- Shows spec readiness checklist
- Stays in spec review mode — proposes spec changes, not implementation changes

## Trace A3: `/review integration` narrows focus

- review.md Step 1: user specified `/review integration`
- Enters review with focus narrowed to integration quality

### Expected

- Goes directly to review
- Focus area restricted to integration quality

## Trace B: Review Step 2 — Focus Area Assessment

### Architecture Coherence
- Tasks 1-8 mostly consistent
- No major contradictions found

### Integration Quality
- Task 3 and Task 7 both modify `src/api/routes.ts`
- Check if their changes compose correctly
- Task 5 depends on Task 3's output — verify handoff

### Pattern Consistency
- Task 3 uses try/catch (matches learnings pattern)
- Task 7 uses .catch() (contradicts learnings pattern)
- Flagged as inconsistency

### Cross-Cutting Concerns
- Error handling inconsistency detected (see pattern consistency)

### Technical Debt
- Task 6 completion notes: "MVP complete. Additional work in task 11"
- 2 minor issues from task_verification across completed tasks

### Decision Implementation Audit
- DEC-001: implementation_anchors point to `src/auth/oauth.ts` line 45 — verify file exists and content matches
- DEC-002: approved but no anchors — flag as potentially drifting

### Expected

```
Implementation Review (Phase 1, 8/12 tasks complete)

Architecture coherence:      ✓ Consistent
Integration quality:         ⚠ 1 concern
Pattern consistency:         ⚠ 1 inconsistency
Cross-cutting concerns:      ⚠ 1 gap
Technical debt:              ⚠ 2 items
Decision implementation:     ⚠ 1 drift

Focusing on: Pattern consistency
```

## Trace C: Review Step 3-5 — Findings and Suggestions

### Findings

1. **Pattern inconsistency (Tasks 3 vs 7):**
   - What: Task 7 uses `.catch()` pattern while project convention (in learnings) and Task 3 use try/catch
   - Where: `src/api/routes.ts` (Task 7's changes)
   - Why it matters: Inconsistent error handling makes debugging harder
   - Suggestion: Refactor Task 7's `.catch()` to try/catch pattern

2. **Decision DEC-002 not yet anchored:**
   - What: DEC-002 is approved but has no implementation_anchors
   - Where: No anchors to reference yet
   - Suggestion: When Tasks 10-12 implement this decision, add anchors

### Questions (max 4)

```
1. Task 7 uses .catch() while the project pattern (documented in learnings) is try/catch.
   Should Task 7 be updated to match, or should the pattern be updated to allow both?

2. Task 6 noted "MVP complete, additional work in Task 11." Is Task 11's scope
   sufficient to cover what was deferred?
```

### Suggestions (after user answers)

```
## Suggestions

### 1. Standardize error handling in Task 7
Refactor src/api/routes.ts to use try/catch pattern (consistent with learnings/patterns.md).

### 2. Verify DEC-002 anchors after Tasks 10-12
When implementing Tasks 10-12, add implementation_anchors to DEC-002.

These are suggestions — apply what makes sense for your project.
```

### Expected

- All findings reference specific tasks and files
- Suggestions are copy-pasteable where appropriate
- No tasks created
- No files modified
- No status changes to any task or decision

## Trace D: Advisory boundary enforcement

Verify `/review` does NOT:
1. Create any new task files
2. Modify any existing task JSON
3. Modify any decision record
4. Write to `.claude/support/learnings/`
5. Regenerate the dashboard
6. Change spec status or content

### Expected

- After review completes, all files are identical to before review started
- Only output is the review report displayed to user

## Trace E: Insufficient completed work

- Modified state: Only 2 tasks are `Finished`
- User runs `/review`

### Expected

```
Not enough completed work for meaningful review. Continue with /work.
```

- Does not proceed to focus area assessment

## Pass criteria

- [ ] `/review` enters review mode and assesses completed work
- [ ] `/review {area}` narrows focus to specified area
- [ ] `/iterate` (bare) stays in spec review mode even with 8 Finished tasks
- [ ] All 6 focus areas assessed with indicators
- [ ] Pattern inconsistency detected (Task 3 vs Task 7 error handling)
- [ ] Decision anchor drift detected (DEC-002 approved but no anchors)
- [ ] Technical debt detected from task completion notes
- [ ] Learnings consulted and compared against implementation
- [ ] Questions asked (max 4) about implementation direction
- [ ] Suggestions provided with specific file:line references
- [ ] NO tasks created (purely advisory)
- [ ] NO files modified (purely advisory)
- [ ] NO status changes to tasks or decisions
- [ ] Stops when < 3 Finished tasks
- [ ] Report format includes phase context and task completion ratio

## Fail indicators

- `/review` creates task files (violates advisory boundary)
- `/review` modifies task JSON or decision records
- `/review` regenerates the dashboard
- `/iterate` enters implementation review mode (should always stay in spec mode)
- Findings lack specific task/file references
- Suggestions assume code context not actually read from files
