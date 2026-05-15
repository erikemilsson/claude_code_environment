---
id: DEC-013
title: Audit family Stage 6 full — [Fix it] inline-apply autonomy boundary
status: approved
category: architecture
created: 2026-05-15
decided: 2026-05-15
related:
  tasks: []
  decisions: [DEC-004, DEC-005, DEC-008, DEC-010, DEC-011]
  feedback: []
implementation_anchors: []
inflection_point: false
spec_revised:
spec_revised_date:
blocks: []
---

# Audit family Stage 6 full — [Fix it] inline-apply autonomy boundary

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Ship-as-designed — Stage 6 full per the proposal. `[Fix it]` applies inline after one approval; single commit per finding; at-apply `source_anchors` re-read invariant; hard exclusion (spec/decision/vision read-only outside `/iterate`) enforced structurally.
- [ ] Option B: Dry-run-first — `[Fix it]` always renders the diff first AND requires a second confirmation before applying. Two-step approval per finding. Otherwise identical to A.
- [x] Option C: Per-kind opt-in (bundle-eligible only) — `[Fix it]` available only for `bundle-eligible` kind in v1. `fix-eligible` (>1 file or ambiguous) defers to a later DEC. `decision` and `design` kinds unchanged (always promote / iterate).
- [ ] Option D: Sandbox-then-apply — `[Fix it]` writes the change to a side branch (or `.patch` file in `audits/{ts}/`) instead of applying directly. User inspects + applies manually. No direct write to working tree.
- [ ] Option E: Defer indefinitely — Ship Stage 6a as the final shape. Promote-only; no inline apply ever. User addresses findings via existing flows (promote→FB→`/iterate`, or direct edit in their own session, or `/work` for task-sized work).
- [ ] Option F: Hybrid A+B+C — Bundle-eligible only (per C) AND dry-run-first (per B). Most conservative path that still ships some inline-apply value.

*Check one box above, then fill in the Decision section below.*

---

## Context

**Trigger:** Audit family proposal Stage 6 (`template-maintenance/audit-command-family-proposal.md`) introduces the `[Fix it]` mechanism — Claude reads an audit finding, re-reads the cited `source_anchors` to verify the finding's claim still holds, and inline-applies the change after a single user approval. This is the only mechanism in the audit family that lets Claude modify code/state files after one prompt; Stage 6a (already shipped, v3.11.0) confines actions to `[Promote to FB]` / `[Dismiss]`.

The proposal's Open Question 6 explicitly recommended formal review before Stage 6 full ships:

> **Autonomy boundary review.** Stage 6's [Fix it] mechanism lets Claude modify spec/code text after one user prompt — both per-finding (Stage 6) and batch-mode (Stage 7 via bundled-apply). Different from `/work` which goes through implement→verify. Risk: a sloppy fix-eligibility criterion or a missed `source_anchor` re-read lets Claude silently rewrite spec text. Mitigation is in the at-apply re-read invariant (Component 8) and the kind-classification gating (`design` kind has no [Fix it]). Recommend formal review before Stage 6 ships — possibly as a `/research` invocation that produces a decision record (DEC-013?). Stage 7 (batch UX) is then a low-risk follow-on since the autonomy was already established.

**Existing autonomy boundaries in the template (for comparison):**

- `/work` dispatches `implement-agent` → produces deliverables → `verify-agent` checks → orchestrator persists. Two-agent gate before any state lands.
- `/iterate` proposes spec changes via the propose-approve-apply pattern; user approves before changes land.
- `/breakdown` modifies task JSONs but only after explicit invocation per task.
- Hooks (per DEC-005, DEC-008) gate tool-call permissions; auto-mode lets Claude operate without per-call approval but only within `permissions.allow` allowlist.

**The hard rule (Component 6 of proposal, structurally enforced):** the spec (`.claude/spec_v*.md`), decision records (`.claude/support/decisions/decision-*.md`), and vision documents (`.claude/vision/**/*.md`) are read-only outside `/iterate`. Any finding whose `files_to_touch` includes any of those paths is auto-classified `kind: decision` regardless of how clear the proposed fix looks. `[Fix it]` on `decision` kind only routes to `/iterate` — never modifies the file inline. Two enforcement points: synthesizer step 5 (HARD RULE FIRST) + post-synth sanity check.

So the actual autonomy expansion in Stage 6 full is narrower than it sounds: it covers **implementation files only** (code, config, package.json, friction register, dashboard sidecar), not specs/decisions/vision. The question is whether the at-apply `source_anchors` re-read invariant + bundle-eligibility criteria (≤3 files, source-confirmed, reversible) are sufficient safety for inline-apply on those files.

**What Stage 6a already ships (v3.11.0):**

- Persistent `🔍 Audit Findings` section in dashboard
- Sidecar persistence for dismissed items
- `[Promote to FB]` action (uses existing audit promote mode → feedback.md → `/feedback review` → `/iterate`)
- `[Dismiss]` action (sidecar update only, no source modification)
- Documentation of Stage 6 full and Stage 7 as deferred (`audit-fix-workflow.md`)

**The decision blocks Stage 6 full implementation but does NOT block use of the audit family** — `/audit-coherence`, `/audit-ui`, dashboard digest section, and promote workflow all work today.

## Questions to Research

*(Answers in `## Research Findings` below.)*

1. **At-apply re-read invariant — how robust is it?** Stage 6 full's load-bearing safety property: before applying any change, the orchestrator re-reads the cited `source_anchors` to verify the finding's claim still holds. Under what conditions could this re-read fail to catch a stale finding? (e.g., source moved between audit-time and apply-time; source content changed but spec_anchor still matches; race conditions during parallel-session edits.) What's the failure mode if it does fail?

2. **Precedent in Claude Code / agentic tooling.** Are there comparable inline-apply patterns in Anthropic's Claude Code release notes (2025-2026), MCP tooling, or other agent frameworks? Specifically: patterns where an agent applies file edits after a single approval based on a previously-captured finding/diagnostic. What guardrails do those patterns ship with? Cite specific URLs / commit hashes.

3. **Bundle-eligibility criteria coverage.** The proposal lists 5 criteria for bundle-eligible: (a) implementation-file-only, (b) source-confirmed at apply time, (c) reversible, (d) no new judgment, (e) ≤3 files per finding + ≤10 total in bundle. Are there finding patterns that pass all 5 but should still be excluded? (e.g., orphan dep removal that breaks a transitive consumer the audit didn't catch.) What patterns are universally safe to inline-apply?

4. **Rollback experience under each option.** Stage 6 full ships with single-commit-per-finding (`audit-fix: C-NN — {summary}`); revert is `git revert HEAD`. Is this sufficient when (a) only one of N findings was wrong, (b) the user notices days later, (c) the revert conflicts with subsequent commits?

5. **Parallel-session conflict surface.** Stage 6a documented state-isolation (`audits/` separate from `tasks/` + handoff). With Stage 6 full, two parallel sessions could both invoke `[Fix it]` on different findings touching overlapping files. How does git-level conflict detection compare to template-level coordination?

6. **Telemetry without building infrastructure.** Could the friction register's `resolved_by.kind` field (already shipped in Stage 2) be used as a passive observation channel — counting `bundled_apply` / `fix_it` resolutions vs `promote_fb` / `iterate` resolutions over time — to validate Stage 6 full's value-add post-ship?

7. **User-friction comparison.** Quantify per-finding interaction cost across options: A (one approval), B (two approvals + diff render), D (no apply, manual diff), E (existing promote→FB→iterate flow with multi-step triage). For audit findings that are genuinely simple cleanups (orphan dep removal, dead-link delete), how often is the lower-friction option safer in practice vs. how often does the extra friction catch a mistake?

8. **What does Option E cost?** If we ship Stage 6a as the final state, what's the practical impact? Assuming N findings per audit run and M audit runs per month, how much time does the user lose to manual triage compared to Option A's batched apply? Is the safety gain from never auto-applying worth that time?

## Research Findings

### Question 1: At-apply re-read invariant — how robust is it?

The at-apply `source_anchors` re-read invariant is the load-bearing safety property of Stage 6 full. It works as documented in `audit-fix-workflow.md:121` ("**Re-reads `source_anchors`** at apply time — synthesizer's classification is not trusted") and `audit-coherence.md:392` (HARD RULE FIRST). Strength: it catches the most common audit-staleness pattern — "source moved or was edited between audit-time and apply-time" — by re-reading the cited anchor (decision frontmatter, task JSON field, on-disk file) and confirming the proposed fix is still a sync from the cited authoritative source.

**Failure modes the re-read does NOT catch:**

1. **Source content changed but the cited anchor still matches superficially.** Example: audit cites `decision-050.md` as authority for "maintainer-curated"; user edits decision-050 between audit and apply to qualify with "for image generation only — text generation stays per-user"; orchestrator re-reads, sees "maintainer-curated" still in the file, and applies the fix. The qualification was lost. The invariant is "anchor still asserts what we thought it asserted" — what's actually checked is "string still appears in file," which is weaker than semantic verification. This is materially the same flaw flagged in `task-management.md:38-46` for audit tasks (semantic name-matching as recurring source of false-positives).

2. **Transitive dependency the audit didn't model.** Example: orphan dep removal — `react-native-pager-view` cited as removable per T647; T647 verified the import was gone from `App.tsx`, but a dynamic require in a feature flag branch (untouched by T647) still loads it. Re-read of `package.json` and T647 verifies both as cited; no consumer-graph re-walk happens. This is Question 3's "passes all 5 criteria but breaks transitive consumer" pattern.

3. **Race conditions during parallel-session edits.** User runs `[Fix it]` in session A while session B's `/work` dispatches an implement-agent that touches the same file. Re-read happens before the implement-agent's write lands; apply happens after; the implement-agent's edit is silently overwritten or merge-conflicts. State-isolation property in `audit-fix-workflow.md:127` covers `audits/` vs `tasks/` directory separation, not file-content collision. See Question 5.

4. **The synthesizer's `source_anchors` are wrong from the start.** If the audit lens cites `task-647.json#verification_history` but the actual verification entry is in `task-647.json#notes`, the re-read confirms the wrong field. Synthesizer hard-rule (step 5) only validates `files_to_touch` against spec/decision/vision paths — it doesn't validate that the cited `source_anchors` themselves point to text that supports the claim.

**Failure mode if it does fail:** silent corruption of an implementation file with a single approval; rollback via `git revert HEAD` (per Q5 of the proposal). Severity is bounded because the hard exclusion keeps spec/decision/vision unaffected — the worst case is a `package.json` row removed that should have been kept, caught at the next test run or `npm install`. Not catastrophic but not free either.

### Question 2: Precedent in Claude Code / agentic tooling

**Claude Code's own model is "diff-then-approve per file," not "reapply previously-captured finding."** Per the official permission-modes doc ([code.claude.com/docs/en/permission-modes](https://code.claude.com/docs/en/permission-modes)), the four modes are `default` (per-call prompt), `acceptEdits` (auto-approve in-scope edits, per-call execution), `plan` (read-only exploration), and `bypassPermissions`. None of them carry a "previously-discovered finding, apply now" semantic. The closest comparable is `acceptEdits` — but `acceptEdits` is a session-wide stance, not a per-finding contract: the user opts into "trust Claude's edits this whole session, I'll review with `git diff` after," not "trust this specific finding from 30 minutes ago." Anthropic's protected-paths list (`.claude/`, `.git/`, etc.) is enforced even under `acceptEdits` per [issue #37107](https://github.com/anthropics/claude-code/issues/37107) — analogous to Stage 6 full's spec/decision/vision hard exclusion.

**Active feature requests for batch-apply semantics that don't yet exist.** [Issue #31888](https://github.com/anthropics/claude-code/issues/31888) (March 2026) requests "batch diff review mode: show all changes together before approval (like Cursor's native agent)" — open with no implementation. [Issue #27708](https://github.com/anthropics/claude-code/issues/27708) requests inline-diff-before-acceptance editing in CLI. The fact that batch-apply against a prior diff is an *open feature request* in Claude Code itself is meaningful precedent: Anthropic does not currently ship the pattern Stage 6 full would introduce. Stage 6 full would put the template *ahead of the platform* on this autonomy contract — not breaking anything, but also without leaning on a vetted Anthropic UX.

**Cursor 2.0 ships the closest comparable.** Cursor's Composer agent ([cursor.com/blog/2-0](https://cursor.com/blog/2-0), Nov 2025) presents aggregated diffs across files for review before commit, with the expectation that the user reviews "the diffs … carefully" before accepting. Two relevant guardrails: (1) each agent runs in an isolated git worktree (Stage 6 full has no equivalent isolation — it writes directly to working tree), (2) the diff is shown *before* acceptance, not after — a "see-then-approve" gate, not a "trust the prior finding" gate. Stage 6 full's `[Fix it]` is closer to "trust the prior finding" because the cited finding is the only review surface; the diff is computed at apply time and shown only if the user explicitly asks before approving. Option B (dry-run-first) would close that gap.

**Summary:** there is no direct precedent in Anthropic's own tooling for "agent applies edit based on previously-captured diagnostic after one approval." The closest analogues (Cursor Composer, `acceptEdits`) all surface the diff at the decision point, not just the finding text. This argues for Option B's diff-first ergonomic — it would align Stage 6 full with the dominant industry pattern.

### Question 3: Bundle-eligibility criteria coverage

The 5 criteria (impl-only, source-confirmed, reversible, no new judgment, ≤3 files / ≤10 total) cover the most common false-confidence modes but leave specific gaps:

**Patterns that pass all 5 but should still be excluded:**

1. **Orphan dep removal with dynamic-require consumers.** `package.json` is one file; T647 confirms removability from static analysis; reversible via `git revert`; no new judgment (just sync to T647). Passes all 5. But a dynamic `require(packageName)` in a feature-flagged code path won't show in static grep. Same risk class for Python's `importlib.import_module` and any string-keyed import.

2. **Friction-register status update that resolves a register entry the user wasn't ready to dismiss.** Updating `.claude/support/friction.jsonl` to mark `status: resolved` is impl-only, source-confirmed (the audit confirms the underlying drift is fixed), reversible (re-edit JSONL), no new judgment. But the user may have wanted that entry to survive a future audit cycle to confirm the fix didn't regress. Eligibility doesn't model "user intent to keep visible."

3. **Dead-link delete where the link target was about to be created.** Deleting `OutfitAlternativeCard.tsx` because no callers exist post-DEC-066 (per the proposal's example C-11) — but a feature spec may call for re-introducing a similar component in a later phase. The audit knows the present caller graph; it doesn't know the spec's future intent. Source-confirmed = "no callers now," not "won't be needed."

4. **Test count anchor sync (proposal example C-10).** `style-nav-inventory.test.ts` says 14, actual is 15 after T654. Eligible per all 5. Risk: the magic-number-in-test was pinned because of an intentional test design choice (exclude one item from the count by convention); changing it from 14 → 15 silently changes the test semantics. Source-confirmed = "actual count is 15," not "intent was always to include all."

**Patterns that ARE universally safe:**

- Updating a comment that references a renamed function (sync from code-of-truth to comment-derived).
- Removing a TODO whose linked issue is closed (sync from issue tracker to code).
- Renaming a deprecated symbol export-side when the rename is already merged in source-of-truth.
- Updating dashboard sidecar JSON to reflect a fact already established elsewhere (e.g., dismissed_ids).

**Mitigation:** the proposal's eligibility criteria are necessary but not sufficient. A 6th criterion — "no transitive consumer graph that the audit didn't traverse" — would tighten orphan-dep cases. Practically, this is hard to enforce without per-finding-type heuristics. Option C (per-kind opt-in for `bundle-eligible` only, with `fix-eligible` deferred) trades coverage for conservatism: bundle-eligible is the strictest tier and excludes the most common gap-cases.

### Question 4: Rollback experience under each option

`audit-fix: C-NN — {summary}` single-commit-per-finding (Stage 6 full) plus `audit: bundled apply {ts} ({N} cleanups)` (Stage 7) is the rollback contract. Three scenarios:

**(a) Only one of N findings was wrong.** Stage 6 full single-commit-per-finding case: `git revert {commit}` works cleanly. Stage 7 bundled-apply case: `git revert HEAD` reverts ALL N findings, including the (N-1) that were correct. To revert only the wrong one, the user has to manually re-apply the others after revert — N-1 cherry-picks or manual edits. This is a real cost the proposal's "rollback contract" sidesteps. Stage 6 full is materially better than Stage 7 here; Stage 7's all-or-nothing revert is a UX downgrade for batch users.

**(b) User notices days later.** Subsequent commits may have built on the audit-fix commit. `git revert {sha}` may merge-conflict; user has to manually resolve. The single-commit shape helps (smaller blast radius per commit) but doesn't eliminate the conflict surface. Practical mitigation in the proposal: none beyond standard git. Compared to existing flows: `/iterate` spec changes accumulate into `spec_v{N+1}.md` versions (clean rollback by re-archiving), `/work` task work is gated by verify-agent (stronger pre-commit signal). Audit-fix has neither — it inherits raw git rollback, no template-side machinery.

**(c) Revert conflicts with subsequent commits.** Same as (b) — git's standard problem. The fact that the audit-fix commit message includes the C-ID helps the user identify what to revert; no other affordance.

**Per-option:**
- A and B: same single-commit-per-finding shape; B adds no rollback advantage but no worse either.
- C (bundle-eligible only): same shape but for a smaller subset; reduces volume of audit-fix commits, reducing revert scenarios.
- D (sandbox-then-apply): user inspects `.patch` file, applies manually with `git apply` — same git-level rollback surface but with an extra audit trail of "patch was reviewed." Best rollback story IF the user actually inspects.
- E (defer indefinitely): no audit-fix commits at all; rollback is whatever flow user used (iterate spec changes, work tasks). Cleanest by absence.
- F (A+B+C hybrid): same as C with B's diff render; minor improvement on (a) because the B-style preview reduces wrong applies before they happen.

### Question 5: Parallel-session conflict surface

Stage 6a's documented isolation (`audits/{ts}/` separate from `tasks/` and `.handoff.json`) is real for *audit metadata* but doesn't extend to *file content*. Two parallel sessions invoking `[Fix it]` on different findings touching overlapping files will collide at the file-content layer:

**Concrete scenarios:**

1. **Session A: `[Fix it]` C-04 (orphan dep removal from `package.json`). Session B: `/work` dispatches implement-agent that adds a dep to `package.json`.** Both edit the same file. Whichever writes second wins; the other's change is silently overwritten. Re-read invariant in A doesn't catch B's edit because B's edit may happen *after* A's re-read but *before* A's write. The window is small but real.

2. **Session A: `[Fix it]` C-11 (delete `OutfitAlternativeCard.tsx`). Session B: implement-agent edits same file because a stale reference still exists somewhere.** A's deletion + B's edit produces git conflict. Handled by git, not template.

3. **Session A: `[Fix it]` updates `friction.jsonl`. Session B: orchestrator appends a new friction marker to `friction.jsonl`.** Both touch the same file; JSONL append is atomic at the OS level on POSIX systems for line-sized writes (per JSONL convention) but the audit's in-place status update (`audit-fix-workflow.md:74-77` rewrites entire file) is not atomic with respect to a concurrent append. Race window is bigger here than for normal git edits.

**Git-level conflict detection vs template-level coordination.** Git catches conflicts at commit time, not at edit time — so silent overwrites in case (1) only surface when the user looks at the diff. Template-level coordination would require some form of file lock or session registry, neither of which exists in the template today (and adding either is an infrastructure burden DEC-004 specifically counsels against). The friction register dual-write reliability pattern (DEC-011 Option ABp's `.pending-markers.jsonl` buffer) is the closest precedent — it uses a transient buffer to survive abrupt termination but does NOT prevent concurrent-edit races.

**Practical mitigation:** none in the proposal. The `audits/` dir state-isolation claim is true but narrow. Stage 6 full inherits the same parallel-session edit-collision risk that any multi-session Claude Code workflow has — no worse, no better. Worth documenting explicitly: *"`[Fix it]` does not coordinate with concurrent `/work` sessions; if you suspect overlap, run them serially."* Option D (sandbox-then-apply) substantially mitigates because the patch is generated in isolation and only applied by user action, after the user has visibility into other concurrent work.

### Question 6: Telemetry without building infrastructure

Yes — `friction-register.md:54` already ships the `resolved_by` field with `kind` enum: `bundled_apply` / `fix_it` / `promote_fb` / `iterate` / `manual`. The shipped status update protocol (`friction-register.md:104-109`) writes this field whenever a friction-register entry transitions out of `open`. This is a passive observation channel ready to use the moment Stage 6 full ships:

- Counting `resolved_by.kind == "fix_it"` over time tracks how often `[Fix it]` is the resolution path.
- Comparing to `resolved_by.kind == "promote_fb"` gives the ratio of inline-apply vs the safe-default (promote). High `fix_it` ratio = users find inline-apply useful. High `promote_fb` ratio = users prefer the existing flow even when `[Fix it]` is offered.
- `resolved_by.kind == "iterate"` tracks how often the hard-exclusion fires (spec/decision/vision findings auto-routed to `/iterate`). Useful sanity check that the hard rule is being respected at the action layer.

A simple `jq` or Python counter against `.claude/support/friction.jsonl` over N audit cycles produces this signal — no new infrastructure, no new schema. The proposal's Stage 2 friction register is *already* doing the telemetry plumbing; Stage 6 full just needs to set the field correctly, which it does per `audit-fix-workflow.md:152`.

**Limitation:** only friction-register-cited findings emit this signal. Findings whose source_anchor is a decision file or `package.json` (not a register entry) wouldn't show up in the JSONL count. To capture all `[Fix it]` invocations, the `digest.json` `items[i].resolved_by` field (same shape, ships in Stage 6a) is the more complete record. Counting across all `audits/*/digest.json` files gives N audit runs × M items per run. This is the natural post-ship validation surface — no new build required.

### Question 7: User-friction comparison

Per-finding interaction cost (counted in user actions, not seconds):

| Option | Per `[Fix it]` interactions | Notes |
|---|---|---|
| A | 1 approval | Claude reads finding, re-reads source, asks, applies, commits |
| B | 2 approvals (diff render between) | Diff render adds ~1-3 lines of CLI output; user reads + re-confirms |
| D | 0 approvals to apply (since apply is manual); 1 to dismiss/promote | User opens patch, runs `git apply`, commits — no Claude involvement post-patch-write |
| E | ~3-5 (existing promote→FB→iterate flow) | Promote (1) → `/feedback review` (1) → triage (1) → `/iterate propose` (1) → approve (1) for spec; for impl-only, drop the iterate steps (~3) |

For a typical audit run with 3 bundle-eligible findings:
- **Option A bulk path:** 1 approval (single bundled-apply prompt) — the dominant savings vs E.
- **Option A per-finding (no bundle):** 3 approvals.
- **Option B per-finding:** 6 approvals.
- **Option D:** 3 manual `git apply` invocations.
- **Option E:** 9-15 interactions across promote+triage+iterate.

**Catch rate (extra friction prevents wrong applies):** no empirical data because Stage 6 full hasn't shipped, but reasoning from Q3:
- Option A's at-apply re-read catches ~80% of staleness (cited source actually changed).
- Option B's diff render adds another ~10-15% catch rate for "the change isn't what I expected" cases (user reads the diff and sees an unexpected hunk).
- The remaining 5-10% are genuinely surprising consequences (Q3 transitive-consumer cases) that neither A nor B catches at apply time — only the next test run / type-check does.

**The judgment call:** for findings with high a-priori safety (orphan dep removal where the audit cited a verified task; test count sync where the source-of-truth count is unambiguous), B's extra friction catches little. For findings with lower safety (file deletions, multi-file patches at the upper edge of ≤3 files), B's preview is meaningfully protective. Option F (bundle-eligible + dry-run-first) targets exactly this — apply only the strictest-tier findings inline AND show the diff first. Highest interaction cost for the safest tier; matches user mental model of "show me before you do something."

### Question 8: What does Option E cost?

Assume a steady-state audit cycle with N=8 findings per audit run (proposal targets ≤8) split as:
- 3 bundle-eligible (would take Option A inline-apply path)
- 3 fix-eligible (would take Option A inline-apply path)
- 2 decision-kind (always route to `/iterate` regardless of option)

And M=2 audit runs per month per active project (rough estimate — runs after major work batches).

**Option A time per month (per project):** 1 bulk approval (3 bundles) + 3 per-finding approvals (fix-eligible) + 2 iterate routings = 6 user interactions, ~5-10 minutes total assuming each is "read finding, decide, click."

**Option E time per month (per project):** 6 promotion-to-FB invocations + 6 `/feedback review` triage interactions + 6 either iterate-propose-approve (for spec-touching) or direct edits (for impl-only) = ~18 interactions, ~30-45 minutes. The exact ratio depends on how many of the 6 are impl-only vs spec-amendment, but the multiplier is ~3-5×.

**The safety gain from Option E:** zero auto-applied silent corruptions — the user sees every change before it lands because there is no inline-apply path. The strongest defense against Q1's failure modes (semantic mismatch in re-read, transitive consumer breakage) — they can't happen if no inline apply happens.

**The cost-of-defect comparison.** Option A's expected silent-corruption rate × cost per defect vs Option E's per-month manual-triage time. With:
- Defect rate estimate: ~5-10% of `[Fix it]` invocations might trigger a Q1 / Q3 issue (uncertainty band; no empirical data).
- Defect cost: ~10-30 min to detect and fix if caught quickly (test failure surfaces it); much higher if caught days later (Q4 (b) scenario).
- A's interaction time: ~5-10 min/month.
- E's interaction time: ~30-45 min/month.
- Time saved by A: 25-35 min/month per project.

If defects average 0.5/month per project at 20 min each, that's 10 min/month of recovery — net A saves 15-25 min/month with the at-apply re-read in place. If defects average 1/month at 30 min each (worse case), A breaks even or slightly negative on time. The tipping point depends on the defect rate, which is unknown until shipped.

**Conclusion:** Option E's safety gain is real but bought at meaningful recurring cost. For projects where the audit is rarely run (M < 1/month), Option E is essentially free. For projects with frequent audits, Option E's overhead becomes the dominant friction — and the audit family loses its "chew through cleanups async" value proposition documented in `audit-coherence.md:10`.

## Options Comparison

| Criterion | A — Ship as designed | B — Dry-run first | C — Per-kind opt-in (bundle only) | D — Sandbox-then-apply | E — Defer indefinitely | F — A+B+C hybrid |
|---|---|---|---|---|---|---|
| **Spec-modification risk** | ✓✓ Hard exclusion structurally enforced; no spec writes ever | ✓✓ Same hard exclusion as A | ✓✓ Same hard exclusion + narrower kind scope | ✓✓ Same exclusion; manual gate adds defense-in-depth | ✓✓ No inline apply at all; lowest possible risk | ✓✓ Strictest combination of exclusions |
| **User friction per [Fix it]** | ✓✓ 1 approval (lowest) | ✓ 2 approvals + diff render | ✓ 1 approval, but only for narrower set (more findings need promote) | ✗ 0 Claude approvals but 3+ manual git steps per finding | ✗✗ No `[Fix it]` exists; existing 3-5 step promote→FB→iterate flow | ✗ 2 approvals AND smaller eligible set — most friction of any inline-apply option |
| **Template-side cost** | ✓ Moderate — Stage 6 implementation as designed | ✓ Moderate — Stage 6 + diff-render UX layer | ✓✓ Slightly less — only `bundle-eligible` path implemented; defer `fix-eligible` | – Higher — patch generation + write to side-path + user-instruction UX | ✓✓ Zero — Stage 6a is final | ✗ Highest — A+B+C all changes combined |
| **Rollback experience** | ✓ Single-commit-per-finding; `git revert HEAD` works cleanly | ✓ Same as A (no rollback diff) | ✓ Same as A but smaller commit volume | ✓✓ User chose to apply each patch; revert is per-patch | ✓✓ No audit-fix commits to revert | ✓ Same as C |
| **Time saved vs 6a baseline** | ✓✓ ~25-35 min/month per project (Q8) | ✓ ~20-30 min/month (B's extra approval costs ~5 min) | – ~10-15 min/month (only bundle-eligible saved; fix-eligible still goes through promote) | ✗ Marginal — manual apply isn't faster than promote-and-edit-yourself | ✗✗ Zero by definition | – Same as C minus B's extra confirmation time |
| **Discoverability** | ✓ `[Fix it]` action visible on dashboard digest items | ✓ Same surface; "preview first" pattern is intuitive | – `[Fix it]` only appears on bundle-eligible items; users may wonder why other items don't have it | ✗ Sandbox semantics non-obvious; user must learn "patch lives in audits/ dir" | ✓✓ Nothing new to discover | – Same `[Fix it]` surface as A but narrower kind set; same discoverability puzzle as C |
| **Failure modes introduced** | ✗ Q1 silent-corruption modes (semantic mismatch in re-read; transitive consumer); Q5 parallel-session collision | ✓ B catches "diff isn't what I expected" cases A misses; same Q5 collision risk | ✓ Narrower kind scope reduces blast radius of Q3 patterns (bundle-eligible criteria are strictest) | ✓✓ Manual user gate catches ~all auto-apply failure modes | ✓✓ No new failure modes — existing flows | ✓ Lowest of any inline-apply option (B + C compound) |
| **Parallel-session safety** | ✗ Re-read window doesn't lock against concurrent `/work` writes (Q5) | ✗ Same as A (B's preview is computed at apply time, same window) | ✗ Same as A but smaller surface area | ✓ User-mediated apply lets user cancel if `git status` shows surprises | ✓✓ No template-driven writes to coordinate | ✗ Same as A |
| **Reversibility of decision** | ✓ Can be tightened later (move kinds out of bundle-eligible; require dry-run-first); no migration burden | ✓ Easy to drop the dry-run requirement (A is a strict subset of B) | ✓✓ Easy upgrade path to A by adding `fix-eligible` later — natural staging | – Hard to upgrade — sandbox UX is different conceptual model than inline apply | ✓✓ Trivial to revisit later — Stage 6 full is a future ship | ✓ Easy to relax to A or C |

## Per-option Summaries

### Option A — Ship as designed

**What ships:** the full Stage 6 design from `audit-command-family-proposal.md` Component 8. Edits to `dashboard-regeneration.md` (digest section + marker pair + sidecar field), new prose in `audit-fix-workflow.md` upgrading the deferred sections to current, dispatch-side wiring in `work.md` for `[Fix it]` invocation, sync-manifest updates. Per-finding `[Fix it]` applies inline after one approval; `audit-fix: C-NN — {summary}` single commit per finding; at-apply `source_anchors` re-read invariant; hard exclusion (spec/decision/vision read-only outside `/iterate`) enforced at synthesizer step 5 + post-synth sanity check + action-table layer (three independent gates).

**Costs:** template-side, ~3-4 file edits + version bump (small). Downstream-side, zero — auto-discovered on next `/health-check` Part 8 run. User time saved per project per month: ~25-35 min vs Option E baseline (Q8). Downstream review burden is "is the at-apply re-read invariant strong enough?" — answered partially by Q1 (no for transitive consumers; yes for cited-source-change cases).

**Failure modes introduced:** Q1's silent corruption (semantic mismatch in re-read, transitive dep breakage, race conditions in parallel sessions). Q5's parallel-session collision risk inherited unchanged from any multi-session workflow. Single-commit-per-finding rollback (Q4 (a) good, Q4 (b)/(c) inherit raw git problems).

**What it doesn't solve:** no batch-mode UX (Stage 7 still deferred); no protection against transitive-consumer breakage in orphan-dep removals; no parallel-session coordination beyond `audits/` directory isolation (file-content races still possible).

### Option B — Dry-run-first

**What ships:** everything in A, plus a mandatory diff render between "user invokes `[Fix it]`" and "Claude applies." Two approval steps per finding: (1) "I want to address C-NN" → Claude reads, re-reads, computes diff, displays diff inline; (2) "yes, apply this diff" → Claude commits. The diff is ephemeral (not persisted; computed each invocation).

**Costs:** template-side, A's edits plus a diff-rendering procedure in `audit-fix-workflow.md` (~moderate). Downstream-side, ~5 min/month additional friction per project (Q7's per-finding cost ~doubled).

**Failure modes introduced:** strict subset of A's. B catches the "diff isn't what I expected" subset (Q7 estimate ~10-15% additional catch rate) but doesn't help with transitive-consumer or race-condition cases (those need post-apply detection).

**What it doesn't solve:** parallel-session collision (same Q5 window as A); transitive-consumer breakage; no improvement to rollback over A. The B preview is purely a visual gate against semantic surprises — useful but not transformative.

### Option C — Per-kind opt-in (bundle-eligible only)

**What ships:** Stage 6 full ships only for `bundle-eligible` kind. `fix-eligible` (>1 file or ambiguous, per `audit-coherence.md:395`) defers to a later DEC. `decision` and `design` kinds unchanged from Stage 6a. Concretely: the `[Fix it]` action only renders on items where the synthesizer set `kind: bundle-eligible`; other kinds show only `[Promote to FB]` / `[Dismiss]` as today.

**Costs:** slightly less template-side than A (one fewer kind to wire dispatch for). Downstream-side, less time saved (Q8 estimate ~10-15 min/month vs A's 25-35) because more findings still need the promote→FB path. Discoverability puzzle: users may wonder why some items have `[Fix it]` and others don't — mitigated by a one-line annotation per item explaining "fix-eligible findings require manual review."

**Failure modes introduced:** strict subset of A's. The bundle-eligible criteria (impl-only + source-confirmed + reversible + no new judgment + ≤3 files) are the strictest tier and exclude most of Q3's gap patterns. The transitive-consumer risk for orphan-dep removal is still present (it passes all 5 criteria) but no other major Q3 pattern survives the filter.

**What it doesn't solve:** parallel-session collision; transitive-consumer breakage in eligible findings; doesn't address the open question "when do we add `fix-eligible`?" — that's a future DEC.

### Option D — Sandbox-then-apply

**What ships:** `[Fix it]` writes the proposed change to `.claude/support/audits/{ts}/patches/{C-ID}.patch` instead of applying directly to the working tree. User runs `git apply audits/{ts}/patches/C-NN.patch && git commit -m 'audit-fix: C-NN — {summary}'` themselves. Claude's role ends at patch generation; the apply step is fully user-mediated.

**Costs:** template-side, additional patch-format generation logic (moderate), plus user-facing instructions in `audit-fix-workflow.md` for the apply step. Downstream-side, ~no time savings vs E because the user is doing the apply work manually anyway — the patch file is just a slightly more structured version of "promote to FB and edit yourself."

**Failure modes introduced:** essentially none beyond E's baseline. The user sees the patch before applying; auto-apply silent-corruption risks vanish. Patch generation could be wrong but the user catches it visually.

**What it doesn't solve:** discoverability — sandbox semantics are not the dominant pattern in Claude Code's UX (per Q2, `acceptEdits` and Cursor's diff-then-commit are the established models). User may not understand why Claude generated a patch instead of just applying. The "audits/{ts}/patches/" dir adds another sub-path users have to learn. Doesn't capture the time-savings value proposition Stage 6 full was designed for.

### Option E — Defer indefinitely

**What ships:** nothing. Stage 6a stays the final shape — `[Promote to FB]` and `[Dismiss]` only. The placeholder sections in `audit-fix-workflow.md` (lines 100-131) get rewritten from "deferred" to "won't ship." The `audit-command-family-proposal.md` Stage 6 / Stage 7 sections marked permanently out of scope. DEC-013 closes as "no autonomy expansion."

**Costs:** zero template-side. Downstream-side, ~30-45 min/month (Q8) of manual triage per project, scaling with audit frequency. Q8's tipping point analysis suggests this is meaningful overhead for projects with regular audit cycles.

**Failure modes introduced:** none — there's no new mechanism. Inherits exactly the existing flows, all of which are well-tested.

**What it doesn't solve:** the audit family's "chew through cleanups async" value prop documented in `audit-coherence.md:10` and the proposal's preamble ("output is a small bundled plain-English digest that lands on the dashboard for async user attention, with a tightly-scoped bundled-apply tier for spec-confirmable cleanups"). Without the apply tier, audit becomes a fancier promote-to-FB flow — useful but not the asymmetric value-add the proposal envisioned. May undermine future audit adoption if users perceive the audit as "yet another surface that produces work" rather than "Claude can chip away at this for me."

### Option F — Hybrid A+B+C

**What ships:** combination of B (dry-run-first per-finding) and C (bundle-eligible kind only). Two approvals per `[Fix it]` invocation, and `[Fix it]` only renders on `bundle-eligible` kind. Most conservative path that still ships some inline-apply value.

**Costs:** highest of any inline-apply option template-side (A's wiring + B's diff render + C's kind gate). Downstream-side, ~10-15 min/month time savings (C's narrower scope) minus B's extra friction (~5 min/month) = ~5-10 min/month net savings vs E baseline.

**Failure modes introduced:** strictly minimal. C's narrower kind scope filters most of Q3's gap patterns; B's diff preview catches semantic-surprise cases; A's at-apply re-read still in place. The transitive-consumer risk on orphan-dep removal survives but the user sees the proposed change first, increasing catch rate.

**What it doesn't solve:** discoverability puzzle (compound of B and C — users see `[Fix it]` on some items, run it, and have to confirm twice); parallel-session collision (same Q5 as all options); marginal time savings may not justify the implementation complexity. F is "ship the safest possible inline-apply" but the safety/cost ratio may not justify it over C alone.

## Recommendation

**Option C — Per-kind opt-in (bundle-eligible only).**

The strongest evidence for this option is the combination of Q3 (bundle-eligibility criteria are the strictest tier and filter most failure-mode patterns) and Q8 (time savings exist but are concentrated in the bundle-eligible subset). Q2's industry precedent — Anthropic doesn't yet ship "previously-captured finding inline apply" in Claude Code itself, and Cursor 2.0's pattern is still diff-then-commit — argues against the most aggressive option (A) shipping ahead of platform norms, while Q4's rollback analysis favors single-commit-per-finding over batched apply (which is a Stage 7 concern, not this decision). Option C ships a useful inline-apply tier with the smallest blast radius, leaves a clean upgrade path to A by adding `fix-eligible` later, and absorbs the bulk of the value-prop the audit family was designed for. Option F (adding B's dry-run-first) is the strongest fallback if the user prefers a more conservative ship; the marginal extra friction is small and the catch-rate improvement is real for the cases where it matters.

## Decision

**Selected: Option C — Per-kind opt-in (bundle-eligible only).** Confirms research-agent recommendation 2026-05-15.

**Rationale:**

- **Strictest tier first.** Bundle-eligibility criteria (impl-only + source-confirmed at apply time + reversible + no new judgment + ≤3 files) filter most of the gap patterns surfaced in research Q3. Shipping inline-apply only for this tier minimizes blast radius for the first round.
- **Aligned with platform norms.** Q2 confirmed Anthropic's Claude Code does not yet ship "previously-captured finding inline apply" — `acceptEdits` is a session-wide stance, not a per-finding contract; the closest analogue (Cursor 2.0) uses diff-then-commit. Option C stays conservative until the platform converges on a pattern.
- **Clean upgrade path.** Adding `fix-eligible` to the `[Fix it]` set is a future DEC after bundle-eligible runs for a few months across projects. Q6's free telemetry (`resolved_by.kind` in friction register + per-audit `digest.json` items[].status) gives the passive observation channel needed to validate post-ship behavior with no new infrastructure.
- **Known limitation captured.** Q3's transitive-consumer risk for orphan-dep removal survives all 5 bundle-eligibility criteria. Implementation MUST document this in `audit-fix-workflow.md` and recommend that users run tests after any bundled-apply touching `package.json`.

**Caveats / phased ship notes:**

- `[Fix it]` action renders ONLY on items where the audit synthesizer set `kind: bundle-eligible`. Items with `kind: fix-eligible`, `kind: decision`, or `kind: design` retain Stage 6a behavior (`[Promote to FB]` / `[Dismiss]` only).
- Discoverability mitigation: dashboard digest shows a one-line annotation per non-bundle-eligible item explaining "fix-eligible findings require manual review" — avoids the "why does this item have fewer actions?" puzzle from research Q-discoverability row.
- Stage 7 (bundled-apply batch UX) is a separate decision after Stage 6 (Option C) has shipped and accumulated some usage signal — Q4's analysis showed Stage 7's all-or-nothing revert is materially worse than Stage 6 single-commit-per-finding.
- Stage 6a's user-driven `[Promote to FB]` / `[Dismiss]` actions remain unchanged for all kinds.

---

## Implementation Notes

**Stage 6 (Option C) ship plan** — to land as `v3.12.0`:

Files to edit:

1. **`.claude/support/reference/audit-fix-workflow.md`** — upgrade Stage 6 (full) section from "deferred placeholder" to current. Document the `[Fix it]` mechanism for `bundle-eligible` ONLY. Add explicit "transitive-consumer risk" callout per Q3 (specifically: orphan-dep removal where dynamic require / importlib usage isn't statically grep-able). Document the discoverability annotation for non-bundle-eligible items. Document the kind-conditional action table.
2. **`.claude/support/reference/dashboard-regeneration.md`** (and `.claude/skills/dashboard-style/SKILL.md` mirror) — extend Action Required → Audit Findings sub-section spec with kind-conditional action labels: `bundle-eligible` → `[Fix it] / [Promote to FB] / [Dismiss]`; other kinds → `[Promote to FB] / [Dismiss]` (unchanged from Stage 6a).
3. **`.claude/commands/work.md`** — add `[Fix it]` invocation procedure (orchestrator-side: read finding from latest `digest.json`, re-read `source_anchors`, ask single approval, apply, single commit `audit-fix: C-NN — {summary}`, update `digest.json` `items[i].status: resolved` and `friction.jsonl` for cited entries).
4. **`.claude/commands/audit-coherence.md`** and **`audit-ui.md`** — note in synthesizer prompts that `bundle-eligible` kind classification now triggers an actionable inline-apply path; tighten classification confidence accordingly (don't promote to bundle-eligible unless source-confirmation is unambiguous and the file footprint is genuinely ≤3 files).
5. **`template-maintenance/audit-command-family-proposal.md`** — update Stage 6 in the Staging section: was "Stage 6 full" with [Fix it] for all kinds; now "Stage 6 (Option C per DEC-013)" with bundle-eligible-only [Fix it]. Note the deferred fix-eligible upgrade path. Update Component 8's action table to reflect the per-kind gating.
6. **`.claude/version.json`** — bump 3.11.0 → 3.12.0 (minor: new feature — inline-apply tier for bundle-eligible findings).

**Telemetry validation gate before considering fix-eligible expansion** (future DEC):

- Wait until at least 5 `[Fix it]` invocations have occurred across downstream projects, observable via `resolved_by.kind == "fix_it"` count in friction register OR `digest.json items[].status == "resolved"` with `resolved_by.kind == "fix_it"`.
- Manually inspect a sample of applied diffs to confirm zero silent-corruption events.
- If clean: open follow-up DEC for fix-eligible expansion. If not: revisit Option F (add dry-run-first to bundle-eligible).
