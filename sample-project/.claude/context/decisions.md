# Architectural Decisions

## Decision Categories

Categories to track:
- **architecture**: System design, framework choices, patterns
- **data**: Storage approaches, data structures
- **testing**: Testing strategies and tools

## Decisions

### Decision 001: Web Framework Selection
- **ID**: decision-001
- **Date**: 2025-12-29
- **Category**: architecture
- **Status**: approved
- **Question**: Which web framework should we use for the REST API?
- **Chosen**: Express.js
- **Alternatives Considered**:
  - Fastify (rejected: less familiar, overkill for simple API)
  - Koa (rejected: smaller ecosystem)
  - Native Node.js HTTP (rejected: too low-level, more boilerplate)
- **Reasoning**: Express.js is mature, has excellent documentation, large ecosystem of middleware, and is the most widely used Node.js web framework. Perfect for a simple REST API.
- **Impacts**:
  - Affects phase-1 component-1-1 (server setup)
  - Affects phase-1 component-1-2 (route implementation)
- **Related Phases**: [phase-1]
- **Related Tasks**: [task-001, task-002]

### Decision 002: Data Storage Approach
- **ID**: decision-002
- **Date**: 2025-12-29
- **Category**: data
- **Status**: approved
- **Question**: How should we store todo items?
- **Chosen**: In-memory JavaScript array
- **Alternatives Considered**:
  - SQLite (rejected: adds complexity, not needed for demo)
  - PostgreSQL (rejected: requires external setup)
  - File-based JSON (rejected: I/O overhead for simple demo)
- **Reasoning**: For a simple demo API, in-memory storage is sufficient. It's fast, requires no setup, and clearly demonstrates API functionality without database complexity.
- **Impacts**:
  - Affects phase-1 component-1-3 (data store)
  - Data lost on server restart (acceptable for demo)
- **Related Phases**: [phase-1]
- **Related Tasks**: [task-003]

### Decision 003: Testing Framework
- **ID**: decision-003
- **Date**: 2025-12-29
- **Category**: testing
- **Status**: approved
- **Question**: Which testing framework should we use?
- **Chosen**: Jest
- **Alternatives Considered**:
  - Mocha + Chai (rejected: requires multiple packages)
  - Vitest (rejected: newer, less established)
- **Reasoning**: Jest provides everything needed out of the box - test runner, assertions, mocking, and coverage reporting. It's the most popular testing framework for Node.js.
- **Impacts**:
  - Affects phase-2 all components
  - Determines test file structure and syntax
- **Related Phases**: [phase-2]
- **Related Tasks**: [task-005]

## Decision Matrix
| ID | Category | Question | Chosen | Status | Impacts |
|----|----------|----------|--------|--------|---------|
| 001 | architecture | Web framework? | Express.js | approved | phase-1, task-001, task-002 |
| 002 | data | Storage approach? | In-memory array | approved | phase-1, task-003 |
| 003 | testing | Testing framework? | Jest | approved | phase-2, task-005 |

## Change Log
- 2025-12-29: Initial decisions defined for project setup