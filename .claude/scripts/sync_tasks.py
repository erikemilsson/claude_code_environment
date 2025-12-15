#!/usr/bin/env python3
"""Sync tasks to generate task overview"""

import json
import os
from pathlib import Path
from datetime import datetime

# Task directory
task_dir = Path('.claude/tasks')

# Collect all tasks
tasks = []
for task_file in sorted(task_dir.glob('task-*.json')):
    if task_file.stem.startswith('task-'):
        with open(task_file, 'r') as f:
            task = json.load(f)
            tasks.append(task)

# Sort by ID numerically
tasks.sort(key=lambda x: int(x['id']))

# Calculate statistics
status_counts = {'Pending': 0, 'In Progress': 0, 'Finished': 0, 'Broken Down': 0, 'Blocked': 0}
difficulty_counts = {
    '1-2': {'count': 0, 'completed': 0},
    '3-4': {'count': 0, 'completed': 0},
    '5-6': {'count': 0, 'completed': 0},
    '7-8': {'count': 0, 'completed': 0},
    '9-10': {'count': 0, 'completed': 0}
}

for task in tasks:
    status = task.get('status', 'Pending')
    status_counts[status] = status_counts.get(status, 0) + 1

    diff = task.get('difficulty', 0)
    if 1 <= diff <= 2:
        difficulty_counts['1-2']['count'] += 1
        if status == 'Finished':
            difficulty_counts['1-2']['completed'] += 1
    elif 3 <= diff <= 4:
        difficulty_counts['3-4']['count'] += 1
        if status == 'Finished':
            difficulty_counts['3-4']['completed'] += 1
    elif 5 <= diff <= 6:
        difficulty_counts['5-6']['count'] += 1
        if status == 'Finished':
            difficulty_counts['5-6']['completed'] += 1
    elif 7 <= diff <= 8:
        difficulty_counts['7-8']['count'] += 1
        if status == 'Finished':
            difficulty_counts['7-8']['completed'] += 1
    elif 9 <= diff <= 10:
        difficulty_counts['9-10']['count'] += 1
        if status == 'Finished':
            difficulty_counts['9-10']['completed'] += 1

# Calculate totals
total_tasks = len(tasks)
completed_tasks = status_counts.get('Finished', 0)
completion_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

# Generate progress bar
progress_filled = int(completion_pct // 5)
progress_empty = 20 - progress_filled
progress_bar = '█' * progress_filled + '░' * progress_empty

# Generate overview markdown
output = f'''# Task Overview

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

## Statistics

### Overall Progress
- **Total Tasks:** {total_tasks}
- **Completed:** {completed_tasks} ({completion_pct:.0f}%)
- **In Progress:** {status_counts.get('In Progress', 0)} ({status_counts.get('In Progress', 0)/total_tasks*100:.0f}%)
- **Pending:** {status_counts.get('Pending', 0)} ({status_counts.get('Pending', 0)/total_tasks*100:.0f}%)
- **Blocked:** {status_counts.get('Blocked', 0)} ({status_counts.get('Blocked', 0)/total_tasks*100:.0f}%)
- **Broken Down:** {status_counts.get('Broken Down', 0)} ({status_counts.get('Broken Down', 0)/total_tasks*100:.0f}%)

**Progress:** `{progress_bar}` {completion_pct:.0f}%

### By Status
| Status | Count | Percentage |
|--------|-------|------------|
| Finished | {status_counts.get('Finished', 0)} | {status_counts.get('Finished', 0)/total_tasks*100:.0f}% |
| Pending | {status_counts.get('Pending', 0)} | {status_counts.get('Pending', 0)/total_tasks*100:.0f}% |
| In Progress | {status_counts.get('In Progress', 0)} | {status_counts.get('In Progress', 0)/total_tasks*100:.0f}% |
| Blocked | {status_counts.get('Blocked', 0)} | {status_counts.get('Blocked', 0)/total_tasks*100:.0f}% |
| Broken Down | {status_counts.get('Broken Down', 0)} | {status_counts.get('Broken Down', 0)/total_tasks*100:.0f}% |

### By Difficulty
| Difficulty Range | Count | Completed | Percentage |
|-----------------|-------|-----------|------------|'''

# Add difficulty rows
for diff_range in ['1-2', '3-4', '5-6', '7-8', '9-10']:
    diff_label = {
        '1-2': '1-2 (Trivial)',
        '3-4': '3-4 (Low)',
        '5-6': '5-6 (Moderate)',
        '7-8': '7-8 (High)',
        '9-10': '9-10 (Extreme)'
    }[diff_range]

    count = difficulty_counts[diff_range]['count']
    completed = difficulty_counts[diff_range]['completed']
    pct = (completed / count * 100) if count > 0 else 0
    pct_str = f"{pct:.0f}%" if count > 0 else "-"

    output += f"\n| {diff_label} | {count} | {completed} | {pct_str} |"

output += '''

## All Tasks

| ID | Title | Status | Difficulty | Dependencies | Subtasks | Parent |
|----|-------|--------|------------|--------------|----------|--------|'''

# Add task rows
for task in tasks:
    status_icon = {
        'Finished': '✅',
        'In Progress': '⏳',
        'Broken Down': '📦',
        'Blocked': '🚫',
        'Pending': '⏸️'
    }.get(task.get('status', 'Pending'), '⏸️')

    title = task['title']
    if len(title) > 60:
        title = title[:60] + '...'

    deps = ', '.join(task.get('dependencies', [])) if task.get('dependencies') else '-'
    subtasks = ', '.join(task.get('subtasks', [])) if task.get('subtasks') else '-'
    parent = task.get('parent_task', '-')

    output += f"\n| {task['id']} | {title} | {status_icon} {task.get('status', 'Pending')} | {task.get('difficulty', '-')} | {deps} | {subtasks} | {parent} |"

# Add notes section for new integration
output += '''

## Recent Updates

### Belief Tracker Integration (Task 60)
- **17 new subtasks** created for comprehensive belief tracking integration
- Features to be implemented:
  - Enhanced task schema with confidence and momentum tracking
  - Assumption validation system
  - Pattern detection and emerging insights
  - Decision tracking and rationale logging
  - Project health dashboard with visualizations
  - Two-step processing for improved accuracy'''

# Write to file
overview_path = task_dir / 'task-overview.md'
with open(overview_path, 'w') as f:
    f.write(output)

print(f'✅ Task overview updated successfully!')
print(f'📊 Total tasks: {total_tasks}')
print(f'🆕 New tasks: 18 (task 60 + 17 subtasks)')
print(f'🎯 Belief tracker integration tasks created!')