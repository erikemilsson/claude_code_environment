# LLM Pitfalls Checklist Template

Use this template to document common mistakes for your specific domain.

---

# LLM Pitfalls: [Project/Domain Name]

**Purpose**: Document common mistakes LLMs make in this domain. Claude must treat this as a **MANDATORY CHECKLIST** before implementing key features.

**Last Updated:** [Date]

---

## How to Use This Document

Before implementing ANY [domain-specific feature]:

1. Read this document completely
2. Check each pitfall against your implementation
3. If you identify a pitfall, STOP and flag it
4. Document your check in code comments

---

## General Pitfalls

### 1. [Pitfall Name]

**Problem:** [What causes this mistake]

**LLM Behavior:** [How the LLM typically gets it wrong]

**Required Action:**
- [Specific step to avoid]
- [Another step]

**Example:**
```
// BAD - [Why it's wrong]
[Bad code example]

// GOOD - [Why it's correct]
[Good code example]
```

---

### 2. [Another Pitfall]

**Problem:** [Description]

**LLM Behavior:** [Common mistake pattern]

**Required Action:**
- [Steps to avoid]

**Example:**
```
// BAD
[Example]

// GOOD
[Example]
```

---

## Domain-Specific Pitfalls

### [Domain Area] Pitfalls

#### 3. [Specific Pitfall]

**Problem:** [Specific to this domain]

**LLM Behavior:** [How it manifests]

**Required Action:**
- [Specific steps]

---

## Pre-Implementation Checklist

Before implementing, verify:

- [ ] Have I checked assumptions.md for relevant decisions?
- [ ] Have I verified terminology in the glossary?
- [ ] Have I documented units for numerical values?
- [ ] Have I handled edge cases explicitly?
- [ ] Have I cross-referenced source documentation?
- [ ] [Add domain-specific checks]

---

## In-Code Validation Block

Add this to implementations:

```
// PITFALL CHECKLIST
// [x] Check 1: [What was verified]
// [x] Check 2: [What was verified]
// [x] Check 3: [What was verified]
// Source: [Reference document]
```

---

## When You Violate These Rules

If you find yourself about to violate any rule:

1. **STOP** implementation
2. **FLAG** the specific pitfall
3. **EXPLAIN** why you think the rule doesn't apply
4. **WAIT** for user confirmation

Example:
```
PITFALL FLAGGED: [Pitfall Name]

I'm about to [describe situation].

Per pitfall #[N], I should not [describe rule].

Please confirm: [Specific question]
Source reference: [Document section]
```

---

## Project-Specific Pitfalls

[Add pitfalls discovered during this project]

---

## Remember

This document exists because these mistakes are **common and costly**.

Taking 2 minutes to check this list can save hours of debugging.

When in doubt: **FLAG, DON'T GUESS**.
