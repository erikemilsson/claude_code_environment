# Specification Creator

Versioned specification system. The active spec is the source of truth for the project.

## Structure

```
.claude/
├── spec_v{N}.md                 # Active specification (source of truth)
├── support/
│   └── previous_specifications/ # Archived spec versions
│       └── spec_v{N-1}.md
└── specification_creator/       # Start Claude Code here for spec sessions
    ├── CLAUDE.md                # Rules for spec-building mode
    ├── README.md                # This file
    └── .archive/                # Research and planning docs
        └── YYYY-MM-DD_topic.md
```

## Specification Format

```yaml
---
version: {N}
status: active | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

## Workflow

### Starting a New Project

1. Copy Claude Code environment to your new project
2. Navigate to `.claude/specification_creator/`
3. Start a Claude Code instance from this folder
4. Work with Claude to build out `../spec_v1.md`

### Building the Specification

Claude will guide you through an iterative review process:

1. Claude reads the current spec
2. Claude identifies an area to discuss
3. Claude asks clarifying questions
4. You answer and discuss
5. Claude suggests specific changes
6. **You edit the spec manually**
7. Repeat for each section

**Important:** Claude suggests changes but does not edit the specification directly. You maintain full control over the spec content.

### What Claude Helps With

- Removing ambiguities
- Clarifying scope boundaries
- Finding inconsistencies
- Surfacing missing details
- Checking feasibility
- Asking questions you hadn't considered

### Archive

During spec creation, Claude may produce research notes, question logs, or planning documents. These go in `.archive/` with dated filenames:

```
.archive/
├── 2026-01-26_research-auth-options.md
├── 2026-01-26_scope-questions.md
└── 2026-01-27_architecture-notes.md
```

**Note:** This `.archive/` is for spec-session working documents. Formal decision records documenting technology/architecture choices should go in `.claude/support/decisions/` using the decision record format.

### Updating (minor changes)

1. Edit the active `../spec_v{N}.md` directly
2. Update the `updated` date in frontmatter

### Versioning (major changes)

1. Copy `../spec_v{N}.md` to `../support/previous_specifications/`
2. In the copied file: change `status: active` to `status: archived`
3. Create new `../spec_v{N+1}.md` with `status: active`
4. Set `created` and `updated` to today's date

### When to Version

- Architecture changes
- Major feature additions/removals
- Changes that invalidate previous assumptions
- User explicitly requests a new version

---

## For Claude Code Environment Builder

Add these instructions to the root CLAUDE.md when building environments:

```markdown
## Specification

The project specification lives at `.claude/spec_v{N}.md`.

**Do not edit the specification directly.** If you identify improvements:
1. Quote the relevant section
2. Explain the suggested change
3. Let the user make the edit

To create or revise specifications, start a Claude Code instance from `.claude/specification_creator/`.
```
