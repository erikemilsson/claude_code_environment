# Archived Feedback

All resolved feedback items. Each entry preserves its final status and reason.

- **promoted** — Incorporated into the spec via `/iterate`
- **absorbed** — Combined into another item (has `absorbed_into` pointer)
- **closed** — Investigated but decided against
- **archived** — Not relevant (quick triage)

---

## FB-001: Context-preserving continuation command for long sessions

**Status:** promoted
**Captured:** 2026-02-27
**Promoted:** 2026-03-05 — Implemented as `/work pause` + PreCompact hook + handoff file system. See `support/reference/context-transitions.md`.

I figured out that I can have a long conversation with Claude when I execute tasks with the work command, by using the plan mode at the end of the context window. That is, Claude creates a plan based on where we are in the progress of executing tasks.

What I'm thinking is that it would be great to have a command that I can run while Claude is maybe working on tasks and has potentially some agents out doing some verification or implementation tasks. If I run that command while it's working, it knows that it's time to kind of wrap up and start to see how we can create a plan so that it can continue without interruption and without losing important context.

Maybe we need to do some tests to make sure that it has all the context for especially between the implementation stage, where an agent is implementing a task, and also where it's validating that task or verifying that task with another agent to ensure that the verification agent has all the necessary context. Also for the phase transitions, when Claude is checking the phase, verifying the phases to make sure that it has the important context there as well.

Also scope out if there's anything else that Claude will potentially need and basically have that in the task so that it knows what to include and not to include and also not make it too restrictive so that it potentially misses something there too. I think the important thing is to give it the philosophy of why this exists. Working name: "continue-plan" or similar.

## FB-002: Use insights report to power per-project CLAUDE.md recommendations

**Status:** closed
**Captured:** 2026-03-22
**Closed:** 2026-03-27 — Decided against automating this. The cross-project→per-project matching is too ambiguous for Claude to do reliably; automating it would create more chaos than structure. User will manually review the insights report and apply relevant rules to `./CLAUDE.md` as needed.

## FB-004: Clarify decision ownership — Claude must not decide for the user

**Status:** absorbed
**Captured:** 2026-03-26
**Absorbed:** 2026-03-29 — Combined into FB-009
**Absorbed Into:** FB-009

For the decisions docs, we need to clarify that Claude should not make decisions for the user. Instead, when Claude encounters an ambiguity or choice point, it should ask the user whether to use the formal decision workflow (create a decision record) or whether the user wants to resolve the ambiguity directly inline. Need to determine the best enforcement mechanism for Claude Code Desktop as well.

## FB-005: User-facing documents should not live in .claude/support/workspace/

**Status:** absorbed
**Captured:** 2026-03-27
**Absorbed:** 2026-03-29 — Combined into FB-010
**Absorbed Into:** FB-010

**Problem:** The template routes all working documents into `.claude/support/workspace/`, which is described as "scratch, research, drafts." In practice, many of these documents become operational artifacts the user actively needs -- invitation letters, consent forms, facilitation guides, participant trackers, etc. Burying them three levels deep in the Claude environment folder makes them hard to find and signals they're temporary when they're not.

**Key insight:** The `.claude/` folder should be Claude's environment. The project root should be the user's environment. Documents the user works with belong in the user's environment.

## FB-006: UX evaluation skill for dashboard and project interaction quality

**Status:** absorbed
**Captured:** 2026-03-27
**Absorbed:** 2026-03-29 — Combined into FB-010
**Absorbed Into:** FB-010

UX evaluation skill concept for assessing dashboard readability, project structure, and interaction flow across different project types.

## FB-008: /iterate must distinguish autonomous changes from user-approved changes

**Status:** absorbed
**Captured:** 2026-03-29
**Absorbed:** 2026-03-29 — Combined into FB-009
**Absorbed Into:** FB-009

When running `/iterate`, Claude sometimes makes decisions on the user's behalf within suggested spec changes without clearly flagging which changes were autonomously decided vs. which were explicitly requested or approved.

## FB-003: Agent Teams as future parallel execution mode

**Status:** closed
**Captured:** 2026-03-05
**Closed:** 2026-03-30 — Community research showed limited demand; current Task-based parallel execution is sufficient. Not worth introducing a new feature dependency.

Agent Teams integration: Consider adding Agent Teams as an optional parallel execution mode (with Task-based fallback) once the feature moves past research preview to a stable release. Natural fit for: phase-level Tier 2 verification (team of verifiers), /review (each teammate takes 1-2 focus areas), and parallel research investigations. Requires tmux/iTerm2.

## FB-010: Project UX — file placement, dashboard quality, and interaction evaluation

**Status:** absorbed
**Captured:** 2026-03-29
**Absorbed:** 2026-03-30 — Split into FB-014 (user-facing document placement convention) and FB-015 (UX evaluation step in /health-check)
**Absorbed Into:** FB-014, FB-015

Two related problems with how users experience project artifacts: file placement (operational documents buried in `.claude/support/workspace/`) and lack of systematic UX evaluation for dashboards and project interaction quality.

## FB-007: Early-exit fast path in /work for non-actionable states

**Status:** promoted
**Captured:** 2026-03-28
**Promoted:** 2026-03-30 — Implemented as Step 1d in `work.md`. Fast-exit for human-owned, blocked, and on-hold states. Updated `workflow.md` and `system-overview.md`.

Add early-exit fast paths to `/work` for three non-actionable states: all human-owned, all blocked, all on hold. Skip full analysis, show brief summary with next steps.

## FB-009: Enforce transparency when Claude acts without explicit approval

**Status:** promoted
**Captured:** 2026-03-29
**Promoted:** 2026-03-30 — Implemented transparency requirement in `iterate.md` (change declaration tags: `[requested]`/`[proposed]`/`[assumption]`, distill transparency section), ambiguity surfacing in `work.md`, design principle update in `system-overview.md`, transparency labels in `spec-workflow.md` and `decisions.md` rules, and vision document prompt updated in `desktop-project-prompt.md` (assumption-surfacing bullet + Assumptions & Interpretations template section).

Core principle: Claude surfaces choices, the user makes them. Enforced at `/iterate` proposals, `/iterate distill`, and decision workflows.

## FB-012: Source of truth for the template repo itself

**Status:** promoted
**Captured:** 2026-03-30
**Promoted:** 2026-03-30 — Formalized `system-overview.md` with source-of-truth declaration, version reference, and 5-step change-proposal process. Root `CLAUDE.md` updated with Template Maintenance Workflow section.

Formalize `system-overview.md` as the template's source of truth with version tracking and a change-proposal process.

## FB-013: Template version not bumped when template files change

**Status:** promoted
**Captured:** 2026-03-30
**Promoted:** 2026-03-30 — Created pre-commit hook (`scripts/pre-commit-hook.sh`, installed to `.git/hooks/pre-commit`) that warns when sync-category files change without version.json bump. Documented in root `CLAUDE.md` with install instructions and SemVer policy outline.

Pre-commit hook to detect sync-category file changes and warn about stale version.json.

## FB-014: User-facing document placement convention

**Status:** promoted
**Captured:** 2026-03-29
**Promoted:** 2026-03-30 — Updated `archiving.md` with three-category file placement (workspace, user-facing docs, reference docs), decomposition prompt, and graduation guidance. Updated `paths.md`.

Default convention for user-facing documents in project root `docs/`, separate from workspace.

## FB-015: UX evaluation step in /health-check

**Status:** promoted
**Captured:** 2026-03-29
**Promoted:** 2026-03-30 — Added Part 6: UX Evaluation to `health-check.md` with 6 initial checks (mermaid readability, workspace graduation, notes utilization, action required actionability, dashboard length, phase collapsing). DEC-002 approved (Option A, D-to-A hybrid path).

UX assessment step in `/health-check` with severity framework and extensible check catalog.

## FB-011: Cross-project interaction logs for template improvement

**Status:** promoted
**Captured:** 2026-03-30
**Promoted:** 2026-03-30 — Implemented hybrid pipeline (DEC-001, Option C). Track 1: friction markers in implement-agent and verify-agent. Track 2: interaction assessment in `/work pause`. Session export compiles both tracks. PreCompact hook handles markers-only fallback. Processing pipeline as Part 7 of `/health-check`. `template_inbox_path` field added to `version.json`. `interaction-logs/` directory created in template repo. Updated `system-overview.md`.

Automated cross-project feedback loop: agents emit friction markers during execution, Claude generates interaction assessments at session end, exports flow to template repo for processing into actionable feedback items.
