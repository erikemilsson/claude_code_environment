# Scenario 39: /health-check Batch Fix Triage (collect, don't prompt)

Verify the Fix Queue Protocol + Step 4 triage table (shipped v4.21.0, Plan 3 T2): parts collect proposed fixes instead of prompting inline; one run = one fix prompt; ⚠ rows (sync-category applies, unreviewed appends) never ride bare `[A]`.

## Context

Observed failure mode (2026-06-10 cross-repo analysis): health-check.md carried 23 menus with nested per-diff/per-file prompts — one run could demand 10+ responses. Erik's sessions are short and frequent, so per-run ceremony never amortizes. Fix compresses responses, never information: every finding still reported, every fix still listed, ⚠/needs-input rows surfaced individually.

## State (Base)

A downstream project where `/health-check` (no flags) finds:

- Part 1: dashboard stale (hash mismatch) → regen fix
- Part 1: task-12 "In Progress" for 9 days → stale, needs user choice
- Part 3: DEC-004 file missing from dashboard Decisions table → add-entry fix
- Part 5: `commands/work.md` differs upstream, local hash ≠ sidecar synced_hash (Modified upstream)
- Part 5: `rules/dashboard.md` differs upstream, local hash == sidecar synced_hash (hash-verified clean)
- Part 2d: capability doc 120 days stale → [V] offer

---

## Trace 39A: Exactly one triage prompt for fixes across 4 parts

- **Path:** Steps 1–3 (scan, checks, report) → Step 4 (Batch Fix Triage)

### Expected

- Parts 1, 2d, 3, 5 each QUEUE their items; zero inline prompts during the run
- After the report: ONE table with 6 rows (id, part, file, one-line fix, risk), then ONE response request
- Risk flags: regen + add-entry + [V] offer = `—`; both sync applies = `⚠ overwrites local` (the clean one annotated `hash-verified: no local edits`); task-12 = `needs-input` with choices inline

### Pass criteria

- [ ] Zero mid-run prompts (no "[V]/[S]/[D]?", no "Apply all / Select individually?", no per-file menus)
- [ ] Exactly one fix prompt in the whole run
- [ ] BOTH sync rows flagged ⚠ — including the hash-verified one
- [ ] task-12 row carries its question inline, not a separate prompt

### Fail indicators

- Part 5 prompting "Apply all / Select individually / Skip?" before Part 6 runs
- Part 2d asking "[V] Verify | [S] Skip | [D] Defer" inline
- Findings summarized away ("4 parts found issues — apply?") instead of enumerated rows

---

## Trace 39B: Bare [A] excludes ⚠ and needs-input rows

- **Path:** Step 4 table → user responds `A`

### Expected

- Applied: dashboard regen, DEC-004 entry, the [V] pass offer (unflagged rows only)
- NOT applied: both sync rows (⚠), task-12 (needs-input) — listed back as still-open in the post-apply summary
- The [V] sub-flow runs after the batch, with its per-section [A]/[R]/[S] adjudication intact

### Pass criteria

- [ ] No sync-category file overwritten by bare `A`
- [ ] Still-open rows listed back explicitly (nothing silently dropped)
- [ ] Dashboard regen runs at most once, last

### Fail indicators

- `commands/work.md` checked out from template on bare `A`
- needs-input row silently dropped from the summary
- [V] sub-flow skipped or auto-accepted without per-section adjudication

---

## Trace 39C: Explicit inclusion + per-item answers in one response

- **Path:** user responds `A include 5, 6: on-hold` (row 5 = hash-verified sync apply; row 6 = task-12)

### Expected

- Row 5 applies (explicit inclusion by id satisfies the ⚠ gate); the Modified-upstream sync row still excluded (not named)
- task-12 → On Hold with notes, from the same single response
- Sidecar updated only for the applied sync file; excluded file resurfaces next sync

### Pass criteria

- [ ] One response carries apply-set + ⚠ inclusion + a needs-input answer simultaneously
- [ ] Only the named ⚠ row applies
- [ ] `[D] 4` before deciding prints the full diff and re-prompts without consuming the response

### Fail indicators

- "include 5" interpreted as including ALL ⚠ rows
- The per-item answer requiring a second round-trip

---

## Trace 39D: Part 8 menu unaffected; --report skips the queue

- **Path:** same run reaching Part 8; separate run with `--report`

### Expected

- Part 8 still presents its interactive audit-dispatch menu (gates expensive audits, not fixes) — unchanged by the protocol
- `--report` run: report only; no queue, no table, no prompts

### Pass criteria

- [ ] Part 8 menu intact and interactive
- [ ] `--report` produces zero fix prompts

### Fail indicators

- Audit dispatch rows appearing in the fix table
- `--report` rendering the triage table anyway
