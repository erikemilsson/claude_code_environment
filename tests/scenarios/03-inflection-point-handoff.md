# Scenario 03: Inflection Point Decision Triggers Spec Revision

Verify that a resolved inflection point pauses `/work`, hands off to `/iterate` for spec revision, and that the `spec_revised` field controls the state transition.

## State

- Phase 1: 3 tasks, all "Finished"
- Phase 2: 3 tasks, Pending, `decision_dependencies: ["DEC-001"]`
- DEC-001: `status: approved`, `inflection_point: true`, `spec_revised`: absent, selected: "Multilevel Modeling"
- Spec still says "Apply appropriate statistical methods" (not yet updated)

## Trace: `/work` post-decision inflection point check
- DEC-001: `inflection_point: true` → check `spec_revised` → absent → pause

### Expected

```
Decision DEC-001 (Analysis Method) was an inflection point.
The outcome may change what needs to be built.
Run /iterate to review affected spec sections, then /work to continue.
```

- No Phase 2 tasks change status
- Spec not edited directly (suggest_only policy)

## Trace: `/iterate` inflection point re-entry
- Detection: `inflection_point: true`, `status: approved`, `spec_revised: NOT true` → match
- Focuses on affected sections (Phase 2 + potential Phase 1 impact)
- Suggests spec changes + suggests adding `spec_revised: true` to DEC-001 frontmatter

### Expected

- Questions specific to MLM (not generic "what method?")
- Cross-phase impact identified (Phase 1 data prep may need changes)
- Copy-pasteable spec content + instruction to set `spec_revised: true`

## Trace: `/work` after spec update and `spec_revised: true`

- DEC-001: `inflection_point: true`, `spec_revised: true` → proceed
- Spec drift detection triggers reconciliation → task updates

### Expected

- Phase 2 tasks unblocked
- Drift reconciliation suggests task updates reflecting MLM choice
- Dashboard updated with resolved decision and unblocked tasks

## Pass criteria

- [ ] `/work` pauses when `spec_revised` absent
- [ ] `/work` proceeds when `spec_revised: true`
- [ ] `/iterate` detects unrevised inflection point
- [ ] `/iterate` suggests `spec_revised: true` in output
- [ ] Questions are MLM-specific, not generic
- [ ] Cross-phase impact (Phase 1) identified
- [ ] Spec drift reconciliation updates tasks after spec change
- [ ] No direct spec edits (suggest_only)

## Fail indicators

- Phase 2 tasks unblocked without spec revision
- Spec edited directly
- Generic review instead of decision-focused
- `spec_revised` field ignored or not checked
