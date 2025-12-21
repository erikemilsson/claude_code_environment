# Specification Templates

Use these templates when creating project specifications for bootstrap. Each template includes the keywords and structure that trigger automatic template detection.

## How to Use These Templates

1. **Choose the template** that matches your project type
2. **Copy the template** to a new file
3. **Fill in your details** where indicated with `[brackets]`
4. **Keep the detection keywords** (marked with ⚡) - these trigger auto-selection
5. **Save as `.md` file** in a convenient location
6. **Run bootstrap** with your specification

## Available Templates

### Power Query Template
**File**: `power-query-spec-template.md`
**Best for**: Excel Power Query projects, regulatory calculations, complex formulas
**Detection keywords**: "Power Query", "M language", "Excel", "regulatory calculation"
**Auto-select confidence**: 90%+ (very high)

### Research/Analysis Template
**File**: `research-spec-template.md`
**Best for**: Academic research, data science experiments, hypothesis testing
**Detection keywords**: "research question", "hypothesis", "literature review", "statistical analysis"
**Auto-select confidence**: 90%+ (very high)

### Life Projects Template
**File**: `life-project-spec-template.md`
**Best for**: Personal goals, fitness tracking, learning journeys, home organization
**Detection keywords**: "personal goal", "my", "I want to", fitness/health keywords
**Auto-select confidence**: 75%+ (high)

### Documentation Template
**File**: `documentation-spec-template.md`
**Best for**: Technical writing, API docs, knowledge bases, content creation
**Detection keywords**: "documentation", "technical writing", "API docs", "content creation"
**Auto-select confidence**: 90%+ (very high)

## Template Structure

All templates follow this structure:

```markdown
# Project Name

## What I'm Building
[Brief description with detection keywords ⚡]

## Technology Stack
[Languages, frameworks, tools - be specific!]

## Goals
[What do you want to achieve?]

## Timeline
[Weekend project, multi-week, long-term]

## Requirements/Features
[List of deliverables or features]

## Additional Context
[Any special considerations]
```

## Detection Tips

**For best auto-detection:**

✅ **DO**:
- Use specific technology names ("Python pandas" not "data processing")
- Mention your domain explicitly ("research", "personal", "regulatory")
- Include timeline indicators ("weekend project", "3-month timeline")
- List concrete deliverables

❌ **DON'T**:
- Use only generic terms ("data", "analysis", "project")
- Skip technology stack
- Be vague about project type
- Omit goals or requirements

## Example Validation

After creating your spec, you can validate it before bootstrap:

```bash
# In Claude Code (VS Code):
"Validate my specification at ~/Documents/my-project-spec.md"
```

The validator will show:
- Detected template and confidence score
- Which keywords triggered detection
- Missing signals with suggestions
- Whether spec is ready for bootstrap

## Need Help?

**Specification too vague?**
- Use the interactive spec builder: `.claude/commands/create-spec.md` (Task 100)
- Review example specifications: `examples/specifications/` directory

**Not sure which template?**
- Describe your project in Claude Desktop first
- Export the conversation as your specification
- Validator will help you identify the best template

**Want to see detection patterns?**
- See: `.claude/reference/template-selection-rules.md`
- Full detection logic with scoring rules
