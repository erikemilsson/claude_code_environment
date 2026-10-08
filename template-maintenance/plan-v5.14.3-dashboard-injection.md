# v5.14.3: dashboard HTML injection through project-owned state (FB-127 ai)

**Status:** built, reviewed, release bookkeeping done; awaiting the user's OK to commit, tag and push.

## Measured (2026-10-09, v5.14.2, read-only)

- `-->` or `--!>` in `version.json` `template_version`, or `-->` in spec frontmatter `status:`, closes the META comment: markup after it lands raw in `<head>` (reproduced in scratch projects, with a control render that kept the block whole).
- A line break in `template_version` adds a second `task_hash:` line to the META block.
- `_mdi` turns `[x](javascript:…)`, `data:`, `VBScript:` and a leading-space `javascript:` into live `href`s, in Notes and in `augment_rows` text.
- Fuzz of 68 free-form state fields with an HTML marker: 26 reached the page, all escaped; 42 did not render in that fixture (not a full audit). The inline script is a constant; `style=` values are computed.
- 9 downstream projects: 40 sidecar links (39 relative, 1 `https`); every `template_version` and spec `status` is a plain word. Old and new renderer output is byte-identical on all nine (`--now` fixed, shasum compared; hashes differ per project, so the renders were not empty).

## Build contract

1. `_meta_value()`: every free-form META value (`spec_version`, `spec_status`, `spec_fingerprint`, `template_version`) has line breaks and control characters (`\x00-\x1f`, `\x7f`, `\x85`, U+2028, U+2029) collapsed to one space and `&`, `<`, `>` written as entities. Ordinary values are unchanged.
2. `_md_link()`: a markdown link becomes `<a>` only for a relative target, a `#` anchor, or `http` / `https` / `mailto`. The scheme is read with ASCII whitespace and control characters removed and entities decoded. Any other scheme renders as plain `label (target)`.
3. Tests: `TestStateCannotInjectMarkup` (9 tests). Against the v5.14.2 renderer, 6 of the first 8 fail and the 2 that pin unchanged behaviour pass; the 9th (entity-spelled colon) was added after and pins behaviour that was already safe.
4. `dashboard-regeneration.md`: one sentence on the link rule in the `user_notes` row.

## Decisions (user, 2026-10-09)

1. Built directly by the main session, then one independent read-only reviewer (no mirrors).
2. `file:` links are not allowed.
3. Ships as v5.14.3, followed by the 9-project sync.

## Amendments

1. Two test expectations were wrong as first written: `javascript&#58;x` and `javascript&colon;x` are escaped before the link is built, so the browser reads a literal `&#58;`, not a colon. They stay relative links; a separate test pins that.

2. Review (one independent read-only pass: 45 link targets, 144 seeded fields, 19 mutants, no browser run): no blocker. Added after it, not seen by the reviewer: a spec-file-name test, a control-character assertion, two doc sentences (the rule covers a decision's selected-option text; META values are one line with entities).
3. User decision 4 (2026-10-09, from the review): a target starting with two slashes or backslashes (`//host`, `\\host`, `/\host`) is refused; `/absolute` paths stay links. `//example.com/x` is no longer a link. Mutant (rule disabled) fails 6 subtests.

## Accepted, not fixed

- `tel:`, editor schemes and Windows drive paths print as text.
- A value such as `5 verification_debt: 99` puts a second field name on the same META line; only a reader that doesn't anchor on line start is fooled.
- Bold or code markup inside a link target garbles the `href` (older behaviour, no quote breakout).

## Results

- 456 tests pass on Python 3.13.15 and 3.10.20 (445 before); renderer tests 153 → 164.
