# Ship Plan 3 — Interaction-Tax Cuts + an Explicit "Awaiting Erik" Queue

> **Temporary working file** — root-level by request (2026-06-10). Not template content; delete after ship or move to `template-maintenance/`. Source: cross-repo usage analysis 2026-06-10. Companions: `ship-plan-1-evidence-based-verification.md`, `ship-plan-2-prose-diet-and-mechanization.md`. Line-number anchors approximate as of v4.12.1 — re-locate by section name.

## Problem

Erik's sessions are short, frequent, and pause-disciplined — so per-session ceremony is barely amortized. Approval flows ask N questions where one batched response would carry the same audit trail, blocking questions hide in handoff prose instead of a queue, and the feedback pipeline's aggregation stage has never run.

## Evidence base (measured 2026-06-10)

- **Session shape (47-export corpus):** mean 2.8 tasks/session, 38% zero-task meta-sessions, up to 9 sessions/day, 16 `/work pause` mentions, 100% graceful endings, zero `/compact` — context is managed by ending sessions, so per-session overhead multiplies.
- **`iterate.md`:** 20 bracket menus + 32 approval phrases; the Step 4→5 gate (~:347/:369) requires every `[NEEDS APPROVAL]` item resolved individually "even to `[Y] Apply all`" — a user choosing Apply-all still answers N prompts.
- **`health-check.md`:** 23 menus; nested per-diff/per-file menus (~:316–325, :590, :693, :734, Part 8 ~:959) — one run can demand 10+ responses.
- **`work.md`:** 28 bracket menus (per-human-task `[R]/[S]/[P]/[F]`, completion `[C]/[F]`, learning `[L]/[S]`).
- **The queue hides in prose:** styler's `.handoff.json` is a 7.8KB hand-curated blob containing two decisions "PAUSED mid-decision (unanswered)" and a known `/work` Step 0e blind spot as a prose warning; 5 On Hold tasks + an entire increment gated on Erik's go-ahead; 25 handoff-themed friction notes.
- **Aggregation never ran:** `interaction-logs/insights/` empty since 2026-03-30 while 41 session exports + 6 bridges sit in inbox/processed (the README's pipeline stage 4, dispatched by template-repo `/health-check` Part 7).
- **Counter-evidence honored:** all 5 explicit Erik corrections in the corpus re-anchor *framing/scope* — he wants full visibility, not fewer facts. Batch UIs below must preserve complete enumeration; they compress *responses*, not *information*.

## Ship items

### T1 — Single-response batch approval in `/iterate` (MINOR) — ✅ SHIPPED v4.20.0 (2026-06-11)

Keep FB-032's "Decisions in This Proposal" structural contract fully intact (every non-trivial choice enumerated with `[NEEDS APPROVAL]` / `[FROM EXISTING SPEC]` / `[USER REQUESTED]` tags and proposed text). Change only the resolution mechanics at the Step 4→5 gate:

- Present all `[NEEDS APPROVAL]` items as one numbered table.
- One response resolves the batch: `[Y]` approve all as listed · `N3: <choice>, N5: <choice>` override specific items · `[M]` walk item-by-item (current behavior, preserved) · `[P]` postpone.
- DEC-016 compliance is unchanged: the declaration is the audit trail of intent; the `permissions.ask` gate still fires on the spec write. DEC-016 requires routing through `/iterate` — it never required N serial prompts.
- **FB-033 watch:** the spec-auditor trial gate keys on silent-decision friction. Batch approval must not reduce visibility — items remain fully enumerated with proposed text before the single response. Note this explicitly in the ship-log entry so the FB-033 trial reads it as a UX change, not a contract change.

**Files:** `commands/iterate.md` (Step 4→5 gate + menu text).

### T2 — `/health-check` batch triage (MINOR) — ✅ SHIPPED v4.21.0 (2026-06-11)

Flatten the nested menus: each part *collects* its proposed fixes instead of prompting inline; the run ends with one consolidated table (id, part, file, one-line diff summary, risk flag) and a single response — `[A]` apply all · `A except 3,5` · `[N]` none · `[D]` show full diff for listed ids first. Items that overwrite local content (sync-category APPLYs) stay individually flagged in the table with a ⚠ and require explicit inclusion (never bundled into bare `[A]`).

**Files:** `commands/health-check.md` (per-part prompt sites ~:316–325, :590, :693, :734; new end-of-run triage table; Part 8 dispatch menu can stay as-is — it gates expensive audits, not fixes).

### T3 — "Awaiting Erik" queue contract (MINOR — do this one first) — ✅ SHIPPED v4.14.0 (2026-06-10)

New invariant: **anything blocked on the user must exist as a dashboard 🚨 Action Required row with the concrete question inline** — never only as handoff prose. Covers: `owner: human` pending tasks, On Hold tasks, unresolved decision records, mid-decision pauses (an AskUserQuestion the user never answered), `owner: both` items awaiting user review.

- `commands/work.md` session start (Step 1 area): print the queue ("Waiting on you: N items — …") before routing.
- `commands/work.md § pause`: before writing the handoff, sweep for open questions; each gets an Action Required row (targeted-edit path per FB-080 is sufficient — no full regen needed). The handoff may *point* to rows, not hold questions exclusively.
- `rules/dashboard.md` + `support/reference/dashboard-regeneration.md`: document the invariant in the Action Required section spec.

**Evidence anchor:** both styler "paused mid-decision (unanswered)" items would have been visible rows instead of buried prose.

### T4 — Pause-ceremony slimming + run the insights backlog (PATCH + maintenance) — ✅ schema cap SHIPPED v4.21.1 (2026-06-11); maintenance run below

- **Handoff schema cap:** give `.handoff.json` bounded fields (active-task state, next step, open-question pointers, session knowledge ≤ ~10 bullets); overflow goes to a workspace file the handoff points at. Today's 7.8KB free-prose blob is write-expensive and read-unreliable.
- **Maintenance action (not a ship):** run `/health-check` in the template repo so Part 7 processes the inbox and pipeline stage 4 finally writes `interaction-logs/insights/` documents over the 47 accumulated exports. Then decide a cadence (e.g., every N exports or monthly) and note it in `interaction-logs/README.md`.

**Files:** `commands/work.md § pause` (handoff write), `support/reference/context-transitions.md` if it specs the handoff shape; `interaction-logs/README.md` (cadence note only).

## Sequencing & version bumps

T3 (MINOR, highest value) → T1 (MINOR) → T2 (MINOR) → T4 (PATCH + the maintenance run). Independent; stop after any.

## Acceptance

- `tests/scenarios/`: (a) pause with an unanswered decision → Action Required row exists + next `/work` start lists it; (b) `/iterate` batch with 4 `[NEEDS APPROVAL]` items → one response applies, declaration unchanged in proposal output; (c) health-check run with fixes across 3 parts → exactly one triage prompt; ⚠ sync-overwrite item excluded from bare `[A]`.
- Count human responses required in a traced `/health-check` + `/iterate` session before/after (target: ≥50% fewer prompts, zero information loss).
- After the T4 maintenance run: `interaction-logs/insights/` non-empty; spot-check one insight doc against its source exports.

## Conflicts with other plans

`commands/work.md` (T3, T4) also edited by Plan 1 S3/S4 and split by Plan 2 P3 — land T3 before P3. `health-check.md` (T2) also touched by Plan 2 P4 (different sections — sequence, don't interleave). `iterate.md` (T1) untouched by other plans.

## Ledger updates on ship

- `template-maintenance/ship-log.md` + `.claude/version.json` per ship.
- If T1 changes observed silent-decision behavior either way, note it on FB-033 (its trial gate consumes exactly this signal).
