# Scenario 40: Handoff Schema Cap (bounded index, not a memoir)

Verify the handoff bounds shipped v4.21.1 (Plan 3 T4a): `.handoff.json` stays a bounded index (`session_knowledge` ≤ ~10 bullets; `recovery_action` ≤ ~3 sentences); overflow goes to a workspace file the handoff points at via `overflow_ref`. From v5.14.0 the whole file is also measured after each write (at most 2560 bytes), and the overflow file is named to the minute. From v5.14.1 the PreCompact hook holds its handoff to the same total, and the overflow file a handoff names is deleted when that handoff is consumed.

## Context

Observed failure mode (styler, 2026-06-10 analysis): a 7.8KB hand-curated free-prose handoff blob — write-expensive, read-unreliable, and a hiding place for blocking questions (the T3 queue contract, v4.14.0, moved those to dashboard rows; this cap bounds what remains).

## State (Base)

A long session ends with `/work pause`: one partial task (7), two unanswered user questions (already swept into sidecar `augment_rows[]`, rendered as Action Required rows, per the T3 contract), and ~18 distinct conversation insights worth preserving.

---

## Trace 40A: Rich session → bounded handoff + overflow file

- **Path:** `/work pause` (at 14:32 on 2026-10-07) → Path A → handoff write per `context-transitions.md § Schema` + `§ Bounds and Overflow`

### Expected

- `session_knowledge` written as an ARRAY of ≤ ~10 bullets (the most load-bearing of the 18), each ≤ ~25 words
- Excess insights land in `.claude/support/workspace/handoff-overflow-2026-10-07-1432.md`, organized by field name; `overflow_ref` set to that path
- `open_question_refs` holds POINTERS to the two Action Required rows — not the question text + discussion
- `recovery_action` ≤ ~3 sentences
- After the write, `wc -c < .claude/tasks/.handoff.json` prints 2310: within 2560, so the total check ends there

### Pass criteria

- [ ] Handoff is a bounded index; no field blows its cap
- [ ] The file was measured after the write, and the measured size is 2560 bytes or fewer
- [ ] Overflow file exists ONLY because content genuinely exceeded a bound
- [ ] Questions live in `augment_rows[]` (rendered as dashboard rows); handoff carries refs only

### Fail indicators

- A multi-KB `session_knowledge` prose blob (old shape)
- Insights silently dropped instead of overflowed
- `overflow_ref` null while bullets were truncated away
- An overflow file named by date only (`handoff-overflow-2026-10-07.md`)

## Trace 40B: Typical session fits — no overflow ceremony

- **Path:** same, but the session yields 4 insights and no open questions

### Expected

- `session_knowledge`: 4 bullets; `open_question_refs` absent or empty; `overflow_ref` null; NO overflow file created preemptively

### Pass criteria

- [ ] No workspace overflow file when everything fits
- [ ] Legacy string-form `session_knowledge` in an old handoff still parses on read (additive union, `partial_notes` precedent)

### Fail indicators

- Empty overflow file created "just in case"
- Reader rejecting an old string-form handoff

## Trace 40C: Every field within its cap, total over — the measurement triggers overflow

- **Path:** `/work pause` (at 16:05 on 2026-10-07, the same day as Trace 40A) → Path A step 5 → `context-transitions.md § Bounds and Overflow`, Total check

### Scenario

The session yields exactly 10 `session_knowledge` bullets of 22–25 words each (about 1.6KB), one partial task whose `partial_notes` is 6 sentences (about 620 bytes), a 3-sentence `recovery_action`, a 2-sentence `phase_context` and two `open_question_refs` pointers. No field exceeds its cap, so the per-field overflow procedure has nothing to do and `overflow_ref` is null after the first write.

### Expected

1. The handoff is written. `wc -c < .claude/tasks/.handoff.json` prints 3040: over 2560.
2. The longest field is `session_knowledge`. Its three least load-bearing bullets move to `.claude/support/workspace/handoff-overflow-2026-10-07-1605.md` under a `session_knowledge` heading; seven stay inline; `overflow_ref` is set to that path; the handoff is rewritten.
3. Second measurement: 2590. Still over.
4. The longest remaining field is `active_work[0].partial_notes`. Its last three sentences move to the same overflow file under `partial_notes`; the handoff is rewritten.
5. Third measurement: 2290. Done.
6. `handoff-overflow-2026-10-07-1432.md` from the earlier pause is untouched.

### Pass criteria

- [ ] The file is measured after the write even though no field exceeded its cap
- [ ] Content moves out largest field first, and the file is measured again after each rewrite, until it is 2560 bytes or fewer
- [ ] Everything moved out is in the overflow file under its field's name; `overflow_ref` points at it
- [ ] `open_question_refs`, the task id and `ready_for_verify` in `active_work`, and the required fields are unchanged
- [ ] The overflow file's name carries the minute, so the day's two pauses have two files

### Fail indicators

- A 3040-byte handoff left as written because every field was within its cap (the pre-v5.14.0 behaviour)
- Bullets deleted to get under the total, with no overflow file
- `open_question_refs` shortened or dropped to save bytes
- The second pause writing over, or appending to, the first pause's overflow file
- The size estimated from the field lengths with no `wc -c` on the written file

## Trace 40D: The PreCompact hook's handoff is held to the same total

- **Path:** auto-compaction → `.claude/hooks/pre-compact-handoff.sh` → `context-transitions.md § "Path B: PreCompact Hook"`, step 3

### Scenario

No handoff exists. Tasks 7, 9 and 11 are "In Progress" with `notes` of 1400, 900 and 2000 characters; Task 12 is "In Progress" with a 40-character note; Task 13 is "Awaiting Verification". Compaction fires the hook.

### Expected

1. The hook builds the handoff with a 600-character head for Tasks 7, 9 and 11 and measures the serialized result: over 2560 bytes.
2. It sets `truncated: true` and lowers one common length over the notes heads to the largest that fits: the three long heads end up the same length, each ending in `…`; Task 12's 40-character note is unchanged.
3. The written file is 2560 bytes or fewer and valid JSON. All five `active_work` entries are there, whole apart from the shortened notes heads; there is no `overflow_ref` and no overflow file.
4. The task files are unchanged: the full notes are still in them.

Variant, it fits: one "In Progress" task with a 2000-character note. The handoff carries the 600-character head, has no `truncated` key, and is byte-for-byte what the hook wrote before v5.14.1.

Variant, a long title: one task's title is 5000 characters. After the notes heads, the hook cuts that title (titles over 60 characters, down to no less than 60) and the file fits; `position.recently_completed` is untouched and the entry keeps all its fields.

Variant, many finished today: 600 tasks were finished today and one is "In Progress". The notes head goes first, then `recently_completed` is shortened to the ids that fit. The In Progress entry is still there with its title.

Variant, many tasks: 12 tasks are in flight. With notes heads, titles and `recently_completed` cut the file is still over, so every `active_work` entry is reduced to its `task_id` and `ready_for_verify`, and then all 12 titles fit back in. With 25 tasks and long titles, only the first entries of `active_work` get a title back, cut to 60 characters. All ids are there either way. The next `/work` Step 0a says in its summary that the hook cut the handoff.

Variant, still over: 60 tasks are in flight. Ids and flags alone are over 2560 bytes. The hook writes the handoff as it is: valid JSON, `truncated: true`, 60 entries, over the bound.

Variant, a handoff exists: the user ran `/work pause` earlier. The hook exits without writing; the richer handoff and its `overflow_ref` are untouched.

### Pass criteria

- [ ] The hook's handoff is 2560 bytes or fewer in every shape but the last variant
- [ ] `truncated: true` appears only when something was cut; a handoff of exactly 2560 bytes is not cut
- [ ] Longer heads are cut before shorter ones; a short note survives whole
- [ ] The order is notes heads, overlong titles, `recently_completed`, remaining titles, then entries reduced to id and flag with titles put back from the front while they fit
- [ ] Every In Progress and Awaiting Verification task id is in `active_work` in every variant
- [ ] The hook exits 0 and never rewrites an existing handoff or a task file

### Fail indicators

- A 3KB hook handoff written as-is (the pre-v5.14.1 behaviour)
- Every head cut to nothing when shortening the three long ones was enough
- An `active_work` entry dropped to make the file fit, with or without a count of what was dropped
- Step 0a rejecting a reduced entry as "missing required fields" and deleting the handoff
- Nine tasks in flight written as bare ids with half the bound unused
- The hook writing an overflow file, or cutting a `/work pause` handoff down to size
- `scripts/tests/test_pre_compact_hook.py` failing

## Trace 40E: The overflow file goes when its handoff is consumed

- **Path:** new session → `/work` Step 0a (`commands/work.md`) → `context-transitions.md § "Restoration"`, step 6

### Scenario

The handoff from Trace 40C is on disk: `overflow_ref` is `.claude/support/workspace/handoff-overflow-2026-10-07-1605.md`. `handoff-overflow-2026-10-07-1432.md` from the earlier pause is also in the workspace; no handoff names it. The next morning the user runs `/work`.

### Expected

1. Step 0a reads the handoff, presents the summary and loads `session_knowledge`. `overflow_ref` is non-null, so it reads the overflow file now, before anything is deleted.
2. The handoff is consumed and deleted. The file `overflow_ref` names is under `.claude/support/workspace/` and matches `handoff-overflow-*.md`, so it is deleted with it.
3. `handoff-overflow-2026-10-07-1432.md` is left: this handoff doesn't name it.

Variant, concurrent session: the handoff's active task has changed status since the handoff's timestamp, so the handoff is preserved (FB-104). Its overflow file is kept too.

Variant, a stale handoff: the user comes back nine days later. The handoff is over 7 days old: it is shown as reference only, not used for routing, and deleted. `handoff-overflow-2026-10-07-1605.md` is deleted with it, unread; the 14:32 file is left.

Variant, a path that doesn't qualify: a hand-edited handoff has `overflow_ref: "docs/notes.md"`. The handoff is consumed and deleted; `docs/notes.md` is not touched.

### Pass criteria

- [ ] After consumption neither `.handoff.json` nor `handoff-overflow-2026-10-07-1605.md` exists
- [ ] A file is deleted only when the consumed handoff's `overflow_ref` names it, it is under `.claude/support/workspace/`, and its name matches `handoff-overflow-*.md`
- [ ] A preserved handoff keeps its overflow file
- [ ] The overflow file is read before it is deleted, except with a stale handoff
- [ ] A stale handoff takes its overflow file with it

### Fail indicators

- The overflow file left behind after its handoff is deleted (the pre-v5.14.1 behaviour: five such files had collected downstream)
- Every `handoff-overflow-*.md` in the workspace deleted by pattern, the 14:32 file included
- `docs/notes.md` deleted because the handoff named it
- The overflow file of a consumed handoff deleted without being read
- A stale handoff deleted and its overflow file left behind
- The overflow file of a preserved concurrent-session handoff deleted
