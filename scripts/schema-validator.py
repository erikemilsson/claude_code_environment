#!/usr/bin/env python3
"""
Schema Validator - Validate and auto-repair task JSON files

Features:
- Validate all tasks against schema
- Auto-repair common issues (missing fields, date formats)
- Fix broken references
- Generate health reports
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import shutil
from jsonschema import validate, ValidationError, Draft7Validator

# Import task manager
try:
    from task_manager import TaskManager, Task, TaskStatus
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from task_manager import TaskManager, Task, TaskStatus


class SchemaValidator:
    """Task schema validation and auto-repair"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.task_manager = TaskManager(base_path)
        self.backup_dir = self.base_path / ".claude" / "backups"
        self.schema = self._load_schema()

    def _load_schema(self) -> Dict:
        """Load task schema definition"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["id", "title", "description", "difficulty", "status",
                        "created_date", "updated_date"],
            "properties": {
                "id": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "difficulty": {"type": "integer", "minimum": 1, "maximum": 10},
                "status": {"type": "string", "enum": ["Pending", "In Progress", "Blocked",
                                                       "Broken Down", "Finished"]},
                "created_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
                "updated_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
                "completion_date": {"type": ["string", "null"], "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
                "completion_notes": {"type": ["string", "null"]},
                "dependencies": {"type": "array", "items": {"type": "string"}},
                "subtasks": {"type": "array", "items": {"type": "string"}},
                "parent_task": {"type": ["string", "null"]},
                "files_affected": {"type": "array", "items": {"type": "string"}},
                "notes": {"type": ["string", "null"]},
                "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "validation_status": {"type": "string"},
                "momentum": {"type": "object"},
                "decision_rationale": {"type": ["string", "null"]}
            }
        }

    def validate_all_tasks(self) -> Tuple[List[str], List[str]]:
        """Validate all task files against schema"""
        valid_tasks = []
        invalid_tasks = []

        for task_file in self.task_manager.tasks_dir.glob("task-*.json"):
            task_id = task_file.stem.replace("task-", "")
            try:
                with open(task_file, 'r') as f:
                    data = json.load(f)
                validate(data, self.schema)
                valid_tasks.append(task_id)
            except (ValidationError, json.JSONDecodeError) as e:
                invalid_tasks.append((task_id, str(e)))

        return valid_tasks, invalid_tasks

    def fix_missing_fields(self, task_id: str) -> bool:
        """Add missing required fields with defaults"""
        task_file = self.task_manager.tasks_dir / f"task-{task_id}.json"

        try:
            with open(task_file, 'r') as f:
                data = json.load(f)

            modified = False

            # Add missing fields with defaults
            defaults = {
                "completion_date": None,
                "completion_notes": None,
                "dependencies": [],
                "subtasks": [],
                "parent_task": None,
                "files_affected": [],
                "notes": None,
                "confidence": 50,
                "assumptions": [],
                "validation_status": "pending",
                "momentum": {
                    "phase": "initializing",
                    "velocity": 0,
                    "last_activity": datetime.now().strftime("%Y-%m-%d")
                },
                "decision_rationale": None
            }

            for field, default_value in defaults.items():
                if field not in data:
                    data[field] = default_value
                    modified = True

            if modified:
                self._backup_file(task_file)
                with open(task_file, 'w') as f:
                    json.dump(data, f, indent=2)

            return modified

        except Exception as e:
            print(f"Error fixing missing fields for {task_id}: {e}")
            return False

    def fix_date_formats(self, task_id: str) -> bool:
        """Fix date format issues"""
        task_file = self.task_manager.tasks_dir / f"task-{task_id}.json"

        try:
            with open(task_file, 'r') as f:
                data = json.load(f)

            modified = False
            date_fields = ["created_date", "updated_date", "completion_date"]

            for field in date_fields:
                if field in data and data[field]:
                    try:
                        # Try to parse and reformat
                        date_obj = datetime.strptime(data[field][:10], "%Y-%m-%d")
                        new_date = date_obj.strftime("%Y-%m-%d")
                        if data[field] != new_date:
                            data[field] = new_date
                            modified = True
                    except:
                        # If can't parse, use today's date for updated_date
                        if field == "updated_date":
                            data[field] = datetime.now().strftime("%Y-%m-%d")
                            modified = True

            if modified:
                self._backup_file(task_file)
                with open(task_file, 'w') as f:
                    json.dump(data, f, indent=2)

            return modified

        except Exception as e:
            print(f"Error fixing date formats for {task_id}: {e}")
            return False

    def fix_broken_references(self) -> Dict[str, List[str]]:
        """Fix broken task references (dependencies, parent, subtasks)"""
        fixes = {"dependencies": [], "parent_refs": [], "subtask_refs": []}
        all_task_ids = set(self.task_manager.get_all_task_ids())

        for task_id in all_task_ids:
            task = self.task_manager.load_task(task_id)
            if not task:
                continue

            modified = False

            # Check dependencies
            if task.dependencies:
                valid_deps = [d for d in task.dependencies if d in all_task_ids]
                if len(valid_deps) != len(task.dependencies):
                    task.dependencies = valid_deps
                    modified = True
                    fixes["dependencies"].append(task_id)

            # Check parent reference
            if task.parent_task and task.parent_task not in all_task_ids:
                task.parent_task = None
                modified = True
                fixes["parent_refs"].append(task_id)

            # Check subtask references
            if task.subtasks:
                valid_subtasks = [s for s in task.subtasks if s in all_task_ids]
                if len(valid_subtasks) != len(task.subtasks):
                    task.subtasks = valid_subtasks
                    modified = True
                    fixes["subtask_refs"].append(task_id)

            if modified:
                self.task_manager.save_task(task)

        return fixes

    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": 0,
            "valid_tasks": 0,
            "invalid_tasks": [],
            "missing_fields": [],
            "date_issues": [],
            "broken_references": {},
            "parent_subtask_mismatches": [],
            "circular_dependencies": [],
            "orphaned_subtasks": []
        }

        all_task_ids = self.task_manager.get_all_task_ids()
        report["total_tasks"] = len(all_task_ids)

        # Validate schemas
        valid, invalid = self.validate_all_tasks()
        report["valid_tasks"] = len(valid)
        report["invalid_tasks"] = invalid

        # Check for issues
        for task_id in all_task_ids:
            task = self.task_manager.load_task(task_id)
            if not task:
                continue

            # Check missing critical fields
            if not task.title or not task.description:
                report["missing_fields"].append(task_id)

            # Check parent-subtask consistency
            if task.parent_task:
                parent = self.task_manager.load_task(task.parent_task)
                if parent and task.id not in (parent.subtasks or []):
                    report["parent_subtask_mismatches"].append(task_id)

            # Check for orphaned subtasks
            if task.parent_task:
                if task.parent_task not in all_task_ids:
                    report["orphaned_subtasks"].append(task_id)

        # Check for circular dependencies
        report["circular_dependencies"] = self._detect_circular_dependencies()

        return report

    def _detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependency chains"""
        cycles = []

        def has_cycle(task_id: str, visited: set, rec_stack: set, path: list) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            path.append(task_id)

            task = self.task_manager.load_task(task_id)
            if task and task.dependencies:
                for dep in task.dependencies:
                    if dep not in visited:
                        if has_cycle(dep, visited, rec_stack, path.copy()):
                            return True
                    elif dep in rec_stack:
                        # Found cycle
                        cycle_start = path.index(dep)
                        cycle = path[cycle_start:] + [dep]
                        if cycle not in cycles:
                            cycles.append(cycle)

            rec_stack.remove(task_id)
            return False

        all_tasks = self.task_manager.get_all_task_ids()
        visited = set()

        for task_id in all_tasks:
            if task_id not in visited:
                has_cycle(task_id, visited, set(), [])

        return cycles

    def _backup_file(self, file_path: Path):
        """Create backup before modifying file"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}.json"
        shutil.copy2(file_path, self.backup_dir / backup_name)

    def auto_repair_all(self) -> Dict[str, Any]:
        """Run all auto-repair operations"""
        results = {
            "missing_fields_fixed": 0,
            "date_formats_fixed": 0,
            "broken_references": {},
            "errors": []
        }

        all_task_ids = self.task_manager.get_all_task_ids()

        for task_id in all_task_ids:
            try:
                # Fix missing fields
                if self.fix_missing_fields(task_id):
                    results["missing_fields_fixed"] += 1

                # Fix date formats
                if self.fix_date_formats(task_id):
                    results["date_formats_fixed"] += 1

            except Exception as e:
                results["errors"].append(f"{task_id}: {str(e)}")

        # Fix broken references (once for all tasks)
        results["broken_references"] = self.fix_broken_references()

        return results


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Schema Validator - Validate and repair task files")
    parser.add_argument("command", choices=["validate", "repair", "health", "fix-missing",
                                           "fix-dates", "fix-refs"],
                       help="Command to execute")
    parser.add_argument("--task-id", help="Task ID for specific operations")
    parser.add_argument("--base-path", default=".", help="Base project path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    validator = SchemaValidator(args.base_path)

    if args.command == "validate":
        valid, invalid = validator.validate_all_tasks()

        if args.json:
            print(json.dumps({"valid": valid, "invalid": invalid}, indent=2))
        else:
            print(f"Valid tasks: {len(valid)}")
            if invalid:
                print(f"Invalid tasks: {len(invalid)}")
                for task_id, error in invalid:
                    print(f"  {task_id}: {error[:100]}")

    elif args.command == "repair":
        results = validator.auto_repair_all()

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("Auto-repair Results:")
            print(f"  Missing fields fixed: {results['missing_fields_fixed']}")
            print(f"  Date formats fixed: {results['date_formats_fixed']}")
            if results['broken_references']:
                print("  Broken references fixed:")
                for ref_type, task_ids in results['broken_references'].items():
                    if task_ids:
                        print(f"    {ref_type}: {', '.join(task_ids)}")

    elif args.command == "health":
        report = validator.generate_health_report()

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print("Task System Health Report")
            print("=" * 50)
            print(f"Total tasks: {report['total_tasks']}")
            print(f"Valid tasks: {report['valid_tasks']}")
            print(f"Invalid tasks: {len(report['invalid_tasks'])}")

            if report['circular_dependencies']:
                print(f"⚠️ Circular dependencies detected: {report['circular_dependencies']}")
            if report['orphaned_subtasks']:
                print(f"⚠️ Orphaned subtasks: {report['orphaned_subtasks']}")

    elif args.command == "fix-missing" and args.task_id:
        if validator.fix_missing_fields(args.task_id):
            print(f"Fixed missing fields for task {args.task_id}")
        else:
            print(f"No missing fields to fix for task {args.task_id}")

    elif args.command == "fix-dates" and args.task_id:
        if validator.fix_date_formats(args.task_id):
            print(f"Fixed date formats for task {args.task_id}")
        else:
            print(f"No date format issues for task {args.task_id}")

    elif args.command == "fix-refs":
        fixes = validator.fix_broken_references()
        print("Fixed broken references:")
        for ref_type, task_ids in fixes.items():
            if task_ids:
                print(f"  {ref_type}: {', '.join(task_ids)}")


if __name__ == "__main__":
    main()