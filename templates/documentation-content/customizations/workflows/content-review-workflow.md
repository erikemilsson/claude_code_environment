# Content Review Workflow

## Purpose

Multi-stage content review process to ensure quality, accuracy, technical correctness, and consistency before publication.

## Context Required

- Content file path or draft location
- Content type (tutorial, API docs, blog post, etc.)
- Target publication date (if applicable)
- Author information

## Review Stages

### Stage 1: Self-Review (Author)

**Before submitting for review, the author should complete**:

1. **Content Checklist**:
   - [ ] All sections complete (no placeholders like "TODO" or "TBD")
   - [ ] Code examples tested and working
   - [ ] Links verified (no broken links)
   - [ ] Images included with alt text
   - [ ] Spell check completed

2. **Style Conformance**:
   - [ ] Follows writing style guide (voice, tone, person)
   - [ ] Uses consistent terminology from glossary
   - [ ] Headings use sentence case
   - [ ] Lists have parallel structure
   - [ ] Code elements properly formatted

3. **Structure Verification**:
   - [ ] Follows appropriate documentation structure pattern
   - [ ] Clear introduction and conclusion
   - [ ] Logical flow between sections
   - [ ] Headings create clear hierarchy

**Action**: Create pull request or share draft link when self-review complete.

---

### Stage 2: Peer Review (Optional for Small Teams)

**Reviewer**: Another content author or team member

**Focus Areas**:
1. **Clarity**: Is the content understandable?
2. **Completeness**: Are there gaps or missing information?
3. **Flow**: Does the content progress logically?
4. **Examples**: Are examples helpful and clear?

**Process**:
1. Read through entire document
2. Add inline comments for issues
3. Provide summary feedback
4. Suggest changes or ask questions

**Timeline**: 1-2 business days

**Acceptance Criteria**:
- [ ] Feedback addressed or discussed
- [ ] Major concerns resolved
- [ ] Content ready for technical review

---

### Stage 3: Technical Review (Required for Technical Content)

**Reviewer**: Subject matter expert, engineer, or product manager

**Focus Areas**:
1. **Accuracy**: Are all technical details correct?
2. **Completeness**: Is critical information missing?
3. **Best Practices**: Does content follow current best practices?
4. **Security**: Are there security concerns or vulnerabilities shown?
5. **Code Examples**: Do all code examples work correctly?

**Review Checklist**:
- [ ] Technical accuracy verified
- [ ] Code examples tested in actual environment
- [ ] API details match current implementation
- [ ] Configuration values are correct
- [ ] Security best practices followed
- [ ] No deprecated features recommended
- [ ] Version information is accurate
- [ ] Error handling shown correctly

**Process**:
1. Review for technical correctness
2. Test all code examples
3. Verify against current product/API version
4. Add comments for corrections needed
5. Approve or request changes

**Timeline**: 2-3 business days

**Acceptance Criteria**:
- [ ] All technical issues resolved
- [ ] Code examples verified working
- [ ] Technical reviewer approves content
- [ ] Product version verified

---

### Stage 4: Editorial Review (Required for External Content)

**Reviewer**: Editor or senior content person

**Focus Areas**:
1. **Style Consistency**: Matches style guide
2. **Grammar and Spelling**: Error-free writing
3. **Readability**: Appropriate for target audience
4. **Tone**: Matches brand voice
5. **Formatting**: Consistent with other content

**Review Checklist**:
- [ ] Grammar and spelling correct
- [ ] Style guide adherence (voice, tone, person)
- [ ] Terminology consistent with glossary
- [ ] Formatting consistent (headings, lists, code blocks)
- [ ] Readability appropriate for audience
- [ ] No jargon without definitions
- [ ] Inclusive language used
- [ ] Links use descriptive text
- [ ] Images have alt text

**Process**:
1. Review for style and grammar
2. Check consistency with other published content
3. Verify readability for target audience
4. Make minor edits or suggest revisions
5. Approve or request changes

**Timeline**: 1-2 business days

**Acceptance Criteria**:
- [ ] Grammar and style issues resolved
- [ ] Consistent with published content
- [ ] Readability verified
- [ ] Editorial reviewer approves

---

### Stage 5: Legal/Compliance Review (If Required)

**Reviewer**: Legal or compliance team

**When Required**:
- Content about licensing, terms, or legal topics
- Security or privacy-related content
- Regulatory compliance documentation
- Content with external quotes or attributions
- Marketing claims or competitive comparisons

**Focus Areas**:
1. **Legal Accuracy**: Legal statements are correct
2. **Compliance**: Meets regulatory requirements
3. **Risk**: No potential legal liabilities
4. **Attributions**: Proper citations and permissions

**Timeline**: 3-5 business days (schedule early)

**Acceptance Criteria**:
- [ ] Legal review complete
- [ ] Compliance requirements met
- [ ] Necessary disclaimers added
- [ ] Legal team approves

---

### Stage 6: Final Approval

**Approver**: Content lead or project owner

**Final Checks**:
- [ ] All review stages completed
- [ ] All feedback addressed
- [ ] No outstanding blockers
- [ ] Publication plan confirmed
- [ ] Promotion plan ready (if applicable)

**Action**: Approve for publication.

---

## Process Flow

```
Author Self-Review
        ↓
    [Ready?] → No → Continue editing
        ↓ Yes
Peer Review (optional)
        ↓
    [Approved?] → No → Revise and resubmit
        ↓ Yes
Technical Review
        ↓
    [Approved?] → No → Revise and resubmit
        ↓ Yes
Editorial Review
        ↓
    [Approved?] → No → Revise and resubmit
        ↓ Yes
Legal Review (if needed)
        ↓
    [Approved?] → No → Revise and resubmit
        ↓ Yes
Final Approval
        ↓
    Publish
```

## Workflow Variants

### Fast Track (Internal Docs, Minor Updates)

For low-risk content:
1. Self-review
2. Peer review (optional)
3. Publish

**Use when**:
- Internal documentation
- Minor corrections to existing content
- Non-technical content updates

---

### Standard Review (Most External Content)

For typical documentation:
1. Self-review
2. Technical review
3. Editorial review
4. Final approval
5. Publish

**Use when**:
- New tutorials or guides
- API documentation
- Feature documentation
- Blog posts

---

### Full Review (High-Risk Content)

For sensitive or critical content:
1. Self-review
2. Peer review
3. Technical review
4. Editorial review
5. Legal/compliance review
6. Final approval
7. Publish

**Use when**:
- Legal or compliance topics
- Security documentation
- Public announcements
- Content with legal implications

---

## Using This Workflow

### As a Command

This file is designed to be used as a `.claude/commands/review-content.md` command.

**Usage**:
```
/review-content [file-path] [stage]
```

**Examples**:
```
/review-content docs/tutorials/getting-started.md technical
/review-content blog/2024-01-15-new-features.md editorial
/review-content api-reference/authentication.md all
```

### Implementation Steps

1. **Copy to project**: Place this file in `.claude/commands/review-content.md`

2. **Customize stages**: Remove or add review stages based on your team

3. **Assign reviewers**: Document who performs each review type

4. **Set timelines**: Adjust timelines based on team size and workload

5. **Track in tasks**: Create review tasks in task management system

---

## Review Tools

### Inline Comments
- GitHub PR comments
- Google Docs comments
- Notion comments

### Checklists
- Use `.claude/reference/content-review-checklist.md`
- Create stage-specific checklists

### Automation
- Linting: Markdown linters, spell checkers
- Link checking: Automated broken link detection
- Code testing: Run code examples in CI/CD
- Style validation: Custom scripts for terminology checks

---

## Handling Feedback

### For Authors

**When receiving feedback**:
1. Read all feedback before responding
2. Ask clarifying questions if needed
3. Address each comment (fix or respond)
4. Mark comments as resolved
5. Request re-review if needed

**Managing disagreements**:
1. Provide rationale for your approach
2. Discuss with reviewer
3. Escalate to content lead if needed
4. Document final decision

### For Reviewers

**Providing effective feedback**:
1. Be specific (cite examples, suggest alternatives)
2. Explain the "why" behind suggestions
3. Distinguish between required changes and suggestions
4. Use positive tone (collaborative, not critical)
5. Acknowledge good work

**Example feedback**:
- ❌ Bad: "This is unclear"
- ✅ Good: "This section could be clearer. Consider adding an example showing how to configure the timeout parameter."

- ❌ Bad: "Wrong"
- ✅ Good: "The default value is 30 seconds, not 60. See config.py:45"

---

## Metrics and Improvement

### Track These Metrics

1. **Review Time**: Average days per stage
2. **Revision Rounds**: Number of back-and-forth cycles
3. **Issue Types**: Common problems found (technical errors, style issues, etc.)
4. **Blocker Rate**: How often content is blocked vs approved

### Use Metrics To

1. **Optimize Process**: Remove bottlenecks, adjust timelines
2. **Improve Writing**: Address common issues in style guide
3. **Train Team**: Focus training on frequent problem areas
4. **Set Expectations**: Realistic timelines based on historical data

---

## Output Location

**Review Status**: Update task JSON with review stage and feedback

**Feedback**: Track in:
- Pull request comments (GitHub)
- Document comments (Google Docs, Notion)
- Task notes

**Approval**: Update task status to "Finished" when all reviews complete

---

## Tips for Success

### For Authors
1. Complete thorough self-review to reduce revision rounds
2. Provide context when requesting review (audience, purpose, deadlines)
3. Address feedback promptly
4. Ask questions when feedback is unclear
5. Learn from common feedback to improve future content

### For Reviewers
1. Review within expected timeline
2. Provide specific, actionable feedback
3. Balance thoroughness with pragmatism
4. Approve when "good enough" (don't let perfect be enemy of done)
5. Celebrate good work

### For Teams
1. Schedule reviews during content planning
2. Account for review time in timelines
3. Have backup reviewers for critical paths
4. Document common issues to prevent repetition
5. Continuously improve the review process
