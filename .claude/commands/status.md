# Status Command

Quick, read-only view of project state without starting any work.

## Usage

```
/status              # Full status overview
/status --brief      # One-line summary only
/status --tasks      # Focus on task status
/status --timeline   # Focus on upcoming dates and milestones
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
- `.claude/tasks/milestone-*.json` - Milestone data
- `.claude/support/questions.md` - Check for blocking questions
- `.claude/spec_v{N}.md` - Check phase (Spec/Execute/Verify)

**Important:** Use dashboard data for display. Only read task/milestone files for phase detection and data not in dashboard.

### Step 2: Determine Phase

| Condition | Phase |
|-----------|-------|
| No spec exists | Pre-spec |
| Spec incomplete | Spec (in progress) |
| Spec complete, no tasks | Ready for decomposition |
| Tasks exist, not all finished | Execute |
| All tasks finished | Ready for verification |
| Verification passed | Complete |

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

### Milestones
| Status | Milestone | Target | Progress |
|--------|-----------|--------|----------|
| ✅ | M1: Foundation | Jan 20 | Complete |
| 🔄 | M2: Core Features | Feb 1 | 6/8 tasks |
| ⏳ | M3: Polish | Feb 10 | Not started |

### Upcoming
- Feb 1: M2 milestone due
- Feb 5: Task 9 due (email scheduling)

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
Execute phase: 12/18 tasks done | 1 in progress | 2 need human | M2 due Feb 1
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

### Timeline Mode (`/status --timeline`)

Focus on dates and milestones:

```markdown
## Timeline

### This Week
| Date | Item | Type | Status |
|------|------|------|--------|
| Jan 28 | Task 5: API keys | Due | ⚠️ Tomorrow |
| Jan 29 | Today | | |
| Feb 1 | M2: Core Features | Milestone | 🔄 75% |

### Coming Up
| Date | Item | Type |
|------|------|------|
| Feb 5 | Task 9: Email scheduling | Due |
| Feb 10 | M3: Polish | Milestone |
| Feb 15 | Task 12: E2E tests | Due |

### At Risk
- ⚠️ Task 5 due tomorrow, still in progress
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
→ Execute phase: 12/18 tasks done | 1 in progress | 2 need human | M2 due Feb 1

# Full status report
/status
→ (full formatted output)

# See what tasks need attention
/status --tasks
→ (task-focused output)

# Check upcoming deadlines
/status --timeline
→ (date-focused output)
```

---

## Notes

- `/status` is purely informational - use `/work` to actually do work
- `/status` displays data from dashboard.md - it does NOT recalculate stats
- If the dashboard seems stale (e.g., task files newer than dashboard), recommend running `/work` to refresh
- Brief mode is ideal for quick context before starting work
- Phase detection requires reading task files since dashboard doesn't track phase explicitly
