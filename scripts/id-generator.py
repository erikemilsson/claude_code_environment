#!/usr/bin/env python3
"""ID Generator - Safe task ID generation with collision prevention.

This module provides:
- Timestamp-based ID generation (format: task-{parent_id}_{timestamp}_{counter})
- ID reservation system to prevent collisions
- Atomic increment using file-based counter
- Rollback capability if task creation fails
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Set, Dict, Any
import threading
from contextlib import contextmanager

# Import file lock manager
try:
    from file_lock_manager import exclusive_lock, FileLockManager
    LOCKS_AVAILABLE = True
except ImportError:
    LOCKS_AVAILABLE = False
    print("Warning: File lock manager not available", file=sys.stderr)


class IDGenerator:
    """Manages safe generation of unique task IDs."""

    def __init__(self, registry_file: Path = None):
        """Initialize the ID generator.

        Args:
            registry_file: Path to ID registry (default: .claude/tasks/.id_registry.json)
        """
        if registry_file is None:
            # Find project root
            current = Path.cwd()
            while current != current.parent:
                if (current / '.claude').exists():
                    registry_file = current / '.claude' / 'tasks' / '.id_registry.json'
                    break
                current = current.parent
            else:
                registry_file = Path.cwd() / '.claude' / 'tasks' / '.id_registry.json'

        self.registry_file = Path(registry_file)
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)

        # Thread-local storage for reservations
        self._local = threading.local()

        # Initialize registry if it doesn't exist
        if not self.registry_file.exists():
            self._init_registry()

    def _init_registry(self):
        """Initialize the ID registry file."""
        initial_data = {
            'counter': 0,
            'reserved_ids': {},
            'used_ids': [],
            'timestamp': datetime.now().isoformat()
        }

        if LOCKS_AVAILABLE:
            with exclusive_lock(self.registry_file, timeout=30):
                with open(self.registry_file, 'w') as f:
                    json.dump(initial_data, f, indent=2)
        else:
            with open(self.registry_file, 'w') as f:
                json.dump(initial_data, f, indent=2)

    def _load_registry(self) -> Dict[str, Any]:
        """Load the ID registry with locking."""
        if not self.registry_file.exists():
            self._init_registry()

        if LOCKS_AVAILABLE:
            with exclusive_lock(self.registry_file, timeout=30):
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
        else:
            with open(self.registry_file, 'r') as f:
                return json.load(f)

    def _save_registry(self, data: Dict[str, Any]):
        """Save the ID registry with locking."""
        data['timestamp'] = datetime.now().isoformat()

        if LOCKS_AVAILABLE:
            with exclusive_lock(self.registry_file, timeout=30):
                with open(self.registry_file, 'w') as f:
                    json.dump(data, f, indent=2)
        else:
            with open(self.registry_file, 'w') as f:
                json.dump(data, f, indent=2)

    def _generate_timestamp_id(self, parent_id: Optional[str] = None) -> str:
        """Generate a timestamp-based ID.

        Format: task-{parent_id}_{YYYYMMDD-HHMMSS-microseconds}_{counter}
        """
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S") + f"-{now.microsecond:06d}"

        # Load and increment counter atomically
        registry = self._load_registry()
        counter = registry['counter'] + 1
        registry['counter'] = counter
        self._save_registry(registry)

        if parent_id:
            return f"task-{parent_id}_{timestamp}_{counter}"
        else:
            return f"task-{timestamp}_{counter}"

    @contextmanager
    def reserve_id(self, parent_id: Optional[str] = None,
                   custom_id: Optional[str] = None):
        """Reserve an ID to prevent collisions.

        Args:
            parent_id: Parent task ID for subtask generation
            custom_id: Specific ID to reserve (for compatibility)

        Yields:
            Reserved ID string

        Example:
            with id_gen.reserve_id(parent_id="110") as task_id:
                # Create task with this ID
                task = create_task(task_id)
                # ID is automatically marked as used on context exit
        """
        registry = self._load_registry()

        # Generate or validate ID
        if custom_id:
            # Check if custom ID is available
            if custom_id in registry['used_ids']:
                raise ValueError(f"ID {custom_id} is already in use")
            if custom_id in registry.get('reserved_ids', {}):
                # Check if reservation is stale (>60 seconds old)
                reserved_time = datetime.fromisoformat(registry['reserved_ids'][custom_id])
                if (datetime.now() - reserved_time).total_seconds() < 60:
                    raise ValueError(f"ID {custom_id} is currently reserved")
            task_id = custom_id
        else:
            # Generate new ID
            task_id = self._generate_timestamp_id(parent_id)

            # Ensure uniqueness
            while task_id in registry['used_ids'] or task_id in registry.get('reserved_ids', {}):
                time.sleep(0.001)  # Wait 1ms
                task_id = self._generate_timestamp_id(parent_id)

        # Reserve the ID
        registry['reserved_ids'][task_id] = datetime.now().isoformat()
        self._save_registry(registry)

        try:
            yield task_id

            # Mark as used on successful completion
            registry = self._load_registry()
            registry['used_ids'].append(task_id)
            registry['reserved_ids'].pop(task_id, None)
            self._save_registry(registry)

        except Exception:
            # On failure, release reservation
            registry = self._load_registry()
            registry['reserved_ids'].pop(task_id, None)
            self._save_registry(registry)
            raise

    def generate_subtask_ids(self, parent_id: str, count: int) -> list[str]:
        """Generate multiple subtask IDs atomically.

        Args:
            parent_id: Parent task ID
            count: Number of subtask IDs to generate

        Returns:
            List of reserved subtask IDs
        """
        ids = []
        registry = self._load_registry()

        for i in range(count):
            # Generate sequential IDs
            base_id = f"{parent_id}_{i+1}"

            # Ensure uniqueness
            task_id = base_id
            suffix = 1
            while task_id in registry['used_ids'] or task_id in ids:
                task_id = f"{base_id}_{suffix}"
                suffix += 1

            ids.append(task_id)
            registry['reserved_ids'][task_id] = datetime.now().isoformat()

        # Save all reservations atomically
        self._save_registry(registry)
        return ids

    def commit_ids(self, ids: list[str]):
        """Commit reserved IDs as used.

        Args:
            ids: List of IDs to commit
        """
        registry = self._load_registry()

        for task_id in ids:
            if task_id in registry['reserved_ids']:
                registry['used_ids'].append(task_id)
                del registry['reserved_ids'][task_id]

        self._save_registry(registry)

    def rollback_ids(self, ids: list[str]):
        """Release reserved IDs without using them.

        Args:
            ids: List of IDs to release
        """
        registry = self._load_registry()

        for task_id in ids:
            registry['reserved_ids'].pop(task_id, None)

        self._save_registry(registry)

    def cleanup_stale_reservations(self, timeout_seconds: int = 300):
        """Clean up reservations older than timeout.

        Args:
            timeout_seconds: Age in seconds before reservation is considered stale
        """
        registry = self._load_registry()
        now = datetime.now()
        stale_ids = []

        for task_id, reserved_time_str in registry.get('reserved_ids', {}).items():
            reserved_time = datetime.fromisoformat(reserved_time_str)
            if (now - reserved_time).total_seconds() > timeout_seconds:
                stale_ids.append(task_id)

        for task_id in stale_ids:
            del registry['reserved_ids'][task_id]

        if stale_ids:
            self._save_registry(registry)
            print(f"Cleaned up {len(stale_ids)} stale ID reservations")

    def get_next_sequential_id(self, parent_id: str) -> str:
        """Get next sequential ID for a parent task.

        Args:
            parent_id: Parent task ID

        Returns:
            Next available sequential ID (e.g., "110_1", "110_2")
        """
        registry = self._load_registry()

        # Find all existing subtask IDs for this parent
        existing = []
        prefix = f"{parent_id}_"

        for task_id in registry['used_ids']:
            if task_id.startswith(prefix):
                # Extract the number part
                try:
                    suffix = task_id[len(prefix):]
                    # Handle nested IDs like "110_1_2"
                    if '_' in suffix:
                        num = int(suffix.split('_')[0])
                    else:
                        num = int(suffix)
                    existing.append(num)
                except ValueError:
                    continue

        # Check reserved IDs too
        for task_id in registry.get('reserved_ids', {}).keys():
            if task_id.startswith(prefix):
                try:
                    suffix = task_id[len(prefix):]
                    if '_' in suffix:
                        num = int(suffix.split('_')[0])
                    else:
                        num = int(suffix)
                    existing.append(num)
                except ValueError:
                    continue

        # Find next available number
        if existing:
            next_num = max(existing) + 1
        else:
            next_num = 1

        return f"{parent_id}_{next_num}"


# Convenience functions
_default_generator = None

def get_default_generator() -> IDGenerator:
    """Get the default ID generator instance."""
    global _default_generator
    if _default_generator is None:
        _default_generator = IDGenerator()
    return _default_generator


def reserve_task_id(parent_id: Optional[str] = None):
    """Reserve a new task ID."""
    gen = get_default_generator()
    return gen.reserve_id(parent_id)


def generate_subtask_ids(parent_id: str, count: int) -> list[str]:
    """Generate multiple subtask IDs."""
    gen = get_default_generator()
    return gen.generate_subtask_ids(parent_id, count)


def get_next_id(parent_id: str) -> str:
    """Get next sequential ID for a parent."""
    gen = get_default_generator()
    return gen.get_next_sequential_id(parent_id)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: id-generator.py [test|next <parent_id>|cleanup]")
        sys.exit(1)

    command = sys.argv[1]
    gen = get_default_generator()

    if command == 'test':
        print("Testing ID generation...")

        # Test single ID reservation
        with gen.reserve_id(parent_id="110") as task_id:
            print(f"Reserved ID: {task_id}")
        print(f"ID committed: {task_id}")

        # Test multiple subtask IDs
        subtask_ids = gen.generate_subtask_ids("110", 3)
        print(f"Generated subtask IDs: {subtask_ids}")
        gen.commit_ids(subtask_ids)
        print("Subtask IDs committed")

        # Test rollback
        with gen.reserve_id(parent_id="111") as task_id:
            print(f"Reserved ID for rollback: {task_id}")
            raise RuntimeError("Simulated failure")

    elif command == 'next' and len(sys.argv) > 2:
        parent_id = sys.argv[2]
        next_id = gen.get_next_sequential_id(parent_id)
        print(f"Next ID for {parent_id}: {next_id}")

    elif command == 'cleanup':
        gen.cleanup_stale_reservations()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)