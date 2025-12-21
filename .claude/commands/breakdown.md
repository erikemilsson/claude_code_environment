# Breakdown Task Command

## Purpose
MUST split high-difficulty tasks (≥7) into manageable subtasks (≤6 difficulty each). This command now uses the **Task Orchestrator Agent** for intelligent task decomposition and hierarchy management.

## Agent Integration

**This command invokes the Task Orchestrator Agent**:
```markdown
AGENT: Task Orchestrator
PHASE: Task Planning
OWNERSHIP: Task breakdown, hierarchy management, dependency analysis
```

The Task Orchestrator will:
1. Analyze task complexity across multiple dimensions
2. Select optimal breakdown strategy
3. Create subtasks with minimal dependencies
4. Validate hierarchy and circular dependencies
5. Hand off to Execution Guardian when ready

## Context Required
- Task ID to break down
- Understanding of task scope and requirements
- `.claude/agents/task-orchestrator.md` - Agent definition
- `.claude/agent-config.json` - Agent ownership matrix

## Process (Agent-Driven)

### 1. Invoke Task Orchestrator
```markdown
User: "Break down task 003"

System: Task 003 has difficulty 8
System: Activating Task Orchestrator Agent

Task Orchestrator: "Analyzing task complexity..."
Task Orchestrator: "Evaluating breakdown strategies..."
```

### 2. Agent Performs Complexity Analysis
The Task Orchestrator will automatically:
- Assess technical, cognitive, operational complexity
- Identify integration points and uncertainties
- Determine optimal number of subtasks
- Select breakdown strategy (functional, architectural, temporal, etc.)

### 3. Agent Creates Subtasks
```markdown
Task Orchestrator: "Breaking down into 4 subtasks..."
Task Orchestrator: "Optimizing for parallel execution..."
Task Orchestrator: "Setting dependencies..."

Created subtasks:
- 003_1: "Design schema" (difficulty: 4)
- 003_2: "Create models" (difficulty: 3)
- 003_3: "Implement endpoints" (difficulty: 5)
- 003_4: "Add tests" (difficulty: 4)
```

### 4. Agent Validates Hierarchy
```markdown
Task Orchestrator: "Validating task hierarchy..."
Task Orchestrator: "No circular dependencies detected"
Task Orchestrator: "Critical path: 003_1 → 003_2 → 003_3"
Task Orchestrator: "Parallel possible: [003_3, 003_4]"
```

### 5. Agent Handoff
```markdown
Task Orchestrator: "Breakdown complete. 4 subtasks ready."
Task Orchestrator: "Updating parent status to 'Broken Down'"
Task Orchestrator: "Handing off to Execution Guardian for task 003_1..."

Execution Guardian: "Received handoff. Ready to execute subtasks..."
```

## Script Integration (If Available)

**The Task Orchestrator uses Python scripts for analysis:**
```bash
# Analyze complexity
python scripts/breakdown-suggester.py analyze --task-id {ID}

# Validate dependencies
python scripts/dependency-analyzer.py check --task-id {ID}

# Update hierarchy
python scripts/task-manager.py update-hierarchy --parent {ID}

# Sync overview
python scripts/task-manager.py sync-overview
```

## Manual Process (Fallback if agent unavailable)

### Pre-Breakdown Validation Gate [MANDATORY]

**BEFORE any breakdown, execute this gate:**
```
VALIDATION_GATE: breakdown_decision
├── CHECK: Task file exists and readable
├── CHECK: Difficulty >= 7 OR user requested
├── CHECK: Task can be decomposed logically
├── CHECK: Each subtask achievable at difficulty <= 6
├── CHECK: Clear dependency chain possible
├── CHECK: Not already broken down
└── RESULT:
    ├── PASS → Proceed with breakdown
    └── FAIL → Stop (explain why breakdown inappropriate)
```

1. **READ** task file `.claude/tasks/task-{id}.json`
2. **EXECUTE** Pre-Breakdown Validation Gate
   ```
   IF gate FAILS:
     IF difficulty < 7 AND not user requested:
       INFORM: "Task difficulty {X} doesn't require breakdown"
       STOP
     ELSE:
       EXPLAIN why breakdown cannot proceed
       SUGGEST alternatives
   ```
3. **ANALYZE AND DECOMPOSE** task:
   - IDENTIFY logical components
   - ENSURE each subtask is independently completable
   - ASSIGN difficulty ≤ 6 to each subtask
   - MAP dependencies between subtasks

**SUBTASK VALIDATION GATE [For each subtask]:**
```
VALIDATION_GATE: subtask_creation
├── CHECK: Difficulty <= 6
├── CHECK: Has clear deliverable/outcome
├── CHECK: Independently testable
├── CHECK: No circular dependencies
├── CHECK: Title is specific and actionable
└── RESULT:
    ├── PASS → Add to subtask list
    └── FAIL → Refine subtask definition
```
4. **CREATE subtask files IN PARALLEL**:
   - GENERATE unique IDs (parent_id_1, parent_id_2, etc.)
   - WRITE clear, imperative descriptions
   - SET `parent_task` field to original task ID
   - POPULATE dependency arrays
   - INITIALIZE progress tracking structure
5. **UPDATE parent task IMMEDIATELY**:
   - SET status = "Broken Down"
   - SET subtasks = [array of all subtask IDs]
   - ADD note: "Broken Down (0/X done)"
   - PRESERVE existing belief tracking data
6. **EXECUTE sync-tasks** to regenerate overview

## Output Location
- New task files: `.claude/tasks/task-{new-id}.json` for each subtask
- Updated parent task file
- Updated task-overview.md

## MANDATORY Rules

**ALWAYS:**
- CREATE all subtask files in a single parallel operation
- VERIFY each subtask difficulty ≤ 6
- ENSURE subtasks are independently testable
- SET parent task status to "Broken Down"
- PRESERVE all existing parent task data

**NEVER:**
- Work on parent task after breakdown
- Create subtasks with difficulty > 6
- Forget to set parent_task field in subtasks
- Skip dependency mapping
- Modify parent completion manually (auto-completes)

## Parallel Execution Opportunities

```markdown
PARALLEL OPERATIONS:
1. CREATE all subtask JSON files simultaneously
2. READ related documentation while analyzing

SEQUENTIAL REQUIREMENTS:
1. MUST read parent before creating subtasks
2. MUST update parent after creating subtasks
3. MUST run sync-tasks after all updates
```
