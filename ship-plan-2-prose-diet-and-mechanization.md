# Ship Plan 2 — Prose Diet + Mechanization (shrink what the LLM must obey; script what it must not skip)

> **Temporary working file** — root-level by request (2026-06-10). Not template content; delete after ship or move to `template-maintenance/`. Source: cross-repo usage analysis 2026-06-10. Companions: `ship-plan-1-evidence-based-verification.md`, `ship-plan-3-interaction-tax-and-queue.md`. Line-number anchors approximate as of v4.12.1 — re-locate by section name.

## Problem

The template's reliability rests on long prose procedures the model must execute under load — and the ship history proves it doesn't: roughly two-thirds of all template ships are fixes to previously-shipped mechanisms, with `work.md` the most-patched file. Each misfire lands on Erik as state corruption or another fix-session. Separately, ~25K of the ~66K chars auto-loaded into every session is rarely load-bearing.

## Evidence base (measured 2026-06-10)

- **~74 ships 2026-04-02 → 2026-05-27; ~50 were fixes/hardening, ~24 net-new** (ship-log classification).
- **`commands/work.md`: ~20 ship touches** — most-patched file; now 71.7K chars, 1,150 lines, 12 top-level steps + 3 modes, 218 lines containing conditionals.
- **"Documented but not executed" is the recurring root cause:** FB-017 (Step 2b decision finalization skipped), FB-045/DEC-011 ("orchestrator skipped the marker-append step throughout the session"), FB-038 (dashboard regressed 5 days after FB-015's fix — user quote: "even more cluttered… *after we implemented a fix*"). Steps 0d/0e/0f exist as recovery machinery compensating for skipped steps.
- **Dashboard content discipline: 5 ships** (FB-015 → FB-038 → FB-080 → FB-090 + v4.7.2 example drift). FB-080 documented orchestrators informally ignoring Tier-1 regen triggers in two projects in the same week; FB-090 removed cap "discretion" outright.
- **`files_affected` accuracy: 6 ships** (FB-058 → FB-065 → FB-064 → FB-073 → FB-086 + FB-043), ending with verify-agent auto-correcting the metadata — an admission declared scope can't be trusted. Echothread T80–T83 declared 4 files, edited 10–14.
- **Always-loaded context:** `.claude/CLAUDE.md` 7.6K + 8 rules files 58.1K ≈ 66K chars per session (styler measures 74.6K with its project files). Rarely load-bearing: `feature-retirement.md` 15.9K (needed only mid-retirement), `agents.md` rare sections ~6–8K (MCP fan-out, MCP result-size, cross-project capture, dispatch rationale), `session-management.md` human-facing tables ~4K.
- **Duplication:** audit twins share verbatim blocks — synthesizer description constraints (audit-coherence ~:396 ≡ audit-ui ~:686), digest.json schema in both (~:487 / ~:853), promote-mode steps restated in both. audit-ui triage already delegates correctly ("identical to `/audit-coherence triage` § Algorithm with these substitutions", ~:320) — the proven pattern.
- **Pointer rot:** `rules/agents.md § Dispatch Convention` cites work.md "line ~605 / ~688" (actual ≈ :747 / :844 — ~150 lines stale); `audit-coherence.md` ~:270 cites `support/reference/audit-template-pattern.md` which does not exist; `.claude/CLAUDE.md` pins `claude-opus-4-7[1m]` while work.md dispatches `model: "opus[1m]"` at 3 sites; `status.md` renders "Complete/At Risk/Overdue" icons that aren't the canonical 8 statuses.

## Ship items

### P1 — Pointer-rot + consistency sweep (PATCH, do first) — ✅ SHIPPED v4.13.1 (2026-06-10)

1. `rules/agents.md § Dispatch Convention`: replace stale line numbers with section-name anchors ("§ If Verifying (Per-Task)", "§ Phase-Level Verification") — and stop using line numbers in cross-file refs generally.
2. `audit-coherence.md` ~:270 phantom citation: read the context; if its intent matches the shared audit core (P4), create the doc under the cited name; otherwise fix the citation now and let P4 name freely.
3. Model pin: make work.md's 3 dispatch sites reference the pin in `.claude/CLAUDE.md § Model Requirement` (one source of truth) instead of a hardcoded variant.
4. `status.md` icon vocabulary: align to canonical statuses or annotate explicitly as a display-layer mapping.

### P2 — Lazy-load diet (MINOR, ~25K chars/session reclaimed)

1. **`feature-retirement.md`:** remove from `.claude/CLAUDE.md` `@imports`; its summary line becomes a trigger: "Before retiring or restoring any feature, READ `.claude/rules/feature-retirement.md` first — it is not auto-loaded." File stays where it is (audit-coherence retired-features lens and `support/retired/README.md` cross-refs remain valid).
2. **`agents.md`:** move "MCP and Parallel Execution", "MCP and Result-Size Constraints", "Cross-Project Capture Protocol", and the dispatch-convention *rationale* paragraphs to `support/reference/` (candidates: a new `mcp-patterns.md` + fold capture protocol into `extension-hooks.md` or `claude-code-authoring.md`); leave 2-line stubs with explicit MUST-read triggers ("before dispatching a parallel batch involving MCP work, read X").
3. **`session-management.md`:** move the human-facing tables (`--continue`/`--resume`/rewind/`/btw`) into `.claude/README.md` (the user guide); keep "Claude's Responsibilities" + the which-mechanism table.
4. Update `.claude/CLAUDE.md § Workflow Rules` summary lines to reflect lazy entries.

**Hazards:** `/health-check` Part 5 sync manifest must reflect moved/added files; trace test that a retirement scenario actually reads the rule via the trigger (the lazy-load failure mode is "model doesn't read it when needed" — the trigger line is the mitigation, and `/health-check` can spot-check for retirements lacking manifests).

### P3 — `work.md` decomposition (MINOR)

Extract into `support/reference/` procedure docs, each behind an explicit "STOP — read X now" gate at its step (precedent: Step 1a/1b already delegates to `drift-reconciliation.md`):

- State Persistence Protocol (the 8+ post-return steps)
- `/work pause` procedure (incl. session-export steps) and `/work complete`
- Auto-archive mode

Keep inline: step skeleton, routing logic, dispatch prompt templates (load-bearing at dispatch time). Target: work.md ≤ ~40K chars. Trace tests for pause + persistence flows after the split.

### P4 — Audit-family shared core (MINOR, ~15–20K saved + drift-proofing)

Create one reference doc (name per P1 item 2) holding: lens-output format block, synthesizer `description` constraints, `digest.json` schema, promote-mode algorithm, triage algorithm. Both audit commands delegate with per-command substitution tables — the exact pattern audit-ui triage already uses. The two copies stop drifting apart (the v4.12.0 mirror-kill for dashboard SKILL.md is precedent that mirrors rot).

### P5 — Mechanization: Family C escalation + new Family F candidate (staged)

- **Family C (dashboard-render.py, hybrid):** `template-maintenance/scripts-candidates.md` gates this on health-check check 4b firing repeatedly (≥2 projects or ≥3 runs). Formal 4b telemetry is absent, but the patch history is the same signal by another route: 5 dashboard-discipline ships, FB-080's documented Tier-1 trigger violations in two projects, FB-090 removing discretion. **Decision — RESOLVED 2026-06-10: trigger declared MET** (user decision; amendment recorded in `template-maintenance/scripts-candidates.md § Family C` — the 4b channel proved structurally unsampled, substituted standard = recurrent post-fix dashboard regressions, scope authorized = PoC only). When this plan executes: start with the inventory's own PoC recommendation — script renders the Tasks-by-phase section only, LLM keeps synthesis sections — then expand per scripts-candidates Family C shape (structural sections between marker pairs; Action Required + Notes stay LLM) only if the PoC holds.
- **Family F (new candidate — add to scripts-candidates.md, don't ship yet):** post-batch **state-invariant checker** — a read-only script the orchestrator runs after each batch / before pause: markers appended when friction kinds were reported (DEC-011/FB-089 class), task JSON transitions legal, handoff/export files exist when expected, `pending_full_regen` consistency. Same shape as `validate-tasks.py`; converts "did I remember every State Persistence step?" from recall into a checklist diff.
- **Family D:** unchanged (watch-gated; FB-086's verify auto-correct addressed the metadata-accuracy half).

## Sequencing & version bumps

P1 (PATCH) → P2 (MINOR) → P4 (MINOR) → P3 (MINOR) → P5 (PoC, MINOR when it ships). P2/P4 are independent; P3 last among the doc work because it churns work.md anchors that Plans 1 and 3 also touch.

## Acceptance

- Byte deltas measured before/after (`wc -c` on the auto-loaded set; target ≥20K reduction; record in ship-log).
- `tests/scenarios/`: retirement-trigger read test; pause + persistence flows post-split; audit delegation resolves (no dangling substitutions).
- `/health-check` clean including Part 5 (sync manifest reflects moved files).
- For P5 PoC: same task set rendered twice → byte-identical structural sections.

## Conflicts with other plans

P3 rewrites work.md structure — land **after** Plan 1 S3/S4 and Plan 3 T3 (their edits are small and anchored; easier into the monolith than into a mid-flight split). P4 touches health-check/audit files that Plan 3 T2 also edits (different sections; sequence, don't interleave).

## Ledger updates on ship

- FB-011 (scripts tracker): update Family C status + add Family F candidate; mirror in root `CLAUDE.md § Active Follow-ups`.
- `template-maintenance/ship-log.md` + `.claude/version.json` per ship; sync manifest for moved/new reference docs.
