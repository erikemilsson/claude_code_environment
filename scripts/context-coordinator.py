#!/usr/bin/env python3
"""Context Coordinator - Manages shared context between parallel execution agents.

This module provides:
- Session registration and heartbeat
- Context publication and subscription
- Stale session detection (60s timeout)
- Context merging on conflicts
- Storage in .claude/shared-context/ directory
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import threading
from collections import defaultdict

# Import file lock manager if available
try:
    from file_lock_manager import exclusive_lock, FileLockManager
    LOCKS_AVAILABLE = True
except ImportError:
    LOCKS_AVAILABLE = False
    print("Warning: File lock manager not available", file=sys.stderr)


class ContextType(Enum):
    """Types of shared context"""
    DISCOVERY = "discovery"        # Discovered information about the codebase
    DECISION = "decision"          # Design decisions made
    ISSUE = "issue"               # Problems encountered
    SOLUTION = "solution"         # Solutions found
    PROGRESS = "progress"         # Task progress updates
    CONFLICT = "conflict"         # Conflicts detected
    RESOURCE = "resource"         # Resource usage/availability


@dataclass
class ContextEntry:
    """Represents a piece of shared context"""
    id: str
    session_id: str
    type: ContextType
    key: str
    value: Any
    timestamp: str
    task_id: Optional[str] = None
    metadata: Optional[Dict] = None


@dataclass
class Session:
    """Represents an agent session"""
    id: str
    task_ids: List[str]
    started_at: str
    last_heartbeat: str
    status: str  # 'active', 'stale', 'completed'
    agent_type: Optional[str] = None


class ContextCoordinator:
    """Coordinates context sharing between parallel agents"""

    def __init__(self, context_dir: Path = None):
        """Initialize the context coordinator.

        Args:
            context_dir: Directory for shared context storage
        """
        if context_dir is None:
            # Find project root
            current = Path.cwd()
            while current != current.parent:
                if (current / '.claude').exists():
                    context_dir = current / '.claude' / 'shared-context'
                    break
                current = current.parent
            else:
                context_dir = Path.cwd() / '.claude' / 'shared-context'

        self.context_dir = Path(context_dir)
        self.context_dir.mkdir(parents=True, exist_ok=True)

        # File paths
        self.sessions_file = self.context_dir / 'sessions.json'
        self.context_file = self.context_dir / 'context.json'
        self.subscriptions_file = self.context_dir / 'subscriptions.json'

        # Initialize files if they don't exist
        self._init_files()

        # Local cache
        self._session_id = None
        self._subscriptions = set()

    def _init_files(self):
        """Initialize storage files if they don't exist"""
        for file_path, initial_data in [
            (self.sessions_file, {"sessions": {}}),
            (self.context_file, {"entries": []}),
            (self.subscriptions_file, {"subscriptions": {}})
        ]:
            if not file_path.exists():
                self._write_json(file_path, initial_data)

    def _read_json(self, file_path: Path) -> Dict:
        """Read JSON file with locking"""
        if LOCKS_AVAILABLE:
            with exclusive_lock(file_path, timeout=30):
                with open(file_path, 'r') as f:
                    return json.load(f)
        else:
            with open(file_path, 'r') as f:
                return json.load(f)

    def _write_json(self, file_path: Path, data: Dict):
        """Write JSON file with locking"""
        if LOCKS_AVAILABLE:
            with exclusive_lock(file_path, timeout=30):
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
        else:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

    def register_session(self, task_ids: List[str],
                        agent_type: Optional[str] = None) -> str:
        """Register a new agent session.

        Args:
            task_ids: List of tasks this session will work on
            agent_type: Type of agent (e.g., 'executor', 'validator')

        Returns:
            Session ID
        """
        # Generate session ID
        session_id = hashlib.md5(
            f"{datetime.now().isoformat()}_{os.getpid()}".encode()
        ).hexdigest()[:16]

        # Create session
        session = Session(
            id=session_id,
            task_ids=task_ids,
            started_at=datetime.now().isoformat(),
            last_heartbeat=datetime.now().isoformat(),
            status='active',
            agent_type=agent_type
        )

        # Save session
        data = self._read_json(self.sessions_file)
        data['sessions'][session_id] = asdict(session)
        self._write_json(self.sessions_file, data)

        # Store session ID locally
        self._session_id = session_id

        # Clean up stale sessions
        self.cleanup_stale_sessions()

        return session_id

    def heartbeat(self, session_id: Optional[str] = None):
        """Send heartbeat for session.

        Args:
            session_id: Session ID (uses stored ID if not provided)
        """
        if session_id is None:
            session_id = self._session_id

        if not session_id:
            return

        data = self._read_json(self.sessions_file)
        if session_id in data['sessions']:
            data['sessions'][session_id]['last_heartbeat'] = datetime.now().isoformat()
            self._write_json(self.sessions_file, data)

    def publish_context(self, context_type: ContextType, key: str, value: Any,
                       task_id: Optional[str] = None,
                       metadata: Optional[Dict] = None):
        """Publish context for other agents to consume.

        Args:
            context_type: Type of context
            key: Context key (e.g., 'database_schema', 'api_endpoint')
            value: Context value
            task_id: Associated task ID
            metadata: Additional metadata
        """
        if not self._session_id:
            raise ValueError("No active session. Call register_session first.")

        # Create context entry
        entry = ContextEntry(
            id=hashlib.md5(f"{key}_{time.time()}".encode()).hexdigest()[:16],
            session_id=self._session_id,
            type=context_type,
            key=key,
            value=value,
            timestamp=datetime.now().isoformat(),
            task_id=task_id,
            metadata=metadata or {}
        )

        # Save to context file
        data = self._read_json(self.context_file)
        data['entries'].append(asdict(entry))

        # Keep only recent entries (last 1000)
        if len(data['entries']) > 1000:
            data['entries'] = data['entries'][-1000:]

        self._write_json(self.context_file, data)

        # Trigger subscriptions
        self._notify_subscribers(key, entry)

    def subscribe(self, keys: List[str], callback=None):
        """Subscribe to context updates for specific keys.

        Args:
            keys: List of keys to subscribe to (supports wildcards)
            callback: Optional callback function for notifications
        """
        if not self._session_id:
            raise ValueError("No active session. Call register_session first.")

        # Update local subscriptions
        self._subscriptions.update(keys)

        # Save to subscriptions file
        data = self._read_json(self.subscriptions_file)
        if self._session_id not in data['subscriptions']:
            data['subscriptions'][self._session_id] = []

        data['subscriptions'][self._session_id] = list(
            set(data['subscriptions'][self._session_id] + keys)
        )
        self._write_json(self.subscriptions_file, data)

    def get_context(self, key: Optional[str] = None,
                   context_type: Optional[ContextType] = None,
                   task_id: Optional[str] = None,
                   since: Optional[datetime] = None) -> List[ContextEntry]:
        """Retrieve shared context.

        Args:
            key: Filter by key (supports wildcards with *)
            context_type: Filter by type
            task_id: Filter by task
            since: Only get entries after this time

        Returns:
            List of matching context entries
        """
        data = self._read_json(self.context_file)
        entries = []

        for entry_dict in data['entries']:
            # Parse entry
            entry = ContextEntry(
                id=entry_dict['id'],
                session_id=entry_dict['session_id'],
                type=ContextType(entry_dict['type']),
                key=entry_dict['key'],
                value=entry_dict['value'],
                timestamp=entry_dict['timestamp'],
                task_id=entry_dict.get('task_id'),
                metadata=entry_dict.get('metadata', {})
            )

            # Apply filters
            if key and not self._matches_pattern(entry.key, key):
                continue

            if context_type and entry.type != context_type:
                continue

            if task_id and entry.task_id != task_id:
                continue

            if since:
                entry_time = datetime.fromisoformat(entry.timestamp)
                if entry_time <= since:
                    continue

            entries.append(entry)

        return entries

    def _matches_pattern(self, text: str, pattern: str) -> bool:
        """Check if text matches pattern (supports * wildcard)"""
        import fnmatch
        return fnmatch.fnmatch(text, pattern)

    def merge_contexts(self, entries: List[ContextEntry]) -> Dict[str, Any]:
        """Merge multiple context entries intelligently.

        Args:
            entries: List of context entries to merge

        Returns:
            Merged context dictionary
        """
        merged = {}
        conflicts = []

        # Group by key
        by_key = defaultdict(list)
        for entry in entries:
            by_key[entry.key].append(entry)

        # Merge each key
        for key, key_entries in by_key.items():
            if len(key_entries) == 1:
                # No conflict
                merged[key] = key_entries[0].value
            else:
                # Multiple values for same key - resolve conflict
                # Sort by timestamp (newest first)
                key_entries.sort(key=lambda e: e.timestamp, reverse=True)

                # Conflict resolution strategies
                values = [e.value for e in key_entries]

                if all(isinstance(v, (int, float)) for v in values):
                    # Numeric - take maximum
                    merged[key] = max(values)
                elif all(isinstance(v, list) for v in values):
                    # Lists - combine unique elements
                    combined = []
                    for v in values:
                        combined.extend(v)
                    merged[key] = list(set(combined))
                elif all(isinstance(v, dict) for v in values):
                    # Dicts - deep merge
                    result = {}
                    for v in values:
                        result.update(v)
                    merged[key] = result
                else:
                    # Default - take most recent
                    merged[key] = values[0]
                    conflicts.append({
                        'key': key,
                        'values': values,
                        'resolution': 'most_recent'
                    })

        if conflicts:
            merged['_conflicts'] = conflicts

        return merged

    def cleanup_stale_sessions(self, timeout_seconds: int = 60):
        """Clean up sessions that haven't sent heartbeat recently.

        Args:
            timeout_seconds: Seconds before considering session stale
        """
        data = self._read_json(self.sessions_file)
        now = datetime.now()
        stale_sessions = []

        for session_id, session in data['sessions'].items():
            if session['status'] == 'completed':
                continue

            last_heartbeat = datetime.fromisoformat(session['last_heartbeat'])
            if (now - last_heartbeat).total_seconds() > timeout_seconds:
                session['status'] = 'stale'
                stale_sessions.append(session_id)

        if stale_sessions:
            self._write_json(self.sessions_file, data)
            print(f"Marked {len(stale_sessions)} sessions as stale")

        # Clean up old stale sessions (>1 hour old)
        old_sessions = []
        for session_id, session in data['sessions'].items():
            if session['status'] == 'stale':
                last_heartbeat = datetime.fromisoformat(session['last_heartbeat'])
                if (now - last_heartbeat).total_seconds() > 3600:
                    old_sessions.append(session_id)

        for session_id in old_sessions:
            del data['sessions'][session_id]

        if old_sessions:
            self._write_json(self.sessions_file, data)
            print(f"Removed {len(old_sessions)} old sessions")

    def complete_session(self, session_id: Optional[str] = None):
        """Mark session as completed.

        Args:
            session_id: Session ID (uses stored ID if not provided)
        """
        if session_id is None:
            session_id = self._session_id

        if not session_id:
            return

        data = self._read_json(self.sessions_file)
        if session_id in data['sessions']:
            data['sessions'][session_id]['status'] = 'completed'
            self._write_json(self.sessions_file, data)

    def _notify_subscribers(self, key: str, entry: ContextEntry):
        """Notify subscribers of new context (placeholder for future enhancement)"""
        # This could be enhanced with actual callbacks or message queue
        pass

    def get_active_sessions(self) -> List[Session]:
        """Get all active sessions"""
        data = self._read_json(self.sessions_file)
        sessions = []

        for session_dict in data['sessions'].values():
            if session_dict['status'] == 'active':
                sessions.append(Session(
                    id=session_dict['id'],
                    task_ids=session_dict['task_ids'],
                    started_at=session_dict['started_at'],
                    last_heartbeat=session_dict['last_heartbeat'],
                    status=session_dict['status'],
                    agent_type=session_dict.get('agent_type')
                ))

        return sessions

    def get_session_context(self, session_id: str) -> List[ContextEntry]:
        """Get all context published by a specific session"""
        return [e for e in self.get_context() if e.session_id == session_id]


def main():
    """CLI interface for context coordination"""
    import argparse

    parser = argparse.ArgumentParser(description="Context Coordinator")
    parser.add_argument('command', choices=['test', 'list', 'cleanup', 'monitor'])
    args = parser.parse_args()

    coordinator = ContextCoordinator()

    if args.command == 'test':
        print("Testing context coordination...")

        # Register session
        session_id = coordinator.register_session(['110_1', '110_2'], 'test_agent')
        print(f"Registered session: {session_id}")

        # Publish some context
        coordinator.publish_context(
            ContextType.DISCOVERY,
            'database_schema',
            {'tables': ['users', 'tasks', 'projects']},
            task_id='110_1'
        )
        print("Published database schema discovery")

        coordinator.publish_context(
            ContextType.DECISION,
            'architecture_choice',
            'microservices',
            task_id='110_2',
            metadata={'reason': 'scalability'}
        )
        print("Published architecture decision")

        # Retrieve context
        entries = coordinator.get_context()
        print(f"\nRetrieved {len(entries)} context entries:")
        for entry in entries:
            print(f"  - {entry.key}: {entry.value} ({entry.type.value})")

        # Complete session
        coordinator.complete_session()
        print("\nSession completed")

    elif args.command == 'list':
        # List active sessions
        sessions = coordinator.get_active_sessions()
        print(f"Active sessions ({len(sessions)}):")
        for session in sessions:
            age = datetime.now() - datetime.fromisoformat(session.started_at)
            print(f"  - {session.id}: {session.agent_type or 'unknown'}")
            print(f"    Tasks: {', '.join(session.task_ids)}")
            print(f"    Age: {age}")

    elif args.command == 'cleanup':
        coordinator.cleanup_stale_sessions()
        print("Cleanup completed")

    elif args.command == 'monitor':
        print("Monitoring shared context (press Ctrl+C to stop)...")
        last_check = datetime.now()

        try:
            while True:
                time.sleep(5)
                new_entries = coordinator.get_context(since=last_check)
                if new_entries:
                    print(f"\n{len(new_entries)} new context entries:")
                    for entry in new_entries:
                        print(f"  [{entry.session_id[:8]}] {entry.key}: {entry.value}")
                last_check = datetime.now()
        except KeyboardInterrupt:
            print("\nMonitoring stopped")


if __name__ == '__main__':
    main()