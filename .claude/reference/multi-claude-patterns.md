# Multi-Claude Coordination Patterns

*Version: 1.0 | Based on: Anthropic Claude Code Best Practices*

## Overview

For complex projects, running multiple Claude instances in parallel can significantly improve throughput and quality. This guide covers patterns for coordinating multiple Claude Code sessions effectively.

## Core Patterns

### Pattern 1: Writer + Reviewer

**Setup:** Two Claude instances with distinct roles.

```markdown
INSTANCE A (Writer):
- Implements features
- Writes code
- Creates tests
- Focus: Forward progress

INSTANCE B (Reviewer):
- Reviews code quality
- Runs test suites
- Checks for issues
- Focus: Quality assurance
```

**Workflow:**
```
Writer completes feature → Commits to branch
Reviewer pulls → Reviews → Documents issues
Writer addresses feedback → Commits
Reviewer approves → Merge ready
```

**Communication:**
```markdown
SHARED SCRATCHPAD: .claude/scratchpad/

Writer creates:
  .claude/scratchpad/feature-auth-ready.md

Contents:
  # Feature: Authentication
  Status: Ready for review
  Files changed:
  - src/auth/login.js
  - src/auth/middleware.js
  - tests/auth.test.js

  Notes:
  - Used JWT approach as discussed
  - Added refresh token handling
  - Edge case: session timeout handled in middleware

Reviewer creates:
  .claude/scratchpad/feature-auth-review.md

Contents:
  # Review: Authentication
  Status: Changes requested

  Issues:
  1. [HIGH] Missing rate limiting on login endpoint
  2. [MED] Token expiry should be configurable
  3. [LOW] Consider extracting token validation to utility

  Questions:
  - Should failed attempts be logged?
```

### Pattern 2: Parallel Worktrees

**Setup:** Multiple git worktrees, each with its own Claude instance.

```bash
# Create worktrees for parallel development
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-bugfix bugfix-123

# Each worktree gets its own terminal/VS Code window
# Each runs independent Claude Code session
```

**Benefits:**
- Full isolation between tasks
- No branch switching overhead
- Independent test runs
- Clean git history per feature

**Coordination:**
```markdown
MAIN WORKTREE:
- Integration and merging
- Conflict resolution
- Release management

FEATURE WORKTREES:
- Independent development
- Own test suites
- Isolated experiments
```

### Pattern 3: Task Fan-Out

**Setup:** Primary Claude breaks down work, spawns specialized sessions.

```markdown
PRIMARY CLAUDE:
1. Analyzes complex task
2. Breaks into subtasks
3. Creates task assignments
4. Monitors progress
5. Integrates results

WORKER CLAUDES (spawned via separate terminals):
- Each handles assigned subtask
- Works independently
- Reports via scratchpad
```

**Task Assignment File:**
```markdown
# .claude/scratchpad/task-assignments.md

## Epic: Implement Dashboard

### Subtask 1: Data API
- Assigned to: Worktree A
- Status: In Progress
- Files: src/api/dashboard/*

### Subtask 2: Chart Components
- Assigned to: Worktree B
- Status: Complete
- Files: src/components/charts/*

### Subtask 3: Real-time Updates
- Assigned to: Worktree C
- Status: Pending (blocked on Subtask 1)
- Files: src/services/websocket/*

### Integration Status:
- API + Charts: Not started
- Full integration: Blocked
```

### Pattern 4: Specialized Roles

**Setup:** Different Claude instances optimized for specific tasks.

```markdown
INSTANCE ROLES:

"Architect Claude":
- System design decisions
- API contract definitions
- Database schema design
- Uses: ultrathink frequently

"Implementation Claude":
- Code writing
- Test implementation
- Bug fixes
- Uses: explore-plan-code-commit

"DevOps Claude":
- CI/CD configuration
- Deployment scripts
- Infrastructure as code
- Monitoring setup

"Documentation Claude":
- API documentation
- README updates
- Code comments
- User guides
```

## Communication Mechanisms

### Scratchpad Directory

```markdown
STRUCTURE:
.claude/
└── scratchpad/
    ├── README.md           # Scratchpad conventions
    ├── decisions/          # Architecture decisions
    │   └── 001-auth.md
    ├── handoffs/           # Task handoffs between instances
    │   └── feature-x.md
    ├── reviews/            # Code review notes
    │   └── pr-123.md
    └── status/             # Current status per instance
        ├── instance-a.md
        └── instance-b.md
```

**Scratchpad File Format:**
```markdown
# [Topic/Feature Name]

## Metadata
- Created: 2024-01-15
- Author: Instance A
- Status: Ready for review | In progress | Complete

## Context
[What this is about]

## Content
[Main content - decisions, notes, code snippets]

## For Next Instance
[What the receiving instance needs to know]

## Questions
[Any open questions]
```

### Status Synchronization

```markdown
INSTANCE STATUS FILE:
# .claude/scratchpad/status/instance-a.md

Last updated: 2024-01-15 14:30

## Current Task
- ID: feature-auth
- Phase: Implementation
- Progress: 60%
- Blocker: None

## Completed Today
- [x] JWT token generation
- [x] Login endpoint
- [x] Basic middleware

## In Progress
- [ ] Refresh token flow
- [ ] Session management

## Needs From Other Instances
- Database schema review (Instance B)
- Frontend auth context (Instance C)
```

## Git Workflow for Multi-Claude

### Branch Strategy
```markdown
main
├── develop
│   ├── feature/auth (Instance A)
│   ├── feature/dashboard (Instance B)
│   └── feature/notifications (Instance C)
└── release/1.0
```

### Merge Protocol
```markdown
1. Feature complete in worktree
2. Update scratchpad with completion status
3. Push to feature branch
4. Create PR (can use Claude)
5. Another instance reviews
6. Address feedback
7. Merge to develop
```

### Conflict Resolution
```markdown
WHEN CONFLICTS OCCUR:

1. Identify scope of conflict
2. Determine which instance "owns" the conflicted files
3. Owner resolves conflicts
4. Other instances pull changes
5. Update scratchpads with resolution notes
```

## Best Practices

### DO:
```markdown
✅ Use separate worktrees for isolation
✅ Maintain scratchpad for communication
✅ Define clear ownership per task/file
✅ Commit frequently to avoid drift
✅ Use descriptive branch names
✅ Document decisions for other instances
✅ Regular status updates in scratchpad
```

### DON'T:
```markdown
❌ Have multiple instances edit same file
❌ Skip scratchpad updates
❌ Assume other instances have context
❌ Let worktrees drift far from main
❌ Ignore merge conflicts
❌ Work on undefined/unassigned tasks
```

## Setup Commands

### Creating Multi-Claude Environment
```bash
# Initialize scratchpad
mkdir -p .claude/scratchpad/{decisions,handoffs,reviews,status}
echo "# Scratchpad Directory" > .claude/scratchpad/README.md

# Create worktrees
git worktree add ../project-feature-a -b feature-a
git worktree add ../project-feature-b -b feature-b

# Open each in separate terminal/editor
code ../project-feature-a
code ../project-feature-b
```

### Monitoring All Instances
```bash
# Quick status check (run from main worktree)
cat .claude/scratchpad/status/*.md

# Check for updates
git fetch --all
git branch -vv
```

## Example: Full Multi-Claude Session

```markdown
SCENARIO: Building e-commerce checkout

INSTANCE A (Backend):
Terminal 1, Worktree: ../checkout-backend
Tasks: API endpoints, payment integration, order processing

INSTANCE B (Frontend):
Terminal 2, Worktree: ../checkout-frontend
Tasks: Checkout UI, cart state, form validation

INSTANCE C (Integration):
Terminal 3, Main worktree
Tasks: API contracts, integration tests, deployment

WORKFLOW:
1. Instance C defines API contracts in scratchpad
2. A and B work in parallel following contracts
3. A/B update status regularly
4. C monitors, runs integration tests
5. C handles merges and conflict resolution
6. All instances update scratchpad on completion
```

## Related Documentation

- `.claude/reference/headless-automation.md` - Scripted multi-instance orchestration
- `.claude/commands/explore-plan-code-commit.md` - Single-instance workflow
- `.claude/reference/context-management.md` - Managing context across sessions
