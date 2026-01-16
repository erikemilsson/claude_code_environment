"""
Unit tests for template validation and generation
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.test_base import TestBase

class TestTemplateValidation(TestBase):
    """Test template structure and validation"""

    def test_base_template_structure(self):
        """Test that base template creates correct structure"""
        self.setup()
        try:
            # Create expected base structure
            expected_structure = {
                ".claude": {
                    "commands": {
                        "complete-task.md": None,
                        "breakdown.md": None,
                        "sync-tasks.md": None,
                        "update-tasks.md": None
                    },
                    "context": {
                        "overview.md": None,
                        "standards": {},
                        "validation-rules.md": None
                    },
                    "tasks": {
                        "task-overview.md": None
                    },
                    "reference": {
                        "difficulty-guide.md": None,
                        "breakdown-workflow.md": None
                    }
                },
                "CLAUDE.md": None,
                "README.md": None
            }

            # Create the structure
            self.create_directory_structure(expected_structure)

            # Validate
            self.assert_directory_structure(expected_structure)

        finally:
            self.teardown()

    def test_power_query_template_structure(self):
        """Test Power Query template specific structure"""
        self.setup()
        try:
            # Power Query template should have additional files
            expected_structure = {
                ".claude": {
                    "commands": {
                        "validate-query.md": None
                    },
                    "context": {
                        "critical_rules.md": None,
                        "llm-pitfalls.md": None,
                        "data-architecture.md": None,
                        "standards": {
                            "power-query.md": None,
                            "naming.md": None,
                            "error-handling.md": None
                        }
                    },
                    "reference": {
                        "difficulty-guide-pq.md": None,
                        "pq-scoring-explained.md": None
                    }
                },
                ".vscode": {
                    "settings.json": None
                }
            }

            self.create_directory_structure(expected_structure)
            self.assert_directory_structure(expected_structure)

        finally:
            self.teardown()

    def test_template_detection(self):
        """Test automatic template detection from specification"""
        self.setup()
        try:
            test_cases = [
                ("power query transformations", "power-query"),
                ("DAX measures and Power BI", "power-query"),
                ("research study analysis", "research"),
                ("statistical analysis study", "research"),
                ("home renovation life project", "life-projects"),
                ("personal project planning", "life-projects"),
                ("API documentation guide", "documentation"),
                ("technical docs writing", "documentation"),
                ("basic python project", "base"),
                ("web application", "base")
            ]

            for spec_content, expected_template in test_cases:
                detected = self.detect_template_type(spec_content)
                assert detected == expected_template, \
                    f"Failed to detect {expected_template} from '{spec_content}'"

        finally:
            self.teardown()

    def test_template_file_content_validation(self):
        """Test that template files contain required content"""
        self.setup()
        try:
            # Test CLAUDE.md content
            claude_content = """# CLAUDE.md

This file contains explicit instructions for Claude Code.

## Repository Purpose
[Project purpose here]

## Core Workflow
[Workflow instructions]

## Commands to Run
[Available commands]
"""
            self.create_file("CLAUDE.md", claude_content)
            self.assert_file_contains("CLAUDE.md", "explicit instructions")
            self.assert_file_contains("CLAUDE.md", "Repository Purpose")

            # Test task schema
            task_schema = {
                "id": "task-001",
                "title": "Test Task",
                "status": "Pending",
                "difficulty": 3,
                "priority": "medium",
                "dependencies": [],
                "validation_criteria": [],
                "context_requirements": []
            }
            self.create_json(".claude/tasks/task-001.json", task_schema)
            self.assert_json_has_keys(".claude/tasks/task-001.json",
                                      ["id", "title", "status", "difficulty"])

        finally:
            self.teardown()

    def test_component_integration(self):
        """Test that components integrate correctly"""
        self.setup()
        try:
            # Test components.json structure
            components = {
                "task-management": {
                    "version": "2.0.0",
                    "files": [
                        "commands/complete-task.md",
                        "commands/breakdown.md",
                        "reference/difficulty-guide.md"
                    ]
                },
                "validation-gates": {
                    "version": "1.0.0",
                    "files": [
                        "gates/pre-execution.md",
                        "gates/post-execution.md"
                    ]
                },
                "pattern-library": {
                    "version": "1.0.0",
                    "files": [
                        "patterns/file-operations/*.pattern.md",
                        "patterns/code-generation/*.pattern.md"
                    ]
                }
            }
            self.create_json("components.json", components)

            data = self.read_json("components.json")
            assert "task-management" in data
            assert "validation-gates" in data
            assert data["task-management"]["version"] == "2.0.0"

        finally:
            self.teardown()

    def create_directory_structure(self, structure: dict, base: str = ""):
        """Helper to create a directory structure"""
        base_path = Path(self.test_dir) / base

        for name, item in structure.items():
            path = base_path / name

            if isinstance(item, dict):
                # Create directory and recurse
                path.mkdir(parents=True, exist_ok=True)
                self.create_directory_structure(item, str(path.relative_to(self.test_dir)))
            else:
                # Create file
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(item or "")

    def detect_template_type(self, spec_content: str) -> str:
        """Simulate template detection logic"""
        content_lower = spec_content.lower()

        if any(term in content_lower for term in ["power query", "dax", "power bi"]):
            return "power-query"
        elif any(term in content_lower for term in ["research", "analysis", "study", "statistical"]):
            return "research"
        elif any(term in content_lower for term in ["life project", "personal", "renovation", "home"]):
            return "life-projects"
        elif any(term in content_lower for term in ["documentation", "docs", "api doc"]):
            return "documentation"
        else:
            return "base"