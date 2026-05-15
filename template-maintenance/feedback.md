# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-011: Explore scripts as alternative to commands or within skills folders

**Status:** ready
**Captured:** 2026-04-08
**Refined:** 2026-04-14 — Identify command procedures where a deterministic script would outperform LLM-executed natural-language instructions — starting with the dashboard, where output variation across regenerations makes the artifact harder to comprehend. Scripts could live alongside commands or inside skills folders if that's a valid pattern. Gains: (1) consistency of standardized artifacts, (2) reduced error rate from procedure drift, (3) lower token cost. Scope is exploratory — inventory candidates and propose which procedures to extract before committing.
**Assessed:** 2026-04-14 — Primary target is dashboard regeneration (touching `.claude/support/reference/dashboard-regeneration.md`, `.claude/rules/dashboard.md`, and call sites in implement-agent Steps 3, 6a, 6c). Shipping scripts needs a new home (likely `.claude/scripts/` — root `scripts/` is template-maintenance and does not ship). Conflict: `rules/agents.md` restricts Bash, and scripts depend on it — connects to FB-010 (subagent Bash sandbox limits). Dependencies: FB-017 (checkbox detection is a concrete second candidate). Scope: start with a workspace inventory doc (`.claude/support/workspace/scripts-candidates.md`) listing candidates with tradeoffs; first extraction targets dashboard regen.

Look into where scripts could be used instead of commands, or even perhaps as part of skills folders if that is a valid use-case. Needs to be more robust or save tokens or minimize errors, improve quality etc.

## FB-033: Spec-auditor subagent + PreToolUse gate (research-first; trial FB-032 first; candidate DEC-009)

**Status:** ready
**Captured:** 2026-04-17
**Assessed:** 2026-04-17 — Affects new `.claude/agents/spec-auditor.md` (subagent, not Skill — resolved by DEC-007), hook wiring, verify-agent integration. Scope: exploratory. Research-first AND trial-gated on FB-032 (only pursue if the structural output contract proves insufficient after real `/iterate` sessions under Opus 4.7). FB-020 dependency resolved by DEC-007 (subagent is the correct home). FB-026 dependency resolved by DEC-008 (layered settings stay; hook wiring goes in `settings.local.json` if pursued). Route: Phase 3 research — **deferred** until FB-032 trial data exists (candidate DEC-009).

Source: Claude Code usage insights report (fetched 2026-04-17) — "On the Horizon" section proposes an adversarial-reviewer subagent that intercepts every `Write`/`Edit` to `spec*.md` or `decisions/*.md`. User edit on capture: *"wait until A1 is trialed properly before deciding"* — this item is explicitly gated on FB-032's trial outcome.

A bigger-hammer version of FB-032. The spec-auditor would diff each proposed change against the prior version, extract new assertions/decisions, cross-reference them against the current session's explicit user instructions, emit a "user-requested vs agent-inferred" table, and block the write until agent-inferred items are approved.

**Trial-gate:** Do not pursue until FB-032's structural output contract is trialed across several real `/iterate` sessions under Opus 4.7. If FB-032 materially reduces silent-decision friction, FB-033 is unnecessary. If FB-032 proves insufficient — silent decisions still slip through, or the output contract is bypassed — FB-033 becomes the structural backstop.

**Questions to resolve if FB-032 proves insufficient (likely via a decision record):**
- Should the spec-auditor be a subagent (`.claude/agents/`) or a Skill (`.claude/skills/`)? Depends on FB-020's findings on subagent-vs-skill context-window separation.
- Where does the PreToolUse hook live — template-owned `.claude/settings.json` (DEC-005 currently restricts that file to `permissions.allow` only), user-owned `settings.local.json`, or a documented example in `setup-checklist.md`?
- If auto mode (DEC-008 / FB-026 outcome) already covers most of the "block unapproved write" goal at the permission layer, does the hook reduce to a narrower belt-and-braces?
- Performance cost of running an adversarial diff-and-review before every spec/decision write.

**Impact scope if pursued:** potentially large — new `.claude/agents/spec-auditor.md` (or `.claude/skills/spec-auditor/`), hook wiring, integration with verify-agent contract.

**Likely outcome:** candidate DEC-009 after FB-032 trial, FB-020 research, and FB-026 resolution all close.

## FB-059: `/health-check` Part 5 selective sync conflates unsynced template content with genuine local additions (false-positive SKIP)

**Status:** new
**Captured:** 2026-05-15
**Source:** observed during downstream Styler `/health-check` after audit family v3.12.0 ship.

**Observation:** Part 5 (Template Sync Check) flagged two files as having "local additions" and offered selective sync that would SKIP both. Inspection showed the flag was correct for one file and a false-positive for the other:

- **`.claude/skills/dashboard-style/SKILL.md`** — 100% false positive. The diff was purely Stage 6 Option C content (kind-conditional `[Fix it]` action labels for the audit findings sub-section) that template shipped in v3.12.0 but Styler's local copy never received. Styler's `version.json` correctly read `template_version: 3.12.0` (the version field synced) but the file content stayed at Stage 6a state. Skipping the SKILL.md sync per the menu offer would have permanently prevented Styler from rendering `[Fix it]` labels until manual reconciliation.
- **`.claude/CLAUDE.md`** — correct flag. Styler genuinely added 2 project-specific rule imports (`brand-mention-provenance.md` per DEC-060, `feature-retirement.md` per FB-070 / § 27.1) plus their summary-table rows.

**Root cause hypothesis:** Part 5's detection compares downstream's *current* file content to template's *new* file content; any line-level diff is treated as a "local addition" warranting skip. This conflates two distinct conditions:
- (a) Downstream has unsynced template content (was at template_version N, template is at N+1, file content didn't sync along with the version field) → should sync
- (b) Downstream has genuinely user-added local content (file was customized after the last sync) → should preserve

The current algorithm can't distinguish these without per-file last-synced state.

**Proposed detection refinement:** Part 5 should compare downstream's file content to *the template version it last synced from*, not the *current template version*. The diff vs last-synced-version reveals genuine local additions. The diff vs current-template reveals all changes (sync delta + local additions). The intersection is what to sync without conflict; the symmetric difference is what to preserve as local. Requires the sync to record per-file last-synced template_version (or content hash). Could live in `dashboard-state.json` or a new `.claude/.sync-state.json` sidecar.

**Practical impact during this observation:** zero immediate harm because the `/audit-coherence` run that triggered the discovery had 0 bundle-eligible findings (so the missing `[Fix it]` labels weren't rendering anywhere). But future audits in Styler with bundle-eligible findings would have rendered with stale Stage 6a labels until manually reconciled.

**Workaround for affected projects (until Part 5 is refined):** when Part 5 offers selective sync, manually review the diff for each "skip" candidate via `diff <template-path> <project-path>`. If the diff is purely template content (lines present in template but not project), override the skip or manually copy the new template content into the project's file.

**Likely route:** scope-add to a new `/health-check` Part 5 refinement (not FB-058 — that's about `/work` decomposition path validation). Worth a research-light to confirm the proposed sidecar-based detection is feasible without restructuring the sync engine. Could also incorporate a "show me the diff" sub-action in the Part 5 menu so users can manually adjudicate per file.

## FB-060: Template-owned vs project-owned file ownership boundary not enforced or discoverable

**Status:** new
**Captured:** 2026-05-15
**Source:** surfaced during FB-059 root-cause investigation. The Styler local-additions case wasn't a one-off — it exposes a structural gap: the template documents file ownership as a convention but ships no enforcement, no detection, and no documented extension pattern.

**Observation:** Template files are conceptually split into ownership categories but the template doesn't make this machine-readable or user-discoverable. Three concrete failure modes observed via Styler:

1. **`.claude/CLAUDE.md` (template-owned) was modified by Styler** to add 2 project-specific rule imports + summary rows. The file's own preamble says `"This file is template-owned — do not edit directly. Project-specific instructions belong in ./CLAUDE.md (project root)."` — but nothing prevents or warns against the violation. Convention exists; enforcement doesn't.
2. **`.claude/skills/dashboard-style/SKILL.md` (template-owned)** got the same false-positive treatment from `/health-check` Part 5 even though it had zero local additions (FB-059) — because Part 5 doesn't know which files are template-owned vs project-extensible.
3. **Discoverability gap:** nowhere in the template is the extension pattern explicitly documented. A user wanting to add project-specific rule imports has to infer that root `./CLAUDE.md` is the right home (rather than `.claude/CLAUDE.md`). The template's `setup-checklist.md`, README, and rules files don't surface this.

**Three sub-concerns to address:**

- **Detection (machine-readable ownership).** `sync-manifest.json` currently lists files in flat arrays without tagging ownership category. Proposed schema extension: each file (or file pattern) carries a `category` field — `template_owned` (sync overwrites, never preserves diffs), `project_extensible` (sync respects local additions per FB-059 refinement), or `template_shipped_then_project_owned` (template ships once at setup, then project takes ownership; sync skips entirely). Existing files like `.claude/CLAUDE.md`, `.claude/rules/*.md`, `.claude/skills/*/SKILL.md`, `.claude/commands/*.md` (template-shipped variants) become `template_owned`. Project-extensible: `.claude/dashboard.md` (mostly template-generated but has user notes section). Template-shipped-then-project-owned: `.claude/spec_v1.md` (placeholder shipped, project replaces).
- **Enforcement / warning behavior.** Part 5 uses the category to decide sync behavior:
  - `template_owned` + project-side diff detected → warn user "your local additions to {file} violate the file-ownership convention; the file is being overwritten. Recommended migration: move additions to {root CLAUDE.md / .claude/rules/ / etc.}"
  - `project_extensible` → use FB-059's per-file last-synced-version detection
  - `template_shipped_then_project_owned` → skip sync entirely
- **Discoverability of extension hooks.** Add a "Project extension hooks" section to README or `setup-checklist.md` documenting where projects should add: rule imports (root `./CLAUDE.md`), project-specific rule files (`.claude/rules/` — auto-loaded if imported), project-specific commands (`.claude/commands/audit-{name}.md` per Component 9 of audit family proposal), project-specific skills (`.claude/skills/`), etc. One canonical map. Could live alongside the file-ownership category map.

**Practical impact observed in Styler:** modified `.claude/CLAUDE.md` caused FB-059's false-positive sync friction; no warning when the violation happened; user didn't know the right alternative. Took a multi-message investigation to surface the structural concern.

**Proposed actions:**
1. Extend `sync-manifest.json` schema with `category` per file/pattern. One-time data entry pass.
2. Refine `/health-check` Part 5 to honor categories (combines with FB-059's per-file last-synced-version detection for `project_extensible` files).
3. Add "Project Extension Hooks" section to `setup-checklist.md` and/or root README. Maps each common extension need to its canonical home.
4. Add a one-line preamble check to template-owned files: if user edits detected at sync time, surface the migration recommendation prominently (not buried in the offered-fixes menu).

**Dependencies / interactions:**
- FB-059 (sync detection refinement for `project_extensible`) is a precondition for the Part 5 refinement here.
- Component 9 of audit family proposal (project-to-template graduation) overlaps — both want clear conventions for "what's project, what's template."

**Likely route:** research-light scope. Could be one DEC covering both FB-059 and FB-060 (the ownership system + sync refinement together), since they're tightly coupled. Or two ships: FB-059's per-file last-synced-version mechanism first; FB-060's category schema + Part 5 refinement second.

**Behavioral complement (preventive layer, separate from structural actions 1-4):**

The structural fixes catch the violation at sync time. A behavioral guideline can prevent the violation at the *upstream* moment — when a Claude session is about to recommend the cross-project capture pattern ("land this change in the template, then run `/health-check` to sync the result back"). FB-002/003/004/005 all followed that pattern; FB-002's session missed a boundary check that surfaced as Styler's modified `.claude/CLAUDE.md` weeks later.

**Concrete prompt shape Claude should run BEFORE recommending the sync:**

> "Before recommending the template→sync flow, let me check whether your project has local additions to template-owned files that would conflict. Template-owned files: `.claude/CLAUDE.md`, `.claude/rules/*.md`, `.claude/skills/*/SKILL.md`, `.claude/support/reference/*.md`, `.claude/agents/*.md`. Diffing against last-synced template state OR enumerating project-side additions."

**Routing the findings:**
- Generically-applicable additions → recommend project→template promotion (FB-003/004/005-style) BEFORE accepting the sync. The promoted rules land first; the subsequent sync becomes a no-op convergence rather than a conflict.
- Project-specific additions → recommend migration to project-owned location (root `./CLAUDE.md`, `.claude/rules/` imported from root, etc.) BEFORE the sync.
- Either way, surface the boundary check at suggestion time, not at sync time.

**Style precedent (Styler-side cross-project capture session, 2026-05-15):** *"I should also flag: check styler-side local mods first. Diff against last-synced template state OR enumerate styler-additions to known-template-owned files before recommending sync. Recommend the file-ownership audit alongside the template feedback. 'Promote rule X to template' should pair with 'and also: anything in styler's template-owned files that should either go to root ./CLAUDE.md or also get promoted alongside?'"*

**Where this lives:** documentation, not template code. Candidate homes: a brief addition to `.claude/rules/agents.md` (alongside § "Behavioral Rules") OR a new "Cross-project capture protocol" sub-section in `.claude/support/reference/` (or appended to the existing graduation pattern in audit family proposal Component 9). Either way, no `/feedback review` ship needed for the behavioral piece itself — it's agent-guidance documentation. Could land alongside action 1 (root `CLAUDE.md` documentation pass).

**Independent of structural actions:** the behavioral guideline reduces the *frequency* of the violation; the structural actions reduce the *blast radius* when violations still happen. Both useful; neither blocks the other.

## FB-061: [RELOCATED — promoted to shipped feedback as FB-003]

**Status:** relocated 2026-05-15
**Source:** originally captured here; moved to `.claude/support/feedback/feedback.md` as **FB-003** to match the FB-002 cross-project capture precedent (small + additive + ready for `/feedback review` triage). See FB-062 below for the rationale on the dual-location convention.

**Cross-link:** the active item is `.claude/support/feedback/feedback.md` § FB-003 — promote `feature-retirement.md` from Styler to template. Triage via `/feedback review` will land the SKILL.md + `.claude/CLAUDE.md` + `audit-coherence.md` edits + version bump.

## FB-062: Two FB-NNN locations in template repo with overlapping purposes + namespace collision risk

**Status:** new
**Captured:** 2026-05-15
**Source:** surfaced during FB-060/FB-061 capture; recognized after Erik shared context from prior Styler session that authored FB-002 in shipped location (which then shipped as v3.13.0). The location convention is undocumented and the two namespaces could collide.

**Observation:** The template repo has two distinct files holding `FB-NNN` items, with overlapping but unclear purposes:

1. **`.claude/support/feedback/feedback.md`** (shipped) — `/feedback review` operates on it. Currently holds FB-003 (feature-retirement promotion). Archive holds FB-001 + FB-002 (both shipped). Used historically for: actionable items captured via `/feedback` in downstream projects OR direct edits from cross-project sessions when the target is a template-owned file (e.g., FB-002 was authored by Styler-side Claude targeting the template's `decomposition-heuristics/SKILL.md`).
2. **`template-maintenance/feedback.md`** (this file) — manual maintainer triage. Currently holds FB-011 + FB-033 (special-case trackers) + FB-058/059/060/061→relocated/062 (recent additions). Per root `CLAUDE.md`: *"Append manually; do NOT use `/feedback` in this repo."*

**Three concrete problems:**

1. **Namespace collision risk.** Both files use `FB-NNN`. FB-002 (shipped, archived) is a different item than FB-011 (maintenance, active). If shipped grows back into the 060s organically, it would collide with FB-058+ in maintenance. No enforcement against ID overlap; no shared counter.
2. **Convention boundary undocumented.** No clear rule for *"when does an item go in shipped vs maintenance?"* Implicit pattern (observed, not documented):
   - **Shipped:** actionable, ready or near-ready, can be triaged via `/feedback review` → ship → archive (e.g., FB-001 stale lock, FB-002 research-spike, FB-003 feature-retirement promotion).
   - **Maintenance:** special-case trackers (FB-011 scripts inventory tracking shipped families A+B + deferred C/D/E), trial gates (FB-033 spec-auditor gated on FB-032 outcome), items requiring design discussion before triage-able (FB-058 decomp pre-pass, FB-059 sync detection, FB-060 ownership boundary).
3. **Cross-project capture pattern unclear.** FB-002 demonstrated a working pattern: surface in project (Styler) → decide in project (DEC-082) → capture FB in template repo (shipped location) → template-side `/feedback review` triages → ship. But the choice of "shipped vs maintenance" for the template-side capture is itself implicit; a downstream user has to infer.

**Proposed actions (ranked by cost):**

- **Cheap (recommended start):** document the convention in root `CLAUDE.md`. Replace the current "do NOT use `/feedback` in this repo" line with a fuller two-location description with examples + the cross-project capture pattern explicitly. Possibly also add a one-line preamble to each FB file explaining its scope and pointing at the other.
- **Medium:** namespace the IDs differently — e.g., `TM-NNN` for template-maintenance items (no collision with `FB-NNN` shipped). Requires renaming existing maintenance items (FB-011, FB-033, FB-058, FB-059, FB-060, FB-062). Backward-compatibility cost in any external references.
- **Higher:** consolidate to one location with a `track:` field (`shipped` / `maintenance`). Single namespace, single source of truth. Requires schema migration, `/feedback review` update to honor `track:`, and a one-time merge of existing items.

**Likely route:** start cheap (documentation). Re-evaluate medium/higher only if observed friction warrants. The current dual-location pattern works in practice (FB-002 → v3.13.0 proves end-to-end), it just isn't legible without the mental model.

**Dependencies:** none — orthogonal to FB-058/059/060.

### Observed empirical instances (2026-05-16)

Two duplicate captures slipped past the Styler-side dedup check because the check probed for the **wrong filename** in the template-maintenance archive:

- **FB-004** ("Audit Tasks: literal-ID comparison" rule promotion) — duplicate of FB-042, which had already shipped in template v3.2.1 (2026-05-13) and was archived in `template-maintenance/feedback-archive.md`. The dedup check looked for `template-maintenance/archive.md` (incorrect — the file is `feedback-archive.md`) and reported "does not exist," missing the predecessor.
- **FB-005** ("MCP and Parallel Execution" rule promotion) — duplicate of FB-056, same root cause as above (FB-056 shipped in template v3.2.1 alongside FB-042).

Both archived as `absorbed (duplicate)` in `.claude/support/feedback/archive.md` on 2026-05-16. The dedup checks captured this assumption explicitly ("`template-maintenance/archive.md` does not exist"), so the gap is surface-able without forensic git work.

**Reinforces the "Cheap" proposed action above:** the documentation should explicitly enumerate **all four** template-side feedback files by exact filename, so cross-project capture sessions can copy-paste rather than infer:

1. `.claude/support/feedback/feedback.md` (active shipped queue)
2. `.claude/support/feedback/archive.md` (shipped queue archive)
3. `template-maintenance/feedback.md` (active maintenance queue)
4. `template-maintenance/feedback-archive.md` (maintenance queue archive — note: **NOT** `archive.md`)

The naming asymmetry (`feedback-archive.md` vs `archive.md`) is the structural booby trap. Renaming `template-maintenance/feedback-archive.md` → `template-maintenance/archive.md` to match the shipped-queue convention is another candidate fix (one-time rename, update any cross-references in active maintenance items), worth weighing against the cost of breaking git-blame continuity on the file.

## FB-063: Background-session auto-worktree breaks commands that read gitignored project state

**Status:** new
**Captured:** 2026-05-16
**Source:** observed mid-run during `/audit-coherence` in the Styler downstream project (background session, 2026-05-15). The audit aborted its initial write attempt with `InputValidationError` ("This background session hasn't isolated its changes yet. Call EnterWorktree first"). Entering the worktree then revealed the worktree's HEAD did not contain the gitignored inputs the audit needs (spec, decisions, feedback, tasks, dashboard — all gitignored under `.claude/**` in Styler's `.gitignore`).

**Observation:** The background-session preamble auto-routes any tool that writes files into an `EnterWorktree` call before "code changes." The current carve-out reads:

> *Before making any code changes, use the EnterWorktree tool to isolate your work from other parallel jobs and the user's working copy — unless your cwd is already under `.claude/worktrees/`, in which case you're already isolated. If you're only reading, searching, or answering questions, skip this and work in place.*

For projects whose primary state (`.claude/spec_v*.md`, `.claude/dashboard.md`, `.claude/support/decisions/`, `.claude/tasks/`, `.claude/support/feedback/`, etc.) is gitignored, this produces a structural failure mode:

1. Command attempts a write → blocked, told to enter worktree.
2. `EnterWorktree` succeeds — but the worktree's HEAD is a fresh checkout from `origin/main` (or local HEAD per `worktree.baseRef`), which does *not* contain any gitignored files.
3. Command runs in the worktree and discovers its inputs don't exist there.
4. To proceed, the command exits the worktree (`ExitWorktree { action: "remove", discard_changes: true }`), which destroys any writes the command made in steps 1-2.
5. Command resumes in the main tree, re-doing the captures via `Bash` redirects (`Bash` writes weren't blocked, only `Write`/`Edit` were).
6. Any files written via `Write`/`Edit` before exiting the worktree are lost — silently. The agent has no audit-trail signal to recreate them.

In the Styler audit run, this left two captured-inputs files missing (`meta.json`, `friction-open.jsonl`) from the otherwise-complete audit dir. The audit ran end-to-end (findings sound) but the input audit trail is incomplete. A future re-run or `/audit-coherence promote` flow that depends on those files would have to re-derive them.

**Why the worktree carve-out doesn't catch this:**

- The existing read-only carve-out (*"only reading, searching, or answering questions"*) doesn't cover audits, which read gitignored state and write to a gitignored audit dir under `.claude/support/audits/{cmd}-{ts}/`.
- "Code changes" the rule was designed to isolate are changes to tracked files. Audit writes are entirely to gitignored locations — they cannot collide with parallel jobs (timestamped subdirs) and cannot affect the user's tracked working copy.
- The worktree's *intended* isolation benefit (parallel-job safety + working-copy safety) is moot in this case: the writes go to gitignored paths, and the timestamp in the audit dir name prevents same-second collisions.
- The worktree's *cost* in this case is real: it severs access to the gitignored inputs the command needs to read.

**Affected commands (template-shipped):**

- `/audit-coherence` — observed failure. Reads spec, decisions, feedback, friction register, retired manifests; writes audit dir.
- `/audit-ui` — same dir pattern. Reads tracked code but writes audit dir. Less broken (inputs aren't gitignored) but the worktree dance is still wasted overhead.
- `/health-check` Part 7 (template repo only) — reads `interaction-logs/inbox/` (gitignored) and writes to `template-maintenance/feedback.md`. Same shape.
- Probably any future audit-family or interaction-log command.

**Proposed actions (ranked by cost):**

- **Cheap (recommended start):** add a one-line note to each audit command file (`commands/audit-coherence.md`, `commands/audit-ui.md`, and the audit family proposal as a documented contract) saying:

  > *Background-session note: this command reads gitignored project state and writes only to a gitignored audit dir. Do not enter a worktree before running it — the worktree's HEAD will not contain the gitignored inputs.*

  Lowest blast radius, surgical fix. The orchestrator dispatching the audit command would see this note in the command body and skip `EnterWorktree`.

- **Medium:** extend the background-session preamble's carve-out from *"only reading, searching, or answering questions"* to *"or writes only to gitignored locations under `.claude/support/audits/`, `.claude/support/workspace/`, or other gitignored audit/scratch paths."* Generalizes the rule for any future command that operates on gitignored state. Harder to verify automatically (the agent would need to know which paths are gitignored, which it can derive from `.gitignore` but isn't always front-of-mind).

- **Higher:** worktree-creation could optionally bind-mount or copy gitignored files into the worktree, so worktree HEAD reflects working-copy reality. Tool-level change with much broader implications (affects every worktree, not just audit commands). Not recommended unless other gitignored-state cases pile up.

**Likely route:** start with **Cheap** — three one-line additions to existing command files. If the audit family grows or the `/health-check` Part 7 path hits the same trap, fold into **Medium** at that time.

**Concrete diff sketch (Cheap):** at the top of `commands/audit-coherence.md`, above `## Usage`, add a `## Background-session note` heading with the line above. Same for `commands/audit-ui.md`. Optionally add a corresponding bullet to `audit-command-family-proposal.md` Component 5 ("/health-check dispatcher integration").

**Dependencies:** none. Surfaces an interaction between the audit family (template-shipped) and the background-session preamble (template-shipped). Both files are template-owned; fix lands wholly inside this repo.

**Cross-reference:** Styler audit run that surfaced this — `.claude/support/audits/coherence-2026-05-15-2337/` (in `~/Developer/styler/`). The missing files in that audit dir's `inputs/` are the visible artifact of the failure mode.
