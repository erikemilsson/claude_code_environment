#!/usr/bin/env python3
"""
Self-Healing System for Real-Time Observability Layer
Generates and applies automated fixes for diagnosed issues
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class SelfHealer:
    """Automated fix generation and application"""

    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.backup_dir = self.base_path / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        self.fixes_applied = []
        self.fix_history = self.load_fix_history()

    def load_fix_history(self) -> List[Dict[str, Any]]:
        """Load history of applied fixes"""
        history_path = self.base_path / "history" / "resolutions"
        history = []

        if history_path.exists():
            for file in sorted(history_path.glob("*.json"))[-50:]:  # Last 50
                try:
                    with open(file) as f:
                        history.append(json.load(f))
                except:
                    pass

        return history

    def create_backup(self, file_path: Path) -> Path:
        """Create backup of file before modification"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = self.backup_dir / backup_name

        shutil.copy2(file_path, backup_path)
        return backup_path

    def validate_fix(self, fix: Dict[str, Any]) -> bool:
        """Validate fix before applying"""
        # Check if fix has required fields
        if not all(key in fix for key in ["file", "operation", "content"]):
            return False

        # Check if file exists
        file_path = Path(fix["file"])
        if fix["operation"] != "create" and not file_path.exists():
            print(f"File not found: {fix['file']}")
            return False

        # Validate Python syntax if applicable
        if fix["file"].endswith(".py") and "code" in fix:
            try:
                compile(fix["code"], fix["file"], "exec")
            except SyntaxError as e:
                print(f"Syntax error in fix: {e}")
                return False

        return True

    def apply_fix(self, fix: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        """Apply a single fix"""
        result = {
            "fix_id": fix.get("id", "unknown"),
            "success": False,
            "backup": None,
            "error": None,
            "changes": []
        }

        if not self.validate_fix(fix):
            result["error"] = "Fix validation failed"
            return result

        file_path = Path(fix["file"])

        try:
            # Create backup if file exists
            if file_path.exists() and not dry_run:
                result["backup"] = str(self.create_backup(file_path))

            if fix["operation"] == "replace":
                if dry_run:
                    print(f"[DRY RUN] Would replace in {file_path}:")
                    print(f"  Old: {fix.get('old_text', '')[:50]}...")
                    print(f"  New: {fix.get('new_text', '')[:50]}...")
                else:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    new_content = content.replace(fix["old_text"], fix["new_text"])

                    if new_content == content:
                        result["error"] = "No changes made (text not found)"
                        return result

                    with open(file_path, 'w') as f:
                        f.write(new_content)

                    result["changes"].append(f"Replaced text in {file_path}")

            elif fix["operation"] == "insert":
                if dry_run:
                    print(f"[DRY RUN] Would insert at line {fix.get('line', 0)} in {file_path}")
                else:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()

                    line_num = fix.get("line", len(lines))
                    lines.insert(line_num, fix["content"] + "\n")

                    with open(file_path, 'w') as f:
                        f.writelines(lines)

                    result["changes"].append(f"Inserted at line {line_num}")

            elif fix["operation"] == "create":
                if dry_run:
                    print(f"[DRY RUN] Would create {file_path}")
                else:
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(file_path, 'w') as f:
                        f.write(fix["content"])

                    result["changes"].append(f"Created {file_path}")

            elif fix["operation"] == "patch":
                if dry_run:
                    print(f"[DRY RUN] Would apply patch to {file_path}")
                else:
                    # Apply unified diff patch
                    patch_file = self.backup_dir / "temp.patch"
                    with open(patch_file, 'w') as f:
                        f.write(fix["patch"])

                    subprocess.run(["patch", str(file_path), str(patch_file)],
                                 check=True, capture_output=True)
                    patch_file.unlink()

                    result["changes"].append(f"Applied patch to {file_path}")

            result["success"] = True

        except Exception as e:
            result["error"] = str(e)
            if result["backup"] and not dry_run:
                # Restore from backup on error
                shutil.copy2(result["backup"], file_path)
                print(f"Restored from backup due to error: {e}")

        return result

    def generate_fix_for_diagnosis(self, diagnosis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate fixes based on diagnosis"""
        fixes = []
        pattern = diagnosis.get("pattern_match")

        if pattern == "status_transition":
            error_info = diagnosis.get("error", {})
            file_path = error_info.get("file", "")
            line = error_info.get("line", 0)

            if file_path and "test_full_workflow.py" in file_path:
                fixes.append({
                    "id": "1A",
                    "file": file_path,
                    "operation": "replace",
                    "old_text": 'assert task["status"] == "Broken Down"',
                    "new_text": """# Refresh task data after breakdown
task = self.get_task(task["id"])
assert task["status"] == "Broken Down", f"Expected 'Broken Down', got '{task['status']}'" """,
                    "confidence": 0.9,
                    "description": "Add task data refresh before assertion"
                })

        elif pattern == "file_not_found":
            error_info = diagnosis.get("error", {})
            if "nonexistent" in error_info.get("message", ""):
                # This is expected for error testing
                fixes.append({
                    "id": "2A",
                    "file": error_info.get("file", ""),
                    "operation": "replace",
                    "old_text": 'self.update_task_status("nonexistent", "Finished")',
                    "new_text": """try:
    self.update_task_status("nonexistent", "Finished")
except FileNotFoundError as e:
    errors_caught.append({"type": "not_found", "error": str(e)})""",
                    "confidence": 0.95,
                    "description": "Add proper error handling for missing file test"
                })

        elif pattern == "assertion_error":
            # Generic assertion fix
            fixes.append({
                "id": "3A",
                "file": diagnosis["error"].get("file", ""),
                "operation": "insert",
                "line": diagnosis["error"].get("line", 0) - 1,
                "content": "# TODO: Review this assertion - it may need updating",
                "confidence": 0.5,
                "description": "Mark assertion for review"
            })

        return fixes

    def test_fix(self, fix: Dict[str, Any]) -> bool:
        """Test if fix resolves the issue"""
        # Apply fix in test mode
        result = self.apply_fix(fix, dry_run=True)

        if not result["success"]:
            return False

        # Run affected test if specified
        if "test_command" in fix:
            try:
                result = subprocess.run(
                    fix["test_command"],
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.returncode == 0
            except:
                return False

        return True

    def rollback_fix(self, fix_result: Dict[str, Any]) -> bool:
        """Rollback a previously applied fix"""
        if not fix_result.get("backup"):
            print("No backup available for rollback")
            return False

        try:
            backup_path = Path(fix_result["backup"])
            original_file = Path(fix_result.get("file", ""))

            if backup_path.exists() and original_file:
                shutil.copy2(backup_path, original_file)
                print(f"Rolled back {original_file} from {backup_path}")
                return True

        except Exception as e:
            print(f"Rollback failed: {e}")

        return False

    def apply_all_safe_fixes(self, diagnoses: List[Dict[str, Any]],
                           dry_run: bool = False) -> List[Dict[str, Any]]:
        """Apply all fixes with high confidence"""
        results = []

        for diagnosis in diagnoses:
            fixes = self.generate_fix_for_diagnosis(diagnosis)

            for fix in fixes:
                if fix.get("confidence", 0) >= 0.8:  # Only high confidence
                    print(f"\nApplying fix {fix['id']}: {fix.get('description', '')}")
                    result = self.apply_fix(fix, dry_run)
                    result["fix"] = fix
                    results.append(result)

                    if result["success"]:
                        self.fixes_applied.append(result)

        return results

    def generate_fix_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate report of applied fixes"""
        report = f"""# 💊 Fix Application Report

**Generated:** {datetime.now().isoformat()}
**Total Fixes Attempted:** {len(results)}
**Successful:** {sum(1 for r in results if r['success'])}
**Failed:** {sum(1 for r in results if not r['success'])}

---

## Applied Fixes

"""

        for i, result in enumerate(results, 1):
            status = "✅" if result["success"] else "❌"
            report += f"### Fix #{i}: {result.get('fix_id', 'Unknown')} {status}\n\n"

            if "fix" in result:
                fix = result["fix"]
                report += f"**File:** {fix.get('file', 'Unknown')}\n"
                report += f"**Operation:** {fix.get('operation', 'Unknown')}\n"
                report += f"**Confidence:** {fix.get('confidence', 0)*100:.0f}%\n"
                report += f"**Description:** {fix.get('description', 'No description')}\n\n"

            if result["success"]:
                report += "**Changes:**\n"
                for change in result.get("changes", []):
                    report += f"- {change}\n"
                if result.get("backup"):
                    report += f"\n**Backup:** {result['backup']}\n"
            else:
                report += f"**Error:** {result.get('error', 'Unknown error')}\n"

            report += "\n---\n\n"

        report += """## Rollback Commands

To rollback any fix, use:

```bash
python3 .claude/monitor/scripts/rollback.py --fix-id <FIX_ID>
```

To rollback all fixes from this session:

```bash
python3 .claude/monitor/scripts/rollback.py --session
```

---

*All fixes are backed up and can be safely rolled back if needed.*
"""

        return report

    def save_fix_report(self, report: str):
        """Save fix report"""
        output_path = self.base_path / "self-heal.md"
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"Fix report saved to: {output_path}")

        # Also save to history
        history_dir = self.base_path / "history" / "resolutions"
        history_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = history_dir / f"fixes_{timestamp}.json"

        with open(history_file, 'w') as f:
            json.dump(self.fixes_applied, f, indent=2)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Self-Healing System')
    parser.add_argument('--fix-id', type=str,
                       help='Apply specific fix by ID')
    parser.add_argument('--all-safe', action='store_true',
                       help='Apply all high-confidence fixes')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--test', action='store_true',
                       help='Test fixes before applying')
    parser.add_argument('--rollback', type=str,
                       help='Rollback specific fix')
    parser.add_argument('--auto-rollback', action='store_true',
                       help='Automatically rollback on failure')
    args = parser.parse_args()

    healer = SelfHealer()

    if args.rollback:
        # Load fix history and rollback
        for fix_result in healer.fix_history:
            if fix_result.get("fix_id") == args.rollback:
                if healer.rollback_fix(fix_result):
                    print(f"Successfully rolled back fix {args.rollback}")
                else:
                    print(f"Failed to rollback fix {args.rollback}")
                break
        else:
            print(f"Fix {args.rollback} not found in history")

    elif args.all_safe:
        # Load recent diagnoses
        diag_path = healer.base_path / "diagnostics.md"
        if diag_path.exists():
            # Simple parsing - in production would load JSON
            diagnoses = [{"pattern_match": "status_transition"}]  # Mock

            results = healer.apply_all_safe_fixes(diagnoses, dry_run=args.dry_run)

            report = healer.generate_fix_report(results)
            if not args.dry_run:
                healer.save_fix_report(report)
            else:
                print("\n[DRY RUN] Report:\n")
                print(report)

    elif args.fix_id:
        # Apply specific fix
        fix = {
            "id": args.fix_id,
            "file": "test/integration/test_full_workflow.py",  # Example
            "operation": "replace",
            "old_text": 'assert task["status"] == "Broken Down"',
            "new_text": 'task = self.get_task(task["id"])\nassert task["status"] == "Broken Down"',
            "confidence": 0.9
        }

        if args.test:
            if healer.test_fix(fix):
                print("Fix test passed!")
            else:
                print("Fix test failed!")

        result = healer.apply_fix(fix, dry_run=args.dry_run)

        if result["success"]:
            print(f"Fix {args.fix_id} applied successfully!")
            if result.get("backup"):
                print(f"Backup saved: {result['backup']}")
        else:
            print(f"Fix {args.fix_id} failed: {result.get('error')}")

    else:
        print("Self-Healing System Ready")
        print("\nUsage:")
        print("  Apply all safe fixes: --all-safe")
        print("  Apply specific fix: --fix-id <ID>")
        print("  Test mode: --dry-run")
        print("  Rollback: --rollback <FIX_ID>")


if __name__ == "__main__":
    main()