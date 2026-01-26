# Workspace

Claude's working area for temporary and in-progress documents.

## Directories

- **scratch/** - Throwaway notes, quick analysis, temporary thinking
- **research/** - Web search results, reference material, gathered context
- **drafts/** - Work-in-progress documents before they move to their final location

## Rules

1. **Use this location** - Never create working documents in the project root
2. **Simple names** - Use descriptive filenames (`api-comparison.md`, not `task-5-research.md`)
3. **Promotion is manual** - When a draft becomes permanent, discuss where it should go
4. **Clean up periodically** - Delete scratch files when no longer needed

## What goes where

| Type | Location |
|------|----------|
| Quick notes while working | `scratch/` |
| Web search summaries | `research/` |
| API docs, reference material | `research/` |
| Design docs in progress | `drafts/` |
| Spec sections being drafted | `drafts/` |

## Graduation: Moving drafts to final locations

When a draft is ready to become permanent, move it to the appropriate location:

| Draft type | Destination |
|------------|-------------|
| Design docs | `.claude/context/` or project's docs folder |
| Spec sections | `.claude/spec_v{N}.md` (via spec revision process) |
| Decision research | `.claude/context/decisions/.archive/` |
| API documentation | Project's docs folder |
| Throwaway notes | Delete when done |

**Process:**
1. Discuss with human where the draft should go
2. Move/copy content to destination
3. Delete original from workspace

**Staleness:** Files in `workspace/` older than 30 days trigger a warning in `/health-check`.
