# CLAUDE.md

Instructions for Claude Code when working on the Kitchen Renovation project.

## Project Overview

Planning and managing a kitchen renovation project.

## Task Management

See `.claude/reference/shared-definitions.md` for:
- Difficulty scale (1-10) with breakdown rules
- Status values and their meanings
- Mandatory task workflow rules

**Key rule**: Break down tasks with difficulty >= 7 before starting.

## Commands

- `/complete-task {id}` - Start and finish tasks (includes work check)
- `/breakdown {id}` - Split complex tasks into subtasks
- `/sync-tasks` - Update task-overview.md from JSON files
- `/health-check` - Combined task system and CLAUDE.md health check
- `/archive-tasks` - Archive old finished tasks (for large projects)
- `/restore-task {id}` - Restore a task from archive
- `/generate-workflow-diagram` - Visual Claude/Human task diagram
- `/check-work` - Review session changes for issues and fix them

## Project Phases

1. **Planning**: Design, permits, contractor selection
2. **Demolition**: Remove existing fixtures
3. **Rough-in**: Plumbing, electrical, framing
4. **Installation**: Cabinets, counters, appliances
5. **Finishing**: Paint, trim, final touches

## Key Contacts

- General Contractor: [TBD]
- Electrician: [TBD]
- Plumber: [TBD]
- Cabinet supplier: [TBD]

## Budget

- Total budget: $45,000
- Contingency: 15% ($6,750)
- Spent to date: $0

## Important Notes

- Permit required before any structural work
- Lead time for custom cabinets is 6-8 weeks
- Need to book temporary kitchen setup during renovation
