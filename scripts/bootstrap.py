#!/usr/bin/env python3
"""
Bootstrap Automation - Smart template detection and environment generation

Features:
- Automatic template detection from specification content
- Pattern-based scoring algorithm
- Fast environment structure generation
- Initial task creation from requirements
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re
import shutil


class BootstrapAutomation:
    """Automated environment bootstrap with template detection"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.claude_dir = self.base_path / ".claude"

        # Template detection patterns with weights
        self.template_patterns = {
            "power-query": {
                "keywords": ["power query", "dax", "power bi", "m language", "excel", "data model"],
                "weight": 10,
                "file_patterns": [".pq", ".dax", ".pbix"],
                "requires_phase_0": True
            },
            "research": {
                "keywords": ["research", "analysis", "study", "investigation", "findings", "hypothesis"],
                "weight": 8,
                "file_patterns": [".ipynb", ".rmd"],
                "requires_gemini": True
            },
            "life-projects": {
                "keywords": ["life project", "personal", "goals", "habits", "wellness", "finance"],
                "weight": 7,
                "file_patterns": [],
                "requires_tracking": True
            },
            "documentation": {
                "keywords": ["documentation", "docs", "api", "guide", "manual", "readme"],
                "weight": 6,
                "file_patterns": [".md", ".rst", ".adoc"],
                "requires_toc": True
            },
            "data-engineering": {
                "keywords": ["etl", "pipeline", "data", "warehouse", "streaming", "kafka", "spark"],
                "weight": 9,
                "file_patterns": [".sql", ".py", ".scala"],
                "requires_orchestration": True
            },
            "bi-dashboard": {
                "keywords": ["dashboard", "visualization", "metrics", "kpi", "tableau", "looker"],
                "weight": 8,
                "file_patterns": [".twb", ".sql"],
                "requires_metrics": True
            },
            "base": {
                "keywords": [],
                "weight": 1,
                "file_patterns": [],
                "is_default": True
            }
        }

    def detect_template(self, spec_content: str, spec_path: Optional[str] = None) -> Tuple[str, Dict[str, float]]:
        """
        Detect the best matching template from specification content

        Returns:
            Tuple of (template_name, confidence_scores)
        """
        scores = {}
        spec_lower = spec_content.lower()

        for template_name, config in self.template_patterns.items():
            score = 0.0

            # Keyword matching
            for keyword in config["keywords"]:
                occurrences = spec_lower.count(keyword.lower())
                if occurrences > 0:
                    # Diminishing returns for multiple occurrences
                    score += config["weight"] * (1 + (occurrences - 1) * 0.3)

            # File pattern matching if spec_path provided
            if spec_path and config["file_patterns"]:
                for pattern in config["file_patterns"]:
                    if pattern in spec_path:
                        score += config["weight"] * 0.5

            # Special condition checks
            if "power" in spec_lower and "bi" in spec_lower:
                if template_name == "power-query":
                    score += 5

            if "research" in spec_lower and "data" in spec_lower:
                if template_name == "research":
                    score += 3

            scores[template_name] = score

        # Select template with highest score
        best_template = max(scores, key=scores.get)

        # Use base template if no significant match
        if scores[best_template] < 5:
            best_template = "base"

        return best_template, scores

    def extract_indicators(self, spec_content: str) -> Dict[str, Any]:
        """Extract project indicators from specification"""
        indicators = {
            "project_name": None,
            "description": None,
            "requirements": [],
            "technologies": [],
            "deliverables": [],
            "complexity": "medium"
        }

        lines = spec_content.split("\n")

        # Extract project name (usually in title or first header)
        for line in lines[:10]:
            if line.startswith("# "):
                indicators["project_name"] = line[2:].strip()
                break

        # Extract requirements
        in_requirements = False
        for line in lines:
            if "requirement" in line.lower() or "objective" in line.lower():
                in_requirements = True
            elif in_requirements and line.startswith("- "):
                indicators["requirements"].append(line[2:].strip())
            elif in_requirements and line.startswith("#"):
                in_requirements = False

        # Detect technologies
        tech_keywords = ["python", "javascript", "sql", "react", "django", "flask",
                        "postgresql", "mongodb", "docker", "kubernetes", "aws", "azure"]
        for tech in tech_keywords:
            if tech in spec_content.lower():
                indicators["technologies"].append(tech)

        # Estimate complexity
        if len(indicators["requirements"]) > 10:
            indicators["complexity"] = "high"
        elif len(indicators["requirements"]) < 3:
            indicators["complexity"] = "low"

        return indicators

    def generate_base_structure(self, template_name: str) -> Dict[str, str]:
        """Generate base directory structure for template"""
        structure = {
            ".claude/commands/complete-task.md": self._get_command_template("complete-task"),
            ".claude/commands/breakdown.md": self._get_command_template("breakdown"),
            ".claude/commands/sync-tasks.md": self._get_command_template("sync-tasks"),
            ".claude/context/overview.md": "# Project Overview\n\n",
            ".claude/tasks/task-overview.md": "# Task Overview\n\n*Generated by bootstrap*\n\n",
            ".claude/reference/difficulty-guide.md": self._get_difficulty_guide(),
            "CLAUDE.md": self._get_claude_md_template(template_name),
            "README.md": "# Project\n\n*Generated by bootstrap automation*\n"
        }

        # Add template-specific files
        if template_name == "power-query":
            structure[".claude/context/phase-0-checklist.md"] = self._get_phase_0_checklist()
            structure[".claude/reference/llm-pitfalls.md"] = self._get_llm_pitfalls()

        elif template_name == "research":
            structure[".claude/context/research-methodology.md"] = "# Research Methodology\n\n"
            structure[".claude/reference/gemini-integration.md"] = self._get_gemini_guide()

        elif template_name == "data-engineering":
            structure[".claude/context/pipeline-architecture.md"] = "# Pipeline Architecture\n\n"
            structure[".claude/reference/orchestration.md"] = "# Orchestration Guide\n\n"

        return structure

    def populate_from_spec(self, structure: Dict[str, str], spec_content: str,
                          indicators: Dict[str, Any]) -> Dict[str, str]:
        """Populate template files with content from specification"""

        # Update overview with project details
        if indicators["project_name"]:
            structure[".claude/context/overview.md"] = f"""# Project Overview: {indicators['project_name']}

## Description
{indicators.get('description', 'Project description to be defined')}

## Technologies
{', '.join(indicators['technologies']) if indicators['technologies'] else 'To be determined'}

## Requirements
{chr(10).join('- ' + req for req in indicators['requirements'][:5]) if indicators['requirements'] else '- To be defined'}

## Complexity
{indicators['complexity'].capitalize()}

---
*Extracted from specification*
"""

        # Update README with project name
        if indicators["project_name"]:
            structure["README.md"] = f"""# {indicators['project_name']}

## Overview
This project was bootstrapped using automated template detection.

## Setup
1. Install dependencies: `pip install -r scripts/requirements.txt`
2. Run validation: `python scripts/validation-gates.py validate-all`
3. View tasks: `python scripts/task-manager.py list`

## Technologies
{', '.join(indicators['technologies']) if indicators['technologies'] else 'To be determined'}
"""

        return structure

    def create_initial_tasks(self, indicators: Dict[str, Any], template_name: str) -> List[Dict]:
        """Create initial task breakdown from requirements"""
        tasks = []

        # Create setup task
        tasks.append({
            "id": "1",
            "title": "Initial Project Setup",
            "description": f"Set up the development environment for {indicators.get('project_name', 'the project')}",
            "difficulty": 3,
            "status": "Pending",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "updated_date": datetime.now().strftime("%Y-%m-%d"),
            "dependencies": [],
            "confidence": 80
        })

        # Create requirement-based tasks
        for i, req in enumerate(indicators["requirements"][:10], start=2):
            # Estimate difficulty based on keywords
            difficulty = 5  # default
            if any(word in req.lower() for word in ["complex", "advanced", "integrate"]):
                difficulty = 7
            elif any(word in req.lower() for word in ["simple", "basic", "update"]):
                difficulty = 3

            tasks.append({
                "id": str(i),
                "title": f"Implement: {req[:50]}..." if len(req) > 50 else f"Implement: {req}",
                "description": req,
                "difficulty": difficulty,
                "status": "Pending",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "updated_date": datetime.now().strftime("%Y-%m-%d"),
                "dependencies": ["1"],  # Depend on setup
                "confidence": 60
            })

        # Add template-specific tasks
        if template_name == "power-query" and not any("phase 0" in t["title"].lower() for t in tasks):
            tasks.insert(0, {
                "id": "0",
                "title": "Phase 0: LLM Knowledge Assessment",
                "description": "Test Claude's Power Query knowledge and identify gaps",
                "difficulty": 2,
                "status": "Pending",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "updated_date": datetime.now().strftime("%Y-%m-%d"),
                "dependencies": [],
                "confidence": 90
            })

        return tasks

    def bootstrap_environment(self, spec_path: str, output_path: str = ".") -> Dict[str, Any]:
        """
        Complete environment bootstrap from specification

        Returns:
            Dictionary with bootstrap results
        """
        results = {
            "template_detected": None,
            "confidence_scores": {},
            "files_created": [],
            "tasks_created": 0,
            "errors": []
        }

        try:
            # Read specification
            with open(spec_path, 'r') as f:
                spec_content = f.read()

            # Detect template
            template_name, scores = self.detect_template(spec_content, spec_path)
            results["template_detected"] = template_name
            results["confidence_scores"] = scores

            # Extract indicators
            indicators = self.extract_indicators(spec_content)

            # Generate base structure
            structure = self.generate_base_structure(template_name)

            # Populate with spec content
            structure = self.populate_from_spec(structure, spec_content, indicators)

            # Create directory structure and files
            output_base = Path(output_path)
            for file_path, content in structure.items():
                full_path = output_base / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
                results["files_created"].append(file_path)

            # Create initial tasks
            tasks = self.create_initial_tasks(indicators, template_name)
            tasks_dir = output_base / ".claude" / "tasks"
            tasks_dir.mkdir(parents=True, exist_ok=True)

            for task in tasks:
                task_file = tasks_dir / f"task-{task['id']}.json"
                with open(task_file, 'w') as f:
                    json.dump(task, f, indent=2)
                results["tasks_created"] += 1

        except Exception as e:
            results["errors"].append(str(e))

        return results

    def _get_command_template(self, command_name: str) -> str:
        """Get command file template"""
        templates = {
            "complete-task": """# Complete Task Command

## Purpose
Complete tasks with proper validation and status tracking.

## Usage
python scripts/task-manager.py --task-id {TASK_ID}
python scripts/validation-gates.py pre --task-id {TASK_ID}
""",
            "breakdown": """# Task Breakdown Command

## Purpose
Break down high-difficulty tasks into manageable subtasks.

## Process
1. Check task difficulty (must be >= 7)
2. Create subtask structure
3. Update parent status to "Broken Down"
""",
            "sync-tasks": """# Sync Tasks Command

## Purpose
Synchronize task-overview.md from JSON files.

## Usage
python scripts/task-manager.py sync
"""
        }
        return templates.get(command_name, "# Command Template\n\n")

    def _get_difficulty_guide(self) -> str:
        """Get difficulty scoring guide"""
        return """# Difficulty Scoring Guide

## Scale (1-10)
- **1-2**: Trivial (typos, text updates)
- **3-4**: Simple (basic CRUD, UI changes)
- **5-6**: Moderate (API integration, validation)
- **7-8**: Complex (MUST break down - architecture, migrations)
- **9-10**: Extreme (MUST break down - distributed systems)

## Breakdown Requirement
Tasks with difficulty >= 7 MUST be broken down before execution.
"""

    def _get_claude_md_template(self, template_name: str) -> str:
        """Get CLAUDE.md template for project"""
        return f"""# CLAUDE.md

## Project Configuration
- **Template**: {template_name}
- **Generated**: {datetime.now().strftime('%Y-%m-%d')}

## Workflow
1. Read `.claude/context/` for project understanding
2. Check `.claude/tasks/task-overview.md` for current work
3. Use validation gates before starting tasks
4. Follow breakdown rules for high-difficulty tasks

## Scripts Available
- `task-manager.py` - Core task operations
- `validation-gates.py` - Pre/post execution checks
- `schema-validator.py` - JSON validation and repair
- `bootstrap.py` - Environment generation
"""

    def _get_phase_0_checklist(self) -> str:
        """Get Phase 0 checklist for Power Query"""
        return """# Phase 0 Checklist - Power Query

## Knowledge Assessment
- [ ] Test basic M language syntax
- [ ] Verify DAX understanding
- [ ] Check Power BI service awareness
- [ ] Identify knowledge gaps

## Required Documentation
- [ ] Provide M language reference
- [ ] Supply DAX function guide
- [ ] Include common patterns
"""

    def _get_llm_pitfalls(self) -> str:
        """Get LLM pitfalls guide"""
        return """# LLM Pitfalls Guide

## Common Mistakes
1. Syntax confusion between languages
2. Outdated function references
3. Performance anti-patterns
4. Security vulnerabilities

## Mitigation
- Always verify syntax
- Test code before committing
- Review performance implications
"""

    def _get_gemini_guide(self) -> str:
        """Get Gemini integration guide"""
        return """# Gemini Integration Guide

## When to Use Gemini
- Current information (grounding=true)
- Domain expertise
- Image analysis
- Research tasks

## Model Selection
- `gemini-2.5-pro` - Complex analysis
- `gemini-2.5-flash` - Quick queries
"""


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Bootstrap Automation")
    parser.add_argument("command", choices=["detect", "generate", "bootstrap"],
                       help="Command to execute")
    parser.add_argument("--spec", required=True, help="Specification file path")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    bootstrap = BootstrapAutomation(args.output)

    if args.command == "detect":
        with open(args.spec, 'r') as f:
            content = f.read()

        template, scores = bootstrap.detect_template(content, args.spec)

        if args.json:
            print(json.dumps({"template": template, "scores": scores}, indent=2))
        else:
            print(f"Detected template: {template}")
            print("\nConfidence scores:")
            for tmpl, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                print(f"  {tmpl}: {score:.1f}")

    elif args.command == "generate":
        with open(args.spec, 'r') as f:
            content = f.read()

        template, _ = bootstrap.detect_template(content, args.spec)
        structure = bootstrap.generate_base_structure(template)

        if args.json:
            print(json.dumps({"files": list(structure.keys())}, indent=2))
        else:
            print(f"Files to generate for {template} template:")
            for file_path in structure:
                print(f"  {file_path}")

    elif args.command == "bootstrap":
        results = bootstrap.bootstrap_environment(args.spec, args.output)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Bootstrap Results:")
            print(f"  Template: {results['template_detected']}")
            print(f"  Files created: {len(results['files_created'])}")
            print(f"  Tasks created: {results['tasks_created']}")
            if results['errors']:
                print(f"  Errors: {results['errors']}")


if __name__ == "__main__":
    main()