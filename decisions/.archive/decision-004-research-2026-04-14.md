# Research Archive: DEC-004 — Subagent Capability Contract

**Decision:** decision-004-subagent-capability-contract.md
**Researcher:** research-agent
**Date:** 2026-04-14
**Status when archived:** proposed (populated)

---

## Investigation Methodology

1. Read the decision record and FB-010 in full to understand the observed problem (Phase 10 styler session: 7 tasks × 3 dispatch rounds; orchestrator handled 14 JSON edits + 7 verify-agent dispatches + 7 verification persistences because subagents could not write to `.claude/tasks/` or use the `Task` tool).
2. Read every file the assessor flagged as touched: `implement-agent.md` (Steps 3, 6a, 6b, 6c), `verify-agent.md` (T6, T7), `commands/work.md` Step 4, `support/reference/parallel-execution.md`, `rules/agents.md`, `system-overview.md` (atomic implement→verify contract).
3. Web-researched current (April 2026) Claude Code subagent capabilities, focusing on:
   - Whether the `Task` tool can be made available to spawned subagents
   - Whether `additionalDirectories` (or any settings entry) can grant write access to `.claude/tasks/`
   - Whether `bypassPermissions`, `permissionMode` frontmatter, or hooks can override `.claude/` directory protection
   - Whether subagents inherit parent permission rules from `settings.json`
4. Consulted official Claude Code documentation (`code.claude.com/docs/en/permissions`, `code.claude.com/docs/en/sub-agents`, `code.claude.com/docs/en/agent-sdk/permissions`, `code.claude.com/docs/en/settings`) and corroborated against open GitHub issues filed against `anthropics/claude-code` in 2026.

## Sources Consulted

### Official documentation
- `code.claude.com/docs/en/permissions` — permission rules, modes, and `.claude/` protection rules
- `code.claude.com/docs/en/sub-agents` — subagent definition format, frontmatter fields
- `code.claude.com/docs/en/agent-sdk/permissions` — SDK-level permission flow, `bypassPermissions` subagent inheritance
- `code.claude.com/docs/en/settings` — `additionalDirectories`, settings precedence, scope semantics

### GitHub issues (anthropics/claude-code)
- **#38806** [open, FEATURE] — Allow `bypassPermissions` to fully bypass `.claude/` protections. Confirms: even explicit `Edit(.claude/**)` / `Write(.claude/**)` rules do not override `.claude/` protection since v2.1.78. Documented exemptions for `.claude/commands`, `.claude/agents`, `.claude/skills` are inconsistently honored.
- **#19077** [open, BUG] — Sub-agents cannot create sub-sub-agents. Subagent reports "Task tool not available" despite `tools: Write, Task` in frontmatter and `Task` in settings.json allow list. No documented workaround.
- **#22665** [closed as duplicate] — Subagents do not inherit permission allowlist from settings.json.
- **#27661** [closed, Feb 22 2026] — Subagents do not inherit parent session hooks and permission rules. Workaround: manually replicate hooks per agent definition. Proposed `propagateToSubagents` setting not yet implemented.
- **#18950** [open] — Skills/subagents do not inherit user-level permissions from `~/.claude/settings.json`.
- **#37730** [open] — Subagents (Agent tool) re-prompt for already-allowed tools.
- **#29610** [closed, "not planned"] — `bypassPermissions` does not bypass for paths outside project root in background subagents.
- **#3146** [closed] — Feature request to configure `additionalDirectories` via settings files (status of implementation unclear).
- **#40606** [open, BUG] — `additionalDirectories` approved in one project leak into all projects via global settings.

### Secondary sources
- `blog.vincentqiao.com/en/posts/claude-code-settings-permissions/` — independent deep-dive on permission system
- `claudefa.st/blog/guide/development/permission-management` — workflow guide for permission management

## Detailed Findings per Question

### Q1: What are subagents *actually* allowed to do?

Definitively, in the current harness (April 2026):

| Capability | Reality |
|------------|---------|
| Read files anywhere within cwd or `additionalDirectories` | Yes |
| Write files within cwd | Yes (subject to permission mode) |
| Write to `.claude/tasks/` | **No** — `.claude/` is protected even with `Edit(.claude/**)` allow rules and `bypassPermissions` mode (#38806) |
| Write to `.claude/commands`, `.claude/agents`, `.claude/skills` | Documented exempt — actual behavior inconsistent (#38806) |
| Use the `Task` tool to spawn nested subagents | **No** — not exposed even when listed in frontmatter `tools:` (#19077) |
| Inherit parent's `permissions.allow` rules | **No** (#22665, #18950, #27661, #37730) |
| Inherit parent's hooks | **No** (#27661) |
| Inherit parent's CLAUDE.md / memory | **No** (#27661) |
| `additionalDirectories` propagation from parent | Partial — file access only, not configuration. Doesn't help `.claude/tasks/` because `.claude/` is protected at a layer above `additionalDirectories`. |

This matches FB-010's observation exactly. The Phase 10 session behavior is not a bug in the template — it is the documented runtime behavior of the harness.

### Q2: Are there harness-level knobs that can change this?

No knob unlocks the two specific blockers:

1. **`.claude/tasks/` writes:** No setting unlocks this. `bypassPermissions` mode does not bypass it. `Edit(.claude/**)` allow rules do not override it. Hooks cannot override it because deny rules are evaluated before hook output. Per #38806, this is by design — it's a hardcoded protection layer separate from the rule system.

2. **`Task` tool in subagents:** No setting unlocks this. Even with `tools: Task` in agent frontmatter and `Task` in `settings.json` allow list, the subagent reports "Task tool not available" (#19077). Anthropic has not exposed a configuration to change this; the limitation appears intentional (preventing agent recursion/cost runaway).

**Theoretical workarounds and why they don't work:**

- **Run from a parent directory with `.claude` not as cwd root:** The protection applies to any path containing `.claude/` — moving cwd doesn't help.
- **Symlink `.claude/tasks/` to a non-`.claude` path:** Untested, but path normalization in Claude Code (per docs) likely resolves symlinks before checking protection. Even if it worked, this would break every other consumer of `.claude/tasks/` (commands, dashboard regen, /work).
- **PreToolUse hook that allow-lists `.claude/tasks/`:** Hook output cannot override deny rules (per docs explicitly). The `.claude/` protection acts like a deny, so hooks can't bypass.
- **`bypassPermissions` mode for subagents:** Inherits from parent only. Parent must already be in `bypassPermissions`. Still doesn't bypass `.claude/` protection.
- **MCP server proxy that writes on the subagent's behalf:** Theoretically possible (an MCP tool can use the OS filesystem directly without going through Claude Code's permission layer), but represents significant new infrastructure — a stateful MCP server, install instructions for users, version coupling. Not lightweight.

### Q3: If the harness can be changed, what's the scope?

The harness cannot be changed by us — we don't ship the Claude Code binary. Two upstream paths exist, neither short-term:

1. **Wait for Anthropic to fix #38806** (allow `Edit(.claude/**)` to override the protection). This would unblock `.claude/tasks/` writes from subagents. No timeline. Active issue, no PR linked.
2. **Wait for Anthropic to fix #19077** (subagents can spawn sub-subagents). No timeline. Open issue with no PR.

Even if both are fixed upstream, neither fix changes immediately for users — they'd need to upgrade Claude Code. The template would still need to handle older versions gracefully, meaning Option B (orchestrator ownership) effectively becomes the floor regardless of what upstream does.

### Q4: If the harness can't be changed, what's the cost of orchestrator ownership?

Concrete costs from the Phase 10 session (FB-010):

| Cost | Quantification |
|------|----------------|
| Orchestrator JSON edits per parallel batch | ~2 per task (mark Awaiting Verification + persist verification) |
| Orchestrator-spawned verify-agents | 1 per task |
| Total orchestrator tool calls per N-task batch | ~3N (1 implement-agent dispatch result read + 1 status edit + 1 verify-agent dispatch + 1 verification persistence) |
| Phase 10 actuals: 7 tasks × 3 dispatch rounds | 14 JSON edits + 7 verify-agent dispatches + 7 verification persistences |

Context window cost: each verify-agent's structured output (~200-500 tokens) lands in orchestrator context. Across 7 tasks that's ~2-4K tokens. Across a 30-task project that's 6-12K tokens — meaningful but not catastrophic.

**Fresh-eyes guarantee:** Verify-agent still runs in its own context — that does not change. The orchestrator does *receive* the verify-agent's structured judgment, but it doesn't re-evaluate it; it persists what the verifier decided. The "fresh eyes" property of verification is about the verifier not having implementation memory, which holds regardless of who persists the result. The orchestrator was already reading verify-agent's pass/fail summary anyway (to know what to do next).

So the actual loss vs. ideal-Option-A is: orchestrator does the *bookkeeping* (JSON writes), not the *verification judgment*. This is a much smaller architectural shift than the decision record's framing suggests.

**Latency:** Per task, persistence adds ~1-2 seconds (one Edit call). Across a parallel batch of 3, this serializes as ~3-6s of orchestrator time after the parallel work completes — modest compared to the 30-90s parallel implementation phase.

**Implementation complexity for the template:** Moderate. Touch points are well-scoped:
- `implement-agent.md` Steps 6a, 6b: rewrite to "return structured report" instead of "spawn verify-agent and persist"
- `verify-agent.md` Steps T6, T7: rewrite to "return structured result" instead of "write to JSON"
- `commands/work.md` Step 4 + `parallel-execution.md`: add the persistence procedure
- `system-overview.md`: update the atomic contract paragraph to reflect orchestrator's persistence role
- `rules/agents.md`: clarify that "context separation" means verify-agent runs in its own Task context, not that it owns the JSON write

This is a 5-file edit, cleanly bounded.

### Q5: Do other workflows in the Claude Code ecosystem face this pattern?

Yes, broadly. From research:
- Per #38806: a user with 80+ auto-generated `.claude/skills/*/SKILL.md` files via PostToolUse hooks reports the same blocker.
- Per #19077: any multi-agent workflow that wants nested delegation hits the Task-tool-unavailable wall.
- The general pattern in the Claude Code community is "main agent orchestrates, subagents do focused work and return reports" — i.e., Option B is the de facto convention. Most public subagent libraries (e.g., VoltAgent's awesome-claude-code-subagents collection of 100+ subagents) describe subagents as returning "results" that the main agent acts on, not as state-mutating actors.

This template is in a minority by attempting to have subagents own task state transitions. Aligning with the ecosystem convention is itself a tailwind for Option B.

## Discarded Approaches

- **MCP server for task JSON writes:** Considered, discarded. Adds installation overhead, version coupling, and a runtime dependency. Possible future work if the per-task JSON shape stabilizes and an MCP server becomes worth the cost — out of scope here.
- **Polling-based file IPC:** Subagent writes a `.handoff.json` to a directory it *can* write (project root or `app/`), orchestrator polls and persists. Adds complexity (polling, cleanup, race conditions) without a clear win over direct return-by-result.
- **Run subagents in `bypassPermissions` mode:** Already established this doesn't help — `.claude/` protection is above the bypass layer.

## Recommendation Rationale

Option B (formalize orchestrator ownership) is the only option that works *today* without harness changes, has a bounded implementation footprint, and aligns with the broader Claude Code ecosystem convention. The "fresh eyes" cost is smaller than the decision record initially framed — verification judgment still runs in a separate context, only the JSON write moves.

Option A is appealing but blocked by upstream Anthropic decisions (#38806, #19077) with no published timeline. Any version of A that doesn't depend on those fixes requires building MCP infrastructure, which is disproportionate.

Option C (hybrid) sounds attractive but pays the cost of both paths: writes the failure-detection plumbing AND the orchestrator-ownership plumbing. The "ideal path" almost never triggers (because the harness doesn't allow it), so the hybrid degenerates to Option B with extra dead code.

## Notes & Caveats

- Recommendation is to revisit if Anthropic resolves #38806 (or both #38806 and #19077). At that point, Option A becomes feasible again and the template could move state ownership back into agents — but only if there's a real cost reason to do so, which the FB-010 evidence does not strongly establish.
- The `.claude/commands`, `.claude/agents`, `.claude/skills` exemption is documented but inconsistently honored (#38806). The template should not rely on this exemption for `.claude/tasks/` even hypothetically.
- The decision record references DEC-005 / FB-012 (base `allowedTools` shipping). DEC-004 and DEC-005 are independent: even a rich shipped `settings.json` with `Edit(.claude/tasks/**)` cannot unlock subagent writes to `.claude/tasks/`, per #38806. So DEC-004 should not block on DEC-005.
