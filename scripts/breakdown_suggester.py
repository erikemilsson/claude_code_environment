#!/usr/bin/env python3
"""
Smart Breakdown Assistant - AI-powered task breakdown suggestions

Features:
- Analyze historical breakdown patterns
- Suggest optimal breakdown strategies
- Estimate subtask count
- Validate breakdown quality
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import sys

sys.path.insert(0, str(Path(__file__).parent))
from task_manager import TaskManager
from pattern_matcher import PatternMatcher


class BreakdownSuggester:
    """Smart assistance for task breakdowns"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.task_manager = TaskManager(base_path)
        self.pattern_matcher = PatternMatcher(base_path)
        self.patterns_dir = self.base_path / ".claude" / "analysis" / "breakdown-patterns"
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        self._analyze_historical_patterns()

    def _analyze_historical_patterns(self):
        """Analyze successful breakdown patterns from history"""
        self.historical_patterns = {
            "by_difficulty": defaultdict(list),
            "by_keywords": defaultdict(list),
            "successful_patterns": []
        }

        all_tasks = self.task_manager.get_all_task_ids()

        for task_id in all_tasks:
            task = self.task_manager.load_task(task_id)
            if task and task.subtasks:
                pattern = {
                    "parent_id": task_id,
                    "title": task.title,
                    "difficulty": task.difficulty,
                    "subtask_count": len(task.subtasks),
                    "success": task.status == "Finished"
                }

                self.historical_patterns["by_difficulty"][task.difficulty].append(pattern)

                # Extract keywords
                keywords = self._extract_keywords(task.title + " " + task.description)
                for keyword in keywords:
                    self.historical_patterns["by_keywords"][keyword].append(pattern)

                if pattern["success"]:
                    self.historical_patterns["successful_patterns"].append(pattern)

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        import re
        keywords = []

        # Common technical terms
        tech_terms = ["api", "database", "auth", "ui", "backend", "frontend",
                     "test", "deploy", "migrate", "refactor", "optimize"]

        text_lower = text.lower()
        for term in tech_terms:
            if term in text_lower:
                keywords.append(term)

        return keywords

    def analyze_similar_tasks(self, task_description: str, difficulty: int) -> List[Dict]:
        """Find similar tasks from history"""
        similar = []

        # Find by difficulty
        difficulty_matches = self.historical_patterns["by_difficulty"].get(difficulty, [])

        # Find by keywords
        keywords = self._extract_keywords(task_description)
        keyword_matches = []
        for keyword in keywords:
            keyword_matches.extend(self.historical_patterns["by_keywords"].get(keyword, []))

        # Combine and deduplicate
        all_matches = difficulty_matches + keyword_matches
        seen = set()
        for match in all_matches:
            if match["parent_id"] not in seen:
                similar.append(match)
                seen.add(match["parent_id"])

        return similar[:10]  # Return top 10

    def suggest_breakdown_strategy(self, task_id: str) -> Dict[str, Any]:
        """Suggest optimal breakdown strategy for a task"""
        task = self.task_manager.load_task(task_id)
        if not task:
            return {"error": "Task not found"}

        # Get pattern suggestions
        pattern_suggestion = self.pattern_matcher.suggest_breakdown(
            task.title + " " + task.description
        )

        # Analyze similar tasks
        similar_tasks = self.analyze_similar_tasks(task.description, task.difficulty)

        # Estimate subtask count
        estimated_count = self.estimate_subtask_count(task.difficulty, similar_tasks)

        # Generate strategy
        strategy = {
            "task_id": task_id,
            "recommended_pattern": pattern_suggestion["pattern"],
            "suggested_subtasks": pattern_suggestion["suggested_subtasks"],
            "estimated_subtask_count": estimated_count,
            "confidence": self._calculate_confidence(pattern_suggestion, similar_tasks),
            "similar_successful_patterns": []
        }

        # Add successful examples
        for similar in similar_tasks[:3]:
            if similar["success"]:
                strategy["similar_successful_patterns"].append({
                    "title": similar["title"],
                    "subtask_count": similar["subtask_count"],
                    "difficulty": similar["difficulty"]
                })

        # Adjust suggestions based on difficulty
        if task.difficulty >= 9:
            strategy["notes"] = "Very high difficulty - consider multiple breakdown levels"
            strategy["suggested_subtasks"] = self._enhance_subtasks_for_complexity(
                strategy["suggested_subtasks"]
            )
        elif task.difficulty >= 7:
            strategy["notes"] = "High difficulty - ensure clear subtask boundaries"

        return strategy

    def estimate_subtask_count(self, difficulty: int, similar_tasks: List[Dict]) -> int:
        """Estimate optimal number of subtasks"""
        # Base estimate from difficulty
        base_estimate = {
            7: 3,
            8: 5,
            9: 7,
            10: 10
        }.get(difficulty, 3)

        # Adjust based on similar tasks
        if similar_tasks:
            similar_counts = [t["subtask_count"] for t in similar_tasks if t["success"]]
            if similar_counts:
                avg_count = sum(similar_counts) / len(similar_counts)
                # Weight: 60% historical, 40% base estimate
                return int(avg_count * 0.6 + base_estimate * 0.4)

        return base_estimate

    def validate_breakdown_quality(self, parent_id: str, subtask_definitions: List[Dict]) -> Dict:
        """Validate quality of proposed breakdown"""
        validation = {
            "is_valid": True,
            "score": 100,
            "issues": [],
            "suggestions": []
        }

        parent = self.task_manager.load_task(parent_id)
        if not parent:
            return {"error": "Parent task not found"}

        # Check subtask count
        count = len(subtask_definitions)
        if count < 2:
            validation["issues"].append("Too few subtasks (minimum 2)")
            validation["score"] -= 20
        elif count > 15:
            validation["issues"].append("Too many subtasks (maximum 15 recommended)")
            validation["score"] -= 10

        # Check difficulty distribution
        difficulties = [s.get("difficulty", 5) for s in subtask_definitions]
        avg_difficulty = sum(difficulties) / len(difficulties) if difficulties else 0

        if avg_difficulty > parent.difficulty:
            validation["issues"].append("Subtasks harder than parent task")
            validation["score"] -= 30

        if max(difficulties) >= 7:
            validation["issues"].append("Subtask with high difficulty may need further breakdown")
            validation["suggestions"].append("Consider breaking down subtasks with difficulty >= 7")
            validation["score"] -= 15

        # Check for clear titles
        for subtask in subtask_definitions:
            if len(subtask.get("title", "")) < 10:
                validation["issues"].append(f"Subtask title too short: {subtask.get('title')}")
                validation["score"] -= 5

        # Check dependencies
        has_dependencies = any(s.get("dependencies") for s in subtask_definitions)
        if count > 3 and not has_dependencies:
            validation["suggestions"].append("Consider adding dependencies between subtasks")

        validation["is_valid"] = validation["score"] >= 60

        return validation

    def _calculate_confidence(self, pattern_suggestion: Dict, similar_tasks: List[Dict]) -> int:
        """Calculate confidence in breakdown suggestion"""
        confidence = 50  # Base confidence

        # Pattern matching confidence
        if pattern_suggestion.get("confidence"):
            confidence = pattern_suggestion["confidence"]

        # Boost for successful similar tasks
        successful_similar = [t for t in similar_tasks if t["success"]]
        if len(successful_similar) >= 3:
            confidence += 20
        elif len(successful_similar) >= 1:
            confidence += 10

        # Cap at 95
        return min(95, confidence)

    def _enhance_subtasks_for_complexity(self, subtasks: List[str]) -> List[str]:
        """Enhance subtask list for complex tasks"""
        enhanced = []

        for subtask in subtasks:
            enhanced.append(subtask)
            # Add validation/testing subtasks
            if "implement" in subtask.lower():
                enhanced.append(f"Test: {subtask}")
            if "design" in subtask.lower():
                enhanced.append(f"Review: {subtask}")

        # Add standard complex task subtasks
        if "Performance testing" not in " ".join(enhanced):
            enhanced.append("Performance testing and optimization")
        if "Documentation" not in " ".join(enhanced):
            enhanced.append("Complete documentation and examples")

        return enhanced

    def learn_from_breakdown(self, parent_id: str, success: bool):
        """Learn from breakdown outcome (for future ML integration)"""
        # Store outcome for pattern learning
        outcome_file = self.patterns_dir / f"outcome_{parent_id}.json"

        parent = self.task_manager.load_task(parent_id)
        if parent:
            outcome = {
                "parent_id": parent_id,
                "difficulty": parent.difficulty,
                "subtask_count": len(parent.subtasks) if parent.subtasks else 0,
                "success": success,
                "timestamp": datetime.now().isoformat()
            }

            with open(outcome_file, 'w') as f:
                json.dump(outcome, f, indent=2)


def main():
    """CLI interface"""
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Breakdown Suggester")
    parser.add_argument("command", choices=["suggest", "validate", "estimate", "analyze"],
                       help="Command to execute")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--subtasks", nargs="+", help="Subtask definitions (JSON)")
    parser.add_argument("--description", help="Task description for analysis")
    parser.add_argument("--difficulty", type=int, help="Task difficulty")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    suggester = BreakdownSuggester()

    if args.command == "suggest":
        if not args.task_id:
            print("Task ID required")
            return

        strategy = suggester.suggest_breakdown_strategy(args.task_id)

        if args.json:
            print(json.dumps(strategy, indent=2))
        else:
            print(f"Breakdown Strategy for {args.task_id}")
            print(f"Pattern: {strategy.get('recommended_pattern')}")
            print(f"Confidence: {strategy.get('confidence')}%")
            print(f"Estimated subtasks: {strategy.get('estimated_subtask_count')}")
            print("\nSuggested subtasks:")
            for i, subtask in enumerate(strategy.get('suggested_subtasks', []), 1):
                print(f"  {i}. {subtask}")

    elif args.command == "validate":
        if not args.task_id or not args.subtasks:
            print("Task ID and subtasks required")
            return

        subtask_defs = []
        for subtask_json in args.subtasks:
            try:
                subtask_defs.append(json.loads(subtask_json))
            except:
                print(f"Invalid JSON: {subtask_json}")
                return

        validation = suggester.validate_breakdown_quality(args.task_id, subtask_defs)

        if args.json:
            print(json.dumps(validation, indent=2))
        else:
            print(f"Validation Score: {validation.get('score')}/100")
            print(f"Valid: {validation.get('is_valid')}")
            if validation.get("issues"):
                print("\nIssues:")
                for issue in validation["issues"]:
                    print(f"  - {issue}")
            if validation.get("suggestions"):
                print("\nSuggestions:")
                for suggestion in validation["suggestions"]:
                    print(f"  - {suggestion}")

    elif args.command == "estimate":
        if not args.difficulty:
            print("Difficulty required")
            return

        similar_tasks = []
        if args.description:
            similar_tasks = suggester.analyze_similar_tasks(args.description, args.difficulty)

        estimate = suggester.estimate_subtask_count(args.difficulty, similar_tasks)
        print(f"Estimated subtask count: {estimate}")

    elif args.command == "analyze":
        if not args.description or not args.difficulty:
            print("Description and difficulty required")
            return

        similar = suggester.analyze_similar_tasks(args.description, args.difficulty)

        if args.json:
            print(json.dumps(similar, indent=2))
        else:
            print(f"Similar tasks found: {len(similar)}")
            for task in similar[:5]:
                print(f"\n  {task['title']}")
                print(f"    Difficulty: {task['difficulty']}")
                print(f"    Subtasks: {task['subtask_count']}")
                print(f"    Success: {task['success']}")


if __name__ == "__main__":
    main()