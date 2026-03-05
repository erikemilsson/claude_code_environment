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

## FB-002: Agent Teams as future parallel execution mode

**Status:** new
**Captured:** 2026-03-05

Agent Teams integration: Consider adding Agent Teams as an optional parallel execution mode (with Task-based fallback) once the feature moves past research preview to a stable release. Natural fit for: phase-level Tier 2 verification (team of verifiers), /review (each teammate takes 1-2 focus areas), and parallel research investigations. Requires tmux/iTerm2.
