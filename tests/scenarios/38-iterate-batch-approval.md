# Scenario 38: /iterate Batch Approval (single-response decision resolution)

Verify that the Step 4→5 gate (changed v4.20.0, Plan 3 T1) resolves the whole `[NEEDS APPROVAL]` table with ONE user response while keeping FB-032's "Decisions in This Proposal" structural contract fully intact — full enumeration, origin tags, proposed text.

## Context

Observed failure mode (2026-06-10 cross-repo analysis): the old gate required every `[NEEDS APPROVAL]` item resolved individually "even to `[Y] Apply all`" — a user choosing Apply-all still answered N prompts. Erik's corrections historically re-anchor *framing/scope*, so the fix compresses responses, never information: items stay fully enumerated with proposed text before the single response.

## State (Base)

- Spec `spec_v3.md` exists; `/iterate` Step 4 produced a change declaration with 3 changes
- `## Decisions in This Proposal` contains 4 unchecked `[NEEDS APPROVAL]` items numbered `N1`–`N4` (plus 1 `[USER REQUESTED]` and 2 `[FROM EXISTING SPEC]`, pre-checked)
- Each `N{n}` item carries its rationale; each related change shows proposed text

---

## Trace 38A: Bare [Y] resolves all items and applies — zero follow-up prompts

- **Path:** Step 4 declaration → user responds `Y` → Step 5 gate

### Expected

- All 4 `N{n}` items are checked `[x]` as approved-as-listed by that single response
- Changes apply immediately (archive-if-warranted → edit spec); NO per-item follow-up question is asked
- Apply report includes the resolved decision list

### Pass criteria

- [ ] Exactly 1 user response between declaration and apply
- [ ] All 4 items resolved as listed; gate passes with zero unchecked items
- [ ] Report lists what changed AND the resolved decisions

### Fail indicators

- Any "Now, about N2…" follow-up prompt after `[Y]`
- Items applied while still unchecked (gate skipped rather than batch-resolved)

---

## Trace 38B: Override response resolves named items, rest as listed

- **Path:** user responds `N2: use prose list, N4: defer to Phase 2`

### Expected

- N2 and N4 resolve per the overrides; N1 and N3 resolve as listed — all from the one response
- Proposed text affected by N2/N4 is revised; revised text shown in the apply report (full re-present only if an override materially alters other changes)
- Apply proceeds without additional prompts

### Pass criteria

- [ ] One response resolves all 4 items (2 overridden, 2 as-listed)
- [ ] Revised text for overridden items is visible to the user before/at apply
- [ ] An override naming a nonexistent item (e.g., `N9: …`) blocks apply and asks about that item only

### Fail indicators

- Unnamed items left unresolved (forcing follow-up prompts)
- Override applied silently without showing the revised text

---

## Trace 38C: [M] preserves the per-item walk; [P] postpones

- **Path:** user responds `M` (then, separately, a fresh run where user responds `P`)

### Expected

- `[M]`: each unchecked `N{n}` item presented one at a time for individual resolution, then apply — the pre-v4.20 guided pass, intact
- `[P]` (or `[N]`): nothing applied; proposal revisitable on the next `/iterate` run

### Pass criteria

- [ ] `[M]` walk asks about exactly the 4 unchecked items, in order, then applies
- [ ] `[P]` leaves the spec file untouched

### Fail indicators

- `[M]` re-litigating pre-checked `[USER REQUESTED]`/`[FROM EXISTING SPEC]` items
- `[P]` applying a subset (old "Partial" semantics leaking back)

---

## Trace 38D: Declaration content unchanged by batching (FB-032 contract)

- **Path:** Step 4 declaration output, any response mode

### Expected

- The `## Decisions in This Proposal` section still enumerates EVERY non-trivial choice with origin tags (`[NEEDS APPROVAL]` / `[FROM EXISTING SPEC]` / `[USER REQUESTED]`) and the changes still show proposed text — identical information content to the pre-batch format, plus `N{n}` numbering
- DEC-016 unchanged: the declaration is the audit trail of intent; `permissions.ask` still fires on the spec write

### Pass criteria

- [ ] No item dropped, summarized away, or collapsed to "and 3 more" to make batching feel lighter
- [ ] Origin tags and rationale present on every item
- [ ] FB-033 trial signal: this is a UX change (response compression), not a contract change

### Fail indicators

- Enumeration trimmed because "the user will just say Y anyway"
- Proposed text omitted from changes tied to `[NEEDS APPROVAL]` items
