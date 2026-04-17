# Plan — FB-011 Stage 2a: Families A + B extraction

**Purpose:** Create the first FB-011 scripts: `fingerprint.py` (Family A — spec/section/dashboard-rollup hashes) and `validate-tasks.py` (Family B — task JSON schema + verification debt). Wire them as advisory alternatives in reference docs. Prose procedures remain the source of truth.

**Status:** Ready to execute in fresh context
**Created:** 2026-04-17
**Source:** FB-011 feedback item + `.claude/support/workspace/scripts-candidates.md` inventory (Families A + B)
**Tracker status line to advance:** `Phase 4 — FB-011 Families A + B extracted (fingerprint.py + validate-tasks.py + advisory wiring); C/D/E remain for later stages`
**Cleanup tag:** DELETE-AFTER (added to tracker Cleanup Manifest in same commit as this plan)

---

## Scope

**New files (3):**
1. `.claude/scripts/fingerprint.py` — spec/section/dashboard-rollup hash computation
2. `.claude/scripts/validate-tasks.py` — task JSON schema validation + verification debt count
3. `.claude/scripts/README.md` — invocation contract, dependency notes, output format

**Edits (7 files):**
1. `.claude/sync-manifest.json` — add `.claude/scripts/**` to `sync` category
2. `.claude/rules/agents.md § "Tool Preferences"` — one-paragraph scripts allow-list note
3. `.claude/support/reference/drift-reconciliation.md` — advisory wiring for hash recipes
4. `.claude/support/reference/decomposition.md` — advisory wiring for fingerprint writes
5. `.claude/commands/health-check.md` Part 1 — advisory wiring for validate-tasks.py
6. `.claude/commands/work.md` Step 1b drift — advisory wiring for fingerprint.py
7. `.claude/commands/status.md` freshness check — advisory wiring for dashboard rollup

### Out of scope

- `task-schema.json` machine-readable schema (inventory open Q2 — deferred to separate decision)
- `.claude/scripts/tests/` test harness (inventory open Q6 — defer until Family C where test payoff is higher)
- Families C (dashboard regen), D (parallel-plan), E (decision finalization) — later stages
- **Mandatory** script invocation — wiring is advisory. Prose procedures stay authoritative. Downstream projects without the scripts dir keep working.
- Retirement of prose hash recipes in drift-reconciliation.md — stays as spec-of-record (script must mirror it)

---

## Decisions locked in

| # | Decision | Source |
|---|----------|--------|
| D1 | Bundle Families A + B | User (2026-04-17) |
| D2 | Python stdlib only (hashlib, json, pathlib, re, argparse, sys) — no pip deps | Default; simplifies ship/test |
| D3 | Advisory wiring, not mandatory | Default; preserves prose-as-truth; backward-compatible for downstream projects |
| D4 | Skip `task-schema.json` this commit | Inventory open Q2 — flag for follow-up |
| D5 | Skip test harness this commit | Inventory open Q6 — defer until Family C |
| D6 | Keep E candidacy in inventory but don't extract | Inventory open Q7 — re-evaluate in 30 days |
| D7 | Script normalization must match `drift-reconciliation.md` lines 70-84 exactly | **Critical — any drift defeats drift detection** |

**D7 details:** Full spec hash = `shasum -a 256 FILE | cut -d' ' -f1`. Section hash = `printf '%s' "heading + content-through-next-##"` piped through sha256. Python equivalent: hash the UTF-8 bytes of the text with NO trailing newline appended. Prefix all outputs with `sha256:`.

---

## Context to Load Before Executing

1. `.claude/support/workspace/scripts-candidates.md` — inventory full context (tiers, tradeoffs, constraints)
2. `.claude/support/reference/drift-reconciliation.md` lines 70-84 — **authoritative hash recipe**. Script must match byte-for-byte.
3. `.claude/support/reference/task-schema.md` — full task JSON field list. Required fields, enum values, boolean fields that validate-tasks.py must check.
4. `.claude/commands/status.md` line 36 — dashboard freshness hash formula: `SHA-256(sorted list of task_id + ":" + status)`.
5. `.claude/sync-manifest.json` — current shape of `sync` array (for placement of new entry).
6. `.claude/rules/agents.md` § "Tool Preferences" — current wording (for the appended scripts note).
7. `template-upgrade-2026-04.md` — File Collision Map, Cleanup Manifest (for bookkeeping).

Auto-memory: no specific entry load-bearing.

---

## Implementation Steps

### Step 1: Create `.claude/scripts/fingerprint.py`

```python
#!/usr/bin/env python3
"""Deterministic hash computation for spec drift detection and dashboard freshness.

Mirrors the recipe in .claude/support/reference/drift-reconciliation.md lines 70-84.
Any change to normalization logic here MUST be mirrored in that reference doc.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def hash_file(path: Path) -> str:
    return sha256_hex(path.read_bytes())


def hash_sections(path: Path) -> dict[str, str]:
    """Split on `## ` level headings. Each section = heading line + content until next `## ` or EOF.
    No trailing newline is added before hashing (matches `printf '%s'` behavior)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []

    def flush():
        if current_heading is not None:
            joined = "".join(current_lines).rstrip("\n")
            sections[current_heading] = sha256_hex(joined.encode("utf-8"))

    for line in lines:
        if re.match(r"^## (?!#)", line):
            flush()
            current_heading = line.rstrip("\n")
            current_lines = [line]
        elif current_heading is not None:
            current_lines.append(line)
    flush()
    return sections


def hash_dashboard_rollup(task_dir: Path) -> str:
    """SHA-256 of sorted 'task_id:status\\n' lines across task-*.json files in task_dir.
    Mirrors the formula in commands/status.md line 36."""
    entries = []
    for task_file in sorted(task_dir.glob("task-*.json")):
        try:
            data = json.loads(task_file.read_text(encoding="utf-8"))
            entries.append(f"{data['task_id']}:{data['status']}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"warning: skipping {task_file.name} ({e})", file=sys.stderr)
    entries.sort()
    joined = "\n".join(entries)
    return sha256_hex(joined.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic hashes for spec drift and dashboard freshness."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--spec", type=Path, help="Hash full spec file contents.")
    group.add_argument("--sections", type=Path, help="Hash each ## section; JSON map to stdout.")
    group.add_argument(
        "--dashboard-rollup",
        type=Path,
        help="Hash sorted task_id:status rollup (pass task dir, e.g. .claude/tasks).",
    )
    args = parser.parse_args()

    if args.spec:
        if not args.spec.is_file():
            print(f"error: not a file: {args.spec}", file=sys.stderr)
            return 2
        print(hash_file(args.spec))
    elif args.sections:
        if not args.sections.is_file():
            print(f"error: not a file: {args.sections}", file=sys.stderr)
            return 2
        print(json.dumps(hash_sections(args.sections), indent=2))
    elif args.dashboard_rollup:
        if not args.dashboard_rollup.is_dir():
            print(f"error: not a directory: {args.dashboard_rollup}", file=sys.stderr)
            return 2
        print(hash_dashboard_rollup(args.dashboard_rollup))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Make executable:** `chmod +x .claude/scripts/fingerprint.py` after write.

**Spot-check after write:**
- `./.claude/scripts/fingerprint.py --spec .claude/spec_v1.md` — should print `sha256:...` matching `shasum -a 256 .claude/spec_v1.md | cut -d' ' -f1` prefixed with `sha256:`.
- `./.claude/scripts/fingerprint.py --sections .claude/spec_v1.md` — should print a JSON map with one entry per `## ` heading in the spec.
- `./.claude/scripts/fingerprint.py --dashboard-rollup .claude/tasks` — should print a hash (template tasks dir may be empty → hash of empty string). Verify with `ls .claude/tasks/task-*.json 2>/dev/null | wc -l`.

### Step 2: Create `.claude/scripts/validate-tasks.py`

```python
#!/usr/bin/env python3
"""Task JSON schema validation + verification debt count.

Mirrors the field list in .claude/support/reference/task-schema.md.
Any schema change there MUST be mirrored here (flagged for follow-up: task-schema.json
as a single source of truth — deferred per inventory open Q2).
"""
import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = {
    "task_id", "title", "description", "status", "difficulty", "owner",
    "dependencies", "files_affected",
}

VALID_STATUSES = {
    "Pending", "In Progress", "Awaiting Verification", "Blocked",
    "On Hold", "Absorbed", "Broken Down", "Finished",
}

VALID_OWNERS = {"claude", "human", "both"}

BOOLEAN_FIELDS = {
    "cross_phase", "parallel_safe", "out_of_spec", "out_of_spec_rejected",
    "user_review_pending",
}


def validate_task(data: dict, path: Path) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")

    if "status" in data and data["status"] not in VALID_STATUSES:
        errors.append(f"invalid status: {data['status']!r}")
    if "owner" in data and data["owner"] not in VALID_OWNERS:
        errors.append(f"invalid owner: {data['owner']!r}")
    if "difficulty" in data:
        d = data["difficulty"]
        if not isinstance(d, int) or not (1 <= d <= 10):
            errors.append(f"difficulty must be int 1-10, got {d!r}")

    for field in BOOLEAN_FIELDS:
        if field in data and not isinstance(data[field], bool):
            errors.append(f"{field} must be boolean, got {type(data[field]).__name__} {data[field]!r}")

    if data.get("status") == "Absorbed" and not data.get("absorbed_into"):
        errors.append("status Absorbed requires non-empty absorbed_into")
    if data.get("status") == "Broken Down" and not data.get("subtasks"):
        errors.append("status Broken Down requires non-empty subtasks array")

    return errors


def check_verification_debt(data: dict) -> str | None:
    """Return a one-line debt description if this Finished task has missing/failed verification."""
    if data.get("status") != "Finished":
        return None
    tv = data.get("task_verification")
    if not tv:
        return "Finished but task_verification is missing"
    if tv.get("result") != "pass":
        return f"Finished but task_verification.result == {tv.get('result')!r}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate task JSON files and count verification debt."
    )
    parser.add_argument(
        "task_dir",
        type=Path,
        nargs="?",
        default=Path(".claude/tasks"),
        help="Task directory (default: .claude/tasks)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary to stdout.")
    args = parser.parse_args()

    if not args.task_dir.is_dir():
        print(f"error: not a directory: {args.task_dir}", file=sys.stderr)
        return 2

    files = sorted(args.task_dir.glob("task-*.json"))
    validation_errors: dict[str, list[str]] = {}
    debt: list[dict] = []

    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            validation_errors[f.name] = [f"invalid JSON: {e}"]
            continue
        errs = validate_task(data, f)
        if errs:
            validation_errors[f.name] = errs
        d = check_verification_debt(data)
        if d:
            debt.append({"file": f.name, "task_id": data.get("task_id"), "reason": d})

    summary = {
        "task_count": len(files),
        "validation_errors": validation_errors,
        "verification_debt": debt,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Validated {len(files)} task files.")
        if validation_errors:
            print(f"\n{len(validation_errors)} file(s) with schema errors:")
            for fname, errs in validation_errors.items():
                print(f"  {fname}:")
                for e in errs:
                    print(f"    - {e}")
        else:
            print("Schema: OK")
        if debt:
            print(f"\nVerification debt: {len(debt)} Finished task(s) without task_verification.result == 'pass':")
            for d in debt:
                print(f"  - {d['task_id']} ({d['file']}): {d['reason']}")
        else:
            print("Verification debt: none")

    return 0 if not validation_errors and not debt else 1


if __name__ == "__main__":
    sys.exit(main())
```

**Make executable:** `chmod +x .claude/scripts/validate-tasks.py`.

**Spot-check after write:**
- `./.claude/scripts/validate-tasks.py .claude/tasks` — on clean template (empty tasks dir), should print `Validated 0 task files. Schema: OK. Verification debt: none` and exit 0.
- `./.claude/scripts/validate-tasks.py --json .claude/tasks` — should emit JSON with `task_count: 0, validation_errors: {}, verification_debt: []`.

### Step 3: Create `.claude/scripts/README.md`

```markdown
# .claude/scripts

Deterministic helpers invoked by the `/work` orchestrator (or by the user directly) when LLM-executed computation has unacceptable drift or token cost.

## Scripts

| Script | Purpose | Mirrors |
|--------|---------|---------|
| `fingerprint.py` | Spec/section/dashboard-rollup SHA-256 hashes | `support/reference/drift-reconciliation.md` lines 70-84, `commands/status.md` line 36 |
| `validate-tasks.py` | Task JSON schema validation + verification debt count | `support/reference/task-schema.md`, `commands/health-check.md` Part 1 |

## Invocation contract

All scripts follow these rules:

- **Stdlib only.** Python 3.10+ assumed. No `pip install` required.
- **Read-only by default.** None of these scripts write to `.claude/` paths. Orchestrator captures stdout and writes where needed.
- **Stdout: machine-parseable** (JSON or newline-delimited records).
- **Stderr: human-readable diagnostics.**
- **Exit codes:** `0` = success, `1` = validation failure, `2` = runtime/usage error.
- **`--help`:** every script supports `--help`.

## When to invoke

Scripts are **advisory**. Prose procedures in reference docs remain the source of truth. Use scripts when:

- Running inside the orchestrator (not a subagent — subagents lack `.claude/` write capability; the prose procedure works without the script).
- Token cost of LLM-executed computation matters (many calls per session).
- Output consistency matters (drift detection depends on deterministic hashes).

If a script is absent or fails, fall back to the prose procedure.

## Agent invocation

- **Orchestrator (main `/work` loop):** invoke freely via the Bash tool.
- **Subagents:** do not invoke. Subagents cannot write to `.claude/`, so the output has nowhere to go; the orchestrator is the right caller.
- **`claude -p`:** suitable for CI-style use. Use `--allowedTools "Bash(.claude/scripts/* *)"` to scope.

## Dual-location risk

Each script mirrors a reference doc. When a reference doc changes, the matching script must change in lockstep — otherwise the script's output diverges from what the prose promises. Before editing the recipe in a reference doc, search for script call sites and update both.

Candidate follow-up: `task-schema.json` as a single machine-readable source of truth, eliminating the dual-edit risk for `validate-tasks.py`. Deferred pending user decision.
```

### Step 4: Update `.claude/sync-manifest.json`

Locate the `sync` array. After the entry for `.claude/skills/*/SKILL.md`, add:

```json
".claude/scripts/*.py",
".claude/scripts/README.md",
```

(Two entries — Python files and the README. The `**` glob alternative is broader but some sync-manifest consumers don't support it; two explicit entries cover the current scripts.)

### Step 5: Update `.claude/rules/agents.md § "Tool Preferences"`

Append one paragraph at the end of the Tool Preferences section (after the existing "Subagents cannot write to `.claude/`..." paragraph):

```markdown
**Scripts under `.claude/scripts/`** are deterministic helpers that ship with the template and are intended to be invoked by the orchestrator via the Bash tool. They have their own invocation contract (see `.claude/scripts/README.md`): stdlib only, read-only, structured stdout, clear exit codes. Subagents should not invoke them — the scripts return computed values for the orchestrator to write to `.claude/` state, which subagents cannot do. When a script is present, it is an advisory alternative to the matching prose procedure; when absent, the prose procedure still works.
```

### Step 6: Advisory wiring in reference and command docs

For each of the five call sites below, add a short "Script alternative" line alongside the existing prose. **Keep the prose fully intact** — advisory, not replacement.

**6a. `support/reference/drift-reconciliation.md`** — after the "Section fingerprint computation" bash block (around line 82), before the "Note: Tasks without `spec_fingerprint`..." line:

```markdown
**Script alternative:** `.claude/scripts/fingerprint.py --spec PATH` (full spec) or `.claude/scripts/fingerprint.py --sections PATH` (JSON map of `## heading` → hash) — produces byte-identical output to the prose recipes above. Use when running in the orchestrator; the prose recipe remains authoritative if the script is absent.
```

**6b. `support/reference/decomposition.md`** — find the section covering provenance-field population (grep for `spec_fingerprint` and `section_fingerprint`). Add one line after the provenance-write description:

```markdown
**Script alternative:** Capture hashes via `.claude/scripts/fingerprint.py --spec` / `--sections`; orchestrator writes the `sha256:...` strings into task JSON `spec_fingerprint` and `section_fingerprint` fields.
```

**6c. `commands/health-check.md` Part 1** — at the end of the "Verification Debt" paragraph, add:

```markdown
**Script alternative:** `.claude/scripts/validate-tasks.py .claude/tasks` runs schema + verification-debt checks deterministically and prints a combined report. `--json` flag emits structured output for downstream consumption.
```

**6d. `commands/work.md` Step 1b drift** — grep for the drift-detection step in Step 1b. Add a line after the hash-computation description:

```markdown
**Script alternative:** `.claude/scripts/fingerprint.py --spec` / `--sections` for deterministic hashes when the orchestrator runs the drift check.
```

**6e. `commands/status.md`** — at the end of the "Dashboard freshness check" paragraph (line 36), add:

```markdown
**Script alternative:** `.claude/scripts/fingerprint.py --dashboard-rollup .claude/tasks` produces the canonical task-JSON rollup hash in a single call.
```

### Step 7: Tracker bookkeeping (`template-upgrade-2026-04.md`)

**7a. Status line:**
```
**Status:** Phase 4 — FB-011 Families A + B extracted (scripts + advisory wiring); C/D/E remain as later stages
```

**7b. Current State:** add bullet:

```
- **FB-011 Families A + B implemented 2026-04-17:** New `.claude/scripts/` directory with `fingerprint.py` (spec/section/dashboard-rollup hashes) and `validate-tasks.py` (task JSON schema + verification debt). `README.md` documents the invocation contract (stdlib-only, read-only, structured stdout, exit codes). Advisory wiring added to `drift-reconciliation.md`, `decomposition.md`, `health-check.md`, `work.md`, `status.md` — prose procedures remain authoritative, scripts are opt-in. `rules/agents.md § "Tool Preferences"` gained a paragraph clarifying scripts are orchestrator-invoked, not subagent-invoked. `sync-manifest.json § sync` includes the new files. Families C (dashboard regen), D (parallel-plan), E (decision finalization) remain as later extraction stages per `support/workspace/scripts-candidates.md`.
```

**7c. Phase 4 single-item section:** flip the FB-011 row:

Locate `- [ ] **FB-011** — Scripts as alternative...`. Replace with:

```
- [x] **FB-011 (partial — Families A + B)** — `.claude/scripts/fingerprint.py` + `validate-tasks.py` + README; advisory wiring in 5 call sites. *(Implemented 2026-04-17. Families C/D/E remain as later stages — see `.claude/support/workspace/scripts-candidates.md` for tiered plan.)*
```

**7d. File Collision Map:** no strike (FB-011 column wasn't pre-populated). Add new rows for the new files:

```
| `.claude/scripts/fingerprint.py` (new file) | | | | ~~FB-011 Family A~~ ✓ | | | | — | — |
| `.claude/scripts/validate-tasks.py` (new file) | | | | ~~FB-011 Family B~~ ✓ | | | | — | — |
| `.claude/scripts/README.md` (new file) | | | | ~~FB-011 contract~~ ✓ | | | | — | — |
```

Also strike FB-011 cells where already populated (search the map for `FB-011`):
- `rules/dashboard.md` row FB-011 column: `~~• (deferred — Family C)~~`
- `.claude/agents/implement-agent.md` row FB-011 column: `~~Steps 3, 6a, 6c (deferred — Family C)~~`
- `support/reference/dashboard-regeneration.md` row FB-011 column: `~~• (deferred — Family C)~~`

**7e. Cleanup Manifest:** add:

```
| `plan-fb-011-scripts-a-b.md` | DELETE-AFTER | FB-011 Families A + B extraction plan for fresh-session execution |
| `.claude/support/workspace/scripts-candidates.md` | KEEP | Multi-stage inventory; referenced by future Families C/D/E plans |
```

(The inventory doc is NOT delete-after — it's the source of truth for later stages.)

**7f. Session Log entry:** append. Content:

- **Done:** summary of the 3 new files + 5 advisory-wiring edits + rules/agents.md paragraph + sync-manifest update + tracker bookkeeping. Note the spot-checks performed after script creation.
- **Judgment calls:**
  1. Advisory wiring (not mandatory) — preserves prose-as-truth, backward-compatible for downstream projects that haven't pulled scripts.
  2. Stdlib-only Python — no pip deps, simplifies ship/test.
  3. Skipped `task-schema.json` — would eliminate dual-edit risk for validate-tasks.py but doubles scope. Flagged as follow-up.
  4. Skipped test harness — spot-check sufficient at this scope; testing infrastructure earns its keep when Family C lands.
  5. Normalization exactness — script mirrors drift-reconciliation.md lines 70-84 byte-for-byte. Any future edit to either must update both (dual-location risk flagged in scripts/README.md).
  6. Sync-manifest uses two explicit entries (`*.py`, `README.md`) rather than `**` glob — broader compatibility across manifest consumers.
- **Next:** Erik reviews the landed scripts. Option A: advance to Family C (dashboard regen hybrid — biggest win, biggest scope). Option B: pause Stage 2 for real-world trial of A + B before more extraction. Option C: close Phase 4 and move to Phase 5 cleanup.
- **Open questions for later:** `task-schema.json` decision; whether advisory wiring is enough or some call sites should become mandatory (learn from trial); whether FB-017 trial window (Family E candidacy) is ready to evaluate.

---

## Step 8: Commit

Single commit covering: 3 new script files, 7 edited files (sync-manifest, rules/agents.md, drift-reconciliation.md, decomposition.md, health-check.md, work.md, status.md), tracker update.

Pre-commit hook: most of the touched files are sync-category — hook will warn about `version.json` (expected per Phase 5 deferral).

Commit message (HEREDOC):

```
Phase 4: FB-011 Families A + B — fingerprint.py + validate-tasks.py

New .claude/scripts/ directory with two deterministic helpers:

- fingerprint.py: spec hash, per-section hash, dashboard-rollup hash.
  Mirrors drift-reconciliation.md lines 70-84 byte-for-byte.
- validate-tasks.py: task JSON schema validation + verification
  debt count. Mirrors task-schema.md field list.

README.md documents the invocation contract: stdlib-only Python,
read-only, structured stdout, clear exit codes, orchestrator-invoked
(not subagents, which lack .claude/ write capability).

Advisory wiring in drift-reconciliation.md, decomposition.md,
health-check.md Part 1, work.md Step 1b, status.md freshness —
prose procedures remain authoritative; scripts are opt-in.
rules/agents.md § Tool Preferences gains a paragraph on script
invocation boundaries. sync-manifest.json includes the new files.

Families C (dashboard regen), D (parallel-plan), E (decision
finalization) remain as later extraction stages per
support/workspace/scripts-candidates.md.

Rationale: LLMs are unreliable at cryptographic hashing and at
exhaustive schema validation under load — the two families
extracted here are pure computation with deterministic
input→output mapping. Token savings secondary; drift-detection
reliability is the primary motivator.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Verification Checklist (post-edit, pre-commit)

- [ ] `.claude/scripts/fingerprint.py` exists, is executable (`chmod +x`), and `--help` prints usage.
- [ ] `.claude/scripts/validate-tasks.py` exists, is executable, and `--help` prints usage.
- [ ] `.claude/scripts/README.md` exists and describes the invocation contract.
- [ ] Spot-check: `.claude/scripts/fingerprint.py --spec .claude/spec_v1.md` matches `shasum -a 256 .claude/spec_v1.md | cut -d' ' -f1` prefixed with `sha256:`.
- [ ] Spot-check: `.claude/scripts/fingerprint.py --sections .claude/spec_v1.md` prints valid JSON with one entry per `## ` heading.
- [ ] Spot-check: `.claude/scripts/validate-tasks.py .claude/tasks` on clean template exits 0 with "Schema: OK. Verification debt: none".
- [ ] `.claude/sync-manifest.json` parses as JSON and includes the two new script entries.
- [ ] `.claude/rules/agents.md § "Tool Preferences"` has the new Scripts paragraph appended.
- [ ] All 5 advisory-wiring edits landed (drift-reconciliation.md, decomposition.md, health-check.md, work.md, status.md).
- [ ] Tracker: status, Current State bullet, Phase 4 row updated to `(partial)`, File Collision Map new rows + strikes, Cleanup Manifest rows, Session Log entry.
- [ ] Pre-commit hook shows `version.json` warning (expected).

---

## What NOT to Do

- **Don't make the wiring mandatory.** Prose procedures stay authoritative; scripts are advisory. Backward compat for downstream projects.
- **Don't add pip dependencies.** Stdlib only. If a future script needs `jsonschema` or `pyyaml`, flag it and get approval — adds install burden.
- **Don't add a test harness in this commit.** Spot-checks suffice. Test infrastructure earns its keep when Family C lands.
- **Don't create `task-schema.json` in this commit.** Separate decision; would double scope.
- **Don't retire the hash recipes in `drift-reconciliation.md`** — they remain the spec-of-record. Script mirrors the prose; not the other way around.
- **Don't extract Family C, D, or E.** Later stages. Only Families A + B per user decision.
- **Don't bump `.claude/version.json`** — Phase 5 handles scope.
- **Don't edit the scripts after write to match some LLM-computed hash** — the script is the authority once it mirrors the prose. If hash comparison fails, the LLM was wrong.

---

## Pointers to Key Files

| What | Where |
|------|-------|
| Authoritative hash recipe | `.claude/support/reference/drift-reconciliation.md` lines 70-84 |
| Authoritative task schema | `.claude/support/reference/task-schema.md` |
| Dashboard freshness formula | `.claude/commands/status.md` line 36 |
| Inventory (source of truth for extraction strategy) | `.claude/support/workspace/scripts-candidates.md` |
| Tracker | `template-upgrade-2026-04.md` (root) |

---

## Post-Commit: What Happens Next

- Erik reviews the landed scripts in real decomposition / health-check flow (non-blocking).
- If hash computation or validation diverges from LLM expectations, **the script is correct** — update the prose/task-schema, not the script.
- Decision on next step: Family C extraction (biggest win, biggest scope), pause for trial window, or close Phase 4.
- Version bump tally for Phase 5 now includes FB-011 partial.
