# Scenario 36: Audit-Family Core Delegation (v4.17.0)

Verify that `/audit-coherence` and `/audit-ui` execute their promote/fix/triage modes from `audit-family-core.md` with correct per-command substitutions, and that synthesizer dispatches splice the shared contract inline.

## Context

v4.17.0 extracted the duplicated promote/fix/triage algorithms and synthesizer classification rules into `support/reference/audit-family-core.md` (the two copies had already drifted — the bundle-eligibility criteria differed by the `transitive_consumer_risk` clause). Commands keep thin delegation sections with substitution rows; the synthesizer prompt carries a `{SPLICE HERE}` marker the orchestrator fills with the core's verbatim text at dispatch time. The failure modes guarded here: dangling substitutions, un-spliced markers reaching sub-agents, and divergence re-creeping into a command file.

## State (Base)

- Project with a completed `/audit-coherence` run at `.claude/support/audits/coherence-2026-06-10-1200/` (digest has 4 pending findings: 1 bundle-eligible, 1 fix-eligible, 2 decision)
- A completed `/audit-ui` run at `ui-2026-06-09-0900/` (3 pending findings, all decision kind)

---

## Trace 36A: Triage runs the canonical algorithm with coherence substitutions

- **Path:** `/audit-coherence triage` → core § "Triage mode (canonical)"

### Expected

- Orchestrator reads the core doc and executes its algorithm with `{AUDIT}: coherence`, `{P}: C`, `{DIR-GLOB}: coherence-*`, `{CMD}: /audit-coherence`
- `latest` resolves to `coherence-2026-06-10-1200`; walk header and empty-state messages render with "coherence", never a literal `{AUDIT}`
- Finding cards show `C-NN (kind)`; per-kind gates match the core table (`[F]ix it` only on the bundle-eligible item)
- Dispatched actions hit the canonical mechanics (Fix → core Fix mode steps 4-7; Promote → core Promote steps 3-9; Dismiss → audit-fix-workflow `[Dismiss]`)

### Pass criteria

- [ ] No literal placeholder (`{AUDIT}`, `{P}`, `{CMD}`, `{DIR-GLOB}`) appears in any user-facing output
- [ ] Action gates match the core's per-kind table exactly
- [ ] State mutations (digest status, sidecar dismissed_ids, friction cascade) follow the core's atomic-per-action spec

### Fail indicators

- The walker improvises steps not in the core algorithm (divergence re-creeping)
- `F` offered on a decision-kind finding
- Empty-state message hardcoded for the wrong audit ("No ui audit..." from the coherence command)

---

## Trace 36B: Synthesizer dispatch splices the shared contract inline

- **Path:** `/audit-coherence` (or `/audit-ui`) Phase 3 → synthesizer dispatch

### Expected

- Before dispatching, the orchestrator reads `audit-family-core.md` §§ "Synthesizer shared contract" + "digest.json schema (shipped canonical)" and replaces the prompt's `{SPLICE HERE}` marker with their verbatim text
- The dispatched sub-agent prompt contains the description constraints, the unified kind-classification rules (including `transitive_consumer_risk` on orphan removals — for BOTH audits now), and the full item schema inline — NO instruction telling the sub-agent to read a file
- The returned digest validates against the canonical schema; `audit`/`viewport` fields set per command

### Pass criteria

- [ ] `{SPLICE HERE}` never reaches the sub-agent
- [ ] UI-audit synthesizer applies `transitive_consumer_risk` on an orphan-component-deletion finding (previously coherence-only — the drift this ship killed)
- [ ] Items reference the shipped canonical schema, not `template-maintenance/audit-command-family-proposal.md` (which doesn't ship to projects)

### Fail indicators

- Sub-agent told "read audit-family-core.md" instead of receiving spliced text
- Classification rules differ between a coherence run and a ui run
- Digest items missing fields the canonical schema requires (e.g., `description`, `evidence_path`)

---

## Trace 36C: Promote single-finding subset stays consistent across both commands

- **Path:** `/audit-ui triage` → `P` on one finding · then `/audit-coherence promote latest --all`

### Expected

- Both promote paths execute the SAME core algorithm: next-FB computation, dedupe pass with `[S]/[U]/[M]/[N]`, FB-entry template (UI entry includes the Effort/Impact line; coherence entry omits it), digest + friction + findings.md cascades
- Source lines render `audit-ui-{ts} F-NN` and `audit-coherence-{ts} C-NN` respectively

### Pass criteria

- [ ] One FB-entry shape for both audits (modulo the documented UI-only line)
- [ ] Cascade updates identical in structure for both
- [ ] Dedupe pass runs in both (no shortcut on the single-finding path)

### Fail indicators

- The two commands produce differently-shaped FB entries
- Either path skips the dedupe pass or a cascade step
