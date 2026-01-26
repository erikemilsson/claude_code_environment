# Specification Creator

Versioned specification system. The active spec is the source of truth for the project.

## Quick Start

1. Navigate to this folder: `cd .claude/specification_creator`
2. Start Claude Code from here
3. Run `/iterate` to begin structured spec review

## Commands

| Command | Purpose |
|---------|---------|
| `/iterate` | Auto-detect weakest area, ask questions, suggest content |
| `/iterate overview` | Focus on Overview section |
| `/iterate architecture` | Focus on Architecture section |
| `/iterate requirements` | Focus on Requirements section |
| `/iterate acceptance` | Focus on Acceptance Criteria |
| `/iterate questions` | Focus on Open Questions |
| `/iterate {topic}` | Focus on custom topic |

## How /iterate Works

```
┌─────────────────────────────────────────────────────────┐
│  1. Check spec against readiness checklist              │
│  2. Identify focus area (yours or weakest)              │
│  3. Ask up to 4 questions                               │
│  4. You answer                                          │
│  5. Claude suggests copy-pasteable content              │
│  6. You edit the spec                                   │
│  7. Repeat until ready                                  │
└─────────────────────────────────────────────────────────┘
```

**Key rule:** Claude suggests, you edit. Claude never modifies the spec directly.

## Spec Readiness

Before moving to `/work` (task decomposition), specs must be "Minimally Ready":

| Section | Minimum Criteria |
|---------|-----------------|
| Overview | Problem statement, target users, 2+ problems/solutions |
| Architecture | Components named, relationships clear, 1+ design decision |
| Requirements | 3+ functional, 1+ non-functional, constraints listed |
| Acceptance Criteria | 5+ testable criteria, pass/fail verifiable |
| Open Questions | No blockers for core architecture/critical path |

See `reference/spec-checklist.md` for full criteria.

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
    ├── commands/
    │   └── iterate.md           # /iterate command definition
    ├── reference/
    │   └── spec-checklist.md    # Readiness criteria
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
4. Run `/iterate` to begin building `../spec_v1.md`

### Building the Specification

1. Run `/iterate` - Claude checks the spec and identifies gaps
2. Answer Claude's questions (max 4 at a time)
3. Review suggested content
4. Edit the spec yourself
5. Run `/iterate` again to continue
6. Repeat until checklist passes

### Updating (Minor Changes)

1. Edit the active `../spec_v{N}.md` directly
2. Update the `updated` date in frontmatter

### Versioning (Major Changes)

1. Copy `../spec_v{N}.md` to `../support/previous_specifications/`
2. In the copied file: change `status: active` to `status: archived`
3. Create new `../spec_v{N+1}.md` with `status: active`
4. Set `created` and `updated` to today's date

### When to Version

- Architecture changes
- Major feature additions/removals
- Changes that invalidate previous assumptions
- User explicitly requests a new version

## Archive

During spec creation, Claude may produce research notes or analysis. These go in `.archive/` with dated filenames:

```
.archive/
├── 2026-01-26_research-auth-options.md
├── 2026-01-26_scope-questions.md
└── 2026-01-27_architecture-notes.md
```

**Note:** This `.archive/` is for spec-session working documents. Formal decision records documenting technology/architecture choices go in `.claude/support/decisions/`.

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
