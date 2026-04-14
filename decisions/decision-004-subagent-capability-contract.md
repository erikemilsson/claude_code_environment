---
id: DEC-004
title: Subagent capability contract — who owns task state transitions
status: approved
category: architecture
created: 2026-04-14
decided: 2026-04-14
related:
  tasks: []
  decisions: []
  feedback: [FB-010]
implementation_anchors: []
inflection_point: true
spec_revised:
spec_revised_date:
blocks: []
---

# Subagent capability contract — who owns task state transitions

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Fix the sandbox — subagents own Steps 6a/6b as documented
- [x] Option B: Formalize orchestrator ownership — docs and code move state transitions to parent `/work`
- [ ] Option C: Hybrid — subagents write what they can, orchestrator fills remaining gaps

*Check one box above, then fill in the Decision section below.*

---

## Context

The template's `implement-agent.md` and `verify-agent.md` define a workflow where spawned subagents own their own task-state transitions: implement-agent sets `Awaiting Verification` and spawns verify-agent (Steps 6a/6b); verify-agent writes `task_verification` and updates status to `Finished` (T6/T7). This is stated as an atomic contract in `system-overview.md`.

In practice (Phase 10 styler session, 7 tasks × 3 dispatch rounds), subagents spawned via the `Task` tool cannot:
1. Write to `.claude/tasks/` — Edit, Write, and Bash (even with `dangerouslyDisableSandbox: true`) return permission-denied despite additional working directories
2. Access the `Task` tool themselves — it's not in the agent's tool list and `ToolSearch` cannot find it

The orchestrator (parent `/work` agent) has to perform all state transitions manually: 14 JSON edits + 7 verify-agent dispatches + 7 verification persistences for that single session. Cost: orchestrator context pressure, slower parallel batches, workflow-contract violation (docs say one thing, runtime does another).

The choice is whether to treat this as a harness bug to fix (make the docs true) or a permanent constraint to accept (make the docs match reality). Both paths lead to different architectures.

## Questions to Research

1. **What are subagents *actually* allowed to do in the current Claude Code harness?** Investigate write access, tool availability, `additionalWorkingDirectories` propagation, Bash sandbox. Document definitively.
2. **Are there harness-level knobs that can change this?** Settings entries, tool configuration, `dangerouslyDisableSandbox`, permission file changes. Can the sandbox be relaxed for subagents writing to specific paths?
3. **If the harness can be changed, what's the scope?** Per-project via `.claude/settings.json`? User-level? Template-shipped?
4. **If the harness can't be changed, what's the cost of orchestrator ownership?** Context window pressure per batch, latency per task, change in agent-separation guarantees (does the orchestrator reading verify-agent output break "fresh eyes"?).
5. **Do other workflows in the Claude Code ecosystem face this pattern?** How do they handle subagent state transitions?

## Options Comparison

| Criteria | A: Fix Sandbox | B: Orchestrator Owns | C: Hybrid |
|----------|----------------|----------------------|-----------|
| Matches current docs | Yes | No (rewrite 5 files) | Partial (rewrite + dual-path) |
| Fresh-eyes guarantee | Preserved | Preserved (verify-agent still separate context; orchestrator only persists, doesn't re-judge) | Preserved |
| Orchestrator context cost | None | ~3N tool calls + ~200-500 tokens of verify output per task | Same as B in practice (fallback path always triggers) |
| Depends on harness changes | Yes — blocked on Anthropic issues #38806 and #19077, no timeline | No | No (but ideal path never triggers in current harness) |
| Implementation complexity | Low *if* harness changes — but no path exists today without building an MCP server | Medium — bounded 5-file rewrite (`implement-agent.md` 6a/6b, `verify-agent.md` T6/T7, `work.md` Step 4, `parallel-execution.md`, `system-overview.md`, `rules/agents.md`) | High — both paths plus failure-detection logic |
| Works today | No — `.claude/` protection cannot be bypassed by `Edit(.claude/**)` rules, `bypassPermissions`, or hooks (#38806). Subagents cannot use `Task` tool (#19077) | Yes | Partial — orchestrator path works, "ideal" path doesn't trigger |
| Aligns with Claude Code ecosystem convention | Against — most subagent libraries treat subagents as report-returning workers | With — main agent orchestrates, subagents return results | Mixed |
| Future-proofing | Best *if* upstream fixes land | Robust — works in any harness configuration | Pays both costs forever |
| Overall | Blocked by harness | **Recommended** | Worst of both worlds |

## Option Details

### Option A: Fix the sandbox

**Description:** Investigate and change the harness so spawned subagents can write to `.claude/tasks/` and use the `Task` tool. Keep implement-agent.md and verify-agent.md as-is. May require shipping `.claude/settings.json` changes (connects to DEC-005 / FB-012).

**Strengths:**
- Preserves the documented atomic implement→verify contract
- No changes to agent definitions, system-overview.md, or rules
- Keeps agent separation guarantees in their original framing

**Weaknesses:**
- Depends on harness being changeable — research shows it isn't, today
- The `.claude/` directory has a hardcoded protection layer that `Edit(.claude/**)` allow rules, `bypassPermissions` mode, and PreToolUse hooks all fail to override (Anthropic issue #38806, open with no timeline)
- Subagents cannot spawn the `Task` tool, even with `tools: Task` in frontmatter and `Task` in settings allow list (Anthropic issue #19077, open with no timeline)
- Subagents do not inherit parent permission rules from `settings.json` (#22665, #18950, #27661, #37730) — even fixing settings wouldn't help propagate to subagents
- The only contemporary unblock would require building an MCP server that writes JSON on the subagent's behalf — disproportionate infrastructure for a workflow concern

**Research Notes:**
- Per `code.claude.com/docs/en/permissions`: "`bypassPermissions` mode skips permission prompts. Writes to `.git`, `.claude`, `.vscode`, `.idea`, and `.husky` directories still prompt for confirmation." Documented exemption for `.claude/commands`, `.claude/agents`, `.claude/skills` is inconsistently honored per #38806.
- Per `code.claude.com/docs/en/sub-agents`: subagents have their own permission context, but multiple open issues confirm settings.json rules don't propagate.
- Full details and source list: `decisions/.archive/decision-004-research-2026-04-14.md`.

### Option B: Formalize orchestrator ownership

**Description:** Rewrite implement-agent.md and verify-agent.md so agents return structured reports and the orchestrator performs all state transitions. Update `system-overview.md` to state that state ownership is a `/work` coordinator responsibility, not an agent responsibility. Agents focus purely on producing deliverables and verification judgments.

**Strengths:**
- Matches observed runtime behavior — eliminates the contract violation
- No harness dependency — works today, works tomorrow regardless of upstream changes
- Cleaner separation: agents do work, orchestrator manages state. Easier to reason about race conditions in parallel mode (orchestrator already serializes JSON writes per the existing parallel-execution rules)
- Aligns with broader Claude Code ecosystem convention (subagents return results; main agent orchestrates)
- Bounded implementation: 5-6 file edits, well-scoped

**Weaknesses:**
- "Fresh eyes" framing needs adjustment in docs — verify-agent still runs in its own context (the actual fresh-eyes property), but the orchestrator does the JSON write. The docs should clarify that fresh eyes = separate verification context, not separate JSON writer
- Doc rewrite touches multiple files (implement-agent, verify-agent, work, parallel-execution, system-overview, rules/agents) — but each edit is small
- Orchestrator context absorbs verify-agent's structured report (~200-500 tokens per task). Across a 30-task project, ~6-12K tokens of verifier output flows through orchestrator. Notable but not catastrophic; the orchestrator was already reading the pass/fail summary anyway

**Research Notes:**
- Cost data from FB-010 (Phase 10 styler session): 7 tasks × ~3 orchestrator tool calls per task = 21 extra orchestrator operations across the batch. Persistence adds ~1-2s per task; in a parallel batch of 3, this serializes to ~3-6s after the 30-90s parallel implementation phase. Not a primary bottleneck.
- The "fresh eyes" property is preserved because it depends on verify-agent running in a separate Task context with no implementation memory — that property is independent of who writes the result JSON.
- Full reasoning: `decisions/.archive/decision-004-research-2026-04-14.md` § Q4.

### Option C: Hybrid

**Description:** Subagents attempt writes; if they fail, return a structured report. Orchestrator detects the report shape and performs fallback persistence. Docs describe both paths.

**Strengths:**
- In theory, would work in any harness configuration (current restrictive, future relaxed)
- Preserves the "ideal" path when possible

**Weaknesses:**
- In current harness, the "ideal" path *never* triggers (writes always fail). The hybrid degenerates to Option B + dead code
- Two code paths to maintain — both must be tested, both can drift
- Failure detection (subagent attempted write, returned failure marker) adds latency and complexity per task
- Doc burden is largest of the three options — must explain both paths and the routing logic
- Future-proofing benefit is hypothetical: if Anthropic fixes #38806 and #19077, the template could be updated reactively at that point with less effort than maintaining the dual path indefinitely

**Research Notes:**
- The "ideal path triggers" condition requires both #38806 and #19077 to be resolved upstream AND the user to be on a recent enough Claude Code version. Until both happen, the hybrid is operationally identical to Option B with extra plumbing.
- Discarded sub-approaches (MCP server for task JSON writes, polling-based IPC, symlink workarounds): all add infrastructure cost without clear short-term wins. See archive § "Discarded Approaches".

## Research Findings

### Q1: What are subagents actually allowed to do?

Definitively, in the current harness (April 2026):
- **Read** anywhere within cwd or `additionalDirectories`: yes
- **Write to project files within cwd**: yes (subject to permission mode)
- **Write to `.claude/tasks/`**: NO — `.claude/` is protected by a layer above the rule system; `Edit(.claude/**)` allow rules and `bypassPermissions` mode do not override it (Anthropic issue #38806)
- **Use the `Task` tool to spawn nested subagents**: NO — not exposed even when listed in frontmatter `tools:` (#19077)
- **Inherit parent's `permissions.allow` rules**: NO (#22665, #18950, #27661, #37730)
- **Inherit parent's hooks / CLAUDE.md / memory**: NO (#27661)

This matches FB-010's observation exactly. The Phase 10 session behavior is documented runtime behavior, not a template bug.

### Q2: Are there harness-level knobs that can change this?

No knob unlocks the two specific blockers. Things tried and confirmed not to work:
- `bypassPermissions` mode → does not bypass `.claude/` (#38806)
- `Edit(.claude/**)` / `Write(.claude/**)` allow rules in settings.json → ignored for `.claude/` paths (#38806)
- PreToolUse hooks returning "allow" → cannot override deny rules per docs explicitly
- `additionalDirectories` propagation → grants file access only, not configuration; `.claude/` protection is above this layer
- `tools: Task` in subagent frontmatter → reported as "Task tool not available" at runtime (#19077)
- `dangerouslyDisableSandbox: true` on Bash → still hits the `.claude/` protection because that protection is in Claude Code's permission layer, not the OS sandbox

The only theoretical unblock is **building an MCP server that performs JSON writes on the subagent's behalf** (MCP tools route through their own permission flow, separate from the `.claude/` protection). This is disproportionate infrastructure for a workflow-state concern.

### Q3: If the harness can be changed, what's the scope?

The harness cannot be changed by us — we don't ship the Claude Code binary. Two upstream paths exist, neither short-term:
- Anthropic resolves #38806 (allow `Edit(.claude/**)` to override the protection)
- Anthropic resolves #19077 (subagents can use Task tool)

Both are open issues with no published timeline. Even if both land, users would need to upgrade Claude Code, so the template would need to handle older versions — meaning Option B effectively becomes the floor regardless.

### Q4: Cost of orchestrator ownership?

From FB-010 actuals (7 tasks × 3 dispatch rounds):
- Orchestrator JSON edits: 14 (~2 per task: mark Awaiting Verification + persist verification)
- Orchestrator verify-agent dispatches: 7 (1 per task)
- Per task overhead: ~3 orchestrator tool calls

Context window cost: ~200-500 tokens of verifier output per task absorbed by orchestrator. Across 30 tasks, ~6-12K tokens — meaningful but not catastrophic.

**Fresh-eyes guarantee preserved.** The orchestrator persists the verifier's judgment, it doesn't re-evaluate. The "fresh eyes" property is about the verifier running in a separate context with no implementation memory — that property is independent of who writes the result JSON.

Latency: ~1-2s per persistence; in a parallel batch of 3, serializes to ~3-6s after the 30-90s parallel work phase. Not a primary bottleneck.

Implementation footprint: 5-6 files, well-scoped. See archive § Q4.

### Q5: Ecosystem precedent?

The broader Claude Code ecosystem treats subagents as **report-returning workers**, not state-mutating actors. Public subagent libraries (e.g., VoltAgent's collection of 100+ subagents) describe subagents as returning "results" the main agent acts on. This template is in a minority by attempting subagent-owned state transitions. Aligning with Option B is also aligning with ecosystem convention.

## Your Notes & Constraints

**Constraints:**
- Template-maintenance decision record — store at root `decisions/` (ephemeral, removed after resolution)
- Whatever is chosen must work for both sequential and parallel dispatch modes
- Independent of DEC-005 (base `allowedTools` shipping) — even a rich shipped `settings.json` cannot unlock subagent writes to `.claude/tasks/`, per #38806

**Research Questions (open for user judgment):**
- The verify-agent's `verification_history` append (T6) and the test_protocol/interaction_hint write (T7) are also subject to the same `.claude/tasks/` write block — under Option B, these all move to the orchestrator. Confirm this matches your intent. (Recommendation in B assumes yes.)
- The friction-marker emission to `.claude/support/workspace/.session-log.jsonl` (implement-agent and verify-agent) likely hits the same `.claude/` protection. Worth confirming via a focused test, but likely the same fix applies (orchestrator-mediated, or move the log path outside `.claude/`).
- If the user has seen any recent behavior where subagent JSON writes *did* succeed, that contradicts the research findings and warrants a focused reproduction test before committing to Option B.

## Recommendation

**Option B (formalize orchestrator ownership).**

**Key tradeoff:** Option B accepts that the documented "atomic agent-owned" contract was aspirational — it never matched runtime in the current harness. The actual atomicity (implement → verify, gated by passing verification before "Finished") is preserved; only the JSON-write responsibility moves from agents to orchestrator. The "fresh eyes" verification property is preserved because verify-agent still runs in a separate context. What's lost is a doc framing that read cleanly but produced a contract violation in every dispatch. What's gained is docs that describe what actually happens, and an architecture that aligns with the broader Claude Code ecosystem convention.

Option A is appealing but blocked on Anthropic upstream work (#38806, #19077) with no timeline. Option C pays both costs without the "ideal path" ever triggering in the current harness.

Confidence: high. The research is grounded in official Claude Code documentation, multiple corroborating GitHub issues, and the user's own Phase 10 observations. The implementation footprint is bounded. If Anthropic resolves the upstream issues later, the template can revisit — but only if the cost of orchestrator ownership turns out to be larger than the FB-010 evidence suggests, which currently it does not.

Decision research archive: `decisions/.archive/decision-004-research-2026-04-14.md`
