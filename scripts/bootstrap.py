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
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import sys


class BootstrapError(Exception):
    """Base exception for bootstrap errors"""
    pass


class SpecFileError(BootstrapError):
    """Error reading or validating spec file"""
    pass


class FileConflictError(BootstrapError):
    """Error when target files already exist"""
    pass


class FileCreationError(BootstrapError):
    """Error creating output files"""
    pass


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

    def detect_template(self, spec_content: str, spec_path: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Detect the best matching template from specification content

        Returns:
            Tuple of (template_name, detection_result) where detection_result contains:
            - scores: Dict[str, float] of template scores
            - is_ambiguous: bool if top templates are too close
            - alternatives: List of close alternatives if ambiguous
            - phase_0_required: bool if Phase 0 assessment recommended
            - explanation: str explaining the selection
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

            # Special condition checks - cap additive boosts to not override clear matches
            if "power" in spec_lower and "bi" in spec_lower:
                if template_name == "power-query":
                    # Cap boost at 50% of base keyword score or 5, whichever is smaller
                    boost = min(5, score * 0.5) if score > 0 else 5
                    score += boost

            if "research" in spec_lower and "data" in spec_lower:
                if template_name == "research":
                    boost = min(3, score * 0.3) if score > 0 else 3
                    score += boost

            scores[template_name] = score

        # Sort templates by score (highest first), excluding 'base'
        sorted_templates = sorted(
            [(name, score) for name, score in scores.items() if name != "base"],
            key=lambda x: x[1],
            reverse=True
        )

        # Build detection result
        result = {
            "scores": scores,
            "is_ambiguous": False,
            "alternatives": [],
            "phase_0_required": False,
            "explanation": ""
        }

        # Check for ambiguity: top 2 templates within 10% of each other
        if len(sorted_templates) >= 2:
            best_name, best_score = sorted_templates[0]
            second_name, second_score = sorted_templates[1]

            if best_score > 0:
                score_difference = (best_score - second_score) / best_score
                if score_difference < 0.15 and second_score >= 5:  # Within 15% is ambiguous
                    result["is_ambiguous"] = True
                    result["alternatives"] = [
                        {"template": best_name, "score": best_score},
                        {"template": second_name, "score": second_score}
                    ]
                    result["explanation"] = (
                        f"Templates '{best_name}' ({best_score:.1f}) and '{second_name}' ({second_score:.1f}) "
                        f"scored within 15% of each other. User should confirm which template to use."
                    )

        # Select template with highest score
        best_template = sorted_templates[0][0] if sorted_templates and sorted_templates[0][1] >= 5 else "base"
        best_score = scores.get(best_template, 0)

        # Low confidence handling: suggest 'base' with explanation
        if best_score < 5:
            best_template = "base"
            if sorted_templates and sorted_templates[0][1] > 0:
                closest = sorted_templates[0]
                result["explanation"] = (
                    f"No strong template match found. Best candidate was '{closest[0]}' "
                    f"with score {closest[1]:.1f} (threshold: 5.0). Using 'base' template. "
                    f"Consider providing more specific requirements for better template detection."
                )
            else:
                result["explanation"] = (
                    "No template keywords detected. Using 'base' template as default."
                )

        # Phase 0 detection: regulatory/compliance + ambiguity keywords
        phase_0_triggers = {
            "regulatory": ["compliance", "regulatory", "audit", "gdpr", "hipaa", "sox", "pci", "legal"],
            "ambiguity": ["unclear", "tbd", "to be determined", "need clarification", "requirements pending",
                         "scope undefined", "not finalized", "draft", "preliminary"]
        }

        has_regulatory = any(kw in spec_lower for kw in phase_0_triggers["regulatory"])
        has_ambiguity = any(kw in spec_lower for kw in phase_0_triggers["ambiguity"])

        if has_regulatory and has_ambiguity:
            result["phase_0_required"] = True
            result["explanation"] += (
                " Phase 0 recommended: regulatory keywords detected alongside ambiguity indicators. "
                "Clarify requirements before proceeding."
            )
        elif has_regulatory:
            # Regulatory without ambiguity: just note it
            result["explanation"] += " Note: regulatory/compliance keywords detected."
        elif has_ambiguity:
            result["phase_0_required"] = True
            result["explanation"] += (
                " Phase 0 recommended: specification contains ambiguity indicators. "
                "Consider clarifying requirements before implementation."
            )

        if not result["explanation"]:
            result["explanation"] = f"Selected '{best_template}' template with score {best_score:.1f}."

        return best_template, result

    def extract_indicators(self, spec_content: str, spec_path: Optional[str] = None) -> Dict[str, Any]:
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

        # Extract project name with fallback chain
        # 1. First try: markdown header
        for line in lines[:10]:
            if line.startswith("# "):
                indicators["project_name"] = line[2:].strip()
                break

        # 2. Fallback: filename without extension
        if not indicators["project_name"] and spec_path:
            filename = Path(spec_path).stem
            # Clean up filename: replace dashes/underscores with spaces, title case
            clean_name = filename.replace('-', ' ').replace('_', ' ')
            # Title case but preserve acronyms (all caps sequences)
            words = clean_name.split()
            processed_words = []
            for word in words:
                if word.isupper() and len(word) > 1:
                    processed_words.append(word)  # Keep acronyms as-is
                else:
                    processed_words.append(word.capitalize())
            indicators["project_name"] = ' '.join(processed_words)

        # 3. Final fallback: generic name
        if not indicators["project_name"]:
            indicators["project_name"] = "New Project"

        # Extract requirements from multiple formats
        in_requirements = False

        for line in lines:
            stripped = line.strip()

            # Check for requirements section header
            if re.match(r'^#{1,3}\s*(requirements?|objectives?|goals?|features?)', stripped, re.IGNORECASE):
                in_requirements = True
                continue

            # Exit section on next header
            if in_requirements and re.match(r'^#{1,3}\s+', stripped) and not re.match(r'^#{1,3}\s*(requirements?|objectives?|goals?|features?)', stripped, re.IGNORECASE):
                in_requirements = False
                continue

            if in_requirements:
                # Format 1: Bullet points (-, *, •)
                bullet_match = re.match(r'^[-*•]\s+(.+)$', stripped)
                if bullet_match:
                    indicators["requirements"].append(bullet_match.group(1).strip())
                    continue

                # Format 2: Numbered lists (1., 2., 1), 2), etc.)
                numbered_match = re.match(r'^(\d+)[.)]\s+(.+)$', stripped)
                if numbered_match:
                    indicators["requirements"].append(numbered_match.group(2).strip())
                    continue

                # Format 3: Nested bullets (indented)
                nested_match = re.match(r'^[\s\t]+[-*•]\s+(.+)$', line)
                if nested_match:
                    # Add as sub-requirement with indent marker
                    indicators["requirements"].append(f"  - {nested_match.group(1).strip()}")
                    continue

                # Format 4: Markdown table rows (| col1 | col2 |)
                table_match = re.match(r'^\|(.+)\|$', stripped)
                if table_match:
                    # Skip header separator rows (|---|---|)
                    if re.match(r'^[\|\s\-:]+$', stripped):
                        continue
                    cells = [c.strip() for c in table_match.group(1).split('|') if c.strip()]
                    if cells and not all(c.startswith('-') for c in cells):
                        # Skip likely header rows (common header words)
                        first_cell_lower = cells[0].lower()
                        header_words = ['id', 'req', 'requirement', 'name', 'description', 'priority', 'status', '#']
                        if not any(first_cell_lower == hw or first_cell_lower.endswith(' id') for hw in header_words):
                            # Use first non-empty cell as requirement, or second if first is an ID
                            if len(cells) > 1 and re.match(r'^[A-Z]{1,3}[-_]?\d+$', cells[0]):
                                # First cell looks like an ID (R1, REQ-01, etc.), use description
                                indicators["requirements"].append(cells[1])
                            else:
                                indicators["requirements"].append(cells[0])
                    continue

                # Format 5: Paragraphs - non-empty lines that could be requirements
                if stripped and len(stripped) > 20 and not stripped.startswith(('|', '#', '---', '```')):
                    # Only add if it looks like a requirement (has verb-like pattern)
                    if re.search(r'\b(must|should|shall|will|need|require|implement|create|build|develop|support|enable|allow|provide)\b', stripped, re.IGNORECASE):
                        indicators["requirements"].append(stripped)

        # Estimate complexity before capping
        req_count = len(indicators["requirements"])
        if req_count > 10:
            indicators["complexity"] = "high"
        elif req_count < 3:
            indicators["complexity"] = "low"

        # Cap at 10 requirements (after complexity assessment)
        indicators["requirements"] = indicators["requirements"][:10]

        # Detect technologies
        tech_keywords = ["python", "javascript", "sql", "react", "django", "flask",
                        "postgresql", "mongodb", "docker", "kubernetes", "aws", "azure"]
        for tech in tech_keywords:
            if tech in spec_content.lower():
                indicators["technologies"].append(tech)

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
            ".claude/reference/shared-definitions.md": self._get_shared_definitions(),
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

    def _resolve_spec_path(self, spec_path: str) -> Path:
        """
        Resolve and validate the specification file path.

        Handles:
        - Tilde expansion (~/path)
        - Relative paths (./spec.md, ../spec.md)
        - Paths with spaces

        Raises:
            SpecFileError: If path cannot be resolved or file is invalid
        """
        try:
            # Expand tilde and resolve relative paths
            path = Path(spec_path).expanduser().resolve()
        except (OSError, RuntimeError) as e:
            raise SpecFileError(f"Cannot resolve path '{spec_path}': {e}")

        # Validate file exists
        if not path.exists():
            raise SpecFileError(f"Specification file not found: {path}")

        # Validate it's a file, not a directory
        if not path.is_file():
            raise SpecFileError(f"Path is not a file: {path}")

        # Check file is readable
        if not os.access(path, os.R_OK):
            raise SpecFileError(f"Cannot read file (permission denied): {path}")

        # Check minimum file size (at least 100 bytes of content)
        file_size = path.stat().st_size
        if file_size < 100:
            raise SpecFileError(
                f"Specification file too small ({file_size} bytes): {path}\n"
                f"A valid specification should contain:\n"
                f"  - Project title or name\n"
                f"  - Description of what the project should do\n"
                f"  - At least a few requirements or objectives"
            )

        return path

    def _validate_spec_content(self, content: str, path: Path) -> None:
        """
        Validate that specification content is meaningful.

        Raises:
            SpecFileError: If content is too minimal or lacks substance
        """
        # Strip whitespace and normalize
        stripped = content.strip()

        # Check if mostly whitespace
        non_whitespace = re.sub(r'\s+', '', stripped)
        if len(non_whitespace) < 50:
            raise SpecFileError(
                f"Specification file has insufficient content: {path}\n"
                f"Found only {len(non_whitespace)} characters of actual text.\n"
                f"A valid specification should contain:\n"
                f"  - Project title or name\n"
                f"  - Description of what the project should do\n"
                f"  - At least a few requirements or objectives"
            )

        # Check if just headers without content
        lines = [l.strip() for l in stripped.split('\n') if l.strip()]
        header_lines = [l for l in lines if l.startswith('#')]
        content_lines = [l for l in lines if not l.startswith('#') and len(l) > 10]

        if len(header_lines) > 0 and len(content_lines) < 2:
            raise SpecFileError(
                f"Specification file contains only headers: {path}\n"
                f"Found {len(header_lines)} header(s) but only {len(content_lines)} content line(s).\n"
                f"Add descriptions under your headers explaining:\n"
                f"  - What the project should accomplish\n"
                f"  - Specific requirements or features needed"
            )

    def _check_file_conflicts(self, output_path: Path, structure: Dict[str, str],
                              force: bool = False, merge: bool = False) -> List[str]:
        """
        Check for existing files that would be overwritten.

        Args:
            output_path: Target directory
            structure: Files to be created
            force: If True, allow overwriting
            merge: If True, skip existing files

        Returns:
            List of conflicting file paths (only actual files, not directories)

        Raises:
            FileConflictError: If conflicts exist and neither force nor merge is set
        """
        conflicts = []
        critical_files = ["CLAUDE.md", ".claude/context/overview.md"]

        for file_path in structure.keys():
            full_path = output_path / file_path
            if full_path.exists():
                conflicts.append(file_path)

        # Check if .claude directory exists (informational, not counted as conflict)
        claude_dir = output_path / ".claude"
        claude_dir_exists = claude_dir.exists() and claude_dir.is_dir()

        if conflicts and not force and not merge:
            critical_conflicts = [f for f in conflicts if any(c in f for c in critical_files)]

            error_msg = f"File conflicts detected ({len(conflicts)} files would be overwritten):\n"
            for f in conflicts[:10]:  # Show first 10
                error_msg += f"  - {f}\n"
            if len(conflicts) > 10:
                error_msg += f"  ... and {len(conflicts) - 10} more\n"

            if claude_dir_exists and not any(f.startswith(".claude/") for f in conflicts):
                error_msg += f"  - .claude/ directory exists (may contain other files)\n"

            error_msg += "\nOptions:\n"
            error_msg += "  --force  : Overwrite all existing files\n"
            error_msg += "  --merge  : Keep existing files, only add new ones\n"

            if critical_conflicts:
                error_msg += "\n⚠️  Critical files would be overwritten:\n"
                for f in critical_conflicts:
                    error_msg += f"  - {f}\n"
                error_msg += "\nConsider backing up your files or using /undo-bootstrap if available."

            raise FileConflictError(error_msg)

        return conflicts

    def bootstrap_environment(self, spec_path: str, output_path: str = ".",
                              force: bool = False, merge: bool = False) -> Dict[str, Any]:
        """
        Complete environment bootstrap from specification

        Args:
            spec_path: Path to specification file (supports ~, relative paths, spaces)
            output_path: Output directory
            force: Overwrite existing files without prompting
            merge: Keep existing files, only add new ones

        Returns:
            Dictionary with bootstrap results
        """
        results = {
            "template_detected": None,
            "confidence_scores": {},
            "files_created": [],
            "files_skipped": [],
            "tasks_created": 0,
            "errors": [],
            "warnings": []
        }

        created_files = []  # Track for rollback
        created_dirs = []   # Track for rollback

        try:
            # Task 301: Resolve and validate spec path
            resolved_path = self._resolve_spec_path(spec_path)

            # Read specification with proper encoding handling
            try:
                with open(resolved_path, 'r', encoding='utf-8') as f:
                    spec_content = f.read()
            except UnicodeDecodeError as e:
                # Try with latin-1 as fallback
                try:
                    with open(resolved_path, 'r', encoding='latin-1') as f:
                        spec_content = f.read()
                    results["warnings"].append(f"File encoding issue, read as latin-1: {e}")
                except Exception:
                    raise SpecFileError(f"Cannot decode file (encoding error): {resolved_path}\n"
                                       f"Try saving the file as UTF-8.")

            # Validate spec content is meaningful (not just whitespace/headers)
            self._validate_spec_content(spec_content, resolved_path)

            # Detect template
            template_name, detection_result = self.detect_template(spec_content, str(resolved_path))
            results["template_detected"] = template_name
            results["confidence_scores"] = detection_result["scores"]
            results["is_ambiguous"] = detection_result["is_ambiguous"]
            results["alternatives"] = detection_result.get("alternatives", [])
            results["phase_0_required"] = detection_result["phase_0_required"]
            results["detection_explanation"] = detection_result["explanation"]

            # Add warnings for ambiguous or phase_0 cases
            if detection_result["is_ambiguous"]:
                results["warnings"].append(
                    f"Template selection is ambiguous: {detection_result['explanation']}"
                )
            if detection_result["phase_0_required"]:
                results["warnings"].append(
                    "Phase 0 assessment recommended before implementation."
                )

            # Extract indicators
            indicators = self.extract_indicators(spec_content, str(resolved_path))

            # Generate base structure
            structure = self.generate_base_structure(template_name)

            # Populate with spec content
            structure = self.populate_from_spec(structure, spec_content, indicators)

            # Task 303: Check for file conflicts
            output_base = Path(output_path).expanduser().resolve()
            conflicts = self._check_file_conflicts(output_base, structure, force, merge)

            if conflicts and merge:
                results["files_skipped"] = conflicts
                # Remove conflicting files from structure for merge mode
                structure = {k: v for k, v in structure.items() if k not in conflicts}

            # Create directory structure and files with per-file error handling
            for file_path, content in structure.items():
                full_path = output_base / file_path
                try:
                    # Track directories created
                    parent_dir = full_path.parent
                    if not parent_dir.exists():
                        parent_dir.mkdir(parents=True, exist_ok=True)
                        created_dirs.append(str(parent_dir))

                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    created_files.append(str(full_path))
                    results["files_created"].append(file_path)

                except PermissionError:
                    raise FileCreationError(f"Permission denied writing to: {full_path}\n"
                                           f"Check directory permissions for: {parent_dir}")
                except OSError as e:
                    if "No space left" in str(e) or e.errno == 28:
                        raise FileCreationError(f"Disk full - cannot create: {full_path}")
                    elif "Read-only file system" in str(e):
                        raise FileCreationError(f"Read-only filesystem: {full_path}")
                    else:
                        raise FileCreationError(f"OS error creating {full_path}: {e}")

            # Create initial tasks
            tasks = self.create_initial_tasks(indicators, template_name)
            tasks_dir = output_base / ".claude" / "tasks"

            try:
                if not tasks_dir.exists():
                    tasks_dir.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(str(tasks_dir))
            except PermissionError:
                raise FileCreationError(f"Permission denied creating tasks directory: {tasks_dir}")
            except OSError as e:
                raise FileCreationError(f"Cannot create tasks directory: {e}")

            for task in tasks:
                task_file = tasks_dir / f"task-{task['id']}.json"
                try:
                    with open(task_file, 'w', encoding='utf-8') as f:
                        json.dump(task, f, indent=2)
                    created_files.append(str(task_file))
                    results["tasks_created"] += 1
                except (PermissionError, OSError) as e:
                    # Non-critical: warn but continue
                    results["warnings"].append(f"Could not create task file {task_file}: {e}")

        except SpecFileError as e:
            results["errors"].append(f"Specification file error: {e}")
            # No rollback needed - we haven't created anything yet

        except FileConflictError as e:
            results["errors"].append(str(e))
            # No rollback needed - we detected conflicts before writing

        except FileCreationError as e:
            results["errors"].append(f"File creation error: {e}")
            # Rollback: clean up partially created files
            self._rollback_files(created_files, created_dirs, results)

        except Exception as e:
            results["errors"].append(f"Unexpected error: {type(e).__name__}: {e}")
            # Attempt rollback for unexpected errors too
            if created_files or created_dirs:
                self._rollback_files(created_files, created_dirs, results)

        return results

    def _rollback_files(self, created_files: List[str], created_dirs: List[str],
                        results: Dict[str, Any]) -> None:
        """
        Clean up files created during a failed bootstrap.

        Args:
            created_files: List of file paths to remove
            created_dirs: List of directory paths to remove (if empty)
            results: Results dict to update with rollback info
        """
        rolled_back = []
        rollback_errors = []

        # Remove files first
        for file_path in reversed(created_files):
            try:
                path = Path(file_path)
                if path.exists():
                    path.unlink()
                    rolled_back.append(file_path)
            except Exception as e:
                rollback_errors.append(f"Could not remove {file_path}: {e}")

        # Remove empty directories (in reverse order of creation)
        # Also try to remove parent directories if they become empty
        dirs_to_check = set(created_dirs)
        for file_path in created_files:
            # Add parent directories of files we removed
            parent = Path(file_path).parent
            while str(parent) != str(parent.parent):  # Stop at root
                dirs_to_check.add(str(parent))
                parent = parent.parent

        # Sort by depth (deepest first) to remove nested dirs before parents
        sorted_dirs = sorted(dirs_to_check, key=lambda d: d.count(os.sep), reverse=True)

        for dir_path in sorted_dirs:
            try:
                path = Path(dir_path)
                if path.exists() and path.is_dir():
                    # Only remove if empty
                    if not any(path.iterdir()):
                        path.rmdir()
                        rolled_back.append(dir_path)
            except Exception as e:
                rollback_errors.append(f"Could not remove directory {dir_path}: {e}")

        if rolled_back:
            results["warnings"].append(f"Rolled back {len(rolled_back)} files/directories due to error")
        if rollback_errors:
            results["warnings"].extend(rollback_errors)

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

    def _get_shared_definitions(self) -> str:
        """Get shared definitions for task management"""
        return """# Shared Definitions

Single source of truth for task management definitions.

## Difficulty Scale (1-10)

| Level | Category | Action |
|-------|----------|--------|
| 1-4 | Standard | Just do it |
| 5-6 | Substantial | May take multiple steps |
| 7-8 | Large scope | MUST break down first |
| 9-10 | Multi-phase | MUST break down into phases |

## Status Values

| Status | Meaning | Rules |
|--------|---------|-------|
| Pending | Not started | Ready to work on |
| In Progress | Currently working | Only ONE at a time |
| Blocked | Cannot proceed | Document blocker in notes |
| Broken Down | Split into subtasks | Work on subtasks, not this |
| Finished | Complete | Auto-set when subtasks done |

## Mandatory Rules

**ALWAYS:**
1. Break down tasks with difficulty >= 7 before starting
2. Only one task "In Progress" at a time
3. Run `/sync-tasks` after completing any task
4. Parent tasks auto-complete when all subtasks finish

**NEVER:**
- Work on "Broken Down" tasks directly
- Skip status updates
- Work on multiple tasks simultaneously
"""

    def _get_claude_md_template(self, template_name: str) -> str:
        """Get CLAUDE.md template for project"""
        return f"""# CLAUDE.md

## Project Configuration
- **Template**: {template_name}
- **Generated**: {datetime.now().strftime('%Y-%m-%d')}

## Task Management

See `.claude/reference/shared-definitions.md` for difficulty scale, status values, and rules.

**Key rule**: Break down tasks with difficulty >= 7 before starting.

## Workflow
1. Read `.claude/context/` for project understanding
2. Check `.claude/tasks/task-overview.md` for current work
3. Use validation gates before starting tasks
4. Follow breakdown rules for high-difficulty tasks

## Commands
- `/complete-task {{id}}` - Start and finish tasks
- `/breakdown {{id}}` - Split complex tasks
- `/sync-tasks` - Update task overview
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


def _read_spec_file(bootstrap: BootstrapAutomation, spec_path: str) -> Tuple[Path, str]:
    """
    Read specification file with proper error handling.

    Args:
        bootstrap: BootstrapAutomation instance for path resolution
        spec_path: Path to specification file

    Returns:
        Tuple of (resolved_path, content)

    Raises:
        SystemExit: On any error (prints message first)
    """
    try:
        resolved_path = bootstrap._resolve_spec_path(spec_path)
    except SpecFileError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        with open(resolved_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(resolved_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

    return resolved_path, content


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Bootstrap Automation - Smart template detection and environment generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bootstrap.py detect --spec ~/Documents/project-spec.md
  python bootstrap.py bootstrap --spec ./spec.md --output ./my-project
  python bootstrap.py bootstrap --spec "path/with spaces/spec.md" --force
  python bootstrap.py bootstrap --spec ~/spec.md --merge

Note: --force and --merge flags only apply to the 'bootstrap' command.
        """
    )
    parser.add_argument("command", choices=["detect", "generate", "bootstrap"],
                       help="Command to execute")
    parser.add_argument("--spec", required=True,
                       help="Specification file path (supports ~, relative paths, paths with spaces)")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--force", action="store_true",
                       help="Overwrite existing files without prompting (bootstrap only)")
    parser.add_argument("--merge", action="store_true",
                       help="Keep existing files, only add new ones (bootstrap only)")

    args = parser.parse_args()

    # Validate mutually exclusive options
    if args.force and args.merge:
        print("Error: --force and --merge cannot be used together")
        sys.exit(1)

    # Warn if flags used with wrong command
    if args.command != "bootstrap" and (args.force or args.merge):
        print(f"Warning: --force and --merge only apply to 'bootstrap' command, ignoring for '{args.command}'")

    bootstrap = BootstrapAutomation(args.output)

    if args.command == "detect":
        resolved_path, content = _read_spec_file(bootstrap, args.spec)
        template, result = bootstrap.detect_template(content, str(resolved_path))

        if args.json:
            print(json.dumps({
                "template": template,
                "scores": result["scores"],
                "is_ambiguous": result["is_ambiguous"],
                "alternatives": result.get("alternatives", []),
                "phase_0_required": result["phase_0_required"],
                "explanation": result["explanation"]
            }, indent=2))
        else:
            print(f"Detected template: {template}")
            print(f"\nExplanation: {result['explanation']}")

            if result["is_ambiguous"]:
                print("\n⚠️  AMBIGUOUS: Top templates scored similarly:")
                for alt in result["alternatives"]:
                    print(f"  - {alt['template']}: {alt['score']:.1f}")
                print("  Consider reviewing the spec or specifying template manually.")

            if result["phase_0_required"]:
                print("\n⚠️  PHASE 0 RECOMMENDED: Clarify requirements before implementation.")

            print("\nConfidence scores:")
            for tmpl, score in sorted(result["scores"].items(), key=lambda x: x[1], reverse=True):
                print(f"  {tmpl}: {score:.1f}")

    elif args.command == "generate":
        resolved_path, content = _read_spec_file(bootstrap, args.spec)
        template, _ = bootstrap.detect_template(content, str(resolved_path))
        structure = bootstrap.generate_base_structure(template)

        if args.json:
            print(json.dumps({"files": list(structure.keys())}, indent=2))
        else:
            print(f"Files to generate for {template} template:")
            for file_path in structure:
                print(f"  {file_path}")

    elif args.command == "bootstrap":
        results = bootstrap.bootstrap_environment(
            args.spec, args.output, force=args.force, merge=args.merge
        )

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            if results['errors']:
                print("Bootstrap Failed:")
                for error in results['errors']:
                    print(f"\n{error}")
                sys.exit(1)
            else:
                print("Bootstrap Successful:")
                print(f"  Template: {results['template_detected']}")
                print(f"  Files created: {len(results['files_created'])}")
                if results['files_skipped']:
                    print(f"  Files skipped (merge mode): {len(results['files_skipped'])}")
                print(f"  Tasks created: {results['tasks_created']}")
                if results['warnings']:
                    print("\nWarnings:")
                    for warning in results['warnings']:
                        print(f"  - {warning}")


if __name__ == "__main__":
    main()