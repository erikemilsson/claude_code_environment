# Parallel Tool Execution Patterns for Claude 4

*Version: 1.0 | Created: 2025-12-16*

## Overview

Claude 4 (Opus 4.1 and Sonnet 4.5) can execute multiple tool calls in parallel within a single message, dramatically improving performance. This reference provides patterns, anti-patterns, and decision criteria for parallel execution.

## Core Principle

**ALWAYS execute independent operations in parallel.**

Send multiple tool calls in a single message when:
- No data dependencies exist between operations
- Operations target different resources
- All required parameters are known upfront

## Pattern Categories

### 1. File Operations

#### ✅ PATTERN: Parallel File Reading

**When:** Reading multiple independent files

```markdown
# CORRECT - Parallel execution
Read task-1.json, task-2.json, task-3.json simultaneously

# Implementation
Single message with 3 Read tool calls
```

**Example Scenarios:**
- Reading all task files for status check
- Loading multiple configuration files
- Gathering context from various documentation files

#### ✅ PATTERN: Parallel Search Operations

**When:** Searching for different patterns or in different locations

```markdown
# CORRECT - Parallel execution
- Grep for "TODO" in *.js files
- Glob for "test-*.json" patterns
- Search for "error" in log files

# Implementation
Single message with Grep, Glob, and another Grep tool call
```

#### ❌ ANTI-PATTERN: Sequential Dependent Reads

**Never parallelize when:**
- Second read depends on first read's content
- Need to check file existence before reading
- Building incremental context

```markdown
# INCORRECT - Don't parallelize
1. Read index.json to get file list
2. Read files from that list

# CORRECT - Sequential execution
Read index.json first, THEN read listed files
```

### 2. Bash Commands

#### ✅ PATTERN: Independent System Commands

**When:** Running unrelated system commands

```markdown
# CORRECT - Parallel execution
- git status
- npm list
- python --version
- docker ps

# Implementation
Single message with 4 Bash tool calls
```

#### ✅ PATTERN: Parallel Test Execution

**When:** Running independent test suites

```markdown
# CORRECT - Parallel execution
- pytest tests/unit/
- pytest tests/integration/
- npm test

# Implementation
Single message with 3 Bash tool calls
```

#### ❌ ANTI-PATTERN: Dependent Command Chains

**Never parallelize when:**
- Commands must run in specific order
- Output of one feeds into another
- State changes affect subsequent commands

```markdown
# INCORRECT - Don't parallelize
- git add .
- git commit -m "message"
- git push

# CORRECT - Use && for sequential
Single Bash call: git add . && git commit -m "message" && git push
```

### 3. Task Management

#### ✅ PATTERN: Bulk Task Updates

**When:** Updating multiple independent tasks

```markdown
# CORRECT - Parallel execution
Update status for tasks 23, 24, 25, 26 simultaneously

# Implementation
Single message with 4 Edit tool calls on different task files
```

#### ✅ PATTERN: Parallel Task Creation

**When:** Creating multiple subtasks

```markdown
# CORRECT - Parallel execution
Create subtask files 78_1.json through 78_5.json

# Implementation
Single message with 5 Write tool calls
```

### 4. Mixed Operations

#### ✅ PATTERN: Comprehensive Project Analysis

**When:** Gathering diverse project information

```markdown
# CORRECT - Parallel execution in single message:
- Read CLAUDE.md
- Grep for "TODO" comments
- Bash: git status
- Glob for "*.test.js" files
- Read package.json

# Result: Complete project context in one operation
```

#### ✅ PATTERN: Environment Setup Verification

**When:** Checking multiple prerequisites

```markdown
# CORRECT - Parallel execution:
- Check Python version
- Check Node version
- Check Docker status
- Verify database connection
- Read config files

# Implementation
Single message with multiple Bash and Read calls
```

## Decision Framework

### Execute in PARALLEL when:

```markdown
✅ Operations are independent
✅ All parameters known upfront
✅ No shared state modifications
✅ Different target resources
✅ Read-only operations
✅ Gathering information phase
```

### Execute SEQUENTIALLY when:

```markdown
❌ Output dependencies exist
❌ State changes affect next operation
❌ Need error handling between steps
❌ Building on previous results
❌ Resource conflicts possible
❌ Order matters for correctness
```

## Performance Patterns

### Pattern: Information Gathering First

```markdown
# OPTIMAL APPROACH
1. PARALLEL: Gather all information needed
   - Read multiple files
   - Run status commands
   - Search operations

2. PROCESS: Analyze gathered data

3. PARALLEL: Apply all changes
   - Write multiple files
   - Update configurations
   - Create new resources
```

### Pattern: Batch Similar Operations

```markdown
# INSTEAD OF:
Loop through files one by one

# DO:
Identify all files first, then operate on ALL simultaneously
```

### Pattern: Preemptive Parallel Reads

```markdown
# When starting any task:
PARALLEL READ:
- Task file
- Related configuration
- Parent task (if exists)
- Documentation
- Current state files

# Result: Full context immediately available
```

## Common Scenarios

### Scenario: Code Review Preparation

```markdown
PARALLEL EXECUTION:
1. Git diff for changes
2. Read all modified files
3. Run linting commands
4. Check test coverage
5. Read coding standards

SINGLE MESSAGE with 5+ tool calls
```

### Scenario: Bug Investigation

```markdown
PARALLEL EXECUTION:
1. Grep for error messages
2. Read log files
3. Check recent commits
4. Read related source files
5. Check issue tracker

SINGLE MESSAGE with mixed tool calls
```

### Scenario: Project Initialization

```markdown
PARALLEL EXECUTION:
1. Create directory structure
2. Write configuration files
3. Initialize git repository
4. Install dependencies
5. Create initial documentation

SINGLE MESSAGE with multiple Write and Bash calls
```

## Implementation Examples

### Example 1: Task Status Check

```markdown
# COMMAND: "Check status of tasks 10-15"

# PARALLEL IMPLEMENTATION:
Single message with:
- Read task-10.json
- Read task-11.json
- Read task-12.json
- Read task-13.json
- Read task-14.json
- Read task-15.json

# Result: All data retrieved in one operation
```

### Example 2: Multi-File Search

```markdown
# COMMAND: "Find all API endpoints"

# PARALLEL IMPLEMENTATION:
Single message with:
- Grep "app.get\\|app.post\\|app.put\\|app.delete" in *.js
- Grep "@RestController\\|@GetMapping" in *.java
- Grep "Route::get\\|Route::post" in *.php
- Read routes configuration files

# Result: Complete endpoint inventory instantly
```

### Example 3: Dependency Check

```markdown
# COMMAND: "Verify all dependencies installed"

# PARALLEL IMPLEMENTATION:
Single message with:
- Bash: python -m pip list
- Bash: npm list
- Bash: gem list
- Bash: cargo --version
- Read requirements.txt
- Read package.json
- Read Gemfile
- Read Cargo.toml

# Result: Full dependency status in one operation
```

## Anti-Patterns to Avoid

### ❌ Sequential Information Gathering

```markdown
# BAD:
Read file1
Process file1
Read file2
Process file2
Read file3
Process file3

# GOOD:
Read file1, file2, file3 (parallel)
Process all together
```

### ❌ Unnecessary Serialization

```markdown
# BAD:
Check if file exists
Then read file

# GOOD:
Just read file (handle error if doesn't exist)
```

### ❌ Loop-Based Operations

```markdown
# BAD:
for file in files:
    read(file)

# GOOD:
read_all(files)  # Single parallel operation
```

## Performance Metrics

### Expected Improvements

| Operation Type | Sequential Time | Parallel Time | Improvement |
|---------------|-----------------|---------------|-------------|
| Read 5 files | 5 seconds | 1 second | 80% faster |
| Run 4 bash commands | 4 seconds | 1 second | 75% faster |
| Search 10 patterns | 10 seconds | 2 seconds | 80% faster |
| Update 6 tasks | 6 seconds | 1 second | 83% faster |

### Parallelization Limits

- **Optimal batch size:** 5-10 operations
- **Maximum recommended:** 20 operations
- **Consider splitting if:** >20 operations needed

## Tool-Specific Guidelines

### Read Tool
- **Parallelize:** Reading different files
- **Don't parallelize:** Reading with calculated offsets

### Grep Tool
- **Parallelize:** Different search patterns or paths
- **Don't parallelize:** Dependent search refinements

### Bash Tool
- **Parallelize:** Independent commands
- **Don't parallelize:** Commands with && or ; chains

### Write Tool
- **Parallelize:** Creating multiple new files
- **Don't parallelize:** Incremental file updates

### Edit Tool
- **Parallelize:** Editing different files
- **Don't parallelize:** Multiple edits to same file

## Integration with Task System

### Parallel Task Operations

```markdown
# Starting multiple tasks:
PARALLEL: Update all task statuses to "In Progress"

# Checking dependencies:
PARALLEL: Read all dependency task files

# Completing tasks:
1. PARALLEL: Read all related tasks
2. SEQUENTIAL: Update based on dependencies
3. PARALLEL: Write all updates
```

## Best Practices Summary

1. **DEFAULT TO PARALLEL** - Unless dependencies exist
2. **BATCH SIMILAR OPERATIONS** - Group reads, writes, searches
3. **GATHER THEN PROCESS** - Parallel read, sequential logic, parallel write
4. **EXPLICIT OVER IMPLICIT** - State why operations must be sequential
5. **MEASURE IMPROVEMENT** - Track time saved through parallelization

## Quick Reference Card

```markdown
PARALLEL ✅
- Multiple file reads
- Independent bash commands
- Different grep searches
- Bulk task updates
- Information gathering
- Status checks
- Independent validations

SEQUENTIAL ❌
- Dependent operations
- Chained commands (&&)
- Progressive refinement
- Error recovery flows
- State modifications
- Ordered workflows
- Resource conflicts
```

## Conclusion

Parallel tool execution is one of the most significant performance improvements in Claude 4. By following these patterns and avoiding anti-patterns, execution time can be reduced by 75-85% for many common operations. Always ask: "Can these operations run simultaneously?" If yes, execute them in parallel within a single message.