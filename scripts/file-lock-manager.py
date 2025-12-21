#!/usr/bin/env python3
"""File Lock Manager - Provides atomic file locking with cross-platform support.

This module implements:
- Atomic file locking using flock (Unix) or msvcrt (Windows)
- Timeout support with exponential backoff
- Lock tracking in .claude/locks/ directory
- Both exclusive and shared lock support
- Automatic lock release on process termination
"""

import os
import sys
import time
import json
import hashlib
import platform
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import atexit

# Platform-specific imports
if platform.system() == 'Windows':
    import msvcrt
else:
    import fcntl


class FileLockManager:
    """Manages file locks with automatic cleanup and tracking."""

    def __init__(self, locks_dir: Path = None):
        """Initialize the lock manager.

        Args:
            locks_dir: Directory to store lock tracking files (default: .claude/locks/)
        """
        if locks_dir is None:
            # Find project root (directory containing .claude)
            current = Path.cwd()
            while current != current.parent:
                if (current / '.claude').exists():
                    locks_dir = current / '.claude' / 'locks'
                    break
                current = current.parent
            else:
                locks_dir = Path.cwd() / '.claude' / 'locks'

        self.locks_dir = Path(locks_dir)
        self.locks_dir.mkdir(parents=True, exist_ok=True)
        self.active_locks = {}
        self.platform = platform.system()

        # Register cleanup on exit
        atexit.register(self.cleanup_all_locks)

    def _get_lock_id(self, filepath: Path) -> str:
        """Generate a unique lock ID for a file path."""
        return hashlib.md5(str(filepath.absolute()).encode()).hexdigest()[:16]

    def _get_lock_info_path(self, filepath: Path) -> Path:
        """Get path to lock info file."""
        lock_id = self._get_lock_id(filepath)
        return self.locks_dir / f"{lock_id}.lock"

    def _save_lock_info(self, filepath: Path, lock_type: str, pid: int):
        """Save lock information to tracking file."""
        lock_info = {
            'filepath': str(filepath.absolute()),
            'lock_type': lock_type,
            'pid': pid,
            'timestamp': datetime.now().isoformat(),
            'hostname': platform.node()
        }

        lock_info_path = self._get_lock_info_path(filepath)
        try:
            with open(lock_info_path, 'w') as f:
                json.dump(lock_info, f, indent=2)
        except Exception:
            # Non-fatal - continue without tracking
            pass

    def _remove_lock_info(self, filepath: Path):
        """Remove lock information file."""
        lock_info_path = self._get_lock_info_path(filepath)
        try:
            if lock_info_path.exists():
                lock_info_path.unlink()
        except Exception:
            # Non-fatal - continue
            pass

    def _is_process_alive(self, pid: int) -> bool:
        """Check if a process with given PID is still running."""
        try:
            if self.platform == 'Windows':
                import subprocess
                result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                                      capture_output=True, text=True)
                return str(pid) in result.stdout
            else:
                os.kill(pid, 0)
                return True
        except (OSError, ProcessLookupError):
            return False

    def _clean_stale_locks(self):
        """Remove lock info files for dead processes."""
        for lock_file in self.locks_dir.glob('*.lock'):
            try:
                with open(lock_file, 'r') as f:
                    info = json.load(f)

                # Check if process is still alive
                if not self._is_process_alive(info['pid']):
                    lock_file.unlink()
            except Exception:
                # If we can't read or process, remove it
                try:
                    lock_file.unlink()
                except:
                    pass

    @contextmanager
    def acquire_lock(self, filepath: Path, exclusive: bool = True,
                    timeout: float = 30.0, retry_delay: float = 0.1):
        """Acquire a file lock with timeout and exponential backoff.

        Args:
            filepath: Path to file to lock
            exclusive: True for exclusive lock, False for shared lock
            timeout: Maximum time to wait for lock (seconds)
            retry_delay: Initial retry delay (seconds)

        Yields:
            File handle with acquired lock

        Raises:
            TimeoutError: If lock cannot be acquired within timeout
            IOError: If file operations fail
        """
        filepath = Path(filepath).absolute()
        file_handle = None
        lock_acquired = False
        start_time = time.time()
        current_delay = retry_delay

        # Clean stale locks periodically
        self._clean_stale_locks()

        try:
            # Open file for locking
            mode = 'r+b' if filepath.exists() else 'w+b'
            file_handle = open(filepath, mode)

            while (time.time() - start_time) < timeout:
                try:
                    if self.platform == 'Windows':
                        # Windows locking using msvcrt
                        if exclusive:
                            msvcrt.locking(file_handle.fileno(),
                                          msvcrt.LK_NBLCK, 1)
                        else:
                            # Windows doesn't have shared locks, use exclusive
                            msvcrt.locking(file_handle.fileno(),
                                          msvcrt.LK_NBLCK, 1)
                    else:
                        # Unix locking using fcntl
                        lock_flag = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
                        fcntl.flock(file_handle.fileno(), lock_flag | fcntl.LOCK_NB)

                    lock_acquired = True
                    break

                except (IOError, OSError):
                    # Lock not available, wait with exponential backoff
                    time.sleep(current_delay)
                    current_delay = min(current_delay * 2, 2.0)  # Cap at 2 seconds

            if not lock_acquired:
                raise TimeoutError(f"Could not acquire lock on {filepath} within {timeout} seconds")

            # Save lock information
            lock_type = 'exclusive' if exclusive else 'shared'
            self._save_lock_info(filepath, lock_type, os.getpid())
            self.active_locks[str(filepath)] = file_handle

            yield file_handle

        finally:
            # Release lock
            if file_handle and lock_acquired:
                try:
                    if self.platform == 'Windows':
                        msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
                except:
                    pass

            # Close file
            if file_handle:
                try:
                    file_handle.close()
                except:
                    pass

            # Remove lock info
            if lock_acquired:
                self._remove_lock_info(filepath)
                self.active_locks.pop(str(filepath), None)

    def is_locked(self, filepath: Path) -> Dict[str, Any]:
        """Check if a file is currently locked.

        Args:
            filepath: Path to check

        Returns:
            Lock info dict if locked, None if not locked
        """
        lock_info_path = self._get_lock_info_path(filepath)

        if not lock_info_path.exists():
            return None

        try:
            with open(lock_info_path, 'r') as f:
                info = json.load(f)

            # Verify process is still alive
            if self._is_process_alive(info['pid']):
                return info
            else:
                # Stale lock - clean it up
                self._remove_lock_info(filepath)
                return None
        except Exception:
            return None

    def get_all_locks(self) -> List[Dict[str, Any]]:
        """Get information about all active locks.

        Returns:
            List of lock info dictionaries
        """
        locks = []
        self._clean_stale_locks()

        for lock_file in self.locks_dir.glob('*.lock'):
            try:
                with open(lock_file, 'r') as f:
                    info = json.load(f)
                if self._is_process_alive(info['pid']):
                    locks.append(info)
            except Exception:
                continue

        return locks

    def cleanup_all_locks(self):
        """Clean up all locks held by this process."""
        for filepath_str, file_handle in list(self.active_locks.items()):
            try:
                filepath = Path(filepath_str)

                # Release lock
                if self.platform == 'Windows':
                    msvcrt.locking(file_handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)

                # Close file
                file_handle.close()

                # Remove lock info
                self._remove_lock_info(filepath)
            except:
                pass

        self.active_locks.clear()

    def wait_for_lock(self, filepath: Path, timeout: float = 60.0) -> bool:
        """Wait for a lock to be released.

        Args:
            filepath: Path to wait for
            timeout: Maximum time to wait

        Returns:
            True if lock was released, False if timeout
        """
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            if not self.is_locked(filepath):
                return True
            time.sleep(0.5)

        return False


# Convenience functions
_default_manager = None

def get_default_manager() -> FileLockManager:
    """Get the default lock manager instance."""
    global _default_manager
    if _default_manager is None:
        _default_manager = FileLockManager()
    return _default_manager


@contextmanager
def exclusive_lock(filepath: Path, timeout: float = 30.0):
    """Convenience function for exclusive locks."""
    manager = get_default_manager()
    with manager.acquire_lock(filepath, exclusive=True, timeout=timeout) as f:
        yield f


@contextmanager
def shared_lock(filepath: Path, timeout: float = 30.0):
    """Convenience function for shared locks."""
    manager = get_default_manager()
    with manager.acquire_lock(filepath, exclusive=False, timeout=timeout) as f:
        yield f


def is_locked(filepath: Path) -> bool:
    """Check if a file is locked."""
    manager = get_default_manager()
    return manager.is_locked(filepath) is not None


def list_all_locks():
    """List all active locks."""
    manager = get_default_manager()
    locks = manager.get_all_locks()

    if not locks:
        print("No active locks")
        return

    print(f"Active locks ({len(locks)}):")
    for lock in locks:
        age = datetime.now() - datetime.fromisoformat(lock['timestamp'])
        print(f"  - {lock['filepath']}")
        print(f"    Type: {lock['lock_type']}, PID: {lock['pid']}")
        print(f"    Host: {lock['hostname']}, Age: {age}")


if __name__ == '__main__':
    # CLI interface
    if len(sys.argv) < 2:
        print("Usage: file-lock-manager.py [list|test|check <file>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'list':
        list_all_locks()

    elif command == 'check' and len(sys.argv) > 2:
        filepath = Path(sys.argv[2])
        lock_info = get_default_manager().is_locked(filepath)
        if lock_info:
            print(f"File is locked: {json.dumps(lock_info, indent=2)}")
        else:
            print("File is not locked")

    elif command == 'test':
        # Test locking functionality
        test_file = Path('.claude/locks/test.lock')
        test_file.parent.mkdir(parents=True, exist_ok=True)

        print("Testing exclusive lock...")
        with exclusive_lock(test_file, timeout=5):
            print(f"  Acquired exclusive lock on {test_file}")
            print(f"  Lock is active: {is_locked(test_file)}")
            time.sleep(1)
        print(f"  Lock released: {not is_locked(test_file)}")

        print("\nTesting shared lock...")
        with shared_lock(test_file, timeout=5):
            print(f"  Acquired shared lock on {test_file}")
            time.sleep(1)
        print(f"  Lock released: {not is_locked(test_file)}")

        print("\nTest completed successfully!")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)