#!/usr/bin/env python3
"""
Task Manager - Core functions for task validation, sync, and management

This module provides the foundation for all task operations including:
- Task schema validation
- Parent/child relationship management
- Task overview synchronization
- Dependency checking
- Metrics calculation
- Breakdown operations
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import hashlib
from dataclasses import dataclass, asdict
import time

# Import file lock manager if available
try:
    from file_lock_manager import FileLockManager, shared_lock, exclusive_lock
    LOCKS_AVAILABLE = True
except ImportError:
    LOCKS_AVAILABLE = False
    print("Warning: File lock manager not available, running without locks", file=sys.stderr)
from enum import Enum


class TaskStatus(Enum):
    """Valid task statuses"""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    BROKEN_DOWN = "Broken Down"
    FINISHED = "Finished"


class MomentumPhase(Enum):
    """Task momentum phases"""
    INITIALIZING = "initializing"
    PENDING = "pending"
    IGNITION = "ignition"
    BUILDING = "building"
    CRUISING = "cruising"
    COASTING = "coasting"
    STALLING = "stalling"
    STOPPED = "stopped"


@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str
    difficulty: int
    status: str
    created_date: str
    updated_date: str
    completion_date: Optional[str] = None
    completion_notes: Optional[str] = None
    dependencies: List[str] = None
    subtasks: List[str] = None
    parent_task: Optional[str] = None
    files_affected: List[str] = None
    notes: Optional[str] = None
    confidence: int = 50
    assumptions: List[str] = None
    validation_status: str = "pending"
    momentum: Dict[str, Any] = None
    decision_rationale: Optional[str] = None

    def __post_init__(self):
        """Initialize default values"""
        if self.dependencies is None:
            self.dependencies = []
        if self.subtasks is None:
            self.subtasks = []
        if self.files_affected is None:
            self.files_affected = []
        if self.assumptions is None:
            self.assumptions = []
        if self.momentum is None:
            self.momentum = {
                "phase": "initializing",
                "velocity": 0,
                "last_activity": datetime.now().strftime("%Y-%m-%d")
            }


class TaskManager:
    """Core task management functionality"""

    def __init__(self, base_path: str = "."):
        """Initialize task manager with base path"""
        self.base_path = Path(base_path)
        self.tasks_dir = self.base_path / ".claude" / "tasks"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self._task_cache = {}

    def validate_task_schema(self, task_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate task data against schema

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        required_fields = ["id", "title", "description", "difficulty", "status",
                          "created_date", "updated_date"]

        # Check required fields
        for field in required_fields:
            if field not in task_data:
                errors.append(f"Missing required field: {field}")

        # Validate difficulty
        if "difficulty" in task_data:
            if not isinstance(task_data["difficulty"], int) or not 1 <= task_data["difficulty"] <= 10:
                errors.append("Difficulty must be an integer between 1 and 10")

        # Validate status
        if "status" in task_data:
            valid_statuses = [s.value for s in TaskStatus]
            if task_data["status"] not in valid_statuses:
                errors.append(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        # Validate dates
        for date_field in ["created_date", "updated_date", "completion_date"]:
            if date_field in task_data and task_data[date_field]:
                try:
                    datetime.strptime(task_data[date_field], "%Y-%m-%d")
                except ValueError:
                    errors.append(f"Invalid date format for {date_field}. Use YYYY-MM-DD")

        # Validate parent/subtask relationships
        if task_data.get("parent_task") and task_data.get("subtasks"):
            errors.append("Task cannot have both parent_task and subtasks")

        # Validate dependencies format
        if "dependencies" in task_data:
            if not isinstance(task_data["dependencies"], list):
                errors.append("Dependencies must be a list")

        # Validate confidence score
        if "confidence" in task_data:
            if not isinstance(task_data["confidence"], int) or not 0 <= task_data["confidence"] <= 100:
                errors.append("Confidence must be an integer between 0 and 100")

        return len(errors) == 0, errors

    def load_task(self, task_id: str, with_lock: bool = True) -> Optional[Task]:
        """Load a task from JSON file

        Args:
            task_id: ID of task to load
            with_lock: Whether to use file locking (default True)
        """
        task_file = self.tasks_dir / f"task-{task_id}.json"

        if not task_file.exists():
            return None

        # Retry logic for lock contention
        max_retries = 5
        retry_delay = 0.1  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                if with_lock and LOCKS_AVAILABLE:
                    # Use shared lock for reading
                    with shared_lock(task_file, timeout=30.0):
                        with open(task_file, 'r') as f:
                            data = json.load(f)
                            return Task(**data)
                else:
                    # No locking
                    with open(task_file, 'r') as f:
                        data = json.load(f)
                        return Task(**data)

            except TimeoutError as e:
                if attempt < max_retries - 1:
                    # Exponential backoff
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 2.0)
                    continue
                else:
                    print(f"Error: Could not acquire lock on task {task_id} after {max_retries} attempts: {e}")
                    return None

            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error loading task {task_id}: {e}")
                return None

        return None

    def save_task(self, task: Task, with_lock: bool = True) -> bool:
        """Save a task to JSON file

        Args:
            task: Task object to save
            with_lock: Whether to use file locking (default True)
        """
        task_file = self.tasks_dir / f"task-{task.id}.json"

        # Retry logic for lock contention
        max_retries = 5
        retry_delay = 0.1  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                # Update timestamps
                task.updated_date = datetime.now().strftime("%Y-%m-%d")
                if task.momentum:
                    task.momentum["last_activity"] = task.updated_date

                # Convert to dict
                task_data = asdict(task)

                if with_lock and LOCKS_AVAILABLE:
                    # Use exclusive lock for writing
                    with exclusive_lock(task_file, timeout=30.0):
                        with open(task_file, 'w') as f:
                            json.dump(task_data, f, indent=2)
                else:
                    # No locking
                    with open(task_file, 'w') as f:
                        json.dump(task_data, f, indent=2)

                # Clear cache for this task
                if task.id in self._task_cache:
                    del self._task_cache[task.id]

                return True

            except TimeoutError as e:
                if attempt < max_retries - 1:
                    # Exponential backoff
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 2.0)
                    continue
                else:
                    print(f"Error: Could not acquire lock on task {task.id} after {max_retries} attempts: {e}")
                    return False

            except Exception as e:
                print(f"Error saving task {task.id}: {e}")
                return False

        return False

    def create_subtask(self, parent_id: str, subtask_data: Dict) -> Optional[str]:
        """
        Create a new subtask for a parent task

        Args:
            parent_id: ID of the parent task
            subtask_data: Data for the new subtask

        Returns:
            ID of the created subtask or None if failed
        """
        parent = self.load_task(parent_id)
        if not parent:
            print(f"Parent task {parent_id} not found")
            return None

        # Generate subtask ID
        existing_subtasks = len(parent.subtasks) if parent.subtasks else 0
        subtask_id = f"{parent_id}_{existing_subtasks + 1}"

        # Set required fields
        subtask_data["id"] = subtask_id
        subtask_data["parent_task"] = parent_id
        subtask_data["created_date"] = datetime.now().strftime("%Y-%m-%d")
        subtask_data["updated_date"] = datetime.now().strftime("%Y-%m-%d")
        subtask_data["status"] = "Pending"

        # Validate and create task
        is_valid, errors = self.validate_task_schema(subtask_data)
        if not is_valid:
            print(f"Invalid subtask data: {', '.join(errors)}")
            return None

        subtask = Task(**subtask_data)
        if self.save_task(subtask):
            # Update parent task
            if parent.subtasks is None:
                parent.subtasks = []
            parent.subtasks.append(subtask_id)
            parent.status = TaskStatus.BROKEN_DOWN.value
            self.save_task(parent)
            return subtask_id

        return None

    def handle_breakdown(self, task_id: str, subtask_definitions: List[Dict]) -> List[str]:
        """
        Break down a task into subtasks

        Args:
            task_id: ID of task to break down
            subtask_definitions: List of subtask data dictionaries

        Returns:
            List of created subtask IDs
        """
        task = self.load_task(task_id)
        if not task:
            print(f"Task {task_id} not found")
            return []

        if task.difficulty < 7:
            print(f"Warning: Task {task_id} has difficulty {task.difficulty} (< 7)")

        created_subtasks = []
        for subtask_def in subtask_definitions:
            subtask_id = self.create_subtask(task_id, subtask_def)
            if subtask_id:
                created_subtasks.append(subtask_id)

        return created_subtasks

    def check_parent_completion(self, task_id: str) -> bool:
        """
        Check if parent task should be auto-completed

        Returns:
            True if parent was auto-completed
        """
        task = self.load_task(task_id)
        if not task or not task.parent_task:
            return False

        parent = self.load_task(task.parent_task)
        if not parent or parent.status == TaskStatus.FINISHED.value:
            return False

        # Check if all subtasks are finished
        all_finished = True
        for subtask_id in parent.subtasks:
            subtask = self.load_task(subtask_id)
            if not subtask or subtask.status != TaskStatus.FINISHED.value:
                all_finished = False
                break

        if all_finished:
            parent.status = TaskStatus.FINISHED.value
            parent.completion_date = datetime.now().strftime("%Y-%m-%d")
            parent.completion_notes = "Auto-completed: All subtasks finished"

            # Calculate average velocity from subtasks
            total_velocity = 0
            count = 0
            for subtask_id in parent.subtasks:
                subtask = self.load_task(subtask_id)
                if subtask and subtask.momentum and "velocity" in subtask.momentum:
                    total_velocity += subtask.momentum["velocity"]
                    count += 1

            if count > 0 and parent.momentum:
                parent.momentum["velocity"] = total_velocity // count
                parent.momentum["phase"] = "cruising"

            self.save_task(parent)
            return True

        return False

    def validate_dependencies(self, task_id: str) -> Tuple[bool, List[str]]:
        """
        Check if all dependencies are complete

        Returns:
            Tuple of (all_complete, list_of_incomplete_deps)
        """
        task = self.load_task(task_id)
        if not task:
            return False, [f"Task {task_id} not found"]

        incomplete = []
        for dep_id in task.dependencies:
            dep = self.load_task(dep_id)
            if not dep:
                incomplete.append(f"{dep_id} (not found)")
            elif dep.status != TaskStatus.FINISHED.value:
                incomplete.append(f"{dep_id} ({dep.status})")

        return len(incomplete) == 0, incomplete

    def calculate_task_metrics(self, task_id: str = None) -> Dict[str, Any]:
        """
        Calculate metrics for a task or all tasks

        Returns:
            Dictionary of metrics
        """
        if task_id:
            task = self.load_task(task_id)
            if not task:
                return {}

            return {
                "id": task.id,
                "title": task.title,
                "difficulty": task.difficulty,
                "status": task.status,
                "confidence": task.confidence,
                "momentum_phase": task.momentum.get("phase") if task.momentum else None,
                "velocity": task.momentum.get("velocity") if task.momentum else 0,
                "has_subtasks": len(task.subtasks) > 0 if task.subtasks else False,
                "is_subtask": task.parent_task is not None,
                "dependencies_count": len(task.dependencies) if task.dependencies else 0
            }
        else:
            # Calculate metrics for all tasks
            all_tasks = list(self.tasks_dir.glob("task-*.json"))
            metrics = {
                "total_tasks": len(all_tasks),
                "by_status": {},
                "by_difficulty": {},
                "average_confidence": 0,
                "average_velocity": 0,
                "breakdown_count": 0
            }

            total_confidence = 0
            total_velocity = 0
            velocity_count = 0

            for task_file in all_tasks:
                try:
                    with open(task_file, 'r') as f:
                        data = json.load(f)

                        # Status counts
                        status = data.get("status", "Unknown")
                        metrics["by_status"][status] = metrics["by_status"].get(status, 0) + 1

                        # Difficulty distribution
                        difficulty = data.get("difficulty", 0)
                        metrics["by_difficulty"][difficulty] = metrics["by_difficulty"].get(difficulty, 0) + 1

                        # Confidence
                        total_confidence += data.get("confidence", 50)

                        # Velocity
                        if data.get("momentum") and "velocity" in data["momentum"]:
                            total_velocity += data["momentum"]["velocity"]
                            velocity_count += 1

                        # Breakdown count
                        if data.get("subtasks"):
                            metrics["breakdown_count"] += 1

                except Exception:
                    pass

            if metrics["total_tasks"] > 0:
                metrics["average_confidence"] = total_confidence // metrics["total_tasks"]

            if velocity_count > 0:
                metrics["average_velocity"] = total_velocity // velocity_count

            return metrics

    def sync_task_overview(self) -> bool:
        """
        Synchronize task-overview.md from all task JSON files

        Returns:
            True if successful
        """
        overview_file = self.tasks_dir / "task-overview.md"

        try:
            # Collect all tasks
            tasks = []
            for task_file in sorted(self.tasks_dir.glob("task-*.json")):
                try:
                    with open(task_file, 'r') as f:
                        data = json.load(f)
                        tasks.append(data)
                except Exception as e:
                    print(f"Error reading {task_file}: {e}")

            # Sort tasks by ID (handling both numeric and hierarchical IDs)
            def sort_key(task):
                id_parts = task["id"].split("_")
                result = []
                for part in id_parts:
                    try:
                        result.append((0, int(part)))
                    except ValueError:
                        result.append((1, part))
                return tuple(result)

            tasks.sort(key=sort_key)

            # Generate markdown
            lines = ["# Task Overview\n"]
            lines.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
            lines.append("\n## Summary\n")

            # Calculate summary stats
            metrics = self.calculate_task_metrics()
            lines.append(f"- **Total Tasks**: {metrics['total_tasks']}\n")

            if metrics["by_status"]:
                status_summary = ", ".join([f"{count} {status}" for status, count in metrics["by_status"].items()])
                lines.append(f"- **Status**: {status_summary}\n")

            lines.append(f"- **Average Confidence**: {metrics['average_confidence']}%\n")
            lines.append(f"- **Average Velocity**: {metrics['average_velocity']}\n")
            lines.append(f"- **Tasks Broken Down**: {metrics['breakdown_count']}\n")

            # Task table
            lines.append("\n## Tasks\n")
            lines.append("| ID | Title | Difficulty | Status | Confidence | Dependencies | Notes |\n")
            lines.append("|---|---|---|---|---|---|---|\n")

            for task in tasks:
                # Format fields
                task_id = task["id"]

                # Add indentation for subtasks
                if "_" in task_id:
                    indent_level = task_id.count("_")
                    title = "&nbsp;" * (indent_level * 4) + "↳ " + task["title"]
                else:
                    title = task["title"]

                difficulty = task["difficulty"]
                status = task["status"]
                confidence = f"{task.get('confidence', 50)}%"

                # Format dependencies
                deps = task.get("dependencies", [])
                deps_str = ", ".join(deps) if deps else "-"

                # Truncate notes
                notes = task.get("notes", "")
                if len(notes) > 100:
                    notes = notes[:97] + "..."

                lines.append(f"| {task_id} | {title} | {difficulty} | {status} | {confidence} | {deps_str} | {notes} |\n")

            # Add archive summary if there are archived tasks
            archive_summary = self.get_archive_summary()
            if archive_summary:
                lines.append(archive_summary)

            # Write to file
            with open(overview_file, 'w') as f:
                f.writelines(lines)

            return True

        except Exception as e:
            print(f"Error syncing task overview: {e}")
            return False

    def get_all_task_ids(self) -> List[str]:
        """Get list of all task IDs"""
        task_ids = []
        for task_file in self.tasks_dir.glob("task-*.json"):
            # Extract ID from filename
            task_id = task_file.stem.replace("task-", "")
            task_ids.append(task_id)
        return sorted(task_ids)

    def bulk_update_status(self, task_ids: List[str], new_status: str) -> Dict[str, bool]:
        """
        Update status for multiple tasks

        Returns:
            Dictionary mapping task_id to success status
        """
        results = {}
        valid_statuses = [s.value for s in TaskStatus]

        if new_status not in valid_statuses:
            print(f"Invalid status: {new_status}")
            return {}

        for task_id in task_ids:
            task = self.load_task(task_id)
            if task:
                task.status = new_status
                if new_status == TaskStatus.FINISHED.value:
                    task.completion_date = datetime.now().strftime("%Y-%m-%d")
                results[task_id] = self.save_task(task)
            else:
                results[task_id] = False

        return results


    def atomic_status_update(self, task_id: str, from_status: str,
                           to_status: str) -> bool:
        """Atomically update task status with compare-and-swap.

        Args:
            task_id: Task ID to update
            from_status: Expected current status
            to_status: New status to set

        Returns:
            True if update succeeded, False if current status doesn't match
        """
        max_retries = 3
        retry_delay = 0.1

        for attempt in range(max_retries):
            try:
                # Load task with lock
                task = self.load_task(task_id, with_lock=True)
                if not task:
                    return False

                # Check current status matches expected
                current_status = task.status if isinstance(task.status, str) else task.status.value
                if current_status != from_status:
                    print(f"Status mismatch: expected {from_status}, got {current_status}")
                    return False

                # Update status
                task.status = to_status
                task.updated_date = datetime.now().strftime("%Y-%m-%d")

                # Save with exclusive lock
                if self.save_task(task, with_lock=True):
                    return True

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    print(f"Failed to atomically update status: {e}")
                    return False

        return False

    def atomic_field_update(self, task_id: str, field: str,
                          updater_func, with_lock: bool = True) -> bool:
        """Atomically update a task field with read-modify-write.

        Args:
            task_id: Task ID to update
            field: Field name to update
            updater_func: Function that takes current value and returns new value
            with_lock: Whether to use locking

        Returns:
            True if update succeeded
        """
        max_retries = 3
        retry_delay = 0.1

        for attempt in range(max_retries):
            try:
                # Load task with lock
                task = self.load_task(task_id, with_lock=with_lock)
                if not task:
                    return False

                # Get current value
                current_value = getattr(task, field, None)

                # Apply update function
                new_value = updater_func(current_value)

                # Set new value
                setattr(task, field, new_value)
                task.updated_date = datetime.now().strftime("%Y-%m-%d")

                # Save with exclusive lock
                if self.save_task(task, with_lock=with_lock):
                    return True

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    print(f"Failed to atomically update field {field}: {e}")
                    return False

        return False

    def atomic_add_to_list(self, task_id: str, field: str,
                          item: Any, unique: bool = True) -> bool:
        """Atomically add item to a list field.

        Args:
            task_id: Task ID to update
            field: List field name
            item: Item to add
            unique: Only add if not already present

        Returns:
            True if item was added
        """
        def updater(current_list):
            if not isinstance(current_list, list):
                current_list = []
            if unique and item in current_list:
                return current_list
            return current_list + [item]

        return self.atomic_field_update(task_id, field, updater)

    def atomic_remove_from_list(self, task_id: str, field: str, item: Any) -> bool:
        """Atomically remove item from a list field.

        Args:
            task_id: Task ID to update
            field: List field name
            item: Item to remove

        Returns:
            True if item was removed
        """
        def updater(current_list):
            if not isinstance(current_list, list):
                return []
            return [x for x in current_list if x != item]

        return self.atomic_field_update(task_id, field, updater)

    def atomic_increment(self, task_id: str, field: str, amount: int = 1) -> bool:
        """Atomically increment a numeric field.

        Args:
            task_id: Task ID to update
            field: Numeric field name
            amount: Amount to increment by

        Returns:
            True if incremented successfully
        """
        def updater(current_value):
            if current_value is None:
                return amount
            if not isinstance(current_value, (int, float)):
                raise ValueError(f"Field {field} is not numeric")
            return current_value + amount

        return self.atomic_field_update(task_id, field, updater)

    def batch_atomic_update(self, updates: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Perform multiple atomic updates in batch.

        Args:
            updates: List of update operations, each containing:
                     - task_id: Task to update
                     - operation: 'status', 'field', 'add_to_list', 'increment'
                     - parameters: Dict of operation-specific parameters

        Returns:
            Dict mapping task_id to success status
        """
        results = {}

        for update in updates:
            task_id = update['task_id']
            operation = update['operation']
            params = update.get('parameters', {})

            try:
                if operation == 'status':
                    success = self.atomic_status_update(
                        task_id,
                        params['from_status'],
                        params['to_status']
                    )
                elif operation == 'field':
                    success = self.atomic_field_update(
                        task_id,
                        params['field'],
                        params['updater_func']
                    )
                elif operation == 'add_to_list':
                    success = self.atomic_add_to_list(
                        task_id,
                        params['field'],
                        params['item'],
                        params.get('unique', True)
                    )
                elif operation == 'increment':
                    success = self.atomic_increment(
                        task_id,
                        params['field'],
                        params.get('amount', 1)
                    )
                else:
                    success = False
                    print(f"Unknown operation: {operation}")

                results[task_id] = success

            except Exception as e:
                print(f"Error in batch update for {task_id}: {e}")
                results[task_id] = False

        return results

    # ============================================
    # Archive Management Methods
    # ============================================

    def _get_archive_dir(self) -> Path:
        """Get or create archive directory"""
        archive_dir = self.tasks_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        return archive_dir

    def _get_archive_index_path(self) -> Path:
        """Get path to archive index file"""
        return self._get_archive_dir() / "archive-index.json"

    def get_archive_index(self) -> Dict[str, Any]:
        """
        Read archive-index.json

        Returns:
            Dictionary with archive metadata and task summaries
        """
        index_path = self._get_archive_index_path()
        if not index_path.exists():
            return {"archived_at": None, "count": 0, "tasks": []}

        try:
            with open(index_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading archive index: {e}")
            return {"archived_at": None, "count": 0, "tasks": []}

    def _save_archive_index(self, index: Dict[str, Any]) -> bool:
        """Save archive index to file"""
        index_path = self._get_archive_index_path()
        try:
            index["archived_at"] = datetime.now().strftime("%Y-%m-%d")
            index["count"] = len(index.get("tasks", []))
            with open(index_path, 'w') as f:
                json.dump(index, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving archive index: {e}")
            return False

    def _is_safe_to_archive(self, task_id: str) -> Tuple[bool, str]:
        """
        Check if a task can be safely archived

        Returns:
            Tuple of (is_safe, reason_if_not_safe)
        """
        task = self.load_task(task_id)
        if not task:
            return False, f"Task {task_id} not found"

        # Must be finished
        if task.status != TaskStatus.FINISHED.value:
            return False, f"Task {task_id} is not finished (status: {task.status})"

        # Check if any active tasks depend on this one
        all_task_ids = self.get_all_task_ids()
        for other_id in all_task_ids:
            if other_id == task_id:
                continue
            other_task = self.load_task(other_id)
            if other_task and other_task.dependencies:
                if task_id in other_task.dependencies:
                    if other_task.status != TaskStatus.FINISHED.value:
                        return False, f"Active task {other_id} depends on {task_id}"

        return True, ""

    def _get_subtask_ids(self, task_id: str) -> List[str]:
        """Get all subtask IDs for a parent task"""
        task = self.load_task(task_id)
        if not task or not task.subtasks:
            return []
        return list(task.subtasks)

    def archive_completed_tasks(self, days_old: int = 7, dry_run: bool = False) -> List[str]:
        """
        Move finished tasks older than N days to archive

        Args:
            days_old: Only archive tasks finished more than this many days ago
            dry_run: If True, just return what would be archived without moving

        Returns:
            List of archived task IDs
        """
        archive_dir = self._get_archive_dir()
        archived = []
        cutoff_date = datetime.now() - __import__('datetime').timedelta(days=days_old)

        # Get all task IDs
        all_task_ids = self.get_all_task_ids()

        # Find archivable tasks (parents first, then subtasks)
        archivable = []
        for task_id in all_task_ids:
            task = self.load_task(task_id)
            if not task:
                continue

            # Skip subtasks - they'll be handled with their parents
            if task.parent_task:
                continue

            # Check if finished and old enough
            if task.status != TaskStatus.FINISHED.value:
                continue

            if task.completion_date:
                try:
                    completion = datetime.strptime(task.completion_date, "%Y-%m-%d")
                    if completion > cutoff_date:
                        continue
                except ValueError:
                    continue
            else:
                continue

            # Check if safe to archive
            is_safe, reason = self._is_safe_to_archive(task_id)
            if not is_safe:
                print(f"Skipping {task_id}: {reason}")
                continue

            archivable.append(task_id)

        if dry_run:
            print(f"Would archive {len(archivable)} tasks:")
            for task_id in archivable:
                task = self.load_task(task_id)
                subtasks = self._get_subtask_ids(task_id)
                if subtasks:
                    print(f"  {task_id}: {task.title} (+ {len(subtasks)} subtasks)")
                else:
                    print(f"  {task_id}: {task.title}")
            return archivable

        # Load existing archive index
        index = self.get_archive_index()

        # Archive each task
        for task_id in archivable:
            task = self.load_task(task_id)
            if not task:
                continue

            # Get subtasks to archive with parent
            subtask_ids = self._get_subtask_ids(task_id)

            # Move parent task file
            src_file = self.tasks_dir / f"task-{task_id}.json"
            dst_file = archive_dir / f"task-{task_id}.json"

            try:
                import shutil
                shutil.move(str(src_file), str(dst_file))
                archived.append(task_id)

                # Add to index (lightweight summary only)
                index["tasks"].append({
                    "id": task_id,
                    "title": task.title,
                    "completion_date": task.completion_date,
                    "difficulty": task.difficulty
                })

                # Move subtask files
                for subtask_id in subtask_ids:
                    subtask_src = self.tasks_dir / f"task-{subtask_id}.json"
                    subtask_dst = archive_dir / f"task-{subtask_id}.json"
                    if subtask_src.exists():
                        shutil.move(str(subtask_src), str(subtask_dst))
                        archived.append(subtask_id)

            except Exception as e:
                print(f"Error archiving {task_id}: {e}")

        # Save updated index
        self._save_archive_index(index)

        print(f"Archived {len(archived)} tasks")
        return archived

    def restore_from_archive(self, task_id: str) -> bool:
        """
        Move task back from archive to active

        Args:
            task_id: ID of task to restore

        Returns:
            True if successful
        """
        archive_dir = self._get_archive_dir()
        src_file = archive_dir / f"task-{task_id}.json"

        if not src_file.exists():
            print(f"Task {task_id} not found in archive")
            return False

        dst_file = self.tasks_dir / f"task-{task_id}.json"

        try:
            import shutil
            shutil.move(str(src_file), str(dst_file))

            # Update archive index
            index = self.get_archive_index()
            index["tasks"] = [t for t in index["tasks"] if t["id"] != task_id]
            self._save_archive_index(index)

            # Check if this is a parent task with subtasks
            task = self.load_task(task_id)
            if task and task.subtasks:
                for subtask_id in task.subtasks:
                    subtask_src = archive_dir / f"task-{subtask_id}.json"
                    subtask_dst = self.tasks_dir / f"task-{subtask_id}.json"
                    if subtask_src.exists():
                        shutil.move(str(subtask_src), str(subtask_dst))

            print(f"Restored task {task_id}")
            return True

        except Exception as e:
            print(f"Error restoring {task_id}: {e}")
            return False

    def get_archive_summary(self) -> str:
        """
        Get a brief summary of archived tasks for display

        Returns:
            Markdown-formatted summary string
        """
        index = self.get_archive_index()
        if index["count"] == 0:
            return ""

        return f"\n## Archived ({index['count']} tasks)\nLast archived: {index['archived_at']}\n"


def main():
    """CLI interface for task manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Task Manager - Core task operations")
    parser.add_argument("command", choices=["validate", "sync", "metrics", "breakdown", "list", "archive", "restore"],
                       help="Command to execute")
    parser.add_argument("--task-id", help="Task ID for operations")
    parser.add_argument("--subtasks", nargs="+", help="Subtask definitions (JSON strings)")
    parser.add_argument("--base-path", default=".", help="Base project path")
    parser.add_argument("--days", type=int, default=7, help="Days old for archive (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without doing it")

    args = parser.parse_args()

    manager = TaskManager(args.base_path)

    if args.command == "validate":
        if args.task_id:
            task = manager.load_task(args.task_id)
            if task:
                is_valid, errors = manager.validate_task_schema(asdict(task))
                if is_valid:
                    print(f"Task {args.task_id} is valid")
                else:
                    print(f"Task {args.task_id} has errors:")
                    for error in errors:
                        print(f"  - {error}")
            else:
                print(f"Task {args.task_id} not found")
        else:
            # Validate all tasks
            task_ids = manager.get_all_task_ids()
            invalid_count = 0
            for task_id in task_ids:
                task = manager.load_task(task_id)
                if task:
                    is_valid, errors = manager.validate_task_schema(asdict(task))
                    if not is_valid:
                        print(f"Task {task_id}: {', '.join(errors)}")
                        invalid_count += 1

            if invalid_count == 0:
                print(f"All {len(task_ids)} tasks are valid")
            else:
                print(f"Found {invalid_count} invalid tasks out of {len(task_ids)}")

    elif args.command == "sync":
        if manager.sync_task_overview():
            print("Task overview synchronized successfully")
        else:
            print("Failed to sync task overview")

    elif args.command == "metrics":
        if args.task_id:
            metrics = manager.calculate_task_metrics(args.task_id)
            if metrics:
                print(json.dumps(metrics, indent=2))
            else:
                print(f"Task {args.task_id} not found")
        else:
            metrics = manager.calculate_task_metrics()
            print(json.dumps(metrics, indent=2))

    elif args.command == "breakdown":
        if not args.task_id:
            print("Task ID required for breakdown")
            return

        if not args.subtasks:
            print("Subtask definitions required")
            return

        subtask_defs = []
        for subtask_json in args.subtasks:
            try:
                subtask_defs.append(json.loads(subtask_json))
            except json.JSONDecodeError:
                print(f"Invalid JSON: {subtask_json}")
                return

        created = manager.handle_breakdown(args.task_id, subtask_defs)
        if created:
            print(f"Created {len(created)} subtasks: {', '.join(created)}")
        else:
            print("Failed to create subtasks")

    elif args.command == "list":
        task_ids = manager.get_all_task_ids()
        print(f"Found {len(task_ids)} tasks:")
        for task_id in task_ids:
            task = manager.load_task(task_id)
            if task:
                print(f"  {task_id}: {task.title} ({task.status})")

    elif args.command == "archive":
        archived = manager.archive_completed_tasks(days_old=args.days, dry_run=args.dry_run)
        if not args.dry_run and archived:
            # Sync overview after archiving
            manager.sync_task_overview()

    elif args.command == "restore":
        if not args.task_id:
            print("Task ID required for restore")
            return
        if manager.restore_from_archive(args.task_id):
            # Sync overview after restoring
            manager.sync_task_overview()


if __name__ == "__main__":
    main()