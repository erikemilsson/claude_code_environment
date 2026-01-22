# Claude Opus 4.5 Guide

*Consolidated reference for Claude Opus 4.5 tool usage and patterns.*

## Core Capabilities

### Parallel Tool Execution

Claude Opus 4.5 executes multiple tool calls in parallel within a single message. Use this for independent operations.

**Execute in PARALLEL when:**
- Operations are independent
- All parameters known upfront
- Different target resources
- Read-only or non-conflicting operations

**Execute SEQUENTIALLY when:**
- Output dependencies exist
- State changes affect next operation
- Need error handling between steps
- Order matters for correctness

### Proactive Execution

| Confidence | Claude Opus 4.5 Behavior |
|------------|-------------------------|
| >90% | Proceeds automatically |
| 70-90% | Single confirmation if needed |
| 50-70% | 1-2 targeted questions |
| <50% | Full requirements gathering |

## Tool Usage Hierarchy

### File Operations
| Operation | Use | Never Use |
|-----------|-----|-----------|
| Read file | Read tool | cat, head, tail via Bash |
| Edit file | Edit tool | sed, awk via Bash |
| Create file | Write tool | echo >, cat > via Bash |
| Find files | Glob tool | find via Bash |
| Search content | Grep tool | grep via Bash |
| Complex search | Task (Explore agent) | Multiple manual searches |

### Parallel Patterns

**File Reading:**
```
PARALLEL: Read task-1.json, task-2.json, task-3.json
Result: All data in one operation
```

**Mixed Operations:**
```
PARALLEL in single message:
- Read CLAUDE.md
- Grep for "TODO" comments
- Bash: git status
- Glob for "*.test.js"
```

**Sequential (when needed):**
```
SEQUENTIAL via &&: git add . && git commit -m "msg" && git push
```

## Performance Patterns

### Information Gathering
1. **PARALLEL**: Gather all information needed
2. **PROCESS**: Analyze gathered data
3. **PARALLEL**: Apply all changes

### Batch Operations
Instead of loop-based sequential:
```
# BAD: Sequential
for file in files: read(file)

# GOOD: Parallel
Read all files in single message
```

### Preemptive Reads
When starting any task:
```
PARALLEL READ:
- Task file
- Configuration
- Parent task
- Documentation
```

## Instruction Style

### Imperative Over Suggestive
```markdown
# Claude 3.5 style (avoid)
"You should read the task file first"
"Consider checking if complete"

# Claude Opus 4.5 style (use)
"READ task file"
"VALIDATE status != Finished"
"STOP if already complete"
```

### Explicit Actions
```markdown
EXECUTE these steps WITHOUT deviation:
1. READ task file
2. VALIDATE pre-conditions
3. UPDATE status immediately
4. DOCUMENT changes
```

## Anti-Patterns

### Avoid Sequential When Parallel Possible
```
# BAD
Read file A → Process → Read file B → Process

# GOOD
[Read A, Read B] → Process all
```

### Avoid Unnecessary Serialization
```
# BAD
Check if file exists → Then read file

# GOOD
Just read file (handle error if doesn't exist)
```

### Avoid Over-Explanation
```
# BAD
"Let me explain what I'm going to do..."

# GOOD
"Reading and updating files."
[Execute]
```

## Performance Metrics

| Operation | Sequential | Parallel | Improvement |
|-----------|------------|----------|-------------|
| Read 5 files | 5 sec | 1 sec | 80% faster |
| Run 4 bash commands | 4 sec | 1 sec | 75% faster |
| Search 10 patterns | 10 sec | 2 sec | 80% faster |

### Parallelization Limits
- **Optimal batch**: 5-10 operations
- **Maximum**: 20 operations
- **Split if**: >20 needed

## Integration with Tasks

### Parallel Task Operations
```
# Starting: Update multiple task statuses
PARALLEL: Edit task-1.json, task-2.json, task-3.json

# Checking: Read all dependency tasks
PARALLEL: Read dep files

# Completing: Write all updates
1. PARALLEL: Read all related tasks
2. SEQUENTIAL: Update based on dependencies
3. PARALLEL: Write all updates
```

## Quick Reference

### PARALLEL
- Multiple file reads
- Independent bash commands
- Different grep searches
- Bulk task updates
- Information gathering

### SEQUENTIAL
- Dependent operations
- Chained commands (&&)
- Progressive refinement
- State modifications
- Ordered workflows
