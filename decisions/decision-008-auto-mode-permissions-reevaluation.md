---
id: DEC-008
title: Auto-mode reevaluation — should DEC-005's shipped allowlist be retired, narrowed, or kept?
status: approved
category: process
created: 2026-04-17
decided: 2026-04-17
related:
  tasks: []
  decisions: [DEC-005]
  feedback: [FB-026]
implementation_anchors: []
inflection_point: true
spec_revised:
spec_revised_date:
blocks: [FB-037]
---

# Auto-mode reevaluation — should DEC-005's shipped allowlist be retired, narrowed, or kept?

## Select an Option

Mark your selection by checking one box:

- [ ] Option A: Full reversal — delete `.claude/settings.json`; rely entirely on auto mode
- [ ] Option B: Narrow to 6–8 essential entries (keep layered two-file model from DEC-005)
- [ ] Option C: Keep DEC-005 unchanged (15 entries)
- [x] Option D: Narrow AND document auto mode as the recommended primary layer in README + setup

*Check one box above, then fill in the Decision section below.*

---

## Context

DEC-005 (approved 2026-04-14, implemented `3cb10d8`) shipped `.claude/settings.json` with a 15-entry base `permissions.allow` set (read-only git/ls/grep/test/sort/shasum/head/wc/tree family) plus a layered `settings.local.json` for user additions. The decision was made assuming auto mode (`--permission-mode auto`) was not available to the user — Max plan support had not launched.

Between DEC-005 and today, auto mode became available on Max + Opus 4.7 (this user's configuration). Auto mode uses a server-side classifier model to approve tool calls without prompting. This changes the baseline assumption DEC-005 was built on: if the classifier already covers most of what the allowlist pre-approves, the shipped list may add complexity without adding value.

FB-026 flags this as an inflection-point reevaluation. FB-037 (optional PreToolUse hook for dev-server guarding in `setup-checklist.md`) is blocked on this decision — the hook recipe shape depends on whether DEC-005's layered-settings model stays, shrinks, or goes away.

**Critical research finding:** `permissions.allow` rules short-circuit the auto-mode classifier (rules are evaluated first; classifier only runs if no rule matches). The shipped allowlist is NOT dead code under auto mode — it reduces latency, saves classifier tokens, and applies in contexts where auto mode isn't active (dontAsk / CI, hooks).

## Questions to Research

(Answers in `## Research Findings` below.)

1. What does auto mode actually do, and what does it approve without prompting?
2. How does auto mode compose with `permissions.allow` — do rules short-circuit the classifier, or does the classifier run anyway?
3. What is the latency and token cost of the classifier per tool call?
4. What contexts (dontAsk, CI, hooks) don't have auto mode available?
5. How much of DEC-005's 15-entry base allowlist is redundant under auto mode, and how much is still load-bearing?

## Options Comparison

| Criteria | A: Full reversal | B: Narrow to 6–8 | C: Keep DEC-005 | D: Narrow + document |
|----------|:---:|:---:|:---:|:---:|
| Reduces maintenance | High (delete file) | Medium (smaller list) | None | Medium |
| Preserves dontAsk/CI utility | No (breaks CI) | Yes | Yes | Yes |
| Preserves hook execution | No (hooks hit prompts) | Yes | Yes | Yes |
| Avoids classifier latency on common ops | No (classifier runs) | Yes (for kept entries) | Yes | Yes |
| Unblocks FB-037 (hook recipe) | Yes (recipe references auto mode) | Yes (recipe is layered) | Yes (recipe is layered) | Yes (recipe is layered) |
| Backward-compat for users not on Max+Opus 4.7 | Breaks | Preserves | Preserves | Preserves |
| Breaking change for existing projects | Yes (file deletion) | Minor (reduced list) | None | Minor (reduced list) |
| Template simplicity signal | Strong | Medium | Weak | Medium |
| Documentation load | Low (remove settings section) | Low (update Settings section) | None | Medium (add auto-mode setup guidance) |

**Recommendation:** Option B or D — see `## Recommendation` below.

## Option Details

### Option A: Full reversal

**Description:** Delete `.claude/settings.json` from the template. Remove it from `sync-manifest.json`. Remove Part 5c (Settings Boundary Validation) from `/health-check`. Remove the Settings-layering bullet from `.claude/CLAUDE.md` Critical Invariants. Users are expected to enable auto mode (Max + Opus 4.7) for a prompt-free experience; users without auto mode fall back to manual approval per operation.

**Strengths:**
- Strongest template-simplicity signal — one less file, one less concept for template users to learn
- Lowest maintenance surface
- Aligns with the "rely on platform intelligence" philosophy that auto mode represents
- Clean for FB-037 (the hook recipe becomes a tight "here's how to add a PreToolUse hook in `settings.local.json`" with no template-owned settings file to worry about)

**Weaknesses:**
- Breaks dontAsk / CI contexts — any user running Claude Code non-interactively gets frequent prompt-equivalent failures
- Breaks hook execution — hooks run under the normal permission framework (not auto mode); without pre-approvals they'll hit permission denials mid-hook
- Breaks for users on Pro plan (no auto mode) or non-Opus models — the template becomes Opus-4.7+Max only for frictionless use
- Classifier latency: every shell command becomes a server round-trip; for sessions with many git/ls/grep operations (verify-agent, dashboard regen) the cumulative overhead is meaningful
- Undoes a decision that was explicitly made for domain-agnostic use — the template is designed to work for research, procurement, renovation projects where users may be on non-Opus models or non-Max plans

**Research notes:** Viable only if you're confident every downstream user is on Opus 4.7 + Max + has auto mode enabled. For this user's personal-use case that may be true; as a template design it's fragile.

### Option B: Narrow to 6–8 essential entries

**Description:** Keep the layered two-file model from DEC-005. Narrow `.claude/settings.json`'s `permissions.allow` from 15 entries to a core 6–8 that are both (a) commonly used by hooks/CI/verify-agent and (b) represent meaningful classifier-round-trip savings.

Proposed narrowed set:
```
Bash(git status:*)   — used by dashboard, verify-agent, hooks
Bash(git log:*)      — used by session recovery, status commands
Bash(git diff:*)     — used by verify-agent for change validation
Bash(ls:*)           — ubiquitous
Bash(grep:*)         — ubiquitous (shell grep; Grep tool is tool-level approved)
Bash(test:*)         — used by hooks for conditional logic
Bash(head:*)         — common for sampling
Bash(wc:*)           — common for size checks
```

Drop: `tree`, `unzip`, `sort`, `shasum`, `find`, `git check-ignore`, `git ls-tree` — most covered by auto mode or better expressed with dedicated tools (Glob for find, etc.).

Everything else about DEC-005 stays: layered `settings.local.json` for user additions, health-check Part 5c boundary validation, documentation.

**Strengths:**
- Reduces maintenance (fewer entries to justify) without breaking non-auto-mode contexts
- Preserves hook and CI utility — hooks that use `git status` / `test` still execute without prompts
- Preserves domain-agnostic design — users on Pro or Haiku still get friction-free common ops
- Classifier still engages for everything else; allowlist complements rather than replaces it
- Small, reversible change

**Weaknesses:**
- Some user-breaking potential if downstream projects lean on the removed entries (though `find` users already have Glob, `shasum` is specialized, etc.)
- Doesn't aggressively capture the auto-mode advantage for users who have it — they might still prefer Option A

**Research notes:** Matches the research agent's recommended middle path. Each kept entry has a concrete justification (hook usage, verify-agent usage, or high-frequency operation). Each dropped entry either has a tool-level replacement or was speculative-inclusion.

### Option C: Keep DEC-005 unchanged

**Description:** No change. The 15-entry allowlist stays. Auto mode layers on top where available; rules short-circuit the classifier; dontAsk contexts have full coverage.

**Strengths:**
- No breaking change for any existing project
- No implementation work
- Research confirms the allowlist is not dead code — rules still save latency and still apply in non-auto contexts

**Weaknesses:**
- Signals no response to FB-026's reevaluation — the inflection question was raised and answered "no change"
- Leaves some specialized entries (shasum, sort, unzip, tree) that aren't obviously load-bearing
- Doesn't acknowledge auto-mode's availability in user-facing documentation — users may not know to enable it

**Research notes:** Fully defensible given the "not dead code" finding. The argument for change is maintenance-minimization, not functional necessity.

### Option D: Narrow AND document auto mode as recommended primary

**Description:** Same allowlist narrowing as Option B, plus:
- Add an "Enabling auto mode" section to `.claude/README.md` (or setup-checklist) explaining when to use it, plan/model requirements, and what it composes with
- Update `.claude/CLAUDE.md` Settings invariant to mention the layered relationship with auto mode
- FB-037's eventual hook recipe goes in the same "Enabling auto mode" area for users who want hard blocks on top of the classifier

**Strengths:**
- All of Option B's benefits
- Plus: users are told about auto mode rather than having to discover it
- Sets up FB-037's implementation cleanly — the hook recipe has an obvious home next to the auto-mode documentation

**Weaknesses:**
- More documentation to maintain
- Risks "feature catalog" creep in the README — the template has deliberately kept setup guidance minimal

**Research notes:** A natural extension of Option B. The question is whether auto-mode documentation belongs in the template or is left for users to discover from Claude Code's own docs.

## Research Findings

### Q1: Auto-mode mechanics

Auto mode uses a server-side classifier model that reviews actions before they run. Documented behavior ([code.claude.com/docs/en/permission-modes](https://code.claude.com/docs/en/permission-modes)):

> "The classifier blocks actions that escalate beyond your request, target unrecognized infrastructure, or appear driven by hostile content Claude read."

**Default allowed without prompting:**
- Local file operations in working directory
- Installing dependencies from lock files / manifests
- Reading `.env` and sending credentials to matching APIs
- Read-only HTTP requests
- Pushing to current branch or new branches

**Default blocked:**
- `curl | bash` patterns
- Sensitive data to external endpoints
- Production deploys / migrations
- Mass deletion on cloud storage
- IAM / repo permission grants
- Force push / push to `main`

### Q2: Rule-classifier interaction

**Decision order** ([code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)):

1. Actions matching `deny` / `ask` / `allow` rules resolve immediately (rules short-circuit classifier)
2. Read-only actions and working-directory file edits auto-approve (skip classifier)
3. Everything else goes to the classifier
4. If classifier blocks, Claude tries an alternative

**Implication:** `permissions.allow` rules pre-empt the classifier. They are not redundant. Each rule saves a server round-trip.

**Additional behavior:** "On entering auto mode, broad allow rules that grant arbitrary code execution are dropped: Blanket `Bash(*)`, Wildcarded interpreters like `Bash(python*)`, Package-manager run commands, `Agent` allow rules. Narrow rules like `Bash(npm test)` carry over." DEC-005's entries are narrow (wildcards bounded to specific commands), so they carry through.

### Q3: Classifier latency and token cost

From the docs: "Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations."

Quantitative data not published, but for sessions with many shell commands (verify-agent runs ~5–10 `git`/`test` calls per task) the cumulative cost is non-trivial.

### Q4: Contexts where auto mode is not available

- **dontAsk mode:** mutually exclusive with auto mode. Used in CI / non-interactive contexts.
- **Hooks:** PreToolUse and PostToolUse hooks run in the normal permission framework — they do not gain classifier intelligence. A hook that shell-execs `git status` still relies on `permissions.allow` (or triggers a prompt).
- **Plan availability:** Auto mode requires Max, Team, Enterprise, or API plan. Not available on Pro.
- **Model availability:** Requires Opus 4.7 on Max. Sonnet and Haiku configurations do not get auto mode under Max.
- **Provider:** Anthropic API only — not Bedrock, Vertex, or Foundry.

### Q5: DEC-005 entry-by-entry redundancy analysis

| Entry | Covered by classifier? | Hook / CI usage? | Verdict |
|-------|:---:|:---:|---|
| `Bash(git status:*)` | Yes (read-only) | Yes (hooks, verify) | Keep (latency savings) |
| `Bash(git log:*)` | Yes (read-only) | Yes (session recovery) | Keep |
| `Bash(git diff:*)` | Yes (read-only) | Yes (verify-agent) | Keep |
| `Bash(git branch:*)` | Yes | Low | Drop (rare outside `git status`) |
| `Bash(git check-ignore:*)` | Yes | Low | Drop (specialized) |
| `Bash(git ls-tree:*)` | Yes | Low | Drop (specialized) |
| `Bash(ls:*)` | Yes (read-only) | Yes | Keep |
| `Bash(tree:*)` | Yes | Low | Drop (`ls -R` covers) |
| `Bash(wc:*)` | Yes | Yes (size checks) | Keep |
| `Bash(head:*)` | Yes | Yes (sampling) | Keep |
| `Bash(grep:*)` | Yes | Yes | Keep (shell grep; Grep tool is separate) |
| `Bash(find:*)` | Yes | Low | Drop (Glob tool preferred) |
| `Bash(test:*)` | Partial | Yes (hook conditionals) | Keep |
| `Bash(sort:*)` | Yes | Low | Drop (pipe-side utility) |
| `Bash(shasum:*)` | Partial | Low | Drop (specialized) |

**Result:** 8 entries recommended to keep; 7 recommended to drop. Consistent with Option B's proposed narrowing.

## Your Notes & Constraints

*Add any constraints, preferences, or context that should inform this decision.*

**Constraints:**
- Template-maintenance decision record — ephemeral, removed after resolution
- Domain-agnostic design: template must remain useful for users on non-Max plans or non-Opus models
- FB-037 (hook recipe) is blocked on this decision — outcome should make the recipe implementable
- Inflection-point: a full reversal would trigger `/iterate` to revisit downstream assertions

**Research questions for the user:**
1. **Auto-mode adoption signal:** Do you want the template to actively promote auto mode (Option D's extra documentation), or let users discover it independently (Option B)?
2. **Downstream compatibility:** Are any existing projects using this template on Pro plans, or running with Sonnet/Haiku, where they'd notice allowlist changes? If yes, Option A is too aggressive.
3. **Hook-recipe preview for FB-037:** Once this decision closes, FB-037's hook recipe will likely reference the same `settings.local.json` layer. Any reason that layer should change shape as part of this decision?
4. **Classifier latency tolerance:** The `git status` / `git diff` calls made by verify-agent during every task verification are the most frequent shell calls in the template. Is the cumulative classifier round-trip cost a concern, or acceptable for the simplicity of Option A?

## Recommendation

**Option B (narrow to 8 entries, keep layered model) is the primary recommendation. Option D is a valid upgrade if documentation of auto mode is desired.**

**Why B (or D) over the alternatives:**
- vs. **A:** Full reversal breaks hooks, CI, and non-Max users. Simplicity gain is outweighed by the loss of domain-agnostic support. Auto-mode availability is specific to Max+Opus 4.7; template users beyond this user's personal config may not have it.
- vs. **C:** DEC-005's 15 entries include several speculative inclusions (shasum, sort, unzip, tree) without clear load-bearing use. Narrowing is honest to the evidence.
- vs. **D:** D is B plus documentation. The choice depends on whether auto-mode promotion fits the template's minimal-setup philosophy.

**Inflection-point note:** This is not a full reversal of DEC-005 — the layered two-file model stays; only the entry count shrinks. The inflection marker is conservative in case narrowing reveals more changes (e.g., if health-check Part 5c needs rewording). Expect `/iterate` to consult this decision and check whether the Settings invariant language in `.claude/CLAUDE.md` needs updating.

**FB-037 unblock implication:** Under B or D, the FB-037 hook recipe references the same `settings.local.json` pattern as today. The recipe documentation becomes: *"Add a PreToolUse hook under the `hooks` key in `.claude/settings.local.json`; if you use auto mode, this hook runs before the classifier and can hard-block even classifier-approved actions."* Clean and unambiguous.

**Confidence:** High on research (mechanics well-documented). High on Option B over Option A (dontAsk/hook breakage is a concrete issue). Moderate between B and D (a documentation judgment call). Low on Option C as a forward path (status quo without an argument for it).
