#!/usr/bin/env python3
"""
Pattern Analyzer for Claude Code Environment Setup Workflows

This analyzer detects patterns in:
- Template usage and selection
- Task breakdown strategies
- Project setup workflows
- Common assumption failures
- Emerging project types
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import re

class PatternAnalyzer:
    def __init__(self, project_root: str = None):
        """Initialize the pattern analyzer with project root directory."""
        self.project_root = Path(project_root or os.getcwd())
        self.claude_dir = self.project_root / ".claude"
        self.tasks_dir = self.claude_dir / "tasks"
        self.insights_dir = self.claude_dir / "insights"
        self.decisions_dir = self.claude_dir / "decisions"

        # Pattern storage
        self.template_patterns = defaultdict(list)
        self.task_patterns = defaultdict(list)
        self.assumption_patterns = defaultdict(list)
        self.workflow_patterns = defaultdict(list)

    def analyze_all(self) -> Dict[str, Any]:
        """Run all pattern analyses and return comprehensive results."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "analyses": {
                "template_usage": self.analyze_template_usage(),
                "task_breakdown": self.analyze_task_breakdown_patterns(),
                "assumption_failures": self.analyze_assumption_patterns(),
                "workflow_efficiency": self.analyze_workflow_patterns(),
                "emerging_patterns": self.detect_emerging_patterns()
            },
            "recommendations": self.generate_recommendations()
        }
        return results

    def analyze_template_usage(self) -> Dict[str, Any]:
        """Analyze template selection patterns from project history."""
        template_usage = Counter()
        confidence_by_template = defaultdict(list)
        selection_indicators = defaultdict(set)

        # Check for CLAUDE.md to determine current template
        claude_md = self.project_root / "CLAUDE.md"
        if claude_md.exists():
            content = claude_md.read_text()
            # Extract template indicators from content
            if "Power Query" in content or "Excel" in content or "DAX" in content:
                template_usage["power-query"] += 1
            elif "research" in content.lower() or "hypothesis" in content:
                template_usage["research"] += 1
            elif "life" in content or "personal" in content:
                template_usage["life-projects"] += 1
            elif "documentation" in content or "guide" in content:
                template_usage["documentation"] += 1
            else:
                template_usage["base"] += 1

        # Analyze task files for template-related patterns
        if self.tasks_dir.exists():
            for task_file in self.tasks_dir.glob("task-*.json"):
                try:
                    with open(task_file) as f:
                        task = json.load(f)

                    # Extract template-related keywords from task descriptions
                    desc = task.get("description", "").lower()
                    title = task.get("title", "").lower()

                    if any(word in desc + title for word in ["excel", "power bi", "dax", "m language"]):
                        selection_indicators["power-query"].add("Excel/Power BI keywords")
                    if any(word in desc + title for word in ["research", "analysis", "hypothesis", "findings"]):
                        selection_indicators["research"].add("Research methodology keywords")
                    if any(word in desc + title for word in ["personal", "habits", "goals", "wellness"]):
                        selection_indicators["life-projects"].add("Personal development keywords")

                    # Track confidence levels
                    if "confidence" in task:
                        if "power" in desc or "excel" in desc:
                            confidence_by_template["power-query"].append(task["confidence"])
                        elif "research" in desc:
                            confidence_by_template["research"].append(task["confidence"])

                except (json.JSONDecodeError, IOError):
                    continue

        return {
            "usage_counts": dict(template_usage),
            "average_confidence": {
                tmpl: sum(conf)/len(conf) if conf else 0
                for tmpl, conf in confidence_by_template.items()
            },
            "selection_indicators": {
                tmpl: list(indicators)
                for tmpl, indicators in selection_indicators.items()
            },
            "most_used": template_usage.most_common(1)[0] if template_usage else None
        }

    def analyze_task_breakdown_patterns(self) -> Dict[str, Any]:
        """Analyze how tasks are broken down based on difficulty."""
        breakdown_patterns = []
        difficulty_accuracy = {"overestimated": [], "underestimated": [], "accurate": []}

        if self.tasks_dir.exists():
            parent_tasks = {}
            all_tasks = {}

            # First pass: collect all tasks
            for task_file in self.tasks_dir.glob("task-*.json"):
                try:
                    with open(task_file) as f:
                        task = json.load(f)
                        all_tasks[task["id"]] = task

                        if task.get("subtasks"):
                            parent_tasks[task["id"]] = task
                except (json.JSONDecodeError, IOError):
                    continue

            # Analyze breakdown patterns
            for parent_id, parent in parent_tasks.items():
                subtask_count = len(parent.get("subtasks", []))
                parent_difficulty = parent.get("difficulty", 0)

                # Calculate average subtask difficulty
                subtask_difficulties = []
                for subtask_id in parent.get("subtasks", []):
                    if subtask_id in all_tasks:
                        subtask_difficulties.append(all_tasks[subtask_id].get("difficulty", 0))

                avg_subtask_difficulty = (
                    sum(subtask_difficulties) / len(subtask_difficulties)
                    if subtask_difficulties else 0
                )

                breakdown_patterns.append({
                    "parent_task": parent.get("title"),
                    "parent_difficulty": parent_difficulty,
                    "subtask_count": subtask_count,
                    "avg_subtask_difficulty": avg_subtask_difficulty,
                    "breakdown_ratio": subtask_count / parent_difficulty if parent_difficulty > 0 else 0
                })

                # Assess difficulty estimation accuracy
                if parent.get("status") == "Finished":
                    if avg_subtask_difficulty < parent_difficulty * 0.5:
                        difficulty_accuracy["overestimated"].append(parent_id)
                    elif avg_subtask_difficulty > parent_difficulty * 0.8:
                        difficulty_accuracy["underestimated"].append(parent_id)
                    else:
                        difficulty_accuracy["accurate"].append(parent_id)

        return {
            "breakdown_patterns": breakdown_patterns,
            "common_breakdown_sizes": Counter([p["subtask_count"] for p in breakdown_patterns]),
            "difficulty_accuracy": {
                k: len(v) for k, v in difficulty_accuracy.items()
            },
            "optimal_breakdown_ratio": 0.3 if breakdown_patterns else None  # Heuristic
        }

    def analyze_assumption_patterns(self) -> Dict[str, Any]:
        """Analyze assumption validation patterns and failures."""
        assumption_stats = {
            "total": 0,
            "validated": 0,
            "failed": 0,
            "pending": 0
        }
        failure_categories = defaultdict(list)

        if self.tasks_dir.exists():
            for task_file in self.tasks_dir.glob("task-*.json"):
                try:
                    with open(task_file) as f:
                        task = json.load(f)

                    assumptions = task.get("assumptions", [])
                    validation_status = task.get("validation_status", "pending")

                    assumption_stats["total"] += len(assumptions)

                    if validation_status == "validated":
                        assumption_stats["validated"] += len(assumptions)
                    elif validation_status == "failed":
                        assumption_stats["failed"] += len(assumptions)
                        # Categorize failure
                        for assumption in assumptions:
                            if "technology" in assumption.lower():
                                failure_categories["technology"].append(assumption)
                            elif "data" in assumption.lower():
                                failure_categories["data"].append(assumption)
                            elif "time" in assumption.lower():
                                failure_categories["time"].append(assumption)
                            else:
                                failure_categories["other"].append(assumption)
                    else:
                        assumption_stats["pending"] += len(assumptions)

                except (json.JSONDecodeError, IOError):
                    continue

        return {
            "statistics": assumption_stats,
            "failure_rate": (
                assumption_stats["failed"] / assumption_stats["total"]
                if assumption_stats["total"] > 0 else 0
            ),
            "failure_categories": dict(failure_categories),
            "validation_timing": self._analyze_validation_timing()
        }

    def analyze_workflow_patterns(self) -> Dict[str, Any]:
        """Analyze workflow efficiency patterns."""
        workflow_metrics = {
            "task_completion_times": [],
            "blocked_tasks": [],
            "momentum_phases": Counter(),
            "velocity_trends": []
        }

        if self.tasks_dir.exists():
            for task_file in self.tasks_dir.glob("task-*.json"):
                try:
                    with open(task_file) as f:
                        task = json.load(f)

                    # Analyze completion time if available
                    if task.get("created_date") and task.get("completion_date"):
                        try:
                            created = datetime.fromisoformat(task["created_date"])
                            completed = datetime.fromisoformat(task["completion_date"])
                            duration = (completed - created).days
                            workflow_metrics["task_completion_times"].append({
                                "task_id": task["id"],
                                "difficulty": task.get("difficulty", 0),
                                "duration_days": duration
                            })
                        except (ValueError, TypeError):
                            pass

                    # Track blocked tasks
                    if task.get("status") == "Blocked":
                        workflow_metrics["blocked_tasks"].append({
                            "task_id": task["id"],
                            "title": task.get("title"),
                            "blockers": task.get("blockers", [])
                        })

                    # Analyze momentum
                    if "momentum" in task:
                        phase = task["momentum"].get("phase", "pending")
                        workflow_metrics["momentum_phases"][phase] += 1

                        velocity = task["momentum"].get("velocity", 0)
                        workflow_metrics["velocity_trends"].append(velocity)

                except (json.JSONDecodeError, IOError):
                    continue

        # Calculate averages and trends
        avg_completion_time = (
            sum(t["duration_days"] for t in workflow_metrics["task_completion_times"]) /
            len(workflow_metrics["task_completion_times"])
            if workflow_metrics["task_completion_times"] else 0
        )

        avg_velocity = (
            sum(workflow_metrics["velocity_trends"]) / len(workflow_metrics["velocity_trends"])
            if workflow_metrics["velocity_trends"] else 0
        )

        return {
            "average_completion_days": avg_completion_time,
            "blocked_task_count": len(workflow_metrics["blocked_tasks"]),
            "momentum_distribution": dict(workflow_metrics["momentum_phases"]),
            "average_velocity": avg_velocity,
            "bottlenecks": self._identify_bottlenecks(workflow_metrics)
        }

    def detect_emerging_patterns(self) -> Dict[str, Any]:
        """Detect emerging patterns that might indicate new template needs."""
        emerging = {
            "keyword_clusters": defaultdict(int),
            "hybrid_patterns": [],
            "new_domains": set()
        }

        # Analyze recent tasks for emerging patterns
        if self.tasks_dir.exists():
            recent_tasks = []
            cutoff_date = datetime.now() - timedelta(days=30)

            for task_file in self.tasks_dir.glob("task-*.json"):
                try:
                    with open(task_file) as f:
                        task = json.load(f)

                    # Check if task is recent
                    if task.get("created_date"):
                        try:
                            created = datetime.fromisoformat(task["created_date"])
                            if created >= cutoff_date:
                                recent_tasks.append(task)
                        except (ValueError, TypeError):
                            pass

                except (json.JSONDecodeError, IOError):
                    continue

            # Analyze keywords in recent tasks
            for task in recent_tasks:
                desc = (task.get("description", "") + " " + task.get("title", "")).lower()

                # Look for emerging technology keywords
                tech_keywords = ["ai", "ml", "machine learning", "llm", "automation",
                               "api", "integration", "cloud", "docker", "kubernetes"]
                for keyword in tech_keywords:
                    if keyword in desc:
                        emerging["keyword_clusters"][keyword] += 1

                # Detect hybrid patterns (multiple template indicators)
                template_indicators = {
                    "power-query": ["excel", "power bi", "dax"],
                    "research": ["analysis", "hypothesis", "findings"],
                    "development": ["api", "backend", "frontend"],
                    "data": ["etl", "pipeline", "transformation"]
                }

                matched_templates = []
                for template, keywords in template_indicators.items():
                    if any(kw in desc for kw in keywords):
                        matched_templates.append(template)

                if len(matched_templates) > 1:
                    emerging["hybrid_patterns"].append({
                        "task_id": task["id"],
                        "templates": matched_templates
                    })

        # Identify truly new domains
        common_domains = {"excel", "research", "documentation", "development", "data"}
        for keyword, count in emerging["keyword_clusters"].items():
            if count >= 3 and keyword not in common_domains:
                emerging["new_domains"].add(keyword)

        return {
            "trending_keywords": dict(emerging["keyword_clusters"]),
            "hybrid_project_count": len(emerging["hybrid_patterns"]),
            "potential_new_templates": list(emerging["new_domains"]),
            "recommendation": self._recommend_new_template(emerging)
        }

    def generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on all analyses."""
        recommendations = []

        # Always include these baseline recommendations
        recommendations.append({
            "priority": "high",
            "category": "workflow",
            "recommendation": "Implement automatic pattern detection during project setup",
            "rationale": "Reduces manual template selection errors"
        })

        recommendations.append({
            "priority": "medium",
            "category": "task_management",
            "recommendation": "Use hierarchical breakdown for all tasks with difficulty >= 7",
            "rationale": "Improves task completion rates and reduces complexity"
        })

        recommendations.append({
            "priority": "medium",
            "category": "validation",
            "recommendation": "Validate assumptions early in project lifecycle",
            "rationale": "Reduces late-stage project failures"
        })

        # Add specific recommendations based on analysis
        if self.tasks_dir.exists() and len(list(self.tasks_dir.glob("task-*.json"))) > 10:
            recommendations.append({
                "priority": "low",
                "category": "optimization",
                "recommendation": "Consider creating task templates for recurring patterns",
                "rationale": f"Found {len(list(self.tasks_dir.glob('task-*.json')))} tasks that could benefit from templates"
            })

        return recommendations

    def _analyze_validation_timing(self) -> Dict[str, int]:
        """Analyze when assumptions are typically validated."""
        timing = {
            "pre_project": 0,
            "early_phase": 0,
            "mid_project": 0,
            "late_phase": 0
        }

        # This would require more detailed timestamp analysis
        # For now, return placeholder distribution
        return timing

    def _identify_bottlenecks(self, metrics: Dict) -> List[str]:
        """Identify workflow bottlenecks from metrics."""
        bottlenecks = []

        if len(metrics["blocked_tasks"]) > 3:
            bottlenecks.append(f"High number of blocked tasks ({len(metrics['blocked_tasks'])})")

        if metrics["momentum_phases"].get("stalled", 0) > metrics["momentum_phases"].get("building", 0):
            bottlenecks.append("More tasks stalled than building momentum")

        return bottlenecks

    def _recommend_new_template(self, emerging: Dict) -> str:
        """Recommend new templates based on emerging patterns."""
        if len(emerging["new_domains"]) >= 2:
            return f"Consider creating templates for: {', '.join(list(emerging['new_domains'])[:3])}"
        elif emerging["hybrid_patterns"]:
            return "Consider creating hybrid templates for multi-domain projects"
        else:
            return "No new templates needed at this time"

    def save_analysis(self, results: Dict[str, Any], output_file: str = None):
        """Save analysis results to file."""
        if output_file is None:
            output_file = self.insights_dir / f"pattern_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        else:
            output_file = Path(output_file)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        return output_file

    def update_pattern_detection_md(self, results: Dict[str, Any]):
        """Update the pattern-detection.md file with latest analysis."""
        pattern_md = self.insights_dir / "pattern-detection.md"

        if not pattern_md.exists():
            print(f"Warning: {pattern_md} not found")
            return

        # This would update specific sections of the markdown file
        # For now, we'll append a summary
        with open(pattern_md, 'a') as f:
            f.write(f"\n\n## Analysis Run: {results['timestamp']}\n")
            f.write(f"- Template usage patterns detected: {len(results['analyses']['template_usage']['usage_counts'])}\n")
            f.write(f"- Task breakdown patterns found: {len(results['analyses']['task_breakdown']['breakdown_patterns'])}\n")
            f.write(f"- Recommendations generated: {len(results['recommendations'])}\n")


def main():
    """Main entry point for pattern analyzer."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze patterns in Claude Code environment")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--update-md", action="store_true", help="Update pattern-detection.md")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    analyzer = PatternAnalyzer(args.root)

    if args.verbose:
        print(f"Analyzing patterns in: {analyzer.project_root}")

    results = analyzer.analyze_all()

    # Save results
    output_file = analyzer.save_analysis(results, args.output)
    print(f"Analysis saved to: {output_file}")

    # Update markdown if requested
    if args.update_md:
        analyzer.update_pattern_detection_md(results)
        print("Updated pattern-detection.md")

    # Print summary
    print("\n=== Pattern Analysis Summary ===")
    print(f"Templates analyzed: {len(results['analyses']['template_usage']['usage_counts'])}")
    print(f"Task patterns found: {len(results['analyses']['task_breakdown']['breakdown_patterns'])}")
    print(f"Assumption failure rate: {results['analyses']['assumption_failures']['failure_rate']:.1%}")
    print(f"Recommendations: {len(results['recommendations'])}")

    if args.verbose:
        print("\n=== Top Recommendations ===")
        for rec in results['recommendations'][:3]:
            print(f"[{rec['priority']}] {rec['recommendation']}")


if __name__ == "__main__":
    main()