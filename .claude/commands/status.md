# Status Command

Quick, read-only view of project state without starting any work.

## Usage

```
/status              # Full status overview
/status --brief      # One-line summary only
/status --tasks      # Focus on task status
```

## What It Does

1. **Read-only** - Never modifies files, never starts work
2. **Fast** - Quick scan, no agent invocation
3. **Informative** - Shows exactly what you need to know

**Key difference from `/work`:** The `/status` command only reads and displays. It never creates tasks, invokes agents, or modifies any files.

---

## Process

### Step 1: Gather State

Read (but don't modify):
- `.claude/dashboard.md` - Current status (primary data source)
- `.claude/tasks/task-*.json` - Task data for phase detection
- `.claude/support/questions.md` - Check for blocking questions
- `.claude/spec_v{N}.md` - Check phase (Spec/Execute/Verify)

**Important:** Use dashboard data for display. Only read task files for phase detection and data not in dashboard.

### Step 2: Determine Phase

| Condition | Phase |
|-----------|-------|
| No spec exists | Pre-spec |
| Spec incomplete | Spec (in progress) |
| Spec complete, no tasks | Ready for decomposition |
| Tasks exist, not all finished | Execute |
| All tasks finished, no valid verification result | Ready for verification |
| All tasks finished, verification result exists and is valid | Complete |

**Verification result check:**
Read `.claude/verification-result.json` if it exists. A result is **valid** when:
- `result` is `"pass"` or `"pass_with_issues"`
- `spec_fingerprint` matches the current spec's fingerprint (spec hasn't changed since verification)
- No tasks have been added or changed status since the `timestamp`

If the file doesn't exist or the result is `"fail"` or invalidated, the phase is "Ready for verification."

### Step 3: Format Output

Display the appropriate output format based on mode.

---

## Output Formats

### Full Mode (default: `/status`)

```markdown
## Project Status

**Phase:** Execute (12/18 tasks complete)
**Current:** Task 5_3 "Add Redis caching layer" - In Progress

### Quick Numbers
| Total | Done | In Progress | Blocked | Human Action |
|-------|------|-------------|---------|--------------|
| 18    | 12   | 1           | 0       | 2            |

### Attention Needed
- Decision pending: Auth approach (decision-001)
- Human task ready: Configure LDAP credentials (Task 7)

### Recent Activity (last 24h)
- ✅ Task 5_1 completed
- ✅ Task 5_2 completed
- 🚀 Task 5_3 started
```

### Brief Mode (`/status --brief`)

Single line for quick check:

```
Execute phase: 12/18 tasks done | 1 in progress | 2 need human
```

### Tasks Mode (`/status --tasks`)

Focus on task breakdown:

```markdown
## Task Status

**By Status:**
- Finished: 12
- In Progress: 1 (Task 5_3)
- Pending: 3
- Blocked: 0
- Broken Down: 2

**By Owner:**
- Claude: 10 remaining
- Human: 2 ready
- Both: 1 pending

**Next Up:**
1. Task 5_4 "Create drill-down endpoints" (blocked by 5_3)
2. Task 6 "Build React dashboard" (ready)
3. Task 7 "Add authentication" (needs human input)
```

---

## Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | Complete |
| 🔄 | In Progress |
| ⏳ | Pending / Not started |
| ⚠️ | At Risk (approaching or past due) |
| 🔴 | Overdue or Critical |
| 🚀 | Just started |

---

## Examples

```
# Quick check before a meeting
/status --brief
→ Execute phase: 12/18 tasks done | 1 in progress | 2 need human

# Full status report
/status
→ (full formatted output)

# See what tasks need attention
/status --tasks
→ (task-focused output)
```

---

## Notes

- `/status` is purely informational - use `/work` to actually do work
- `/status` displays data from dashboard.md - it does NOT recalculate stats
- If the dashboard seems stale (e.g., task files newer than dashboard), recommend running `/work` to refresh
- Brief mode is ideal for quick context before starting work
- Phase detection requires reading task files since dashboard doesn't track phase explicitly
