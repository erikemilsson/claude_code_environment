"""Tests for dashboard-render.py --html (DEC-024).

The dashboard is a single read-only, offline, file://-openable HTML page.
These tests pin the load-bearing invariants: determinism, the META block in
<head> (freshness consumers string-parse it), the synthesis placeholders, the
inline-SVG charts, the adaptive dependency graph, and — critically — the
absence of any file://-breaking runtime dep (no type="module", no CDN
import/fetch). The only permitted external ref is the Google Fonts <link>.
"""

import importlib.util
import json
import re
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "dashboard-render.py"
spec = importlib.util.spec_from_file_location("dashboard_render", SCRIPT)
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)

NOW = datetime(2026, 6, 24, 0, 0, 0, tzinfo=timezone.utc)


def task(id, status="Pending", phase="1", **kw):
    base = {"id": str(id), "title": f"Task {id}", "status": status,
            "difficulty": 3, "owner": "claude", "dependencies": [], "phase": str(phase)}
    base.update(kw)
    return base


def decision_md(num, title, status, selected=None):
    body = f"---\nid: DEC-{num:03d}\ntitle: {title}\nstatus: {status}\ncreated: 2026-01-01\n---\n\n## Select an Option\n"
    body += f"- [x] **{selected}**\n" if selected else "- [ ] Option A\n"
    return body


class HtmlBase(unittest.TestCase):
    def make_env(self, active=(), archived=(), decisions=(), sidecar=None,
                 verification=None, spec_text="---\ntitle: Fixture Project\n---\n\n## Overview\n\nBody.\n",
                 spec_index=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        tasks = root / "tasks"
        tasks.mkdir()
        for t in active:
            (tasks / f"task-{t['id']}.json").write_text(json.dumps(t), encoding="utf-8")
        if archived:
            (tasks / "archive").mkdir()
            for t in archived:
                (tasks / "archive" / f"task-{t['id']}.json").write_text(json.dumps(t), encoding="utf-8")
        dec_dir = root / "support" / "decisions"
        dec_dir.mkdir(parents=True)
        for i, d in enumerate(decisions, start=1):
            (dec_dir / f"decision-{i:03d}-x.md").write_text(d, encoding="utf-8")
        if sidecar is not None:
            (root / "dashboard-state.json").write_text(json.dumps(sidecar), encoding="utf-8")
        if verification is not None:
            (root / "verification-result.json").write_text(json.dumps(verification), encoding="utf-8")
        (root / "spec_v1.md").write_text(spec_text, encoding="utf-8")
        if spec_index is not None:
            (root / "spec_v1.index.json").write_text(json.dumps(spec_index), encoding="utf-8")
        (root / "version.json").write_text(json.dumps({"template_version": "9.9.9"}), encoding="utf-8")
        return root

    def render(self, root):
        return dr.render_full_html(root, NOW)

    def chain(self, n):
        """n-task dependency chain → a non-degenerate graph."""
        out = [task(1, "Pending", "1")]
        for i in range(2, n + 1):
            out.append(task(i, "Pending", "1", dependencies=[str(i - 1)]))
        return out


class TestDeterminism(HtmlBase):
    def test_byte_identical_for_fixed_now(self):
        root = self.make_env(active=[task(1, "Finished", "1"), task(2, "In Progress", "1")],
                             decisions=[decision_md(1, "Pick", "approved", "A")])
        self.assertEqual(self.render(root).encode(), self.render(root).encode())

    def test_no_date_or_random_in_output(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")]))
        # the only timestamp is the fixed --now
        self.assertIn("2026-06-24T00:00:00Z", out)
        self.assertNotIn("Math.random", out)
        self.assertNotIn("Date.now", out)


class TestMetaInHead(HtmlBase):
    def head(self, out):
        return out[:out.index("</head>")]

    def test_meta_block_in_head_with_task_hash(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")]))
        head = self.head(out)
        self.assertIn("<!-- DASHBOARD META", head)
        self.assertRegex(head, r"task_hash:\s*sha256:[0-9a-f]{64}")
        self.assertIn("template_version: 9.9.9", head)

    def test_meta_task_hash_matches_canonical(self):
        active = [task(1, "Pending", "1"), task(2, "Finished", "1")]
        out = self.render(self.make_env(active=active))
        expect = dr.canonical_task_hash(active)
        self.assertIn(f"task_hash: {expect}", out)


class TestPlaceholders(HtmlBase):
    def test_action_required_placeholder_emitted(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")]))
        self.assertIn("<!-- CLAUDE: fill", out)
        self.assertIn("Needs you", out)

    def test_custom_views_placeholder_when_toggled(self):
        root = self.make_env(active=[task(1, "Pending", "1")],
                             sidecar={"section_toggles": {"custom_views": True},
                                      "custom_views_instructions": "**By owner:** group tasks"})
        out = self.render(root)
        self.assertIn("<!-- CUSTOM VIEWS INSTRUCTIONS -->", out)
        self.assertEqual(out.count("<!-- CLAUDE: fill"), 2)  # action-required + custom-views


class TestNoFileBreakers(HtmlBase):
    def test_no_module_script_no_cdn(self):
        out = self.render(self.make_env(active=self.chain(5),
                                        decisions=[decision_md(1, "Pick", "approved", "A")]))
        self.assertNotIn('type="module"', out)
        self.assertNotIn("import ", out.split("<style>")[0] + out.split("</style>")[-1])  # no JS import
        self.assertNotIn("cdn.", out)
        self.assertNotIn("fetch(", out)
        self.assertNotIn("jsdelivr", out)

    def test_only_external_ref_is_google_fonts(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")]))
        ext = set(re.findall(r'https?://[^\s"\')]+', out))
        nonfont = [u for u in ext if "fonts.googleapis" not in u and "fonts.gstatic" not in u]
        self.assertEqual(nonfont, [])

    def test_well_formed_document(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")]))
        self.assertTrue(out.startswith("<!doctype html>"))
        self.assertTrue(out.rstrip().endswith("</html>"))


class TestSvgCharts(HtmlBase):
    def test_ring_and_donut_present(self):
        out = self.render(self.make_env(active=[task(1, "Finished", "1"), task(2, "Pending", "1")]))
        self.assertIn('class="ring"', out)        # completion ring
        self.assertIn("COMPLETE", out)
        self.assertIn("<svg", out)
        self.assertIn('class="grid"', out)         # phase heatmap container
        self.assertIn('class="cell', out)

    def test_completion_ring_reflects_done_fraction(self):
        # 1 of 2 finished → 50%
        out = self.render(self.make_env(active=[task(1, "Finished", "1"), task(2, "Pending", "1")]))
        self.assertIn(">50<", out)


class TestDependencyGraph(HtmlBase):
    def test_graph_renders_with_chain(self):
        out = self.render(self.make_env(active=self.chain(5)))
        self.assertIn('class="depgraph"', out)
        self.assertIn('class="gnode', out)
        self.assertIn('class="gedge', out)
        self.assertIn("gcrit", out)  # critical-path emphasis present

    def test_graph_omitted_under_4_task_nodes(self):
        out = self.render(self.make_env(active=self.chain(3)))
        self.assertNotIn('class="depgraph"', out)

    def test_graph_omitted_when_no_edges(self):
        out = self.render(self.make_env(active=[task(i, "Pending", "1") for i in range(1, 6)]))
        self.assertNotIn('class="depgraph"', out)  # 5 disconnected nodes → degenerate

    def test_graph_omitted_on_cycle(self):
        active = [task(1, "Pending", "1", dependencies=["2"]),
                  task(2, "Pending", "1", dependencies=["1"]),
                  task(3, "Pending", "1", dependencies=["1"]),
                  task(4, "Pending", "1", dependencies=["1"])]
        out = self.render(self.make_env(active=active))
        self.assertNotIn('class="depgraph"', out)

    def test_graph_scale_reduction_over_15(self):
        # 5-chain + 14 disconnected tasks (19 > 15 nodes) → reduction keeps the
        # critical path + neighbors and omits the off-path islands, with a note.
        active = self.chain(5) + [task(100 + i, "Pending", "1") for i in range(14)]
        out = self.render(self.make_env(active=active))
        self.assertIn('class="depgraph"', out)
        self.assertIn("more tasks omitted", out)

    def test_pure_chain_over_15_renders_whole(self):
        # a pure chain has no off-path nodes — reduction omits nothing (correct)
        out = self.render(self.make_env(active=self.chain(20)))
        self.assertIn('class="depgraph"', out)
        self.assertNotIn("more tasks omitted", out)


class TestSections(HtmlBase):
    def test_decisions_card_present_and_links_out(self):
        out = self.render(self.make_env(
            active=[task(1, "Pending", "1")],
            decisions=[decision_md(1, "Pick a vendor", "approved", "Acme")]))
        self.assertIn("📋 Decisions", out)
        self.assertIn("support/decisions/decision-001-x.md", out)  # link-out
        self.assertIn("decFilter", out)  # search/filter JS retained

    def test_decisions_omitted_when_none(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")]))
        self.assertNotIn("📋 Decisions", out)

    def test_decisions_toggle_off(self):
        root = self.make_env(active=[task(1, "Pending", "1")],
                             decisions=[decision_md(1, "Q", "approved", "A")],
                             sidecar={"section_toggles": {"decisions": False}})
        self.assertNotIn("📋 Decisions", self.render(root))

    def test_spec_card_links_out_with_index_headings(self):
        out = self.render(self.make_env(
            active=[task(1, "Pending", "1")],
            spec_index={"sections": [{"heading": "## Overview"}, {"heading": "## Architecture"}]}))
        self.assertIn("📄 Specification", out)
        self.assertIn("spec_v1.md", out)
        self.assertIn("Overview", out)
        self.assertIn("Architecture", out)
        self.assertNotIn("<!-- spec body -->", out)  # headings only, no embedded spec text

    def test_notes_card_from_sidecar(self):
        out = self.render(self.make_env(active=[task(1, "Pending", "1")],
                                        sidecar={"user_notes": "**Quick Links:**\n- [spec](spec_v1.md)"}))
        self.assertIn("Quick Links", out)
        self.assertIn('href="spec_v1.md"', out)

    def test_timeline_renders_with_due_dates(self):
        out = self.render(self.make_env(active=[
            task(1, "Pending", "1", due_date="2026-01-01", owner="human"),
            task(2, "Pending", "1", due_date="2026-12-01")]))
        self.assertIn("Timeline", out)
        self.assertIn("OVERDUE", out)  # 2026-01-01 < NOW


if __name__ == "__main__":
    unittest.main()
