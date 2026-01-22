# CLAUDE.md

Instructions for Claude Code when working on the Todo API project.

## Project Overview

A REST API for managing todo items with user authentication.

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

## Technology Stack

- **Language**: Node.js / TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Auth**: JWT tokens
- **Testing**: Jest

## Conventions

### Code Style
- ESLint with Airbnb config
- Prettier for formatting
- camelCase for variables, PascalCase for types/classes

### File Structure
```
src/
├── controllers/    # Route handlers
├── services/       # Business logic
├── models/         # Database models
├── middleware/     # Express middleware
├── utils/          # Helper functions
└── routes/         # Route definitions
```

### Git
- Conventional commits (feat:, fix:, docs:, etc.)
- Feature branches off main
- Squash merge PRs

## Testing

```bash
npm test           # Run all tests
npm run test:watch # Watch mode
npm run test:cov   # With coverage
```

## Build & Run

```bash
npm install        # Install dependencies
npm run dev        # Development server
npm run build      # Production build
npm start          # Production server
```
