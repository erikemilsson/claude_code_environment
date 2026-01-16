"""
Unit tests for task management system
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_base import TestBase

class TestTaskManagement(TestBase):
    """Test task management functionality"""

    def test_task_creation(self):
        """Test creating a new task"""
        self.setup()
        try:
            task_data = {
                "id": "task-001",
                "title": "Implement feature X",
                "description": "Implement the new feature X with all requirements",
                "status": "Pending",
                "difficulty": 5,
                "priority": "high",
                "created_at": datetime.now().isoformat(),
                "dependencies": [],
                "validation_criteria": [
                    "All tests pass",
                    "Code reviewed",
                    "Documentation updated"
                ],
                "context_requirements": [
                    "Understanding of existing codebase",
                    "Access to API documentation"
                ],
                "belief_score": 0.8,
                "confidence_level": "high",
                "assumptions": [],
                "completion_percentage": 0
            }

            self.create_json(".claude/tasks/task-001.json", task_data)
            loaded = self.read_json(".claude/tasks/task-001.json")

            assert loaded["id"] == "task-001"
            assert loaded["status"] == "Pending"
            assert loaded["difficulty"] == 5
            assert len(loaded["validation_criteria"]) == 3

        finally:
            self.teardown()

    def test_task_status_transitions(self):
        """Test valid task status transitions"""
        self.setup()
        try:
            # Valid transitions
            valid_transitions = [
                ("Pending", "In Progress"),
                ("In Progress", "Blocked"),
                ("Blocked", "In Progress"),
                ("In Progress", "Finished"),
                ("Pending", "Broken Down")
            ]

            for from_status, to_status in valid_transitions:
                assert self.is_valid_transition(from_status, to_status), \
                    f"Transition from {from_status} to {to_status} should be valid"

            # Invalid transitions
            invalid_transitions = [
                ("Finished", "Pending"),
                ("Broken Down", "In Progress"),
                ("Finished", "Blocked")
            ]

            for from_status, to_status in invalid_transitions:
                assert not self.is_valid_transition(from_status, to_status), \
                    f"Transition from {from_status} to {to_status} should be invalid"

        finally:
            self.teardown()

    def test_task_breakdown(self):
        """Test breaking down high difficulty tasks"""
        self.setup()
        try:
            # Parent task with difficulty >= 7
            parent_task = {
                "id": "task-100",
                "title": "Implement authentication system",
                "status": "Pending",
                "difficulty": 8,
                "priority": "critical",
                "subtasks": []
            }

            # Break down into subtasks
            subtasks = [
                {
                    "id": "task-100.1",
                    "title": "Design authentication schema",
                    "status": "Pending",
                    "difficulty": 3,
                    "parent_id": "task-100"
                },
                {
                    "id": "task-100.2",
                    "title": "Implement login endpoint",
                    "status": "Pending",
                    "difficulty": 4,
                    "parent_id": "task-100"
                },
                {
                    "id": "task-100.3",
                    "title": "Add JWT token handling",
                    "status": "Pending",
                    "difficulty": 4,
                    "parent_id": "task-100"
                },
                {
                    "id": "task-100.4",
                    "title": "Write authentication tests",
                    "status": "Pending",
                    "difficulty": 3,
                    "parent_id": "task-100"
                }
            ]

            # Update parent task
            parent_task["status"] = "Broken Down"
            parent_task["subtasks"] = [st["id"] for st in subtasks]

            # Validate breakdown
            assert parent_task["status"] == "Broken Down"
            assert len(parent_task["subtasks"]) == 4

            # All subtasks should have difficulty < 7
            for subtask in subtasks:
                assert subtask["difficulty"] < 7, \
                    f"Subtask {subtask['id']} has difficulty >= 7"

            # Sum of subtask difficulties should approximate parent
            total_difficulty = sum(st["difficulty"] for st in subtasks)
            assert 10 <= total_difficulty <= 20, \
                "Total subtask difficulty should be reasonable"

        finally:
            self.teardown()

    def test_task_auto_completion(self):
        """Test automatic parent task completion when all subtasks complete"""
        self.setup()
        try:
            # Create parent and subtasks
            parent = {
                "id": "task-200",
                "title": "Parent task",
                "status": "Broken Down",
                "subtasks": ["task-200.1", "task-200.2", "task-200.3"]
            }

            subtasks = [
                {"id": "task-200.1", "status": "Finished", "parent_id": "task-200"},
                {"id": "task-200.2", "status": "Finished", "parent_id": "task-200"},
                {"id": "task-200.3", "status": "In Progress", "parent_id": "task-200"}
            ]

            # Check parent should not be complete yet
            assert not self.should_auto_complete(parent, subtasks)

            # Complete last subtask
            subtasks[2]["status"] = "Finished"

            # Now parent should auto-complete
            assert self.should_auto_complete(parent, subtasks)

        finally:
            self.teardown()

    def test_task_dependencies(self):
        """Test task dependency validation"""
        self.setup()
        try:
            tasks = {
                "task-001": {
                    "id": "task-001",
                    "status": "Finished",
                    "dependencies": []
                },
                "task-002": {
                    "id": "task-002",
                    "status": "In Progress",
                    "dependencies": ["task-001"]
                },
                "task-003": {
                    "id": "task-003",
                    "status": "Pending",
                    "dependencies": ["task-001", "task-002"]
                }
            }

            # Task 002 can start (001 is finished)
            assert self.can_start_task(tasks["task-002"], tasks)

            # Task 003 cannot start (002 not finished)
            assert not self.can_start_task(tasks["task-003"], tasks)

            # Complete task 002
            tasks["task-002"]["status"] = "Finished"

            # Now task 003 can start
            assert self.can_start_task(tasks["task-003"], tasks)

        finally:
            self.teardown()

    def test_task_overview_generation(self):
        """Test generating task-overview.md from JSON files"""
        self.setup()
        try:
            # Create sample tasks
            tasks = [
                {
                    "id": "task-001",
                    "title": "Setup project",
                    "status": "Finished",
                    "difficulty": 2,
                    "priority": "high"
                },
                {
                    "id": "task-002",
                    "title": "Implement core feature",
                    "status": "In Progress",
                    "difficulty": 5,
                    "priority": "critical",
                    "completion_percentage": 60
                },
                {
                    "id": "task-003",
                    "title": "Write documentation",
                    "status": "Pending",
                    "difficulty": 3,
                    "priority": "medium"
                }
            ]

            for task in tasks:
                self.create_json(f".claude/tasks/{task['id']}.json", task)

            # Generate overview
            overview = self.generate_task_overview(tasks)

            # Check overview contains expected sections
            assert "# Task Overview" in overview
            assert "## Summary" in overview
            assert "Total Tasks: 3" in overview
            assert "Finished: 1" in overview
            assert "In Progress: 1" in overview
            assert "Pending: 1" in overview

            # Check task table
            assert "| ID | Title | Status | Difficulty | Priority |" in overview
            assert "task-001" in overview
            assert "Setup project" in overview
            assert "✓" in overview  # Finished marker

        finally:
            self.teardown()

    def test_belief_tracking(self):
        """Test belief tracking in tasks"""
        self.setup()
        try:
            task = {
                "id": "task-300",
                "title": "Complex analysis",
                "status": "In Progress",
                "belief_score": 0.7,
                "confidence_level": "medium",
                "assumptions": [
                    {
                        "assumption": "Database contains required data",
                        "confidence": 0.8,
                        "validated": False
                    },
                    {
                        "assumption": "API rate limits won't be exceeded",
                        "confidence": 0.6,
                        "validated": True
                    }
                ],
                "validation_attempts": [
                    {
                        "timestamp": datetime.now().isoformat(),
                        "validation": "Check database schema",
                        "result": "success",
                        "belief_adjustment": 0.1
                    }
                ]
            }

            self.create_json(".claude/tasks/task-300.json", task)
            loaded = self.read_json(".claude/tasks/task-300.json")

            assert loaded["belief_score"] == 0.7
            assert len(loaded["assumptions"]) == 2
            assert loaded["assumptions"][1]["validated"] == True
            assert len(loaded["validation_attempts"]) == 1

        finally:
            self.teardown()

    def test_momentum_tracking(self):
        """Test momentum tracking for tasks"""
        self.setup()
        try:
            task = {
                "id": "task-400",
                "title": "Feature implementation",
                "status": "In Progress",
                "momentum": {
                    "velocity": 0.8,
                    "trend": "increasing",
                    "blockers": [],
                    "last_progress": datetime.now().isoformat(),
                    "checkpoints": [
                        {
                            "timestamp": datetime.now().isoformat(),
                            "progress": 30,
                            "note": "Initial implementation"
                        }
                    ]
                }
            }

            self.create_json(".claude/tasks/task-400.json", task)
            loaded = self.read_json(".claude/tasks/task-400.json")

            assert "momentum" in loaded
            assert loaded["momentum"]["velocity"] == 0.8
            assert loaded["momentum"]["trend"] == "increasing"
            assert len(loaded["momentum"]["checkpoints"]) == 1

        finally:
            self.teardown()

    # Helper methods
    def is_valid_transition(self, from_status: str, to_status: str) -> bool:
        """Check if a status transition is valid"""
        valid = {
            "Pending": ["In Progress", "Broken Down"],
            "In Progress": ["Blocked", "Finished", "Pending"],
            "Blocked": ["In Progress", "Pending"],
            "Broken Down": ["Finished"],
            "Finished": []
        }
        return to_status in valid.get(from_status, [])

    def should_auto_complete(self, parent: dict, subtasks: list) -> bool:
        """Check if parent should auto-complete"""
        if parent["status"] != "Broken Down":
            return False

        for subtask in subtasks:
            if subtask["parent_id"] == parent["id"] and subtask["status"] != "Finished":
                return False

        return True

    def can_start_task(self, task: dict, all_tasks: dict) -> bool:
        """Check if task dependencies are met"""
        for dep_id in task.get("dependencies", []):
            if dep_id in all_tasks and all_tasks[dep_id]["status"] != "Finished":
                return False
        return True

    def generate_task_overview(self, tasks: list) -> str:
        """Generate task overview markdown"""
        finished = sum(1 for t in tasks if t["status"] == "Finished")
        in_progress = sum(1 for t in tasks if t["status"] == "In Progress")
        pending = sum(1 for t in tasks if t["status"] == "Pending")

        overview = f"""# Task Overview

## Summary
- Total Tasks: {len(tasks)}
- Finished: {finished}
- In Progress: {in_progress}
- Pending: {pending}

## Tasks

| ID | Title | Status | Difficulty | Priority |
|---|---|---|---|---|
"""
        for task in tasks:
            status_marker = "✓" if task["status"] == "Finished" else task["status"]
            overview += f"| {task['id']} | {task['title']} | {status_marker} | {task['difficulty']} | {task.get('priority', 'normal')} |\n"

        return overview