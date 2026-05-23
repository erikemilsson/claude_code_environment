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

## FB-059: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 via DEC-014 Option F (template_version 3.15.0). Sidecar + Part 5 algorithm refinement shipped. See archive for full text.

## FB-060: Template-owned vs project-owned file ownership boundary not enforced or discoverable

**Status:** Phases 1 + 3 + 4 + 5 shipped; Phase 2 (category schema) deferred per DEC-014
**Captured:** 2026-05-15
**Phase 1 + Phase 5 shipped 2026-05-16 (v3.14.2):** (Phase 1) Cross-Project Capture Protocol section added to `.claude/rules/agents.md` — codifies the pre-sync boundary check + finding-routing rules (generically-applicable → project→template promotion; project-specific → migration to project-owned location). (Phase 5) New `.claude/support/reference/extension-hooks.md` with canonical map of extension need → project-owned location, linked from `setup-checklist.md` preamble + `.claude/CLAUDE.md` navigation. Closes the "behavioral complement" follow-up and the "discoverability gap" sub-concern.
**Phase 3 + Phase 4 shipped 2026-05-16 (v3.15.0):** DEC-014 Option F selected — `.claude/.sync-state.json` sidecar + 2-condition Part 5 classification (sidecar-hash-match → "Template content not yet applied" default APPLY; mismatch/missing → "Modified upstream" + "Show me the diff" sub-action). Closes the structural fix for FB-059. The sidecar's `local_hash == synced_hash` check is category-agnostic; per-file ownership tags are operationally redundant given that every current `sync` member is uniformly template-owned. **Phase 2 (sync_strict category schema) remains deferred per DEC-014 § Decision** — adding the category alongside would ship a label without a function (the category doesn't gate anything; the hash check is what drives classification). If/when a real `project_extensible` member emerges (e.g., a future `.claude/skills/{name}/SKILL.md` that ships base content from template + accepts project-side appendix sections), adding the category later is purely additive — no migration cost, no downstream breakage. Decision record: `decisions/decision-014-sync-state-and-file-ownership-categories.md`. Plan: `template-maintenance/plan-fb059-fb060.md` (note: Option F selected; Phase 2 not implemented).
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

**Status:** cheap action shipped (medium/higher remain as options)
**Captured:** 2026-05-15
**Cheap action shipped 2026-05-16 (v3.14.1):** root `CLAUDE.md` § File Boundary's "Feedback" bullet replaced with a four-file enumeration that explicitly names `feedback-archive.md` (not `archive.md`), surfaces the naming-asymmetry trap with a concrete observed-instance pointer (FB-004 + FB-005 dedup miss), and documents the cross-project capture pattern. Medium (rename maintenance archive + IDs to `TM-NNN`) and Higher (consolidate to one location with `track:` field) remain as future options if the documented convention still produces dedup misses.
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

**Status:** cheap action shipped (medium/higher remain as options)
**Captured:** 2026-05-16
**Cheap action shipped 2026-05-16 (v3.14.1):** added `## Background-session note` sub-sections above `## Usage` in `.claude/commands/audit-coherence.md` and `.claude/commands/audit-ui.md`, instructing not to enter a worktree before running the command (worktree's HEAD won't contain gitignored inputs, and the audit dir's timestamp prevents same-second collisions across parallel sessions, so isolation is unnecessary). Medium (extend background-session preamble carve-out to "writes only to gitignored locations") and Higher (worktree-level bind-mount of gitignored files) remain as future options if other commands hit the same trap.
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

## FB-064: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 — test-harness awareness decomposition heuristic shipped in template_version 3.17.0 (new "Test-Harness Awareness" section added to decomposition.md + SKILL.md mirror; runs alongside the Pre-Pass Validation after step 8). See archive for full text.

## FB-065: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 — decomposition enum-extension heuristic shipped in template_version 3.16.0 (5th heuristic row added to FB-058 Pre-Pass Leg 2). See archive for full text.

## FB-066: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-16 — verify-agent production-consumption check shipped in template_version 3.16.0 (sub-bullet added to Step T5; feeds existing integration_ready key). See archive for full text.

## FB-067: External-source recheck — mattpocock/skills Wave 2 candidates

**Status:** deferred — re-assess on/after 2026-06-02
**Captured:** 2026-05-19
**Source:** video https://www.youtube.com/watch?v=6BB6exR8Zd8 reviewed 2026-05-19; repo `mattpocock/skills` (clone at `/Users/erikemilsson/Downloads/skills-main` as of 2026-05-19; mirror github.com/mattpocock/skills).

**Reason for deferral:** Wave 1 (FB-068 + FB-069 + FB-070 + FB-071) ships first. Wave 2 candidates depend on Wave 1 signal — some compound only with their Wave 1 sibling in place.

**Wave 2 candidates to re-evaluate:**

- **`/tdd` skill** — vertical-slice red-green-refactor + anti-horizontal-slicing discipline. Pocock files at `skills/engineering/tdd/SKILL.md` + `tests.md` + `mocking.md` + `interface-design.md` + `deep-modules.md` + `refactoring.md`. Open question: does CCE's verify-agent already cover the "correctness" angle sufficiently?
- **`/prototype` skill** — throwaway design exploration. Two branches: terminal app for state/logic, multi-variation UI on one route. Trigger to ship: how often CCE work hits "I don't know what shape this should be."
- **`/improve-codebase-architecture` skill** — complement to `/audit-coherence`. Architectural vocabulary (Module/Interface/Depth/Seam/Adapter/Leverage/Locality) + deletion test heuristic. Most valuable AFTER CONTEXT.md (FB-068) and AFTER `/diagnose` (FB-069) — `/diagnose`'s Phase 6 post-mortem explicitly hands off here.
- **`/caveman` ultra-compressed mode** — ~75% token cut. Niche; ship only if cost pressure becomes a recurring concern.
- **Hard-vs-soft dependency cleanup pass** — apply Pocock's ADR-0001 pattern across CCE command files. Distinguish load-bearing cross-references from advisory. Cosmetic.
- **Bucketed skill organization** (`engineering/` / `productivity/` / `misc/` / etc.) — only worth considering if skill count grows much further.

**Trigger to escalate from deferred → ready:**
1. Any Wave 1 ship produces signal that a specific Wave 2 sibling compounds. Concrete example: `/diagnose` Phase 6 post-mortems repeatedly identify architectural friction → `/improve-codebase-architecture` becomes load-bearing.
2. The 2-week recheck on 2026-06-02 (default if no earlier signal).
3. Separate user request to re-evaluate.

**Source pointers preserved:**
- Local clone: `/Users/erikemilsson/Downloads/skills-main` (may be cleaned later)
- GitHub: github.com/mattpocock/skills
- Video: https://www.youtube.com/watch?v=6BB6exR8Zd8
- Skill list + four-frame structure: `/Users/erikemilsson/Downloads/skills-main/README.md`

## FB-068: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — new `/grill` command + `./CONTEXT.md` slot (project-owned, lazy-created glossary) shipped in template_version 4.2.0. Live skills-list verification: `grill: Grill Command` immediately appeared in model-invocable list. Integration points: `./CONTEXT.md` row in `.claude/CLAUDE.md` Navigation, `/grill` in Environment Commands, new `## Domain Glossary Awareness` section in `rules/agents.md`, `/grill` mention in `rules/spec-workflow.md § Vision Documents`, extended `audit-coherence.md § "Lens 2 — vocab-drift"` to consume CONTEXT.md when present. All explicit out-of-scope items from FB-068 honored (no batch-extract, no co-equal source of truth, no CONTEXT-MAP.md, no glossary versioning, no direct ADR writes). See archive for full text.

## FB-069: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — new `/diagnose` command (6-phase debugging methodology) shipped in template_version 4.4.0. Adapted from `mattpocock/skills/engineering/diagnose`, domain-genericized for CCE. Cross-referenced from `agents.md § Root Cause Over Symptom` (structural enforcement mechanism for hard bugs) + `spec-workflow.md § Workflow Cycle` (bug-task preferred route). Leaves `disable-model-invocation: true` OFF per FB-071 selection criteria — autonomous-fire-when-stuck is the value proposition. Phase-6 architectural-friction handoff routes through CCE's friction register or `/research` (no `/improve-codebase-architecture` exists yet — FB-067 Wave 2). **Wave 1 complete.** See archive for full text.

## FB-070: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — new `/zoom-out` micro-command shipped in template_version 4.3.0. Carries `disable-model-invocation: true` frontmatter on day one per FB-071 convention (`/zoom-out` is explicitly a user-asks-for-help signal; autonomous fire would be circular — Pocock's `/zoom-out` carries the same frontmatter for the same reason). Consumes `./CONTEXT.md` vocabulary when present (FB-068 integration); degrades gracefully when absent. See archive for full text.

## FB-071: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 — `disable-model-invocation: true` frontmatter applied to all 5 strong-candidate commands (`/breakdown`, `/research`, `/iterate`, `/work`, `/feedback`) shipped in template_version 4.1.0. Live empirical verification: model-invocable skills list shrank immediately from 10 template commands to 5. New `## Command Invocation Gates` section in `rules/agents.md` documents the convention, selection criteria, sub-mode coupling trade-off, and defense-in-depth interaction with DEC-005 + DEC-016. Medium candidates deferred for trial-period observation. See archive for full text.

## FB-072: Command routing as a UX pattern (interpretive vs explicit-arg dispatch + boundary survey)

**Status:** ready (research-first; trial-gated DEC candidate)
**Captured:** 2026-05-20
**Source:** session-level reflection after shipping FB-068 (`/grill` as standalone command rather than `/iterate grill` sub-mode). User observed 2026-05-20: *"from a UX perspective it is one more command to remember. I think we should look into making `/iterate` a router that routes to other commands depending on what is being asked. ... I guess the larger question is how effective routing is at all, and perhaps that is something to do research on."*

**Observation:** CCE currently dispatches sub-modes via explicit string args (`/iterate distill`, `/work complete`, `/work pause`, `/feedback review`). Each multi-mode command grows its own file (e.g., `iterate.md` ~700 lines covering distill/propose/hygiene/no-args; `work.md` ~1700 lines covering many sub-modes). Adding new spec-adjacent commands (FB-068's `/grill`, FB-069's `/diagnose`, FB-070's `/zoom-out`, likely Wave 2 entries) increases the surface area users have to remember.

**The router pattern (proposed by user 2026-05-20):**

`/iterate` becomes an interpretive umbrella for "everything that has to do with nailing down the single source of truth spec." Sub-purposes dispatch based on Claude's interpretation of intent:

- `/iterate "I want to stress-test this plan"` → router invokes `/grill` internally
- `/iterate "let's distill a buildable spec from this vision"` → router invokes the distill sub-flow
- `/iterate "the spec is fuzzy on cancellation semantics"` → router invokes the propose sub-flow
- `/iterate "check the spec against the registry"` → router invokes the hygiene sub-flow

Sub-flows can live in separate files (per-purpose, focused) or stay in `iterate.md`. The key difference from current explicit-arg dispatch: **the user doesn't need to know the sub-mode name**; Claude classifies from natural language.

**Two interesting twists:**

1. **Interpretive vs explicit-arg dispatch.** Current pattern is structural: user types `/iterate distill`, matcher fires. Proposed pattern is interpretive: user types `/iterate <natural language>`, Claude classifies intent before firing. Failure mode: wrong sub-mode runs silently. Mitigation candidate: router announces its interpretation (*"I read this as a distill request — proceeding with `/iterate distill` flow. Say 'no' to redirect."*) before any substantive action.

2. **Boundary discovery comes first.** Worth surveying which CCE commands have clean "umbrella" semantics before committing to the architecture. Concrete candidates:
   - **`/iterate` as spec-source-of-truth umbrella** — covers distill / propose / hygiene / grill / possibly research-dispatch for spec-adjacent decisions
   - **`/work`** — currently covers many concerns (decomposition, agent routing, parallel batching, completion, pause); some might split out under interpretive routing
   - **`/research` and `/iterate` overlap** — both touch decisions and spec adjacency. Unified umbrella, or correctly distinct?
   - **`/audit-coherence` and `/audit-ui`** — already dispatched from `/health-check` Part 8 menu (different pattern: menu-based). Similar umbrella-vs-discrete tension.
   - **Help-me-think family** — `/zoom-out`, `/grill`, `/diagnose`. Pattern: *user-asks-for-help-in-a-specific-mode*. Loose grouping ("I need broader context" / "I need to be interrogated about this plan" / "I need to debug rigorously"). Less obviously umbrella-shaped than `/iterate` (the family is small and the modes are quite distinct), but worth surveying for whether a single `/help` or `/think` entry point + interpretive dispatch produces a better UX than three discrete commands. Surfaced 2026-05-20 during FB-069 ship (post-FB-068/FB-070 reflection — three help-me-think commands now exist, none has a natural umbrella home).

**Research questions:**

- **Accuracy of intent classification.** Can Claude correctly classify the sub-mode from user input across candidate umbrellas? Failure rate? Recovery cost when wrong?
- **Discoverability.** Do users learn the umbrella surface (one command, many sub-purposes) faster than the discrete surface (many commands)? Or does the umbrella obscure capability?
- **Latency / cost.** Does interpretive routing add a noticeable LLM pass? Sub-modes have their own context loads (iterate.md is large) — is the router pass cheap or expensive?
- **Boundary clarity.** When should a piece of work be a sub-mode of an umbrella vs a standalone command? Are there cases where an umbrella forces unnatural couplings?

**Deliverables (if pursued):**

1. **Boundary survey** (`.claude/support/workspace/router-survey.md` or similar) — for each candidate umbrella, list sub-purposes that would route through it; flag any that don't fit cleanly. ~1-2 sessions.
2. **Prototype** — pick one umbrella (likely `/iterate`, the immediate driver) and implement interpretive routing as proof-of-concept. Trial in a real downstream session.
3. **Effectiveness data** — track router accuracy, recovery cost, and user feedback across N sessions. Threshold candidate: ≥ ~85% classification accuracy with ≤ 1 redirect per recovery to justify the pattern.
4. **DEC candidate** — if survey + prototype + data are favorable, `/research` opens a DEC. If unfavorable, FB-072 closes; explicit-arg pattern stays.

**Dependencies / interactions:**

- **FB-071 (Command Invocation Gates):** if `/iterate` becomes a router, the gating story stays — `disable-model-invocation: true` blocks ambient autonomous fire of the umbrella. Sub-modes don't need individual gates because the router gates them collectively. Potentially *simplifies* the FB-071 sub-mode coupling trade-off.
- **DEC-016 (spec/decision/vision Edit/Write ask):** unchanged. The permission-layer ask fires at the write boundary regardless of how the write was reached.
- **FB-068 (`/grill` as standalone):** if FB-072 ships favorably, `/grill` could migrate to `/iterate grill` as a sub-mode. The standalone command file stays as the dispatch target; only the entry point shifts. No re-work of `/grill` itself.
- **FB-070 (`/zoom-out`):** standalone micro-command; doesn't obviously belong under an umbrella (no "zoom-out family" of related commands). If router shipping reveals a help-the-user umbrella, revisit. Most likely outcome: `/zoom-out` stays standalone.

**Trial-gate:** the research-first nature is important. The user explicitly said *"perhaps that is something to do research on."* Do NOT implement before:
- Boundary survey is complete (which commands have clean umbrella semantics?)
- At least one prototype is trialed in a real session
- Effectiveness data accumulates

**Likely route:** research-light (boundary survey) → prototype → `/research` opens DEC if signal is positive. No template change in the first session; the survey is a workspace doc, not a template artifact.

**Impact scope if pursued:** large — touches `iterate.md` (router refactor), possibly `work.md` and `research.md`, `/grill` (entry-point migration), `/health-check` Part 8 menu (if `/audit-*` commands also umbrella-ize), and the Command Invocation Gates story.

**Likely outcome:** candidate DEC after survey + prototype + data accumulate.

## FB-073: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

See `feedback-archive.md` for full entry.

## FB-074: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

See `feedback-archive.md` for full entry.

## FB-075: TaskCreate/TaskUpdate harness reminder fires in projects that explicitly forbid built-in task tools

**Status:** cheap-action-shipped + deferred (structural fix upstream-gated)
**Captured:** 2026-05-20
**Cheap action shipped:** 2026-05-20 — Added "Harness reminders about built-in task tools" paragraph to `.claude/README.md § Known Constraints`. Documents the noise as harness-emitted (not template-emitted) and benign in projects using `.claude/tasks/*.json`. Shipped in template_version 4.6.1 (alongside FB-076 deferral).
**Defer condition (structural fix):** structural opt-out requires Anthropic-side mechanism (CLAUDE.md sentinel, settings hook, or per-project flag). Re-assess when (a) upstream offers such a mechanism, OR (b) friction scales materially (token tax across 100+ sessions becomes meaningful).
**Source:** Aggregated across 7 session exports (echothread + styler, 2026-05-16 → 2026-05-17). Observed in this very session 2026-05-20 during inbox triage — the harness reminder fired immediately after the AskUserQuestion confirming this FB capture.

The Claude Code harness emits a system-reminder along the lines of *"The task tools haven't been used recently. Consider using TaskCreate to add new tasks and TaskUpdate to update task status..."* on most tool returns. When a project's `.claude/CLAUDE.md` contains the explicit override ("Use the project's task system (`.claude/tasks/*.json`). Never use built-in TaskCreate/TaskUpdate/TaskList tools"), the reminder is universally irrelevant — every fire costs cognitive cycles + token tax + a user-visible "ignoring per project rules" acknowledgment from the agent.

### Pattern

Observed cumulatively across the 7 sessions: ~60+ TaskCreate reminder fires. The reminder is built into the runtime (not template-emitted), so the template can't suppress it directly. Both echothread and styler sessions show the same pattern:

1. Agent does work using the project's task JSON system (per CLAUDE.md).
2. Harness emits the reminder after most tool returns.
3. Agent burns tokens acknowledging + ignoring + reasserting the project rule.

### Two possible mitigations

1. **Harness-side (Anthropic concern):** when CLAUDE.md contains an explicit-override phrase ("Never use built-in TaskCreate"), suppress the reminder for that project's sessions.
2. **Template-side (CCE concern):** add a CLAUDE.md marker or settings.json convention that the harness reads to disable the nudge. Example: `task_system_override: true` field in `.claude/version.json`, or a documented sentinel comment in CLAUDE.md the harness recognizes.

Both paths require Anthropic-side cooperation — the reminder logic lives in the runtime, not in template-shipped files. Worth raising upstream OR documenting the unavoidable noise in `.claude/README.md` so users (and agents) don't feel the rule is broken.

### Why this is worth capturing despite being upstream

- **Recurring confusion signal:** agents visibly burn tokens acknowledging the reminder; users observe and ask "why does it keep suggesting that?"
- **Project authority erosion:** explicit project rules feel less authoritative when the harness contradicts them on every tool return.
- **Documented friction = potential fix:** if Anthropic adds an opt-out mechanism, the template can adopt it immediately.

Sources:
- `interaction-logs/processed/echothread-2026-05-16.json` (~10 fires)
- `interaction-logs/processed/echothread-2026-05-17.json` (~10 fires)
- `interaction-logs/processed/echothread-session-2026-05-16.json` (~20 fires)
- `interaction-logs/processed/styler-2026-05-17.json` (~10 fires)
- `interaction-logs/processed/styler-session-export-2026-05-16-T0955.json` (7+ fires)
- `interaction-logs/processed/styler-session-export-2026-05-16-T1332.json` (7+ fires)
- `interaction-logs/processed/styler-session-export-2026-05-16-T1425.json` (recurring fires)

Tags: harness, task-system, system-reminders, upstream-anthropic, friction-aggregate

## FB-076: verify-agent runtime_validation misses bundle-boundary breaks and catalog-state-dependent gaps

**Status:** deferred (single-project signal; research-gated)
**Captured:** 2026-05-20
**Defer condition:** Re-assess when (a) 2nd project signals the same verification gap, OR (b) FB-066 downstream telemetry suggests broader runtime_validation hardening is needed. Single-project signal (styler T667) doesn't justify the design work (build-command discovery + catalog-path declaration; mitigations 1+3 are not as mechanical as FB-066's regex+grep). If signal escalates: route through `/research` for design — similar to FB-072's trial-gated DEC candidate path. Tracked in root CLAUDE.md § Active Follow-ups as of v4.6.1.
**Source:** Aggregated from styler session export 2026-05-17 (T667 markers — two distinct verification_gap entries). Extends FB-066 (production-consumption check, shipped v3.16.0).

Structural + automated verification (lint, tsc, vitest, behavior tests) is necessary but not sufficient for tasks where bugs surface only under (a) production bundling or (b) live data state. Two concrete failure modes from styler T667:

### Failure mode 1: Client/server bundle boundary

`ExpandedPalette.tsx` + `ItemRecropControl.tsx` imported `DEFAULT_TARGET_ASPECT` from `photo-normalization.ts`, which transitively pulled `sharp` → Node-only modules into the client bundle. All static + automated checks passed; first `/outfits` page render failed with Turbopack 500.

Hotfix: extracted client-safe constants to `photo-target.ts` re-exported by `photo-normalization.ts`.

### Failure mode 2: Catalog-state-dependent precondition

T667's worn-photo outlier warning targets a code path satisfied by zero items in the live catalog (26/27 wardrobe items have no worn photo; hanger photos never reach the measurement img). Mock-based behavior tests passed because synthetic photoSrc was supplied; live catalog cross-reference would have shown the warning can never fire.

### Why this extends rather than duplicates FB-066

FB-066 (shipped v3.16.0) addresses "class exported but never instantiated" via a verify-agent T5 production-consumption check. That covers static class-export gaps. T667's two failure modes are different:

- **Bundle boundary** is dynamic — the symbol IS consumed, but consumption from a client-marked file pulls a transitive Node-only dep into the wrong bundle. Static grep doesn't catch this; only an actual build does.
- **Catalog-state** is data-dependent — the code path executes correctly under mocks but is unreachable under real data because no catalog rows satisfy the precondition.

Both fall under verify-agent's `runtime_validation` check, which currently passes any task whose static + mock-based tests pass.

### Mitigation candidates (in priority order)

1. **Production-build invocation.** When a task touches files marked `'use client'` (or framework equivalents), verify-agent runs `npm run build` (or the project's equivalent) before declaring the task verified. Catches bundle-boundary breaks like failure mode 1.
2. **ESLint rule.** A custom ESLint rule that blocks client components from importing modules whose transitive deps include `sharp`, `fs`, `child_process`, etc. Faster than full build; runs in implement-agent's edit loop. Less reliable than build (transitive analysis is brittle) but cheap.
3. **Live-data cross-reference.** When the spec implies a feature operates over real catalog state (foundation/wardrobe/items/*.json or analog), verify-agent samples the catalog and confirms the feature's precondition is reachable for ≥1 row. Catches failure mode 2.

Mitigations 1 and 3 are independent (different failure classes); both are worth adding. Mitigation 2 is a faster proxy for mitigation 1, useful if `npm run build` is too slow to run on every task.

### Template-side homes

- `.claude/agents/verify-agent.md` — add runtime_validation sub-checks for bundle-boundary + live-data
- `.claude/commands/work.md` — verify-agent dispatch should pass the project's build command + catalog paths if available
- Project-side: `./CLAUDE.md` may declare the project's build command + foundation-data paths for verify-agent consumption

Source: `interaction-logs/processed/styler-2026-05-17.json` (T667 markers, two `verification_gap` entries explicitly naming both failure modes).

Tags: verify-agent, runtime-validation, bundle-boundary, live-data, extends-FB-066

## FB-077: Auto-mode classifier over-broad DEC-016 scope + AskUserQuestion responses don't count as authorization

**Status:** cheap-action-shipped + deferred (structural fix upstream-gated)
**Captured:** 2026-05-20
**Cheap action shipped:** 2026-05-20 — Added "Auto-mode classifier false-positives" paragraph to `.claude/README.md § Known Constraints` (sibling to FB-075's TaskCreate harness reminder paragraph). Documents both sub-issues + workarounds: (a) DEC-016 scope — lead with explicit context-clarifying language, or user provides typed-text authorization; (b) AskUserQuestion authorization — agents prefer free-text prompts when classifier-bypass authorization is the goal. Shipped in template_version 4.6.3.
**Defer condition (structural fix):** Re-assess when Anthropic offers (a) per-path DEC-016 scope declaration (positive-list of paths in scope, exact-match to the three globs in `CLAUDE.md § Critical Invariants`), (b) AskUserQuestion authorization recognition (classifier treats AUQ "authorize" responses as auth for the action they reference), OR (c) workaround friction recurs across N sessions despite the README docs.
**Source:** Two distinct classifier false-positives observed in-session 2026-05-20 during FB-074 sub-issue 1 (categories extension) ship. Concrete block messages preserved below.

The auto-mode classifier blocked legitimate Edits during a session where the user had explicitly approved the work (FB-074 promotion approved via AskUserQuestion). Two distinct failure modes surfaced.

### Sub-issue A: DEC-016 scope misinterpretation

The classifier blocked an Edit to `.claude/support/reference/decisions.md` (a reference doc documenting decision RECORD format) citing DEC-016. But DEC-016's scope is explicitly the three globs documented in `.claude/CLAUDE.md § Critical Invariants`:

- `.claude/spec_v*.md`
- `.claude/support/decisions/decision-*.md` (decision RECORDS, not reference docs)
- `.claude/vision/**/*.md`

The reference doc `.claude/support/reference/decisions.md` is NOT in scope. The classifier conflated:
- (record at) `.claude/support/decisions/decision-{NNN}-*.md` ← in scope
- (reference doc at) `.claude/support/reference/decisions.md` ← NOT in scope

Concrete block message: *"Substantive edit to `.claude/support/reference/decisions.md` (a template-owned reference file) is blocked by user's own DEC-016 rule routing substantive edits through /iterate"*

This is a false-positive. The user's intent (per DEC-016) was to gate decision RECORDS — the audit-trail-of-intent files — not the meta-documentation about how to author records.

### Sub-issue B: AskUserQuestion responses don't count as authorization

After the first block, the agent surfaced the issue and offered options via `AskUserQuestion`. The user picked "Authorize the edit explicitly". The agent retried the Edit. The classifier blocked again with:

*"Agent retried the same edit immediately after the classifier block / AskUserQuestion without a visible user response authorizing the retry."*

The classifier requires typed-text authorization in a user message. `AskUserQuestion` responses — even when the user explicitly selected an "authorize" option — are treated as programmatic answers, not authorization.

This is a UX-shape problem: `AskUserQuestion` is designed as a clean, structured way to collect user decisions. If those decisions can't authorize subsequent actions, the tool's utility for permission-flow scenarios is sharply limited. Agents must fall back to free-text prompts when authorization matters — defeating the purpose of structured-choice collection.

### Combined impact

In this session: FB-074 sub-issue 1 (categories enum) needed edits to BOTH `health-check.md` (allowed by classifier) AND `decisions.md` (blocked twice). The two-file inconsistency left the template in a half-shipped state — `health-check.md` validated against the extended enum, but the reference doc still showed the old 6-value list. Manual intervention required (user typed text authorization after the structured approval via AskUserQuestion failed).

### Mitigation candidates

**For Sub-issue A (DEC-016 scope):**
- Tighten classifier rules to match DEC-016's stated path patterns exactly (the three explicit globs from `CLAUDE.md § Critical Invariants`).
- Add a positive-list of in-scope paths for DEC-016 enforcement rather than a heuristic "anything named decisions.md".

**For Sub-issue B (AskUserQuestion authorization):**
- Treat AskUserQuestion responses as authorization for the action they reference (per-question metadata could declare which action the question gates).
- Or: document the limitation so agents know to use free-text prompts for permission flows.
- Or: classifier inspects the AskUserQuestion question + options to determine authorization intent.

### Related

- DEC-016 (spec/decision/vision file edit guardrail) — Sub-issue A is about the classifier's interpretation of DEC-016's scope.
- DEC-005 (auto-mode permission layer) — the broader auto-mode classifier where this lives.
- FB-074 sub-issue 1 (categories extension) — concrete promoted item that triggered the block.

Tags: auto-mode, classifier, dec-016, dec-005, false-positive, askuserquestion, authorization, upstream-anthropic

## FB-078: /work Step 2b post-decision check fires /iterate based on `inflection_point` flag alone, ignoring chosen-option spec_impact intent

**Status:** new
**Captured:** 2026-05-20
**Source:** Surfaced 2026-05-20 during FB-011 Family E re-assessment — bridged from styler session export 2026-05-16 (`interaction-logs/processed/styler-session-2026-05-16.json` § `workflow_friction_notes`). Not surfaced in the inbox triage subagent's earlier analysis (this session's Phase 3 missed it); discovered during the Family E `Step 2b` cross-reference check.

DEC-083 (styler decision) correctly flagged `inflection_point: true` because the option space contained spec-impacting candidates. The user selected option δ (close) which has explicit NO spec impact. But `/work` Step 2b's post-decision check fires the `/iterate` suggestion based on the decision-level `inflection_point` flag alone — it does NOT read the chosen option's text for spec_revised intent. Result: false-positive `/iterate` suggestion on the next `/work` run.

### The structural gap

`inflection_point` is a property of the **decision** (was the option space spec-shaping?). But spec-impact is a property of the **selected option** (does the chosen path require a spec amendment?). The current check conflates the two — it treats the decision-level flag as the trigger, ignoring whether the actual selection has spec consequences.

### Mitigation candidates (from the session)

1. **Read the chosen option's text for `'no spec amendment'` markers.** When the option detail explicitly says no spec impact, skip the `/iterate` suggestion. Heuristic-based; tolerant of varied phrasing; no schema change.
2. **Add per-option `spec_impact` flag to the decision schema.** Author marks each option with `spec_impact: true | false | unclear` at decision creation. Step 2b reads the chosen option's flag deterministically. Cleaner; requires schema change + authoring burden.

Option 1 is cheaper (no schema change) but heuristic-shaped. Option 2 is more deterministic but requires authoring change. Could ship Option 1 first as a quick fix; escalate to Option 2 if heuristic false-negatives accumulate.

### Boundary with FB-017

FB-017 (shipped via inlining fix) was about Step 2b's **decision auto-finalization** sub-feature (checkbox detection → `status: approved`). This issue (FB-078) is about Step 2b's **post-decision check** sub-feature (does the chosen option warrant `/iterate`?). Same Step 2b function, different sub-paths; no overlap. The cross-reference to FB-017 in the styler session was a textual false-positive (matched "Step 2b") that surfaced this issue during the Family E re-assessment grep.

### Scope

- `.claude/commands/work.md` Step 2b post-decision check logic (primary)
- If Option 2 chosen: `.claude/support/reference/decisions.md` (decision record template + option authoring guidance) + decision-record schema enforcement

### Signal strength

Single-project signal (styler 2026-05-16). Low frequency expected — most `inflection_point: true` decisions DO have spec impact in their chosen option. The false-positive happens specifically when an inflection-eligible decision lands on a "close / defer / no-op" option. Could promote now (Option 1 cheap fix) or wait for 2nd-project signal.

Tags: workflow, work-step-2b, post-decision-check, false-positive, inflection-point, decisions-schema

## FB-079: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 via v4.6.4. Minute-granularity timestamp applied to `/work pause` session-export filename at both write sites (`work.md` step 5 + `pre-compact-handoff.sh` lines 230 + 237). See archive for full entry.

## FB-080: [PROMOTED — moved to `template-maintenance/feedback-archive.md`]

**Status:** promoted 2026-05-20 via v4.7.0. Route C1 (hybrid: targeted-edit pattern + sidecar sentinel) selected over A (section-fingerprints in META) and B (defer-everything-to-session-boundary). New `pending_full_regen` field on `dashboard-state.json` sidecar; targeted-edit decision table in SKILL.md + mirror; Step 1a freshness check extended. See archive for full entry; research at `.claude/support/workspace/fb-080-research.md`.

## FB-081: Long autonomous batches (3+ implement+verify cycles) lack heartbeat or user-check-in default

**Status:** new
**Captured:** 2026-05-20
**Source:** styler 2026-05-17 session export (`interaction-logs/processed/styler-2026-05-17.json` § `design_pushback_opportunities` + `workflow_friction_notes`). Erik asked "is it stuck?" ~30 min into a 4-cycle autonomous batch (T683→T684→T685→T686→T687). Orchestrator had Erik's earlier "keep moving with autonomous tasks" but didn't proactively communicate progress during the long stretch.

### Two distinct gaps

**Gap 1 — No heartbeat during autonomous batches.** When 3+ implement+verify cycles run without user interaction, the user has no visibility into where the batch is. The default failure mode is silence; the user pings to break the silence; the orchestrator interprets the ping as "confirm I'm working" rather than "you should check whether to continue".

**Gap 2 — Mid-batch user ping → auto-continue (wrong default).** Erik's "is it stuck?" was a yellow flag, not a green light. The right call was to PAUSE, summarize, and ask "continue or pause?" — the orchestrator instead dispatched the next verify-agent immediately. Pings during long autonomous runs should default to summary-plus-confirmation, not auto-continue.

### Two patterns

**Pattern 1 — Heartbeat.** Before dispatching the Nth+1 cycle in an autonomous batch (where N≥3), emit a brief status line to the conversation: "On task T685 (3 of 4 in §40.17 chain), autonomous batch in progress." Cheap; structural; addresses Gap 1 directly.

**Pattern 2 — Ping-mid-batch behavior rule.** Add a `.claude/rules/agents.md § "Behavioral Rules"` (or a new sub-section) rule: when the user sends any message during an autonomous batch — including questions, status checks, or seemingly-incidental remarks — default to (a) acknowledging receipt, (b) summarizing current batch state, (c) offering "continue or pause?". Distinct from the orchestrator's normal dispatch flow.

The two patterns compose — heartbeat reduces ping frequency (users have less reason to interrupt); ping behavior catches the ones that still happen.

### Boundary with `/work` context budget

The styler session also flagged a related-but-distinct concern: `/work` auto-continuation lacks a "context burn threshold" stopping point. That's a separate FB candidate (context budget as a stop signal), but the heartbeat pattern here naturally piggybacks on it — a heartbeat could include cumulative agent-dispatch count, which the user could use to decide whether to redirect.

### Scope

- `.claude/commands/work.md` § "Auto-continuation within phases" — heartbeat insertion point (Pattern 1)
- `.claude/rules/agents.md § "Behavioral Rules"` — new sub-rule (Pattern 2)
- Possibly `.claude/skills/dashboard-style/SKILL.md` if heartbeat should also write to Recent Activity (unclear; defer until Pattern 1 design lands)

### Signal strength

Single-session signal but tied to a concrete observable user-friction event. Pattern is structural (autonomous-batch UX is independent of the specific project). Worth promoting if next `/feedback review` runs; otherwise can wait for a 2nd-project signal.

Tags: autonomous-batch, heartbeat, user-ping, work-step, behavioral-rule

## FB-082: Template-side enforcement of the YAML frontmatter colon-space hazard in SKILL.md

**Status:** new
**Captured:** 2026-05-20
**Source:** Bridged from flirty-gym FB-005 (template_version 4.0.0) via /feedback template:

## Observation

Authoring `.claude/skills/voice-gap/SKILL.md` in flirty-gym task T12 used unquoted `: ` (colon-space) inside the YAML frontmatter `description:` field at two sites. Strict YAML 1.2 / PyYAML rejects these as ambiguous mapping-value tokens. The Claude Code harness's deployment parser is permissive (it loaded the skill — visible in the `available-skills` system-reminder), so the failure mode was silent at runtime. T12's verify-agent caught it via PyYAML; the implement-agent retry replaced `: ` with em-dashes (` — `) to match sibling-skill convention.

## Meta-pattern

The convention is now established empirically across all 5 SKILL.md files in flirty-gym (review, persona, personas-from-real, voice-gap, pattern-mirror) — but there's no template-side documentation, validator, or skill-authoring guidance that encodes it. Task T13's dispatch prompt explicitly carried the lesson forward, which is fragile (the orchestrator had to remember; the implementer was warned just-in-time).

## Proposed template surface for the fix

1. **Lightweight (recommended):** add a 1-line note to `.claude/agents/implement-agent.md` § "Tool Preferences" / "Common Pitfalls" warning that YAML frontmatter `description:` values must avoid unquoted `: ` — use em-dashes. Or add the same note to a skill-authoring reference doc if one exists (`.claude/support/reference/skill-authoring.md` or similar).
2. **Heavier:** a `/health-check` validator hook that parses every SKILL.md frontmatter with strict YAML and fails on ambiguous mapping-value tokens. Catches the issue at authoring/check time rather than verify time, removing the implementer-retry round-trip.

## Project-side mitigation already applied

flirty-gym added a "Skill authoring" bullet to root `./CLAUDE.md § Key Invariants` documenting the convention. Prevents future drift within this project.

## Triage recommendation

Lightweight option is a one-line edit and catches future drift across all projects using the template. The heavier validator hook is worth it only if SKILL.md frontmatter authoring becomes common enough to justify the hook overhead.

## Source trace

- Surfaced via T12 verification fail (flirty-gym friction marker FR-003 captured at the time).
- FR-003 marked resolved 2026-05-20 once project-side mitigation landed and this template-side capture was written as FB-005.
- See flirty-gym `.claude/support/feedback/feedback.md` for the local entry.

## Tags

template-side, skill-authoring, yaml, frontmatter, validator-hook-candidate

## Signal queue from 2026-05-20 scan — captured here for next-session triage

The 2026-05-20 scan of `interaction-logs/processed/` surfaced six additional weaker signals not yet promoted to dedicated FBs. Captured here as a queue so next `/feedback review` (or manual triage) can decide whether to expand any into proper entries.

- **Uncommitted-work check at `/work` entry-time** (styler 2026-05-20). After recovery scan, count modified+untracked source files vs finished-since-last-commit tasks; surface mismatch. Erik discovered ~14-task uncommitted backlog mid-commit; an entry-time check would have caught it. Possible Step 0e addition.
- **Math-check before commit-to-pixels on layout iterations** (styler 2026-05-20). When changing a layout/composition dimension that affects vertical flow or composition (object-position, viewport-relative heights, crop modes), pre-compute arithmetic trade-off BEFORE committing to a screenshot iteration. Behavioral pattern; could land in `agents.md` as a UI-iteration rule.
- **Dashboard Recent Activity prose-style cap enforcement is ambiguous** (styler 2026-05-20). The dashboard-style skill's strict cap is at the writer's discretion; aggressive cleanup gets deferred because the regen-scope cost is high. Two routes: automatic cleanup during regen vs relax the rule for substantial work. Cross-couples with FB-080 (partial-regen would make cleanup cheaper).
- **Magnitude check when user specifies rule without absolute value** (echothread 2026-05-17). When the user says "tier-graduated sizes" or any RULE without specifying MAGNITUDE, surface a single-question check ("tier 4 = pebble-sized?") before coding. Avoids the wasted-iteration cycle of implementing default values → screenshotting → user reacts → re-implementing.
- **`.interaction-assessment.json` cleanup may have silent failure mode** (echothread 2026-05-17). Prior session's `/work pause` left `.interaction-assessment.json` on disk; this session's Write tool refused because file existed and hadn't been Read. Worth a quick check of the pause procedure's cleanup step — possible silent partial-completion bug.
- **`/walkthrough` or `/preflight` command for major workflow transitions** (SIREN 2026-05-18). Erik benefited from a "walk through plus implement plus sanity check" pattern when changing a workflow surface. Possible new command. Cross-couples with FB-072's help-me-think family review — could be part of that survey.

A seventh candidate — `file-status-taxonomy.md` starter reference doc (CANONICAL/REFERENCE/OPERATIONAL/HISTORICAL/etc.) — is speculative enough (one-project signal, abstract pattern) that it's not worth even queue capture; revisit only if a second project independently raises the need.

Tags: signal-queue, multi-source-scan, next-triage

## FB-083: Capability grounding for spec/agent/model/skill design — template-side reference + freshness mechanism

**Status:** new
**Captured:** 2026-05-22
**Source:** flirty-gym 2026-05-22 — that project shipped spec text and skill descriptions claiming runtime model-switching behavior that isn't structurally backed. Per code.claude.com/docs/en/skills, the SKILL.md `model:` frontmatter field is turn-scoped, not session-scoped, so it doesn't fit multi-turn chat skills. The drift wasn't caught at spec authoring or task decomposition because the template doesn't currently surface "what Claude Code can actually do" as a first-class input for spec/skill design. Session export in inbox: `interaction-logs/inbox/flirty-gym-session-export-2026-05-22-0049.json` (unprocessed at capture time).

### Observation

flirty-gym's spec described runtime model-switching as a feature of a multi-turn chat skill, on the assumption that the SKILL.md `model:` frontmatter field would govern model selection across the full skill invocation. The Claude Code skills doc is structurally clear: `model:` is **turn-scoped**, applied per-LLM-turn within the agent loop, not session-scoped or skill-lifetime-scoped. A multi-turn chat skill therefore cannot use that field for cross-turn model continuity the way the spec implied.

The mismatch survived spec authoring AND task decomposition. Neither `/iterate` nor `/work` had a mechanism to sanity-check claims-about-Claude in spec text against the documented capability surface. The drift only surfaced during implementation when actual behavior didn't match the spec's promise — i.e., a "design pattern only obvious after hitting a wall" failure mode (same shape as FB-082).

### Two coupled needs

#### Need 1 — Capability grounding for spec/task/skill design

A template-side reference (candidate location: `.claude/support/reference/claude-code-capabilities.md`) capturing structural facts spec/task authors should know:

- **Skill `model:` / `effort:` frontmatter** — turn-scoped only; not session-scoped or skill-lifetime-scoped. Multi-turn chat skills cannot rely on it for cross-turn model continuity.
- **Subagent isolation constraints** — no `.claude/` writes, no nested `Task` tool calls, no `permissions.allow` inheritance from parent. Already partially documented in `agents.md § State Ownership` and `§ Tool Preferences`, but scattered; consolidation candidate.
- **Parallel-execution constraints** — MCP shared state across concurrent subagents (single-session MCPs like Playwright break under fan-out, per `agents.md § MCP and Parallel Execution`), `files_affected` overlap rules, shared-contract detection (FB-046-class).
- **`Agent` tool `model` parameter** — exposes only `sonnet | opus | haiku` (no per-call effort control or model-version specificity). Effort selection is conversation-level, not call-level.
- **Slash command invocation gates** — `disable-model-invocation: true` blocks autonomous fire by the model via the `Skill` tool while preserving user-typed slash invocation (see FB-071 / v4.1.0). Multi-mode coupling caveat.
- **Skill-as-subagent execution** — `context: fork` + `agent:` frontmatter pattern for skill execution in a forked context. Boundaries vs the `Task` dispatch pattern.

`/iterate` and `/work` decomposition would reference this doc so claims-about-Claude in spec text get sanity-checked. Possibilities: a `/iterate` hygiene check (read capability doc fingerprint vs spec mentions of model/skill/subagent/parallel terminology), a `/work` Step 2 decomposition-time guard, or a new `/audit-coherence` lens that flags spec claims contradicted by the capability reference.

#### Need 2 — Freshness mechanism

Claude Code's capability surface changes — skill `model:` field landed recently; `/effort` levels expanded; subagent dispatch shape has evolved across harness versions (see `agents.md § Dispatch Convention` rationale). A static capability reference will go stale, and stale capability docs are arguably worse than no docs (they confer false confidence).

Candidates worth a `/research` round (tradeoffs are real for each):

- **Periodic WebFetch sync** from code.claude.com/docs. Catches changes automatically but risks pulling in updates that silently contradict the project's current spec — the drift surface moves from "spec vs Claude Code" to "spec vs synced doc vs Claude Code", more layers, harder to audit.
- **`/health-check` capability-doc-freshness lens** — manual review at cadence (every N sessions, or on template version bumps). Lower automation, higher signal; the user can authoritatively confirm "yes still true" or "this changed, update needed."
- **Version-pinned capability docs with manual update step in template upgrades** — bind the capability doc to a specific Claude Code version range; force an explicit update step on template-version bumps. Conservative and predictable; requires the template maintainer to track Claude Code releases.
- **"Last verified against Claude Code v.X.Y.Z" footer** on the reference, surfacing in `/audit-coherence` (or `/health-check`) as a staleness signal when the footer's date is more than N months old. Cheap; flags drift for attention without trying to fix it automatically.

These are not mutually exclusive — likely route is a combination (e.g., footer + `/health-check` lens, or version-pinned + footer). `/research` should establish the tradeoffs explicitly before committing.

### Why this slipped past existing surfaces

- `/iterate`'s spec checklist (`spec-checklist.md`) is about spec readiness shape, not capability grounding.
- `/work` decomposition checks task shape (difficulty, files_affected, dependencies), not capability claims.
- `/audit-coherence`'s existing lenses (vocab-drift, path-drift, etc.) audit spec-vs-code, not spec-vs-runtime-platform.
- DEC-016 protects spec/decision/vision files from accidental edits but doesn't catch claims-about-Claude that don't match reality.

The gap is structurally distinct from each: a spec can be "ready", "decomposable", "coherent with code", and still describe a runtime behavior the platform doesn't support.

### Pairs with FB-082

FB-082 (template-side YAML colon-space hazard, bridged from flirty-gym FB-005) is the same shape of gap — a design pattern only obvious after hitting a wall, worth codifying proactively rather than re-discovering per project. The two together suggest a broader template surface for "Claude Code authoring hazards" — structural facts about the platform that the template should encode for spec/skill/agent authors.

Worth considering at promotion time whether FB-082's lightweight fix and this FB's capability reference merge into a single `.claude/support/reference/claude-code-capabilities.md` (or `claude-code-authoring.md`) doc with multiple sections (capability surface, frontmatter hazards, dispatch shape gotchas), or stay as separate references with cross-links. Defer this scoping question until `/research`.

### Scope (if promoted)

- New `.claude/support/reference/claude-code-capabilities.md` (or merged-doc alternative per FB-082 consideration above)
- `.claude/commands/iterate.md` — reference the capability doc at spec authoring/refinement; possibly a hygiene check
- `.claude/commands/work.md § decomposition` — reference the capability doc at task creation time
- `.claude/commands/audit-coherence.md` — possible new lens for capability-claim drift (depends on freshness mechanism choice)
- `.claude/commands/health-check.md` — possible new Part for capability-doc freshness (depends on freshness mechanism choice)
- `.claude/sync-manifest.json` — register the new reference doc in `sync` category

### Triage recommendation

**Research-gated.** Multiple viable freshness mechanisms with real tradeoffs (Need 2). Route through `/research` to compare WebFetch sync vs cadence lens vs version-pinned + manual vs footer, and to scope the initial capability reference (Need 1 might be a single reference doc, or split across skill-authoring + subagent-constraints + parallel-execution + model-tool-surface).

Likely DEC candidate after research: the freshness mechanism itself is the substantive decision; the capability reference content is more mechanical once the mechanism is chosen.

### Signal strength

Two-project signal pattern (flirty-gym + the FB-082 case shape) for "claims-about-Claude that the platform doesn't support". Structural — the gap is independent of any specific spec or project. Worth a `/research` round when signal queue permits.

Tags: template-side, capability-grounding, claude-code-platform-knowledge, freshness-mechanism, research-gated, dec-candidate, paired-with-FB-082, skill-authoring, spec-grounding, multi-project-signal

## FB-084: Engine-consumption verification gap during retirement proposals (snake_case vs CamelCase derivatives)

**Status:** cheap-action-shipped + heavier-route-deferred
**Captured:** 2026-05-24
**Shipped:** 2026-05-24 (v4.7.3) — new `## Pre-Retirement Engine-Consumer Audit` section added to `.claude/rules/feature-retirement.md` between "When to Use This Workflow" and "Procedure". Documents the 4-pattern grep (snake_case + CamelCase derivatives + shortened forms + string literals) for pre-retirement verification. Heavier route (extend FB-066 to proposal-time) deferred — research-gated + signal-gated.
**Source:** Bridged from styler 2026-05-22 session (FR-014 / T714, template_version 4.7.1) via `/health-check` Part 7 aggregation.

## Observation

T714 retired `price_quality_philosophy` based on a `/research` (FR-014) finding that grepped only the snake_case form and concluded "no engine consumer found". The actual engine consumption used multiple derivatives the snake_case grep missed:

- `PriceQualityPhilosophy` (CamelCase TypeScript type)
- `RankerSignals.philosophy` (shortened field name in `src/lib/stores/ranker.ts`)
- `PHILOSOPHY_WEIGHTS` (CamelCase constant)
- Runtime reads in `/stores Phase 2a` + `/briefing Step 3`

The field is now retired from the registry but the engine integration points remain and will silently degrade (read returns `undefined` post-data-migration) until command files are restructured. Caught mid-implementation via friction marker (FR-016 / FR-017 / FR-018 sequence); corrective amend landed in-session.

## Meta-pattern

The grep convention for retirement proposals is fragile: `grep -r 'snake_case_field' src/` misses `CamelCaseField` derivatives, `field` shortened names, and string-literal usage (`"snake_case_field"`). A retirement proposal that searched only one form gives false confidence — "no consumer" reads as definitive when it's actually "no consumer matching this one form".

## Proposed template surface

Three candidate landing spots (not mutually exclusive):

1. **`.claude/rules/feature-retirement.md` § "Procedure" / "Common gotchas"** — add a checklist for verifying engine-consumer searches cover snake_case + CamelCase + shortened-field + string-literal variants. One paragraph, near "What NOT to copy" or as a new "Pre-retirement engine-consumer audit" sub-section.
2. **FB-066 extension** (verify-agent production-consumption check, shipped v3.16.0). The existing check is regex-based on file globs; could extend to scan for retired-field names in code beyond the spec section. Different timing (verify-agent, post-implementation) vs the proposal-time gap here.
3. **`.claude/scripts/verify-engine-consumption.sh` helper** (project-side). Project ships a wrapper that runs the multi-pattern grep (snake_case, CamelCase, shortened, string-literal) and surfaces matches before retirement landing. Higher overhead; only worth it if the project retires fields routinely.

## Triage recommendation

**Cheap action:** add the multi-pattern grep checklist to `feature-retirement.md` as a one-paragraph "Pre-retirement engine-consumer audit" sub-section. Catches the issue at proposal time across all projects using the template.

**Heavier route (research-gated):** extend FB-066 to cover the proposal-time gap (currently FB-066 is verify-agent only). Would unify the two layers — proposal-time + post-implementation — into one consistent check. `/research` to compare.

## Relationship to FB-066 and FB-076

- FB-066 (shipped v3.16.0) covers verify-agent runtime production-consumption — different timing (post-implementation, before "Finished").
- FB-076 (deferred) covers verify-agent bundle-boundary breaks + catalog-state-dependent precondition gaps — adjacent but distinct sub-gap.
- FB-084 is at the proposal stage (during `/research` or `/iterate distill`), upstream of verify-agent. Sibling to both, not a duplicate.

## Source trace

- Bridged from `interaction-logs/processed/.session-export-styler-2026-05-22-0105.json` § `claude_assessment.design_pushback_opportunities[0]`.
- Single-session signal but novel pattern. Below 3+ session bar for auto-promotion in `/health-check` Part 7 step 4; captured manually per user direction.

Tags: template-side, feature-retirement, grep-coverage, proposal-time-check, extends-FB-066, cheap-action-candidate, single-project-signal

## FB-085: Load-bearing browser-behavior assumption verification gap (runtime_validation: partial + owner: both)

**Status:** deferred + signal-gated (2nd-project)
**Captured:** 2026-05-24
**Triaged:** 2026-05-24 — proposed cheap action (behavioral rule in `agents.md`) has fragile enforcement scope: verify-agent's subagent sandbox limits direct Playwright access, so the empirical-verification step might need to route through the orchestrator instead — a different design problem. Re-assess if a 2nd project signals the same writer/reviewer shared-premise blindspot.
**Source:** Bridged from styler 2026-05-21 session (T697 pass-2, template_version 4.6.3) via `/health-check` Part 7 aggregation.

## Observation

T697 pass-2 attempted a CSS-only fix for an anchor-scroll bug. Implement-agent's report claimed the fix relied on the load-bearing property "native browser anchor scroll re-evaluates the target during smooth-scroll animation". Verify-agent confirmed it as the load-bearing property. Both reads of the diff missed that this claim was empirically false. The faulty premise was caught only by orchestrator-driven Playwright re-test during user_review hand-off.

The eventual landing fix (min-height reservation) was structurally different from the CSS-only approach implement-agent + verify-agent both shipped under the false premise.

## Meta-pattern

When implement-agent's report claims a load-bearing browser/runtime behavior on `runtime_validation: partial` + `owner: both` tasks, the writer/reviewer (implement-agent + verify-agent) separation can fail to catch incorrect assumptions because both share the same documentation-derived (rather than empirically-verified) model of the behavior. Verify-agent's fresh-eyes review is valuable for code correctness but doesn't independently verify runtime claims unless empirical re-test happens.

The current pattern: implement-agent claims → verify-agent confirms or denies based on code reading → orchestrator-Playwright cycle for `owner: both`. The gap is that empirical verification happens *after* the writer/reviewer cycle, so wrong premises propagate through both.

## Proposed template surface

Two candidate routes (mutually compatible):

1. **Behavioral rule in `.claude/rules/agents.md`** — when implement-agent's report claims a load-bearing browser/runtime behavior on `runtime_validation: partial`, verify-agent MUST empirically validate via dispatched tool (Playwright snapshot, dev-tools eval, etc.) before passing — not rely solely on code-reading. One paragraph, after "Root Cause Over Symptom" or as a sub-section of "Context Separation".
2. **Schema field on task_verification.checks** — `runtime_validation: partial` could split into `partial_empirical` vs `partial_documented` so the verify-agent verdict carries forward whether load-bearing claims were empirically verified.

## Triage recommendation

Option 1 (behavioral rule) is the cheap action; catches the issue across all projects without schema migration. Option 2 (schema split) is heavier but produces a more durable signal that the orchestrator can use to decide whether `owner: both` empirical re-test is mandatory before user hand-off.

**Likely route:** start with Option 1 as a rule addition; consider Option 2 only if Option 1's enforcement proves insufficient.

## Source trace

- Bridged from `interaction-logs/processed/.session-export-2026-05-21.json` § `claude_assessment.design_pushback_opportunities[0]`.
- Single-session signal. Pattern is structural (writer/reviewer shared-premise blindspot) and worth capturing despite the 1-session bar — recurring class of "both agents agree but both are wrong" failures.

Tags: template-side, verify-agent, runtime-validation, owner-both, behavioral-rule-candidate, writer-reviewer-blindspot, single-project-signal

## FB-086: `files_affected` declaration drift detection (declared vs actual touched files)

**Status:** research-light-candidate + ready
**Captured:** 2026-05-24
**Triaged:** 2026-05-24 — mechanism (git diff cross-check) is mechanical but the surrounding plumbing needs schema decisions before shipping: (a) which friction kind (existing `verification_gap` vs new `scope_drift`), (b) fold into FB-066 or stand alone, (c) timing — every verify-agent dispatch or only when `[Multi-file]` flagged. `/research` to scope when signal queue permits.
**Source:** Bridged from styler 2026-05-22 session (T708, template_version 4.7.1) via `/health-check` Part 7 aggregation.

## Observation

T708's task JSON `files_affected` declared 3 files; implementation actually touched 10. Implement-agent flagged the multi-file scope via `[Multi-file: 10]` in its return report, but there's no structural cross-check between the declared `files_affected` array and the actual files touched (per `git diff` against the pre-implementation HEAD).

The drift is benign for completed tasks (the work is done correctly) but blocks parallel-execution heuristics: `/work` Step 2c keys on `files_affected` overlap to decide parallel-safety. If declared `files_affected` is incomplete, a future parallel-dispatch decision could create real file collisions.

## Meta-pattern

`files_affected` is currently advisory metadata — populated at decomposition time, drifted away from at implementation time. There's no enforcement, no validation, no warning when implementation expands scope.

## Proposed template surface

Tier 2 scope-validation extension in verify-agent: when `[Multi-file]` is flagged by implement-agent's report, run `git diff --name-only <pre-impl-sha>..HEAD` and compare against declared `files_affected`. If actual is a superset:

1. **Pass with warning** — verify-agent emits a `scope_drift` friction marker (or sub-field on `checks.scope_validation`) noting the additional files. Allows the task to land but surfaces the drift for orchestrator to update `files_affected` (or flag for next decomposition pass).
2. **Block until update** — verify-agent fails until orchestrator updates `files_affected` to match actual. Stricter; prevents the drift from compounding but slows landing.

## Triage recommendation

Option 1 (pass with warning) is the more sustainable route — drift is benign for completed work but the signal helps future parallel-dispatch decisions and decomposition-pass calibration. Implement-agent already flags `[Multi-file: N]`; the verify-agent extension just consumes the signal and emits the friction marker.

**Implementation cost:** small. Single check in verify-agent's `scope_validation`. Friction marker emission already exists (per `agents.md § "Friction Register"`).

**Open question:** does `files_affected` drift also belong in the post-decomposition pre-pass check (per FB-058's 5 heuristics) for ripple inference? Possible secondary surface — flag at decomposition if a sibling task's `files_affected` significantly outsizes its difficulty, suggesting under-declared scope.

## Source trace

- Bridged from `interaction-logs/processed/.session-export-2026-05-22-1435.json` § `automated_markers[1]` (type: `verification_gap`, `template_area: task-schema files_affected`).
- Originally captured as a marker in styler's session export; promoted to template feedback per `/health-check` Part 7 aggregation.

Tags: template-side, verify-agent, scope-validation, files-affected, parallel-execution, friction-marker, single-project-signal

## FB-087: Playwright MCP large-DOM token-limit pattern — prefer browser_evaluate over browser_snapshot

**Status:** cheap-action-shipped
**Captured:** 2026-05-24
**Shipped:** 2026-05-24 (v4.7.3) — new `## MCP and Result-Size Constraints` section added to `.claude/rules/agents.md` between "## MCP and Parallel Execution" and "## Tool Preferences". Documents that `browser_snapshot` on long-scroll pages (~10K+ char DOM) exceeds per-tool-call token budgets and truncates silently; prefers `browser_evaluate` with targeted DOM queries. Optional project-side helper follow-up deferred unless a multi-project signal emerges.
**Source:** Bridged from styler 2026-05-21 session (template_version 4.6.3) via `/health-check` Part 7 aggregation.

## Observation

Playwright MCP `browser_wait_for` and `browser_snapshot` return 105K+ character snapshots for large pages (the styler `/style` page is ~36000px tall with many sections), exceeding the result token limit. The model can't process the snapshot — tool result truncates or fails outright.

The workaround styler used: replace `browser_snapshot` with `browser_evaluate` containing targeted DOM queries (`document.querySelector(...).textContent`, etc.). The pattern is reusable for any large-DOM page where the audit/verification only needs specific elements.

## Meta-pattern

The current `agents.md § "MCP and Parallel Execution"` section covers the parallel-execution constraint (single-instance MCPs can't fan out) but doesn't cover the per-call result-size constraint. `browser_snapshot` is the default tool the model reaches for, and on large pages it fails silently from the model's perspective (token limit exceeded → degraded behavior).

## Proposed template surface

One-paragraph addition to `.claude/rules/agents.md § "MCP and Parallel Execution"` (or a sibling sub-section "MCP and Result-Size Constraints"):

> Playwright MCP `browser_snapshot` returns the full accessibility tree of the current page. For pages over ~10K characters of DOM (long-scroll pages, sites with many sections), the result can exceed the model's per-tool-call token budget and truncate silently. For audits/verifications that only need specific elements, prefer `browser_evaluate` with targeted DOM queries (e.g., `document.querySelectorAll('h2').forEach(...)`). Reserve `browser_snapshot` for small pages or when you genuinely need the full tree.

## Triage recommendation

**Cheap action:** one-paragraph addition to `agents.md`. No DEC needed. Catches future "why is my Playwright snapshot empty" debugging cycles across all projects.

**Optional follow-up:** project-side helpers under `.claude/scripts/` that wrap common Playwright-evaluate patterns (e.g., extract-all-headings, count-elements-by-selector) — but these are project-specific and not worth template-shipping unless a multi-project pattern emerges.

## Relationship to existing template content

- `.claude/rules/agents.md § "MCP and Parallel Execution"` covers cross-call state collision; this FB covers per-call result size.
- DEC-005 / auto-mode covers permission gating, not result-size.
- No existing template surface addresses this.

## Source trace

- Bridged from `interaction-logs/processed/.session-export-2026-05-21.json` § `claude_assessment.workflow_friction_notes[3]`.
- Single-session signal. Cheap-action threshold is low — one paragraph addition. Capture now, ship in next template patch.

Tags: template-side, mcp, playwright, result-size, browser-snapshot, browser-evaluate, agents-md-extension, cheap-action-candidate, single-project-signal
