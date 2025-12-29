# Decision Tracking Schema

This document defines the standard structure for tracking architectural and major project decisions.

## Purpose

Decision tracking provides:
- Historical context for why the project is structured a certain way
- Visibility into alternatives considered
- Impact analysis for changes
- Traceability between decisions, phases, and tasks

## Schema Structure

```yaml
# Architectural Decisions

## Decision Categories
[Defined during /init-specification]

Categories to track:
- [Category 1]: [Description of what decisions belong here]
- [Category 2]: [Description]

## Decisions

### Decision NNN: [Decision Title]
- **ID**: decision-NNN (unique identifier)
- **Date**: YYYY-MM-DD
- **Category**: [category-name]
- **Status**: proposed | approved | implemented | superseded
- **Question**: What problem does this decision address?
- **Chosen**: The selected approach (concise summary)
- **Alternatives Considered**:
  - Alternative 1 (rejected because...)
  - Alternative 2 (rejected because...)
- **Reasoning**: Why this approach was chosen over alternatives
- **Impacts**:
  - Affects [phase-N] [component-N-M]
  - Requires [task-XXX] to implement
  - Depends on [decision-YYY]
- **Related Phases**: [phase-N, phase-M]
- **Related Tasks**: [task-XXX, task-YYY]
- **Superseded By**: [decision-ZZZ] (if applicable)

## Decision Matrix
| ID | Category | Question | Chosen | Status | Impacts |
|----|----------|----------|--------|--------|---------|
| NNN | [cat] | ... | ... | [status] | [phases/tasks] |

## Change Log
- YYYY-MM-DD: [Description of change]
```

## Field Definitions

### ID
- **Format**: `decision-NNN` where NNN is a zero-padded number (001, 002, ..., 999)
- **Uniqueness**: Must be unique across all decisions
- **Usage**: Referenced in task JSON (`related_decisions` field) and phases.md
- **Immutability**: Never reuse IDs, even if decision is superseded

### Date
- **Format**: YYYY-MM-DD (ISO 8601)
- **Purpose**: When the decision was made (not when documented)
- **Usage**: Helps understand project timeline and decision sequencing

### Category
- **Custom**: Defined during `/init-specification`
- **Common Examples**:
  - `architecture`: System design, tech stack, patterns
  - `data`: Storage, schemas, migrations
  - `integration`: APIs, external services
  - `security`: Auth, encryption, compliance
  - `infrastructure`: Hosting, CI/CD, monitoring
- **Rules**: Only track major/architectural decisions, not minor implementation choices

### Status
- **Values**:
  - `proposed`: Decision under consideration, not yet finalized
  - `approved`: Decision finalized but not yet implemented
  - `implemented`: Decision has been put into practice
  - `superseded`: Decision replaced by another (link via `Superseded By`)
- **Flow**: `proposed → approved → implemented` OR `proposed → superseded`
- **Auto-Update**: Can automatically update status when related tasks complete

### Question
- **Format**: Clear question statement
- **Purpose**: Frames the problem that needed a decision
- **Examples**:
  - "How should we store user session data?"
  - "Which frontend framework should we use?"
  - "How do we handle database migrations in production?"

### Chosen
- **Format**: Concise summary (1-2 sentences)
- **Purpose**: Quick reference for the decision outcome
- **Example**: "Use PostgreSQL with Redis for session caching"

### Alternatives Considered
- **Format**: Bulleted list with rejection rationale
- **Purpose**: Shows due diligence and provides context
- **Example**:
  ```
  - MongoDB (rejected: ACID compliance needed for financial data)
  - DynamoDB (rejected: higher cost, vendor lock-in concerns)
  - MySQL (rejected: team has more PostgreSQL experience)
  ```

### Reasoning
- **Format**: Paragraph explaining the decision
- **Purpose**: Captures the "why" for future reference
- **Should Include**:
  - Key factors influencing the decision
  - Trade-offs accepted
  - Assumptions made
- **Example**:
  ```
  PostgreSQL provides ACID guarantees needed for financial transactions,
  has excellent JSON support for flexible schemas, and aligns with team
  expertise. Redis caching addresses session lookup performance concerns
  without sacrificing data consistency.
  ```

### Impacts
- **Format**: Bulleted list of concrete effects
- **Purpose**: Shows ripple effects of the decision
- **Types**:
  - Affects phases/components: "Impacts phase-1 component-1-2 design"
  - Requires tasks: "Requires task-025 to implement migration"
  - Dependencies: "Depends on decision-003 (API auth strategy)"
  - Blockers: "Blocks phase-2 until implemented"

### Related Phases
- **Format**: Array of phase IDs `[phase-1, phase-2]`
- **Purpose**: Links decision to project structure
- **Bidirectional**: Should match phases.md `Related Decisions` field

### Related Tasks
- **Format**: Array of task IDs `[task-025, task-026]`
- **Purpose**: Links decision to implementation work
- **Bidirectional**: Should match task JSON `related_decisions` field

### Superseded By
- **Format**: Single decision ID `decision-050`
- **Purpose**: Tracks when decisions are replaced
- **Usage**: Original decision status becomes `superseded`, new decision explains why

## Update Rules

### When to Create a Decision Entry

**DO create entries for:**
- Technology stack choices (languages, frameworks, databases)
- Architectural patterns (monolith vs microservices, REST vs GraphQL)
- Data modeling approaches (normalization, schema design)
- Security/auth strategies (OAuth, JWT, session-based)
- Integration methods (API design, message queues)
- Infrastructure choices (cloud provider, containerization)

**DON'T create entries for:**
- Variable naming conventions
- Code formatting preferences
- Minor refactoring choices
- Routine bug fixes
- Standard library selections

**Rule of Thumb**: If the decision affects multiple phases or components, track it.

### How to Update

#### Adding New Decision
1. Add entry to `.claude/context/decisions.md` with status `proposed`
2. Fill in all required fields
3. Run `/update-executive-summary`
4. Review and approve
5. Claude updates decision matrix and change log

#### Approving Proposed Decision
1. Change status from `proposed` to `approved`
2. Run `/update-executive-summary`
3. Claude can auto-approve status changes (not structural changes)

#### Implementing Decision
1. Create tasks for implementation
2. Link tasks to decision via `related_decisions` field
3. When all tasks complete, update status to `implemented`
4. Run `/update-executive-summary`

#### Superseding Decision
1. Create new decision entry explaining the change
2. In old decision, add `Superseded By: decision-XXX`
3. Change old decision status to `superseded`
4. Run `/update-executive-summary`

### Approval Required

**Requires explicit approval:**
- Adding new decision entry
- Changing categories (after initial setup)
- Superseding a decision

**Can be auto-updated:**
- Status changes (proposed → approved → implemented)
- Adding related tasks
- Adding related phases (if phase already references the decision)

## Examples

### Example 1: Database Selection Decision

```yaml
### Decision 001: Database Technology Selection
- **ID**: decision-001
- **Date**: 2025-12-15
- **Category**: architecture
- **Status**: implemented
- **Question**: Which database technology should we use for the staging and production layers?
- **Chosen**: PostgreSQL for both staging and production with Redis for caching
- **Alternatives Considered**:
  - MongoDB (rejected: ACID compliance required for financial transactions)
  - MySQL (rejected: team has more PostgreSQL experience, weaker JSON support)
  - DynamoDB (rejected: vendor lock-in concerns, higher cost at scale)
- **Reasoning**: PostgreSQL provides the ACID guarantees we need for financial data integrity, has excellent JSON support for our semi-structured data needs, and aligns with team expertise. Redis caching layer addresses read-heavy session lookup performance without sacrificing consistency. The combination gives us flexibility (JSON), reliability (ACID), and performance (Redis).
- **Impacts**:
  - Affects phase-1 component-1-4 (staging schema design)
  - Affects phase-2 component-2-1 (transformation logic must use PostgreSQL-specific features)
  - Requires task-001 (set up PostgreSQL instances)
  - Requires task-002 (design staging schema)
  - Requires task-015 (implement Redis caching layer)
  - Depends on decision-003 (cloud provider selection - affects database hosting)
- **Related Phases**: [phase-1, phase-2]
- **Related Tasks**: [task-001, task-002, task-015]
```

### Example 2: API Design Decision

```yaml
### Decision 005: API Architecture Pattern
- **ID**: decision-005
- **Date**: 2025-12-20
- **Category**: integration
- **Status**: approved
- **Question**: Should we use REST or GraphQL for the data serving API?
- **Chosen**: RESTful API with OpenAPI specification
- **Alternatives Considered**:
  - GraphQL (rejected: overkill for our simple query patterns, team unfamiliar)
  - gRPC (rejected: internal service only, no need for high-performance RPC)
- **Reasoning**: Our use case involves straightforward CRUD operations with predictable query patterns. REST provides simplicity, wide tooling support, and aligns with team experience. OpenAPI spec gives us automated documentation and client generation. GraphQL's flexibility isn't needed for our access patterns and would add complexity.
- **Impacts**:
  - Affects phase-3 component-3-1 (API service implementation)
  - Requires task-008 (design OpenAPI specification)
  - Requires task-009 (implement FastAPI service)
  - Depends on decision-002 (authentication strategy)
- **Related Phases**: [phase-3]
- **Related Tasks**: [task-008, task-009]
```

### Example 3: Superseded Decision

```yaml
### Decision 007: Session Storage Strategy (SUPERSEDED)
- **ID**: decision-007
- **Date**: 2025-12-18
- **Category**: architecture
- **Status**: superseded
- **Question**: How should we store user session data?
- **Chosen**: In-memory session storage with sticky sessions
- **Alternatives Considered**:
  - Redis (rejected at the time: seemed like over-engineering)
  - Database sessions (rejected: performance concerns)
- **Reasoning**: Simple in-memory approach seemed sufficient for initial deployment with sticky session load balancing.
- **Impacts**:
  - Affected phase-1 component-1-2 (authentication module)
- **Related Phases**: [phase-1]
- **Related Tasks**: [task-012]
- **Superseded By**: decision-013

---

### Decision 013: Session Storage Strategy (Updated)
- **ID**: decision-013
- **Date**: 2025-12-22
- **Category**: architecture
- **Status**: implemented
- **Question**: How should we store user session data at scale?
- **Chosen**: Redis-backed session storage with session sharing across instances
- **Alternatives Considered**:
  - Keep in-memory sessions (rejected: doesn't support horizontal scaling)
  - Database sessions (rejected: still too slow for session lookups)
- **Reasoning**: Load testing revealed that sticky sessions limited our scaling options and created single points of failure. Redis provides fast session lookups while allowing any instance to handle any request. This supersedes decision-007 based on new performance requirements.
- **Impacts**:
  - Affects phase-1 component-1-2 (refactor authentication module)
  - Requires task-025 (migrate to Redis sessions)
  - Requires task-026 (remove sticky session configuration)
- **Related Phases**: [phase-1]
- **Related Tasks**: [task-025, task-026]
```

## Decision Matrix Examples

```yaml
## Decision Matrix
| ID | Category | Question | Chosen | Status | Impacts |
|----|----------|----------|--------|--------|---------|
| 001 | Architecture | Database technology? | PostgreSQL + Redis | Implemented | phase-1, phase-2, task-001, task-002, task-015 |
| 002 | Security | Authentication method? | JWT with refresh tokens | Implemented | phase-1, task-012, task-013 |
| 003 | Infrastructure | Cloud provider? | AWS | Implemented | phase-1, phase-3, task-020 |
| 005 | Integration | API pattern? | REST with OpenAPI | Approved | phase-3, task-008, task-009 |
| 007 | Architecture | Session storage? | In-memory (superseded) | Superseded | phase-1, task-012 |
| 013 | Architecture | Session storage updated? | Redis-backed | Implemented | phase-1, task-025, task-026 |
```

## Common Decision Categories

### Architecture
- System structure (monolith vs microservices)
- Design patterns (MVC, repository pattern, etc.)
- Database technology and schemas
- Caching strategies

### Data
- Data modeling approaches
- Schema design decisions
- Migration strategies
- Data validation rules

### Integration
- API design (REST, GraphQL, gRPC)
- Message queue selection
- Third-party service integration
- Event-driven patterns

### Security
- Authentication methods (OAuth, JWT, sessions)
- Authorization models (RBAC, ABAC)
- Encryption strategies
- Compliance requirements (GDPR, HIPAA)

### Infrastructure
- Cloud provider selection
- Containerization approach
- CI/CD pipeline design
- Monitoring and logging strategy

## Troubleshooting

### Problem: Too many trivial decisions being tracked
**Solution**: Revisit decision categories, raise the bar for what counts as "major/architectural"

### Problem: Can't decide if something should be tracked
**Solution**: Ask "Will someone ask 'why did we do it this way?' in 6 months?" If yes, track it.

### Problem: Decision impacts keep growing
**Solution**: This is normal for foundational decisions. Consider breaking into sub-decisions.

### Problem: Decisions contradict each other
**Solution**: Use `Superseded By` to show evolution. Don't delete old decisions - they provide history.

### Problem: Too hard to keep decision matrix updated
**Solution**: Run `/update-executive-summary` after completing tasks. It will propose matrix updates.
