# Agent Rules

## Separated Concerns

Three specialist agents with distinct roles:
- **implement-agent** — executes tasks and produces deliverables. Does not verify.
- **verify-agent** — validates implementation independently (separate context, no implementation memory). Does not fix.
- **research-agent** — investigates options for decisions. Populates evidence and comparison matrices but never makes selections.

## Context Separation

verify-agent always runs as a separate Task agent, dispatched by the `/work` orchestrator — never inline in the implementation conversation. This applies to both sequential and parallel execution modes. "Fresh eyes" is preserved because the verifier evaluates in its own context with no implementation memory; the fact that the orchestrator (not the verify-agent itself) writes the verification result to the task JSON does not affect verification independence. See DEC-004.

## State Ownership

All `.claude/` state transitions (task JSON writes, dashboard regeneration, verification-result.json, session-log.jsonl) are owned by the `/work` orchestrator. Subagents (implement-agent, verify-agent, research-agent) return structured reports; they do not write to `.claude/` paths. This is a hard constraint of the Claude Code harness (subagents are sandboxed from `.claude/` writes per Anthropic issue #38806) and is not expected to change. See DEC-004 for the full rationale.

## Tool Preferences

All agents use dedicated tools (Read, Glob, Grep, Edit, Write) for file operations. Bash is reserved for operations requiring shell execution: git commands, running tests, executing deliverables, network requests. This minimizes permission prompts when agents run as subagents.

Subagents cannot write to `.claude/` paths, cannot spawn nested `Task` tool calls, and do not inherit parent `permissions.allow` rules. When an agent's documented workflow describes a state transition, it means "include in return report"; the orchestrator performs the actual write.

## Model Requirement

All agents must run on Claude Opus 4.7 (`claude-opus-4-7[1m]`).

**Effort defaults:** Max/Team subscriptions default to medium reasoning effort. Use "ultrathink" in prompts when deeper reasoning is needed (phase-level verification, complex design decisions).

## References

- implement-agent: `.claude/agents/implement-agent.md`
- verify-agent: `.claude/agents/verify-agent.md`
- research-agent: `.claude/agents/research-agent.md`
