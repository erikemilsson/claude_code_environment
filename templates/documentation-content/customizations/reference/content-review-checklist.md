# Content Review Checklist

## Purpose

Comprehensive checklist for reviewing content quality, accuracy, completeness, and style. Use this checklist during self-review, peer review, technical review, and editorial review stages.

## How to Use This Checklist

1. **Select Relevant Sections**: Not all sections apply to all content types
2. **Check Items as You Review**: Mark items complete as you verify them
3. **Document Issues**: Note specific problems and their locations
4. **Prioritize**: Address critical issues first, then nice-to-haves
5. **Use for Training**: Share common issues with team to improve writing

---

## Self-Review Checklist (Author)

### Completeness

- [ ] All planned sections are written
- [ ] No placeholder text (TODO, TBD, FIXME, XXX)
- [ ] Introduction explains what content covers
- [ ] Conclusion or "Next Steps" section included
- [ ] All required prerequisites listed
- [ ] All necessary images/diagrams included
- [ ] All code examples complete and included
- [ ] All links added (no missing reference links)

### Code Examples

- [ ] All code examples tested and working
- [ ] Code examples use realistic variable/function names
- [ ] Code includes necessary imports/dependencies
- [ ] Code follows current best practices
- [ ] Code examples include comments where helpful
- [ ] Language specified for all code blocks
- [ ] Output shown for code that produces output
- [ ] Error handling included where appropriate

### Links and References

- [ ] All external links tested (no 404s)
- [ ] All internal links tested (no broken cross-references)
- [ ] Links use descriptive text (not "click here")
- [ ] External links open in new tab (if platform supports)
- [ ] Links to specific versions documented (e.g., /v2/docs not /docs)
- [ ] Archived content linked to archived versions

### Images and Media

- [ ] All images uploaded and accessible
- [ ] Image file names are descriptive
- [ ] Images optimized for web (< 500KB for screenshots)
- [ ] Alt text provided for all images
- [ ] Images show what's described in text
- [ ] Diagrams are clear and readable
- [ ] Videos have captions/transcripts (if applicable)
- [ ] Screenshots show current UI (not outdated)

### Metadata

- [ ] Page title is descriptive and unique
- [ ] Meta description written (if applicable)
- [ ] Tags/categories assigned
- [ ] Author name included
- [ ] Publication date set
- [ ] Last updated date accurate

---

## Style and Formatting Review

### Writing Style

- [ ] Voice matches style guide (formal/conversational)
- [ ] Tone appropriate for content type (tutorial/reference/etc.)
- [ ] Person consistent (second person "you" recommended)
- [ ] Active voice used (passive only where appropriate)
- [ ] Contractions match formality level
- [ ] Terminology consistent with glossary
- [ ] Jargon defined or avoided
- [ ] Acronyms spelled out on first use

### Grammar and Mechanics

- [ ] Spell check completed (no typos)
- [ ] Grammar check completed
- [ ] Punctuation correct (serial commas used)
- [ ] Capitalization consistent
- [ ] Numbers formatted correctly (spell out 1-9, use numerals for 10+)
- [ ] Dates formatted consistently
- [ ] No run-on sentences
- [ ] No sentence fragments (unless intentional)

### Headings

- [ ] Sentence case used (not Title Case)
- [ ] Heading hierarchy logical (no skipped levels)
- [ ] Headings descriptive and action-oriented
- [ ] Only one H1 per page (page title)
- [ ] Headings create clear content outline
- [ ] No deep nesting (avoid going beyond H4)

### Lists

- [ ] Bulleted lists for unordered items
- [ ] Numbered lists for sequential steps or priority
- [ ] Parallel structure maintained in lists
- [ ] Periods used consistently (all items or no items)
- [ ] Lists not excessively long (consider breaking up)

### Code and Technical Formatting

- [ ] Inline code (backticks) for functions, variables, file names
- [ ] Code blocks for multi-line code
- [ ] Language specified for syntax highlighting
- [ ] UI elements in bold (buttons, menu items)
- [ ] Keyboard shortcuts formatted consistently
- [ ] File paths formatted correctly
- [ ] Commands use proper syntax

### Tables

- [ ] Tables used appropriately (structured data)
- [ ] Headers clearly labeled
- [ ] Cells aligned properly
- [ ] Not too wide (readable on mobile)
- [ ] Alternative format for complex tables (lists, multiple tables)

---

## Technical Review Checklist

### Accuracy

- [ ] All technical statements are correct
- [ ] API details match current implementation
- [ ] Configuration values accurate
- [ ] Default values correct
- [ ] Version numbers current
- [ ] Deprecated features not recommended
- [ ] Product names spelled correctly
- [ ] Technical terms used correctly

### Completeness

- [ ] All necessary steps included
- [ ] Edge cases addressed
- [ ] Error scenarios covered
- [ ] Troubleshooting guidance provided
- [ ] Prerequisites clearly stated
- [ ] Required permissions documented
- [ ] Dependencies listed

### Best Practices

- [ ] Current best practices followed
- [ ] Security best practices included
- [ ] Performance considerations mentioned
- [ ] Scalability guidance provided (if relevant)
- [ ] Common pitfalls warned against
- [ ] Anti-patterns called out
- [ ] Recommended approaches highlighted

### Code Quality

- [ ] Code follows language conventions
- [ ] Code is production-ready (not just PoC)
- [ ] Error handling included
- [ ] Security vulnerabilities avoided (no SQL injection, XSS, etc.)
- [ ] Code is efficient (no obvious performance issues)
- [ ] Code includes logging where appropriate
- [ ] Code is testable

### Testing and Validation

- [ ] All code examples tested in target environment
- [ ] All procedures tested step-by-step
- [ ] API calls tested with actual API
- [ ] Commands tested in actual terminal
- [ ] Error messages verified as accurate
- [ ] Screenshots match current UI
- [ ] Links to external resources verified

---

## Audience and Usability Review

### Target Audience

- [ ] Appropriate for stated audience level
- [ ] Assumptions about prior knowledge stated
- [ ] Technical depth matches audience
- [ ] Examples relevant to audience's use cases
- [ ] Prerequisites match audience's likely setup

### Clarity

- [ ] Content is easy to understand
- [ ] Complex concepts explained clearly
- [ ] Ambiguous statements clarified
- [ ] Technical terms defined
- [ ] Examples illustrate points effectively
- [ ] Step-by-step instructions are clear

### Structure and Flow

- [ ] Logical progression of ideas
- [ ] Smooth transitions between sections
- [ ] Content organized for scanning
- [ ] Related information grouped together
- [ ] No repetition (or intentional for emphasis)
- [ ] Build up from simple to complex

### Readability

- [ ] Paragraphs not too long (3-5 sentences)
- [ ] Sentences not too long (< 25 words ideal)
- [ ] Readability score appropriate (Hemingway grade level)
- [ ] Whitespace used effectively
- [ ] Visual breaks between sections
- [ ] Not too dense (mix of text, lists, code, images)

### Scannability

- [ ] Headings create clear outline
- [ ] Lists break up dense text
- [ ] Important information highlighted
- [ ] Code examples clearly labeled
- [ ] Key takeaways easy to spot
- [ ] Table of contents provided (for long content)

---

## Accessibility Review

### Screen Reader Compatibility

- [ ] Heading hierarchy supports navigation
- [ ] Links have descriptive text
- [ ] Images have meaningful alt text
- [ ] Tables have proper headers
- [ ] Lists properly marked up
- [ ] Code blocks properly labeled

### Visual Accessibility

- [ ] Color not sole means of conveying information
- [ ] Sufficient contrast for text
- [ ] Text resizable without breaking layout
- [ ] Images include text descriptions
- [ ] Diagrams have text equivalents

### Language and Inclusion

- [ ] Gender-neutral language used
- [ ] Inclusive examples (diverse names, scenarios)
- [ ] Ableist language avoided
- [ ] Cultural assumptions avoided
- [ ] Idioms explained or avoided (for non-native speakers)

---

## SEO and Discoverability Review

### Search Optimization

- [ ] Page title includes target keywords
- [ ] Meta description compelling and keyword-rich
- [ ] Headings include relevant keywords
- [ ] First paragraph includes main topic
- [ ] Internal links to related content
- [ ] Image alt text includes keywords (where natural)

### Navigation

- [ ] Content findable from main navigation
- [ ] Breadcrumbs show location (if applicable)
- [ ] Related content linked
- [ ] "See Also" section included
- [ ] Back links from new to existing content

### Search Engine Considerations

- [ ] URL slug descriptive and readable
- [ ] Canonical URL set (if applicable)
- [ ] No duplicate content
- [ ] Proper use of noindex/nofollow (if needed)

---

## Content Type Specific Checklists

### Tutorial Checklist

- [ ] Clear learning objectives stated
- [ ] Prerequisites listed
- [ ] Estimated time to complete provided
- [ ] Step-by-step instructions included
- [ ] Each step has expected outcome
- [ ] Troubleshooting section included
- [ ] "What's Next" conclusion provided
- [ ] Complete working example at end

### How-To Guide Checklist

- [ ] Goal clearly stated upfront
- [ ] Prerequisites listed
- [ ] Steps numbered sequentially
- [ ] Each step is a clear action
- [ ] Verification step included
- [ ] Common issues addressed
- [ ] Links to related guides provided

### API Reference Checklist

- [ ] Endpoint/function name clear
- [ ] HTTP method specified (for REST APIs)
- [ ] Authentication requirements stated
- [ ] All parameters documented (name, type, required, default)
- [ ] Request body schema shown
- [ ] Response schema shown
- [ ] Success response example included
- [ ] Error responses documented
- [ ] Rate limiting information provided
- [ ] Code examples in multiple languages
- [ ] Changelog included

### Conceptual/Explanation Checklist

- [ ] Concept defined clearly
- [ ] "Why it matters" explained
- [ ] How it works explained
- [ ] Use cases provided
- [ ] Benefits and tradeoffs discussed
- [ ] Diagrams or illustrations included
- [ ] Examples demonstrate concept
- [ ] Links to practical guides provided

### Troubleshooting Guide Checklist

- [ ] Issues organized by symptom
- [ ] Each issue has clear symptoms
- [ ] Causes explained
- [ ] Solutions step-by-step
- [ ] Multiple solutions provided where applicable
- [ ] Diagnostic commands shown
- [ ] When to contact support clarified

### Release Notes Checklist

- [ ] Version number and date clear
- [ ] Changes categorized (new, improved, fixed, breaking, deprecated)
- [ ] Breaking changes highlighted
- [ ] Migration guide provided for breaking changes
- [ ] Security updates noted
- [ ] Deprecation timeline stated
- [ ] Download links included
- [ ] Upgrade instructions provided

---

## Legal and Compliance Review

### Licensing and Attribution

- [ ] Code examples include license info (if required)
- [ ] External sources cited
- [ ] Quotes attributed
- [ ] Images properly licensed
- [ ] Trademark usage correct
- [ ] Copyright notices included (if needed)

### Legal Language

- [ ] No legal claims without approval
- [ ] Disclaimers included where needed
- [ ] Terms like "guarantee" used carefully
- [ ] Competitive comparisons factual and fair
- [ ] Privacy implications explained
- [ ] GDPR/compliance requirements addressed (if applicable)

### Security and Privacy

- [ ] No credentials or keys in examples
- [ ] No PII (personally identifiable information) in examples
- [ ] Security warnings included where appropriate
- [ ] Privacy best practices followed
- [ ] Vulnerability disclosure handled properly

---

## Pre-Publication Final Check

### Last Look

- [ ] Final spell check
- [ ] Final link check
- [ ] All reviewer comments addressed
- [ ] Approval from required reviewers received
- [ ] Publication date confirmed
- [ ] Promotion plan ready

### Production Readiness

- [ ] Content renders correctly in production
- [ ] No formatting issues in published version
- [ ] Images load correctly
- [ ] Code blocks render with syntax highlighting
- [ ] Mobile view acceptable
- [ ] Page speed acceptable

---

## Common Issues to Watch For

### Frequent Mistakes

- [ ] "It's" vs "its" (it's = it is, its = possessive)
- [ ] "Their" vs "they're" vs "there"
- [ ] "Your" vs "you're"
- [ ] "Then" vs "than"
- [ ] Inconsistent tense (pick present or past and stick with it)
- [ ] Missing articles (a, an, the)
- [ ] Comma splices (two independent clauses joined with comma)

### Technical Writing Pitfalls

- [ ] Assuming too much knowledge
- [ ] Skipping error cases
- [ ] Not testing code examples
- [ ] Outdated screenshots
- [ ] Broken links to external resources
- [ ] Missing prerequisites
- [ ] Inconsistent terminology
- [ ] Jargon without definition

---

## Issue Tracking Template

When you find issues during review, document them:

**Issue Template**:
```
Location: [Section/line number]
Issue Type: [Technical/Style/Grammar/etc.]
Severity: [Critical/High/Medium/Low]
Description: [What's wrong]
Suggestion: [How to fix]
```

**Example**:
```
Location: "Authentication" section, step 3
Issue Type: Technical accuracy
Severity: High
Description: The default timeout is 30 seconds, not 60 seconds
Suggestion: Change "after 60 seconds" to "after 30 seconds"
```

---

## Review Sign-Off Template

After completing review:

```
Content: [File name or title]
Review Type: [Self/Peer/Technical/Editorial]
Reviewer: [Name]
Date: [Date]
Status: [Approved / Changes Requested]

Summary:
[Brief summary of review findings]

Issues Found: [Count by severity]
- Critical: 0
- High: 2
- Medium: 5
- Low: 3

Next Steps:
[What author should do next]
```

---

## Continuous Improvement

### Learn from Reviews

After each review cycle:
1. Track common issues
2. Update style guide to address patterns
3. Create examples for confusing areas
4. Improve templates to prevent issues
5. Share learnings with team

### Measure Quality

Track these metrics:
- Issues found per review type
- Time spent in review per content type
- Revision cycles needed
- Post-publication issues reported
- User satisfaction with content

### Update Checklist

Periodically review and update this checklist:
- Add new items based on common issues
- Remove items that are always passing
- Reorganize for better flow
- Adjust for new content types
- Incorporate feedback from reviewers
