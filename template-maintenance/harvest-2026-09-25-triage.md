# Harvest 2026-09-25 — triage

**Source:** `/health-check` Part 7, 13 exports (9 oemmatinsightbi @ template 5.4.0, 2026-08-12 → 09-19; 4 styler @ 5.0.0, 2026-09-20 → 09-24). All `export_quality: full`. Moved to `interaction-logs/processed/`.
**Status:** COMPLETE, triaged with the maintainer 2026-09-25 (one question per cluster). Final filing in `template-maintenance/feedback.md`:
- **FB-118** = clusters 6 + 7 merged (Needs-you derivation gaps + augment persistence)
- **FB-119** = cluster 8 (orchestrator is the unverified actor); absorbs the "live-state records go stale" line removed from the FB-115 amendment
- **FB-120** = clusters 9 + 10 bundled (Python floor, timeout-vs-interrupted, pending-markers)
- Amendments landed on FB-113 (two-project; caveat superseded; cross-link to FB-115), FB-114 (all four), FB-115 (caveat kept), FB-116, FB-117

The draft entries below keep their **provisional numbers (FB-118…FB-122) and are superseded** by the filed text.

Dedup was checked against all four FB files by exact filename (`template-maintenance/feedback.md`, `template-maintenance/feedback-archive.md`, `.claude/support/feedback/feedback.md`, `.claude/support/feedback/archive.md`). Highest existing ID: FB-117.

## Cluster table

| # | Pattern | Incidents (exports) | Projects | Route |
|---|---------|--------------------|----------|-------|
| 1 | `files_affected` under-counts synchronized locations (docs that summarise a changed pattern, shared types, `package.json` test wiring) | 08-13-0916, 08-20, 09-21, 09-24-1745 ×2, 09-24-2256 | both | **amend FB-113** |
| 2 | Negative-findings probe defeated: `Grep` absent in subagents (again), ripgrep honours `.gitignore` → gitignored `.claude/` state silently missed; rule governs findings but not *sweeps* | 08-12, 09-19 ×2, 09-21 | both | **amend FB-114** |
| 3 | Sweeps scoped to what was edited, not what the edit invalidated; **re-dating a section silently re-certifies stale counts under it**; synonym-blind residue sweeps | 08-12 (4 sites), 08-21-0642, 08-21-1945, 09-19 | oemmat | **amend FB-115** |
| 4 | Evidence gate: Playwright MCP blocked by the user's Chrome, no "held pending evidence" / "not run" state; unbounded `browser_evaluate` loops hang | 09-21, 09-24-1745 ×2, 09-24-2256 | styler | **amend FB-116** |
| 5 | Tasks whose only legal path is a user-typed gated command (`/iterate`) are effectively human-owned, but `owner` says `claude`/`both` → unroutable | 08-21-0642, 08-21-1945, 09-19 | oemmat | **amend FB-117** |
| 6 | **Needs-you derivation gaps** (verified in `dashboard-render.py`) | 08-13-0916, 08-18, 08-19, 08-21-1945, 09-19 | oemmat | **new FB-118** |
| 7 | **Augment slot wiped on every regen** — judgment rows re-authored by hand, up to ~10×/session | 08-19, 08-20, 09-19, 09-24-1745, 09-24-2256 | both | **new FB-119** |
| 8 | **The orchestrator is the unverified actor** — inline implementation skips implement-agent self-review; orchestrator-authored state annotations (verification-result.json, task notes) are never independently checked | 08-12, 08-19, 08-21-0642, 08-21-1945, 09-20, 09-21 | both | **new FB-120** |
| 9 | `dashboard-render.py` needs Python 3.12 but `scripts/README.md` says 3.10+ (verified: SyntaxError on 3.10.20 and 3.9.6) | 08-18, 08-21-1945 | oemmat | **new FB-121** (verified defect, below 3-incident bar) |
| 10 | Pause/verify bookkeeping inconsistencies: `work.md:749` timeout clause burns an attempt on an infra kill (conflicts with `work.md:944`); Session Export step 7 doesn't truncate `.pending-markers.jsonl` → markers re-imported and re-exported | 08-12, 08-21-1945 (+ styler 09-24-1745 ×5 cutoffs on pre-FB-103 5.0.0) | both | **new FB-122** (small bundle, FB-006 precedent) |

**Single-incident / not escalated** (recorded here, no FB): handoff 2.5KB bound → point overflow at auto-memory (08-21-0642, 09-20 — 2); friction-register dedup rule for one finding surfaced twice (08-20, 08-21-0642 — same FR-096, 2); drift reconciliation lacks an "absorb" option + no script for intended-drift fingerprint refresh (09-21, 09-24-2256 — 2); audit digest never learns a finding was fixed elsewhere (09-20); no template home for data-integrity audits (09-20); `notes` field polymorphic list/string + `validate-tasks.py` misses character-shredded lists (08-19); `test_protocol` dropped by post-verify persistence (08-12); `test_protocol` command steps lack a blast-radius flag before `[R] Run` (08-13-1443); merge-queue `current_text` needs an exactly-once uniqueness check (08-12); subagents don't inherit mid-session hazard memories (08-13-0916); DEC-NNN namespace collision between template docs and project records (08-13-0916); parallel batches contend on shared build dir `.next` (09-24-1745); MEMORY.md exceeded load limit silently (09-21); `persist-friction.py` returns `assigned_ids` as objects (09-24-2256); ledger doesn't model the external delivery surface (08-18); minified one-line dashboard HTML defeats grep (09-21).

**Positive signal (no action):** separate-context verification caught real defects in 10 of 13 sessions, including errors in orchestrator-authored work (08-21-0642, 08-21-1945); research-agent reframing a fork produced the option the user actually chose (08-12).

**Version skew:** styler is on template 5.0.0 (five minor versions behind). Its usage-limit-cutoff friction (09-24-1745) is covered by FB-103 (shipped v5.3.0).

---

## Proposed new entries

## FB-118: Needs-you mechanical derivation has four gaps — the human-gated coverage invariant is claimed but not enforced

**Status:** new
**Captured:** 2026-09-25
**Source:** harvest 2026-09-25, cluster 6 (oemmatinsightbi, 5 exports 08-13 → 09-19, template 5.4.0). Insight: `interaction-logs/insights/2026-09-25_dashboard_needs-you-derivation-gaps.md`

`rules/dashboard.md` says the script enforces every blocked-on-user case except paused-session questions. Four cases are not enforced:

1. **The both-owned review row can never render (verified).** `dashboard-render.py:1051` checks `owner == "both" and user_review_pending`, but it iterates `open_tasks`, which is defined at `:992` as `status != "Finished"`. `work-procedures.md:53` sets `user_review_pending` only together with `status: "Finished"`, so no task can match. The branch had never been exercised until task-065/066, which then never appeared in Needs-you.
2. **A claude-owned task with `user_review_pending` is invisible.** task-059 survived six sessions only because a hand-written augment row kept re-adding it.
3. **A Blocked `owner: both` task waiting on a user choice gets no row.** Example: task-080's A/B/C choice lived only in the augment slot, which the invariant says must never be an item's only home.
4. **`task_hash` omits `user_review_pending`** (`:358`). Clearing a review flag does not change the hash, so the freshness check misses exactly the staleness this card exists for.

**Fix sketch:** derive review rows from all non-absorbed tasks with `user_review_pending`, whatever the status or owner. Add a Blocked + `owner ∈ {both, human}` row. Add `user_review_pending` to the `task_hash` row tuple (a canonical-hash change, so bump and regen). Add unit tests for each case, since case 1 would have been caught by a one-line test.

## FB-119: Dashboard augment rows are destroyed on every regen — no persistence path for LLM-authored Needs-you content

**Status:** new
**Captured:** 2026-09-25
**Source:** harvest 2026-09-25, cluster 7 (5 exports, both projects). Insight: `interaction-logs/insights/2026-09-25_dashboard_augment-slot-persistence.md`

Every full regen rewrites the whole HTML, so `<!-- CLAUDE: augment -->` rows are lost and must be re-authored by hand: 2× (08-19), 4× (08-20), 4× (09-19), and about 10× (styler 09-24-2256, "re-extracted from the previous HTML and re-injected… error-prone, regex/anchor asserts needed"). A heredoc injection also hit an apostrophe-quoting bug (09-24-1745). This undercuts FB-105: the augment slot holds the one invariant case the script can't cover, which is also the case most likely to be lost.

**Fix sketch:** add a sidecar field (for example `dashboard-state.json::augment_rows[]`, holding text, optional task id, and created date) that the renderer reads and places in the slot, like `user_notes`. The orchestrator then writes to the sidecar instead of editing HTML. Rows tied to a task id could expire once that task is Finished and no longer flagged, so they don't go stale. This also removes the need for a card-HTML-from-file helper.

## FB-120: The orchestrator is the one unverified actor — inline implementation and orchestrator-authored state annotations bypass both self-review and verify-agent

**Status:** new
**Captured:** 2026-09-25
**Source:** harvest 2026-09-25, cluster 8 (6 exports, both projects). Insight: `interaction-logs/insights/2026-09-25_work_orchestrator-unverified-actor.md`

Two related shapes:

- **Inline implementation.** The orchestrator implements a task itself instead of dispatching implement-agent, which skips implement-agent's self-review and sweep discipline. task-070 then failed verification twice on the exact defect class that self-review targets (08-12). A routing change was labelled a "bug fix" without a before/after sweep and regressed a user-visible count from 5 to 0 (styler 09-21). One harness had a "don't call Agent unless asked" instruction, which forced ad-hoc judgment about which dispatches are load-bearing (08-19). A spec/audit-heavy inline session produced zero Track-1 markers (09-20).
- **Orchestrator-authored state.** The orchestrator wrote "The BUILD did not change" into `verification-result.json` without checking commits after the verification timestamp; 12 hours of commits had landed (08-21-0642, repeated 08-21-1945). It also made four annotation errors in one session: a hash matching no real state, a misread numstat, a wrong timezone offset, and an inherited false premise. Verify-agent caught these only because the work happened to be scoped as a task.

**Fix sketch (cheap first):** (a) state in `rules/agents.md` which dispatches are invariants (verify-agent: always) and which are efficiency defaults (implement-agent: inline is allowed for difficulty ≤ N, provided the orchestrator runs the same self-review/sweep checklist). (b) Require any annotation that argues a stale result is still valid to cite the git range it checked (`git log <verified_at>..HEAD -- <paths>`). Escalate to `/research` only if this recurs after (a) and (b).

## FB-121: `dashboard-render.py` requires Python 3.12 but the scripts contract says 3.10+

**Status:** new
**Captured:** 2026-09-25
**Source:** harvest 2026-09-25, cluster 9 (oemmatinsightbi 08-18, 08-21-1945). Verified 2026-09-25 by template-side `py_compile`.

`.claude/scripts/README.md:21` says "Python 3.10+ assumed". `dashboard-render.py` uses a backslash inside an f-string expression, which is only legal from Python 3.12 (PEP 701). It fails to compile on 3.10.20 with "f-string expression part cannot include a backslash" and on 3.9.6 as well. Every other `.claude/scripts/*.py` compiles on 3.10. Template settings allow a bare `python3 .claude/scripts/*.py`, and a stale shell snapshot resolves that to macOS 3.9.6. The resulting SyntaxError looks like a corrupt file, not a version problem.

**Fix:** hoist the backslash expressions out of the f-strings so the script meets the documented 3.10 floor, and add a `sys.version_info` guard at the top of each script with a clear message. Optionally, add a CI or unit test that compiles every script under the floor version. Patch-level.

## FB-122: Pause/verify bookkeeping — two small verified inconsistencies (bundle)

**Status:** new
**Captured:** 2026-09-25
**Source:** harvest 2026-09-25, cluster 10 (oemmatinsightbi 08-12, 08-21-1945). Both verified against current source.

(a) **The timeout clause conflicts with the interrupted-verifier rule.** `work.md:749` (and `work-procedures.md:56`) says: "If verify-agent exhausts `max_turns` without returning a valid report, treat as verification failure — increment `verification_attempts`, set Blocked". `work.md:944` says: "Do NOT increment `verification_attempts` if verify-agent was interrupted". A platform usage-limit kill after 4 tool calls matches the literal timeout clause and would burn one of three attempts on an outage. The 749 clause should exclude the FB-103 zero-token / infra-termination case explicitly.

(b) **`.pending-markers.jsonl` is not truncated at export.** `context-transitions.md:416` (Session Export step 7) deletes `.session-log.jsonl` and `.interaction-assessment.json` but leaves `.pending-markers.jsonl`. At the next session, Step 0d sees no session log, builds an empty dedup set, and re-imports every already-exported marker. The following pause then exports them again. Fix: truncate `.pending-markers.jsonl` in step 7.

---

## Proposed amendments to open items

Each amendment is appended as a dated `**Harvest 2026-09-25 evidence:**` paragraph at the end of the item. None changes the item's status or unlocks a gated mitigation.

- **FB-113** (+6 incidents, now **both projects**): prose docs that summarise a changed DAX/code pattern sit outside declared scope (08-13-0916, 08-20 schema-grain docs). Styler adds shared response types, reused helper signatures, new test files, and **`package.json` test-script wiring**, which touches nearly every task and therefore defeats the file-overlap parallelism heuristic unless it's exempted (09-21, 09-24-1745 ×2, 09-24-2256). A decomposition split a type-narrowing task from the task holding the consumer repair it forces (09-21). The "single-project" caveat no longer applies.
- **FB-114** (+4): `Grep` was unavailable to both subagents again (09-19 ×2), so the rule and the harness still disagree. New axis 4: **ripgrep honours `.gitignore`**, so repo-root absence probes silently skip gitignored `.claude/` state and user data. The rule should name `rg -uu` or explicit paths (09-21). Scope gap: the rule governs *findings* but not *sweeps*; mis-anchored sweep probes returned empty twice in one task (08-12). Fail-before-trust is suggested as an explicit rule: a new guard must be shown failing on the exact regression (09-21).
- **FB-115** (+4): the four-site "scope the sweep to what you edited" pattern in one session (08-12). New mechanism: **re-dating a section silently re-certifies every stale count beneath it**, turning an honestly stale claim into a falsely fresh one. This caused task-076's first verification failure (08-21-0642, 08-21-1945). Residue sweeps searched the three edited phrases and missed a synonym site (09-19). A related record-class issue: annotations about *live/external* state go stale silently (four instances in 08-21-1945).
- **FB-116** (+4, styler): the Empirical Evidence Gate was blocked twice when Playwright MCP was locked by the user's Chrome. There is no "verify PASS held pending evidence" or "not run" state (the schema is pass|fail only), so the report had to be parked in a workspace file (09-21, 09-24-1745). Unbounded `while` loops in `browser_evaluate` hung the MCP for 2+ minutes; bounded loops should be the documented pattern (09-24-2256). This does not meet FB-076 condition (a) for mitigations 2/3.
- **FB-117** (+3): new authoring-site shape. **Tasks whose only legal path is a user-typed `disable-model-invocation` command are effectively human-owned**: task-076 was `owner: both` but its entire deliverable routes through `/iterate` (08-21-0642), and task-081 was `owner: claude` for the same reason (08-21-1945, 09-19), making it unroutable by design. Only a handoff note prevented a doomed implement-agent dispatch. This is the FB-100 shape one layer up. Phase-level verifier follow-up tasks also shipped an AC that no implementation could meet (drillthrough reachability, 09-19) and carried no options for a design fork.
