# Feedback Log

Items are captured via `/feedback` and triaged via `/feedback review`.

---

## FB-003: Promote `feature-retirement.md` from Styler to template (generally-useful workflow rule)

**Status:** new
**Captured:** 2026-05-15
**Source:** discovered as a Styler-local rule file during investigation of `/health-check` Part 5 sync friction (template-maintenance FB-059 + FB-060). Originally captured at `template-maintenance/feedback.md` as FB-061; relocated here to match the FB-002 cross-project capture precedent (small, additive, ready for `/feedback review` triage).

**Observation:** Styler has a project-local rule file at `.claude/rules/feature-retirement.md` that codifies a generally-useful workflow: how to retire a feature in a frozen, restorable state. The workflow shape:
- Snapshot lives at the retirement commit (no orphaned state)
- Spec keeps a "Retired (YYYY-MM-DD)" marker (discoverability for future readers)
- Directory convention (`.claude/support/retired/{slug}/manifest.json`) enables mechanical restoration

This is not fashion-domain-specific. Any project doing iterative feature work that occasionally retires surfaces (renamed routes, removed components, sunset features) could benefit. The workflow integrates cleanly with the template's existing patterns (spec-as-source-of-truth, decision records, audit family's `retired-features` lens which already greps for `.claude/support/retired/*/manifest.json`).

The audit family's `audit-coherence` lens for `retired-features` already assumes this file structure exists — it scans `.claude/support/retired/*/manifest.json` and flags retired features missing spec markers. Without the workflow rule shipped in the template, downstream projects would hit the lens but have no guidance on the convention. So promoting `feature-retirement.md` makes the audit lens more legible.

**Counterpart not promoted:** Styler's `brand-mention-provenance.md` (when Claude can name brands vs substitute attributes per DEC-060) is fashion/retail-domain-specific. Stays Styler-only.

**Proposed action (small ship):**
1. Copy `styler/.claude/rules/feature-retirement.md` to `claude_code_environment/.claude/rules/feature-retirement.md`. Edit lightly to remove Styler-specific language (e.g., FB-070 references → generic "feedback item") if any.
2. Add the file to `sync-manifest.json` (rules category).
3. Add the import to template's `.claude/CLAUDE.md` (workflow rules section) + summary row.
4. Update template's `.claude/commands/audit-coherence.md` lens-retired-features prompt to reference the workflow rule (improves the lens's "what counts as a finding" precision).
5. Bump template_version (minor — new feature: workflow rule shipped).

**Risk:** low. Pure additive — no breaking changes to existing template files. Downstream projects that don't use feature retirement see the rule but don't act on it.

**Dependencies:** none.

**Open question:** does the workflow rule depend on a specific `.claude/support/retired/` directory structure that Styler defined? Need to verify the manifest.json schema is template-shippable or whether it carries Styler-specific fields. If Styler-specific, document the abstract structure in the rule and let projects define their own manifest fields.

### Pointers for template-side `/feedback review`

- **Rule file source:** `/Users/erikemilsson/Developer/styler/.claude/rules/feature-retirement.md`
- **Audit family lens that consumes the convention:** `.claude/commands/audit-coherence.md` § "Lens 5 — `retired-features`"
- **Template-maintenance cross-link:** see `template-maintenance/feedback.md` § FB-061 for the relocation marker.

### Tags

rule-file-promotion, feature-retirement, audit-coherence, retired-features-lens, derived-from-styler

---

## FB-004: Promote "Audit Tasks: literal-ID comparison" rule from Styler to template (`task-management.md`)

**Status:** new
**Captured:** 2026-05-15
**Source:** discovered in styler-local addition to template-owned `.claude/rules/task-management.md` during ownership-boundary audit (counterpart to FB-003 feature-retirement promotion). Surfaces during cross-project capture session 2026-05-15.

**Dedup check (2026-05-15, performed in styler-side session):** searched all 4 template-side feedback locations (`.claude/support/feedback/feedback.md` + `archive.md`, `template-maintenance/feedback.md` — `template-maintenance/archive.md` does not exist). Adjacent items reviewed:

- **FB-033** (Spec-auditor subagent + PreToolUse gate) — adjacent but different. FB-033 is about a structural backstop that intercepts `Write`/`Edit` calls to `spec*.md` or `decisions/*.md` and blocks silent agent-inferred changes. This rule is about how implement-agents reason about audit-task descriptions that ask "is downstream task X still needed?" — instructing literal-ID comparison over semantic similarity. Different mechanism, different triggering site.
- **FB-058** (referenced in template-maintenance but no defining heading found at scan time) — concerns `/work` decomposition path validation, per FB-059 cross-reference at line 61. Different scope from audit-task ID comparison.
- **No other items** touch audit-task implementation rules, literal-ID vs semantic matching, or false-positive stale-task findings.

**If a future-Claude triaging this entry finds new items captured after 2026-05-15 that DO cover this rule, treat that as the canonical capture and close this entry as absorbed.**

**Observation:** Styler has a project-local addition to template-owned `.claude/rules/task-management.md` (a new `## Audit Tasks` section added at lines 32-43). The rule codifies implementer behavior for any audit task whose body asks "verify whether downstream task X is still needed" (pre-flight audits, phase-restoration audits, scope-staleness checks).

**The rule (verbatim from styler):**

> When a task description says "verify whether downstream task X is needed" or similar (pre-flight audits, phase-restoration audits, scope-staleness checks), the implementer must compare target IDs **literally** — not by count, semantic name, or shape similarity.
>
> Required behavior for any audit task with a downstream-needed question:
>
> 1. Read task X's body to extract the literal target IDs / values that X is supposed to produce or modify
> 2. Compare against current state **by ID**, not by count or semantic name match
> 3. Report `stale` / `no-op` only when the literal IDs match exactly
> 4. Report `scope_clarification_needed` when there's a semantic match without literal-ID match (e.g., "X adds field A but the registry already has field B with similar meaning") — do NOT report `stale`
>
> This rule exists because semantic name-matching is a recurring source of false-positive "stale" findings. Observed in a styler Phase 20 audit that reported "T429 will be a verify-only no-op" based on a name-shape match; T429's actual 7 target IDs were entirely distinct from the 10 already present, and the task was real work.

### Why template-worthy

The rule is **generic**: it applies to any project running pre-flight or scope-staleness audits as tasks. The styler Phase 20 example is illustrative, not load-bearing. Any project using the template's task-decomposition workflow can produce audit-shaped tasks (e.g., "verify whether T-X is still needed given changes in T-Y/T-Z") and will hit the same false-positive class if implementers compare semantically rather than by literal ID.

Symmetric with FB-003 (feature-retirement.md promotion) — same pattern: styler authored a generic rule locally; the rule belongs in the template so all forks inherit it; styler's project-owned files should not carry it after promotion.

### Proposed action (small ship; same shape as FB-003)

1. **Add the "Audit Tasks" section** to template's `.claude/rules/task-management.md` (currently at the version that lacks this section).
   - Suggested placement: between `## Parallel Execution` and `## References` (matches styler's structural placement).
   - Suggested edit at triage time: keep the styler-specific Phase 20 example as illustration ("Observed in a project's Phase N audit…" or "Observed in a Styler Phase 20 audit…" — whichever phrasing matches template's existing tone). The rule itself is generic; the example anchors it.
2. **Add to `sync-manifest.json`** if `task-management.md` isn't already covered there (likely is — it's a core rule file).
3. **No CLAUDE.md import changes** — the rule lives inside an already-imported rule file.
4. **Bump `template_version`** (minor — additive rule clarification within an existing file).
5. **After ship + sync:** styler's `.claude/rules/task-management.md` re-syncs cleanly with the template (the local addition becomes the template version; no styler-side conflict). Styler's "Audit Tasks" section can then come out of the project-owned `./CLAUDE.md` rule-imports block (it doesn't need to; it lives inside the template-owned rule file).

**Risk:** very low. Pure additive section to an existing rule file. Downstream projects that don't run audit-shaped tasks see the rule but don't trigger it.

**Dependencies:** none. Independent of FB-003 / FB-005 / FB-060 / FB-062. Can land in any order.

### Pointers for template-side `/feedback review`

- **Rule source (verbatim):** `/Users/erikemilsson/Developer/styler/.claude/rules/task-management.md` lines 32-43.
- **Concrete trigger case in styler:** Phase 20 audit that reported "T429 will be a verify-only no-op" based on a name-shape match. T429's 7 actual target IDs were entirely distinct from the 10 already present; the task was real work.
- **Sibling cross-project promotions in this batch:** FB-003 (`feature-retirement.md`), FB-005 (`MCP and Parallel Execution`). Style + tone should match across the trio.

### Out of scope for this feedback

- No changes to audit-coherence command (separate, FB-003 covers that lens).
- No new agent-contract changes — `implement-agent.md` continues to read the rules file as before; the new section is just additional guidance the agent picks up.
- No retroactive remediation of past false-positive audit findings in any project.
- This feedback does NOT carry the file change itself — it carries the proposal for template-side triage to authorize the change.

### Tags

rule-file-promotion, task-management, audit-tasks, literal-id-comparison, derived-from-styler

---

## FB-005: Promote "MCP and Parallel Execution" rule from Styler to template (`agents.md`)

**Status:** new
**Captured:** 2026-05-15
**Source:** discovered in styler-local addition to template-owned `.claude/rules/agents.md` during ownership-boundary audit (counterpart to FB-003 + FB-004). Surfaces during cross-project capture session 2026-05-15.

**Dedup check (2026-05-15, performed in styler-side session):** searched all 4 template-side feedback locations for any item touching MCP servers, Playwright MCP, parallel-subagent dispatch, or single-session resource sharing. Findings:

- **FB-001** (mcp-server-git stale `.git/index.lock`) — closed-out-of-scope per archive entry; about a specific MCP server's crash artifact at user-level config, not about parallel-batch dispatch routing. Not a duplicate.
- **No other items** touch MCP parallel execution, Playwright MCP fan-out, or single-session resource overlap. The `/work` Step 2c parallel-batch heuristic mentioned in this rule's "Detection" sub-section is not separately tracked by any current feedback item.

**If a future-Claude triaging this entry finds new items captured after 2026-05-15 that DO cover this rule, treat that as the canonical capture and close this entry as absorbed.**

**Observation:** Styler has a project-local addition to template-owned `.claude/rules/agents.md` (a new `## MCP and Parallel Execution` section added at lines 51-63). The rule documents an orchestrator pattern for handling parallel batches when one or more tasks rely on a single-session MCP server (Playwright MCP is the canonical example).

**The rule (verbatim from styler):**

> Single-session MCP servers cannot be safely fanned out across parallel subagents. Servers that expose stateful single-instance resources — Playwright MCP (one browser session), browser-automation MCPs, auth-session MCPs, connection-pooled MCPs — share their underlying state across all concurrent calls. Two parallel subagents calling the same MCP drive the **same** tab / session / connection; navigations, clicks, snapshots, and reads interleave silently. The failure mode is invisible — snapshots look fine but reflect another agent's mid-action state.
>
> **Orchestrator pattern when a parallel batch involves MCP-driving work:**
>
> 1. **Route MCP-driving work through one agent.** Dispatch a single agent to handle all calls to the shared MCP (e.g., one Playwright agent for all UI inspection across routes).
> 2. **Parallelize the rest.** Other agents in the same batch do code reads, greps, test runs — anything that doesn't touch the shared MCP server.
> 3. **For multi-route inspection.** Dispatch sequential agents with focused scopes ("audit /coloring", then "audit /wardrobe"), not a parallel batch driving the browser.
>
> True parallel browser inspection would require multiple MCP server instances on different ports or `user-data-dir`s — not how the template ships and not trivial to set up. Out of scope for most projects.
>
> **Detection (lower priority):** `/work` Step 2c parallel-batch heuristic currently keys on `files_affected` only. It could be extended to check `mcp_resource_overlap` (any pair of tasks both expected to use the same single-instance MCP server) — same dispatch site as `shared_contract` detection in `parallel-execution.md`. Tracked separately if it becomes a recurring foot-gun.

### Why template-worthy

The rule is **fully generic** — no styler-specific references in the body. Any project using the template + Playwright MCP (or any other single-session MCP) for parallel-batch work will hit the same silent-interleave failure mode. The orchestrator pattern (one MCP-routing agent + parallelize-the-rest) applies regardless of the project's domain.

The "Detection (lower priority)" sub-section explicitly references template-owned infrastructure (`/work` Step 2c parallel-batch heuristic + `parallel-execution.md`'s `shared_contract` detection) — it belongs in the template, not in any individual project.

Symmetric with FB-003 + FB-004 — same pattern: styler authored a generic rule locally; the rule belongs in the template; styler-side stays clean after promotion.

### Proposed action (small ship; same shape as FB-003 / FB-004)

1. **Add the "MCP and Parallel Execution" section** to template's `.claude/rules/agents.md`.
   - Suggested placement: between `## Behavioral Rules` and `## Tool Preferences` (matches styler's structural placement at lines 51-63, between the prior-kills rule and the dedicated-tools mapping).
   - **Tone audit at triage time:** the verbatim text is generic; should pass as-is.
2. **Add to `sync-manifest.json`** if `agents.md` isn't already covered (likely is — it's a core rule file).
3. **No CLAUDE.md import changes** — rule lives inside an already-imported rule file.
4. **Optional sub-edit:** if the template's `parallel-execution.md` (referenced in the rule's "Detection" sub-section) doesn't yet exist or doesn't carry `shared_contract` detection, the cross-reference becomes a forward-pointer rather than a current state. Triage decides whether to also create the linked content or leave it as a pointer.
5. **Bump `template_version`** (minor — additive rule).
6. **After ship + sync:** styler's `.claude/rules/agents.md` re-syncs cleanly with the template.

**Risk:** very low. Pure additive section. Downstream projects without Playwright MCP (or any single-session MCP) see the rule but don't trigger it.

**Dependencies:** none mandatory. The "Detection (lower priority)" sub-section's forward-reference to `parallel-execution.md`'s `shared_contract` detection is informational; if that detection exists in the template, the reference becomes load-bearing; if not, it remains a tracked future enhancement.

### Pointers for template-side `/feedback review`

- **Rule source (verbatim):** `/Users/erikemilsson/Developer/styler/.claude/rules/agents.md` lines 51-63.
- **Concrete trigger pattern in styler:** UI-audit tasks across multiple `/style` sub-routes (Suggest / Wardrobe / Coloring) using Playwright MCP. Parallelizing these fans onto the same browser session and interleaves snapshots invisibly.
- **Sibling cross-project promotions in this batch:** FB-003 (`feature-retirement.md`), FB-004 (`Audit Tasks` rule). Style + tone should match across the trio.

### Out of scope for this feedback

- No changes to `parallel-execution.md`'s `shared_contract` detection (separate; mentioned as forward-reference only).
- No new MCP server installation guidance — the rule operates on whatever MCP servers are configured at user level.
- No retroactive remediation of past parallel-batch dispatches that may have silently interleaved.
- This feedback does NOT carry the file change itself — it carries the proposal for template-side triage to authorize the change.

### Tags

rule-file-promotion, agents-rules, mcp, parallel-execution, playwright-mcp, single-session-resource, derived-from-styler

