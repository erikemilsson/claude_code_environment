# Iterate Command

Structured spec review that identifies gaps, asks focused questions, and suggests content for you to add.

## Usage

```
/iterate                    # Auto-detect weakest area from checklist
/iterate overview           # Focus on Overview section
/iterate architecture       # Focus on Architecture section
/iterate requirements       # Focus on Requirements section
/iterate acceptance         # Focus on Acceptance Criteria section
/iterate questions          # Focus on Open Questions section
/iterate {custom topic}     # Focus on specific topic you name
```

## What It Does

1. **Reads current spec** and checklist
2. **Identifies focus area** (your choice or weakest section)
3. **Asks up to 4 questions** about that area
4. **Generates suggested content** based on your answers
5. **You edit the spec** with the suggestions
6. **Repeat** until section is solid

---

## Process

### Step 1: Load Context

Read:
- `../spec_v{N}.md` - Current specification
- `reference/spec-checklist.md` - Readiness criteria

### Step 2: Determine Focus Area

**If user specified an area:** Use that area.

**If no area specified:** Evaluate spec against checklist and identify:
1. Sections with placeholder text (highest priority)
2. Sections missing required criteria
3. Sections with red flags

Select the weakest area. Report:
```
Checking spec against readiness checklist...

Section Status:
- Overview: Needs work (missing problem statement)
- Architecture: Not started (placeholder text)
- Requirements: Partial (2 of 3 criteria met)
- Acceptance Criteria: Partial (3 criteria, need 5+)
- Open Questions: Blocking (architecture questions unresolved)

Focusing on: Architecture (has placeholder text)
```

### Step 3: Ask Questions (max 4)

Generate focused questions for the target area. Questions should:
- Be specific and answerable
- Build on each other logically
- Extract concrete details, not opinions
- Avoid yes/no when possible

**Question format:**
```
## Architecture Questions

1. What are the main components of this system?
   (e.g., "web frontend, API server, database" or "CLI tool, config files")

2. How do these components communicate?
   (e.g., "REST API", "message queue", "direct function calls")

3. Where does data live and how does it flow?
   (e.g., "User submits form → API validates → stored in Postgres")

4. What's the deployment model?
   (e.g., "single server", "containerized microservices", "serverless functions")
```

**Wait for user responses before proceeding.**

### Step 4: Generate Suggestions

Based on answers, generate spec-ready content:

```
## Suggested Content for Architecture Section

Based on your answers, here's suggested content to add:

---

### Components

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   React     │────▶│   Express   │────▶│  PostgreSQL │
│   Frontend  │◀────│   API       │◀────│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Frontend (React)**
- Single-page application
- Handles user authentication UI
- Communicates with API via REST

**API Server (Express)**
- RESTful endpoints for all operations
- JWT-based authentication
- Validates all input before database operations

**Database (PostgreSQL)**
- Stores user accounts and application data
- Schema migrations managed with Knex

### Key Design Decisions

- **REST over GraphQL**: Simpler for MVP, team familiarity
- **PostgreSQL over MongoDB**: Relational data model, ACID compliance needed

---

Copy the above into your spec's Architecture section, then modify as needed.
```

### Step 5: Confirm and Continue

After presenting suggestions:

```
Please edit the spec with these suggestions (modify as needed).

When ready:
- Type "next" to continue to another weak area
- Type "done" to finish this session
- Or specify a section: /iterate requirements
```

---

## Question Banks by Section

### Overview Questions
1. In one sentence, what does this system do?
2. Who specifically will use this? (role, not "users")
3. What problem does this solve that isn't solved today?
4. What's the simplest success scenario? (user does X, gets Y)

### Architecture Questions
1. What are the main components/services?
2. How do components communicate?
3. Where does data live and how does it flow?
4. What external services/APIs does this depend on?

### Requirements Questions
1. What must a user be able to do? (list 3-5 actions)
2. What must the system do automatically? (without user action)
3. What are the hard constraints? (tech, budget, timeline, compliance)
4. What's explicitly out of scope?

### Acceptance Criteria Questions
1. How would you demo this to someone? (the steps)
2. What would make you say "this is broken"?
3. What's the minimum performance you'd accept?
4. What security requirements are non-negotiable?

### Open Questions Questions
1. What technical decisions haven't been made yet?
2. What are you unsure about in the requirements?
3. What dependencies on external factors exist?
4. What would you ask a domain expert if you had one?

---

## Examples

### Example 1: Auto-detect mode
```
User: /iterate

Claude: Checking spec against readiness checklist...

Section Status:
- Overview: Good
- Architecture: Needs work (no component relationships)
- Requirements: Good
- Acceptance Criteria: Needs work (only 2 criteria)
- Open Questions: Good

Focusing on: Architecture

## Architecture Questions

1. You've listed Frontend and API as components. How do they communicate?
   (REST, GraphQL, WebSocket, etc.)

2. You mention a database but not which one. What type of data are you storing
   and what database fits? (relational, document, key-value)

3. Are there any background jobs or async processes?
   (email sending, report generation, data sync)

4. What handles authentication - the API directly or a separate service?
```

### Example 2: Focused mode
```
User: /iterate acceptance

Claude: Focusing on Acceptance Criteria.

Current criteria in spec:
1. User can create an account
2. User can log in

Checklist requires: 5+ testable criteria covering core user journey.

## Acceptance Criteria Questions

1. After login, what's the first thing a user does?
   (This is likely your core feature - needs criteria)

2. What error scenarios must be handled visibly to the user?
   (Failed login, validation errors, network issues)

3. Is there any data the user creates/manages?
   (Each CRUD operation typically needs a criterion)

4. What would a user complain about if it was slow or broken?
   (These are your critical path criteria)
```

---

## Rules

**Claude MUST NOT:**
- Edit the spec file directly
- Skip the question step and jump to suggestions
- Ask more than 4 questions at once
- Generate suggestions before receiving answers

**Claude MUST:**
- Always check the spec against the checklist first
- Present section status before diving into questions
- Format suggestions as copy-pasteable content
- Wait for explicit signal to continue to next area
