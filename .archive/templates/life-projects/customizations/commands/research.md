# Research Command

## Purpose
Gather information via web search to inform project decisions, find options, understand best practices, and document findings.

## Context Required
- Project brief from `.claude/context/project-brief.md`
- Current research notes from `.claude/context/research-notes.md`
- Decision log for context on what's being decided

## Process

1. **Clarify Research Goal**
   - Understand what information is needed
   - Identify specific questions to answer
   - Determine how research will be used

2. **Perform Web Search**
   - Use WebSearch tool for current information
   - For complex analysis, consider using Gemini API (via MCP) with `grounding: true`
   - Search for:
     - Product/material options
     - Best practices and guides
     - Vendor comparisons
     - Cost estimates
     - Reviews and recommendations
     - Local requirements (codes, permits)

3. **Analyze Findings**
   - Summarize key information
   - Identify viable options
   - Note pros/cons of each option
   - Extract relevant specifications
   - Capture cost ranges
   - Note availability and lead times

4. **Document Research**
   - Add findings to `.claude/context/research-notes.md`
   - Organize by category or decision area
   - Include sources and dates
   - Note confidence level in information

5. **Identify Next Steps**
   - What decisions can now be made
   - What additional research is needed
   - Who needs to be consulted
   - When decision should be made

## Output Location
- `.claude/context/research-notes.md` - Append research findings
- `.claude/context/decisions.md` - Link to related decisions
- May create new tasks for follow-up research or decisions

## Example Usage

```
/research

User asks:
> What are the pros and cons of porcelain vs ceramic tile for
> shower walls? What's the cost difference?

Claude:
1. Performs web search on tile types
2. Searches for cost comparisons
3. Looks up installation considerations
4. Finds best practices for shower applications
5. Documents findings:
   - Porcelain: denser, more water-resistant, $8-15/sq ft
   - Ceramic: lighter, easier to cut, $3-8/sq ft
   - For showers: both work, porcelain preferred for floors
   - Installation: porcelain needs stronger adhesive
6. Adds to research notes with source links
7. Suggests creating decision task if needed
```

## Research Note Template

```markdown
## Research: [Topic] - [Date]

### Question/Goal
[What you're trying to find out]

### Findings

**Option 1: [Name]**
- Description: [What it is]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Cost: $[Range or amount]
- Availability: [Lead time, where to buy]
- Best for: [Use cases]

**Option 2: [Name]**
- [Same structure]

### Best Practices
- [Key recommendation 1]
- [Key recommendation 2]

### Considerations
- [Important factor to keep in mind]
- [Another consideration]

### Sources
- [Website/article with date accessed]
- [Another source]

### Next Steps
- [Decision to make]
- [Additional research needed]
- [People to consult]
```

## Research Categories

### Product/Material Research
- Specifications and features
- Price ranges and availability
- Reviews and ratings
- Warranty and support
- Maintenance requirements

### Vendor/Service Research
- Local options in your area
- Reviews and reputation
- Licensing and insurance
- Typical pricing
- Availability and lead times

### Process/Method Research
- Best practices for task
- Step-by-step guides
- Required tools and materials
- Estimated time
- Skill level needed
- Common mistakes to avoid

### Regulatory Research
- Permit requirements
- Code compliance
- Inspection requirements
- HOA rules (if applicable)
- Local restrictions

### Cost Research
- Typical price ranges
- Cost breakdowns (labor vs materials)
- Ways to save money
- Hidden costs to consider
- ROI or resale value impact

## Integration with Other Commands

**With `/compare-options`:**
- Research provides raw information
- Compare-options creates decision matrix
- Use research findings as input to comparison

**With `/update-progress`:**
- Research findings inform progress notes
- Document what was learned during execution
- Note if research was accurate vs actual experience

**With decision-making:**
- Research informs criteria and options
- Findings feed into decision documentation
- Track decisions back to research source

## Tips for Effective Research

1. **Be specific in queries** - "Best shower tile for small bathroom" vs "bathroom tile"

2. **Check dates** - Prefer recent information (within 1-2 years) for products and prices

3. **Cross-reference** - Verify important information across multiple sources

4. **Save sources** - Include URLs and access dates for future reference

5. **Watch for bias** - Manufacturer sites vs independent reviews

6. **Local considerations** - Filter for your geographic area when relevant

7. **Budget context** - Research within your budget range to avoid wanting what you can't afford

8. **Practical focus** - Prioritize information you can actually act on
