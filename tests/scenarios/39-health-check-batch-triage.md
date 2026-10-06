# Scenario 39: /health-check Batch Fix Triage (collect, don't prompt)

Verify the Fix Queue Protocol + Step 4 triage table (shipped v4.21.0, Plan 3 T2): parts collect proposed fixes instead of prompting inline; one run = one fix prompt; ⚠ rows (locally modified sync files, unreviewed appends) never ride bare `[A]`. Since v5.12.0 a sync file that is an unchanged template copy is a `—` row and applies under bare `[A]`.

## Context

Observed failure mode (2026-06-10 cross-repo analysis): health-check.md carried 23 menus with nested per-diff/per-file prompts — one run could demand 10+ responses. Erik's sessions are short and frequent, so per-run ceremony never amortizes. Fix compresses responses, never information: every finding still reported, every fix still listed, ⚠/needs-input rows surfaced individually.

## State (Base)

A downstream project where `/health-check` (no flags) finds:

- Part 1: dashboard stale (hash mismatch) → regen fix
- Part 1: task-12 "In Progress" for 9 days → stale, needs user choice
- Part 3: DEC-004's `status:` line has a trailing `# comment` → rewrite-line fix
- Part 5: `commands/work.md` differs upstream and matches no template version of its path (`sync-check.py` status `modified`: Locally modified)
- Part 5: `rules/dashboard.md` differs upstream and equals the template's v5.4.0 copy of its path (status `template_copy`: Unchanged template copy)
- Part 2d: capability doc 120 days stale → [V] offer

---

## Trace 39A: Exactly one triage prompt for fixes across 4 parts

- **Path:** Steps 1–3 (scan, checks, report) → Step 4 (Batch Fix Triage)

### Expected

- Parts 1, 2d, 3, 5 each QUEUE their items; zero inline prompts during the run
- After the report: ONE table with 6 rows (id, part, file, one-line fix, risk), then ONE response request
- Rows in queue order: 1 dashboard regen, 2 DEC-004 rewrite, 3 [V] offer, 4 `commands/work.md`, 5 `rules/dashboard.md`, 6 task-12
- Risk flags: regen + rewrite-line + [V] offer = `—`; row 4 `Update template file (locally modified, [D] shows the diff)` = `⚠ overwrites local`; row 5 `Update template file (unchanged copy of v5.4.0; includes dashboard regen)` = `—`; task-12 = `needs-input` with choices inline

### Pass criteria

- [ ] Zero mid-run prompts (no "[V]/[S]/[D]?", no "Apply all / Select individually?", no per-file menus)
- [ ] Exactly one fix prompt in the whole run
- [ ] The locally modified sync row is flagged ⚠; the unchanged-copy row is `—`
- [ ] task-12 row carries its question inline, not a separate prompt

### Fail indicators

- Part 5 prompting "Apply all / Select individually / Skip?" before Part 6 runs
- Part 2d asking "[V] Verify | [S] Skip | [D] Defer" inline
- Findings summarized away ("4 parts found issues — apply?") instead of enumerated rows

---

## Trace 39B: Bare [A] excludes ⚠ and needs-input rows

- **Path:** Step 4 table → user responds `A`

### Expected

- Applied: dashboard regen, DEC-004 line rewrite, the [V] pass offer, and the `rules/dashboard.md` update (unflagged rows only)
- NOT applied: the `commands/work.md` row (⚠), task-12 (needs-input) — listed back as still-open in the post-apply summary
- `rules/dashboard.md` is a dashboard-rule file, so its row's regen and row 1's are one regen, run last
- The [V] sub-flow runs after the batch, with its per-section [A]/[R]/[S] adjudication intact

### Pass criteria

- [ ] No locally modified sync file overwritten by bare `A`; the unchanged copy is updated
- [ ] Still-open rows listed back explicitly (nothing silently dropped)
- [ ] Dashboard regen runs at most once, last
- [ ] A Part 5 row was applied, so after the post-apply summary Part 5 Step 5 offers the commit: `M .claude/rules/dashboard.md` and `M .claude/version.json` (plus `M .claude/sync-manifest.json` if the write-back changed it), with `[C]` / `[L]` and the message suffix ` (partial: 1 sync files not updated)`. The DEC-004 rewrite, the regenerated dashboard and `.sync-state.json` are not listed (not Part 5 paths, or gitignored)

### Fail indicators

- `commands/work.md` checked out from template on bare `A`
- needs-input row silently dropped from the summary
- [V] sub-flow skipped or auto-accepted without per-section adjudication

---

## Trace 39C: Explicit inclusion + per-item answers in one response

- **Path:** user responds `A include 4, 6: on-hold` (row 4 = the locally modified `commands/work.md`; row 6 = task-12)

### Expected

- Row 4 applies (explicit inclusion by id satisfies the ⚠ gate); row 5 applies under the bare `A`. Without `include 4`, row 4 would stay open
- task-12 → On Hold with notes, from the same single response
- One `sync-apply.py` call writes both files; afterwards the sidecar has an entry for every compare-set file that equals upstream, not only these two
- After the post-apply summary Part 5 Step 5 offers the commit: `M .claude/commands/work.md`, `M .claude/rules/dashboard.md` and `M .claude/version.json` (plus `M .claude/sync-manifest.json` if the write-back changed it), with `[C]` / `[L]`. The DEC-004 rewrite, task-12's change, the regenerated dashboard and `.sync-state.json` are not listed (not Part 5 paths, or gitignored)

### Pass criteria

- [ ] One response carries apply-set + ⚠ inclusion + a needs-input answer simultaneously
- [ ] The ⚠ row applies only because it is named
- [ ] `[D] 4` before deciding prints the full diff and re-prompts without consuming the response
- [ ] The commit offer comes after the post-apply summary and lists only Part 5 paths

### Fail indicators

- `commands/work.md` overwritten by a response that doesn't name row 4
- The per-item answer requiring a second round-trip
- The commit offer appearing before the batch applies, or listing the decision record or task file

---

## Trace 39D: Part 8 menu unaffected; --report skips the queue

- **Path:** same run reaching Part 8; separate run with `--report`

### Expected

- Part 8 still presents its interactive audit-dispatch menu (gates expensive audits, not fixes) — unchanged by the protocol
- `--report` run: report only; no queue, no table, no prompts (no Part 5 Step 5 commit offer either)

### Pass criteria

- [ ] Part 8 menu intact and interactive
- [ ] `--report` produces zero fix prompts and no commit offer

### Fail indicators

- Audit dispatch rows appearing in the fix table
- `--report` rendering the triage table anyway
