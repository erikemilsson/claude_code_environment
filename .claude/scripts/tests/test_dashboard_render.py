"""Tests for dashboard-render.py (Family C PoC).

The load-bearing test is byte-identical re-rendering (the PoC acceptance
gate from scripts-candidates.md § Family C). Rule tests pin the Section
Display Rules the script mirrors from dashboard-regeneration.md.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "dashboard-render.py"
spec = importlib.util.spec_from_file_location("dashboard_render", SCRIPT)
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)


def write_tasks(dirpath, tasks):
    for t in tasks:
        (dirpath / f"task-{t['id']}.json").write_text(json.dumps(t), encoding="utf-8")


def task(id, status="Pending", phase="1", **kw):
    base = {"id": str(id), "title": f"Task {id}", "status": status,
            "difficulty": 3, "owner": "claude", "dependencies": [], "phase": str(phase)}
    base.update(kw)
    return base


class TestDeterminism(unittest.TestCase):
    def test_byte_identical_rerender(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            write_tasks(d, [
                task(1, "Finished", "1", phase_name="Planning"),
                task(2, "Finished", "1", phase_name="Planning"),
                task(3, "In Progress", "2", phase_name="Build", dependencies=["1"]),
                task(4, "Pending", "2", phase_name="Build", owner="human",
                     decision_dependencies=["DEC-002"]),
                task("4_1", "Pending", "2", phase_name="Build"),
            ])
            first = dr.render_tasks_section(dr.load_tasks(d))
            second = dr.render_tasks_section(dr.load_tasks(d))
            self.assertEqual(first.encode(), second.encode())

    def test_order_independent_of_file_mtime(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            tasks = [task(i, phase="1") for i in (3, 1, 10, 2)]
            write_tasks(Path(a), tasks)
            write_tasks(Path(b), list(reversed(tasks)))
            self.assertEqual(dr.render_tasks_section(dr.load_tasks(Path(a))),
                             dr.render_tasks_section(dr.load_tasks(Path(b))))


class TestDisplayRules(unittest.TestCase):
    def render(self, tasks):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            write_tasks(d, tasks)
            return dr.render_tasks_section(dr.load_tasks(d))

    def test_completed_phase_collapses(self):
        out = self.render([task(1, "Finished"), task(2, "Finished"),
                           task(3, "Absorbed", absorbed_into="1")])
        self.assertIn("✅ 2 tasks finished", out)
        self.assertNotIn("| 1 |", out)  # no individual rows

    def test_finished_summarization_over_10(self):
        tasks = [task(i, "Finished", "1") for i in range(1, 12)]
        tasks.append(task(20, "Pending", "1"))
        out = self.render(tasks)
        self.assertIn("✅ 11 tasks finished", out)
        self.assertIn("| 20 |", out)
        self.assertNotIn("| 5 |", out)  # finished rows summarized away

    def test_blocked_phase_collapses(self):
        tasks = [task(i, "Blocked", "2", dependencies=["99"]) for i in range(1, 8)]
        out = self.render(tasks)
        self.assertIn("⏳ 7 tasks awaiting upstream", out)
        self.assertIn("blocked by task-99", out)

    def test_small_blocked_phase_stays_tabular(self):
        tasks = [task(i, "Blocked", "2") for i in range(1, 4)]  # 3 <= 5
        out = self.render(tasks)
        self.assertIn("| 1 |", out)

    def test_status_displays(self):
        out = self.render([
            task(1, "On Hold"),
            task(2, "Absorbed", absorbed_into="1"),
            task(3, "Finished", verification_history=[{}, {}, {}]),
            task(4, "Pending", conflict_note="9"),
            task(5, "Pending", out_of_spec=True),
            task(6, "Pending", cross_phase=True),
        ])
        self.assertIn("⏸️ On Hold", out)
        self.assertIn("Absorbed → Task 1", out)
        self.assertIn("Finished (2 retries)", out)
        self.assertIn("Pending (held: conflict with Task 9)", out)
        self.assertIn("⚠️ Task 5", out)
        self.assertIn("Task 6 (cross-phase)", out)

    def test_counts_exclude_absorbed_include_on_hold(self):
        out = self.render([
            task(1, "Finished"), task(2, "On Hold"),
            task(3, "Absorbed", absorbed_into="1"),
        ])
        self.assertIn("*Phase 1: 1/2 complete (50%)", out)
        self.assertIn("*1/2 tasks complete (50%)*", out)

    def test_deps_column_merges_decision_deps(self):
        out = self.render([task(1, dependencies=["9"], decision_dependencies=["DEC-002"])])
        self.assertIn("| 9, DEC-002 |", out)

    def test_phase_naming_and_subtask_sort(self):
        out = self.render([
            task("2_1", "Pending", "1", phase_name="Core"),
            task(2, "Pending", "1", phase_name="Core"),
            task(10, "Pending", "1", phase_name="Core"),
        ])
        self.assertIn("### Phase 1 — Core", out)
        rows = [l for l in out.splitlines() if l.startswith("| ")]
        ids = [r.split("|")[1].strip() for r in rows[1:]]
        self.assertEqual(ids, ["2", "2_1", "10"])

    def test_empty_dir(self):
        out = self.render([])
        self.assertIn("## 📋 Tasks", out)
        self.assertIn("*0/0 tasks complete (0%)*", out)


class TestCli(unittest.TestCase):
    def test_requires_mode_flag(self):
        self.assertEqual(dr.main([]), 2)

    def test_missing_dir(self):
        self.assertEqual(dr.main(["--tasks-section", "--tasks-dir", "/nonexistent-xyz"]), 2)


if __name__ == "__main__":
    unittest.main()
