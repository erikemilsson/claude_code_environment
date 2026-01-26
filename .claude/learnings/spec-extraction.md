# Spec Extraction from Source Documents

Converting PDFs/regulations/technical documents into machine-readable specifications.

## When to Use

Complex calculations or logic defined in:
- Regulatory documents (legal text with formulas)
- Technical standards
- Academic papers with methodologies
- Any authoritative source with ambiguities

## Process

### 1. Create Structured Markdown from Source

Extract into clean format:
- **Formulas** - LaTeX or code-friendly notation
- **Variables** - Machine-readable names (no subscripts, no special chars)
- **Parameters** - Tables with types, units, defaults
- **Decision points** - Where interpretation was needed

### 2. Variable Naming Convention

| Original | Machine-readable | Notes |
|----------|------------------|-------|
| E_v,mat | `ev_mat` | Subscripts become suffixes |
| R₁ | `r1_mat` | Numeric subscripts inline |
| Q_sin/Q_p | `qsin_over_qp` | Fractions spelled out |

### 3. Decision Log for Ambiguities

For each ambiguity resolved:

```markdown
## [Short title]

**Source text:** "[exact quote]"

**Ambiguity:** What's unclear

**Options:**
- A: [interpretation]
- B: [interpretation]

**Decision:** [A or B]

**Rationale:** [why]
```

## Key Principle

The extracted spec becomes the source of truth for implementation. Claude reads the spec, not the original PDF. Human resolves ambiguities once, documents them, Claude follows.
