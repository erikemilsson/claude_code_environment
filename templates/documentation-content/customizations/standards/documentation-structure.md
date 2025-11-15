# Documentation Structure Patterns

## Purpose

This guide provides structural templates for different types of documentation. Using consistent patterns helps readers know what to expect and makes content easier to scan, understand, and maintain.

## Document Types

### Tutorial

**Goal**: Teach a beginner how to accomplish a specific task through hands-on learning.

**Characteristics**:
- Learning-oriented
- Assumes minimal prior knowledge
- Provides step-by-step instructions
- Includes explanations of concepts along the way
- Results in a working example

**Structure**:

```markdown
# [Tutorial Title]

## Overview
- What you'll build or learn
- Who this tutorial is for
- What you'll need (prerequisites)
- Estimated time to complete

## Prerequisites
- Required knowledge
- Required software/tools
- Required accounts or access

## What You'll Learn
- Bullet list of learning objectives
- Skills or concepts covered

## Step 1: [Action]
- Clear instruction
- Code example or screenshot
- Explanation of what's happening
- Expected result

## Step 2: [Action]
[Repeat pattern]

## Step 3: [Action]
[Repeat pattern]

## Conclusion
- Summary of what was accomplished
- What to do next
- Links to related tutorials or advanced topics

## Troubleshooting
- Common issues and solutions
- Where to get help

## Complete Code
- Full working example
- Link to repository if applicable
```

**Example Titles**:
- "Build Your First REST API with Python"
- "Create a Real-Time Dashboard with React"
- "Deploy a Machine Learning Model to Production"

**Writing Tips**:
- Use second person ("you will", "your application")
- Explain why you're doing each step
- Test every step with a beginner's mindset
- Include screenshots for UI-heavy tutorials
- Provide checkpoint validation ("You should now see...")

---

### How-To Guide

**Goal**: Help someone accomplish a specific task who already has basic knowledge.

**Characteristics**:
- Task-oriented
- Assumes some familiarity with the system
- Focused on achieving a specific goal
- Provides clear, sequential steps
- Minimal conceptual explanation

**Structure**:

```markdown
# How to [Accomplish Task]

## Overview
Brief description of what this guide covers and when to use it.

## Prerequisites
- What you need before starting
- Links to setup guides if needed

## Steps

### 1. [First Action]
Clear instruction with code example or command.

### 2. [Second Action]
Clear instruction with code example or command.

### 3. [Third Action]
Clear instruction with code example or command.

## Verification
How to confirm the task was completed successfully.

## Next Steps
- What to do after completing this task
- Links to related how-to guides

## Troubleshooting
- Common issues
- Quick fixes
```

**Example Titles**:
- "How to Configure Environment Variables"
- "How to Enable Two-Factor Authentication"
- "How to Export Data to CSV"

**Writing Tips**:
- Get straight to the steps (minimal introduction)
- Use imperative mood ("Click Save", "Run the command")
- One clear action per step
- Show expected output
- Link to concepts/reference for more detail

---

### Reference Documentation

**Goal**: Provide complete, accurate information about a specific feature, API, or component.

**Characteristics**:
- Information-oriented
- Comprehensive and precise
- Organized for lookup, not reading start-to-finish
- Dry, factual tone
- Includes all parameters, options, return values

**Structure**:

```markdown
# [Feature/Component/Function Name]

## Overview
Brief description of what this is and what it does.

## Syntax
```language
code_signature_or_usage_pattern
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `param1`  | string | Yes | - | Description |
| `param2`  | number | No | 0 | Description |

## Return Value
What this returns, including type and possible values.

## Examples

### Basic Usage
```language
simple_example
```

### Advanced Usage
```language
complex_example
```

## Errors

| Error Code | Description | Resolution |
|------------|-------------|------------|
| ERR_001 | Error description | How to fix |

## See Also
- Links to related reference pages
- Links to conceptual documentation
- Links to how-to guides
```

**Example Titles**:
- "Authentication API Reference"
- "`calculate_metrics()` Function Reference"
- "Configuration File Reference"

**Writing Tips**:
- Use tables for structured information
- Be exhaustive (document everything)
- Use consistent parameter order
- Include type information
- Test all examples
- Use neutral, precise language

---

### Conceptual/Explanation

**Goal**: Explain a concept, design decision, or how something works.

**Characteristics**:
- Understanding-oriented
- Provides context and background
- Explains "why" not just "how"
- May include diagrams or illustrations
- Connects to bigger picture

**Structure**:

```markdown
# [Concept Name]

## Introduction
What is this concept and why does it matter?

## Background
- Historical context if relevant
- Problem this concept solves
- Alternative approaches

## How It Works

### [Aspect 1]
Explanation with diagrams or examples.

### [Aspect 2]
Explanation with diagrams or examples.

### [Aspect 3]
Explanation with diagrams or examples.

## Use Cases
When and why to use this concept.

## Benefits and Tradeoffs

**Benefits**:
- Advantage 1
- Advantage 2

**Tradeoffs**:
- Consideration 1
- Consideration 2

## Best Practices
- Recommendation 1
- Recommendation 2

## Common Misconceptions
- Misconception 1: [Explanation of truth]
- Misconception 2: [Explanation of truth]

## Examples in Practice
Real-world scenarios or code examples.

## Related Concepts
- Link to related explanations
- Link to tutorials using this concept
```

**Example Titles**:
- "Understanding Database Transactions"
- "The Authentication Flow Explained"
- "How Caching Works"

**Writing Tips**:
- Start with what the reader likely already knows
- Use analogies for complex concepts
- Include diagrams (architecture, flows, relationships)
- Explain both what and why
- Address common misunderstandings
- Link to practical guides

---

### API Documentation

**Goal**: Document an API endpoint completely and precisely.

**Structure**:

```markdown
# [HTTP Method] [Endpoint Path]

## Description
What this endpoint does in one or two sentences.

## Endpoint
```
[METHOD] /api/v1/resource/{id}
```

## Authentication
Required authentication method (API key, OAuth, etc.)

## Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Resource identifier |

## Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter` | string | No | null | Filter criteria |
| `limit` | integer | No | 10 | Max results |

## Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | Bearer token |
| `Content-Type` | Yes | Must be `application/json` |

## Request Body

```json
{
  "field1": "value",
  "field2": 123
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field1` | string | Yes | Description |
| `field2` | integer | No | Description |

## Response

### Success Response (200 OK)

```json
{
  "id": "123",
  "status": "success",
  "data": {}
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Resource ID |
| `status` | string | Operation status |
| `data` | object | Response data |

### Error Responses

#### 400 Bad Request
```json
{
  "error": "Invalid parameter",
  "message": "The 'id' parameter is required"
}
```

#### 401 Unauthorized
```json
{
  "error": "Authentication failed",
  "message": "Invalid or expired token"
}
```

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "No resource found with id '123'"
}
```

## Code Examples

### cURL
```bash
curl -X POST https://api.example.com/v1/resource \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field1": "value"}'
```

### Python
```python
import requests

response = requests.post(
    "https://api.example.com/v1/resource",
    headers={
        "Authorization": "Bearer YOUR_TOKEN",
        "Content-Type": "application/json"
    },
    json={"field1": "value"}
)
```

### JavaScript
```javascript
fetch('https://api.example.com/v1/resource', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({field1: 'value'})
})
.then(response => response.json())
.then(data => console.log(data));
```

## Rate Limiting
- Limits: 100 requests per minute
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Changelog
- v1.1 (2024-01-15): Added `filter` parameter
- v1.0 (2023-12-01): Initial release

## See Also
- Related endpoints
- Authentication guide
- Rate limiting documentation
```

**Writing Tips**:
- Be exhaustive and precise
- Show request and response examples
- Document all possible error responses
- Include code examples in multiple languages
- Test all examples before publishing
- Keep format consistent across all endpoints

---

### Troubleshooting Guide

**Goal**: Help users diagnose and fix problems.

**Structure**:

```markdown
# Troubleshooting [Feature/Component]

## Overview
Common issues and solutions for [feature].

## Quick Diagnostics

Run these commands to gather information:
```bash
command to check status
command to view logs
```

## Common Issues

### Issue: [Problem Description]

**Symptoms**:
- What the user sees or experiences
- Error messages

**Causes**:
- Possible reason 1
- Possible reason 2

**Solutions**:

#### Solution 1: [Description]
1. Step-by-step fix
2. Expected result

#### Solution 2: [Description]
1. Alternative fix
2. Expected result

---

### Issue: [Another Problem]
[Repeat pattern]

## Still Having Issues?

If none of the above solutions work:
1. Check [system status page]
2. Review [logs location]
3. Contact [support channel]

## Provide These Details

When reporting an issue, include:
- Version number
- Operating system
- Steps to reproduce
- Error messages
- Relevant logs
```

**Writing Tips**:
- Organize by symptom, not cause
- Start with most common issues
- Provide multiple solutions when applicable
- Show how to gather diagnostic information
- Link to detailed documentation

---

### Release Notes

**Goal**: Inform users about changes in a new version.

**Structure**:

```markdown
# Release Notes - Version X.Y.Z

Released: YYYY-MM-DD

## Overview
Brief summary of this release (major features, focus areas).

## New Features

### Feature Name
Description of what it does and why it's valuable.

**How to Use**:
Quick example or link to documentation.

---

## Improvements

### Improvement Name
What was improved and the impact.

---

## Bug Fixes

### Fixed: [Issue Description]
- **Issue**: What was broken
- **Impact**: Who was affected
- **Resolution**: How it's fixed

---

## Breaking Changes

### Change Description
- **What Changed**: Technical details
- **Migration Required**: Yes/No
- **Migration Guide**: Link or steps

---

## Deprecations

### Deprecated Feature
- **Reason**: Why it's being deprecated
- **Timeline**: When it will be removed
- **Alternative**: What to use instead
- **Migration Guide**: Link

---

## Security Updates

### Security Fix [CVE if applicable]
- **Severity**: Critical/High/Medium/Low
- **Impact**: What was vulnerable
- **Action Required**: What users must do

---

## Known Issues

### Issue Description
- **Impact**: Who is affected
- **Workaround**: Temporary solution
- **Status**: Timeline for fix

---

## Upgrade Instructions

1. Step-by-step upgrade process
2. Verification steps
3. Rollback procedure if needed

## Download

- Download links
- Checksums for verification

## Thank You

Credits to contributors, acknowledgments.
```

**Writing Tips**:
- Lead with most important changes
- Be specific about breaking changes
- Provide migration guides for major changes
- Include version compatibility information
- Link to detailed documentation

---

## Choosing the Right Structure

Use this decision tree:

**Is the reader learning for the first time?**
- Yes → Tutorial

**Does the reader have basic knowledge and need to complete a task?**
- Yes → How-To Guide

**Does the reader need to understand a concept?**
- Yes → Conceptual/Explanation

**Does the reader need to look up specific details?**
- Yes → Reference

**Does the reader have a problem?**
- Yes → Troubleshooting

**Is this about a new version?**
- Yes → Release Notes

## Cross-Referencing

Connect different document types:

- **Tutorials** → Link to reference docs for details, conceptual docs for background
- **How-To Guides** → Link to tutorials for beginners, reference for parameters
- **Reference** → Link to tutorials and how-tos for practical usage
- **Conceptual** → Link to tutorials for hands-on learning, reference for details

## Content Reuse

Avoid duplicating information across documents:

- Put detailed parameter info in reference docs only
- Link to reference from tutorials and how-tos
- Put conceptual explanations in one place
- Use includes/snippets if your platform supports them

## Maintenance

Keep structures current:

- Review and update templates quarterly
- Gather feedback from users and authors
- Adjust based on analytics (high-bounce sections, search queries)
- Update examples with current best practices

## Customization

Adapt these patterns for your project:

1. **Add Domain-Specific Sections**: Include sections unique to your product
2. **Adjust Formality**: Match your organization's voice
3. **Simplify for Smaller Projects**: Use lighter-weight versions
4. **Add Required Sections**: Legal disclaimers, compliance notes, etc.
5. **Create Templates**: Turn these into actual template files to copy
