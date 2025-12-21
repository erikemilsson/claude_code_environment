#!/usr/bin/env python3
"""File Conflict Detector - Detects file conflicts between parallel tasks.

This module provides:
- Detection of overlapping files_affected fields across parallel tasks
- Classification of conflicts as BLOCKING (write-write) or WARNING (read-write)
- Pattern matching for file globs
- Directory overlap detection
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import fnmatch
import re


class ConflictType(Enum):
    """Types of file conflicts."""
    NONE = "none"
    BLOCKING = "blocking"  # Write-write conflict
    WARNING = "warning"    # Read-write conflict
    INFO = "info"         # Read-read (no conflict but informational)


@dataclass
class FileConflict:
    """Represents a file conflict between tasks."""
    file_path: str
    task1_id: str
    task2_id: str
    conflict_type: ConflictType
    task1_operation: str  # 'read' or 'write'
    task2_operation: str  # 'read' or 'write'
    message: str


class ConflictDetector:
    """Detects and analyzes file conflicts between tasks."""

    def __init__(self, tasks_dir: Path = None):
        """Initialize the conflict detector.

        Args:
            tasks_dir: Directory containing task JSON files
        """
        if tasks_dir is None:
            # Find project root
            current = Path.cwd()
            while current != current.parent:
                if (current / '.claude').exists():
                    tasks_dir = current / '.claude' / 'tasks'
                    break
                current = current.parent
            else:
                tasks_dir = Path.cwd() / '.claude' / 'tasks'

        self.tasks_dir = Path(tasks_dir)

    def _expand_pattern(self, pattern: str, base_dir: Path = None) -> Set[Path]:
        """Expand a glob pattern to actual file paths.

        Args:
            pattern: Glob pattern (e.g., "src/**/*.py")
            base_dir: Base directory for relative patterns

        Returns:
            Set of matched file paths
        """
        if base_dir is None:
            base_dir = Path.cwd()

        # Handle absolute paths
        if pattern.startswith('/'):
            base_dir = Path('/')
            pattern = pattern[1:]

        # Convert pattern to Path
        pattern_path = base_dir / pattern

        # Check if it's a specific file (no wildcards)
        if not any(char in pattern for char in ['*', '?', '[', ']']):
            if pattern_path.exists():
                return {pattern_path.resolve()}
            else:
                # File doesn't exist yet but might be created
                return {pattern_path.resolve()}

        # Handle glob patterns
        matched = set()

        # Try to match existing files
        try:
            for match in base_dir.glob(pattern):
                matched.add(match.resolve())
        except Exception:
            pass

        # If pattern ends with /, it's a directory pattern
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/') + '/**/*'
            try:
                for match in base_dir.glob(pattern):
                    matched.add(match.resolve())
            except Exception:
                pass

        return matched

    def _analyze_file_operation(self, task_data: Dict[str, Any],
                               file_path: str) -> str:
        """Determine if a task will read or write a file.

        Args:
            task_data: Task dictionary
            file_path: File path to analyze

        Returns:
            'read', 'write', or 'unknown'
        """
        # Analyze task description and title for operation hints
        description = task_data.get('description', '').lower()
        title = task_data.get('title', '').lower()
        combined_text = f"{title} {description}"

        # Keywords indicating write operations
        write_keywords = [
            'create', 'write', 'generate', 'implement', 'add', 'modify',
            'update', 'enhance', 'refactor', 'fix', 'patch', 'delete',
            'remove', 'replace', 'save', 'export', 'build', 'compile'
        ]

        # Keywords indicating read-only operations
        read_keywords = [
            'read', 'analyze', 'review', 'check', 'validate', 'test',
            'verify', 'inspect', 'examine', 'audit', 'search', 'find',
            'document', 'report'
        ]

        # Check file extension for hints
        file_ext = Path(file_path).suffix.lower()

        # Documentation files are usually read or updated
        doc_extensions = ['.md', '.txt', '.rst', '.doc', '.pdf']
        if file_ext in doc_extensions:
            if any(keyword in combined_text for keyword in ['create', 'write', 'update']):
                return 'write'
            else:
                return 'read'

        # Count keyword matches
        write_score = sum(1 for keyword in write_keywords if keyword in combined_text)
        read_score = sum(1 for keyword in read_keywords if keyword in combined_text)

        # Determine operation based on scores
        if write_score > read_score:
            return 'write'
        elif read_score > write_score:
            return 'read'
        else:
            # Default to write for safety (more conservative)
            return 'write'

    def detect_conflicts(self, task_ids: List[str]) -> List[FileConflict]:
        """Detect file conflicts between specified tasks.

        Args:
            task_ids: List of task IDs to check

        Returns:
            List of detected conflicts
        """
        conflicts = []
        task_files = {}

        # Load tasks and expand their file patterns
        for task_id in task_ids:
            task_file = self.tasks_dir / f"task-{task_id}.json"
            if not task_file.exists():
                print(f"Warning: Task {task_id} not found", file=sys.stderr)
                continue

            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)

                # Get files affected by this task
                files_affected = task_data.get('files_affected', [])
                expanded_files = set()

                for file_pattern in files_affected:
                    # Expand pattern to actual files
                    matched = self._expand_pattern(file_pattern)
                    expanded_files.update(matched)

                # Store with operation type
                task_files[task_id] = {
                    'files': expanded_files,
                    'data': task_data,
                    'operations': {}
                }

                # Determine operation for each file
                for file_path in expanded_files:
                    operation = self._analyze_file_operation(task_data, str(file_path))
                    task_files[task_id]['operations'][file_path] = operation

            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading task {task_id}: {e}", file=sys.stderr)
                continue

        # Check for conflicts between all pairs of tasks
        task_id_list = list(task_files.keys())
        for i, task1_id in enumerate(task_id_list):
            for task2_id in task_id_list[i + 1:]:
                task1 = task_files[task1_id]
                task2 = task_files[task2_id]

                # Find overlapping files
                overlapping = task1['files'] & task2['files']

                for file_path in overlapping:
                    op1 = task1['operations'].get(file_path, 'unknown')
                    op2 = task2['operations'].get(file_path, 'unknown')

                    # Determine conflict type
                    if op1 == 'write' and op2 == 'write':
                        conflict_type = ConflictType.BLOCKING
                        message = f"Both tasks will modify {file_path}"
                    elif (op1 == 'write' and op2 == 'read') or \
                         (op1 == 'read' and op2 == 'write'):
                        conflict_type = ConflictType.WARNING
                        message = f"Read-write conflict on {file_path}"
                    elif op1 == 'read' and op2 == 'read':
                        conflict_type = ConflictType.INFO
                        message = f"Both tasks will read {file_path}"
                    else:
                        conflict_type = ConflictType.WARNING
                        message = f"Potential conflict on {file_path} (operations unclear)"

                    conflict = FileConflict(
                        file_path=str(file_path),
                        task1_id=task1_id,
                        task2_id=task2_id,
                        conflict_type=conflict_type,
                        task1_operation=op1,
                        task2_operation=op2,
                        message=message
                    )

                    conflicts.append(conflict)

        return conflicts

    def check_directory_overlaps(self, task_ids: List[str]) -> List[FileConflict]:
        """Check for directory-level overlaps that might cause conflicts.

        Args:
            task_ids: List of task IDs to check

        Returns:
            List of directory overlap conflicts
        """
        conflicts = []
        task_dirs = {}

        # Extract directory patterns from tasks
        for task_id in task_ids:
            task_file = self.tasks_dir / f"task-{task_id}.json"
            if not task_file.exists():
                continue

            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)

                files_affected = task_data.get('files_affected', [])
                directories = set()

                for file_pattern in files_affected:
                    # Extract directory part
                    if file_pattern.endswith('/'):
                        directories.add(Path(file_pattern))
                    else:
                        parent = Path(file_pattern).parent
                        if str(parent) != '.':
                            directories.add(parent)

                task_dirs[task_id] = {
                    'dirs': directories,
                    'data': task_data
                }

            except Exception as e:
                print(f"Error processing task {task_id}: {e}", file=sys.stderr)
                continue

        # Check for overlapping directories
        task_id_list = list(task_dirs.keys())
        for i, task1_id in enumerate(task_id_list):
            for task2_id in task_id_list[i + 1:]:
                dirs1 = task_dirs[task1_id]['dirs']
                dirs2 = task_dirs[task2_id]['dirs']

                # Check if any directories overlap or are parent/child
                for dir1 in dirs1:
                    for dir2 in dirs2:
                        if dir1 == dir2:
                            conflict = FileConflict(
                                file_path=str(dir1),
                                task1_id=task1_id,
                                task2_id=task2_id,
                                conflict_type=ConflictType.WARNING,
                                task1_operation='directory',
                                task2_operation='directory',
                                message=f"Both tasks affect directory {dir1}"
                            )
                            conflicts.append(conflict)
                        elif dir1 in dir2.parents:
                            conflict = FileConflict(
                                file_path=f"{dir1} -> {dir2}",
                                task1_id=task1_id,
                                task2_id=task2_id,
                                conflict_type=ConflictType.INFO,
                                task1_operation='parent_dir',
                                task2_operation='child_dir',
                                message=f"Task {task1_id} affects parent directory of task {task2_id}"
                            )
                            conflicts.append(conflict)
                        elif dir2 in dir1.parents:
                            conflict = FileConflict(
                                file_path=f"{dir2} -> {dir1}",
                                task1_id=task2_id,
                                task2_id=task1_id,
                                conflict_type=ConflictType.INFO,
                                task1_operation='parent_dir',
                                task2_operation='child_dir',
                                message=f"Task {task2_id} affects parent directory of task {task1_id}"
                            )
                            conflicts.append(conflict)

        return conflicts

    def validate_parallel_execution(self, task_ids: List[str]) -> Tuple[bool, List[FileConflict]]:
        """Validate if tasks can be executed in parallel.

        Args:
            task_ids: List of task IDs to validate

        Returns:
            Tuple of (can_parallel, blocking_conflicts)
        """
        # Detect all conflicts
        conflicts = self.detect_conflicts(task_ids)

        # Filter blocking conflicts
        blocking_conflicts = [
            c for c in conflicts
            if c.conflict_type == ConflictType.BLOCKING
        ]

        can_parallel = len(blocking_conflicts) == 0
        return can_parallel, blocking_conflicts

    def suggest_execution_order(self, task_ids: List[str]) -> List[List[str]]:
        """Suggest execution order for tasks with conflicts.

        Args:
            task_ids: List of task IDs

        Returns:
            List of task groups that can run in parallel
        """
        # Build conflict graph
        conflict_graph = {task_id: set() for task_id in task_ids}
        conflicts = self.detect_conflicts(task_ids)

        for conflict in conflicts:
            if conflict.conflict_type == ConflictType.BLOCKING:
                conflict_graph[conflict.task1_id].add(conflict.task2_id)
                conflict_graph[conflict.task2_id].add(conflict.task1_id)

        # Group tasks that don't conflict
        groups = []
        remaining = set(task_ids)

        while remaining:
            # Find tasks that don't conflict with each other
            current_group = []
            for task_id in list(remaining):
                # Check if this task conflicts with any in current group
                has_conflict = False
                for group_task in current_group:
                    if group_task in conflict_graph[task_id]:
                        has_conflict = True
                        break

                if not has_conflict:
                    current_group.append(task_id)
                    remaining.remove(task_id)

            if current_group:
                groups.append(current_group)
            else:
                # Shouldn't happen, but handle edge case
                groups.append(list(remaining))
                break

        return groups


def main():
    """CLI interface for conflict detection."""
    if len(sys.argv) < 2:
        print("Usage: conflict-detector.py <task_id1> <task_id2> [...]")
        print("       conflict-detector.py --validate <task_id1> <task_id2> [...]")
        print("       conflict-detector.py --suggest <task_id1> <task_id2> [...]")
        sys.exit(1)

    detector = ConflictDetector()

    if sys.argv[1] == '--validate':
        # Validate parallel execution
        task_ids = sys.argv[2:]
        can_parallel, blocking = detector.validate_parallel_execution(task_ids)

        if can_parallel:
            print(f"✓ Tasks {task_ids} can run in parallel")
        else:
            print(f"✗ Tasks {task_ids} have blocking conflicts:")
            for conflict in blocking:
                print(f"  - {conflict.message}")
                print(f"    Tasks: {conflict.task1_id} vs {conflict.task2_id}")

    elif sys.argv[1] == '--suggest':
        # Suggest execution order
        task_ids = sys.argv[2:]
        groups = detector.suggest_execution_order(task_ids)

        print("Suggested execution order:")
        for i, group in enumerate(groups, 1):
            print(f"  Phase {i}: {', '.join(group)} (can run in parallel)")

    else:
        # Detect all conflicts
        task_ids = sys.argv[1:]
        conflicts = detector.detect_conflicts(task_ids)

        if not conflicts:
            print(f"No conflicts detected between tasks: {task_ids}")
        else:
            print(f"Conflicts detected ({len(conflicts)} total):")

            # Group by type
            blocking = [c for c in conflicts if c.conflict_type == ConflictType.BLOCKING]
            warnings = [c for c in conflicts if c.conflict_type == ConflictType.WARNING]
            info = [c for c in conflicts if c.conflict_type == ConflictType.INFO]

            if blocking:
                print(f"\nBLOCKING conflicts ({len(blocking)}):")
                for conflict in blocking:
                    print(f"  ✗ {conflict.message}")
                    print(f"    {conflict.task1_id} ({conflict.task1_operation}) vs "
                          f"{conflict.task2_id} ({conflict.task2_operation})")

            if warnings:
                print(f"\nWARNING conflicts ({len(warnings)}):")
                for conflict in warnings:
                    print(f"  ⚠ {conflict.message}")
                    print(f"    {conflict.task1_id} ({conflict.task1_operation}) vs "
                          f"{conflict.task2_id} ({conflict.task2_operation})")

            if info:
                print(f"\nINFO conflicts ({len(info)}):")
                for conflict in info:
                    print(f"  ℹ {conflict.message}")


if __name__ == '__main__':
    main()