# Archived Feedback

All resolved feedback items. Each entry preserves its final status and reason.

- **promoted** — Incorporated into the spec via `/iterate`
- **absorbed** — Combined into another item (has `absorbed_into` pointer)
- **closed** — Investigated but decided against
- **archived** — Not relevant (quick triage)

---

## FB-002: `decomposition-heuristics` skill needs a "Research-spike pattern" section — methodology→empirical→analysis task shape doesn't fit the `owner` enum cleanly

**Status:** promoted
**Captured:** 2026-05-15
**Refined:** 2026-05-15 — Template skill edit: add a "Research-spike pattern" section to `.claude/skills/decomposition-heuristics/SKILL.md` covering the methodology→empirical-loop→analysis task shape. Documents trigger (task shape combines methodology + empirical loop + analysis), decomposition (TXXXa claude-methodology blocks TXXXb human-loop blocks TXXXc claude-analysis), collapse rule for trivial spikes (single Claude task with in-prose hand-off), description discipline (TXXXb carries the empirical-prompt; TXXXc carries the analysis shell), and verification convention (TXXXa/TXXXc normal verify; TXXXb self-attests via `/work complete`). Per styler DEC-082 Option ε. Zero schema churn (uses existing `/breakdown` primitive and 3-value `owner` enum). Optional companion edit: a worked example in `.claude/commands/breakdown.md`. **Mirror constraint:** per DEC-007 Option B (Skills trial), the same section must also land in `.claude/support/reference/decomposition.md` until one file is retired.
**Assessed:** 2026-05-15 — Scope: additive (one new section in SKILL.md + mirror in `decomposition.md`; optional worked example in `commands/breakdown.md`). No conflicts with resolved decisions; aligns with downstream styler DEC-082 Option ε. Template version bump on promotion: MINOR (new feature in a shipped skill). No interaction with current Active Follow-ups (FB-011 Families C/D/E, FB-033 / DEC-009, DEC-013 audit-family follow-ups).
**Promoted:** 2026-05-15 — Applied as template-maintenance edit (no spec involvement; template repo has no project spec per CLAUDE.md). New "Research-spike Pattern" section added to BOTH `.claude/skills/decomposition-heuristics/SKILL.md` AND its mirror `.claude/support/reference/decomposition.md` (DEC-007 Option B mirror constraint honored). Sub-sections: Trigger, Decomposition, Collapse rule, Description discipline, Verification convention, Why this shape. Optional companion edit in `.claude/commands/breakdown.md` deferred — can be added later if a worked example proves useful. Template version bumped 3.12.0 → 3.13.0. Downstream projects (e.g., styler) inherit via `/health-check` sync.
**Source:** styler project (`/Users/erikemilsson/Developer/styler/`) — surfaced via FB-162 (2026-05-06 audit), formalized via DEC-082 (decided 2026-05-15 with Option ε). The decision record + research archive live in styler at `.claude/support/decisions/decision-082-task-owner-field-refinement.md` + `.claude/support/decisions/.archive/decision-082-research-2026-05-15.md` for the full reasoning. **This feedback exists in the template repo because the implementation surface — `.claude/skills/decomposition-heuristics/SKILL.md` — is template-owned and the pattern generalises across forks.**

### The structural finding

The `owner` field uses a 3-value enum (`claude | human | both`) per `.claude/rules/task-management.md`. Today's enum encodes **who is responsible**, conflated with **who executes the work**. For most tasks the two are the same. For a specific task shape — **methodology → empirical loop → analysis** — they split cleanly.

**Concrete example (styler T610):** a research spike investigated `pngpaste` / AppleScript clipboard reliability. The task was filed as `owner: claude` because the deliverable was a workspace markdown report (Claude-authorable artifact). But the **empirical test loop** required the user to paste images into the Claude Code conversation under various conditions — something only a human can do. `owner: claude` was misleading; the spike's structural shape was "Claude authors methodology → human runs empirical loop → Claude analyzes results and writes report."

**`owner: both` doesn't fit either.** Today's `both` is documented (`.claude/support/reference/task-schema.md:160-162`) for **review-shaped** work: "design work (human provides direction, Claude implements)" / "content requiring human judgment (Claude drafts, human refines)." A research spike's human empirical loop is NOT a review — the user IS the experimental apparatus.

### The pattern recurs

Two known instances in styler's 525-task corpus (T610 + T456). The pattern generalises beyond styler to:
- Onboarding sniff tests (Claude designs the sniff; human runs it; Claude analyzes friction signals)
- Perceptual A/Bs (Claude generates A vs B; human picks; Claude synthesizes the preference)
- Brand-new feature dogfooding cycles (Claude scaffolds the feature; human uses it for N days; Claude reviews observed friction)
- Any task whose validation step requires human-only sensors (taste, perception, in-the-moment judgment)

### The decision (DEC-082 → Option ε, decided 2026-05-15)

Five options were evaluated against 9 criteria (full matrix in styler's DEC-082). **Option ε won:** instead of changing the `owner` enum or adding new fields, **decompose research-spike tasks at decomposition time** via the existing `/breakdown` primitive:

```
TXXXa (owner: claude)            — authors methodology + drafts the empirical-prompt + leaves analysis shell
   ↓ blocks
TXXXb (owner: human)             — runs the empirical loop, reports results in conversation; self-attests via /work complete
   ↓ blocks
TXXXc (owner: claude, deps: [TXXXa, TXXXb]) — synthesizes results into the final report
```

For tiny spikes where the empirical step is "paste one image", **collapse to a single Claude task** with an in-prose hand-off (today's de-facto pattern, called α in DEC-082). The paired-sub-task structure is for spikes where the empirical loop is independently worth tracking.

**Why ε won:** zero schema churn (uses existing `/breakdown`); surfaces the human empirical loop as a first-class dashboard artifact (TXXXb appears in "Your Tasks" with `❗`); each sub-task gets native verification routing (TXXXa/TXXXc via verify-agent's 7-check suite; TXXXb via self-attestation); generalises broadly. Trade-off: 1 task → 2-3 sub-tasks of bookkeeping for low-difficulty work.

Worst options (ranked low in DEC-082): γ (split `owner` + `executor` fields) had highest contract-surface impact; β (sub-token `both:research`) overloads the enum with a separator; α (convention-only) leaves the empirical step invisible to dispatch + dashboard.

### Implementation surface (template-owned)

**Single edit:** add a "Research-spike pattern" section to `.claude/skills/decomposition-heuristics/SKILL.md` documenting:

1. **Trigger** — task shape is methodology + empirical loop + analysis (research spikes, perceptual A/Bs, sniff tests, dogfood cycles).
2. **Decomposition** — split into TXXXa (claude methodology, drafts empirical-prompt), TXXXb (human empirical loop, self-attests via `/work complete`), and optionally TXXXc (claude analysis with `deps: [TXXXa, TXXXb]`).
3. **Collapse rule** — if the empirical step is trivial (~1 user action, no iteration), single Claude task with in-prose hand-off is fine. The paired pattern is for spikes where the empirical loop is independently worth tracking.
4. **Description discipline** — TXXXb's description must include the empirical-prompt template TXXXa drafted (so user knows what to test); TXXXc's description must include the analysis shell TXXXa stubbed.
5. **Verification convention** — TXXXa/TXXXc verified normally; TXXXb self-attests via `/work complete`. Acceptance for TXXXa is "did Claude produce a methodology that matches the spike's directional question?", not "did the empirical loop produce a specific answer?"

**Optional second edit:** `.claude/commands/breakdown.md` could gain a worked example mirroring this pattern (decomposition-time call).

### Why this fits the template, not the project

- The owner-enum semantics + decomposition heuristics are template-owned (`.claude/rules/`, `.claude/skills/`).
- The pattern applies to ANY Claude Code project that runs research spikes, perceptual tests, sniff tests, or dogfood cycles — not just styler.
- DEC-082 itself stays in styler's decision log (the friction surfaced there; the reasoning trail belongs with the surfacing context) — but the implementation lands in the template so all forks inherit the convention.

### Erik's plan

Capture this feedback in the template repo; let template-side Claude `/feedback review` triage it on its own schedule. After the SKILL.md edit lands in the template, Erik runs `/health-check` in styler to sync the updated template files back into styler's working tree.

### Pointers for template-side Claude

- **Full reasoning + research archive:** `/Users/erikemilsson/Developer/styler/.claude/support/decisions/decision-082-task-owner-field-refinement.md` (decision record, 240 lines, status: approved, includes 5 options × 9 criteria matrix + per-option Details + 4 open research questions). Research archive: `/Users/erikemilsson/Developer/styler/.claude/support/decisions/.archive/decision-082-research-2026-05-15.md` (187 lines, per-contract-site grep findings, dispatch spike per option, prior art from Jira/Linear/Asana).
- **Source feedback:** styler's FB-162 (now archived as `promoted` in styler's `archive.md` with reference to DEC-082).
- **The motivating concrete case:** styler T610 (Finished, owner:claude, but the empirical loop was structurally human-driven). T456 is a second, structurally similar instance.

### Out of scope for this feedback

- No changes to `.claude/rules/task-management.md` (3-value `owner` enum stays).
- No changes to `.claude/support/reference/task-schema.md`.
- No changes to `.claude/agents/implement-agent.md` or `.claude/agents/verify-agent.md`.
- No retroactive migration of existing tasks — pattern is forward-only.
- No new task statuses or sub-statuses introduced.
- A future `task_kind` field (option δ in DEC-082) could land alongside as a complement if drift surfaces — explicitly NOT part of this feedback; if it becomes worthwhile, capture as a fresh feedback item.

### Tags

decomposition-heuristics, task-schema, owner-field, research-spikes, skill-edit, template-fix, derived-from-styler-DEC-082

---

## FB-001: `mcp-server-git` leaves stale empty `.git/index.lock` on crash — blocks git in affected repos

**Status:** closed
**Captured:** 2026-05-15
**Closed:** 2026-05-15 — Out of template scope. Both proposed fixes (Option A: remove `mcp-server-git` from user-level Claude Code config; Option B: user-level `SessionStart` hook clearing verified-stale locks) live in `~/.claude/`, not in template-shipped `.claude/`. Nothing for the template to ship. Erik can apply Option A in his personal setup directly. Preserved here for cross-project audit trail; if the pattern recurs in another project, re-open as a template-side troubleshooting doc.
**Source:** observed in two projects (`styler/` and `styler-phone/`) during a single Claude Code session on 2026-05-15. Both repos had zero-byte `.git/index.lock` files dated **exactly `May 15 08:42`** (same minute, both 0 bytes, no holding process). Required manual `rm .git/index.lock` to unblock subsequent git commits. Surfaced twice in one day from a single crash event.

### The observation

The Anthropic-shipped `mcp-server-git` MCP server (Python, `~/.local/bin/mcp-server-git`) creates `.git/index.lock` at the start of any git operation that modifies the index (add, commit, etc.). If the server process crashes or is killed mid-operation, the lock stays behind. Subsequent git commands fail with:

```
fatal: Unable to create '/path/to/.git/index.lock': File exists.

Another git process seems to be running in this repository, e.g.
an editor opened by 'git commit'. Please make sure all processes
are terminated then try again.
```

**Detection signal — distinguishes stale from real:**
- Stale lock: zero bytes (`stat` shows `size=0`)
- Stale lock: minutes-to-hours old
- Stale lock: no active git process holding it (`ps aux | grep "git "` shows nothing besides idle `mcp-server-git` MCP-tool-host instances)
- Real lock during active git operation: non-zero size, very fresh (sub-second old), `git` process visible in `ps`

### Evidence from the 2026-05-15 incident

```
$ ls -la /Users/erikemilsson/Developer/styler/.git/index.lock \
        /Users/erikemilsson/Developer/styler-phone/.git/index.lock
-rw-r--r--  1 erikemilsson  staff  0  May 15 08:42  styler/.git/index.lock
-rw-r--r--  1 erikemilsson  staff  0  May 15 08:42  styler-phone/.git/index.lock

$ ps aux | grep "git " | grep -v grep
(nothing besides idle mcp-server-git instances — no active git process)
```

Same minute, both repos, zero bytes. Single crash event affected two repos because one `mcp-server-git` instance was touching both (or two instances crashed in lock-step). The locks survived ~7 hours into the day's work before being noticed at commit time.

### Two fix options

**Option A — Disable `mcp-server-git`, fall back to Bash (recommended — root-cause).**

The MCP server is configured at the user level (`~/.claude/...`) and spawns one instance per Claude Code session. In observed workflows, Claude reaches for the Bash tool for git operations (clearer permission rules per project CLAUDE.md preferences), leaving the MCP server idle. Removing its entry from the relevant Claude Code config (`~/.claude/settings.json` or the MCP-server registry, depending on installation) eliminates the crash class entirely.

- **Pro:** zero stale-lock surface (no crashing process = no stale locks); lighter memory footprint (fewer Python processes resident across sessions); cleaner permission model.
- **Con:** any workflow that explicitly invokes `mcp__git__*` tools would need to fall back to Bash. Unknown without inspecting individual workflows; for sessions observed during the incident, no such workflow existed.
- **Implementation:** edit user-level Claude Code config to remove the `git` MCP server entry; restart sessions.

**Option B — `SessionStart` hook that auto-clears verified-stale locks (belt-and-suspenders).**

A hook that scans known repos at session start and removes `.git/index.lock` files that are (a) zero bytes AND (b) older than ~60 seconds AND (c) not held by any active git process. Safe because real git operations don't satisfy all three conditions simultaneously — real locks always have content and are fresh.

- **Pro:** neutralizes the symptom regardless of which MCP/tool crashed; doesn't require removing functionality.
- **Con:** another moving part; needs a list of known repos to scan (or it scans nothing and is useless); doesn't address why `mcp-server-git` crashes.
- **Implementation:** add a `SessionStart` hook in `~/.claude/settings.json` invoking a small bash script under `~/.claude/scripts/`. ~10 lines of bash.

### Recommendation

Ship Option A as the primary fix. Add Option B if and only if some other tool ever exhibits the same crash-leaves-lock pattern. For Erik's setup specifically, Option A is a one-line config change with no observed downside.

### Investigation worth doing alongside

Why does `mcp-server-git` crash? Two repos at the exact same minute suggests one of:
- A signal (SIGKILL/SIGTERM) hit the process — system suspend, hibernation, OOM, manual kill — that the server didn't handle with a cleanup phase.
- An exception in the server's git-invoking code path that escaped without releasing the lock.

If Claude Code keeps logs of MCP server lifecycle events (start/crash/exit), check `~/.claude/logs/` or equivalent for entries near `08:42` on the incident date. Could be a one-off (machine suspended mid-operation) or a repeatable bug.

### Related signals

- The MCP server itself is part of the Anthropic-shipped `mcp-server-git` package (or its successor). If the crash is reproducible, worth a bug report upstream.
- Empirically: stale locks DO happen with regular `git` CLI usage too (e.g., killing a `git rebase -i` mid-edit), but those typically have content in the lock file and are easy to distinguish.

### Tags

mcp, mcp-server-git, git-lock, stale-lock, claude-code-environment, crash-cleanup

---

## FB-003: Promote `feature-retirement.md` from Styler to template (generally-useful workflow rule)

**Status:** promoted
**Captured:** 2026-05-15
**Promoted:** 2026-05-16 — Shipped in template_version 3.14.0. Genericized port of Styler's project-local rule. Two new files: (1) `.claude/rules/feature-retirement.md` documenting the 5-step retirement procedure (snapshot, commit pin, archive placement, spec annotation, discoverability), restore path (manual cherry-pick + optional project-side `/restore`), edge cases (application state, multi-file, merged spec sections, shared helpers, graduation to permanent deletion); (2) `.claude/support/retired/README.md` documenting the directory convention and `manifest.json` schema. Imports added to `.claude/CLAUDE.md` (rule + summary row); both files added to `sync-manifest.json`. Styler-specific references stripped (FB-070/071, T504/T497, DEC-055/050/051, spec § 27.1/13/21/22, foundation/* paths, Next.js-specific extensions, playwright dep removal example); replaced with generic examples. Worked example shifted from the rule file to the README schema doc. No changes to `audit-coherence.md` — Lens 5 (`retired-features`) already keys on the documented directory convention and reads manifests generically. After ship + sync, Styler's project-owned copy of `.claude/rules/feature-retirement.md` and `.claude/support/retired/README.md` can be retired (the template versions become the canonical home).
**Source:** discovered as a Styler-local rule file during investigation of `/health-check` Part 5 sync friction (template-maintenance FB-059 + FB-060). Originally captured at `template-maintenance/feedback.md` as FB-061; relocated to shipped queue 2026-05-15.

**Observation:** Styler had a project-local rule file at `.claude/rules/feature-retirement.md` that codifies a generally-useful workflow: how to retire a feature in a frozen, restorable state. The workflow shape:
- Snapshot lives at the retirement commit (no orphaned state)
- Spec keeps a "Retired (YYYY-MM-DD)" marker (discoverability for future readers)
- Directory convention (`.claude/support/retired/{slug}/manifest.json`) enables mechanical restoration

Not fashion-domain-specific. Any project doing iterative feature work that occasionally retires surfaces (renamed routes, removed components, sunset features) benefits. Integrates cleanly with the template's existing patterns (spec-as-source-of-truth, decision records, audit family's `retired-features` lens which already greps `.claude/support/retired/*/manifest.json`).

The audit family's `audit-coherence` lens for `retired-features` already assumed this file structure exists — it scans `.claude/support/retired/*/manifest.json` and flags retired features missing spec markers. Promoting `feature-retirement.md` to the template makes the audit lens fully legible to downstream projects.

**Counterpart not promoted:** Styler's `brand-mention-provenance.md` (when Claude can name brands vs substitute attributes per DEC-060) is fashion/retail-domain-specific. Stays Styler-only.

**Open question (resolved at promotion):** the workflow rule did reference a `.claude/support/retired/README.md` sibling doc holding the manifest schema. Styler's schema field names (`feature_slug`, `successor_feature`, `rationale`) were kept verbatim during promotion — they correctly populate the conceptual fields the audit-coherence Lens 5 prompt names (`slug`, `replaced_by`, `retirement_reason`). The audit lens prompt's conceptual field names are descriptive, not strict JSON keys; the lens reads the manifest contents and maps them. No schema migration needed.

### Tags

rule-file-promotion, feature-retirement, audit-coherence, retired-features-lens, derived-from-styler

---

## FB-004: Promote "Audit Tasks: literal-ID comparison" rule from Styler to template (`task-management.md`)

**Status:** absorbed (duplicate)
**Captured:** 2026-05-15
**Closed:** 2026-05-16 — Duplicate of `template-maintenance/feedback-archive.md` § FB-042 (promoted 2026-05-13, shipped in template v3.2.1 via commit 18951e8). The `## Audit Tasks` section was already present in `.claude/rules/task-management.md` at the time FB-004 was captured. No template change needed.
**Absorbed into:** FB-042 (`template-maintenance/feedback-archive.md`).
**Source:** discovered in styler-local addition to template-owned `.claude/rules/task-management.md` during ownership-boundary audit (counterpart to FB-003 + FB-005). Surfaced during cross-project capture session 2026-05-15.

### Why it slipped past the Styler-side dedup check

The dedup check probed four template-side feedback locations and concluded no prior item touched audit-task literal-ID comparison. The miss was caused by a **filename mismatch**: the check looked for `template-maintenance/archive.md` and reported "does not exist." The actual template-maintenance archive file is `template-maintenance/feedback-archive.md`, which contains FB-042 (the predecessor). Captured separately under FB-062 (template-maintenance) as an empirical instance of the dual-location convention gap.

### What FB-042 already shipped (and FB-004 redundantly proposed)

- A `## Audit Tasks` section in `.claude/rules/task-management.md` (between `## Parallel Execution` and `## References`) requiring 4-step literal-ID comparison in audit tasks of the form "verify whether downstream task X is needed."
- `scope_clarification_needed` reporting path for semantic-match-without-literal-ID-match (a partial match should not be reported as `stale` / `no-op`).
- Calibrated against the Styler Phase 20 T429 false-positive `no-op` finding.

### Tags

rule-file-promotion, task-management, audit-tasks, literal-id-comparison, derived-from-styler, duplicate

---

## FB-005: Promote "MCP and Parallel Execution" rule from Styler to template (`agents.md`)

**Status:** absorbed (duplicate)
**Captured:** 2026-05-15
**Closed:** 2026-05-16 — Duplicate of `template-maintenance/feedback-archive.md` § FB-056 (promoted 2026-05-13, shipped in template v3.2.1 via commit 18951e8). The `## MCP and Parallel Execution` section was already present in `.claude/rules/agents.md` at the time FB-005 was captured. No template change needed.
**Absorbed into:** FB-056 (`template-maintenance/feedback-archive.md`).
**Source:** discovered in styler-local addition to template-owned `.claude/rules/agents.md` during ownership-boundary audit (counterpart to FB-003 + FB-004). Surfaced during cross-project capture session 2026-05-15.

### Why it slipped past the Styler-side dedup check

Same root cause as FB-004 above: the dedup check looked for `template-maintenance/archive.md` rather than the actual `template-maintenance/feedback-archive.md` and missed the predecessor (FB-056). See FB-062 (template-maintenance) for the convention-gap empirical-instance note.

### What FB-056 already shipped (and FB-005 redundantly proposed)

- A `## MCP and Parallel Execution` section in `.claude/rules/agents.md` (between `## Behavioral Rules` and `## Tool Preferences`) documenting single-session MCP server constraint (Playwright, browser automation, auth-session MCPs).
- Three-pattern orchestrator response: route MCP-driving work through one agent / parallelize the rest / dispatch sequential agents for multi-route inspection.
- Notes a lower-priority `mcp_resource_overlap` heuristic for a future `/work` Step 2c extension (parallel to FB-046's `shared_contract` detection).

### Tags

rule-file-promotion, agents-rules, mcp, parallel-execution, playwright-mcp, single-session-resource, derived-from-styler, duplicate

---

## FB-006: Audit-findings dashboard/CLI workflow — courier pattern, dead UI, name burden, opacity

**Status:** promoted
**Captured:** 2026-05-16
**Split:** 2026-05-16 — Original FB-006 split during `/feedback review` Phase 1. This item retains sub-issues 1-4 (dashboard/CLI workflow UX). Sub-issue 5 (Claude direct-edit guardrail) extracted to FB-007 because it is a behavioral/rule concern orthogonal to the UX rough edges and worth a separate assessment + promotion track.
**Refined:** 2026-05-16 — The audit-findings → feedback → spec-amendment workflow has four convergent UX rough edges that compound during triage: **(a) courier pattern** — dashboard tick is the only interactive element, but acting on ticks requires re-specifying state in the CLI (`/audit-coherence promote <name>`); user couriers the audit name from dashboard to terminal. **(b) name memory burden** — audit names (e.g. `coherence-2026-05-15-2337`) must be remembered or copy-pasted; especially painful when multiple audits have populated the dashboard. **(c) dead UI** — inline `[Promote to FB] / [Dismiss]` text per finding looks selectable but isn't; only the checkbox is interactive and it can only express promote-tick (unticked is ambiguous: not-yet-triaged vs dismissed). **(d) opacity at decision moment** — dashboard digest shows only short titles; full description lives in `findings.md` which the user must open separately; auto-routing via `/audit-coherence promote` doesn't surface plain-English at the moment of decision. User-stated requirement: "a simple description in plain English about what was found and what the issue is" *on the dashboard*, enough to triage without opening `findings.md`. Three candidate directions (not mutually exclusive): **(1) render-time consolidation** — drop dead inline text, expand each finding's dashboard entry to a one-line plain-English description, render audit name in one copy-paste-friendly header; **(2) single triage command** — `/audit-coherence triage` reads dashboard state and walks promote/dismiss interactively, eliminating name-memory; **(3) dual-checkbox column** — promote-tick vs dismiss-tick, removes implicit-state ambiguity. Implementation surface is template-owned (`commands/audit-coherence.md`, dashboard render rules in `rules/dashboard.md` + `support/reference/dashboard-regeneration.md`, audit digest format under `.claude/support/audits/<name>/`).
**Assessed:** 2026-05-16 — Scope: corrective + additive (dead-UI removal reductive; plain-English description per finding + triage command additive). Template files affected: `commands/audit-coherence.md` (digest synthesizer + possible `triage` subcommand), `rules/dashboard.md` + `support/reference/dashboard-regeneration.md` (audit-findings render rules), `skills/dashboard-style/SKILL.md` (section format), possibly `support/audits/<name>/digest.json` schema (`plain_english_description` field per finding). No decision conflicts — DEC-013 specified routing rules for findings, not the visual element shape; Direction 1's change to the `[Promote to FB] / [Dismiss]` inline text is compatible. Active follow-ups: precursor to deferred Audit family Stage 7 (bundled-apply batch UX); no interaction with Fix-eligible inline-apply expansion telemetry gate; no interaction with FB-011/FB-033/FB-060/FB-062/FB-063. Decision character: pick-and-go (no inflection). Version bump on promotion: likely sequenced as PATCH (drop dead-UI inline text alone) → MINOR (plain-English digest extension) → MINOR (`/audit-coherence triage` interactive walker) → MINOR-or-deferred (dual-checkbox column; depends on whether single triage command obsoletes the need). Promotion route: direct template change(s); no /research needed.
**Promoted:** 2026-05-16 — All four sub-issues closed via direct template edits across three iterations (template repo has no project spec per `CLAUDE.md`; promotion route is template-maintenance direct ship per the Assessed-line forecast). **Iteration 1 (v3.17.1 PATCH, commit `ded0e03`)** closed sub-issue 3 "dead UI": dropped per-finding `[Promote to FB] / [Dismiss]` inline text from the dashboard render (`[Fix it]` retained for `bundle-eligible` since it has no keyword alternative; non-bundle-eligible kinds show italicized kind annotation only). Updated `dashboard-regeneration.md` § "Audit Findings sub-section" + `dashboard-style/SKILL.md` mirror + `audit-fix-workflow.md` example; new "How to act on findings" sub-section documents promote (tick + bulk CLI) + dismiss (natural-language) invocation patterns. **Iteration 2 (v3.18.0 MINOR, commit `30d8170`)** closed sub-issue 4 "opacity at decision moment": added `description` field to `digest.json items[]` (Component 2 schema) — plain-English synthesizer-written sentence per finding rendered on the dashboard digest in place of the terse `title`. Synthesizer prompts in `commands/audit-coherence.md` + `commands/audit-ui.md` Algorithm step 4 specify the writing convention (complete sentence, period-terminated, ~80-140 chars, names the affected artifact, distinct from `title`); render rules use `{description ?? title}` fallback for pre-v3.18.0 digest.json files. **Iteration 3 (v3.19.0 MINOR, commit `a43d977`)** closed sub-issue 1 "courier pattern" + sub-issue 2 "audit-name memory burden": `/audit-coherence triage [audit-ts]` + `/audit-ui triage [audit-ts]` interactive walkers. `audit-ts` defaults to `latest` (newest by `ran_at`) so the user never types the audit name; walker iterates pending non-dismissed findings, presents kind-conditional actions `[F]ix it · [P]romote · [D]ismiss · [S]kip · [Q]uit`, supports single-letter shorthand + natural-language verbs (`dismiss because X` parses reason inline). Dispatches to canonical per-action mechanics in `audit-fix-workflow.md` (no divergence; the walker is a dispatcher, not a separate flow). Cross-references added in `audit-fix-workflow.md` "Preferred entry point for N pending findings" section + `dashboard-regeneration.md` "How to act on findings" + `dashboard-style/SKILL.md` mirror. **Dual-checkbox promote-vs-dismiss column** (originally MINOR-or-deferred candidate for sub-issue 3): closed as obsoleted by iteration 3's triage walker, which provides explicit per-action dispatch without relying on checkbox semantics. Sub-issue 5 (Claude direct-edit guardrail on `.claude/spec_v*.md`) was extracted to FB-007 during /feedback review Phase 1 — still active in `feedback.md`, routed to `/research` per user disposition 2026-05-16 (DEC-NNN for the three architectural alternatives).

Surfaced live while working `coherence-2026-05-15-2337` finding C-01 in the styler project. User concerns, captured directly:

1. **Dashboard ticking is disconnected from the CLI follow-up.** On the dashboard the user can only tick boxes. To act on those ticks the user has to go to the CLI and re-specify what they want (`/audit-coherence promote <audit-name>`). The dashboard knows the audit name; the CLI also wants it; the user is the courier between them.

2. **Audit-name memory burden.** The user has to remember the audit name (e.g. `coherence-2026-05-15-2337`) when running the CLI command. Especially painful if more than one audit has populated the dashboard.

3. **"[Promote to FB] / [Dismiss]" inline text is dead UI.** Each finding renders "[Promote to FB] / [Dismiss]" next to its title. These look like options but aren't selectable — the only interactive element on the dashboard is the checkbox, and there's no way to express "dismiss" via the checkbox (ticking it = promote; not-ticking = ambiguous between "not yet triaged" and "dismissed"). The "[Dismiss]" text takes up real estate without offering function. (Promote text is also moot since the actual promote action is the CLI command at the bottom of the section, not the inline text.)

4. **Promotion is opaque.** The dashboard digest gives only a short title per finding. The full description lives in `.claude/support/audits/<name>/findings.md`, which the user has to open and read separately. And if a ticked finding auto-routes onward (e.g. into `/iterate` after `/audit-coherence promote`), the user doesn't see the plain-English description at the moment of decision. The user wants "a simple description in plain English about what was found and what the issue is" *on the dashboard* — enough to triage without opening the findings.md.

Possible directions for the broader dashboard ↔ CLI split (user has not chosen — starting points only):

- **Render-time consolidation:** drop the dead `[Promote to FB] / [Dismiss]` inline text; expand each finding's dashboard entry to include a one-line plain-English description (currently it's just a short title); render the audit name in one copy-paste-friendly header so the user reads it from one place
- **Single triage command:** `/audit-coherence triage` (or similar) reads the dashboard state, walks the user through promote/dismiss per finding interactively, and removes the need to remember the audit name
- **Add a second checkbox column** so the dashboard supports both promote-tick and dismiss-tick, removing the implicit-state ambiguity of unticked-vs-dismissed

### Context

Triggered while working audit `coherence-2026-05-15-2337` finding C-01 (Phase 28 `template/` prefix drift) in styler. The audit's path-drift evidence was largely stale (~40 claimed callsites → 0 bare-path matches in current spec, since Phase 28 implementation work had already swept them). The behavioral concern that surfaced in the same session — Claude running direct `Edit` calls on the spec instead of routing through `/iterate` — is extracted to FB-007.

### Related

Sibling capture FB-007 covers the Claude direct-edit guardrail concern that surfaced in the same C-01 session.

### Tags

audit-findings, dashboard-cli-split, workflow-friction, render-consolidation, triage-command

---

## FB-007: Claude direct-edit guardrail on `.claude/spec_v*.md` — rule tension between "direct edits safe" and audit `iterate_routing: /iterate`

**Status:** promoted
**Captured:** 2026-05-16
**Split:** 2026-05-16 — Extracted from original FB-006 during `/feedback review` Phase 1. Sub-issue 5 of the original capture. FB-006 retains sub-issues 1-4 (dashboard/CLI workflow UX). This item carries the behavioral/rule concern about direct spec edits because (a) it's structurally independent — the rule tension exists regardless of whether the source is an audit finding, and (b) the implementation surface is `rules/spec-workflow.md` not `commands/audit-coherence.md`.
**Refined:** 2026-05-16 — Two rule sources are in direct tension. `.claude/rules/spec-workflow.md` says: "Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation." Audit findings declare `iterate_routing.target: "/iterate"` and the dashboard prose says "spec amendment via /iterate". When Claude judges audit evidence stale and decides to sweep residual drift inline, no rule explicitly intercepts. Observed in styler `coherence-2026-05-15-2337` C-01 session: Claude ran 5 direct `Edit` calls on `spec_v13.md` to sweep residual noun-drift (`Personalized principles` → `Archetype Principles`) before being challenged, then reverted via 5 more direct edits. Net spec state unchanged, workflow bypassed twice. Three structural alternatives (user has not chosen): **(1) explicit rule override** — spec/decision-file edits sourced from an audit finding's `iterate_routing` MUST route through `/iterate`, regardless of how small the change appears (rule-only, lightest, narrowest); **(2) size-based carveout** — distinguish "drift sweep <N lines" from "spec amendment requiring formal flow" (rule-only, lighter still but introduces a numeric threshold needing calibration); **(3) permission/hooks-layer gate** — intercept `Edit` calls on `.claude/spec_v*.md` for confirmation regardless of provenance (structural, heavier-handed, catches non-audit-sourced edits too — broader than the originating concern). Implementation surface is template-owned: `.claude/rules/spec-workflow.md` as primary; possibly `.claude/rules/agents.md` for behavioral framing adjacent to "Root Cause Over Symptom"; option (3) would touch `.claude/settings.json` PreToolUse hooks. Tension also exists with `.claude/rules/spec-workflow.md`'s "Propose-Approve-Apply" rule which already says infrastructure operations are autonomous-OK but spec text changes are user-facing — option (1) could be framed as a clarifying refinement of that existing rule rather than a new constraint.
**Assessed:** 2026-05-16 — Scope: corrective (sharpening implicit constraint to explicit). Template files affected: `rules/spec-workflow.md` (primary site for rule clarification); possibly `rules/agents.md` adjacent to "Root Cause Over Symptom" for behavioral framing; Option 3 (PreToolUse hook) would touch `.claude/settings.json` PreToolUse hooks on Edit/Write for `.claude/spec_v*.md` paths. Pre-existing structural enforcement (already in place): DEC-013 HARD RULE at `audit-coherence.md:394` routes spec-file findings to `kind: decision` → `[Fix it]` never modifies spec inline — this is the **audit-system** layer. FB-007's concern is at a **different layer**: Claude's general Edit-tool usage on spec files outside the audit fix-it flow. Pre-existing rule: propose-approve-apply already says spec changes need user approval; "infrastructure operations autonomous" carveout enumerates archiving/version transitions/frontmatter updates — substantive text edits not in the enumeration. FB-007 sharpens the implicit constraint. Decision conflicts: DEC-013 (supportive — extends same principle from audit-system layer to Claude's general behavior); propose-approve-apply pattern (Option 1 is a clarifying refinement of the existing rule, not a new constraint). Active follow-ups: closes a gap revealed by Audit family Stage 6 / DEC-013 — DEC-013 secured the audit-system surface; FB-007 secures Claude's general behavior on the same files. Decision character: borderline — Option 1 and Option 2 are pick-and-go; Option 3 (PreToolUse hook) is an inflection point with structural permission-layer impact. Three alternatives with materially different blast radii. Version bump on promotion: MINOR for Option 1 or 2 (rule clarification); MAJOR for Option 3 (PreToolUse hook is a permission-layer change). Promotion route: **/research → DEC-NNN** (per user disposition 2026-05-16) — three architectural alternatives warrant evaluation together rather than direct promotion of one. Active Follow-up entry added to root `CLAUDE.md` to trigger `/research` at next template-side session.
**Promoted:** 2026-05-16 — Promotion route was `/research` → DEC-016 → user selection (Option D + Q6 symmetric extension to decisions + vision + MAJOR bump). Shipped in template_version **4.0.0**. Research-agent's load-bearing Q3 finding reframed the cost calculus: what FB-007 originally called "PreToolUse hook" is actually `permissions.ask` with gitignore-glob path matching — the same primitive DEC-005 / DEC-008 already use for `permissions.allow`, just `ask` flavor (2-6 lines of JSON, not a custom hook script). With Option C this cheap, Option D's composite shape (rule clarification + permission gate) became reachable at near-zero combined cost. Q1 finding additionally disqualified Option A alone (provenance is not platform-trackable — `PreToolUse` JSON has no slash-command-source field — so "audit-sourced edits" degenerates to "all spec edits" in practice). Q2 disqualified Option B (no defensible N; the autonomy axis users want is *kind*, not *size*; DEC-013 already established the kind-based axis). Implementation across 7 template files (Decision record's `implementation_anchors`): `.claude/settings.json` (6 `permissions.ask` entries — Edit + Write × spec/decisions/vision); `.claude/rules/spec-workflow.md` (new `## Direct edits to spec, decision, and vision files (DEC-016)` section replacing the "direct edits always safe" line); `.claude/CLAUDE.md` Critical Invariants (two invariants updated); `.claude/sync-manifest.json` notes; `.claude/README.md` settings description; `.claude/support/reference/extension-hooks.md` settings-layering reference; `.claude/commands/health-check.md` Part 5c validation logic. Per-amendment user cost: one click per `/iterate apply` (or `/research`) session at the first Edit; platform-native "Yes don't ask again" persists through session end. Decision record: `decisions/decision-016-spec-file-edit-guardrail.md` (status: implemented). Research archive: `decisions/.archive/decision-016-research-2026-05-16.md` (full 8-question methodology + URLs).

The captured concern, verbatim from FB-006 sub-issue 5:

**No Claude guardrail against direct spec edits.** Audit findings declare `iterate_routing.target: "/iterate"` and the dashboard prose says "spec amendment via /iterate". But `spec-workflow.md` says "Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation." These are in tension. In a live C-01 session, Claude judged most of the audit's evidence to be stale (path-drift swept in earlier work) and ran 5 direct `Edit` calls to sweep the residual noun-drift before being challenged. The reverts also went through direct edits. Net spec state was unchanged, but the workflow was bypassed twice. Possible directions:

- An explicit override clause: spec/decision-file edits sourced from an audit finding's `iterate_routing` MUST route through `/iterate`, regardless of how small the change appears
- A carveout that distinguishes "drift sweep <N lines" from "spec amendment requiring formal flow"
- A permission/hooks-layer gate that intercepts `Edit` calls on `.claude/spec_v*.md` for confirmation (heavier-handed, but structural rather than rule-based)

### Context

Triggered while working audit `coherence-2026-05-15-2337` finding C-01 (Phase 28 `template/` prefix drift) in styler. Claude found the audit's path-drift evidence largely stale (~40 claimed callsites → 0 bare-path matches in current spec, since Phase 28 implementation work had already swept them) and made 5 direct `Edit` calls to sweep the residual Layer-2 noun-drift (`Personalized principles` → `Archetype Principles`). User challenged the bypass; Claude reverted via 5 more direct Edits. Net change to `styler/.claude/spec_v13.md`: zero — but the workflow was bypassed twice.

### Related

Sibling capture FB-006 covers the dashboard/CLI workflow UX rough edges (sub-issues 1-4) that surfaced in the same session.

### Tags

spec-edit-guardrails, claude-behavior, rule-tension, audit-iterate-routing, hooks-layer-gate, propose-approve-apply

---
