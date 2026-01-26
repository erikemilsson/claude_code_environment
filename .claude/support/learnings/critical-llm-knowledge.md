# Critical LLM Knowledge

Rules and patterns where Claude consistently makes mistakes or needs explicit guidance.

## When to Use

Create this document when you notice Claude:
- Repeatedly makes the same error despite corrections
- Simplifies something that must stay complex
- Applies logic uniformly when it should vary
- Misinterprets domain-specific conventions

## Format

Number each rule. Keep entries scannable.

```markdown
## Rule N: [Short descriptive title]

**Symptom:** What Claude does wrong

**Correct behavior:** What should happen

**Why it's counterintuitive:** Why Claude gets confused

**Example:**
[Brief code/formula showing correct implementation]
```

## Common Categories

| Category | Example |
|----------|---------|
| **Special values** | "n/a" means no credit, not default to 1 |
| **Term-specific logic** | Different signs/formulas per calculation term |
| **Hidden conversions** | All X inputs auto-convert to aggregate Y |
| **Deliberate asymmetry** | Term 3 uses `ev_star`, Term 2 uses `e_eol` (not a typo) |
| **Domain conventions** | Negative = credit, positive = burden (or vice versa) |

## Usage

Reference this file explicitly:
- "Check critical LLM knowledge before implementing Term 4"
- "Review Rule 5 - we discussed this yesterday"

Add new rules as patterns emerge. Remove rules once Claude demonstrates consistent understanding.
