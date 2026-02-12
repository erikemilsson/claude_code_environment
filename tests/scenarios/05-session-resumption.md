# Scenario 05: Session Resumption

Verify that workflow state persists across session boundaries using file-based checkpoints, not conversation history.

## Durable State Map

| State element | Persists in | Read by |
|---------------|-------------|---------|
| Spec completeness | `.claude/spec_v{N}.md` content | `/iterate`, `/work` |
| Task status | `.claude/tasks/task-*.json` | `/work` task routing |
| Decision status | `.claude/support/decisions/decision-*.md` | `/work` decision check |
| Inflection point revision | `spec_revised` field in decision frontmatter | `/work` inflection point check, `/iterate` |
| Dashboard | `.claude/dashboard.md` (+ META block hash) | `/work` dashboard freshness check |
| Phase progress | Derived from task statuses | `/work` task routing |
| Drift state | `.claude/drift-deferrals.json` | `/work` drift check |

---

## 5A: Interrupted during `/iterate`

### State
- Spec has gaps (same as Scenario 01)
- User ran `/iterate`, answered questions, got suggestions
- Session ended before pasting suggestions into spec

### Trace: `/iterate` spec readiness check

- Reads spec → same gaps still exist → same readiness check → same questions
- `/iterate` is stateless: the spec IS the checkpoint

### Pass criteria
- [ ] Same gaps detected (spec unchanged → same assessment)
- [ ] Doesn't assume previous answers were applied

---

## 5B: Interrupted during `/work` (mid-implementation)

### State
- Task 3: "In Progress" in task JSON
- Some files partially modified

### Trace: `/work` task routing

- Detects task 3 status "In Progress" → routes to implement-agent to continue
- Does not re-select a different task or re-decompose

### Pass criteria
- [ ] Task 3 resumed (not restarted)
- [ ] Doesn't pick a different task

---

## 5C: Interrupted between decision resolution and `/iterate`

### State
- DEC-001: `status: approved`, `inflection_point: true`, `spec_revised`: absent
- Spec still says "appropriate statistical methods"
- Previous session's `/work` said "run /iterate" but session ended

### Trace: `/work` inflection point check

- DEC-001: `inflection_point: true`, check `spec_revised` → absent → pause
- Same message as previous session — no conversation state needed

### Expected
```
Decision DEC-001 (Analysis Method) was an inflection point.
Run /iterate to review affected spec sections.
```

### Pass criteria
- [ ] Re-detects inflection point (doesn't assume /iterate already ran)
- [ ] Phase 2 tasks remain blocked
- [ ] Works identically whether 5 minutes or 5 weeks between sessions

---

## 5D: Interrupted between phases

### State
- Phase 1: all tasks "Finished" with passing verification
- Phase 2: tasks "Pending" (decisions resolved, no blockers)

### Trace: `/work` task routing

- Phase 1 all Finished → Phase 2 tasks eligible → dispatches

### Pass criteria
- [ ] Phase 2 begins without re-checking Phase 1
- [ ] No re-decomposition or re-verification of finished work

---

## Dashboard Freshness (cross-cutting)

### Trace: `/work` dashboard freshness check

- Computes `task_hash` from current task files
- Compares to dashboard META block's `task_hash`
- Mismatch → regenerate; match → use as-is

### Pass criteria
- [ ] Stale dashboard detected and regenerated
- [ ] Fresh dashboard used without unnecessary regeneration
