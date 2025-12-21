#!/usr/bin/env python3
"""
Validation Gates - Pre and post-execution validation checks

This module provides validation gates that can block or warn about issues:
- Pre-execution: Check task readiness before starting work
- Post-execution: Validate completion and suggest follow-ups
- Breakdown validation: Ensure high-difficulty tasks are properly broken down
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import sys

# Import task manager for core functionality
try:
    from task_manager import TaskManager, Task, TaskStatus
except ImportError:
    # Fallback for module import
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from task_manager import TaskManager, Task, TaskStatus

# Import conflict detector and file lock manager if available
try:
    from conflict_detector import ConflictDetector, ConflictType
    CONFLICT_DETECTOR_AVAILABLE = True
except ImportError:
    CONFLICT_DETECTOR_AVAILABLE = False

try:
    from file_lock_manager import is_locked, FileLockManager
    LOCKS_AVAILABLE = True
except ImportError:
    LOCKS_AVAILABLE = False


class GateLevel(Enum):
    """Validation gate severity levels"""
    BLOCKING = "blocking"  # Must fix before proceeding
    WARNING = "warning"    # Should review but can proceed
    INFO = "info"         # Informational only


class ValidationResult:
    """Result of a validation check"""

    def __init__(self, check_name: str, level: GateLevel, passed: bool,
                 message: str, details: Optional[Dict] = None):
        self.check_name = check_name
        self.level = level
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "check_name": self.check_name,
            "level": self.level.value,
            "passed": self.passed,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }


class ValidationGates:
    """Main validation gate implementation"""

    def __init__(self, base_path: str = "."):
        """Initialize validation gates with base path"""
        self.base_path = Path(base_path)
        self.task_manager = TaskManager(base_path)
        self.gates_log = self.base_path / ".claude" / "validation-gates.log"

    def run_pre_execution_gates(self, task_id: str) -> Tuple[bool, List[ValidationResult]]:
        """
        Run all pre-execution validation checks

        Returns:
            Tuple of (can_proceed, list_of_results)
        """
        results = []

        # Load task
        task = self.task_manager.load_task(task_id)
        if not task:
            results.append(ValidationResult(
                "task_exists",
                GateLevel.BLOCKING,
                False,
                f"Task {task_id} not found"
            ))
            return False, results

        # Check 1: Valid status for execution
        results.append(self._check_status_valid(task))

        # Check 2: Dependencies complete
        results.append(self._check_dependencies_complete(task))

        # Check 3: Difficulty breakdown requirement
        results.append(self._check_difficulty_breakdown(task))

        # Check 4: Parent task not broken down
        results.append(self._check_parent_status(task))

        # Check 5: Files exist
        results.append(self._check_files_exist(task))

        # Check 6: Confidence threshold
        results.append(self._check_confidence_threshold(task))

        # Check 7: Assumptions documented
        results.append(self._check_assumptions_documented(task))

        # Check 8: File conflicts (if detector available)
        if CONFLICT_DETECTOR_AVAILABLE:
            results.append(self._check_file_conflicts(task))

        # Check 9: Lock availability (if locks available)
        if LOCKS_AVAILABLE:
            results.append(self._check_lock_availability(task))

        # Determine if can proceed
        can_proceed = all(
            r.passed for r in results
            if r.level == GateLevel.BLOCKING
        )

        # Log results
        self._log_results(f"PRE_EXECUTION_{task_id}", results)

        return can_proceed, results

    def run_post_execution_gates(self, task_id: str) -> Tuple[bool, List[ValidationResult]]:
        """
        Run all post-execution validation checks

        Returns:
            Tuple of (all_passed, list_of_results)
        """
        results = []

        # Load task
        task = self.task_manager.load_task(task_id)
        if not task:
            results.append(ValidationResult(
                "task_exists",
                GateLevel.BLOCKING,
                False,
                f"Task {task_id} not found"
            ))
            return False, results

        # Check 1: Task marked as finished
        results.append(self._check_task_finished(task))

        # Check 2: Completion notes provided
        results.append(self._check_completion_notes(task))

        # Check 3: Files were modified (if expected)
        results.append(self._check_files_modified(task))

        # Check 4: Parent auto-completion
        parent_completed = self._check_and_complete_parent(task)
        if parent_completed:
            results.append(ValidationResult(
                "parent_auto_complete",
                GateLevel.INFO,
                True,
                f"Parent task {task.parent_task} auto-completed"
            ))

        # Check 5: Suggest patterns based on task
        results.append(self._suggest_patterns(task))

        # Check 6: Validate assumptions
        results.append(self._check_assumptions_validated(task))

        # Check 7: Momentum updated
        results.append(self._check_momentum_updated(task))

        # All checks passed?
        all_passed = all(r.passed for r in results)

        # Log results
        self._log_results(f"POST_EXECUTION_{task_id}", results)

        return all_passed, results

    def _check_status_valid(self, task: Task) -> ValidationResult:
        """Check if task status is valid for execution"""
        valid_statuses = [TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value]

        if task.status in valid_statuses:
            return ValidationResult(
                "status_valid",
                GateLevel.BLOCKING,
                True,
                f"Task status '{task.status}' is valid for execution"
            )
        elif task.status == TaskStatus.FINISHED.value:
            return ValidationResult(
                "status_valid",
                GateLevel.WARNING,
                False,
                "Task is already finished"
            )
        elif task.status == TaskStatus.BROKEN_DOWN.value:
            return ValidationResult(
                "status_valid",
                GateLevel.BLOCKING,
                False,
                "Cannot work on broken down task - work on subtasks instead",
                {"subtasks": task.subtasks}
            )
        else:
            return ValidationResult(
                "status_valid",
                GateLevel.BLOCKING,
                False,
                f"Task status '{task.status}' is not valid for execution"
            )

    def _check_dependencies_complete(self, task: Task) -> ValidationResult:
        """Check if all dependencies are complete"""
        if not task.dependencies:
            return ValidationResult(
                "dependencies_complete",
                GateLevel.INFO,
                True,
                "No dependencies to check"
            )

        all_complete, incomplete = self.task_manager.validate_dependencies(task.id)

        if all_complete:
            return ValidationResult(
                "dependencies_complete",
                GateLevel.BLOCKING,
                True,
                f"All {len(task.dependencies)} dependencies are complete"
            )
        else:
            return ValidationResult(
                "dependencies_complete",
                GateLevel.BLOCKING,
                False,
                f"{len(incomplete)} dependencies are not complete",
                {"incomplete": incomplete}
            )

    def _check_difficulty_breakdown(self, task: Task) -> ValidationResult:
        """Check if high-difficulty task should be broken down"""
        if task.difficulty >= 7 and not task.subtasks:
            return ValidationResult(
                "difficulty_breakdown",
                GateLevel.BLOCKING,
                False,
                f"Task has difficulty {task.difficulty} (>=7) and must be broken down first",
                {"difficulty": task.difficulty, "threshold": 7}
            )
        elif task.difficulty >= 7 and task.subtasks:
            return ValidationResult(
                "difficulty_breakdown",
                GateLevel.INFO,
                True,
                f"High-difficulty task ({task.difficulty}) has been properly broken down",
                {"subtask_count": len(task.subtasks)}
            )
        else:
            return ValidationResult(
                "difficulty_breakdown",
                GateLevel.INFO,
                True,
                f"Task difficulty ({task.difficulty}) is below breakdown threshold"
            )

    def _check_parent_status(self, task: Task) -> ValidationResult:
        """Check parent task is not in workable state"""
        if not task.parent_task:
            return ValidationResult(
                "parent_status",
                GateLevel.INFO,
                True,
                "No parent task"
            )

        parent = self.task_manager.load_task(task.parent_task)
        if not parent:
            return ValidationResult(
                "parent_status",
                GateLevel.WARNING,
                False,
                f"Parent task {task.parent_task} not found"
            )

        if parent.status == TaskStatus.BROKEN_DOWN.value:
            return ValidationResult(
                "parent_status",
                GateLevel.INFO,
                True,
                f"Parent task properly marked as broken down"
            )
        else:
            return ValidationResult(
                "parent_status",
                GateLevel.WARNING,
                False,
                f"Parent task has status '{parent.status}' instead of 'Broken Down'"
            )

    def _check_files_exist(self, task: Task) -> ValidationResult:
        """Check if files referenced in task exist"""
        if not task.files_affected:
            return ValidationResult(
                "files_exist",
                GateLevel.INFO,
                True,
                "No files to check"
            )

        missing_files = []
        for file_path in task.files_affected:
            full_path = self.base_path / file_path
            if not full_path.exists() and not "*" in file_path:
                missing_files.append(file_path)

        if missing_files:
            return ValidationResult(
                "files_exist",
                GateLevel.WARNING,
                False,
                f"{len(missing_files)} referenced files do not exist yet",
                {"missing": missing_files}
            )
        else:
            return ValidationResult(
                "files_exist",
                GateLevel.INFO,
                True,
                f"All {len(task.files_affected)} referenced files exist or are patterns"
            )

    def _check_confidence_threshold(self, task: Task) -> ValidationResult:
        """Check if confidence is above warning threshold"""
        if task.confidence < 30:
            return ValidationResult(
                "confidence_threshold",
                GateLevel.WARNING,
                False,
                f"Low confidence ({task.confidence}%) - consider gathering more information",
                {"confidence": task.confidence, "threshold": 30}
            )
        elif task.confidence >= 80:
            return ValidationResult(
                "confidence_threshold",
                GateLevel.INFO,
                True,
                f"High confidence ({task.confidence}%)"
            )
        else:
            return ValidationResult(
                "confidence_threshold",
                GateLevel.INFO,
                True,
                f"Moderate confidence ({task.confidence}%)"
            )

    def _check_assumptions_documented(self, task: Task) -> ValidationResult:
        """Check if assumptions are documented"""
        if not task.assumptions:
            return ValidationResult(
                "assumptions_documented",
                GateLevel.WARNING,
                False,
                "No assumptions documented for this task"
            )
        else:
            return ValidationResult(
                "assumptions_documented",
                GateLevel.INFO,
                True,
                f"{len(task.assumptions)} assumptions documented"
            )

    def _check_task_finished(self, task: Task) -> ValidationResult:
        """Check if task is marked as finished"""
        if task.status == TaskStatus.FINISHED.value:
            return ValidationResult(
                "task_finished",
                GateLevel.INFO,
                True,
                "Task marked as finished"
            )
        else:
            return ValidationResult(
                "task_finished",
                GateLevel.WARNING,
                False,
                f"Task status is '{task.status}' not 'Finished'"
            )

    def _check_completion_notes(self, task: Task) -> ValidationResult:
        """Check if completion notes are provided"""
        if task.completion_notes:
            word_count = len(task.completion_notes.split())
            if word_count >= 10:
                return ValidationResult(
                    "completion_notes",
                    GateLevel.INFO,
                    True,
                    f"Detailed completion notes provided ({word_count} words)"
                )
            else:
                return ValidationResult(
                    "completion_notes",
                    GateLevel.WARNING,
                    False,
                    f"Brief completion notes ({word_count} words) - consider adding more detail"
                )
        else:
            return ValidationResult(
                "completion_notes",
                GateLevel.WARNING,
                False,
                "No completion notes provided"
            )

    def _check_files_modified(self, task: Task) -> ValidationResult:
        """Check if expected files were modified"""
        if not task.files_affected:
            return ValidationResult(
                "files_modified",
                GateLevel.INFO,
                True,
                "No files expected to be modified"
            )

        # For now, just check existence - could enhance with modification time
        existing_count = sum(
            1 for f in task.files_affected
            if (self.base_path / f).exists() or "*" in f
        )

        if existing_count == len(task.files_affected):
            return ValidationResult(
                "files_modified",
                GateLevel.INFO,
                True,
                f"All {existing_count} expected files exist"
            )
        else:
            return ValidationResult(
                "files_modified",
                GateLevel.WARNING,
                False,
                f"Only {existing_count}/{len(task.files_affected)} expected files exist"
            )

    def _check_and_complete_parent(self, task: Task) -> bool:
        """Check and auto-complete parent if needed"""
        if task.parent_task:
            return self.task_manager.check_parent_completion(task.id)
        return False

    def _suggest_patterns(self, task: Task) -> ValidationResult:
        """Suggest relevant patterns based on task"""
        suggestions = []

        # Suggest based on keywords in title/description
        text = (task.title + " " + task.description).lower()

        if "test" in text:
            suggestions.append("Consider adding pytest tests")
        if "api" in text or "endpoint" in text:
            suggestions.append("Consider API documentation")
        if "database" in text or "schema" in text:
            suggestions.append("Consider migration scripts")
        if "ui" in text or "frontend" in text:
            suggestions.append("Consider accessibility testing")
        if "performance" in text or "optimize" in text:
            suggestions.append("Consider benchmarking")

        if suggestions:
            return ValidationResult(
                "pattern_suggestions",
                GateLevel.INFO,
                True,
                "Pattern suggestions available",
                {"suggestions": suggestions}
            )
        else:
            return ValidationResult(
                "pattern_suggestions",
                GateLevel.INFO,
                True,
                "No specific patterns to suggest"
            )

    def _check_assumptions_validated(self, task: Task) -> ValidationResult:
        """Check if assumptions were validated during execution"""
        if not task.assumptions:
            return ValidationResult(
                "assumptions_validated",
                GateLevel.INFO,
                True,
                "No assumptions to validate"
            )

        # In a real implementation, would check validation_status field
        if task.validation_status == "validated":
            return ValidationResult(
                "assumptions_validated",
                GateLevel.INFO,
                True,
                "All assumptions validated"
            )
        elif task.validation_status == "pending":
            return ValidationResult(
                "assumptions_validated",
                GateLevel.WARNING,
                False,
                f"{len(task.assumptions)} assumptions not yet validated"
            )
        else:
            return ValidationResult(
                "assumptions_validated",
                GateLevel.INFO,
                True,
                f"Validation status: {task.validation_status}"
            )

    def _check_momentum_updated(self, task: Task) -> ValidationResult:
        """Check if momentum was updated"""
        if task.momentum:
            if task.momentum.get("velocity", 0) > 0:
                return ValidationResult(
                    "momentum_updated",
                    GateLevel.INFO,
                    True,
                    f"Momentum updated - phase: {task.momentum.get('phase')}, velocity: {task.momentum.get('velocity')}"
                )
            else:
                return ValidationResult(
                    "momentum_updated",
                    GateLevel.WARNING,
                    False,
                    "Momentum velocity is 0"
                )
        else:
            return ValidationResult(
                "momentum_updated",
                GateLevel.WARNING,
                False,
                "Momentum not tracked"
            )

    def _log_results(self, context: str, results: List[ValidationResult]):
        """Log validation results to file"""
        try:
            self.gates_log.parent.mkdir(parents=True, exist_ok=True)

            log_entry = {
                "context": context,
                "timestamp": datetime.now().isoformat(),
                "results": [r.to_dict() for r in results],
                "summary": {
                    "total": len(results),
                    "passed": sum(1 for r in results if r.passed),
                    "failed": sum(1 for r in results if not r.passed),
                    "blocking": sum(1 for r in results if r.level == GateLevel.BLOCKING and not r.passed),
                    "warnings": sum(1 for r in results if r.level == GateLevel.WARNING and not r.passed)
                }
            }

            # Append to log file
            with open(self.gates_log, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")

        except Exception as e:
            print(f"Warning: Could not log results: {e}")

    def validate_all_tasks(self) -> Dict[str, Any]:
        """Run validation on all tasks and return summary"""
        task_ids = self.task_manager.get_all_task_ids()
        summary = {
            "total_tasks": len(task_ids),
            "pre_execution_failures": [],
            "post_execution_warnings": [],
            "breakdown_required": [],
            "low_confidence": []
        }

        for task_id in task_ids:
            task = self.task_manager.load_task(task_id)
            if not task:
                continue

            # Check pre-execution for pending tasks
            if task.status == TaskStatus.PENDING.value:
                can_proceed, results = self.run_pre_execution_gates(task_id)
                if not can_proceed:
                    summary["pre_execution_failures"].append(task_id)

            # Check if breakdown required
            if task.difficulty >= 7 and not task.subtasks:
                summary["breakdown_required"].append(task_id)

            # Check confidence
            if task.confidence < 30:
                summary["low_confidence"].append((task_id, task.confidence))

            # Check post-execution for finished tasks
            if task.status == TaskStatus.FINISHED.value:
                all_passed, results = self.run_post_execution_gates(task_id)
                warnings = [r for r in results if r.level == GateLevel.WARNING and not r.passed]
                if warnings:
                    summary["post_execution_warnings"].append((task_id, len(warnings)))

        return summary


    def _check_file_conflicts(self, task: Task) -> ValidationResult:
        """Check for file conflicts with other in-progress tasks"""
        if not CONFLICT_DETECTOR_AVAILABLE:
            return ValidationResult(
                "file_conflicts",
                GateLevel.INFO,
                True,
                "File conflict detection not available"
            )

        detector = ConflictDetector()

        # Get all in-progress tasks
        in_progress_tasks = []
        for task_file in Path(self.base_path / ".claude" / "tasks").glob("task-*.json"):
            try:
                with open(task_file, 'r') as f:
                    other_task = json.load(f)
                    if other_task.get('status') == 'In Progress' and other_task['id'] != task.id:
                        in_progress_tasks.append(other_task['id'])
            except:
                continue

        if not in_progress_tasks:
            return ValidationResult(
                "file_conflicts",
                GateLevel.INFO,
                True,
                "No other tasks in progress"
            )

        # Check for conflicts
        task_ids = [task.id] + in_progress_tasks
        can_parallel, blocking = detector.validate_parallel_execution(task_ids)

        if can_parallel:
            return ValidationResult(
                "file_conflicts",
                GateLevel.INFO,
                True,
                "No file conflicts detected"
            )
        else:
            return ValidationResult(
                "file_conflicts",
                GateLevel.BLOCKING,
                False,
                f"File conflicts with tasks: {', '.join(in_progress_tasks)}",
                {"blocking_conflicts": len(blocking)}
            )

    def _check_lock_availability(self, task: Task) -> ValidationResult:
        """Check if required file locks are available"""
        if not LOCKS_AVAILABLE:
            return ValidationResult(
                "lock_availability",
                GateLevel.INFO,
                True,
                "File locking not available"
            )

        lock_manager = FileLockManager()
        locked_files = []

        for file_path in task.files_affected:
            # Skip patterns and directories
            if '*' in file_path or file_path.endswith('/'):
                continue

            file_p = Path(file_path)
            if lock_manager.is_locked(file_p):
                locked_files.append(str(file_p))

        if locked_files:
            return ValidationResult(
                "lock_availability",
                GateLevel.WARNING,
                False,
                f"Files currently locked: {', '.join(locked_files[:3])}",
                {"locked_count": len(locked_files)}
            )
        else:
            return ValidationResult(
                "lock_availability",
                GateLevel.INFO,
                True,
                "All required files available"
            )


class ParallelExecutionGates:
    """Validation gates for parallel task execution"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.task_manager = TaskManager(base_path)
        self.gates = ValidationGates(base_path)

    def validate_parallel_group(self, task_ids: List[str]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate a group of tasks for parallel execution

        Returns:
            Tuple of (can_execute_parallel, validation_report)
        """
        report = {
            "can_parallel": False,
            "task_count": len(task_ids),
            "file_conflicts": [],
            "circular_dependencies": [],
            "lock_issues": [],
            "resource_capacity": {},
            "context_budget": {},
            "recommendations": []
        }

        # Check 1: File conflicts
        if CONFLICT_DETECTOR_AVAILABLE:
            detector = ConflictDetector()
            can_parallel, blocking = detector.validate_parallel_execution(task_ids)

            if not can_parallel:
                report["file_conflicts"] = [
                    {
                        "task1": c.task1_id,
                        "task2": c.task2_id,
                        "file": c.file_path,
                        "type": c.conflict_type.value
                    }
                    for c in blocking
                ]
                report["recommendations"].append(
                    "Execute conflicting tasks sequentially or modify files_affected"
                )

        # Check 2: Circular dependencies
        dependency_graph = {}
        for task_id in task_ids:
            task = self.task_manager.load_task(task_id)
            if task:
                dependency_graph[task_id] = task.dependencies

        cycles = self._find_cycles(dependency_graph)
        if cycles:
            report["circular_dependencies"] = cycles
            report["recommendations"].append(
                "Break circular dependencies before parallel execution"
            )

        # Check 3: Lock availability
        if LOCKS_AVAILABLE:
            lock_manager = FileLockManager()
            for task_id in task_ids:
                task = self.task_manager.load_task(task_id)
                if task:
                    for file_path in task.files_affected:
                        if not ('*' in file_path or file_path.endswith('/')):
                            if lock_manager.is_locked(Path(file_path)):
                                report["lock_issues"].append({
                                    "task": task_id,
                                    "file": file_path
                                })

        # Check 4: Resource capacity (simplified check)
        report["resource_capacity"] = {
            "max_parallel_tasks": 5,  # Configurable limit
            "requested": len(task_ids),
            "available": max(0, 5 - len(task_ids))
        }

        if len(task_ids) > 5:
            report["recommendations"].append(
                f"Consider batching tasks (max 5, requested {len(task_ids)})"
            )

        # Check 5: Context budget
        total_complexity = 0
        for task_id in task_ids:
            task = self.task_manager.load_task(task_id)
            if task:
                total_complexity += task.difficulty

        report["context_budget"] = {
            "total_complexity": total_complexity,
            "max_complexity": 30,  # Configurable limit
            "within_budget": total_complexity <= 30
        }

        if total_complexity > 30:
            report["recommendations"].append(
                f"High combined complexity ({total_complexity}), consider smaller batches"
            )

        # Final determination
        report["can_parallel"] = (
            len(report["file_conflicts"]) == 0 and
            len(report["circular_dependencies"]) == 0 and
            len(report["lock_issues"]) == 0 and
            report["resource_capacity"]["available"] >= 0 and
            report["context_budget"]["within_budget"]
        )

        return report["can_parallel"], report

    def _find_cycles(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """Find circular dependencies in task graph"""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, path[:]):
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
                    return True

            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                dfs(node, [])

        return cycles

    def suggest_execution_batches(self, task_ids: List[str]) -> List[List[str]]:
        """Suggest optimal batches for parallel execution"""
        if not CONFLICT_DETECTOR_AVAILABLE:
            # Simple batching without conflict detection
            batch_size = 5
            return [task_ids[i:i+batch_size] for i in range(0, len(task_ids), batch_size)]

        detector = ConflictDetector()
        return detector.suggest_execution_order(task_ids)


def main():
    """CLI interface for validation gates"""
    import argparse

    parser = argparse.ArgumentParser(description="Validation Gates - Task validation checks")
    parser.add_argument("command", choices=["pre", "post", "validate-all"],
                       help="Validation command to execute")
    parser.add_argument("--task-id", help="Task ID for validation")
    parser.add_argument("--base-path", default=".", help="Base project path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    gates = ValidationGates(args.base_path)

    if args.command == "pre":
        if not args.task_id:
            print("Task ID required for pre-execution validation")
            sys.exit(1)

        can_proceed, results = gates.run_pre_execution_gates(args.task_id)

        if args.json:
            output = {
                "can_proceed": can_proceed,
                "results": [r.to_dict() for r in results]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\nPre-execution validation for task {args.task_id}:")
            print("-" * 50)

            for result in results:
                status = "✓" if result.passed else "✗"
                level_icon = {
                    GateLevel.BLOCKING: "🚫",
                    GateLevel.WARNING: "⚠️",
                    GateLevel.INFO: "ℹ️"
                }.get(result.level, "")

                print(f"{status} {level_icon} {result.check_name}: {result.message}")

                if result.details:
                    for key, value in result.details.items():
                        print(f"    {key}: {value}")

            print("-" * 50)
            if can_proceed:
                print("✅ All blocking gates passed - OK to proceed")
            else:
                print("❌ Blocking gates failed - Fix issues before proceeding")

    elif args.command == "post":
        if not args.task_id:
            print("Task ID required for post-execution validation")
            sys.exit(1)

        all_passed, results = gates.run_post_execution_gates(args.task_id)

        if args.json:
            output = {
                "all_passed": all_passed,
                "results": [r.to_dict() for r in results]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\nPost-execution validation for task {args.task_id}:")
            print("-" * 50)

            for result in results:
                status = "✓" if result.passed else "✗"
                level_icon = {
                    GateLevel.BLOCKING: "🚫",
                    GateLevel.WARNING: "⚠️",
                    GateLevel.INFO: "ℹ️"
                }.get(result.level, "")

                print(f"{status} {level_icon} {result.check_name}: {result.message}")

                if result.details:
                    for key, value in result.details.items():
                        print(f"    {key}: {value}")

            print("-" * 50)
            if all_passed:
                print("✅ All checks passed")
            else:
                print("⚠️ Some checks failed - Review warnings")

    elif args.command == "validate-all":
        summary = gates.validate_all_tasks()

        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("\nTask System Validation Summary")
            print("=" * 50)
            print(f"Total tasks: {summary['total_tasks']}")
            print(f"Tasks needing breakdown: {len(summary['breakdown_required'])}")
            if summary['breakdown_required']:
                print(f"  {', '.join(summary['breakdown_required'])}")
            print(f"Tasks with pre-execution failures: {len(summary['pre_execution_failures'])}")
            if summary['pre_execution_failures']:
                print(f"  {', '.join(summary['pre_execution_failures'])}")
            print(f"Tasks with low confidence: {len(summary['low_confidence'])}")
            if summary['low_confidence']:
                for task_id, confidence in summary['low_confidence']:
                    print(f"  {task_id}: {confidence}%")
            print(f"Finished tasks with warnings: {len(summary['post_execution_warnings'])}")
            if summary['post_execution_warnings']:
                for task_id, warning_count in summary['post_execution_warnings']:
                    print(f"  {task_id}: {warning_count} warnings")


if __name__ == "__main__":
    main()