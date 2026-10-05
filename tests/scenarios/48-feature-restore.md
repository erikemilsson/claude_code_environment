# Scenario 48 — Restoring a retired feature (FB-134 a)

Conceptual trace test for v5.10.0. A restore undoes the **retirement commit** (the commit that added the feature's manifest) instead of cherry-picking `commit_sha`, which replays the wrong diff. A removal check confirms that commit actually removed the feature, a pin check compares its parent with `commit_sha`, and one of three routes restores the feature: revert, scoped inverse diff, or files only. Git never edits the spec in a restore: spec files are put back after a revert, and the marker comes out through `/iterate` (DEC-016). Every git behaviour traced below was reproduced in a throwaway repository.

Command path for every trace: `.claude/rules/feature-retirement.md § "Restore Path"` (removal check → pin check → route → snapshot line → gotchas), with `§ "Step 2 — Commit Pin"` and `.claude/support/retired/README.md § "manifest.json Schema"` for the fields.

## Setup / State

- A git project on `main`. The spec is `.claude/spec_v2.md`; each retired feature's section carries a `**Retired (2026-04-29)**` marker (Step 4).
- `legacy-checkout-flow` was retired in commit **R1**, whose parent **L1** is the manifest's `commit_sha`. R1:
  - deleted `src/app/checkout/page.tsx` and `src/lib/checkout/session.ts`;
  - cut the checkout registration from `src/app/routes.ts` and the `stripe-checkout` line from `package.json`;
  - added `.claude/support/retired/legacy-checkout-flow/` (manifest, `spec-excerpt.md`, mirrored copies of the two deleted files);
  - added the `## Checkout` marker to `.claude/spec_v2.md`;
  - set Task 41 (the retirement task) to Finished in `.claude/tasks/task-41.json`.
- The manifest's `affected_paths`: the two deleted files, `src/app/routes.ts`, `package.json`.
- A later commit **N1** added an unrelated route to `src/app/routes.ts` and edited `## Reports` in the spec.
- Sidecar `user_notes` holds a `**Retired Features:**` list with one entry per retired feature.
- Each trace states what differs.

## Trace A — route 1: one feature, one retirement commit

1. `RETIRE=$(git log --diff-filter=A --format=%H -1 -- .claude/support/retired/legacy-checkout-flow/manifest.json)` → R1.
2. Removal check: `git diff --name-status R1^ R1 -- <affected_paths>` prints `D` for both deleted files and `M` for `routes.ts` and `package.json`. The removals are in R1, so R1 stays the retirement commit.
3. Pin check: `git rev-parse R1^` = L1 = `commit_sha`. Nothing to report.
4. `git show --stat R1`: one manifest added; apart from the feature, only `task-41.json` → route 1.
5. `git checkout -b restore/legacy-checkout-flow && git revert --no-commit R1`. Staged result: both deleted files are back; the checkout registration is back in `routes.ts` and N1's route is still there; the `stripe-checkout` line is back; the snapshot directory is deleted. Two staged changes aren't the feature: `task-41.json` is back at its pre-retirement status, and the `## Checkout` marker is gone from `spec_v2.md` (R1 added it).
6. Both go back before committing: `git checkout HEAD -- .claude/tasks/task-41.json .claude/spec_v*.md`. Task 41 stays Finished, and the marker is back in the working tree; git has changed no spec file.
7. The snapshot directory is already gone, so the snapshot line needs no `git rm`.
8. The marker comes out of `## Checkout` through `/iterate`, a recorded spec edit (DEC-016).
9. Gotchas: `npm install` for the restored dependency; the `legacy-checkout-flow` entry is removed from `user_notes` and the dashboard regenerated; tests and build run.

**Variant A2 — the spec changed version since.** `/iterate` archived `spec_v2.md` to `.claude/support/previous_specifications/spec_v2.md` and created `spec_v3.md`, which still carries the marker. The revert follows the rename: it removes the marker from the archived copy and leaves `spec_v3.md` untouched. Step 6 therefore puts the archived copy back too (`git checkout HEAD -- .claude/spec_v*.md .claude/support/previous_specifications/`), and step 8 removes the marker from `spec_v3.md` through `/iterate`.

**Expected:** the feature is back as of L1, on top of everything committed since; the snapshot is gone; the restore commit changes no spec file, and the marker leaves the current spec through `/iterate`; task history is unchanged.

**Pass criteria:**
- [ ] `RETIRE` comes from the commit that added the manifest, not from `commit_sha`
- [ ] Route 1 is chosen because R1 retired only this feature
- [ ] The revert brings back the deleted files, the cut registration and the dependency line without losing N1's edits
- [ ] `task-41.json` and the spec file are put back before committing; the snapshot directory is gone
- [ ] The marker leaves the current spec through `/iterate`, never through the revert
- [ ] A2: the archived copy is put back too, and the marker leaves `spec_v3.md` through `/iterate`
- [ ] The Retired Features entry is removed from `user_notes`

**Fail indicators:** a `git cherry-pick` anywhere in the restore; the restore commit sets Task 41 back to its pre-retirement status; the restore commit changes a `spec_v*.md` or `previous_specifications/` file; the snapshot directory survives the restore (Lens 5 of `/audit-coherence` would then report a retired feature whose spec has no marker); A2 declared complete with the marker still in `spec_v3.md`.

## Trace B — route 2: one commit retired two features

State: commit **R2** retired `pdf-export-route` and `csv-export-route` together. It deleted `src/app/api/export/pdf/route.ts`, the PDF button's icon `public/export/pdf-icon.png` (a binary file) and `src/app/api/export/csv/route.ts`, cut both registrations from `src/app/routes.ts`, added both snapshot directories and both spec markers. `pdf-export-route`'s `affected_paths`: the PDF route, the icon and `src/app/routes.ts`, which the CSV manifest lists too. A later commit added a route at the end of `routes.ts`. The user wants PDF export back, not CSV export.

1. `RETIRE` from `pdf-export-route/manifest.json` → R2. The removal check shows `D .../pdf/route.ts`, `D public/export/pdf-icon.png` and `M src/app/routes.ts`; the pin check passes.
2. `git show --stat R2` lists two added manifests → route 2. A revert would bring CSV export back too.
3. `git checkout -b restore/pdf-export-route`, then `git diff --binary --no-ext-diff --no-color --src-prefix=a/ --dst-prefix=b/ R2 R2^ -- src/app/api/export/pdf/route.ts public/export/pdf-icon.png src/app/routes.ts | git apply --3way`. `pdf/route.ts` comes back, and so does the icon, byte-identical to `R2^`'s copy. `routes.ts` gets **both** registrations back, because the inverse diff is per file, and keeps the later route.
   The plain `git diff R2 R2^ -- <paths> | git apply --3way` fails here with `error: cannot apply binary patch to 'public/export/pdf-icon.png' without full index line`. `git apply` is all-or-nothing, so nothing comes back, not even the route file.
4. Per route 2, the CSV registration is deleted from `routes.ts` by hand.
5. `git rm -rq .claude/support/retired/pdf-export-route`; the `csv-export-route` snapshot stays.
6. Route 2 doesn't touch the spec, so the `## PDF export` marker is removed through `/iterate`. The PDF entry leaves `user_notes`.

**Variant B2 — the user's git config sets `diff.noprefix = true`, `diff.external` or `color.ui = always`.** Each one alone breaks the plain command even on text-only paths: `noprefix` drops the `a/`/`b/` prefixes, so `git apply` strips `src/` and finds no `app/routes.ts`; an external diff tool prints its own format with temporary file paths; colour codes leave `No valid patches in input`. The route 2 command's flags override all three, and step 3 restores the same files.

**Expected:** PDF export is restored, icon included. CSV export is still retired in every respect: its route file is absent, its registration is absent, and its snapshot, manifest, spec marker and Notes entry are all in place.

**Pass criteria:**
- [ ] Two manifests in `git show --stat R2` select route 2, not route 1
- [ ] The inverse diff is limited to this feature's `affected_paths`
- [ ] The inverse diff carries `--binary --no-ext-diff --no-color --src-prefix=a/ --dst-prefix=b/`, and the icon comes back byte-identical to `R2^`'s copy, with or without the B2 config
- [ ] The other feature's fragment in the shared file is removed by hand
- [ ] Only `pdf-export-route`'s snapshot directory is deleted

**Fail indicators:** `git revert R2`; the plain `git diff R2 R2^ … | git apply`, which rejects the whole patch on the binary icon; the CSV registration left in `routes.ts`; the `csv-export-route` snapshot or marker removed.

## Trace C — route 3: a partly retired shared file is merged, not overwritten

State: Trace A's state. The user wants the checkout files back without the rest of R1.

1. `RETIRE` = R1; the removal and pin checks pass as in Trace A.
2. `affected_paths` entries absent from the tree: `git checkout R1^ -- src/app/checkout/page.tsx src/lib/checkout/session.ts`.
3. `src/app/routes.ts` still exists, so it was partly retired. `git checkout R1^ -- src/app/routes.ts` would bring the registration back but drop N1's later route, and copying a snapshot copy over it would do the same. Instead, `git diff R1^ R1 -- src/app/routes.ts` shows the removed registration, and it is re-added by hand.
4. `package.json` also still exists: the `stripe-checkout` line is re-added by hand from `git diff R1^ R1 -- package.json`, then `npm install`.
5. `git rm -rq .claude/support/retired/legacy-checkout-flow`. Route 3 doesn't touch the spec, so the `## Checkout` marker is removed through `/iterate`. The Notes entry is removed.

**Variant C2 — no git history** (the project was imported with a squashed history): the two deleted files are copied back from the snapshot's mirrored paths. `routes.ts` still exists, so its registration is merged back by hand from `restore_notes` (or from a snapshot copy of `routes.ts`, if the snapshot holds one), never copied over.

**Expected:** the deleted files are back; `routes.ts` keeps N1's route and regains only the checkout registration.

**Pass criteria:**
- [ ] Only absent paths are checked out from `R1^` (or copied from the snapshot)
- [ ] Every path that still exists is merged by hand from the fragment diff
- [ ] N1's route survives in `routes.ts`

**Fail indicators:** `routes.ts` replaced by `R1^`'s or the snapshot's version; a `cp -r` of the whole snapshot tree.

## Trace D — a mis-pinned `commit_sha`

State: as Trace A, except that after committing R1 the retirer ran `git rev-parse HEAD` and wrote the result into the manifest in follow-up commit **F1**. So `commit_sha` = R1, the retirement commit itself.

1. `RETIRE` = R1: F1 only modified the manifest, so R1 is still the commit that added it. The removal check passes.
2. Pin check: `git rev-parse R1^` = L1, which differs from `commit_sha` (R1). The restorer says so ("`commit_sha` pins the retirement commit itself; using R1^ as the last-live state") and every route works from `R1^`.
3. Using the pin would fail: `git checkout R1 -- src/app/checkout/page.tsx` stops with `error: pathspec 'src/app/checkout/page.tsx' did not match any file(s) known to git`, because the file doesn't exist at R1. Route 3 checks out from `R1^` instead and the file comes back.
4. Route 1 never reads `commit_sha`, but F1 edited the manifest after R1, so `git revert --no-commit R1` stops with `CONFLICT (modify/delete)` on `manifest.json`; everything else is staged as in Trace A. The snapshot line resolves it: `git rm -rq .claude/support/retired/legacy-checkout-flow`. The task and spec files go back as in Trace A, then commit.

**Expected:** the mis-pin is reported and never used; the restore reads the last-live state from `R1^`.

**Pass criteria:**
- [ ] The pin check runs before any route and names the mismatch
- [ ] No file is checked out from `commit_sha`
- [ ] The manifest conflict is settled by deleting the snapshot directory

**Fail indicators:** files checked out from `commit_sha`; the conflict left unresolved; the manifest's pin "fixed" during the restore (pointless, since the restore deletes it).

## Trace E — why `git cherry-pick "$SHA"` is wrong

State: as Trace A. The old rule restored with `git cherry-pick "$SHA"`, where `$SHA` is `commit_sha` (L1).

1. A cherry-pick replays the diff L1 itself introduced (L1^ → L1). Suppose L1 bumped a README line: that change is already in history, so git reports `The previous cherry-pick is now empty` and nothing comes back.
2. Suppose instead L1 fixed a bug in `page.tsx`. The cherry-pick stops with `CONFLICT (modify/delete)` and leaves only L1's version of `page.tsx` in the tree. `session.ts`, the `routes.ts` registration and the `stripe-checkout` line stay gone.
3. The retirement's own change is R1 (L1 → R1). Only undoing R1 (routes 1 and 2) or checking out from `R1^` (route 3) brings the feature back.

**Expected:** neither the rule nor the README instructs a cherry-pick. The rule's one mention of it explains why not.

**Pass criteria:**
- [ ] `grep -in cherry` over `.claude/rules/feature-retirement.md` and `.claude/support/retired/README.md` finds exactly one line: the rule's "Don't cherry-pick `commit_sha`" sentence
- [ ] The README's `commit_sha` row says a restore checks out from the retirement commit's parent, which should equal it

## Trace F — the manifest landed apart from the removal

State: a third feature, `saved-carts`, was retired in two commits. **S1** added its snapshot and manifest while the feature was still live, and also bumped an unrelated dependency in `package.json`. The next commit, **R3**, deleted `src/app/carts/page.tsx`, cut its registration from `src/app/routes.ts`, and re-pinned `commit_sha` to S1 (= R3^). `affected_paths`: `src/app/carts/page.tsx`, `src/app/routes.ts`, `package.json`.

1. `git log --diff-filter=A ... saved-carts/manifest.json` → S1.
2. Removal check: `git diff --name-status S1^ S1 -- <affected_paths>` shows only `M package.json` (the unrelated bump); `page.tsx` isn't deleted there. The manifest landed apart from the removal.
3. `RETIRE=$(git log --diff-filter=D --format=%H -1 -- src/app/carts/page.tsx)` → R3, whose diff shows `D src/app/carts/page.tsx` and `M src/app/routes.ts`.
4. Pin check: `git rev-parse R3^` = S1 = `commit_sha`. Consistent.
5. R3 retired only this feature → route 1 on R3. The revert brings back `page.tsx` and the registration. The snapshot was added in S1, so it is still there, and the snapshot line deletes it.

**Expected:** S1 is never reverted: that would undo the unrelated dependency bump and only delete the snapshot, without restoring the feature.

**Pass criteria:**
- [ ] The removal check rejects S1 because it shows none of the feature's removals
- [ ] `RETIRE` becomes the commit that deleted the feature's files
- [ ] The snapshot directory is deleted after the revert

**Fail indicators:** `git revert S1`; the pin check run against S1 and "trust `S1^`" applied (S1^ is a live state too, so this hides the error until route 1 reverts the wrong commit).
