# Tutorial: Bootstrap Your First Environment

## Purpose
Interactive tutorial that walks first-time users through the bootstrap process using example specifications. Provides a safe learning environment with immediate feedback and explanations.

## Who This Is For
- First-time users of the Claude Code environment system
- Users who want to understand the bootstrap process before using real projects
- Users exploring template capabilities

## What You'll Learn
1. How to read and structure project specifications
2. How template detection analyzes your spec
3. What files get generated and why
4. How to verify the environment is correct
5. How to customize for your needs

## Prerequisites
- Claude Code installed and running
- This repository cloned locally
- 10-15 minutes of uninterrupted time

---

## Tutorial Flow

### Welcome Message
```markdown
Welcome to the Claude Code Environment Bootstrap Tutorial!

This interactive tutorial will walk you through creating a complete project
environment using an example specification. You'll see:
- How template detection works
- What files get generated
- How the task system initializes
- Where to customize for your needs

We'll use a simple research project as our example. Ready? Let's begin!

Time required: 10-15 minutes
```

### Step 1: Show Example Specification

**Action**: Display the example spec and explain key parts

```markdown
STEP 1: Understanding Project Specifications

Let me show you an example specification for a remote work research project:

[Read and display: examples/specifications/templates/research-spec-template.md]

KEY SECTIONS TO NOTICE:
1. Research Question - Clear, specific question (triggers Research template)
2. Hypothesis - Testable prediction (high confidence signal)
3. Literature Review - Academic context (Research template indicator)
4. Methodology - Quantitative/qualitative approach
5. Timeline - Research phases with dates

TEMPLATE DETECTION KEYWORDS:
- "research question" (+30 points)
- "hypothesis" (+30 points)
- "literature review" (+15 points)
- "statistical analysis" (+15 points)

Expected detection confidence: 90%+ (auto-select Research template)

Press ENTER when ready for Step 2...
```

**Educational Note**: Explain why these keywords matter and how they map to templates.

### Step 2: Template Detection Analysis

**Action**: Run template detection and show detailed reasoning

```markdown
STEP 2: Template Detection in Action

Now I'll analyze this specification using the same process you'll use
for your own projects. Watch how the system identifies patterns...

[Execute smart detection process]

ANALYSIS RESULTS:

Template Scores:
████████████████████ Research (90%) ✓ AUTO-SELECTED
████░░░░░░░░░░░░░░░░ Base (20%)
██░░░░░░░░░░░░░░░░░░ Power Query (10%)
██░░░░░░░░░░░░░░░░░░ Life Projects (10%)
█░░░░░░░░░░░░░░░░░░░ Documentation (5%)

WHY RESEARCH WON:
✓ Found "research question" in heading → +30pts (high signal)
✓ Found "hypothesis" with predictions → +30pts (high signal)
✓ Found "literature review" section → +15pts (medium signal)
✓ Found "statistical analysis" → +15pts (medium signal)
Total: 90pts (threshold: 85pts for auto-select)

OTHER TEMPLATES:
- Base template got 20pts from generic "project" mentions
- No Power BI/Power Query keywords found
- No personal life project indicators

CONFIDENCE LEVEL: HIGH (90% > 85% threshold)
ACTION: Auto-select Research template (no confirmation needed)

This high confidence means we can skip the confirmation questions
and go straight to environment generation!

Press ENTER when ready for Step 3...
```

**Educational Note**: Show visual confidence bars and explain threshold logic.

### Step 3: Environment Generation

**Action**: Create temporary demo environment and explain each file

```markdown
STEP 3: Generating Your Environment

Now I'll create the complete .claude/ structure in a temporary
demo directory. You'll see exactly what gets created and why.

[Create temporary directory: /tmp/tutorial-remote-work-research/]

Creating files in parallel:
✓ CLAUDE.md (router file)
✓ README.md (human documentation)
✓ .claude/context/overview.md
✓ .claude/context/validation-rules.md
✓ .claude/commands/complete-task.md
✓ .claude/commands/breakdown.md
✓ .claude/commands/sync-tasks.md
✓ .claude/reference/difficulty-guide.md
✓ .claude/tasks/task-001.json (from requirements)
✓ .claude/tasks/task-002.json (from requirements)
✓ .claude/tasks/task-overview.md

TEMPLATE-SPECIFIC FILES (Research):
✓ .claude/context/research-methodology.md
✓ .claude/reference/statistical-analysis-guide.md
✓ .claude/commands/literature-review.md

Total: 14 files created in 2.3 seconds

Press ENTER to explore the generated files...
```

**Educational Note**: Explain base files vs. template-specific additions.

### Step 4: File Walkthrough

**Action**: Show key generated files with annotations

```markdown
STEP 4: Understanding Generated Files

Let's examine the key files that were created:

═══════════════════════════════════════════════════════════
FILE: CLAUDE.md (Router file for AI context)
═══════════════════════════════════════════════════════════

[Show first 30 lines with annotations]

KEY FEATURES:
- Points to .claude/ structure for detailed context
- Stays under 100 lines (lightweight)
- Template-specific routing (Research commands)
- Navigation guide for AI

WHY IT EXISTS: Keeps AI context organized without overwhelming

═══════════════════════════════════════════════════════════
FILE: .claude/context/overview.md (Extracted from spec)
═══════════════════════════════════════════════════════════

[Show generated overview with spec content]

NOTICE:
✓ Research question automatically extracted
✓ Timeline populated from spec
✓ Methodology section populated
✓ Expected outcomes listed

This is YOUR specification content, formatted for AI understanding!

═══════════════════════════════════════════════════════════
FILE: .claude/tasks/task-001.json (Initial task)
═══════════════════════════════════════════════════════════

{
  "id": "1",
  "title": "Complete literature review",
  "description": "Review 5 key papers on remote work and productivity",
  "difficulty": 5,
  "status": "Pending",
  "created_date": "2025-12-17",
  "dependencies": [],
  "subtasks": [],
  "parent_task": null,
  "files_affected": [".claude/context/research-methodology.md"],
  "notes": "Extracted from specification - Section: Literature Review",
  "priority": "high",
  "tags": ["research", "literature-review"]
}

NOTICE:
✓ Extracted from "Literature Review" section in spec
✓ Difficulty scored automatically (5 = moderate)
✓ Ready to work on immediately
✓ Links back to source section

Press ENTER to see customization options...
```

**Educational Note**: Show how spec content flows into generated files.

### Step 5: Customization Points

**Action**: Highlight what users typically customize

```markdown
STEP 5: Customizing for Your Needs

The generated environment is fully functional, but here's what
users typically customize:

COMMON CUSTOMIZATIONS:

1. CLAUDE.md Navigation
   Location: /CLAUDE.md
   Typical change: Add project-specific command patterns
   Example: Add "/analyze-survey-data" command for research

2. Validation Rules
   Location: .claude/context/validation-rules.md
   Typical change: Add domain-specific quality gates
   Example: "All statistical tests must include power analysis"

3. Task Breakdown
   Location: .claude/tasks/
   Typical change: Refine difficulty scores, add dependencies
   Example: Mark tasks requiring IRB approval

4. Context Standards
   Location: .claude/context/standards/
   Typical change: Add technology-specific conventions
   Example: "All Python code must use scipy.stats for analysis"

TEMPLATE-SPECIFIC (Research):

5. Research Methodology
   Location: .claude/context/research-methodology.md
   Typical change: Detail your specific approach
   Example: Add survey instrument details

6. Statistical Analysis Guide
   Location: .claude/reference/statistical-analysis-guide.md
   Typical change: List your specific tests
   Example: "Use mixed-effects models for longitudinal data"

WHAT NOT TO CHANGE:
× Command file structure (.claude/commands/*.md format)
× Task JSON schema (breaks automation)
× Router pattern in CLAUDE.md (AI needs this)

Press ENTER to see verification steps...
```

**Educational Note**: Show before/after examples of customizations.

### Step 6: Verification Checklist

**Action**: Provide concrete checklist for users

```markdown
STEP 6: Verifying Your Environment

Before starting work, verify the environment is correct:

VERIFICATION CHECKLIST:

Structure:
[ ] CLAUDE.md exists and is under 100 lines
[ ] README.md explains project to humans
[ ] .claude/ directory has 4 subdirectories (commands, context, tasks, reference)

Content:
[ ] .claude/context/overview.md contains your project details
[ ] .claude/tasks/ has at least 1 task JSON file
[ ] .claude/tasks/task-overview.md was generated
[ ] Template-specific files present (if not using Base)

Functionality:
[ ] Run: /complete-task 1 → Should show task details
[ ] Run: /sync-tasks → Should regenerate overview
[ ] Check task-overview.md → Should show task table

Template Detection:
[ ] Selected template matches your project type
[ ] Confidence score was reasonable (>70%)
[ ] Template-specific commands are relevant

IF ANY CHECKS FAIL:
1. Re-run bootstrap with updated specification
2. Check spec has clear template indicators (see examples/)
3. Use /bootstrap for interactive template selection

ALL CHECKS PASSED? You're ready to work on your project!

Press ENTER for next steps...
```

**Educational Note**: Explain what to do if verification fails.

### Step 7: Next Steps & Real Project

**Action**: Guide user to apply learning to their project

```markdown
STEP 7: Try It With Your Own Project!

You've seen the complete bootstrap process with an example.
Now it's time to use your own project specification!

YOUR TURN:

1. Create Your Specification
   - Use examples/specifications/templates/ as reference
   - Include clear template indicators (see tutorial)
   - Export from Claude Desktop as single .md file

2. Navigate to Your Project Directory
   cd ~/Projects/your-new-project/

3. Run Bootstrap
   Say: "Create environment from claude_code_environment repo using: [spec-path]"

   OR use interactive mode:
   /bootstrap

4. Verify Environment
   Use checklist from Step 6

5. Start Working
   /complete-task 1
   [Do the work]
   /sync-tasks

TIPS FOR SUCCESS:

✓ Write clear, specific project descriptions
✓ Include domain-specific terminology (Power BI, research, etc.)
✓ List concrete requirements (becomes initial tasks)
✓ Specify technology stack clearly
✓ Include timeline or phases

COMMON MISTAKES:

× Vague specs ("I want to analyze data")
× Missing template indicators
× No concrete requirements listed
× Mixing multiple project types in one spec

LEARNING RESOURCES:

- examples/specifications/templates/ → Spec templates for each type
- .claude/reference/template-selection-rules.md → Detection patterns
- legacy-template-reference.md → Comprehensive documentation
- README.md → Quick reference

QUESTIONS? Check the FAQ section in README.md

═══════════════════════════════════════════════════════════
                    TUTORIAL COMPLETE!
═══════════════════════════════════════════════════════════

You now understand:
✓ How to structure project specifications
✓ How template detection analyzes content
✓ What files get generated and why
✓ How to verify and customize environments
✓ How to start working on tasks

Temporary demo directory preserved at:
/tmp/tutorial-remote-work-research/

Feel free to explore the files before deleting.

Ready to bootstrap your first real project? Good luck! 🚀
```

---

## Implementation Notes

### Tutorial Execution Flow

1. **Interactive Mode**: Pause after each step for user acknowledgment
2. **Non-Interactive Mode**: Run all steps and show summary
3. **Cleanup**: Offer to preserve or delete demo directory

### Demo Directory Management

**Create temporary environment**:
```bash
DEMO_DIR="/tmp/tutorial-remote-work-research-$(date +%s)"
mkdir -p "$DEMO_DIR"
```

**Cleanup after tutorial**:
```bash
# Ask user
echo "Keep demo directory for exploration? (y/n)"
read -r response
if [ "$response" = "n" ]; then
  rm -rf "$DEMO_DIR"
  echo "Demo directory deleted."
else
  echo "Demo preserved at: $DEMO_DIR"
fi
```

### Educational Enhancements

**Visual confidence bars**:
```
Research:     ████████████████████ 90%
Base:         ████░░░░░░░░░░░░░░░░ 20%
Power Query:  ██░░░░░░░░░░░░░░░░░░ 10%
```

**Before/After examples** for customizations:
```
BEFORE (generated):
Task difficulty: 5 (auto-scored)

AFTER (customized):
Task difficulty: 7 (requires IRB approval, multiple dependencies)
```

**Annotation format** for file displays:
```
FILE: .claude/context/overview.md
[Lines 1-10 shown]

→ This section: Extracted from spec "Research Question"
→ This section: Populated from "Timeline"
→ This section: Generated from requirements analysis
```

## Success Metrics

Users who complete this tutorial should be able to:
1. Write effective project specifications
2. Predict which template will be selected
3. Verify generated environment correctness
4. Customize environment for their needs
5. Start working on tasks immediately

## Related Commands

- `/smart-bootstrap` - One-command environment creation
- `/bootstrap` - Interactive template selection
- `/complete-task` - Start/finish tasks
- `/sync-tasks` - Update task overview

## File Location
`.claude/commands/tutorial-bootstrap.md`
