# Update Budget Command

## Purpose
Track actual spending against budget estimates, record variances, and maintain accurate financial status for the project.

## Context Required
- Budget tracker from `.claude/context/budget-tracker.md`
- Project brief for original budget
- Receipts or invoices for costs being recorded

## Process

1. **Gather Transaction Information**
   - Who was paid (vendor/store name)
   - Amount paid
   - Date of transaction
   - What it was for (description)
   - Which budget line item it belongs to
   - Receipt or invoice number
   - Payment method

2. **Record in Budget Tracker**
   - Add transaction to appropriate line item
   - Update "Actual Cost" column
   - Update status (Estimated → Quoted → Committed → Paid)
   - File receipt reference

3. **Calculate Variance**
   - Compare actual to estimated cost
   - Calculate difference (actual - estimated)
   - Calculate percentage variance
   - Note if over or under budget

4. **Analyze Variance**
   - If significant variance (>10%), note reason
   - Categorize: scope change, market price, mistake in estimate, etc.
   - Assess if pattern or one-time

5. **Update Totals**
   - Recalculate total spent to date
   - Add committed (not yet paid) amounts
   - Calculate remaining budget
   - Check contingency usage
   - Update completion forecast

6. **Check Status**
   - Are we on track with budget?
   - Any concerning trends?
   - Do we need to cut scope?
   - Should we tap contingency?

7. **Communicate if Needed**
   - Inform stakeholders of significant overages
   - Discuss options if trending over budget
   - Update decision-makers on financial status

## Output Location
- `.claude/context/budget-tracker.md` - Update with transaction
- `.claude/context/progress-log.md` - Reference budget changes
- May create new tasks if budget issues need addressing

## Example Usage

```
/update-budget

User provides:
> Paid ABC Plumbing $2,400 for rough plumbing work. Invoice #1234.
> Originally estimated $2,200.

Claude:
1. Records in budget tracker:
   - Line item: Plumbing Labor
   - Estimated: $2,200
   - Actual: $2,400
   - Variance: +$200 (9%)
   - Status: Paid
   - Receipt: Invoice #1234
2. Asks for reason if variance significant
3. Updates total spent
4. Recalculates remaining budget
5. Notes variance reason (if provided): "Additional shutoff valves required by code"
6. Checks overall budget health
```

## Budget Update Template

```markdown
## Budget Update - [Date]

### Transaction
- **Vendor:** [Who was paid]
- **Amount:** $[Amount]
- **Date:** [Payment date]
- **Invoice/Receipt:** [Number or reference]
- **Payment Method:** [Check, card, cash]
- **Description:** [What this was for]

### Budget Impact
- **Line Item:** [Budget category]
- **Estimated:** $[Original estimate]
- **Actual:** $[What you paid]
- **Variance:** +/- $[Difference] ([%])
- **Status:** [Updated status]

### Variance Reason
[Why actual differed from estimate if significant]

### Updated Budget Status
- **Total Budget:** $[Project budget]
- **Spent to Date:** $[Sum of actual costs]
- **Committed (unpaid):** $[Contracted but not yet paid]
- **Remaining:** $[Budget - spent - committed]
- **Contingency Used:** $[Amount] of $[Total contingency]
- **On Track:** [Yes/No - explain if no]

### Forecast
- **Projected Final Cost:** $[Estimate based on trends]
- **Expected Variance:** +/- $[Amount] ([%])

### Action Items
- [ ] [Any needed budget adjustments]
- [ ] [Scope cuts if over budget]
- [ ] [Stakeholder communication if needed]
```

## Budget Tracker Structure

The budget tracker should include:

### Header Section
- Project name and date
- Total budget
- Contingency amount and percentage
- Key assumptions

### Line Item Table

| Line Item | Category | Estimated | Quoted | Actual | Variance | Variance % | Status | Notes |
|-----------|----------|-----------|--------|--------|----------|------------|--------|-------|
| [Item name] | [Labor/Materials/Services/etc] | $[Est] | $[Quote] | $[Actual] | +/- $[Diff] | [%] | [Status] | [Reason for variance] |

### Summary Section
- Total estimated
- Total spent
- Total committed
- Remaining budget
- Contingency usage
- Projected final cost

### Status Values
- **Estimated** - Rough guess, not yet quoted
- **Quoted** - Formal quote received
- **Committed** - Contract signed or order placed
- **Paid** - Payment processed
- **Complete** - No further costs expected for this item

## Transaction Recording Best Practices

1. **Record immediately** - Don't wait, you'll forget details

2. **Keep receipts** - Digital photos or physical filed
   - Save in `documents/receipts/YYYY-MM-DD-vendor-description.pdf`

3. **Include all costs** - Don't forget:
   - Tax and fees
   - Delivery charges
   - Tips for service
   - Return trip expenses

4. **Categorize accurately** - Assign to correct line item for tracking

5. **Note variances** - Explain why actual differed from estimate

6. **Update status** - Move from Estimated → Quoted → Committed → Paid

7. **Check patterns** - Regular review catches trends early

## Common Variance Reasons

**Over Budget:**
- Scope creep ("while we're at it")
- Underestimated complexity
- Market price increase
- Discovered issues (damage, code)
- Change orders
- Mistakes requiring rework
- Upgrade decisions
- Forgot to include items

**Under Budget:**
- Found sale or discount
- Negotiated better price
- Simpler than expected
- Overestimated initially
- Did yourself instead of hiring
- Used existing materials
- Skipped nice-to-haves

## Budget Health Indicators

### Green (On Track)
- Spending matches estimates (±10%)
- Contingency mostly unused
- Trending to finish on budget
- No concerning patterns

### Yellow (Caution)
- Some items over budget (10-20%)
- Using contingency as expected
- May finish slightly over budget
- Need to watch closely

### Red (Concern)
- Multiple items significantly over (>20%)
- Contingency depleted
- Trending well over budget
- Need corrective action

## Corrective Actions When Over Budget

### Option 1: Use Contingency
- **Best for:** Unexpected but necessary costs
- **Pros:** Designed for this purpose
- **Cons:** Safety net is gone

### Option 2: Cut Scope
- **Best for:** Nice-to-haves that can wait
- **Pros:** Stays within budget
- **Cons:** Less complete project
- **Examples:** Fewer fixtures, simpler materials, smaller scope

### Option 3: Find Savings Elsewhere
- **Best for:** When some items came in under budget
- **Pros:** Keep full scope
- **Cons:** May compromise on something
- **Examples:** DIY instead of hire, shop sales, downgrade finishes

### Option 4: Add Funds
- **Best for:** When project value justifies it
- **Pros:** Get what you want
- **Cons:** Spending more than planned
- **Caution:** Understand why over budget first

### Option 5: Phase the Work
- **Best for:** When timeline is flexible
- **Pros:** Complete in stages as funds available
- **Cons:** Living with incomplete project
- **Examples:** Do essentials now, nice-to-haves later

## Reporting

### Weekly Budget Check (During Execution)

```markdown
## Budget Status - Week of [Date]

**Spending This Week:** $[Amount]
- [Vendor]: $[Amount]
- [Vendor]: $[Amount]

**Cumulative Status:**
- Spent: $[X] ([%] of budget)
- Remaining: $[Y]
- Contingency: $[Z] available

**Trending:** [On track / Slightly over / Significantly over]

**Concerns:** [Any issues to watch]
```

### Milestone Budget Review

```markdown
## Budget Review - [Milestone Name]

**Budget Performance:**
- Original budget: $[Amount]
- Spent through this milestone: $[Amount]
- Expected spend: $[Amount]
- Variance: +/- $[Amount] ([%])

**Major Variances:**
1. [Line item] - +/- $[Amount] - [Reason]
2. [Line item] - +/- $[Amount] - [Reason]

**Forecast to Completion:**
- Projected final cost: $[Amount]
- Expected final variance: +/- $[Amount]
- Confidence: [High/Medium/Low]

**Actions Required:**
- [Any budget adjustments needed]
```

### Final Budget Reconciliation

At project completion:

```markdown
## Final Budget Reconciliation

**Original Budget:** $[Amount]
**Contingency:** $[Amount] ([%])
**Available:** $[Original - Contingency]

**Final Costs:** $[Actual total]
**Variance:** +/- $[Amount] ([%])

**Status:** [Under budget / On budget / Over budget]

**Top Variances:**
1. [Item] - +/- $[Amount] - [Reason]
2. [Item] - +/- $[Amount] - [Reason]
3. [Item] - +/- $[Amount] - [Reason]

**Lessons Learned:**
- [What to estimate differently next time]
- [Where to build in more contingency]
- [What was well-estimated]

**By Category:**
- Labor: $[Amount] ([% of total])
- Materials: $[Amount] ([% of total])
- Services: $[Amount] ([% of total])
- Contingency used: $[Amount] ([% of total])
```

## Tips for Budget Success

1. **Be realistic in estimates** - Research actual costs, don't guess low

2. **Include everything** - Tax, delivery, disposal, tools, trips

3. **Build in contingency** - 15-30% for most projects

4. **Track as you go** - Real-time updates catch problems early

5. **Keep receipts** - All of them, organize immediately

6. **Review regularly** - Weekly during active work

7. **Communicate early** - Tell stakeholders about budget issues promptly

8. **Learn and adjust** - Each project improves your estimating

## Integration with Other Commands

**With `/update-progress`:**
- Progress updates include budget changes
- Budget updates reference progress milestones

**With decisions:**
- Decision impacts reflected in budget
- Budget status informs decisions

**With `/compare-options`:**
- Budget constraints guide comparisons
- Chosen option updated in budget
