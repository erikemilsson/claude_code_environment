# Parallel Execution Gates

## Overview

Parallel execution gates are safety checks that validate whether multiple tasks can be executed simultaneously without conflicts or corruption. These gates are essential for maintaining data integrity and system stability when running tasks in parallel.

## Pre-Parallel-Execution Safety Checks

### 1. File Conflicts Detection

**Purpose**: Prevent simultaneous modification of the same files

**Check Types**:
- **BLOCKING (Write-Write)**: Both tasks modify the same file
- **WARNING (Read-Write)**: One task reads while another modifies
- **INFO (Read-Read)**: Both tasks only read the file

**Implementation**:
```python
from conflict_detector import ConflictDetector

detector = ConflictDetector()
can_parallel, blocking_conflicts = detector.validate_parallel_execution(task_ids)
```

**Resolution Strategies**:
- Execute conflicting tasks sequentially
- Partition files between tasks
- Use file locking mechanisms

### 2. Circular Dependencies Check

**Purpose**: Detect dependency loops that would cause deadlock

**Detection Algorithm**:
1. Build dependency graph from task dependencies
2. Perform depth-first search to find cycles
3. Report any circular dependency chains

**Example Circular Dependency**:
```
Task A → depends on → Task B
Task B → depends on → Task C
Task C → depends on → Task A  (CIRCULAR!)
```

**Resolution**:
- Break the dependency chain
- Refactor tasks to eliminate circular references
- Execute tasks in topological order

### 3. Lock Availability Check

**Purpose**: Ensure required file locks can be acquired

**Check Process**:
1. Enumerate all files affected by tasks
2. Check current lock status for each file
3. Predict lock contention scenarios

**Lock Types**:
- **Exclusive Lock**: Required for write operations
- **Shared Lock**: Sufficient for read operations

**Resolution**:
- Wait for locks to be released
- Use lock timeout with exponential backoff
- Queue tasks based on lock availability

### 4. Resource Capacity Check

**Purpose**: Prevent system overload from too many parallel tasks

**Resource Limits**:
- **Max Parallel Tasks**: 5 (configurable)
- **CPU Usage Threshold**: 80%
- **Memory Limit**: 70% of available RAM
- **File Handle Limit**: OS-dependent

**Monitoring**:
```python
resource_capacity = {
    "max_parallel_tasks": 5,
    "requested": len(task_ids),
    "available": max(0, 5 - active_task_count)
}
```

**Resolution**:
- Batch tasks into smaller groups
- Implement queue with rate limiting
- Use priority-based scheduling

### 5. Context Budget Check

**Purpose**: Ensure combined task complexity doesn't exceed processing capacity

**Complexity Calculation**:
```python
total_complexity = sum(task.difficulty for task in tasks)
max_complexity = 30  # Configurable threshold
```

**Factors**:
- Task difficulty scores (1-10)
- Expected execution time
- Context window consumption
- Error recovery overhead

**Resolution**:
- Split high-complexity task groups
- Execute complex tasks individually
- Use checkpoint/resume for long tasks

### 6. Shared Mutable State Check

**Purpose**: Identify shared resources that could cause race conditions

**Common Shared State**:
- Task counters and IDs
- Progress tracking files
- Shared configuration files
- Database connections
- API rate limit counters

**Protection Mechanisms**:
- Atomic operations for counters
- File locking for shared files
- Connection pooling for databases
- Distributed rate limiting

## ParallelExecutionGates Class Usage

### Basic Validation

```python
from validation_gates import ParallelExecutionGates

gates = ParallelExecutionGates()
task_ids = ["110_1", "110_2", "110_3"]

can_parallel, report = gates.validate_parallel_group(task_ids)

if can_parallel:
    print("Tasks can run in parallel")
else:
    print("Issues found:")
    for rec in report["recommendations"]:
        print(f"  - {rec}")
```

### Validation Report Structure

```json
{
    "can_parallel": false,
    "task_count": 3,
    "file_conflicts": [
        {
            "task1": "110_1",
            "task2": "110_2",
            "file": "/path/to/file.py",
            "type": "blocking"
        }
    ],
    "circular_dependencies": [],
    "lock_issues": [
        {
            "task": "110_3",
            "file": "/path/to/locked.json"
        }
    ],
    "resource_capacity": {
        "max_parallel_tasks": 5,
        "requested": 3,
        "available": 2
    },
    "context_budget": {
        "total_complexity": 18,
        "max_complexity": 30,
        "within_budget": true
    },
    "recommendations": [
        "Execute conflicting tasks sequentially",
        "Wait for file locks to be released"
    ]
}
```

### Batch Suggestion

```python
# Get optimal execution batches
batches = gates.suggest_execution_batches(all_task_ids)

for i, batch in enumerate(batches, 1):
    print(f"Batch {i} (can run in parallel):")
    for task_id in batch:
        print(f"  - Task {task_id}")
```

## Best Practices

### 1. Pre-Validation

Always validate before parallel execution:
```python
# Bad: Execute without checking
execute_parallel(task_ids)

# Good: Validate first
if gates.validate_parallel_group(task_ids)[0]:
    execute_parallel(task_ids)
else:
    execute_sequential(task_ids)
```

### 2. Progressive Batching

Start with smaller batches and increase gradually:
```python
def execute_with_progressive_batching(tasks):
    batch_sizes = [2, 3, 5]  # Progressive sizes

    for size in batch_sizes:
        batches = [tasks[i:i+size] for i in range(0, len(tasks), size)]
        for batch in batches:
            if validate_batch(batch):
                execute_parallel(batch)
            else:
                execute_sequential(batch)
```

### 3. Conflict Resolution Priority

1. **Eliminate conflicts**: Modify task definitions
2. **Partition resources**: Assign exclusive file sets
3. **Sequential fallback**: Run conflicting tasks one by one
4. **Retry with backoff**: For transient lock conflicts

### 4. Monitoring and Logging

```python
def execute_with_monitoring(task_ids):
    # Pre-execution validation
    can_parallel, report = gates.validate_parallel_group(task_ids)
    log_validation_report(report)

    if can_parallel:
        # Monitor during execution
        with parallel_execution_monitor(task_ids) as monitor:
            results = execute_parallel(task_ids)
            monitor.log_results(results)
    else:
        # Log why parallel execution was blocked
        log_blocking_reasons(report)
        results = execute_sequential(task_ids)

    return results
```

### 5. Error Recovery

Implement rollback for failed parallel executions:
```python
def safe_parallel_execution(task_ids):
    # Create checkpoint before execution
    checkpoint = create_checkpoint()

    try:
        if not validate_parallel(task_ids):
            raise ValueError("Validation failed")

        results = execute_parallel(task_ids)

        # Validate results
        if not validate_results(results):
            raise ValueError("Result validation failed")

        return results

    except Exception as e:
        # Rollback to checkpoint
        restore_checkpoint(checkpoint)
        # Fallback to sequential
        return execute_sequential(task_ids)
```

## Common Issues and Solutions

### Issue: File conflicts detected
**Solution**:
- Review `files_affected` fields in task definitions
- Use more specific file paths instead of wildcards
- Consider task ordering to avoid conflicts

### Issue: Lock timeout during validation
**Solution**:
- Increase timeout values
- Implement stale lock detection
- Use lock manager's cleanup function

### Issue: Context budget exceeded
**Solution**:
- Break down high-difficulty tasks
- Reduce batch sizes
- Use task prioritization

### Issue: Circular dependencies found
**Solution**:
- Review task dependency graph
- Refactor to eliminate cycles
- Use dependency analyzer to suggest order

## Configuration

### Environment Variables

```bash
# Maximum parallel tasks
export MAX_PARALLEL_TASKS=5

# Context complexity budget
export MAX_CONTEXT_COMPLEXITY=30

# Lock timeout in seconds
export LOCK_TIMEOUT=30

# Validation gate log level
export GATE_LOG_LEVEL=INFO
```

### Configuration File

`.claude/config/parallel-execution.json`:
```json
{
    "max_parallel_tasks": 5,
    "max_context_complexity": 30,
    "lock_timeout_seconds": 30,
    "retry_delays": [0.1, 0.5, 1.0, 2.0],
    "conflict_resolution": "sequential",
    "enable_monitoring": true,
    "checkpoint_frequency": 3
}
```

## Integration with Task System

### Command Line Usage

```bash
# Validate parallel execution
python validation-gates.py --validate-parallel 110_1 110_2 110_3

# Get execution batches
python conflict-detector.py --suggest 110_1 110_2 110_3 110_4

# Execute with validation
python task-manager.py execute --parallel --validate 110_1 110_2
```

### Programmatic Integration

```python
from validation_gates import ParallelExecutionGates
from task_manager import TaskManager

class SafeParallelExecutor:
    def __init__(self):
        self.gates = ParallelExecutionGates()
        self.task_manager = TaskManager()

    def execute_tasks(self, task_ids):
        # Validate
        can_parallel, report = self.gates.validate_parallel_group(task_ids)

        if can_parallel:
            # Execute in parallel with monitoring
            return self._execute_parallel_with_monitoring(task_ids)
        else:
            # Get suggested batches
            batches = self.gates.suggest_execution_batches(task_ids)
            return self._execute_batches(batches)
```

## Summary

Parallel execution gates provide comprehensive safety checks to ensure tasks can run simultaneously without conflicts. By implementing these checks, you can:

1. **Prevent data corruption** from concurrent file modifications
2. **Avoid deadlocks** from circular dependencies
3. **Manage resources** effectively
4. **Maintain system stability** under parallel load
5. **Provide clear feedback** on why tasks cannot run in parallel

Always validate before parallel execution and have a sequential fallback strategy for when parallel execution is not safe.