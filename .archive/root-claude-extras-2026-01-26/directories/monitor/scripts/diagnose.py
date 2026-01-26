#!/usr/bin/env python3
"""
Self-Diagnosis Engine for Real-Time Observability Layer
Automatically analyzes failures and identifies root causes
"""

import json
import os
import re
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter

class DiagnosisEngine:
    """Automated diagnosis and root cause analysis"""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.patterns = self.load_patterns()
        self.history = self.load_history()
        self.diagnosis_results = []

    def load_patterns(self) -> Dict[str, Any]:
        """Load diagnosis patterns"""
        patterns_path = self.base_path / "config" / "patterns.json"

        default_patterns = {
            "file_not_found": {
                "indicators": ["FileNotFoundError", "ENOENT", "No such file", "cannot find"],
                "root_causes": [
                    "File or directory does not exist",
                    "Incorrect path specified",
                    "Permission denied",
                    "File deleted or moved"
                ],
                "solutions": [
                    "Verify file exists at specified path",
                    "Check path spelling and case sensitivity",
                    "Ensure proper permissions",
                    "Create missing directories/files"
                ],
                "confidence": 0.9
            },
            "status_transition": {
                "indicators": ["status", "transition", "Invalid status", "AssertionError.*status"],
                "root_causes": [
                    "Invalid status transition attempted",
                    "Status not updated after operation",
                    "Race condition in status update",
                    "Missing status validation"
                ],
                "solutions": [
                    "Refresh task data after operations",
                    "Add status transition validation",
                    "Implement status guard clauses",
                    "Add retry logic for status checks"
                ],
                "confidence": 0.85
            },
            "assertion_error": {
                "indicators": ["AssertionError", "assert.*==", "Expected.*got"],
                "root_causes": [
                    "Test assertion failed",
                    "Unexpected value returned",
                    "Timing issue in test",
                    "Mock data mismatch"
                ],
                "solutions": [
                    "Update test expectations",
                    "Add data refresh before assertion",
                    "Implement retry logic",
                    "Fix mock data generation"
                ],
                "confidence": 0.8
            },
            "import_error": {
                "indicators": ["ImportError", "ModuleNotFoundError", "No module named"],
                "root_causes": [
                    "Missing dependency",
                    "Incorrect import path",
                    "Virtual environment issue",
                    "Package not installed"
                ],
                "solutions": [
                    "Install missing package",
                    "Fix import statement",
                    "Activate correct virtual environment",
                    "Update requirements.txt"
                ],
                "confidence": 0.95
            },
            "timeout": {
                "indicators": ["timeout", "timed out", "deadline exceeded"],
                "root_causes": [
                    "Operation taking too long",
                    "Deadlock condition",
                    "Resource unavailable",
                    "Network latency"
                ],
                "solutions": [
                    "Increase timeout value",
                    "Optimize slow operations",
                    "Add async/parallel processing",
                    "Check resource availability"
                ],
                "confidence": 0.75
            },
            "memory_error": {
                "indicators": ["MemoryError", "out of memory", "memory allocation failed"],
                "root_causes": [
                    "Insufficient memory",
                    "Memory leak",
                    "Large data structure",
                    "Infinite recursion"
                ],
                "solutions": [
                    "Increase memory allocation",
                    "Fix memory leaks",
                    "Process data in chunks",
                    "Add recursion depth limit"
                ],
                "confidence": 0.85
            },
            "permission_denied": {
                "indicators": ["Permission denied", "EACCES", "PermissionError"],
                "root_causes": [
                    "Insufficient permissions",
                    "File locked by another process",
                    "Directory read-only",
                    "User lacks privileges"
                ],
                "solutions": [
                    "Check file permissions",
                    "Run with appropriate privileges",
                    "Unlock or close file",
                    "Change directory permissions"
                ],
                "confidence": 0.9
            }
        }

        if patterns_path.exists():
            try:
                with open(patterns_path) as f:
                    loaded = json.load(f)
                    default_patterns.update(loaded)
            except:
                pass

        return default_patterns

    def load_history(self) -> List[Dict[str, Any]]:
        """Load diagnosis history"""
        history_path = self.base_path / "history" / "failures"
        history = []

        if history_path.exists():
            for file in sorted(history_path.glob("*.json"))[-100:]:  # Last 100
                try:
                    with open(file) as f:
                        history.append(json.load(f))
                except:
                    pass

        return history

    def extract_error_info(self, error_data: Any) -> Dict[str, Any]:
        """Extract error information from various formats"""
        error_info = {
            "message": "",
            "type": "",
            "traceback": "",
            "file": "",
            "line": 0,
            "function": ""
        }

        if isinstance(error_data, str):
            error_info["message"] = error_data
            # Try to extract type from message
            if "Error" in error_data:
                match = re.search(r'(\w+Error)', error_data)
                if match:
                    error_info["type"] = match.group(1)
        elif isinstance(error_data, dict):
            error_info["message"] = error_data.get("error", error_data.get("message", ""))
            error_info["type"] = error_data.get("type", "")
            error_info["traceback"] = error_data.get("traceback", "")
        elif isinstance(error_data, Exception):
            error_info["message"] = str(error_data)
            error_info["type"] = type(error_data).__name__
            error_info["traceback"] = traceback.format_exc()

        # Extract file and line from traceback
        if error_info["traceback"]:
            file_match = re.search(r'File "([^"]+)", line (\d+)', error_info["traceback"])
            if file_match:
                error_info["file"] = file_match.group(1)
                error_info["line"] = int(file_match.group(2))

            func_match = re.search(r'in (\w+)', error_info["traceback"])
            if func_match:
                error_info["function"] = func_match.group(1)

        return error_info

    def match_pattern(self, error_info: Dict[str, Any]) -> Tuple[Optional[str], float]:
        """Match error against known patterns"""
        best_match = None
        best_confidence = 0

        error_text = f"{error_info['message']} {error_info['type']} {error_info['traceback']}"

        for pattern_name, pattern in self.patterns.items():
            match_score = 0
            indicators = pattern.get("indicators", [])

            for indicator in indicators:
                if re.search(indicator, error_text, re.IGNORECASE):
                    match_score += 1

            if match_score > 0:
                confidence = (match_score / len(indicators)) * pattern.get("confidence", 0.5)
                if confidence > best_confidence:
                    best_match = pattern_name
                    best_confidence = confidence

        return best_match, best_confidence

    def find_similar_issues(self, error_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find similar issues from history"""
        similar = []

        for historical in self.history:
            similarity = self.calculate_similarity(error_info, historical)
            if similarity > 0.7:
                similar.append({
                    "issue": historical,
                    "similarity": similarity,
                    "resolution": historical.get("resolution", "Unknown")
                })

        return sorted(similar, key=lambda x: x["similarity"], reverse=True)[:3]

    def calculate_similarity(self, error1: Dict[str, Any], error2: Dict[str, Any]) -> float:
        """Calculate similarity between two errors"""
        score = 0
        total = 0

        # Compare error types
        if error1.get("type") == error2.get("type"):
            score += 3
        total += 3

        # Compare files
        if error1.get("file") == error2.get("file"):
            score += 2
        total += 2

        # Compare functions
        if error1.get("function") == error2.get("function"):
            score += 1
        total += 1

        # Compare message keywords
        words1 = set(error1.get("message", "").lower().split())
        words2 = set(error2.get("message", "").lower().split())
        if words1 and words2:
            overlap = len(words1 & words2) / len(words1 | words2)
            score += overlap * 2
        total += 2

        return score / total if total > 0 else 0

    def analyze_root_cause(self, error_info: Dict[str, Any], pattern_match: Optional[str]) -> Dict[str, Any]:
        """Perform root cause analysis"""
        analysis = {
            "pattern_match": pattern_match,
            "confidence": 0,
            "likely_causes": [],
            "evidence": [],
            "recommendations": []
        }

        if pattern_match and pattern_match in self.patterns:
            pattern = self.patterns[pattern_match]
            analysis["likely_causes"] = pattern.get("root_causes", [])
            analysis["recommendations"] = pattern.get("solutions", [])
            analysis["confidence"] = pattern.get("confidence", 0.5)

            # Add specific evidence
            if "status" in error_info["message"].lower():
                analysis["evidence"].append("Status-related error detected")
                analysis["evidence"].append("Common in test assertions")
            if "file" in error_info["message"].lower():
                analysis["evidence"].append("File operation error")
                analysis["evidence"].append("Check path handling")
            if error_info.get("line"):
                analysis["evidence"].append(f"Error at line {error_info['line']}")

        return analysis

    def generate_fix_code(self, error_info: Dict[str, Any], pattern_match: Optional[str]) -> List[Dict[str, Any]]:
        """Generate code fixes for the issue"""
        fixes = []

        if pattern_match == "status_transition":
            fixes.append({
                "title": "Add Status Refresh",
                "code": """# Refresh task data after operations
task = self.get_task(task["id"])
assert task["status"] == "Broken Down", f"Expected 'Broken Down', got '{task['status']}'" """,
                "confidence": 0.9
            })

            fixes.append({
                "title": "Add Retry Logic",
                "code": """import time

def wait_for_status(task_id, expected_status, timeout=5):
    for _ in range(timeout):
        task = self.get_task(task_id)
        if task["status"] == expected_status:
            return True
        time.sleep(1)
    return False

assert wait_for_status(task["id"], "Broken Down")""",
                "confidence": 0.85
            })

        elif pattern_match == "file_not_found":
            fixes.append({
                "title": "Add File Existence Check",
                "code": """import os

file_path = f".claude/tasks/{task_id}.json"
if not os.path.exists(file_path):
    # Handle missing file
    if expected_missing:
        raise KeyError(f"Task {task_id} not found (expected)")
    else:
        raise FileNotFoundError(f"Unexpected missing file: {file_path}")""",
                "confidence": 0.95
            })

        elif pattern_match == "assertion_error":
            fixes.append({
                "title": "Update Assertion",
                "code": """# Make assertion more flexible
assert actual_value == expected_value or similar_condition, \\
    f"Assertion failed: {actual_value} != {expected_value}" """,
                "confidence": 0.7
            })

        return fixes

    def diagnose(self, error_data: Any) -> Dict[str, Any]:
        """Perform complete diagnosis"""
        # Extract error information
        error_info = self.extract_error_info(error_data)

        # Match against patterns
        pattern_match, confidence = self.match_pattern(error_info)

        # Find similar historical issues
        similar_issues = self.find_similar_issues(error_info)

        # Analyze root cause
        root_cause_analysis = self.analyze_root_cause(error_info, pattern_match)

        # Generate fixes
        code_fixes = self.generate_fix_code(error_info, pattern_match)

        # Build diagnosis result
        diagnosis = {
            "timestamp": datetime.now().isoformat(),
            "error": error_info,
            "pattern_match": pattern_match,
            "confidence": confidence,
            "root_cause_analysis": root_cause_analysis,
            "similar_issues": similar_issues,
            "code_fixes": code_fixes,
            "preventive_measures": self.get_preventive_measures(pattern_match)
        }

        self.diagnosis_results.append(diagnosis)
        return diagnosis

    def get_preventive_measures(self, pattern_match: Optional[str]) -> List[str]:
        """Get preventive measures for pattern"""
        measures = {
            "status_transition": [
                "Implement status transition state machine",
                "Add comprehensive status validation",
                "Use atomic status updates",
                "Add status change logging"
            ],
            "file_not_found": [
                "Always verify paths before operations",
                "Use absolute paths consistently",
                "Create parent directories automatically",
                "Add path validation utility"
            ],
            "assertion_error": [
                "Make test assertions more specific",
                "Add debug output before assertions",
                "Use appropriate assertion methods",
                "Consider timing in assertions"
            ]
        }
        return measures.get(pattern_match, ["Review code for potential issues"])

    def save_diagnosis(self, diagnosis: Dict[str, Any]):
        """Save diagnosis to file"""
        output_path = self.base_path / "diagnostics.md"

        # Generate markdown report
        report = self.generate_diagnosis_report(diagnosis)

        with open(output_path, 'w') as f:
            f.write(report)

        print(f"Diagnosis saved to: {output_path}")

        # Also save to history
        history_dir = self.base_path / "history" / "failures"
        history_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = history_dir / f"diagnosis_{timestamp}.json"

        with open(history_file, 'w') as f:
            json.dump(diagnosis, f, indent=2)

    def generate_diagnosis_report(self, diagnosis: Dict[str, Any]) -> str:
        """Generate markdown diagnosis report"""
        report = f"""# 🔍 Diagnosis Report

**Generated:** {diagnosis['timestamp']}
**Confidence:** {diagnosis['confidence']*100:.0f}%
**Pattern Match:** {diagnosis.get('pattern_match', 'Unknown')}

---

## Error Details

**Type:** {diagnosis['error'].get('type', 'Unknown')}
**Message:** {diagnosis['error'].get('message', 'No message')}
**File:** {diagnosis['error'].get('file', 'Unknown')}
**Line:** {diagnosis['error'].get('line', 'Unknown')}
**Function:** {diagnosis['error'].get('function', 'Unknown')}

---

## Root Cause Analysis

**Confidence:** {diagnosis['root_cause_analysis']['confidence']*100:.0f}%

### Likely Causes:
"""

        for i, cause in enumerate(diagnosis['root_cause_analysis']['likely_causes'], 1):
            report += f"{i}. {cause}\n"

        report += "\n### Evidence:\n"
        for evidence in diagnosis['root_cause_analysis']['evidence']:
            report += f"- {evidence}\n"

        report += "\n### Recommendations:\n"
        for i, rec in enumerate(diagnosis['root_cause_analysis']['recommendations'], 1):
            report += f"{i}. {rec}\n"

        report += "\n---\n\n## Code Fixes\n\n"

        for fix in diagnosis['code_fixes']:
            report += f"### {fix['title']} (Confidence: {fix['confidence']*100:.0f}%)\n\n"
            report += f"```python\n{fix['code']}\n```\n\n"

        if diagnosis['similar_issues']:
            report += "---\n\n## Similar Historical Issues\n\n"
            for similar in diagnosis['similar_issues']:
                report += f"- **Similarity:** {similar['similarity']*100:.0f}%\n"
                report += f"  - Resolution: {similar['resolution']}\n\n"

        report += "---\n\n## Preventive Measures\n\n"
        for measure in diagnosis['preventive_measures']:
            report += f"- {measure}\n"

        return report

    def run_diagnosis_on_test_results(self):
        """Run diagnosis on test results file"""
        test_results_path = Path(__file__).parents[3] / "test" / "test_results.json"

        if test_results_path.exists():
            with open(test_results_path) as f:
                results = json.load(f)

            print(f"Analyzing {len(results['details']['failed'])} failures...")

            for failure in results['details']['failed']:
                print(f"\nDiagnosing: {failure['test']}")
                diagnosis = self.diagnose(failure)
                self.save_diagnosis(diagnosis)

            for error in results['details']['errors']:
                print(f"\nDiagnosing: {error['test']}")
                diagnosis = self.diagnose(error)
                self.save_diagnosis(diagnosis)

            return True
        return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Diagnosis Engine')
    parser.add_argument('--error', type=str,
                       help='Error message to diagnose')
    parser.add_argument('--file', type=str,
                       help='Error log file to analyze')
    parser.add_argument('--test-results', action='store_true',
                       help='Analyze test results file')
    parser.add_argument('--issue', type=str,
                       help='Specific issue ID to diagnose')
    args = parser.parse_args()

    engine = DiagnosisEngine()

    if args.test_results:
        if engine.run_diagnosis_on_test_results():
            print("\nTest results diagnosis complete!")
        else:
            print("Test results file not found.")
    elif args.error:
        diagnosis = engine.diagnose(args.error)
        engine.save_diagnosis(diagnosis)
        print(f"\nDiagnosis confidence: {diagnosis['confidence']*100:.0f}%")
        print(f"Pattern match: {diagnosis.get('pattern_match', 'Unknown')}")
    elif args.file:
        with open(args.file) as f:
            error_data = f.read()
        diagnosis = engine.diagnose(error_data)
        engine.save_diagnosis(diagnosis)
    else:
        # Run on most recent error
        print("Running diagnosis on recent issues...")
        engine.run_diagnosis_on_test_results()


if __name__ == "__main__":
    main()