#!/usr/bin/env python3
"""dashboard-render.py — Family C PoC (FB-011, v4.19.0): deterministic
renderer for the dashboard's structural "## 📋 Tasks" section.

Scope (PoC, per template-maintenance/scripts-candidates.md § Family C):
renders the Tasks-by-phase section ONLY. Synthesis sections (Action
Required, Notes) stay LLM-written. The full-port decision gates on this
PoC. Mirrors: support/reference/dashboard-regeneration.md § "Section
Display Rules" (Tasks rules) + § "Per-Section Format" (Tasks row).

Determinism contract: same task files -> byte-identical output (the PoC
acceptance gate; tested in tests/test_dashboard_render.py).

Per-phase qualifier lines are deterministic count enumerations (fixed
status order + decision blockers), a simplification of the example
dashboard's judgment-flavored phrasing. Refine at full-port time.

Usage:
  python3 .claude/scripts/dashboard-render.py --tasks-section [--tasks-dir .claude/tasks]

Read-only. Stdout: the section markdown. Stderr: diagnostics.
Exit codes: 0 success, 2 runtime/usage error.
"""

import argparse
import json
import sys
from pathlib import Path

STATUS_ORDER = ["In Progress", "Awaiting Verification", "Pending", "Blocked", "On Hold"]
ACTIONABLE = {"Pending", "In Progress", "Awaiting Verification", "On Hold"}


def numeric_key(value):
    """Numeric-aware sort key for ids/phases like '2', '2_1', '10', 'A'."""
    parts = []
    for chunk in str(value).replace("-", "_").split("_"):
        parts.append((0, int(chunk)) if chunk.isdigit() else (1, chunk))
    return parts


def load_tasks(tasks_dir: Path):
    tasks = []
    for path in sorted(tasks_dir.glob("task-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"warning: skipping unreadable {path.name}: {exc}", file=sys.stderr)
            continue
        if isinstance(data, dict) and data.get("id") is not None:
            tasks.append(data)
        else:
            print(f"warning: skipping {path.name}: no id field", file=sys.stderr)
    return tasks


def display_status(task):
    status = task.get("status", "Pending")
    if status == "On Hold":
        return "⏸️ On Hold"
    if status == "Absorbed":
        return f"Absorbed → Task {task.get('absorbed_into', '?')}"
    if status == "Finished":
        retries = max(len(task.get("verification_history", [])) - 1, 0)
        return f"Finished ({retries} retries)" if retries >= 1 else "Finished"
    if status == "Pending" and task.get("conflict_note"):
        return f"Pending (held: conflict with Task {task['conflict_note']})"
    return status


def display_title(task):
    title = task.get("title", "(untitled)")
    if task.get("out_of_spec"):
        title = f"⚠️ {title}"
    if task.get("cross_phase"):
        title = f"{title} (cross-phase)"
    return title


def display_deps(task):
    deps = [str(d) for d in task.get("dependencies", [])]
    deps += [str(d) for d in task.get("decision_dependencies", [])]
    return ", ".join(deps) if deps else "—"


def task_row(task):
    cells = [
        str(task.get("id", "?")),
        display_title(task),
        display_status(task),
        str(task.get("difficulty", "—")),
        str(task.get("owner", "claude")),
        display_deps(task),
    ]
    return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"


def phase_blockers(blocked_tasks, finished_ids, prev_phase):
    """Deterministic blocker summary: decision deps + unfinished task deps,
    sorted; fall back to the previous phase. Max 2 shown + 'and N others'."""
    blockers = set()
    for task in blocked_tasks:
        blockers.update(str(d) for d in task.get("decision_dependencies", []))
        for dep in task.get("dependencies", []):
            if str(dep) not in finished_ids:
                blockers.add(f"task-{dep}")
    ordered = sorted(blockers, key=numeric_key)
    if not ordered:
        return f"awaiting Phase {prev_phase}" if prev_phase else "awaiting upstream work"
    shown = ", ".join(f"blocked by {b}" if not b.startswith("task-") else f"blocked by {b}" for b in ordered[:2])
    if len(ordered) > 2:
        shown += f" and {len(ordered) - 2} others"
    return shown


def qualifier_line(active_tasks):
    """Fixed-order status-count enumeration for the per-phase footer."""
    counts = []
    for status in STATUS_ORDER:
        n = sum(1 for t in active_tasks if t.get("status") == status)
        if n:
            counts.append(f"{n} {status.lower()}")
    return ", ".join(counts)


def render_phase(phase_key, phase_name, tasks, finished_ids, prev_phase):
    non_absorbed = [t for t in tasks if t.get("status") != "Absorbed"]
    finished = [t for t in non_absorbed if t.get("status") == "Finished"]
    active = [t for t in non_absorbed if t.get("status") != "Finished"]
    header = f"### Phase {phase_key} — {phase_name}" if phase_name else f"### Phase {phase_key}"
    lines = [header, ""]

    # Completed phase collapsing: every non-absorbed task Finished.
    if non_absorbed and not active:
        lines.append(f"✅ {len(finished)} tasks finished")
        lines.append("")
        return lines, len(finished), len(non_absorbed)

    # Blocked phase collapsing: zero actionable, >5 non-actionable.
    non_actionable = [t for t in active if t.get("status") in {"Blocked", "Broken Down"}]
    if active and not any(t.get("status") in ACTIONABLE for t in active) and len(non_actionable) > 5:
        summary = phase_blockers(non_actionable, finished_ids, prev_phase)
        lines.append(f"⏳ {len(non_actionable)} tasks awaiting upstream — {summary}")
        lines.append("")
        return lines, len(finished), len(non_absorbed)

    lines.append("| ID | Title | Status | Diff | Owner | Deps |")
    lines.append("|----|-------|--------|------|-------|------|")
    # Completed task summarization: >10 finished in an active phase.
    rows = tasks if len(finished) <= 10 else [t for t in tasks if t.get("status") not in {"Finished"}]
    summarize_finished = len(finished) > 10
    for task in sorted(rows, key=lambda t: numeric_key(t.get("id"))):
        lines.append(task_row(task))
    lines.append("")
    if summarize_finished:
        lines.insert(2, f"✅ {len(finished)} tasks finished")
        lines.insert(3, "")
    done, total = len(finished), len(non_absorbed)
    pct = round(100 * done / total) if total else 0
    qualifier = qualifier_line(active)
    footer = f"*Phase {phase_key}: {done}/{total} complete ({pct}%)"
    footer += f" — {qualifier}*" if qualifier else "*"
    lines.append(footer)
    lines.append("")
    return lines, done, total


def render_tasks_section(tasks):
    phases = {}
    for task in tasks:
        key = str(task.get("phase", "?"))
        phases.setdefault(key, []).append(task)

    out = ["## 📋 Tasks", ""]
    total_done = total_all = 0
    ordered = sorted(phases.keys(), key=lambda k: (k == "?", numeric_key(k)))
    finished_ids = {str(t.get("id")) for t in tasks if t.get("status") == "Finished"}
    for idx, key in enumerate(ordered):
        group = phases[key]
        names = sorted({t.get("phase_name") for t in group if t.get("phase_name")})
        phase_name = names[0] if names else None
        prev_phase = ordered[idx - 1] if idx > 0 else None
        lines, done, total = render_phase(key, phase_name, group, finished_ids, prev_phase)
        out.extend(lines)
        total_done += done
        total_all += total
    pct = round(100 * total_done / total_all) if total_all else 0
    out.append(f"*{total_done}/{total_all} tasks complete ({pct}%)*")
    out.append("")
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Deterministic dashboard section renderer (Family C PoC).")
    parser.add_argument("--tasks-section", action="store_true", help="render the '## 📋 Tasks' section (only mode in the PoC)")
    parser.add_argument("--tasks-dir", default=".claude/tasks", help="task JSON directory (default: .claude/tasks; archive/ excluded)")
    args = parser.parse_args(argv)

    if not args.tasks_section:
        parser.print_usage(sys.stderr)
        print("error: --tasks-section is required (only PoC mode)", file=sys.stderr)
        return 2

    tasks_dir = Path(args.tasks_dir)
    if not tasks_dir.is_dir():
        print(f"error: tasks dir not found: {tasks_dir}", file=sys.stderr)
        return 2

    print(render_tasks_section(load_tasks(tasks_dir)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
