#!/usr/bin/env python3
"""
Checkpoint Manager - Fast checkpoint creation and restore

Features:
- Create timestamped checkpoints
- Diff between checkpoints
- Restore to previous state
- SHA-256 integrity verification
"""

import json
import os
import hashlib
import gzip
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class CheckpointManager:
    """Manage task system checkpoints"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.checkpoint_dir = self.base_path / ".claude" / "checkpoints"
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def create_checkpoint(self, description: str = "") -> str:
        """Create a new checkpoint"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_id = f"checkpoint_{timestamp}"
        checkpoint_path = self.checkpoint_dir / checkpoint_id

        checkpoint_path.mkdir(exist_ok=True)

        # Copy task files
        tasks_dir = self.base_path / ".claude" / "tasks"
        if tasks_dir.exists():
            tasks_backup = checkpoint_path / "tasks"
            shutil.copytree(tasks_dir, tasks_backup)

        # Create metadata
        metadata = {
            "id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "files_count": len(list(tasks_dir.glob("*.json"))),
            "hash": self._calculate_hash(tasks_dir)
        }

        with open(checkpoint_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        # Compress checkpoint
        self._compress_checkpoint(checkpoint_path)

        return checkpoint_id

    def list_checkpoints(self) -> List[Dict]:
        """List all checkpoints"""
        checkpoints = []

        for checkpoint_dir in self.checkpoint_dir.glob("checkpoint_*"):
            metadata_file = checkpoint_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    checkpoints.append(json.load(f))

        return sorted(checkpoints, key=lambda x: x['timestamp'], reverse=True)

    def diff_checkpoint(self, checkpoint_id: str) -> Dict[str, List]:
        """Show diff between checkpoint and current state"""
        checkpoint_path = self.checkpoint_dir / checkpoint_id
        if not checkpoint_path.exists():
            raise ValueError(f"Checkpoint {checkpoint_id} not found")

        diffs = {
            "added": [],
            "modified": [],
            "deleted": []
        }

        # Current task files
        current_tasks = self.base_path / ".claude" / "tasks"
        current_files = {f.name: f for f in current_tasks.glob("*.json")}

        # Checkpoint task files
        checkpoint_tasks = checkpoint_path / "tasks"
        checkpoint_files = {f.name: f for f in checkpoint_tasks.glob("*.json")}

        # Find changes
        for filename in current_files:
            if filename not in checkpoint_files:
                diffs["added"].append(filename)
            else:
                if self._file_hash(current_files[filename]) != \
                   self._file_hash(checkpoint_files[filename]):
                    diffs["modified"].append(filename)

        for filename in checkpoint_files:
            if filename not in current_files:
                diffs["deleted"].append(filename)

        return diffs

    def rollback_to(self, checkpoint_id: str, confirm: bool = False) -> bool:
        """Rollback to a checkpoint"""
        if not confirm:
            print(f"Warning: This will overwrite current state. Use confirm=True to proceed.")
            return False

        checkpoint_path = self.checkpoint_dir / checkpoint_id
        if not checkpoint_path.exists():
            raise ValueError(f"Checkpoint {checkpoint_id} not found")

        # Decompress if needed
        self._decompress_checkpoint(checkpoint_path)

        # Backup current state first
        self.create_checkpoint(f"Pre-rollback to {checkpoint_id}")

        # Restore checkpoint
        current_tasks = self.base_path / ".claude" / "tasks"
        checkpoint_tasks = checkpoint_path / "tasks"

        if current_tasks.exists():
            shutil.rmtree(current_tasks)
        shutil.copytree(checkpoint_tasks, current_tasks)

        return True

    def _calculate_hash(self, directory: Path) -> str:
        """Calculate SHA-256 hash of directory contents"""
        hasher = hashlib.sha256()

        for file_path in sorted(directory.glob("*.json")):
            with open(file_path, 'rb') as f:
                hasher.update(f.read())

        return hasher.hexdigest()

    def _file_hash(self, file_path: Path) -> str:
        """Calculate hash of single file"""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _compress_checkpoint(self, checkpoint_path: Path):
        """Compress checkpoint directory"""
        archive_path = checkpoint_path.with_suffix('.tar.gz')
        shutil.make_archive(str(checkpoint_path), 'gztar', checkpoint_path.parent, checkpoint_path.name)

    def _decompress_checkpoint(self, checkpoint_path: Path):
        """Decompress checkpoint if needed"""
        archive_path = checkpoint_path.with_suffix('.tar.gz')
        if archive_path.exists() and not checkpoint_path.exists():
            shutil.unpack_archive(archive_path, checkpoint_path.parent)


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Checkpoint Manager")
    parser.add_argument("command", choices=["create", "list", "diff", "rollback"],
                       help="Command to execute")
    parser.add_argument("--description", help="Checkpoint description")
    parser.add_argument("--checkpoint-id", help="Checkpoint ID")
    parser.add_argument("--confirm", action="store_true", help="Confirm rollback")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    manager = CheckpointManager()

    if args.command == "create":
        checkpoint_id = manager.create_checkpoint(args.description or "")
        print(f"Created checkpoint: {checkpoint_id}")

    elif args.command == "list":
        checkpoints = manager.list_checkpoints()
        if args.json:
            print(json.dumps(checkpoints, indent=2))
        else:
            for cp in checkpoints:
                print(f"{cp['id']}: {cp['description']} ({cp['files_count']} files)")

    elif args.command == "diff":
        if not args.checkpoint_id:
            print("Checkpoint ID required")
            return

        diffs = manager.diff_checkpoint(args.checkpoint_id)
        if args.json:
            print(json.dumps(diffs, indent=2))
        else:
            print(f"Changes since {args.checkpoint_id}:")
            print(f"  Added: {len(diffs['added'])}")
            print(f"  Modified: {len(diffs['modified'])}")
            print(f"  Deleted: {len(diffs['deleted'])}")

    elif args.command == "rollback":
        if not args.checkpoint_id:
            print("Checkpoint ID required")
            return

        if manager.rollback_to(args.checkpoint_id, args.confirm):
            print(f"Rolled back to {args.checkpoint_id}")


if __name__ == "__main__":
    main()