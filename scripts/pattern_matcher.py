#!/usr/bin/env python3
"""
Pattern Matching Engine - Fast pattern suggestion from error catalog

Features:
- Keyword-based pattern matching
- Relevance scoring
- Error pattern suggestions
- Task decomposition patterns
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from collections import Counter
import math


class PatternMatcher:
    """Pattern matching engine for error catalog and best practices"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.patterns_dir = self.base_path / ".claude" / "reference"
        self.patterns_cache = {}
        self._load_patterns()

    def _load_patterns(self):
        """Load pattern library from markdown files"""
        self.patterns = {
            "error_patterns": [],
            "best_practices": [],
            "breakdown_patterns": []
        }

        # Load error catalog
        error_catalog = self.patterns_dir / "error-catalog.md"
        if error_catalog.exists():
            with open(error_catalog, 'r') as f:
                content = f.read()
                self.patterns["error_patterns"] = self._extract_patterns(content)

        # Load breakdown patterns
        breakdown_guide = self.patterns_dir / "breakdown-workflow.md"
        if breakdown_guide.exists():
            with open(breakdown_guide, 'r') as f:
                content = f.read()
                self.patterns["breakdown_patterns"] = self._extract_breakdown_patterns(content)

    def _extract_patterns(self, content: str) -> List[Dict]:
        """Extract patterns from markdown content"""
        patterns = []
        current_pattern = None
        lines = content.split("\n")

        for line in lines:
            if line.startswith("## "):
                if current_pattern:
                    patterns.append(current_pattern)
                current_pattern = {
                    "title": line[3:].strip(),
                    "keywords": [],
                    "description": "",
                    "solution": ""
                }
            elif current_pattern:
                # Extract keywords
                if "keyword" in line.lower():
                    # Extract words in quotes or after colon
                    words = re.findall(r'"([^"]+)"', line)
                    current_pattern["keywords"].extend(words)
                elif line.strip() and not line.startswith("#"):
                    if "solution" in line.lower():
                        current_pattern["solution"] += line + "\n"
                    else:
                        current_pattern["description"] += line + "\n"

        if current_pattern:
            patterns.append(current_pattern)

        return patterns

    def _extract_breakdown_patterns(self, content: str) -> List[Dict]:
        """Extract task breakdown patterns"""
        patterns = []

        # Common breakdown patterns
        patterns.extend([
            {
                "title": "API Development",
                "keywords": ["api", "endpoint", "rest", "graphql"],
                "subtask_suggestions": [
                    "Design API schema",
                    "Implement endpoints",
                    "Add validation",
                    "Write tests",
                    "Add documentation"
                ]
            },
            {
                "title": "Database Migration",
                "keywords": ["database", "migration", "schema", "sql"],
                "subtask_suggestions": [
                    "Design schema changes",
                    "Create migration scripts",
                    "Test rollback procedures",
                    "Update ORM models",
                    "Verify data integrity"
                ]
            },
            {
                "title": "Authentication System",
                "keywords": ["auth", "login", "security", "oauth"],
                "subtask_suggestions": [
                    "Design auth flow",
                    "Implement user model",
                    "Add password hashing",
                    "Create login/logout endpoints",
                    "Add session management",
                    "Implement authorization"
                ]
            },
            {
                "title": "UI Component",
                "keywords": ["ui", "component", "frontend", "react", "vue"],
                "subtask_suggestions": [
                    "Design component API",
                    "Implement base functionality",
                    "Add styling",
                    "Handle edge cases",
                    "Write unit tests",
                    "Add documentation"
                ]
            }
        ])

        return patterns

    def match_patterns(self, text: str, pattern_type: str = "all") -> List[Tuple[Dict, float]]:
        """
        Match text against patterns and return sorted results

        Args:
            text: Input text to match
            pattern_type: Type of patterns to search ("error_patterns", "breakdown_patterns", "all")

        Returns:
            List of (pattern, relevance_score) tuples
        """
        if pattern_type == "all":
            all_patterns = []
            for p_type in self.patterns:
                all_patterns.extend(self.patterns[p_type])
        else:
            all_patterns = self.patterns.get(pattern_type, [])

        # Tokenize input text
        text_lower = text.lower()
        text_words = re.findall(r'\w+', text_lower)
        text_word_freq = Counter(text_words)

        results = []

        for pattern in all_patterns:
            score = self._calculate_relevance_score(
                text_lower, text_words, text_word_freq, pattern
            )
            if score > 0:
                results.append((pattern, score))

        # Sort by relevance score
        results.sort(key=lambda x: x[1], reverse=True)

        return results

    def _calculate_relevance_score(self, text_lower: str, text_words: List[str],
                                  text_word_freq: Counter, pattern: Dict) -> float:
        """Calculate relevance score using TF-IDF-like approach"""
        score = 0.0

        # Keyword matching with position weight
        for keyword in pattern.get("keywords", []):
            keyword_lower = keyword.lower()
            if keyword_lower in text_lower:
                # Full phrase match gets higher score
                score += 10

                # Position weight (earlier = better)
                position = text_lower.find(keyword_lower)
                position_weight = 1.0 - (position / len(text_lower))
                score += position_weight * 2

            # Individual word matching
            keyword_words = re.findall(r'\w+', keyword_lower)
            for word in keyword_words:
                if word in text_word_freq:
                    # TF component
                    tf = text_word_freq[word] / len(text_words)
                    # Simple IDF (assuming rare words are more important)
                    idf = 1.0 if text_word_freq[word] == 1 else 0.5
                    score += tf * idf * 5

        # Title similarity
        if "title" in pattern:
            title_words = set(re.findall(r'\w+', pattern["title"].lower()))
            text_word_set = set(text_words)
            overlap = title_words & text_word_set
            if overlap:
                score += len(overlap) * 3

        return score

    def suggest_errors(self, task_description: str, limit: int = 5) -> List[Dict]:
        """Suggest potential errors based on task description"""
        matches = self.match_patterns(task_description, "error_patterns")

        suggestions = []
        for pattern, score in matches[:limit]:
            suggestions.append({
                "pattern": pattern["title"],
                "relevance": score,
                "description": pattern.get("description", "").strip()[:200],
                "solution": pattern.get("solution", "").strip()[:200]
            })

        return suggestions

    def suggest_breakdown(self, task_description: str) -> Dict[str, Any]:
        """Suggest task breakdown strategy"""
        matches = self.match_patterns(task_description, "breakdown_patterns")

        if not matches:
            # Default breakdown suggestion
            return {
                "pattern": "Generic Task Breakdown",
                "suggested_subtasks": [
                    "Analyze requirements",
                    "Design solution",
                    "Implement core functionality",
                    "Add error handling",
                    "Write tests",
                    "Document changes"
                ],
                "confidence": 30
            }

        best_match, score = matches[0]
        confidence = min(100, int(score * 10))

        return {
            "pattern": best_match["title"],
            "suggested_subtasks": best_match.get("subtask_suggestions", []),
            "confidence": confidence,
            "keywords_matched": best_match.get("keywords", [])
        }

    def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """Analyze task complexity based on patterns"""
        complexity_indicators = {
            "high": ["distributed", "architecture", "migration", "security", "performance",
                    "integration", "scalability", "concurrent", "async"],
            "medium": ["api", "database", "authentication", "validation", "refactor",
                      "optimize", "cache", "test"],
            "low": ["update", "fix", "typo", "rename", "comment", "document", "format"]
        }

        text_lower = task_description.lower()
        scores = {"high": 0, "medium": 0, "low": 0}

        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    scores[level] += 1

        # Determine complexity
        if scores["high"] > 0:
            complexity = "high"
            suggested_difficulty = 8
        elif scores["medium"] > scores["low"]:
            complexity = "medium"
            suggested_difficulty = 5
        else:
            complexity = "low"
            suggested_difficulty = 3

        return {
            "complexity": complexity,
            "suggested_difficulty": suggested_difficulty,
            "indicators_found": {
                level: count for level, count in scores.items() if count > 0
            }
        }


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Pattern Matching Engine")
    parser.add_argument("command", choices=["match", "suggest-errors", "suggest-breakdown",
                                           "analyze-complexity"],
                       help="Command to execute")
    parser.add_argument("--text", required=True, help="Text to analyze")
    parser.add_argument("--type", default="all", choices=["all", "error_patterns",
                                                          "breakdown_patterns"],
                       help="Pattern type to match")
    parser.add_argument("--limit", type=int, default=5, help="Max results to return")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    matcher = PatternMatcher()

    if args.command == "match":
        matches = matcher.match_patterns(args.text, args.type)

        if args.json:
            results = [
                {"title": p["title"], "score": score}
                for p, score in matches[:args.limit]
            ]
            print(json.dumps(results, indent=2))
        else:
            print(f"Pattern matches for: {args.text[:50]}...")
            for pattern, score in matches[:args.limit]:
                print(f"\n  {pattern['title']} (score: {score:.1f})")
                if pattern.get("keywords"):
                    print(f"    Keywords: {', '.join(pattern['keywords'][:5])}")

    elif args.command == "suggest-errors":
        suggestions = matcher.suggest_errors(args.text, args.limit)

        if args.json:
            print(json.dumps(suggestions, indent=2))
        else:
            print("Potential error patterns:")
            for s in suggestions:
                print(f"\n  {s['pattern']} (relevance: {s['relevance']:.1f})")
                print(f"    {s['description']}")

    elif args.command == "suggest-breakdown":
        suggestion = matcher.suggest_breakdown(args.text)

        if args.json:
            print(json.dumps(suggestion, indent=2))
        else:
            print(f"Suggested breakdown: {suggestion['pattern']}")
            print(f"Confidence: {suggestion['confidence']}%")
            print("\nSuggested subtasks:")
            for i, subtask in enumerate(suggestion['suggested_subtasks'], 1):
                print(f"  {i}. {subtask}")

    elif args.command == "analyze-complexity":
        analysis = matcher.analyze_task_complexity(args.text)

        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print(f"Complexity: {analysis['complexity']}")
            print(f"Suggested difficulty: {analysis['suggested_difficulty']}")
            print("Indicators found:")
            for level, count in analysis['indicators_found'].items():
                print(f"  {level}: {count}")


if __name__ == "__main__":
    main()