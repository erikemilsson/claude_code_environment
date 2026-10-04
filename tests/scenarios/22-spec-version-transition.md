# Scenario 22: Spec Version Transition (v1 → v2)

Verify that `/iterate` correctly handles spec version transitions — archiving, creating the new version, and that `/work` properly migrates tasks to the new spec.

## Context

Version transitions happen at natural project boundaries: phase completion, inflection point resolution, or major scope changes. The transition must maintain the single-spec invariant (exactly one `spec_v{N}.md` at root), archive the old version, and ensure `/work` can reconcile existing tasks against the new spec. This is one of the most complex state transitions in the workflow.

## State (for 22A-22C)

- `spec_v1.md` is active (status: "active" in frontmatter)
- 10 tasks decomposed from v1: Tasks 1-5 (Phase 1, all Finished), Tasks 6-10 (Phase 2, all Pending)
- Phase 1 complete, Phase 2 about to begin
- User requests version transition: "Phase 1 is done, let's revise the spec for Phase 2 learnings"

---

## Trace 22A: `/iterate` version transition procedure

- **Path:** /iterate version transition

### Scenario

User runs `/iterate` and requests a version bump. `/iterate` executes the 5-step transition.

### Expected

1. **CONFIRM:** Claude asks: "Suggest creating spec v2. Reason: Phase 1 complete, incorporating learnings. Proceed? [Y/N]"
2. **ARCHIVE:** `spec_v1.md` copied to `.claude/support/previous_specifications/spec_v1.md`
3. **CREATE:** `spec_v1.md` copied to `spec_v2.md`, frontmatter updated:
   - `version: 2`
   - `status: draft` (new version starts as draft)
   - `updated: {today}`
4. **REMOVE:** `spec_v1.md` deleted (single-spec invariant maintained)
5. **REPORT:** Claude logs archive location, notes new spec is draft

### Pass criteria

- [ ] User confirmation required before any file operations
- [ ] Archive created BEFORE original deleted (no data loss window)
- [ ] Exactly one spec file exists after transition (`spec_v2.md`)
- [ ] New spec starts with `status: draft` (not carried over from v1's "active")
- [ ] Frontmatter version number bumped correctly
- [ ] Previous spec preserved verbatim in archive (no content changes)

### Fail indicators

- Original deleted before archive created
- Both `spec_v1.md` and `spec_v2.md` exist simultaneously after transition
- New spec inherits `status: active` from v1
- Transition proceeds without user confirmation
- Archive location wrong (not in `previous_specifications/`)

---

## Trace 22B: `/work` after version transition — task migration

- **Path:** /work spec discovery and task migration

### Scenario

User edited `spec_v2.md` (added Phase 2 detail, removed one Phase 2 section, modified another). User runs `/work`.

### Expected

1. `/work` discovers `spec_v2.md` (globs for `spec_v{N}.md`)
2. The drift check (`fingerprint.py --drift .claude`) sees every task on `spec_version` 1: Finished Tasks 1-5 count as `historical`, Pending Tasks 6-10 are listed as `unmigrated`
3. Version mismatch triggers task migration flow:
   - Finished tasks (1-5): provenance left unchanged (historical record; they were verified against v1), so the drift check keeps skipping them
   - Pending tasks mapped to unchanged sections: fingerprints updated
   - Pending tasks mapped to changed sections: `spec_version` updated, then flagged for reconciliation
   - Pending tasks mapped to removed sections: flagged for user decision (archive or reassign)
   - After migrating, `/work` re-runs `fingerprint.py --drift .claude`: the migrated tasks now name spec v2, so those in changed sections come back under `drifted` and reach the reconciliation prompt in this run, not the next
4. New sections in v2 without corresponding tasks: flagged as "needs decomposition"

### Pass criteria

- [ ] Spec version mismatch detected (tasks say v1, spec is v2)
- [ ] Finished tasks keep their v1 provenance (historical, not flagged by the drift check)
- [ ] Changed sections trigger per-task reconciliation in the same `/work` run (the drift check is re-run after migration)
- [ ] Removed sections don't silently orphan tasks
- [ ] New sections flagged for additional decomposition
- [ ] No tasks lost during migration

### Fail indicators

- All tasks re-decomposed from scratch (losing Finished status and history)
- Orphaned tasks (reference sections that no longer exist) silently ignored
- New spec sections not detected as needing decomposition
- Finished tasks re-opened for verification against new spec

---

## Trace 22C: Decomposed snapshot updated after migration

- **Path:** /work decomposition

### Scenario

After task migration (22B), `/work` needs a new decomposed snapshot for v2, so future reconciliation prompts can show what changed in v2.

### Expected

1. Old snapshot (`spec_v1_decomposed.md`) retained in `previous_specifications/`
2. If new tasks decomposed from v2's new sections: new snapshot created as `spec_v2_decomposed.md`
3. All migrated (unfinished) tasks now reference `spec_version: 2` with current fingerprints; Finished Tasks 1-5 stay on v1 as historical records
4. Future drift checks compare each migrated task's fingerprints with the current v2 sections; the v2 snapshot supplies the diffs shown at reconciliation

### Pass criteria

- [ ] Old decomposed snapshot preserved (not overwritten)
- [ ] New snapshot reflects v2 content
- [ ] Migrated task fingerprints align with v2 sections
- [ ] Drift detection baseline (migrated tasks' fingerprints) reset for v2

### Fail indicators

- Old snapshot overwritten (can't compare v1 → v2 changes later)
- No new snapshot created (reconciliation prompts can't show v2 diffs; detection itself still works)
- Some unfinished tasks still reference v1 fingerprints after migration

---

## Trace 22D: Version transition refused — when NOT to bump

- **Path:** /iterate version bump assessment

### Scenario

User asks to bump the version after making minor clarifications to the spec (typos, adding detail to existing sections). No phase transition, no inflection point, no scope change.

### Expected

1. `/iterate` evaluates the change scope
2. Recommends against version bump: "These changes are clarifications to existing sections. Suggest editing spec_v1.md directly — `/work` will handle drift reconciliation."
3. No version transition initiated
4. User can override if they insist

### Pass criteria

- [ ] Minor changes don't trigger version bump suggestion
- [ ] Claude explains why a bump isn't warranted
- [ ] Direct editing path recommended instead
- [ ] User can still force a bump if they want

### Fail indicators

- Every spec edit triggers a version bump
- No guidance on when versions are appropriate
- User unable to override Claude's recommendation
