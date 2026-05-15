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
