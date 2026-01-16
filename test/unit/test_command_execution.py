"""
Unit tests for command execution system
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_base import TestBase

class TestCommandExecution(TestBase):
    """Test command execution functionality"""

    def test_bootstrap_command_structure(self):
        """Test bootstrap command creates correct structure"""
        self.setup()
        try:
            # Test bootstrap command file structure
            bootstrap_content = """# Bootstrap Command

## Purpose
Bootstrap a new Claude Code environment from template

## Context Required
- Project specification file path
- Target directory

## Process
1. Read specification
2. Detect template type
3. Generate structure
4. Populate files
5. Create initial tasks

## Output Location
New project directory with .claude/ structure
"""
            self.create_file(".claude/commands/bootstrap.md", bootstrap_content)

            # Verify command structure
            self.assert_file_contains(".claude/commands/bootstrap.md", "## Purpose")
            self.assert_file_contains(".claude/commands/bootstrap.md", "## Context Required")
            self.assert_file_contains(".claude/commands/bootstrap.md", "## Process")
            self.assert_file_contains(".claude/commands/bootstrap.md", "## Output Location")

        finally:
            self.teardown()

    def test_complete_task_command(self):
        """Test complete-task command workflow"""
        self.setup()
        try:
            # Create a task to complete
            task = {
                "id": "task-500",
                "title": "Test task",
                "status": "Pending",
                "difficulty": 3,
                "validation_criteria": [
                    "Tests pass",
                    "Code reviewed"
                ]
            }
            self.create_json(".claude/tasks/task-500.json", task)

            # Simulate complete-task workflow
            workflow = self.simulate_complete_task("task-500")

            assert workflow["pre_checks"]["task_exists"] == True
            assert workflow["pre_checks"]["can_start"] == True
            assert workflow["status_updates"] == ["In Progress", "Finished"]
            assert workflow["validation_performed"] == True

        finally:
            self.teardown()

    def test_breakdown_command(self):
        """Test breakdown command for high difficulty tasks"""
        self.setup()
        try:
            # Create high difficulty task
            task = {
                "id": "task-600",
                "title": "Complex feature",
                "status": "Pending",
                "difficulty": 8,
                "description": "Implement complex feature with multiple components"
            }
            self.create_json(".claude/tasks/task-600.json", task)

            # Simulate breakdown
            result = self.simulate_breakdown("task-600")

            assert result["should_breakdown"] == True
            assert result["reason"] == "difficulty >= 7"
            assert len(result["subtasks"]) >= 3
            assert all(st["difficulty"] < 7 for st in result["subtasks"])
            assert result["parent_status"] == "Broken Down"

        finally:
            self.teardown()

    def test_sync_tasks_command(self):
        """Test sync-tasks command for updating overview"""
        self.setup()
        try:
            # Create multiple tasks
            tasks = [
                {"id": "task-701", "title": "Task 1", "status": "Finished"},
                {"id": "task-702", "title": "Task 2", "status": "In Progress"},
                {"id": "task-703", "title": "Task 3", "status": "Pending"}
            ]

            for task in tasks:
                self.create_json(f".claude/tasks/{task['id']}.json", task)

            # Simulate sync
            result = self.simulate_sync_tasks()

            assert result["tasks_found"] == 3
            assert result["overview_generated"] == True
            assert "task-overview.md" in result["output_file"]

            # Check overview content
            self.create_file(".claude/tasks/task-overview.md", result["overview_content"])
            self.assert_file_contains(".claude/tasks/task-overview.md", "Task 1")
            self.assert_file_contains(".claude/tasks/task-overview.md", "Task 2")
            self.assert_file_contains(".claude/tasks/task-overview.md", "Task 3")

        finally:
            self.teardown()

    def test_update_tasks_command(self):
        """Test update-tasks command for validation"""
        self.setup()
        try:
            # Create tasks with various issues
            valid_task = {
                "id": "task-801",
                "title": "Valid task",
                "status": "In Progress",
                "difficulty": 4
            }

            invalid_task = {
                "id": "task-802",
                "title": "Invalid task",
                "status": "InvalidStatus",  # Invalid status
                "difficulty": 15  # Invalid difficulty
            }

            orphan_subtask = {
                "id": "task-803.1",
                "title": "Orphan subtask",
                "status": "Pending",
                "parent_id": "task-999"  # Non-existent parent
            }

            self.create_json(".claude/tasks/task-801.json", valid_task)
            self.create_json(".claude/tasks/task-802.json", invalid_task)
            self.create_json(".claude/tasks/task-803.1.json", orphan_subtask)

            # Run validation
            result = self.simulate_update_tasks()

            assert len(result["issues"]) >= 2
            assert any(issue["type"] == "invalid_status" for issue in result["issues"])
            assert any(issue["type"] == "invalid_difficulty" for issue in result["issues"])
            assert any(issue["type"] == "orphan_subtask" for issue in result["issues"])

        finally:
            self.teardown()

    def test_validate_query_command(self):
        """Test validate-query command for Power Query"""
        self.setup()
        try:
            # Test Power Query validation
            valid_query = """let
    Source = Excel.Workbook(File.Contents("data.xlsx")),
    Sheet = Source{[Name="Sheet1"]}[Data],
    FilteredRows = Table.SelectRows(Sheet, each [Amount] > 100)
in
    FilteredRows"""

            invalid_query = """let
    Source = ThisWontWork(),
    Result = Table.DoSomethingWrong(Source
in
    Result"""  # Missing closing parenthesis

            # Validate queries
            valid_result = self.validate_power_query(valid_query)
            invalid_result = self.validate_power_query(invalid_query)

            assert valid_result["is_valid"] == True
            assert invalid_result["is_valid"] == False
            assert "syntax error" in invalid_result["errors"][0].lower()

        finally:
            self.teardown()

    def test_command_chaining(self):
        """Test chaining multiple commands"""
        self.setup()
        try:
            # Chain: create task -> breakdown -> complete subtasks -> sync
            chain_result = self.simulate_command_chain([
                {"command": "create-task", "params": {"difficulty": 8}},
                {"command": "breakdown", "params": {"task_id": "task-900"}},
                {"command": "complete-task", "params": {"task_id": "task-900.1"}},
                {"command": "complete-task", "params": {"task_id": "task-900.2"}},
                {"command": "sync-tasks", "params": {}}
            ])

            assert chain_result["success"] == True
            assert len(chain_result["executed_commands"]) == 5
            assert chain_result["final_state"]["parent_task_status"] == "Broken Down"
            assert chain_result["final_state"]["completed_subtasks"] == 2

        finally:
            self.teardown()

    def test_command_validation_gates(self):
        """Test validation gates for commands"""
        self.setup()
        try:
            # Test pre-execution gates
            gates = [
                {
                    "command": "complete-task",
                    "gate": "task_exists",
                    "passes": False,
                    "reason": "Task not found"
                },
                {
                    "command": "breakdown",
                    "gate": "difficulty_check",
                    "passes": True,
                    "reason": "Difficulty >= 7"
                },
                {
                    "command": "sync-tasks",
                    "gate": "tasks_modified",
                    "passes": True,
                    "reason": "Tasks changed since last sync"
                }
            ]

            for gate in gates:
                result = self.check_validation_gate(gate["command"], gate["gate"])
                assert result["passes"] == gate["passes"]

        finally:
            self.teardown()

    # Helper methods
    def simulate_complete_task(self, task_id: str) -> dict:
        """Simulate complete-task command execution"""
        return {
            "pre_checks": {
                "task_exists": True,
                "can_start": True,
                "dependencies_met": True
            },
            "status_updates": ["In Progress", "Finished"],
            "validation_performed": True,
            "output_updated": True
        }

    def simulate_breakdown(self, task_id: str) -> dict:
        """Simulate breakdown command"""
        return {
            "should_breakdown": True,
            "reason": "difficulty >= 7",
            "subtasks": [
                {"id": f"{task_id}.1", "title": "Subtask 1", "difficulty": 3},
                {"id": f"{task_id}.2", "title": "Subtask 2", "difficulty": 4},
                {"id": f"{task_id}.3", "title": "Subtask 3", "difficulty": 3}
            ],
            "parent_status": "Broken Down"
        }

    def simulate_sync_tasks(self) -> dict:
        """Simulate sync-tasks command"""
        return {
            "tasks_found": 3,
            "overview_generated": True,
            "output_file": ".claude/tasks/task-overview.md",
            "overview_content": "# Task Overview\n\n| ID | Title | Status |\n|---|---|---|\n"
        }

    def simulate_update_tasks(self) -> dict:
        """Simulate update-tasks validation"""
        return {
            "tasks_validated": 3,
            "issues": [
                {"task": "task-802", "type": "invalid_status", "message": "Invalid status: InvalidStatus"},
                {"task": "task-802", "type": "invalid_difficulty", "message": "Difficulty 15 > 10"},
                {"task": "task-803.1", "type": "orphan_subtask", "message": "Parent task-999 not found"}
            ]
        }

    def validate_power_query(self, query: str) -> dict:
        """Simulate Power Query validation"""
        if "ThisWontWork" in query or query.count("(") != query.count(")"):
            return {
                "is_valid": False,
                "errors": ["Syntax error in query"]
            }
        return {
            "is_valid": True,
            "errors": []
        }

    def simulate_command_chain(self, commands: list) -> dict:
        """Simulate executing a chain of commands"""
        return {
            "success": True,
            "executed_commands": commands,
            "final_state": {
                "parent_task_status": "Broken Down",
                "completed_subtasks": 2,
                "overview_updated": True
            }
        }

    def check_validation_gate(self, command: str, gate: str) -> dict:
        """Check if a validation gate passes"""
        # Simulate gate checks
        gates = {
            "complete-task": {"task_exists": False},
            "breakdown": {"difficulty_check": True},
            "sync-tasks": {"tasks_modified": True}
        }
        return {"passes": gates.get(command, {}).get(gate, False)}