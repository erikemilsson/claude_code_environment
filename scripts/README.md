# Task Management Scripts Documentation

## Overview

This directory contains Python scripts that automate and enhance the task management system. These scripts handle deterministic operations at 10x speed compared to LLM operations, while preserving LLM capabilities for creative decisions.

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python claude-cli.py --version
```

### Basic Usage

```bash
# List all tasks
python claude-cli.py task list

# Validate a task before starting
python claude-cli.py validate pre TASK_ID

# Create a checkpoint
python claude-cli.py checkpoint create --description "Before major refactor"

# Check system health
python claude-cli.py metrics health
```

## Scripts Overview

### Core Scripts

#### 1. **task-manager.py**
Core task operations including validation, synchronization, and parent/child management.

**Key Functions:**
- `validate_task_schema()` - Validate task JSON against schema
- `sync_task_overview()` - Generate task-overview.md from JSON files
- `check_parent_completion()` - Auto-complete parent when subtasks finish
- `handle_breakdown()` - Create subtasks from parent task

**CLI Usage:**
```bash
python task-manager.py validate [--task-id ID]
python task-manager.py sync
python task-manager.py metrics
python task-manager.py breakdown --task-id ID --subtasks '{"title":"..."}'
```

#### 2. **validation-gates.py**
Pre and post-execution validation with blocking/warning/info levels.

**Key Features:**
- Pre-execution gates (status, dependencies, difficulty)
- Post-execution gates (completion, notes, parent updates)
- Breakdown enforcement (difficulty >= 7 must be broken down)

**CLI Usage:**
```bash
python validation-gates.py pre --task-id ID
python validation-gates.py post --task-id ID
python validation-gates.py validate-all
```

#### 3. **schema-validator.py**
Validate and auto-repair task JSON files.

**Key Features:**
- Schema validation against JSON schema
- Auto-repair missing fields
- Fix date format issues
- Repair broken references

**CLI Usage:**
```bash
python schema-validator.py validate
python schema-validator.py repair
python schema-validator.py health
```

### Automation Scripts

#### 4. **bootstrap.py**
Smart template detection and environment generation.

**Key Features:**
- Automatic template detection from spec content
- Pattern-based scoring algorithm
- Fast structure generation (2-3 seconds)
- Initial task creation from requirements

**CLI Usage:**
```bash
python bootstrap.py detect --spec spec.md
python bootstrap.py generate --spec spec.md --output ./project
python bootstrap.py bootstrap --spec spec.md --output ./project
```

#### 5. **pattern-matcher.py**
Fast keyword-based pattern matching.

**Key Features:**
- TF-IDF relevance scoring
- Error pattern suggestions
- Task breakdown patterns
- Complexity analysis

**CLI Usage:**
```bash
python pattern-matcher.py match --text "implement authentication"
python pattern-matcher.py suggest-errors --text "database migration"
python pattern-matcher.py suggest-breakdown --text "API development"
```

### Analysis Scripts

#### 6. **dependency-analyzer.py**
Analyze task dependency graphs.

**Key Features:**
- Circular dependency detection
- Critical path analysis
- Parallelizable task groups
- Impact analysis

**CLI Usage:**
```bash
python dependency-analyzer.py cycles
python dependency-analyzer.py critical-path
python dependency-analyzer.py parallel
python dependency-analyzer.py impact --task-id ID
```

#### 7. **metrics-dashboard.py**
Generate metrics and health scores.

**Key Features:**
- Velocity calculation
- Confidence trends
- Health score (0-100)
- Breakdown effectiveness

**CLI Usage:**
```bash
python metrics-dashboard.py health
python metrics-dashboard.py dashboard
python metrics-dashboard.py export
```

### Utility Scripts

#### 8. **checkpoint-manager.py**
Fast checkpoint creation and restore.

**Key Features:**
- SHA-256 integrity verification
- Compressed storage
- Diff between checkpoints
- Rollback capability

**CLI Usage:**
```bash
python checkpoint-manager.py create --description "Before refactor"
python checkpoint-manager.py list
python checkpoint-manager.py diff --checkpoint-id ID
python checkpoint-manager.py rollback --checkpoint-id ID --confirm
```

#### 9. **breakdown-suggester.py**
Smart task breakdown assistance.

**Key Features:**
- Historical pattern analysis
- Subtask count estimation
- Breakdown quality validation
- Success pattern learning

**CLI Usage:**
```bash
python breakdown-suggester.py suggest --task-id ID
python breakdown-suggester.py validate --task-id ID --subtasks '[...]'
python breakdown-suggester.py estimate --difficulty 8
```

### Unified CLI

#### 10. **claude-cli.py**
Single entry point for all operations.

**Command Groups:**
- `task` - Task management operations
- `validate` - Validation gates
- `bootstrap` - Environment generation
- `analyze` - Dependency analysis
- `metrics` - Metrics and health
- `checkpoint` - Checkpoint management

**Examples:**
```bash
# Task operations
claude-cli.py task list --status Pending
claude-cli.py task show TASK_ID
claude-cli.py task sync

# Validation
claude-cli.py validate pre TASK_ID
claude-cli.py validate all

# Bootstrap
claude-cli.py bootstrap detect spec.md
claude-cli.py bootstrap create spec.md --output ./new-project

# Analysis
claude-cli.py analyze cycles
claude-cli.py analyze critical

# Metrics
claude-cli.py metrics health
claude-cli.py metrics dashboard

# Checkpoints
claude-cli.py checkpoint create
claude-cli.py checkpoint list
```

## Integration Patterns

### LLM/Script Hybrid Workflow

1. **LLM Initiates**: LLM calls script for deterministic operations
2. **Script Validates**: Pre-execution gates ensure task readiness
3. **LLM Creates**: Creative work (descriptions, strategy)
4. **Script Manages**: JSON operations, sync, validation
5. **Script Reports**: Metrics, health scores, suggestions

### Command File Integration

Update `.claude/commands/*.md` files to call scripts:

```markdown
# complete-task.md

## Process
1. Run validation: `python scripts/validation-gates.py pre --task-id {ID}`
2. If gates pass, perform work
3. Update task: `python scripts/task-manager.py update --task-id {ID}`
4. Run post-validation: `python scripts/validation-gates.py post --task-id {ID}`
5. Sync overview: `python scripts/task-manager.py sync`
```

## Performance Benchmarks

| Operation | LLM Time | Script Time | Improvement |
|-----------|----------|-------------|-------------|
| JSON Validation | 2-3s | 50ms | 40-60x |
| Task Sync | 20-30s | 200ms | 100-150x |
| Pattern Matching | 5-10s | 100ms | 50-100x |
| Dependency Analysis | 10-15s | 150ms | 66-100x |
| Bootstrap Environment | 30-60s | 2-3s | 10-20x |

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `scripts/` is in Python path
   - Install all requirements: `pip install -r requirements.txt`

2. **JSON Validation Failures**
   - Run repair: `python schema-validator.py repair`
   - Check for circular dependencies: `python dependency-analyzer.py cycles`

3. **Performance Issues**
   - Create checkpoint: `python checkpoint-manager.py create`
   - Check health: `python metrics-dashboard.py health`

### Debug Mode

Set environment variable for verbose output:
```bash
export CLAUDE_DEBUG=1
python claude-cli.py task list
```

## API Reference

### TaskManager Class

```python
from task_manager import TaskManager

manager = TaskManager(base_path=".")
task = manager.load_task("task_id")
manager.save_task(task)
manager.sync_task_overview()
```

### ValidationGates Class

```python
from validation_gates import ValidationGates

gates = ValidationGates(base_path=".")
can_proceed, results = gates.run_pre_execution_gates("task_id")
```

### MetricsDashboard Class

```python
from metrics_dashboard import MetricsDashboard

dashboard = MetricsDashboard(base_path=".")
health = dashboard.generate_health_score()
```

## Contributing

When adding new scripts:
1. Follow existing patterns (CLI interface, error handling)
2. Add to `claude-cli.py` for unified access
3. Update this documentation
4. Add tests in `test-templates.py`
5. Ensure compatibility with command files

## License

Internal use only. Part of Claude Code Environment template system.