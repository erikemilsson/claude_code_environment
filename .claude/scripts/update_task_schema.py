#!/usr/bin/env python3
"""
Update all task JSON files to include belief-tracking fields.
Adds confidence, assumptions, validation_status, momentum, and decision_rationale fields.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def update_task_json(filepath):
    """Add belief-tracking fields to a task JSON file."""
    with open(filepath, 'r') as f:
        task = json.load(f)

    # Add new fields if they don't exist
    if 'confidence' not in task:
        task['confidence'] = 75  # Default medium-high confidence

    if 'assumptions' not in task:
        task['assumptions'] = []

    if 'validation_status' not in task:
        task['validation_status'] = 'pending'

    if 'momentum' not in task:
        task['momentum'] = {
            'phase': 'pending',  # pending/ignition/building/cruising/coasting/stalling/stopped
            'velocity': 0,
            'last_activity': task.get('updated_date', task.get('created_date', str(datetime.now().date())))
        }

    if 'decision_rationale' not in task:
        task['decision_rationale'] = ""

    # Write updated task back
    with open(filepath, 'w') as f:
        json.dump(task, f, indent=2)

    return task['id']

def main():
    """Update all task JSON files in the tasks directory."""
    tasks_dir = Path(__file__).parent.parent / 'tasks'
    updated_tasks = []

    # Process all JSON files
    for json_file in sorted(tasks_dir.glob('task-*.json')):
        try:
            task_id = update_task_json(json_file)
            updated_tasks.append(task_id)
            print(f"Updated task {task_id}: {json_file.name}")
        except Exception as e:
            print(f"Error updating {json_file.name}: {e}")

    print(f"\nSuccessfully updated {len(updated_tasks)} task files with belief-tracking fields.")
    print("New fields added:")
    print("  - confidence: 0-100 score (default: 75)")
    print("  - assumptions: array of assumption objects")
    print("  - validation_status: pending/validated/invalidated")
    print("  - momentum: phase, velocity, last_activity tracking")
    print("  - decision_rationale: text field for decision explanations")

if __name__ == "__main__":
    main()