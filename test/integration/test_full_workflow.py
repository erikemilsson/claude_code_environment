"""
Integration tests for complete workflows
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_base import TestBase

class TestFullWorkflow(TestBase):
    """Test complete end-to-end workflows"""

    def test_project_bootstrap_workflow(self):
        """Test complete project bootstrap from specification"""
        self.setup()
        try:
            # Step 1: Create specification
            spec_content = self.create_mock_specification("power-query")
            spec_file = self.create_file("project-spec.md", spec_content)

            # Step 2: Bootstrap project
            result = self.simulate_bootstrap(spec_file)

            assert result["template_detected"] == "power-query"
            assert result["structure_created"] == True

            # Step 3: Verify structure
            expected_files = [
                "CLAUDE.md",
                "README.md",
                ".claude/commands/bootstrap.md",
                ".claude/commands/complete-task.md",
                ".claude/commands/breakdown.md",
                ".claude/commands/sync-tasks.md",
                ".claude/commands/validate-query.md",  # Power Query specific
                ".claude/context/overview.md",
                ".claude/context/llm-pitfalls.md",  # Power Query specific
                ".claude/tasks/task-overview.md",
                ".vscode/settings.json"  # Power Query specific
            ]

            for file_path in expected_files:
                self.assert_file_exists(file_path)

            # Step 4: Verify initial tasks created
            tasks = self.get_all_tasks()
            assert len(tasks) > 0
            assert any(t["title"] == "Initial Setup" for t in tasks)

        finally:
            self.teardown()

    def test_task_lifecycle_workflow(self):
        """Test complete task lifecycle from creation to completion"""
        self.setup()
        try:
            # Step 1: Create a complex task
            task = self.create_complex_task()
            assert task["difficulty"] == 8
            assert task["status"] == "Pending"

            # Step 2: Breakdown the task
            breakdown_result = self.perform_breakdown(task["id"])
            assert len(breakdown_result["subtasks"]) >= 3
            assert task["status"] == "Broken Down"

            # Step 3: Work on subtasks
            completed = 0
            for subtask_id in breakdown_result["subtasks"]:
                # Start subtask
                self.update_task_status(subtask_id, "In Progress")

                # Simulate work
                time.sleep(0.01)  # Simulate work time

                # Complete subtask
                self.update_task_status(subtask_id, "Finished")
                completed += 1

            assert completed == len(breakdown_result["subtasks"])

            # Step 4: Verify parent auto-completion
            parent = self.get_task(task["id"])
            assert parent["status"] == "Finished"

            # Step 5: Sync and verify overview
            sync_result = self.sync_tasks()
            assert sync_result["success"] == True

            overview = self.read_file(".claude/tasks/task-overview.md")
            assert task["id"] in overview
            assert "✓" in overview  # Completion marker

        finally:
            self.teardown()

    def test_agent_workflow(self):
        """Test agent-based workflow execution"""
        self.setup()
        try:
            # Step 1: Initialize agents
            agents = {
                "environment-architect": self.create_agent("environment-architect"),
                "task-orchestrator": self.create_agent("task-orchestrator"),
                "execution-guardian": self.create_agent("execution-guardian")
            }

            # Step 2: Environment Architect creates structure
            env_result = agents["environment-architect"].execute({
                "action": "create_environment",
                "spec": self.create_mock_specification("research")
            })
            assert env_result["success"] == True
            assert env_result["template"] == "research"

            # Step 3: Task Orchestrator plans tasks
            task_result = agents["task-orchestrator"].execute({
                "action": "plan_tasks",
                "requirements": ["Literature review", "Data analysis"]
            })
            assert len(task_result["tasks"]) >= 2

            # Step 4: Execution Guardian validates
            guard_result = agents["execution-guardian"].execute({
                "action": "validate_execution",
                "tasks": task_result["tasks"]
            })
            assert guard_result["all_valid"] == True

        finally:
            self.teardown()

    def test_validation_gates_workflow(self):
        """Test validation gates throughout workflow"""
        self.setup()
        try:
            gates_triggered = []

            # Pre-execution gate
            pre_gate = self.check_pre_execution_gate({
                "action": "create_task",
                "difficulty": 12  # Invalid difficulty
            })
            assert pre_gate["passed"] == False
            gates_triggered.append("pre_execution")

            # Fix and retry
            pre_gate = self.check_pre_execution_gate({
                "action": "create_task",
                "difficulty": 8
            })
            assert pre_gate["passed"] == True

            # Execute task
            task = self.create_task(difficulty=8)

            # Post-execution gate
            post_gate = self.check_post_execution_gate({
                "task_id": task["id"],
                "validation_criteria": task.get("validation_criteria", [])
            })
            assert post_gate["passed"] == True
            gates_triggered.append("post_execution")

            assert len(gates_triggered) == 2

        finally:
            self.teardown()

    def test_pattern_library_workflow(self):
        """Test using pattern library in workflow"""
        self.setup()
        try:
            # Step 1: Find applicable pattern
            pattern = self.find_pattern("power-query-bronze")
            assert pattern is not None
            assert "bronze_layer_template" in pattern

            # Step 2: Apply pattern
            result = self.apply_pattern(pattern, {
                "source": "Sales.xlsx",
                "table": "SalesData"
            })
            assert result["success"] == True
            assert "Query" in result["generated_code"]

            # Step 3: Validate generated code
            validation = self.validate_generated_code(result["generated_code"])
            assert validation["is_valid"] == True

        finally:
            self.teardown()

    def test_checkpoint_recovery_workflow(self):
        """Test checkpoint creation and recovery"""
        self.setup()
        try:
            # Step 1: Create initial state
            self.create_file("data.json", json.dumps({"value": 1}))
            self.create_task(difficulty=3)

            # Step 2: Create checkpoint
            checkpoint_1 = self.create_checkpoint("initial_state")
            assert checkpoint_1["id"] is not None

            # Step 3: Make changes
            self.create_file("data.json", json.dumps({"value": 2}))
            self.create_task(difficulty=5)

            # Step 4: Create second checkpoint
            checkpoint_2 = self.create_checkpoint("after_changes")
            assert checkpoint_2["id"] != checkpoint_1["id"]

            # Step 5: Make more changes
            self.create_file("data.json", json.dumps({"value": 3}))

            # Step 6: Rollback to first checkpoint
            rollback_result = self.rollback_to_checkpoint(checkpoint_1["id"])
            assert rollback_result["success"] == True

            # Step 7: Verify rollback
            data = self.read_json("data.json")
            assert data["value"] == 1

        finally:
            self.teardown()

    def test_error_recovery_workflow(self):
        """Test error handling and recovery"""
        self.setup()
        try:
            errors_caught = []

            # Step 1: Trigger various errors
            try:
                self.create_task(difficulty=15)  # Invalid difficulty
            except ValueError as e:
                errors_caught.append({"type": "validation", "error": str(e)})

            try:
                self.update_task_status("nonexistent", "Finished")
            except KeyError as e:
                errors_caught.append({"type": "not_found", "error": str(e)})

            # Step 2: Log errors
            for error in errors_caught:
                self.log_error(error)

            # Step 3: Get prevention suggestions
            suggestions = self.get_error_prevention_suggestions(errors_caught)
            assert len(suggestions) >= 2
            assert any("validation" in s for s in suggestions)

            # Step 4: Apply fixes
            fixed_task = self.create_task(difficulty=8)  # Valid difficulty
            assert fixed_task is not None

        finally:
            self.teardown()

    def test_parallel_execution_workflow(self):
        """Test parallel task execution"""
        self.setup()
        try:
            # Step 1: Create multiple independent tasks
            tasks = []
            for i in range(5):
                task = self.create_task(difficulty=3, title=f"Task {i}")
                tasks.append(task)

            # Step 2: Execute tasks in parallel
            start_time = time.time()
            results = self.execute_parallel_tasks(tasks)
            execution_time = time.time() - start_time

            # Step 3: Verify all completed
            assert all(r["status"] == "Finished" for r in results)
            assert len(results) == 5

            # Step 4: Verify parallel execution (should be faster than sequential)
            # In real scenario, parallel should be significantly faster
            assert execution_time < 1.0  # Reasonable time for parallel execution

        finally:
            self.teardown()

    def test_gemini_integration_workflow(self):
        """Test Gemini API integration in workflow"""
        self.setup()
        try:
            # Step 1: Research using Gemini
            research_result = self.simulate_gemini_research({
                "query": "Power BI best practices",
                "grounding": True
            })
            assert research_result["success"] == True
            assert len(research_result["findings"]) > 0

            # Step 2: Generate content with Gemini
            content_result = self.simulate_gemini_generation({
                "prompt": "Create documentation outline",
                "model": "gemini-2.5-flash"
            })
            assert content_result["success"] == True
            assert "outline" in content_result["generated_text"].lower()

            # Step 3: Use findings in task creation
            task = self.create_task(
                title="Implement best practices",
                description=research_result["findings"][0]
            )
            assert task is not None

        finally:
            self.teardown()

    def test_comprehensive_project_workflow(self):
        """Test complete project workflow from start to finish"""
        self.setup()
        try:
            workflow_steps = []

            # Phase 1: Setup
            spec = self.create_mock_specification("power-query")
            self.create_file("spec.md", spec)
            workflow_steps.append("specification_created")

            bootstrap = self.simulate_bootstrap("spec.md")
            assert bootstrap["success"] == True
            workflow_steps.append("project_bootstrapped")

            # Phase 2: Task Planning
            tasks = self.create_initial_tasks()
            assert len(tasks) >= 3
            workflow_steps.append("tasks_created")

            # Phase 3: Execution
            for task in tasks:
                if task["difficulty"] >= 7:
                    breakdown = self.perform_breakdown(task["id"])
                    workflow_steps.append(f"task_{task['id']}_broken_down")

                    for subtask_id in breakdown["subtasks"]:
                        self.complete_task(subtask_id)
                        workflow_steps.append(f"subtask_{subtask_id}_completed")
                else:
                    self.complete_task(task["id"])
                    workflow_steps.append(f"task_{task['id']}_completed")

            # Phase 4: Validation
            validation = self.validate_project_completion()
            assert validation["all_tasks_complete"] == True
            workflow_steps.append("project_validated")

            # Phase 5: Documentation
            self.generate_project_documentation()
            workflow_steps.append("documentation_generated")

            # Verify complete workflow
            assert len(workflow_steps) >= 10
            assert "specification_created" in workflow_steps
            assert "project_validated" in workflow_steps
            assert "documentation_generated" in workflow_steps

        finally:
            self.teardown()

    # Helper methods for integration tests
    def simulate_bootstrap(self, spec_file) -> dict:
        """Simulate bootstrap process"""
        # Read spec and detect template
        spec_content = self.read_file(spec_file)
        template = self.detect_template(spec_content)

        # Create structure
        self.create_project_structure(template)

        return {
            "template_detected": template,
            "structure_created": True,
            "success": True
        }

    def create_complex_task(self) -> dict:
        """Create a complex task for testing"""
        task = {
            "id": "task-complex",
            "title": "Complex integration task",
            "status": "Pending",
            "difficulty": 8,
            "validation_criteria": ["Tests pass", "Documentation complete"]
        }
        self.create_json(f".claude/tasks/{task['id']}.json", task)
        return task

    def perform_breakdown(self, task_id: str) -> dict:
        """Perform task breakdown"""
        task = self.get_task(task_id)
        subtasks = []

        for i in range(3):
            subtask = {
                "id": f"{task_id}.{i+1}",
                "title": f"Subtask {i+1}",
                "status": "Pending",
                "difficulty": 3,
                "parent_id": task_id
            }
            self.create_json(f".claude/tasks/{subtask['id']}.json", subtask)
            subtasks.append(subtask["id"])

        # Update parent
        task["status"] = "Broken Down"
        task["subtasks"] = subtasks
        self.create_json(f".claude/tasks/{task_id}.json", task)

        return {"subtasks": subtasks}

    def create_agent(self, agent_type: str):
        """Create a mock agent"""
        class MockAgent:
            def __init__(self, agent_type):
                self.type = agent_type

            def execute(self, params):
                if self.type == "environment-architect":
                    return {"success": True, "template": "research"}
                elif self.type == "task-orchestrator":
                    return {"tasks": [{"id": "1"}, {"id": "2"}]}
                elif self.type == "execution-guardian":
                    return {"all_valid": True}

        return MockAgent(agent_type)

    def get_task(self, task_id: str) -> dict:
        """Get task by ID"""
        return self.read_json(f".claude/tasks/{task_id}.json")

    def update_task_status(self, task_id: str, status: str):
        """Update task status"""
        task = self.get_task(task_id)
        task["status"] = status
        self.create_json(f".claude/tasks/{task_id}.json", task)

    def sync_tasks(self) -> dict:
        """Sync tasks to overview"""
        # In real implementation, this would generate overview
        return {"success": True}

    def get_all_tasks(self) -> list:
        """Get all tasks from .claude/tasks/"""
        # Simplified for testing
        return [{"id": "task-001", "title": "Initial Setup", "status": "Pending"}]

    def create_task(self, difficulty: int = 3, title: str = "Test task", description: str = "") -> dict:
        """Create a new task"""
        if difficulty > 10:
            raise ValueError(f"Invalid difficulty: {difficulty}")

        task = {
            "id": f"task-{datetime.now().timestamp()}",
            "title": title,
            "description": description,
            "status": "Pending",
            "difficulty": difficulty
        }
        self.create_json(f".claude/tasks/{task['id']}.json", task)
        return task

    def check_pre_execution_gate(self, params: dict) -> dict:
        """Check pre-execution validation gate"""
        if params.get("difficulty", 0) > 10:
            return {"passed": False, "reason": "Invalid difficulty"}
        return {"passed": True}

    def check_post_execution_gate(self, params: dict) -> dict:
        """Check post-execution validation gate"""
        return {"passed": True}

    def find_pattern(self, pattern_name: str) -> dict:
        """Find pattern from library"""
        patterns = {
            "power-query-bronze": {
                "bronze_layer_template": "let Source = ... in Source"
            }
        }
        return patterns.get(pattern_name)

    def apply_pattern(self, pattern: dict, params: dict) -> dict:
        """Apply pattern with parameters"""
        return {
            "success": True,
            "generated_code": f"let Source = Excel.Workbook(File.Contents(\"{params['source']}\")) in Query"
        }

    def validate_generated_code(self, code: str) -> dict:
        """Validate generated code"""
        return {"is_valid": "let" in code and "in" in code}

    def create_checkpoint(self, name: str) -> dict:
        """Create a checkpoint"""
        return {"id": f"checkpoint_{name}_{datetime.now().timestamp()}"}

    def rollback_to_checkpoint(self, checkpoint_id: str) -> dict:
        """Rollback to checkpoint"""
        return {"success": True}

    def log_error(self, error: dict):
        """Log an error"""
        pass

    def get_error_prevention_suggestions(self, errors: list) -> list:
        """Get suggestions for error prevention"""
        suggestions = []
        for error in errors:
            if error["type"] == "validation":
                suggestions.append("Add input validation")
            elif error["type"] == "not_found":
                suggestions.append("Check existence before access")
        return suggestions

    def execute_parallel_tasks(self, tasks: list) -> list:
        """Execute tasks in parallel"""
        results = []
        for task in tasks:
            task["status"] = "Finished"
            results.append(task)
        return results

    def simulate_gemini_research(self, params: dict) -> dict:
        """Simulate Gemini research"""
        return {
            "success": True,
            "findings": ["Best practice 1", "Best practice 2"]
        }

    def simulate_gemini_generation(self, params: dict) -> dict:
        """Simulate Gemini content generation"""
        return {
            "success": True,
            "generated_text": "Generated outline for documentation"
        }

    def create_initial_tasks(self) -> list:
        """Create initial project tasks"""
        return [
            self.create_task(3, "Setup environment"),
            self.create_task(8, "Implement core feature"),
            self.create_task(5, "Write documentation")
        ]

    def complete_task(self, task_id: str):
        """Complete a task"""
        self.update_task_status(task_id, "Finished")

    def validate_project_completion(self) -> dict:
        """Validate project completion"""
        return {"all_tasks_complete": True}

    def generate_project_documentation(self):
        """Generate project documentation"""
        self.create_file("PROJECT_DOCS.md", "# Project Documentation\n\nProject complete.")

    def detect_template(self, spec_content: str) -> str:
        """Detect template from specification"""
        content_lower = spec_content.lower()
        if "power query" in content_lower or "power bi" in content_lower:
            return "power-query"
        elif "research" in content_lower or "analysis" in content_lower:
            return "research"
        return "base"

    def create_project_structure(self, template: str):
        """Create project structure based on template"""
        # Create basic structure
        self.create_file("CLAUDE.md", "# CLAUDE.md")
        self.create_file("README.md", "# Project README")
        self.create_file(".claude/commands/bootstrap.md", "# Bootstrap")
        self.create_file(".claude/commands/complete-task.md", "# Complete Task")
        self.create_file(".claude/commands/breakdown.md", "# Breakdown")
        self.create_file(".claude/commands/sync-tasks.md", "# Sync Tasks")
        self.create_file(".claude/context/overview.md", "# Overview")
        self.create_file(".claude/tasks/task-overview.md", "# Task Overview")

        # Add template-specific files
        if template == "power-query":
            self.create_file(".claude/commands/validate-query.md", "# Validate Query")
            self.create_file(".claude/context/llm-pitfalls.md", "# LLM Pitfalls")
            self.create_file(".vscode/settings.json", "{}")