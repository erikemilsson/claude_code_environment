# Inbox Harvest Triage — 2026-07-19

First-pass triage of the full `interaction-logs/inbox/` backlog: **38 files** (2026-06-11 → 2026-07-06; the previous harvest ran 2026-06-11). 35 session exports + 3 user-feedback bridges. Projects: styler (~17), tinder-streamliner (~16), flirty-gym (1), OEMMatInsightBI (1 bridge). Note: `styler-…-06-25-1205` / `-1308` are the same session exported twice (identical markers).

**Status: ROUTED 2026-07-19 (user "do all").** Tier 1 shipped as **v5.2.0** (see ship-log); Tier 2 A–F captured as **FB-103 … FB-108** in `template-maintenance/feedback.md`; all 38 files moved to `processed/`; insights written for the three big clusters (limit-cutoff, concurrency, AR auto-render). Marker totals: 19 `verification_gap` (mostly `files_affected` prediction drift), 13 `design_contradiction` + 8 `path_drift` (project-internal, not template signal), 1 `template_gap`.

---

## Tier 1 — Cheap, high-confidence fixes (proposed ship bundle)

| # | Fix | Evidence | Files |
|---|---|---|---|
| 1 | **Decomposition ordering:** flip spec status draft→active BEFORE the fingerprint/index/snapshot step (current order stamps task JSONs with a pre-flip hash → false-drift trap) | tinder 06-23 (pushback) + tinder 06-25-2008 (friction) — hit twice, manually re-stamped both times | `reference/decomposition.md` |
| 2 | **/iterate post-apply index regen:** apply step must regenerate `spec_v{N}.index.json` after editing the spec | tinder 07-02-2210 (had to regen manually); tinder 07-03 shows the fixed flow working | `commands/iterate.md` |
| 3 | **`fingerprint.py --index` prints to stdout, doesn't write the file** — bare command in docs reads like it writes; cost a silent stale index twice | tinder 06-24-1431, 06-27-0814 (index said 18 sections, spec had 19) | either make `--index` write the file, or fix the phrasing in `rules/spec-workflow.md` + `.claude/CLAUDE.md` nav (only work.md Step 1b shows the redirect) |
| 4 | **`fingerprint.py --spec` output shape:** bare `sha256:` string while `--index`/`--sections` emit JSON — `json.loads()` consumers crash | tinder 06-25-2008 | `fingerprint.py` (emit JSON) or document the bare-string contract |
| 5 | **Dispatch-prompt JSON-envelope hardening:** add explicit "return valid JSON matching this exact schema" to the agent dispatch prompts (persona-via-prompt didn't transmit the Step-6 envelope contract) | styler 07-06 (agent returned prose; orchestrator recovered) | `commands/work.md` dispatch blocks |
| 6 | **`desktop-project-prompt.md` scope blockquote:** clarify it describes the *pre-spec brainstorming* project only, not an operational/runtime claude.ai project surface | tinder bridge 06-23 (project carries a local edit that Part 5 flags every sync) | `reference/desktop-project-prompt.md` — converges the downstream edit |
| 7 | **Mixed `src/` + `.claude/` tasks:** decomposition note — split or annotate (`.claude/` portion is orchestrator-inline per DEC-004; agent takes the rest) | styler 06-13, tinder 06-14-1540, tinder 06-23 (corrected mid-flow via precedent) — 3 sessions | `reference/decomposition.md` + `reference/parallel-execution.md` |
| 8 | **`files_affected` prediction heuristics:** declare the sibling test file by default; new-component extraction lands edits in the *new* file, not the declared shared ones | 19 `verification_gap` markers across styler + tinder, all benign drift reconciled post-hoc | `reference/decomposition.md` (heuristics section) |
| 9 | **Pause-as-checkpoint:** acknowledge mid-session checkpoint pauses (user pauses, keeps working, pauses again) — current framing is wind-down-only | tinder 06-14-1605 (double export same session) | `commands/work.md § pause` or `rules/session-management.md` |
| 10 | **Project-vs-template DEC numbering note:** project decision files (DEC-001…) numerically collide with template DEC references (DEC-016/021/024) in spec/rules text | tinder 06-27 | `reference/decisions.md` |
| 11 | **Renderer nits** (verify against v5.1.x first): (a) status legend shows lifetime/archived Finished count unlabeled beside the active total ("Finished 865" vs "285 tasks"); (b) phase heatmap labels a whole phase "Blocked" when only 1 of M tasks is gated — "N of M dispatchable" reads better | styler 06-25-1308; tinder 06-27 | `scripts/dashboard-render.py` + tests |

## Tier 2 — Structural candidates (proposed FB captures)

- **A. Hard session-limit agent cutoff — strongest cluster (4 distinct sessions).** DEC-010's `partial_completion` envelope assumes the agent detects its *own* budget; a platform usage-limit cutoff kills the subagent mid-tool-call with `subagent_tokens: 0`, no report, and partial files on disk. Happened ≥5 times (styler 06-15 ×2 agents, 06-22, 06-24-2026 ×2, 07-01 ×2). A recovery pattern is **proven twice** (07-01): orchestrator runs typecheck+tests directly; if green, dispatch a fresh agent for formal self-review only (not a rebuild). Capture: codify the recovery path in `work-procedures.md`, add pre-dispatch budget awareness before parallel long-agent batches, and after one limit-hit, confirm with the user before re-attempting parallel dispatch (07-01 pushback: second parallel batch also got cut).
- **B. Multi-session concurrency on one repo (4+ sessions, both projects).** No template model: handoff overwrite/consume races (flirty-gym + styler both hit stale handoffs from parallel threads), git-index races, a concurrent session's `git add` sweeping this session's edits into its commit, verify-agent confused by files a parallel session modified. Cheap slice now: pre-parallel-dispatch `git status` re-check (not just Step 0e session start) + handoff preserve-not-consume when it references another session's task. Full model: research-gated.
- **C. Action Required card auto-render (3 convergent signals).** Styler: empty unfilled placeholder at session start silently broke the human-gated coverage invariant; styler: the fill step is a repeated per-regen Read+Edit dance; tinder: locally diverged its script to auto-render the card from structured sources (task JSONs, feedback.md, audit_digest). Direction: script renders the mechanical portion (human/both tasks, on-hold, decisions, audit counts) deterministically; LLM augments judgment items. MINOR + renderer tests.
- **D. New spec section → no decompose trigger (styler 06-24, two linked notes).** After `/iterate` adds a section, the `/work` fast-path (matching META fingerprint) actively *skips* drift detection; and regenerating the dashboard at pause would enable that fast-path, so the session deliberately left the dashboard stale. Capture: `/iterate` sets a "new section, 0 tasks reference it" marker `/work` consumes + a documented pause carve-out.
- **E. Build-blocking vs validation phase gates (tinder 06-27).** A next phase's build was gated behind an un-forceable `owner:human` real-use acceptance task; only workaround was `cross_phase` on every build task. Capture: distinguish gate types (or document the workaround).
- **F. owner:both verification without a subagent for personal data (tinder 06-25-1955).** Real-canonical-data tasks used user sign-off + orchestrator structural check (`verified_by: "user + orchestrator"`) to avoid pulling personal data into a subagent — worked well, undocumented. Capture: name this path in the State Persistence Protocol / work-procedures.
- **G. (defer, single signal)** Autonomous-batch model has no notion of a task too large for one response (tinder 06-25-2150: two diff-6 authoring tasks each consumed the output budget + forced manual "continue").

## Tier 3 — Close, no action

- **OEMMatInsightBI mermaid-sanitization bridge (06-14):** superseded — DEC-024/v5.0.0 deleted the mermaid renderer entirely; the bug can't exist at 5.x. Action: reply-to-project = sync to 5.x; archive the bridge.
- **work-procedures.md missing downstream at 4.27.0 (tinder 06-14):** stale-sync artifact; file ships in the sync manifest and the project is on 5.1.x now.
- **TaskCreate/TaskUpdate reminder noise:** 2 further reports (tinder 06-25-2150 "fired nearly every turn", styler 06-23-1755). FB-075's condition (b) (token tax scaling) is trending toward met but the fix remains upstream-Anthropic-gated. Noted on FB-075.
- **Auto-mode classifier (styler 07-06):** logged as FB-077 trigger-(c) candidate in root `CLAUDE.md` (2026-07-19). The export itself concludes confirm-on-delete is probably correct behavior; no template action.
- **BSD-grep silent-fail recurrences (styler):** already covered by `rules/agents.md § Negative Findings` — the rule demonstrably fired and prevented a false finding (06-23-1859).

## Working-as-designed evidence (confidence + capability-research input)

Validated end-to-end this window: the merge-queue re-entry transport (tinder 07-02: two shakedown findings queued mid-session, drained at `/iterate` with no restatement); the DEC-023 vision-hub arc ×3 (styler occasion + wardrobe-coverage, tinder v3 commands); writer/reviewer separation catching real cross-task integration bugs the per-task tests missed (styler 06-16 `capture_lighting` path bug; 06-22 unwired AC behind green tests); the owner:both visual-iteration loop (styler face-drape work); the Empirical Evidence Gate verify→orchestrator handoff (styler 07-06, "worked exactly as documented"); the negative-findings positive-control rule preventing a false chart-WB finding.

**Capability-research conclusion:** across 38 exports there is no demand signal for a new capability — every recurring ask is a robustness ask (concurrency model, limit-resilient dispatch, prediction accuracy, doc truth-ups). This matches the stated investment direction: make it run smoother, not wider.

## Confirmation-gated next steps

1. **Ship Tier 1** as one bundle (mostly MINOR: procedure-order changes + script output shapes; renderer nits verified first).
2. **Capture Tier 2 A–F** as new FB entries in `template-maintenance/feedback.md` (IDs assigned at capture after the four-file dedup scan).
3. **Move all 38 inbox files to `processed/`** and write `insights/` entries for the three big clusters (limit-cutoff, concurrency, AR auto-render).
4. Reply-to-project notes: OEMMatInsightBI → sync to 5.x; tinder → Tier-1 #6 converges their local edit.
