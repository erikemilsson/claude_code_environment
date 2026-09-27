# Claude Code Authoring Hazards

Load-bearing facts about the Claude Code platform that spec, skill, agent, and command authors need to know — and that aren't obvious without hitting a wall during implementation.

This doc is **additive and cross-referencing**: it consolidates facts not currently surfaced elsewhere (turn-scoped frontmatter, skill-content lifecycle, etc.) and cross-links to facts already canonically placed (subagent isolation in `agents.md`, MCP constraints, etc.).

**Last verified:** see footer at bottom of file.

---

## YAML Frontmatter Hazards

### Colon-space in `description:` field

The `description:` field in YAML frontmatter rejects unquoted `: ` (colon-space) under strict YAML 1.2 / PyYAML — the parser treats the second colon as an ambiguous mapping-value token and fails. Claude Code's deployment parser is permissive (silently loads the skill anyway), so the failure mode is silent at runtime but `verify-agent`'s strict YAML check rejects.

**Convention:** use em-dash (` — `) or quote the entire description value.

**Examples:**

```yaml
# BAD — strict YAML rejects
---
description: My skill: does the thing
---

# GOOD — em-dash separator
---
description: My skill — does the thing
---

# ALSO GOOD — quoted value
---
description: "My skill: does the thing"
---
```

The em-dash convention is the empirically-converged pattern across the template's 5+ SKILL.md files. Source: FB-082 (flirty-gym 2026-05-20, surfaced when verify-agent's PyYAML check failed on initial skill authoring; convergence on em-dash documented after T12 retry).

### Other ambiguous-mapping-value tokens

Beyond colon-space, avoid unquoted YAML values that begin with `[`, `{`, `&`, `*`, `!`, `|`, `>`, `'`, `"`, `%`, `@`, `` ` ``. These are also strict-YAML special-meaning tokens. If a description must start with one of these, quote the entire value.

---

## Skill Frontmatter Scope

### `model:` and `effort:` are turn-scoped, not session-scoped

Per `code.claude.com/docs/en/skills`: *"The override applies for the rest of the current turn and is not saved to settings; the session model resumes on your next prompt."*

This means:

- A skill that sets `model: opus` in its frontmatter overrides the model **for the rest of the current turn only**
- On the next user prompt, the session model (whatever was active before the skill) resumes
- **A multi-turn chat skill cannot rely on `model:` for cross-turn model continuity** — the override does not persist across turns

Two further `model:` details from the docs: a value excluded by the organization's `availableModels` allowlist is ignored (the session keeps its current model), and under `context: fork` the field sets the **forked subagent's** model instead of overriding the turn.

`effort:` applies *"when this skill is active"* and overrides the session effort level. The docs do **not** say whether that ends with the turn the way `model:` does, so don't design a multi-turn skill around `effort:` continuity either.

**Implications for spec authoring:**
- Don't write spec text describing runtime model-switching as a feature of a multi-turn skill (this premise survived flirty-gym's spec authoring + task decomposition and only failed at implementation — see FB-083)
- For multi-turn flows requiring a specific model, the session model must be set by the user (CLI flag, `/model` slash command, settings file) — not by skill frontmatter

### `disable-model-invocation: true`

Prevents the model from autonomously invoking the skill via the `Skill` tool. User-typed slash invocation continues to work; the model can still suggest the skill in conversation. The gate only blocks the model's autonomous decision to fire.

Two further effects: the skill also cannot be **preloaded into subagents** (via an agent definition's `skills` field), and, as of Claude Code v2.1.196, it **does not run when a scheduled task fires with the skill as its prompt**. For this template, that means the gated commands below can't be the prompt of a `/schedule` or `/loop` routine.

**Template-shipped gated commands** (FB-071, plus FB-070's `/zoom-out`): `/breakdown`, `/research`, `/iterate`, `/work`, `/feedback`, `/zoom-out`. Selection criteria and trade-offs (moved here from `rules/agents.md` 2026-09-27 to keep the auto-loaded rules lean):

**Selection criteria:**
- **Gate**: substantive writes, irreversible state transitions, ledger changes, expensive/long-running flows where autonomous fire is a foot-gun.
- **Leave open**: read-only audits (`/status`, `/health-check`, `/review`, `/audit-coherence` / `/audit-ui` non-triage modes) and conversational entry points where the model legitimately benefits from being able to ambient-invoke.

**Sub-mode coupling.** `disable-model-invocation` is per-file. Multi-mode commands (`/iterate`, `/work`, `/feedback`) gate as a whole — the model can no longer ambient-invoke their read-only sub-modes (`/work` no-args, `/iterate` no-args, `/feedback [text]` capture, `/feedback list`) either. Acceptable because user-typed slash invocation continues to work for all sub-modes, and the model can still surface suggestions in conversation. Future refactor option: split multi-mode files (e.g., `work-complete.md` separate from `work.md`) if the coupling produces observed friction.

**Defense-in-depth.** Upstream of DEC-005 (permission-layer auto mode) and DEC-016 (spec/decision/vision Edit/Write ask). DEC-005 catches tool calls the model shouldn't make; DEC-016 catches writes to protected paths; this gate prevents the model's *decision* to fire the command in the first place. All three layers compound.


### `context: fork` + `agent:` pattern

A skill can declare `context: fork` to run as a new subagent of the type named by `agent:` (built-in `Explore` / `Plan` / `general-purpose`, or any custom agent from `.claude/agents/`; **defaults to `general-purpose`** when omitted). The subagent gets the agent type's system prompt, the SKILL.md content as its task, and **CLAUDE.md per that agent's startup context** — except the built-in `Explore` and `Plan`, which skip CLAUDE.md and git status (so `agent: Explore` sees only SKILL.md + its own system prompt). It does **NOT** see the parent's conversation history.

**Runs in the background by default** (since Claude Code v2.1.218): you keep working, and the result arrives in the conversation when it completes. Set `background: false` to block the invoking turn until it finishes, which older harnesses always did.

**Authoring guidance:** if a skill's instructions must reference parent-conversation state, do NOT use `context: fork`. Forked skills are best for self-contained workflows where the SKILL.md body fully specifies the work. If a later step in the same turn needs the fork's result, set `background: false`.

### `allowed-tools` and `permissions.allow` interaction

A skill's `allowed-tools` frontmatter **pre-approves** the listed tools so Claude can use them without prompting. The grant lasts **only for the turn that invokes the skill**: it clears when the user sends the next message, even though the skill content stays in context (see "Skill content lifecycle" below). Re-invoking the skill re-applies it for that turn. Workspace trust doesn't gate it.

It is a pre-approval, **not a restriction**: every tool stays callable, and permission settings still govern unlisted tools. Use the separate `disallowed-tools` field to remove tools while the skill is active. Declare only the tools the skill actually needs. Over-declaring grants unnecessary access; under-declaring triggers permission prompts mid-execution. Multi-turn skills get prompts on later turns regardless.

### Skill listing budget: dynamic total (~1% of context) + 1,536-char per-entry cap

Two distinct limits govern the skill listing (the metadata the model sees to decide what to invoke) — don't conflate them:

- **Total listing budget — dynamic, not fixed.** It scales at **~1% of the model's context window**. All skill *names* are always included; when the budget overflows, the *descriptions* of the least-invoked skills are dropped first, so the skills you actually use keep their full text. Raise it with the `skillListingBudgetFraction` setting (e.g. `0.02` = 2%) or the `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var (fixed char count); set low-priority entries to `"name-only"` in `skillOverrides` to reclaim budget.
- **Per-entry cap — 1,536 chars.** Each skill's combined `description` + `when_to_use` is capped at **1,536 characters regardless of the total budget** (configurable via the `skillListingMaxDescChars` setting — renamed; an older `maxSkillDescriptionChars` key does nothing). Put the key use case first; keep `when_to_use` to usage criteria, not a feature catalog.

**Observability:** `/doctor` estimates the listing's context cost and names its biggest contributors; `/skill-doctor` finds unused skills worth turning off; the Skills row in `/context` reports the post-budget listing size (what the model actually receives); overflow also writes a warning to the `--debug` log.

### Auto-compaction re-attachment: first 5K tokens per skill, 25K combined

When auto-compaction summarizes the conversation, Claude Code re-attaches the **most recent invocation of each skill** after the summary, keeping only the **first 5,000 tokens** of each. All re-attached skills share a **combined 25,000-token budget**, filled starting from the most recently invoked skill, so after many invocations in one session, older skills can be **dropped entirely**.

**Authoring guidance:** put everything that must survive compaction in the first ~5K tokens of the SKILL.md body. Offload large reference content to separate files under the skill's directory (referenced from SKILL.md, loaded only when needed).

### Skill content lifecycle: one-message-and-stays-for-session

The rendered SKILL.md content enters the conversation as one message and remains in the context for the rest of the session. This changes the spec/skill authoring model in two ways:

1. **Written guidance must be standing instructions, not one-time steps.** If the SKILL.md says "first do X, then do Y", the message persists — when the same skill is invoked again later in the session, the same "first do X" instruction is still in context. Authors should write skill bodies as *patterns* that apply to every invocation, not as *procedures* that fire once.

2. **Re-invocation is cheap only when the rendered content is identical.** Re-invoking a skill whose rendered content matches the copy already in context adds just a short "already loaded" note. If the rendered content *differs* (different arguments, or a dynamic-context `` !`command` `` produced new output), the **full content is appended again**. Keep argument-varying and dynamic-context skill bodies small; for static skills, optimize for first-load cost.

Only the *instructions* persist, not the permissions: the `allowed-tools` grant clears after the invoking turn (see "`allowed-tools` and `permissions.allow` interaction" above).

---

## Subagent Boundaries

Load-bearing constraints for spec and task authors. Full rules in `rules/agents.md § "State Ownership"` and `§ "Tool Preferences"`. The facts here are the ones spec/skill/agent authors most frequently violate.

### No `.claude/` writes (DEC-004)

Subagents are sandboxed from writing to `.claude/` paths. This is a hard Claude Code harness constraint, not a template convention. Spec authors must NOT specify subagent workflows that include writing task JSON, dashboard, decision records, friction.jsonl, or any other `.claude/` state. Subagents return structured reports; the orchestrator performs the writes.

### Nested dispatch: platform-supported, template-avoided

**Platform fact (docs-verified 2026-09-25):** a subagent *can* spawn subagents of its own, by default up to **three layers** below the main conversation, configurable with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`. At the depth limit, Claude Code withholds the `Agent` tool (a fork keeps it in its tool list, but calling it errors). Older harnesses did not allow nesting at all.

**Template convention: don't rely on it.** The orchestrator (`/work` or a top-level slash command) still performs all dispatch. Two reasons: portability to downstream projects on older harnesses, and the state-ownership model (only the orchestrator writes `.claude/`, so results must come back to it anyway). Spec authors should not specify nested-dispatch workflows unless a project deliberately pins a harness that supports them. `rules/agents.md` still states the older "cannot spawn nested `Task` calls" wording; reconciling it is tracked as a maintenance FB.

### Permission rules and modes in subagents

**Harness-observed (not documented either way):** subagents do not inherit the parent conversation's session-approved `permissions.allow` rules; each dispatch operates under the settings-file allow set. Spec authors must NOT assume tools approved ad hoc in the parent are available in subagents.

**Documented, permission *mode*:** when the main conversation is in `bypassPermissions`, `acceptEdits`, or **auto mode**, the subagent runs in that same mode and its `permissionMode` frontmatter is ignored. Under auto mode, the classifier evaluates the subagent's tool calls with the main conversation's block and allow rules. In `default`, `dontAsk`, or `plan` mode, the subagent's own `permissionMode` applies.

### Explore / Plan agents skip CLAUDE.md + git status

Built-in `Explore` and `Plan` subagent types do NOT auto-read CLAUDE.md or run git status before working. Spec authors expecting agent-side context-awareness must either (a) include the context in the dispatch prompt, OR (b) use a different subagent type (e.g., `general-purpose`).

### Forked-skill context inheritance

Skills declared with `context: fork` get the SKILL.md content, the agent type's system prompt, and CLAUDE.md per that agent's startup context (`Explore` / `Plan` skip CLAUDE.md). They do NOT inherit the parent's conversation history, and by default they return their result in the **background**, not within the invoking turn. Spec authors must NOT design forked-skill workflows that depend on parent-conversation state. Full detail: "`context: fork` + `agent:` pattern" above.

---

## Tool & Dispatch Surface

### `Agent` tool `model` parameter granularity

The subagent model surface (per-invocation `model` parameter + agent-definition `model:` frontmatter) accepts: the aliases `sonnet | opus | haiku | fable`; a **full model ID** (e.g., `claude-opus-5-5` — same values as the `--model` flag); or `inherit` (use the main conversation's model). Resolution order: **per-invocation `model` parameter → agent definition's `model:` frontmatter (`inherit` = main model) → `CLAUDE_CODE_SUBAGENT_MODEL` env var → main conversation's model.** The env var is a *default*, not an override. **Exception:** with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` (Claude Code v2.1.257+), every subagent runs on `CLAUDE_CODE_SUBAGENT_MODEL` (or on the main model if only the force flag is set). Definition `model:` fields are then ignored, and **Claude can't pass a per-invocation `model`**, so the template's `"opus[1m]"` dispatch value is silently overridden in such an environment. (Verified against the sub-agents docs page 2026-09-25; the order changed since the 2026-06-11 check, which had the env var first. The template's dispatch value `"opus[1m]"` is a documented model alias (model-config docs, checked 2026-09-27); on Opus 4.7 and later the `[1m]` suffix is redundant on the Anthropic API because 1M is native.)

Effort: there is no per-invocation effort parameter, but agent definitions take an `effort:` frontmatter field (`low | medium | high | xhigh | max`; available levels depend on the model) that overrides the session effort while that subagent is active. Ad-hoc dispatches without a custom agent definition inherit session-level effort — prompt-engineering ("ultrathink") remains the lever there. `ultrathink` adds an in-context instruction for that turn; the effort level sent to the API is unchanged (model-config docs, checked 2026-09-27).

**Implication:** spec authors CAN vary the model per subagent dispatch (alias or explicit full-ID pin), and can vary effort by defining a custom agent with `effort:` frontmatter. For ad-hoc dispatches, effort still rides the session level.

### `subagent_type: "general-purpose"` portability convention

Per `rules/agents.md § "Dispatch Convention"`: the three dispatch sites (`commands/work.md` per-task verify, phase-level verify; `commands/research.md` research-agent) use `subagent_type: "general-purpose"` and direct the agent persona via prompt content. This is portable across all current Claude Code harness versions. Future migration to named subagent types is gated on `.claude/agents/*.md` auto-discovery stability.

**Why not named subagent_types?** Claude Code can auto-discover `.claude/agents/*.md` and expose each definition file as a named subagent_type (`implement-agent`, `verify-agent`, etc.), which would align dispatch shape with definition shape. As of 2026-05-13, the runtime availability of named-from-disk subagent types is not uniform across Claude Code harness versions — relying on auto-discovery risks dispatch failures in harnesses where it's absent. The persona-via-prompt-content pattern is portable across all current harness versions.

**Future migration:** When Claude Code's `.claude/agents/*.md` auto-discovery is stable across all supported harness versions, switch the three dispatch sites to named types. Validation gate: smoke-test by dispatching a single task with `subagent_type: "verify-agent"` and confirming the agent returns a per-task verification report (vs an error). Once validated, sweep all three sites and remove this rationale.

**Spec authors:** do not write tasks that reference named subagent types directly. Reference the orchestrator's dispatch behavior or the agent's prompt body instead.

---

## MCP Constraints

(Pointers — do NOT consolidate. Full rules live with the surrounding agent dispatch context.)

- **`support/reference/mcp-patterns.md § "MCP and Parallel Execution"`** — single-session MCPs (Playwright, browser automation) cannot be safely fanned out across parallel subagents. Orchestrator pattern: route MCP-driving work through one agent; parallelize the rest.
- **`support/reference/mcp-patterns.md § "MCP and Result-Size Constraints"`** — Playwright MCP `browser_snapshot` returns full accessibility tree; on long-scroll pages (~10K+ char DOM) the result truncates silently. Prefer `browser_evaluate` with targeted DOM queries.

---

<!-- Last verified against Claude Code docs: https://code.claude.com/docs @ 2026-09-25; against template_version: 5.5.0 -->
