# Compare Options Command

## Purpose
Create structured comparison of alternatives to make informed decisions using criteria evaluation and decision matrices.

## Context Required
- Research notes from `.claude/context/research-notes.md`
- Project brief for budget and goals
- Decision log from `.claude/context/decisions.md`

## Process

1. **Define the Decision**
   - What's being decided
   - Why this decision matters
   - When decision needs to be made
   - Who's involved in deciding

2. **Establish Criteria**
   - List what matters for this decision
   - Prioritize criteria (must-have, high, medium, low)
   - Assign weights if using scoring
   - Common criteria: cost, quality, timeline, features, aesthetics

3. **Gather Options**
   - Pull from research notes
   - Typically 3-5 viable alternatives
   - Ensure options are comparable
   - Verify current pricing and availability

4. **Create Comparison Matrix**
   - Build table comparing options across criteria
   - Rate each option on each criterion
   - Calculate scores if using weighted approach
   - Highlight strengths and weaknesses

5. **Analyze Trade-Offs**
   - What do you gain/lose with each option
   - Identify deal-breakers
   - Note where compromise is needed
   - Consider total cost of ownership

6. **Make Recommendation**
   - Based on criteria and trade-offs
   - Explain rationale
   - Note any assumptions
   - Suggest backup option

7. **Document Decision**
   - Add comparison to decisions.md
   - Record final choice and why
   - Note impact on budget/timeline
   - File for future reference

## Output Location
- `.claude/context/decisions.md` - Add decision with comparison
- May reference research-notes.md for details
- Update budget/timeline if decision affects them

## Example Usage

```
/compare-options

User requests:
> Compare three vanity options: IKEA Godmorgon ($350), Home Depot
> Glacier Bay ($580), and custom carpenter quote ($1,200). Need to
> decide by Friday.

Claude creates:
1. Defines decision: Bathroom vanity selection
2. Establishes criteria: Cost, quality, size fit, installation ease,
   aesthetics, warranty
3. Builds comparison matrix with all three options
4. Analyzes trade-offs
5. Recommends Home Depot option as best value balance
6. Documents in decisions.md
```

## Comparison Matrix Template

```markdown
## Decision: [Title] - [Date]

### Context
[What you're deciding and why]

### Criteria (Priority)
1. [Criterion 1] (High/Medium/Low)
2. [Criterion 2] (High/Medium/Low)
3. [Criterion 3] (High/Medium/Low)

### Options Comparison

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| **Cost** | $[X] ⭐⭐⭐⭐⭐ | $[X] ⭐⭐⭐ | $[X] ⭐⭐ |
| **Quality** | [Rating] | [Rating] | [Rating] |
| **[Criterion]** | [Rating] | [Rating] | [Rating] |
| **Overall** | **[Score]** | **[Score]** | **[Score]** |

### Detailed Comparison

**Option A: [Name]**
- Cost: $[Amount]
- Pros:
  - [Benefit 1]
  - [Benefit 2]
- Cons:
  - [Drawback 1]
  - [Drawback 2]
- Best for: [When this is the right choice]

**Option B: [Name]**
- [Same structure]

**Option C: [Name]**
- [Same structure]

### Trade-Off Analysis

**Choosing Option A means:**
- ✅ [What you gain]
- ❌ [What you give up]

**Choosing Option B means:**
- ✅ [What you gain]
- ❌ [What you give up]

### Recommendation

**Suggested choice:** Option [X]

**Rationale:**
[Why this option best meets criteria and goals]

**When to choose different:**
- Choose A if: [Condition]
- Choose C if: [Condition]

**Next steps:**
- [ ] [Action required]
- [ ] [Update budget if needed]
- [ ] [Place order or schedule]

### Decision Made
**Final choice:** [To be filled in after deciding]
**Date decided:** [Date]
**By:** [Who decided]
**Impact:** Budget +/- $[X], Timeline +/- [Y] days
```

## Comparison Strategies

### Simple Rating Matrix

Use star ratings (1-5 stars) for subjective comparison:
- ⭐⭐⭐⭐⭐ Excellent
- ⭐⭐⭐⭐ Good
- ⭐⭐⭐ Adequate
- ⭐⭐ Below expectations
- ⭐ Poor

### Weighted Scoring

For complex decisions, assign weights:

```markdown
| Criteria (Weight) | Option A | Option B | Option C |
|-------------------|----------|----------|----------|
| Cost (30%) | 5×0.3=1.5 | 3×0.3=0.9 | 2×0.3=0.6 |
| Quality (30%) | 3×0.3=0.9 | 4×0.3=1.2 | 5×0.3=1.5 |
| Timeline (20%) | 4×0.2=0.8 | 5×0.2=1.0 | 2×0.2=0.4 |
| Aesthetics (20%) | 5×0.2=1.0 | 4×0.2=0.8 | 5×0.2=1.0 |
| **Total Score** | **4.2** | **3.9** | **3.5** |
```

### Pros/Cons List

Simpler approach for straightforward decisions:

```markdown
**Option A:**
Pros:
- Least expensive
- Available immediately
- Easy to install

Cons:
- Basic quality
- Limited warranty
- Not as attractive

**Overall:** Good budget choice if cutting costs is priority
```

### Must-Have Filter

Eliminate options that don't meet requirements:

```markdown
Must-have criteria:
- [ ] Under $600
- [ ] Fits 48" space
- [ ] Available within 2 weeks

Option A: ✅ Pass all must-haves
Option B: ✅ Pass all must-haves
Option C: ❌ Fails (over budget, 4 week lead time)

Only compare A and B further
```

## Common Decision Types

### Vendor Selection
**Criteria:**
- Price and payment terms
- Experience and reviews
- Timeline and availability
- Communication and professionalism
- Warranty and guarantees

### Material/Product Selection
**Criteria:**
- Cost (purchase + installation)
- Quality and durability
- Aesthetics and style
- Maintenance requirements
- Availability and lead time
- Warranty

### Scope Decisions (Do X or Not)
**Criteria:**
- Necessity vs nice-to-have
- Cost impact
- Timeline impact
- Future regret if skip
- ROI or value added

### Method/Approach Selection
**Criteria:**
- DIY vs professional
- Cost difference
- Time required
- Skill level needed
- Risk of mistakes
- Quality outcome

## Integration with Workflows

**After Research:**
- Research provides raw information on options
- Compare-options structures that into decision matrix
- Leads to documented decision

**Before Deciding:**
- Create comparison to inform decision
- Share with stakeholders for input
- Use as basis for discussion

**In Decision Process:**
- Comparison is middle step in decision workflow
- Feeds into final decision documentation
- Becomes reference for why choice was made

## Tips for Effective Comparison

1. **Apples to apples** - Ensure scope is truly comparable across options

2. **Include all costs** - Don't just compare price tags, include installation, operating costs, maintenance

3. **Check current info** - Verify prices and availability are up to date

4. **Be realistic** - Rate objectively, not based on what you want to win

5. **Consider total value** - Sometimes most expensive is best value long-term

6. **Set deadline** - Don't compare forever, make decision and move on

7. **Limit options** - Too many choices is paralyzing, narrow to 3-5 serious contenders

8. **Involve stakeholders** - Get input before finalizing if others are affected

## Example Comparisons

### Example 1: Contractor Selection

```markdown
## Decision: Plumbing Contractor - May 15, 2025

### Criteria
1. Price (High) - Within $8,000-$10,000 budget
2. Experience/Reviews (High) - 4+ stars, 3+ years
3. Timeline (Medium) - Can start within 3 weeks
4. Communication (Medium) - Responsive, professional

### Comparison

| | ABC Plumbing | XYZ Contractors | Quality Bath |
|---|---|---|---|
| Price | $8,500 ⭐⭐⭐⭐⭐ | $7,200 ⭐⭐⭐⭐⭐ | $9,800 ⭐⭐⭐ |
| Reviews | 4.8 (120) ⭐⭐⭐⭐⭐ | 4.2 (45) ⭐⭐⭐⭐ | 4.9 (200) ⭐⭐⭐⭐⭐ |
| Experience | 12 yrs ⭐⭐⭐⭐⭐ | 3 yrs ⭐⭐⭐ | 25 yrs ⭐⭐⭐⭐⭐ |
| Timeline | 2 weeks ⭐⭐⭐⭐ | 3 weeks ⭐⭐⭐ | 10 days ⭐⭐⭐⭐⭐ |
| **Overall** | **⭐⭐⭐⭐⭐** | **⭐⭐⭐⭐** | **⭐⭐⭐⭐** |

### Recommendation: ABC Plumbing
Best balance of price, experience, and quality. Quality Bath is excellent
but $1,300 premium not justified. XYZ is cheapest but newer business.

**Decision:** Selected ABC Plumbing
**Impact:** Budget: $8,500, Timeline: Starts June 1
```

### Example 2: Material Selection

```markdown
## Decision: Shower Tile - May 22, 2025

### Criteria
1. Cost (High) - Under $2,000 total
2. Water resistance (High) - Must be suitable for shower
3. Aesthetics (Medium) - Modern, neutral
4. Installation (Medium) - Standard or easier

### Options

**Porcelain Subway - $1,650 total**
- Pros: Classic look, very durable, water-resistant
- Cons: Heavier (needs stronger adhesive +$100)

**Ceramic Large Format - $1,250 total**
- Pros: Fewer grout lines, modern, budget-friendly
- Cons: Harder to get perfect layout, can crack if substrate flexes

**Natural Stone - $2,800 total**
- Pros: Unique, high-end look
- Cons: Over budget, needs sealing, more maintenance

### Decision: Porcelain Subway
Classic choice, within budget, contractor familiar with installation.
Good balance of cost and quality.

**Impact:** Budget: $1,650, Timeline: No change
```
