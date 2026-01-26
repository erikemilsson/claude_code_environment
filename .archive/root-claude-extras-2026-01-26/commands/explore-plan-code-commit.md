<!-- Type: Direct Execution -->
<!-- Based on: Anthropic Claude Code Best Practices -->

# Explore-Plan-Code-Commit Workflow

## Purpose
Structured workflow for complex features that prevents premature coding and improves outcomes through systematic exploration and planning before implementation.

## When to Use
- Complex features requiring deep analysis
- Multi-file changes or refactors
- Unfamiliar codebases or domains
- Architecture decisions
- Tasks with difficulty >= 7

## Process

### Phase 1: EXPLORE (No Code Writing)

**Goal:** Build complete understanding before writing any code.

```markdown
EXPLORATION CHECKLIST:
□ Read all relevant files (use parallel reads)
□ Understand existing patterns and conventions
□ Identify dependencies and integration points
□ Note potential risks or complications
□ Map affected areas of codebase
```

**Actions:**
1. READ relevant source files in parallel
2. GREP for related patterns and usages
3. EXAMINE tests for expected behaviors
4. CHECK documentation for context
5. IDENTIFY similar implementations for reference

**Output:** Mental model of current state + list of files that will be affected.

### Phase 2: PLAN (Extended Thinking)

**Goal:** Design solution with full context before implementation.

**Trigger Extended Thinking:**
Use these phrases based on complexity:
- **"think"** - Basic extended reasoning
- **"think hard"** - Thorough multi-step analysis
- **"think harder"** - Deep analysis for complex problems
- **"ultrathink"** - Maximum reasoning depth for architecture decisions

```markdown
PLANNING DELIVERABLES:
□ Clear problem statement
□ Proposed solution approach
□ Files to create/modify (with specifics)
□ Potential risks and mitigations
□ Success criteria / acceptance tests
□ Estimated subtask breakdown (if difficulty >= 7)
```

**Actions:**
1. DOCUMENT plan in `.claude/planning/` or as GitHub issue
2. LIST specific changes per file
3. IDENTIFY test cases needed
4. NOTE assumptions to validate
5. DEFINE rollback strategy if needed

**Output:** Written plan document ready for implementation.

### Phase 3: CODE (Implementation)

**Goal:** Execute plan with verification at each step.

```markdown
IMPLEMENTATION APPROACH:
□ Follow TDD where applicable (tests first)
□ Make atomic, focused changes
□ Verify each change works before proceeding
□ Document deviations from plan
□ Create checkpoints for complex changes
```

**Actions:**
1. IMPLEMENT changes following the plan
2. TEST each component as you build
3. VERIFY integration points work
4. UPDATE plan if deviations needed
5. CREATE checkpoint every 3-5 significant changes

**Output:** Working implementation with passing tests.

### Phase 4: COMMIT (Documentation & Version Control)

**Goal:** Create clean, documented commit history.

```markdown
COMMIT CHECKLIST:
□ All tests passing
□ Code reviewed against plan
□ Documentation updated
□ Commit message explains "why"
□ Related issues referenced
```

**Actions:**
1. REVIEW changes against original plan
2. RUN full test suite
3. UPDATE documentation if needed
4. CREATE descriptive commit message
5. REFERENCE issue/task IDs

**Output:** Clean commit(s) with full traceability.

## Example Usage

### Starting the Workflow
```markdown
User: "Add user authentication to the API"

Claude: "I'll use the explore-plan-code-commit workflow for this.

**EXPLORE PHASE:**
Let me read the relevant files to understand the current architecture..."
[Reads auth-related files, API structure, existing middleware]

"**PLAN PHASE:**
Now let me think through the implementation approach... [ultrathink]

Based on my exploration, here's my plan:
1. Add JWT middleware in `src/middleware/auth.js`
2. Create user model in `src/models/user.js`
3. Add auth routes in `src/routes/auth.js`
4. Update API gateway to use auth middleware

Risks:
- Existing endpoints need backwards compatibility
- Session handling needs consideration

Shall I proceed with this plan?"

User: "Yes, proceed"

Claude: "**CODE PHASE:**
Starting implementation following TDD approach..."
[Implements with tests, checkpoints]

"**COMMIT PHASE:**
All tests passing. Creating commit..."
[Creates atomic commits with clear messages]
```

## Integration with Task System

When using this workflow with the task management system:

1. **High-Difficulty Tasks (>= 7):** Run `/breakdown` after PLAN phase
2. **Create Task:** Create task JSON during PLAN phase
3. **Update Progress:** Use `/complete-task` during CODE phase
4. **Sync:** Run `/sync-tasks` after COMMIT phase

## Parallel Execution Opportunities

```markdown
PARALLEL OPERATIONS (EXPLORE phase):
- Multiple file reads
- Multiple grep searches
- Documentation lookups

SEQUENTIAL REQUIREMENTS:
- EXPLORE must complete before PLAN
- PLAN must complete before CODE
- CODE must complete before COMMIT
```

## Output Location
- Plans: `.claude/planning/` directory
- Tasks: `.claude/tasks/` directory
- Checkpoints: `.claude/checkpoints/` directory

## Tips for Success

1. **Resist the urge to code early** - Complete exploration first
2. **Use extended thinking** - Especially for architecture decisions
3. **Document assumptions** - Validate them during implementation
4. **Make atomic changes** - Easier to debug and rollback
5. **Keep commits focused** - One logical change per commit
