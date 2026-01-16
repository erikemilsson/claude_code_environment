# Life Projects Template

A comprehensive template for managing everyday non-technical projects using Claude Code's task management and documentation capabilities.

## When to Use This Template

Use the Life Projects template when you need to plan, execute, and track progress on real-world projects that benefit from structured planning and documentation. Perfect for projects where you may lack expertise and need guidance through the process.

### Ideal For

**Home Improvement:**
- Bathroom or kitchen renovation
- Basement finishing
- Landscaping and garden design
- Home office setup
- Roof replacement or major repairs

**Life Events:**
- Wedding planning and coordination
- Moving and relocation
- Baby preparation and nursery setup
- College application process
- Career transition planning

**Personal Projects:**
- Learn a new skill (language, instrument, cooking)
- Fitness and health programs
- Home organization (KonMari method, decluttering)
- Vehicle restoration or customization
- Multi-week travel planning

**Financial and Administrative:**
- Estate planning
- Insurance review and consolidation
- Home buying process
- Retirement planning
- Starting a non-tech business

## What This Template Provides

### 1. Structured Planning
- Project brief template to define goals, budget, timeline, and constraints
- Research documentation for gathering information
- Decision logging to track choices and rationale
- Budget tracking against estimates

### 2. Task Management Integration
- Hierarchical task breakdown (project → phases → tasks)
- Difficulty scoring based on complexity/risk for non-experts
- Dependency tracking (e.g., can't install tile before waterproofing)
- Status updates with notes and photo documentation

### 3. Progress Tracking
- Update workflows for documenting progress
- Photo and receipt organization
- Issue and blocker tracking
- Milestone celebration points

### 4. Decision Support
- Vendor comparison frameworks
- Option evaluation matrices
- Research-guided recommendations
- Cost-benefit analysis templates

## Template Structure

```
project/
├── CLAUDE.md                    # Points to context files
├── README.md                    # Project-specific documentation
└── .claude/
    ├── commands/
    │   ├── update-progress.md   # Log progress with photos/notes
    │   ├── research.md          # Web search for information
    │   ├── compare-options.md   # Decision matrix for choices
    │   └── update-budget.md     # Track spending vs estimates
    ├── context/
    │   ├── project-brief.md     # Goals, budget, timeline, constraints
    │   ├── research-notes.md    # Findings, vendor info, options
    │   ├── decisions.md         # Decision log with rationale
    │   ├── budget-tracker.md    # Costs, quotes, actuals
    │   └── standards/
    │       ├── project-planning.md
    │       ├── budget-management.md
    │       └── timeline-planning.md
    └── tasks/
        ├── task-overview.md
        └── task-*.json
```

## Example: Bathroom Renovation Project

### Initial Setup

**User provides specification:**
> "I want to renovate my master bathroom. Budget is $15,000. Goals: replace tub with walk-in shower, new tile floor and walls, modern vanity, new toilet, improved lighting. I have no plumbing experience and need to hire contractors. Timeline: 3 months. Located in Seattle, WA."

**Claude Code generates:**

1. **Project Brief** with goals, budget, timeline, constraints
2. **Task Breakdown** (35+ tasks):
   - Research phase (shower systems, tile options, contractors, permits)
   - Planning phase (design, measurements, material selection)
   - Contractor phase (quotes, selection, contract review)
   - Execution phase (demo, plumbing, electrical, tile, fixtures)
   - Completion phase (inspection, punch list, documentation)

3. **Research Templates** for:
   - Shower system options (walk-in, curb, curbless)
   - Tile materials and costs
   - Local contractor vetting
   - Seattle permit requirements

4. **Budget Tracker** with line items:
   - Labor (plumbing, electrical, tile, general)
   - Materials (shower, tile, vanity, toilet, lighting)
   - Permits and fees
   - Contingency (15%)

### During Execution

**User updates progress:**
```
/update-progress
> Contractor removed old tub and tile. Found some water damage behind
> wall that needs repair. Adding $800 to budget. Attaching photos.
```

**Claude Code:**
- Updates task status (Demo → Complete)
- Logs issue in decisions.md
- Updates budget tracker (+$800)
- Creates new task for water damage repair
- Adjusts timeline if needed

**User researches options:**
```
/research
> What are the pros/cons of porcelain vs ceramic tile for shower walls?
```

**Claude Code:**
- Performs web search with grounding
- Documents findings in research-notes.md
- Creates comparison table
- Updates decision log when choice is made

### Completion

**Final deliverables:**
- Complete task history with status updates
- Photo documentation of before/during/after
- Final budget with variance analysis
- Vendor contact list with ratings
- Warranty and receipt storage
- Lessons learned for future projects

## Components Used

This template integrates the following components:

- **Task Management** (v1.0.0) - Core task tracking with difficulty scoring and dependencies
- **Project Brief** (custom) - Structured project definition
- **Budget Tracking** (custom) - Financial planning and tracking
- **Decision Logging** (custom) - Choice documentation with rationale
- **Progress Documentation** (custom) - Updates with photos and notes

## Customization Options

### Adjust Difficulty Scoring

For life projects, difficulty often relates to:
- Technical complexity for non-experts
- Financial risk
- Time commitment
- Need for professional help
- Regulatory requirements (permits, inspections)

Example custom scale:
```json
{
  "difficulty_mapping": {
    "1-2": "Simple DIY (paint a room, organize closet)",
    "3-4": "Moderate DIY (install shelving, minor repairs)",
    "5-6": "Complex DIY or simple contractor work (fence installation, appliance replacement)",
    "7-8": "Major contractor work (kitchen remodel, electrical panel upgrade)",
    "9-10": "Extensive projects requiring multiple specialists (home addition, full renovation)"
  }
}
```

### Add Custom Workflows

Examples:
- Vendor evaluation process
- Permit application workflow
- Safety inspection checklist
- Quality assurance reviews
- Insurance claim documentation

### Extend Reference Templates

Add project-specific templates:
- Material selection guides
- Room measurement forms
- Contractor interview questions
- Payment milestone schedules
- Warranty registration tracking

## Integration with Other Templates

### Combine with Documentation Template
For projects requiring extensive documentation (e.g., estate planning):
- Use Life Projects for task management and progress tracking
- Use Documentation template for formal document creation

### Combine with Research Template
For projects heavy on research (e.g., buying a home):
- Use Life Projects for overall project coordination
- Use Research template for market analysis and due diligence

## Getting Started

### Quick Start (5 minutes)

1. **Copy base structure** to your project directory
2. **Edit project-brief.md** with your goals, budget, timeline
3. **Run initial breakdown**: `/breakdown` to create task hierarchy
4. **Start first research task**: Begin gathering information
5. **Update as you go**: Use `/update-progress` regularly

### Full Setup (30 minutes)

1. **Define project scope** in detail
2. **Research initial options** for major decisions
3. **Create comprehensive task breakdown** with dependencies
4. **Set up budget tracker** with line items and estimates
5. **Identify key vendors** and add to contacts
6. **Establish decision criteria** for major choices
7. **Create photo organization** system
8. **Set milestone dates** and review schedule

## Tips for Success

### For First-Time Users
- Start with simple projects to learn the system
- Don't over-plan; adjust as you learn
- Document decisions immediately (you'll forget why you chose X over Y)
- Take photos at every stage
- Build in 20% budget contingency

### For Complex Projects
- Break down into phases with clear completion criteria
- Create dependencies carefully (what truly blocks what)
- Use difficulty ≥7 trigger for breaking down into subtasks
- Schedule regular reviews (weekly for major projects)
- Track lessons learned for future reference

### For Budget-Sensitive Projects
- Get multiple quotes (3+ for major work)
- Research material costs before contractor estimates
- Track every expense immediately
- Use `/compare-options` for significant purchases
- Document all warranty and return policies

## Command Reference

### `/update-progress`
Log progress updates with notes, photos, and status changes.

**Usage:**
```
/update-progress
> Completed tile installation in shower. Contractor found proper slope
> to drain. Grout scheduled for tomorrow. See attached photos.
```

### `/research`
Perform web searches and document findings.

**Usage:**
```
/research
> Best practices for waterproofing shower walls before tile installation
```

### `/compare-options`
Create decision matrix for evaluating choices.

**Usage:**
```
/compare-options
> Compare three vanity options: IKEA Godmorgon vs Home Depot Glacier Bay
> vs custom local carpenter. Criteria: cost, quality, timeline, warranty.
```

### `/update-budget`
Track actual spending against budget estimates.

**Usage:**
```
/update-budget
> Contractor invoice for plumbing rough-in: $2,400 (estimated $2,200).
> Variance: +$200 due to additional shutoff valves required by code.
```

## Version History

- **v1.0.0** (2025-11-16) - Initial template creation
  - Project brief and planning templates
  - Budget tracking system
  - Decision logging framework
  - Progress update workflows
  - Research and comparison commands
  - Vendor management templates

## Related Templates

- **Documentation/Content** - For projects requiring formal documentation
- **Research/Analysis** - For projects heavy on research and data analysis
- **Task Management Component** - Core task tracking system used by this template

## Support and Feedback

This template is part of the Claude Code environment system. For questions or improvements, refer to the main repository documentation.
