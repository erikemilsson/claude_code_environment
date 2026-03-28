# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-001: Context-preserving continuation command for long sessions

**Status:** refined
**Captured:** 2026-02-27
**Refined:** 2026-03-05 — Implemented as `/work pause` + PreCompact hook + handoff file system. See `support/reference/context-transitions.md`.

I figured out that I can have a long conversation with Claude when I execute tasks with the work command, by using the plan mode at the end of the context window. That is, Claude creates a plan based on where we are in the progress of executing tasks.

What I'm thinking is that it would be great to have a command that I can run while Claude is maybe working on tasks and has potentially some agents out doing some verification or implementation tasks. If I run that command while it's working, it knows that it's time to kind of wrap up and start to see how we can create a plan so that it can continue without interruption and without losing important context.

Maybe we need to do some tests to make sure that it has all the context for especially between the implementation stage, where an agent is implementing a task, and also where it's validating that task or verifying that task with another agent to ensure that the verification agent has all the necessary context. Also for the phase transitions, when Claude is checking the phase, verifying the phases to make sure that it has the important context there as well.

Also scope out if there's anything else that Claude will potentially need and basically have that in the task so that it knows what to include and not to include and also not make it too restrictive so that it potentially misses something there too. I think the important thing is to give it the philosophy of why this exists. Working name: "continue-plan" or similar.

## FB-002: Use insights report to power per-project CLAUDE.md recommendations

**Status:** closed
**Captured:** 2026-03-22
**Closed:** 2026-03-27 — Decided against automating this. The cross-project→per-project matching is too ambiguous for Claude to do reliably; automating it would create more chaos than structure. User will manually review the insights report and apply relevant rules to `./CLAUDE.md` as needed.

---

## FB-003: Agent Teams as future parallel execution mode

**Status:** new
**Captured:** 2026-03-05

Agent Teams integration: Consider adding Agent Teams as an optional parallel execution mode (with Task-based fallback) once the feature moves past research preview to a stable release. Natural fit for: phase-level Tier 2 verification (team of verifiers), /review (each teammate takes 1-2 focus areas), and parallel research investigations. Requires tmux/iTerm2.

## FB-004: Clarify decision ownership — Claude must not decide for the user

**Status:** new
**Captured:** 2026-03-26

For the decisions docs, we need to clarify that Claude should not make decisions for the user. Instead, when Claude encounters an ambiguity or choice point, it should ask the user whether to use the formal decision workflow (create a decision record) or whether the user wants to resolve the ambiguity directly inline. Need to determine the best enforcement mechanism for Claude Code Desktop as well.

## FB-005: User-facing documents should not live in .claude/support/workspace/

**Status:** new
**Captured:** 2026-03-27

**Problem:** The template routes all working documents into `.claude/support/workspace/`, which is described as "scratch, research, drafts." In practice, many of these documents become operational artifacts the user actively needs -- invitation letters, consent forms, facilitation guides, participant trackers, etc. Burying them three levels deep in the Claude environment folder makes them hard to find and signals they're temporary when they're not.

**Observed in:** SIREN Task 7.5. Workshop preparation produced 7 operational documents in `.claude/support/workspace/` that the user needed to access regularly for recruitment and workshop execution. The user couldn't find them without asking Claude to search, and the dashboard links pointed into the hidden folder.

**Proposed fix:** The template should distinguish between two kinds of workspace output:

1. **Intermediate analysis artifacts** (IO map drafts, search logs, policy scans) -- these are genuinely Claude's working space and belong in `.claude/support/workspace/`.
2. **User-facing operational documents** (anything the user sends to participants, uses during execution, or needs to reference regularly) -- these should live in top-level project folders, visible alongside `README.md`, `references/`, etc.

The template should:
- Provide guidance in the archiving rules or workspace README about when a document has "graduated" from scratch to operational and should move to a project-level folder.
- During spec decomposition or task creation, prompt the user about folder structure for deliverable and operational documents rather than defaulting everything to workspace.
- Consider a convention like top-level folders named by activity domain (e.g., `workshop/`, `procurement/`, `analysis/`) that the spec decomposition step helps establish.
- Update the spec template's "Working Documents and Data" section to distinguish workspace (Claude's scratch) from project folders (user's operational files).

**Key insight:** The `.claude/` folder should be Claude's environment. The project root should be the user's environment. Documents the user works with belong in the user's environment.

## FB-006: UX evaluation skill for dashboard and project interaction quality

**Status:** new
**Captured:** 2026-03-27

As part of the workflow, I think it would be good to create a skill that is used by the work command, the iterate command, or some other part of the workflow (I'm not sure). I want a skill that evaluates the current state of the repo or project the template is in for user interaction, and also, in some ways, user experience. Technically, it should cover both.

I'm thinking it would be good to do some research to find different ways people are working with Claude, and maybe something similar to what I'm doing with the dashboard, to get examples of what really works and what works as a workflow when you're using Claude in a similar way that I am here. For instance, the dashboard is the guiding tool I use to interact with the project, and I'm supposed to get an overview.

I feel like there's a lot that can be done, and if you have a skill, you can put some examples of different types of projects. I don't necessarily have to have the same structure for every project, so it could really be different depending on the project. Giving Claude some context about how it's done well, I think, would help a lot, so searching the web for that would be a good step toward that.

One example is the markdown document for the dashboard has a mermaid diagram with the different types of steps. Instead of rendering all of them at a reasonable size, the mermaid diagrams actually have a limitation because they just shrink them, and it's really hard to see. That's just one kind of example of a problem I find with the user experience with the dashboard. We don't have any hard rules about what is produced from the user input section, and I think that's one area that has a lot of potential to get better. It could really help with the user experience when I use the template in projects.

As per my previous feedback, just before this one, I actually had a lot of the files that were project-specific, that I would be interacting with in the workshop documents, stored in the wrong folder. Looking into how to structure the different project files based on what type of project I have and how I interact with it over the course of the project, I think, is also super important.

## FB-007: Early-exit fast path in /work for human-only task states

**Status:** new
**Captured:** 2026-03-28

**Problem:** `/work` is a 7-step process that reads the spec, dashboard, all task files, decision records, checks drift, checks phase gates, assesses parallelism, and then finally routes to work. The command definition alone is ~600 lines. Combined with rules files (loaded automatically via CLAUDE.md), agent definitions, and reference docs, a single `/work` invocation consumes a large fraction of the context window before any actual work begins.

For projects where the current state is "all remaining tasks in the active phase are owner: human, no Claude-executable work," the system goes through all 7 steps only to conclude there's nothing for Claude to do.

**Suggestion:** Add an early-exit fast path to `/work` that checks task ownership before the full analysis. If all remaining tasks in the active phase are `owner: "human"`, skip Steps 2-4 and go straight to surfacing the dashboard Action Required section. The dashboard META hash already exists for freshness checks — extend this to include a "next-actionable-task" indicator.

**Source:** External evaluation of user interaction and flow on a live project (SIREN).
