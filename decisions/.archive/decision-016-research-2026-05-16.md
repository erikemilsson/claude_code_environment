# Research Archive: DEC-016 — Claude direct-edit guardrail on `.claude/spec_v*.md`

**Date:** 2026-05-16
**Researcher:** research-agent (Opus 4.7)
**Decision record:** `decisions/decision-016-spec-file-edit-guardrail.md`
**Feedback source:** FB-007 (`.claude/support/feedback/feedback.md`)
**Predecessor:** DEC-013 (audit-system `[Fix it]` HARD RULE — closed the inline-apply surface; DEC-016 closes the broader behavioral surface)
**Related decisions:** DEC-005 (base allowedTools shipping policy — Option E layered model), DEC-008 (auto-mode reevaluation — narrowed allowlist, classifier short-circuit behavior)

---

## Investigation Methodology

1. Read decision record draft (Options A-D pre-populated, 8 research questions Q1-Q8, criteria table seeded but unevaluated)
2. Read FB-007 source entry in `.claude/support/feedback/feedback.md` (refined capture from 2026-05-16; preserved styler `coherence-2026-05-15-2337` C-01 observation)
3. Read predecessor decision DEC-013 (audit-fix-it autonomy boundary) for layered-enforcement precedent and HARD RULE pattern that DEC-016 extends
4. Audited template state for current enforcement surfaces:
   - `.claude/rules/spec-workflow.md` (verbatim text of "direct edits are safe" claim; full Propose-Approve-Apply rule)
   - `.claude/commands/audit-coherence.md` lines 380-480 (synthesizer HARD RULE FIRST, kind classification, action table)
   - `.claude/settings.json` (template-owned base permissions; only 9 entries today — read-only git/ls/grep/test/head/wc plus python3 scripts)
   - `.claude/settings.local.json` (hook landing surface; currently has PreCompact hook only, no PreToolUse)
   - `.claude/support/reference/extension-hooks.md` (canonical map of project-extension landings — confirms `settings.local.json` is the documented user-hook surface)
5. Reviewed DEC-005 (base allowedTools — Option E established the two-file split) and DEC-008 (narrowed list, documented classifier short-circuit) for permission-layer precedent
6. Web research on PreToolUse hook capabilities (load-bearing Q3):
   - Anthropic official: `code.claude.com/docs/en/hooks` (full hook reference, decision control semantics, JSON input shape)
   - Anthropic official: `code.claude.com/docs/en/permissions` (permission rule syntax, `Edit(path)` gitignore-glob support, rule evaluation order, mode interactions)
   - Web searches for hook matchers, ask-rule behavior, provenance/source field availability, and managed-hooks bypass behavior
7. Reviewed existing archive style (`decisions/.archive/decision-005-research-2026-04-14.md`) for format conventions

---

## Q1 Research: Is provenance trackable (audit-sourced vs free-form)?

### Direct evidence from the Claude Code platform

**For permission rules (settings.json):** rule matching is on `Tool` + path/argument specifier only. There is no "which command invoked this" or "which slash command initiated the call" filter available in the permission rule syntax. The rule grammar (per [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions)) is `Tool` or `Tool(specifier)` with gitignore-style globs for file paths and bash wildcard patterns for shell commands. Slash-command source is not part of the matchable surface.

**For PreToolUse hooks:** the JSON input shape (per [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)) includes:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": { "file_path": "...", "old_string": "...", "new_string": "..." },
  "tool_use_id": "unique_id",
  "effort": { "level": "medium" }
}
```

Notably **absent** from this payload: any field equivalent to "active slash command" or "invocation source." `session_id` identifies the conversation, not the command being executed. `transcript_path` points at the JSONL but a hook would have to read+parse the transcript to infer "the user just typed `/iterate`" — that's an expensive and racey heuristic, not a structured signal.

(Web search reveals `UserPromptExpansion` hooks do receive `command_name` / `command_source` fields when a slash command is being expanded, but `UserPromptExpansion` fires at *prompt-expansion time* — not at *tool-call time*. Edits during a slash command's execution are PreToolUse events, not UserPromptExpansion events. So even with that field present in another hook type, it can't directly gate Edit calls.)

### Application to FB-007's "audit-sourced" qualifier

Option A's qualifier — "edits whose origin is an audit finding's `iterate_routing` MUST route through `/iterate`" — requires Claude to *self-classify* the edit as audit-sourced. The mechanisms available are:

1. **Behavioral self-classification.** Claude reads the rule clarification, recognizes the audit context (because it just read a `findings.md` or invoked `[Fix it]`), and routes accordingly. This is the rule-only approach: no platform mechanism enforces the classification — it's pure behavior.
2. **Synthesizer-side tagging.** The audit synthesizer already writes `iterate_routing.target: "/iterate"` for `kind: decision` items (per DEC-013 HARD RULE, `audit-coherence.md:397`). Claude reading that field is the existing signal.
3. **No platform-enforced provenance.** There is no way for a hook or permission rule to read "this Edit call was triggered by Claude having just read findings.md" — the runtime doesn't track that.

### The downside of Option A's reliance on self-classification

In the observed C-01 incident, the audit-routing context was *present* — Claude had just read the audit's `findings.md` and processed `iterate_routing` annotations. The rule that triggered the bypass was `spec-workflow.md`'s "direct edits are always safe" override. Adding Option A's clarification fixes the **rule-source tension** (which currently has two contradictory rules and the wrong one wins), but it doesn't add any **enforcement** beyond Claude's own reading.

**Implication:** if FB-007's primary failure mode is rule-contradiction-induced bypass (the observed pattern), Option A's clarification is sufficient. If it's a behavioral pattern that recurs even when the rule is unambiguous, Option A degenerates to "all spec edits route through /iterate" — broader than intended, and the natural endpoint is something like Option C's structural gate (which doesn't rely on Claude reading the rule).

### Verdict for Q1

**Provenance is not trackable at the permission-layer/hook-layer level.** "Audit-sourced" can only be identified behaviorally by Claude itself. Option A is therefore a *behavioral* rule clarification, not a *structural* enforcement. It depends on Claude reliably reading and applying the rule — which is exactly what failed in the originating incident.

This finding *materially weakens* Option A as a stand-alone choice and *materially strengthens* the case for either (a) broadening Option A to "ALL spec edits route through `/iterate`, regardless of source" or (b) adding a structural layer (Option C) that doesn't rely on self-classification.

---

## Q2 Research: What's the right N for Option B's size threshold?

### Empirical data sources

The decision record asks: "typical drift-sweep edit sizes in the styler / template-maintenance history; pre-existing thresholds in other parts of the template (if any); analogous patterns in other agent frameworks."

**Template-side thresholds.** The template has no existing line-based or size-based thresholds for edit-class autonomy. The Propose-Approve-Apply pattern uses *kind* (infrastructure operations vs substantive text edits), not *size*. Drift detection (`drift-reconciliation.md`) uses *section_fingerprint* hash matching, not line counts. The audit family's bundle-eligibility criteria use *file count* (≤3 files) — but that's per-finding scope, not per-edit-size.

**Observed C-01 incident sizes.** Per FB-007's verbatim capture: "5 direct `Edit` calls on `spec_v13.md` to sweep residual noun-drift (`Personalized principles` → `Archetype Principles`)." Each Edit was a single-token replacement. If counted as line diffs, each is ~2 lines (one removal, one addition per Edit). 5 edits × 2 lines = ~10 lines net. If counted as "lines containing the changed token" it's also ~5-10 lines.

**Industry analogues.**
- Linter "diff stat" thresholds (CI tools like Danger.js) commonly use 200-500 lines as a "needs human review" threshold for PR size. Not analogous because they target review burden, not "safe to edit autonomously."
- Cursor 2.0 / Composer (per DEC-013 Q2 research) uses *no* size threshold; it presents the full diff regardless of size.
- GitHub Copilot agent mode uses *file count* (similar to bundle-eligibility) plus per-file diff preview, not absolute line count.
- The closest "small enough to apply directly" pattern in published prior art is **lint-fix autonomy** — autofix-eligible warnings apply without prompting in ESLint, Prettier, ruff. Their criterion isn't line count but **rule-class** (the rule's autofix output is deterministically reversible). This is closer to DEC-013's bundle-eligibility criteria than a line threshold.

### What "small enough to apply directly" actually means

Reframing Q2: the user-stated rationale in FB-007 was "keep Claude's ability to do trivial sync-style sweeps without round-tripping." The valuable autonomy isn't "any small change" — it's "deterministic sync from an authoritative source to a derived/dependent location." That's precisely DEC-013's bundle-eligibility criteria (source-confirmed, reversible, no new judgment) **without a line threshold**.

If the carveout's purpose is to preserve sync-style autonomy, **line count is the wrong axis**. The right axis is *fix kind* — which is the axis DEC-013 already uses for `[Fix it]` (bundle-eligible vs fix-eligible vs decision vs design). For spec/decision/vision files specifically, DEC-013 already says ALL changes route through `/iterate` — there is no "small enough" carveout in the audit family. The HARD RULE classifies ALL spec/decision/vision edits as `kind: decision` regardless of size.

### Concrete N values if Option B were pursued

If the user explicitly wants a numeric threshold despite the above:

- **N = 1 line (single-line edit):** captures the noun-rename case observed in C-01. But trivially boilable-frog — 10 separate 1-line Edits accumulate to 10 lines of substantive change.
- **N = 5 lines:** captures the C-01 sweep (5 Edits × ~2 lines each = ~10 lines, but per-Edit each ≤ 2 lines). Still boils — the cumulative footprint isn't bounded.
- **N = 10 lines:** allows multi-paragraph drift sweeps. Inconsistent with the audit family's "ALL spec-touching findings → /iterate" rule (DEC-013).
- **N as percentage of file:** even worse — spec_v13.md in styler is thousands of lines; 1% is dozens of lines.

### Verdict for Q2

**There is no defensible N.** The "size-based carveout" framing presumes "small changes are safe" — but the C-01 incident specifically demonstrated that small changes (5 single-token edits totaling ~10 lines) can bypass the workflow contract even when individually trivial. Option B's threshold doesn't address the structural concern; it just sets a smaller boil-the-frog window.

**Stronger framing:** the autonomy axis users actually want isn't size — it's *kind*. DEC-013 already established this axis for the audit family. Option B as proposed (line-count threshold) duplicates a less-precise version of work DEC-013 did better. Recommend Option B be **discarded** in favor of either Option A (rule-only) or Option C (structural).

If the user pushes back and wants *some* autonomy carveout for spec edits, the right framing is "infrastructure operations" — which is already in the Propose-Approve-Apply rule (`archiving, version transitions, frontmatter updates`). Extending that enumeration explicitly (e.g., adding "section-fingerprint-preserving whitespace normalization") would be a *kind-based* carveout, not a size-based one. That's a rule clarification, not a new threshold.

---

## Q3 Research: PreToolUse hook precedent + feasibility (LOAD-BEARING)

This is the question that determines whether Option C is technically viable. Lead findings:

### A1: Path-pattern matching on Edit/Write is fully supported via permission rules alone

Per the official [Configure permissions](https://code.claude.com/docs/en/permissions) doc:

> `Edit` rules apply to all built-in tools that edit files. … Read and Edit rules both follow the [gitignore](https://git-scm.com/docs/gitignore) specification with four distinct pattern types: … `path` or `./path` — Path **relative to current directory** — `Read(*.env)` — `<cwd>/*.env`

A rule of the form:

```json
{
  "permissions": {
    "ask": [
      "Edit(.claude/spec_v*.md)",
      "Write(.claude/spec_v*.md)"
    ]
  }
}
```

is well-formed, uses gitignore-glob semantics that correctly match `spec_v1.md`, `spec_v13.md`, etc. relative to project root, and **does not require any hook**. The `ask` rule force-prompts on every matching call.

### A2: `ask` rules pre-empt the auto-mode classifier short-circuit

Per [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions):

> Rules are evaluated in order: **deny -> ask -> allow**. The first matching rule wins, so deny rules always take precedence.

And from DEC-008 Q2 finding (corroborated by current docs):

> Actions matching `deny` / `ask` / `allow` rules resolve immediately (rules short-circuit classifier)

Critically, the `ask` rule applies *in addition to* auto mode's classifier check — the classifier doesn't get to "approve" past an `ask` rule. This means a downstream user running auto mode (the FB-026/DEC-008 case) still gets prompted before any Edit to `.claude/spec_v*.md`. This is the load-bearing property that makes Option C work without breaking auto-mode users' flow.

### A3: PreToolUse hooks add rich decision control on top of permission rules

Per [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks):

The hook input includes `tool_name`, full `tool_input` (e.g., `file_path` for Edit), `cwd`, `permission_mode`, and `session_id`. The hook can return:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "..."
  }
}
```

A hook could implement custom logic — e.g., "deny Edit on spec files unless `tool_input.old_string` is shorter than N characters" — that permission rules alone can't express. But for FB-007's concern, the simple `ask` permission rule covers the case without custom logic.

### A4: Hook + rule interaction (key safety property)

> Hook decisions do not bypass permission rules. Deny and ask rules are evaluated regardless of what a PreToolUse hook returns, so a matching deny rule blocks the call and a matching ask rule still prompts even when the hook returned `"allow"` or `"ask"`. This preserves the deny-first precedence described in [Manage permissions](#manage-permissions), including deny rules set in managed settings.

This means: if Option C uses the *permission rule* approach (no hook), it can't be silently disabled by a hook misconfiguration. If Option C uses a *hook* approach, the rule layer is still independent. Either way, the safety property is durable.

### A5: Bypass conditions to be aware of

- **`bypassPermissions` mode** (per the official docs): "skips all permission prompts, including writes to `.git`, `.claude`, `.vscode`, `.idea`, and `.husky`." So `ask` rules are skipped under `bypassPermissions`. But: `bypassPermissions` is documented as "Only use this mode in isolated environments like containers or VMs where Claude Code cannot cause damage." A user in this mode has explicitly opted out of safety; this is not a vulnerability in Option C, it's a user choice.
- **Managed-settings deny override:** managed settings (org-deployed) can set `allowManagedPermissionRulesOnly: true` which would discard user/project `ask` rules. Template-side rules wouldn't apply in that environment. Negligible concern for the template's target audience.

### A6: Implementation cost comparison

| Implementation path | Cost | Where it lands |
|---|---|---|
| `permissions.ask` rule with `Edit(.claude/spec_v*.md)` | 2 lines of JSON | `.claude/settings.json` (template-owned per DEC-005) |
| `permissions.ask` rule covering Edit + Write + spec + decisions + vision | ~6 lines of JSON | `.claude/settings.json` |
| Custom PreToolUse hook script (e.g., shell + jq) | ~20-40 lines + script file + permission to invoke | `.claude/settings.local.json` hooks section + `.claude/hooks/` dir |

The simplest viable Option C is the pure permission-rule approach. A hook is only needed if the rule needs to do something fancier than "prompt always" — e.g., deny + show a custom message + emit telemetry. For FB-007's stated goal (intercept and prompt), the rule alone is sufficient.

### Verdict for Q3

**Option C is technically straightforward** — the simplest implementation is 2-6 lines of JSON added to `.claude/settings.json` (template-owned per DEC-005), no custom script required. This *materially changes the cost calculus* for the decision: Option C's "permission-layer change" framing in the decision record overstates the implementation complexity. The `permissions.ask` mechanism is the same primitive DEC-005/DEC-008 already use for `permissions.allow`; the only new thing is using `ask` instead of `allow` for a path-glob.

**Reframing for the decision record:** Option C is more accurately characterized as "shipping an `ask` rule in the template-owned settings.json" — analogous to DEC-005's "shipping an `allow` rule," not analogous to "writing a custom hook script." This drops the implementation-complexity criterion from "medium-high" to "low" in the comparison table.

A hook layer would still be available as an Option C-prime if extra logic is desired (e.g., suppress the prompt when an environment variable signals an `/iterate` flow) — but the baseline doesn't require it.

---

## Q4 Research: Blast radius of Option C

### How many legitimate spec edits per project per month would the gate intercept?

The template's design intent (per `rules/spec-workflow.md`) is:
- Spec changes go through `/iterate` (propose-approve-apply pattern)
- Direct edits are "always safe" because drift detection reconciles them
- `/iterate` itself writes the spec at its apply stage

Under that design, the **expected** spec-write profile is:
1. `/iterate apply` Edits/Writes to `.claude/spec_v{N}.md` at version bump or amendment time
2. Occasional direct edits by Claude when a small drift sweep is desired (the contested pattern)
3. User direct edits (typing in their editor, not via Claude) — these don't go through Claude Code's permission layer at all

For category (1): `/iterate apply` invocations. Typical project cadence: 1-3 per month per active project (based on template-maintenance observation; FB-007 mentions the styler's `spec_v13` indicating 13 iterations in a multi-month project).

For category (2): the contested pattern. The whole point of Option C is to gate this. Frequency unknown — observed at least once (C-01 in styler).

For category (3): not relevant — local-only editor changes don't trigger the hook.

### Net legitimate-prompt frequency under Option C

Assuming `/iterate apply` issues 5-15 Edits per amendment (small spec drift fix vs full version bump), and 1-3 amendments per month: **5-45 prompts/month per active project from legitimate `/iterate apply` flow**.

This is the blast radius cost — it's not zero. Each `/iterate apply` invocation that previously ran headlessly now incurs an `ask` prompt per Edit. For a 15-Edit amendment, that's 15 user clicks.

### Mitigation: the `/iterate apply` exemption (see Q7)

Two viable shapes:

**Shape A — explicit user override per session.** User running `/iterate apply` is told upfront: "this will Edit the spec N times; allow all? [yes/no]." After "yes," subsequent Edits in the same session-block proceed without additional prompts. This is the existing "Yes, don't ask again" UX that Claude Code already supports for repeated Bash commands; the question is whether it works for Edit.

Per the official docs: "Yes, don't ask again" behavior for File modification is "**Until session end**" (vs Bash's "Permanently per project directory and command"). So Edit rule approval persists for the session only — naturally resetting between `/iterate` invocations. This is good safety behavior.

**Shape B — `acceptEdits` mode toggle inside `/iterate apply`.** The `/iterate apply` flow could explicitly use `acceptEdits` mode for its duration. This is a Claude Code permission-mode change (per [permission-modes](https://code.claude.com/docs/en/permission-modes)) — auto-accepts edits in the working directory. But: `acceptEdits` doesn't bypass `ask` rules (only `allow` rules pre-approve; `ask` still prompts). Per the docs: `acceptEdits` auto-approves edits to paths "in the working directory or `additionalDirectories`" — but `ask` rules still take precedence. So this doesn't actually fix the blast radius.

**Shape C — slash-command-aware hook (sophisticated).** A PreToolUse hook reads `transcript_path`, parses last few entries, detects "user just typed `/iterate apply`" → returns `permissionDecision: allow`. Fragile (transcript parsing is unstandardized), but it's the only platform mechanism that gives provenance-based exemption. Not recommended without strong need.

### Recommended mitigation

**For the v1 ship, Shape A (session-bounded "Yes don't ask again") is sufficient.** The user opens `/iterate apply`, sees the first prompt, clicks "Yes, don't ask again for this session," and proceeds. Cost per `/iterate apply`: 1 extra click at the start. Total monthly blast radius for legitimate flows: 1-3 extra clicks per project. Acceptable.

### Other potential spurious-fire sites

- **`/work decomposition`** — does it write to the spec? Per `rules/spec-workflow.md`: tasks follow the spec, not the other way around. `/work decomposition` reads the spec and writes task JSONs, not spec edits. No spurious-fire here.
- **`/health-check` Part 5 sync** — does the sync ever touch `.claude/spec_v*.md`? Per `sync-manifest.json` (referenced in extension-hooks.md), `spec_v{N}.md` is in `ignore` category — sync doesn't touch it. No spurious-fire here.
- **`/feedback review` promotion** — could write to spec only via `/iterate` (per the documented routing). No direct spec write outside `/iterate`. No spurious-fire here.
- **Audit `[Fix it]`** — DEC-013 HARD RULE auto-classifies spec-touching findings as `kind: decision` → no inline write. No spurious-fire here.

So the *only* legitimate spec-write path is `/iterate apply`, and the blast radius is bounded to that single command. This is much narrower than the decision record's "blast radius beyond originating concern: large" estimate — corrects the criterion's score.

### Verdict for Q4

**Blast radius is narrow and easily mitigable.** Only `/iterate apply` legitimately writes the spec, and session-bounded "Yes don't ask again" reduces the per-amendment cost to 1 extra click. The decision record's "large" blast-radius score in the criterion table should be revised downward — closer to "small" given the existing exemption mechanism. The criterion should be reframed as "blast radius of legitimate flows: small (one extra click per `/iterate apply` session)" rather than "every spec edit."

---

## Q5 Research: Composite (Option D) — necessary or redundant?

### What each layer catches

Reference DEC-013's three-layer HARD RULE enforcement (synthesizer step 5 + post-synth sanity check + action-table gate). Per DEC-013 Q1 analysis, each layer caught different failure modes:
- Synthesizer step 5 caught misclassification at *creation* time (the synthesizer might propose `bundle-eligible` for a spec-touching change).
- Post-synth sanity check caught the same at *validation* time (independent recheck against the same paths).
- Action-table gate caught it at *execution* time (when the user clicks `[Fix it]`, the action layer refuses if `kind == decision`).

These three layers caught *the same class of error* (misclassified spec-touching finding) at *three different lifecycle stages*. Defense-in-depth.

### Applied to Option D (Option A + Option C)

**What Option A catches that Option C doesn't:** the *intent* signal. Reading "audit-sourced edits MUST route through /iterate" before Claude tries an Edit gives Claude the right behavior *before* the permission layer fires. This means in normal flow there's no prompt at all — Claude reads the rule, doesn't try the Edit, and instead drafts an `/iterate` proposal. The user experience is "Claude did the right thing on its own" rather than "Claude tried, got prompted, then backed off."

**What Option C catches that Option A doesn't:** the *rationalization* failure. When Claude reads "the audit's evidence is partially stale, the residual is just 5 trivial noun-renames, I should just sweep them inline" (the observed C-01 reasoning), the rule is being weighed against the rationalization. Sometimes the rationalization wins. Option C's `ask` rule doesn't care about the rationalization — the Edit just prompts.

**What neither catches:** parallel-session edit collisions (DEC-013 Q5), transitive-consumer breakage (DEC-013 Q3), and other failure modes outside the FB-007 concern. Option D doesn't address these and doesn't pretend to.

### The cost of belt-and-suspenders

- **Rule layer (Option A):** trivial wording change in `spec-workflow.md`. Cost: ~3-5 lines of new prose. Friction added to Claude's behavior: zero (rule changes are read-once-per-session via memory).
- **Permission layer (Option C):** 2-6 lines of JSON. Friction added: 1 prompt per `/iterate apply` session (mitigable via "Yes don't ask again").
- **Combined (Option D):** sum of above. No new friction (the rule doesn't add prompts; the permission doesn't add prose).

**Belt-and-suspenders for free.** Unlike DEC-013's three-layer enforcement which had real implementation cost per layer (each was its own code change), Option D's two layers are cheap individually and don't compound their costs.

### When the composite would be redundant

If Option A's rule clarification is **structurally complete and Claude reliably reads and applies it**, then Option C never fires and is redundant. The C-01 observation contradicts the precondition — Claude is *not* reliably applying the existing rule contract (specifically the audit-routing context). The existence of FB-007 is itself evidence that the rule-only approach has a known failure mode.

### Verdict for Q5

**Option D is the recommended composite — it is not redundant.** Each layer catches a failure mode the other doesn't:
- A catches "Claude's intent should reflect the workflow contract" (preventive — Claude doesn't try the Edit in the first place)
- C catches "Claude's intent was overridden by rationalization" (corrective — the Edit prompts, user catches it)

The total implementation cost is small (rule clarification + ~6 lines of JSON), the total friction is small (~1 click per `/iterate apply` session), and the combined coverage is materially stronger than either alone. **Option D is strictly better than Option A or Option C in isolation** for the FB-007 concern.

The DEC-013 precedent (three-layer HARD RULE) is the comparable: layered enforcement is a recurring pattern for spec/decision/vision protection, and FB-007 is asking for exactly that pattern to extend to Claude's general behavior.

---

## Q6 Research: Symmetric extension to decision records and vision documents?

### What DEC-013 already protects

The audit-system HARD RULE covers ALL of:
- `.claude/spec_v*.md`
- `.claude/support/decisions/decision-*.md`
- `.claude/vision/**/*.md`

…via the same logic (auto-classify as `kind: decision` if `files_to_touch` includes any of these paths). Per `audit-coherence.md:397`, all three paths trigger the same routing.

### FB-007's framing scopes only to spec

The captured concern in FB-007 mentions `.claude/spec_v*.md` exclusively. The originating C-01 incident was a `spec_v13.md` edit. The verbatim "Possible directions" list also only mentions spec files.

### Why the asymmetry?

The asymmetry is likely accidental — FB-007 captured what was *observed* (spec edits), not what was *at risk* (any of the three categories). The structural reasons for protecting spec also apply to decisions and vision:

- **Decisions** are the authoritative record for "why we built X this way." A direct edit to a decision file outside `/research` workflow (which decisions don't have a formal flow for, but the propose-approve pattern would handle them) breaks the same audit-trail property. DEC-013 already enforces this via the audit-system layer; FB-007's symmetric extension would close the broader behavioral surface.
- **Vision documents** are pre-spec ideation inputs. They're less load-bearing than spec/decisions but still flagged for protection by DEC-013. Editing them in-place mid-project mutates the historical record of project genesis.

### Cost of symmetric extension

- **For Option A (rule):** add to the wording: "spec, decision, and vision file edits MUST route through `/iterate`" (or analogous flow per category — `/research` for decisions, ideation tools for vision). Cost: zero additional lines beyond the rule prose.
- **For Option C (permission rule):** add path globs:
  ```json
  "ask": [
    "Edit(.claude/spec_v*.md)",
    "Edit(.claude/support/decisions/decision-*.md)",
    "Edit(.claude/vision/**/*.md)",
    "Write(.claude/spec_v*.md)",
    "Write(.claude/support/decisions/decision-*.md)",
    "Write(.claude/vision/**/*.md)"
  ]
  ```
  Cost: ~4 additional lines. Blast radius extension is the same kind (legitimate-flow exemption needed for `/research` if it writes decisions directly; `/iterate distill` if it writes vision).

### What about decision record updates by research-agent?

This is a real spurious-fire site. The research-agent (this very agent) writes to `.claude/support/decisions/decision-*.md` as part of its workflow — populating `Research Findings`, `Options Comparison`, updating frontmatter status from `draft` to `proposed`. If Option C extends to decisions, **every research-agent invocation prompts**.

For the template repo specifically, decisions live at `decisions/` (root) not `.claude/support/decisions/`. The permission rule applies to `<cwd>/.claude/support/decisions/...` — the template repo's research-agent writes wouldn't match. But downstream projects' research-agents would.

Mitigations:
1. Use the same session-bounded "Yes don't ask again" UX as Q4 — research-agent's first decision-write prompts, subsequent writes in same session don't.
2. Or scope the permission rule narrowly: `Edit(.claude/support/decisions/decision-*.md)` for hand-edits only, knowing the research-agent writes through `/research`'s session. Same exemption shape as `/iterate apply`.

### Vision documents

Vision docs aren't currently written by any template-shipped command — they're user-pasted from outside Claude Code (per `rules/spec-workflow.md`: "Brainstorm in Claude Desktop (or any tool); Save the result to `.claude/vision/`"). So Option C's vision-path entries would intercept nothing in the auto-generated case. They only fire if Claude tries to *edit* an existing vision doc — which is the exact bypass surface FB-007 worries about.

### Verdict for Q6

**Recommend symmetric extension to decisions and vision.** Costs are marginal (4 extra path globs in Option C; trivial prose extension in Option A). DEC-013's audit-system layer already enforces this symmetry, so the broader behavioral layer should match for consistency. The research-agent's decision-writing flow is the one notable exemption — handled by the same session-bounded UX that handles `/iterate apply`'s spec-writing flow.

**Asymmetric alternative (less recommended):** ship Option C for spec only; document that decisions and vision are covered by DEC-013 from the audit-system side; revisit if behavioral bypasses on decision/vision files surface. This is the minimum-blast-radius path but leaves a known structural gap.

---

## Q7 Research: Interaction with `/iterate`'s own edits (exemption mechanism)

This was largely answered in Q4. Recap:

### Available exemption mechanisms

1. **Session-bounded "Yes don't ask again"** (default Claude Code behavior for Edit rule approvals). User clicks once per `/iterate apply` invocation; subsequent Edits in same session proceed without prompts. Reset on next session start. **This is the recommended approach** — it uses platform-native UX with no template-side complexity.

2. **`acceptEdits` mode toggle inside `/iterate apply`.** Documented in [permission-modes](https://code.claude.com/docs/en/permission-modes). But per Q3 finding A2, `ask` rules pre-empt `acceptEdits` — so this doesn't actually exempt the Edit calls. Not viable as written.

3. **Custom PreToolUse hook with slash-command-source detection.** Hook reads `transcript_path`, looks for recent user messages, detects `/iterate apply` invocation, returns `permissionDecision: allow`. Fragile and not recommended without strong need.

4. **Disable the `ask` rule conditionally via environment variable.** A hook reads an env var (e.g., `CLAUDE_ITERATE_APPLY_IN_PROGRESS=1`) set by `/iterate apply` and bypasses. Requires hook + command-side env coordination. Moderate complexity.

5. **Allow-list `/iterate`'s session as a whole.** Not a platform mechanism — there's no per-command session in the harness. Not viable.

### Recommended exemption

**Use the session-bounded "Yes don't ask again" UX.** Costs: 1 click per `/iterate apply` invocation. Benefits: no custom hook, no env-var coordination, leverages platform-native UX.

If the user finds the per-session click too friction-y after Option C ships, mechanism 4 (env-var-gated hook) is the natural upgrade path. Document this in `setup-checklist.md` as an optional refinement, not a v1 requirement.

### Documentation surface

`/iterate apply` documentation should mention: "If you have `permissions.ask` rules on spec files (per DEC-016), the first Edit in this session will prompt. Click 'Yes, don't ask again' to proceed; subsequent edits will go through without prompts until session end." This sets user expectations and prevents confusion at first encounter.

### Verdict for Q7

**`/iterate`'s own edits exempt via session-bounded "Yes don't ask again" — no custom hook needed.** The platform UX already supports the pattern. Document the expectation in `/iterate apply` setup notes and in setup-checklist. No template-side coordination required.

---

## Q8 Research: Failure mode severity if guardrail fails

### Drift detection's role

Per `rules/spec-workflow.md`: "Direct edits to the spec are always safe — the decomposed snapshot preserves the before-state, and drift detection handles reconciliation." Per `.claude/support/reference/drift-reconciliation.md` (referenced from spec-workflow.md): section_fingerprint hashes drive drift detection. The decomposed snapshot at `previous_specifications/spec_v{N}_decomposed.md` is the "what tasks were derived from" snapshot.

**What drift detection catches:** changes to spec sections that have already been decomposed into tasks — these flag for reconciliation at next `/iterate` or `/work` invocation.

**What drift detection misses:**
1. Changes to sections that weren't yet decomposed (e.g., new sections added before any task derived from them).
2. Whitespace / formatting changes that don't alter section_fingerprint but alter human reading.
3. Sub-section reorderings where overall content matches but ordering changes meaning.
4. Changes that hit-and-revert (the C-01 pattern — net state unchanged, fingerprint unchanged, drift detection sees nothing).

### Severity calibration

**Class A — Corruption (state diverges semantically without detection).** Drift detection's fingerprint-based approach catches gross changes but not subtle semantic shifts. Example: editing a spec section to flip "should" to "must" — same fingerprint if word count is preserved (depends on hash specifics, but typical hashes don't preserve word-level semantics). The audit-trail property is also lost — there's no `/iterate` proposal record explaining why "should" → "must" happened.

**Class B — Workflow infraction (state ends up correct, but audit trail is missing).** The C-01 scenario: 5 Edits forward + 5 Edits backward, net state unchanged. Fingerprint identical. Drift detection sees nothing. The audit trail (which would have shown an `/iterate` proposal explaining the cleanup) is absent. Future Claude reading just `spec_v13.md` sees no record of the cleanup intent.

**Class C — Pure cosmetic infraction.** Edit-then-revert where the edits were meant to be cosmetic anyway. Negligible.

### Worst-case severity under each option

- **Option A fails (Claude rationalizes past the rule):** Class B incident (workflow infraction, state OK). Severity: low — no semantic harm; cost is "audit trail incomplete." This is precisely what C-01 was.
- **Option C fails (hook misfires or user clicks through carelessly):** Class B or A depending on the user click. If user clicks "yes, apply" without reviewing, could escalate to Class A. Severity: low to medium.
- **Option D fails (both A's rule and C's rule are bypassed):** would require both Claude ignoring its rule reading AND user clicking through `ask` prompts without review. Highly unlikely simultaneous failure. Severity: residual.

### Comparison to consequences of not having the guardrail

The C-01 incident was Class B (no harm beyond audit trail). If guardrails were absent and a similar incident occurred with Class A semantics (semantic flip rather than noun-rename), the worst case is **subtle spec drift that survives until next audit cycle**, by which point the original intent may be unrecoverable. Cost to recover: significant — would require git archaeology, deciphering what change happened when, and reconstructing intent without an `/iterate` proposal artifact.

### Verdict for Q8

**The guardrail prevents a class of *workflow infractions* primarily, with secondary protection against *low-grade corruption* (Class B with risk of escalating to Class A).** The severity is low-to-medium per incident, but the recurrence cost compounds because each Class B incident degrades the audit trail's reliability — over time, "I can find why this section changed via /iterate proposals" stops being trustworthy.

The complexity worth-it question for the decision: Option C is *cheap* (2-6 lines of JSON, 1 click per `/iterate apply`) and Option A is *free* (rule wording). Even at low per-incident severity, the cumulative audit-trail erosion + the marginal implementation cost both point to "ship the guardrail."

**Option D combines both at near-zero combined cost.** The complexity-to-value ratio is favorable.

---

## Discarded Approaches

### "Ship a deny rule instead of ask"

A `permissions.deny` on `Edit(.claude/spec_v*.md)` would hard-block all direct edits, including `/iterate apply`'s own writes. The deny precedence is absolute — even Claude itself reading "use /iterate" can't issue the Edit. This requires extensive exemption machinery (per-session escalation, env-var-gated overrides) to be workable. Rejected because `ask` rule with session-bounded "Yes don't ask again" achieves the safety property at materially lower complexity.

### "Move the spec file to a path outside `.claude/` to avoid the rule"

Wouldn't help — the path is part of the template's spec-workflow contract and changing it is a much larger structural decision. Rejected immediately.

### "Use a sandbox mode to restrict spec file edits OS-level"

[Sandboxing](https://code.claude.com/docs/en/sandboxing) provides OS-level enforcement, but: (a) it applies to Bash subprocesses, not Edit tool calls directly — Edit goes through Claude Code's own permission system, not the sandbox; (b) it's much heavier-weight than needed for this concern. Rejected as overkill.

### "Add the rule to `.claude/CLAUDE.md` Critical Invariants section"

The Critical Invariants section already has "Exactly one `spec_v{N}.md` exists in `.claude/` at any time." Adding "Spec edits must route through `/iterate`" to this section would be redundant with Option A's rule clarification in `spec-workflow.md` — better to keep the workflow rule in the dedicated rule file. Note: a one-line cross-reference in CLAUDE.md pointing to the new rule would be appropriate but isn't its own option.

---

## Cross-cutting Considerations

### Interaction with DEC-005 / DEC-008 (template settings model)

DEC-005 established the two-file split: `.claude/settings.json` is template-owned (base `permissions.allow` only); `.claude/settings.local.json` is user-owned (hooks, env, theme, additional permissions). DEC-008 narrowed the allow list.

**Question:** does shipping `permissions.ask` rules in `.claude/settings.json` (template-owned) conflict with DEC-005's scope ("permissions.allow only")?

DEC-005's framing was *which permissions to ship*, not *which permission kinds are allowed in the template file*. The two-file split rationale (template owns its file; user owns their additions) doesn't intrinsically restrict `ask` rules from the template file — and shipping `ask` rules is semantically aligned with shipping `allow` rules (both are template-set policy; user can override in local).

**However:** DEC-005's `.claude/CLAUDE.md` Critical Invariants line says "`.claude/settings.json` is template-owned (base `permissions.allow` only)." If Option C adds `permissions.ask`, this invariant line needs updating.

**Recommendation:** update the Critical Invariants language to "`.claude/settings.json` is template-owned (base `permissions.allow` AND `permissions.ask` only)" — clarifies that both kinds of template-set rules live in the same file. This is a minor wording change in `.claude/CLAUDE.md`, not a structural DEC-005 reversal.

### Interaction with DEC-008 (auto-mode permissions reevaluation)

DEC-008 confirmed that `permissions.allow` rules short-circuit the auto-mode classifier. The same is true for `permissions.ask` — `ask` rules are evaluated before the classifier runs, per the decision order (deny → ask → allow → classifier). So Option C remains effective under auto mode.

This is important because: a downstream user running auto mode (the FB-026/DEC-008 case) might assume "auto mode will handle this" — but `ask` rules pre-empt auto mode. The behavior is: even in auto mode, Edit calls on `.claude/spec_v*.md` prompt the user. Documented expectation needs to match.

### Interaction with cross-project capture protocol

`rules/agents.md § Cross-Project Capture Protocol` flags scenarios where a session in a downstream project might inadvertently modify template-owned files. Option C's `ask` rule on `.claude/spec_v*.md` is *also* a guardrail against accidentally editing the *template's own* `.claude/spec_v1.md` placeholder during template-side sessions. So the protection applies bidirectionally (template-side maintenance and downstream-project usage).

### Sync category placement

The rule ships in `.claude/settings.json` which is already in `sync-manifest.json`'s `sync` category (per DEC-005). No category change needed.

---

## Sources

**Anthropic official docs (Claude Code):**
- Permission system, rule syntax, modes, mode interactions: https://code.claude.com/docs/en/permissions
- PreToolUse hooks, JSON input shape, decision control, hook + rule interaction: https://code.claude.com/docs/en/hooks
- Permission modes (default / acceptEdits / plan / auto / dontAsk / bypassPermissions): https://code.claude.com/docs/en/permission-modes
- Sandboxing (OS-level enforcement comparison): https://code.claude.com/docs/en/sandboxing

**Anthropic API SDK (parallel docs):**
- Hooks reference (API SDK): https://platform.claude.com/docs/en/agent-sdk/hooks

**Internal template precedent:**
- DEC-005 (base allowedTools shipping policy — Option E layered model): `decisions/decision-005-base-allowedtools-shipping-policy.md`
- DEC-008 (auto-mode reevaluation — narrowed allowlist, classifier short-circuit): `decisions/decision-008-auto-mode-permissions-reevaluation.md`
- DEC-013 (audit-fix-it autonomy boundary — HARD RULE three-layer enforcement, the inline-apply surface): `decisions/decision-013-audit-fix-it-autonomy-boundary.md`
- FB-007 (originating capture): `.claude/support/feedback/feedback.md` § FB-007
- `rules/spec-workflow.md` (rule in tension — "direct edits are safe"): `.claude/rules/spec-workflow.md`
- `commands/audit-coherence.md` (HARD RULE FIRST at synthesizer step 5, lines 396-407): `.claude/commands/audit-coherence.md`
- Extension hooks reference: `.claude/support/reference/extension-hooks.md`

**Third-party deep-dives (corroborating):**
- Hooks practical guides (search results): smartscope.blog, datacamp.com, claudefa.st, aiproductivity.ai, systemprompt.io, pixelmojo.io, ksred.com, felo.ai, stevekinney.com

---

## Recommendation Summary

See the Recommendation section in the decision record itself. Short version:

**Option D (Composite — A + C) is the recommended choice.** Q3 revealed that Option C's implementation is materially simpler than initially framed (2-6 lines of JSON in template-owned `settings.json`, no custom hook needed). Q4 revealed the blast radius is narrow (only `/iterate apply` legitimately writes spec; session-bounded "Yes don't ask again" handles it). Q5 confirmed that A + C are not redundant — each catches a failure mode the other doesn't (A is preventive via Claude's rule reading; C is corrective via permission-layer prompt). Q1 confirmed that A alone is insufficient because provenance is not platform-trackable and the rule-only approach failed in C-01. Q2 confirmed that B's size-threshold is not defensible — recommend B be discarded. Q6 recommends symmetric extension to decisions and vision (DEC-013 already enforces this on the audit-system side; broader behavioral symmetry matters). Q7 confirmed `/iterate apply` exemption is handled by platform-native session-bounded UX. Q8 confirmed the failure-mode severity is low-to-medium per incident but compounds through audit-trail erosion.

**Confidence: High.** The platform mechanisms (gitignore-glob in Edit path-rules, ask-rule pre-emption of classifier, session-bounded "Yes don't ask again") are well-documented in current Claude Code docs and corroborated by DEC-005/DEC-008 internal precedent. The cost calculation favors Option D unambiguously.

**Alternative if user prefers minimum-change path:** Option A alone — rule clarification only, no permission-layer change. Acknowledged limitation: depends on Claude reliably reading the rule (the precondition that failed in C-01). Acceptable if FB-007 is treated as a "clarify the rule first; ship structural enforcement only if behavioral recurrence happens."

**Reject:** Option B (size-based carveout) — no defensible N; duplicates DEC-013's kind-based axis with a less-precise mechanism. Discard.
