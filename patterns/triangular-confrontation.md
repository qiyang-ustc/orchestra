# Triangular Confrontation Pattern

## Problem

In multi-agent translation pipelines, errors propagate silently when agents trust each other's outputs. If Doc-Writer makes a mistake, Translator copies it, and Verifier validates against the wrong spec.

## Solution

**No agent trusts another. Every output is a hypothesis to be challenged.**

```
            Doc (hypothesis)
             ↗️      ↖️
        challenge  challenge
           ↙️          ↘️
    Source ←───compare───→ Target
       │                      │
       └────── oracle ────────┘
```

## Core Principle

**Truth emerges from disagreement, not agreement.**

Three independent verifications must align:
1. Doc describes Source correctly
2. Target implements Doc correctly
3. Target matches Source (oracle)

If any edge fails → the triangle is broken → downgrade to L0.

## Agent Responsibilities

### Doc-Writer (Hypothesis Generator)

```
INPUT:  Source code
OUTPUT: Documentation (hypothesis)
STANCE: "I believe I understand the source"

MUST:
- Read source code directly
- Generate testable claims
- Mark output as L0 (draft)

MUST NOT:
- Claim certainty
- Skip ambiguous cases
```

### Translator (Skeptical Implementer)

```
INPUT:  Source code + Doc (hypothesis)
OUTPUT: Target code + challenges
STANCE: "I will verify doc against source while translating"

MUST:
- Read source code independently
- Compare doc claims with source behavior
- Raise challenge if doc != source
- Mark output as L0 (draft)

MUST NOT:
- Blindly follow doc
- Assume doc is correct
- Ignore inconsistencies
```

### Verifier (Adversarial Auditor)

```
INPUT:  Source + Target + Doc
OUTPUT: Verification report + challenges
STANCE: "I trust nothing. I will try to break everything."

MUST:
- Verify Target matches Source (oracle test)
- Verify Doc describes Source correctly
- Verify Doc describes Target correctly
- Actively try to find counterexamples
- Mark verified items as L2/L3

MUST NOT:
- Assume any input is correct
- Skip edge cases
- Accept without adversarial testing
```

## The Confrontation Protocol

### Phase 1: Hypothesis Generation

```
Doc-Writer reads Source
  → Generates Doc (L0)
  → Records uncertainty: "Source line 45 unclear, assumed X"
```

### Phase 2: Skeptical Translation

```
Translator reads Source + Doc
  → Compares Doc claims with Source
  → IF match: proceeds with translation
  → IF mismatch:
      CHALLENGE {
        doc_claim: "Function returns sorted array"
        source_behavior: "Function returns array in original order"
        evidence: "source.jl:45 - no sort call"
      }
      → Doc downgrades to L0
      → Translator makes own interpretation
```

### Phase 3: Adversarial Verification

```
Verifier receives Source + Target + Doc (all L0/L1)
  → Test 1: Oracle comparison
      FOR random inputs x:
        assert target(x) ≈ source(x)
  → Test 2: Doc-Source consistency
      FOR each doc claim:
        verify source satisfies claim
  → Test 3: Doc-Target consistency
      FOR each doc claim:
        verify target satisfies claim
  → Test 4: Adversarial attack
      TRY to find x where target(x) != source(x)
      TRY to find doc claim that code violates
```

## Challenge Workflow

```
Agent finds inconsistency
    │
    ▼
┌─────────────────────────────────────┐
│ CHALLENGE RECORD                    │
│ - who: which agent                  │
│ - what: inconsistency description   │
│ - where: file:line evidence         │
│ - severity: critical/major/minor    │
└─────────────────────────────────────┘
    │
    ▼
Affected item downgrades to L0
    │
    ▼
Challenge queued for resolution
    │
    ├──[resolved by agent]──→ Item re-verified
    │
    └──[needs human]──→ human_review_queue.md
```

## Example Confrontation

### Scenario

Doc-Writer wrote:
```markdown
## contract_tensors
Contracts two tensors along specified dimensions.
**dims**: 0-indexed list of dimensions
```

Translator found:
```julia
# Source: contract.jl:52
result = contract(a, b, dims .+ 1)  # Julia adds 1 to dims!
```

### Challenge Raised

```yaml
challenge:
  id: CHG-042
  date: 2024-01-15
  raised_by: source-to-target
  against: docs/contract_tensors.md

  description: |
    Doc claims dims is 0-indexed, but source code adds 1 to dims
    before passing to internal contract function. This suggests
    the source actually expects 0-indexed input (Python-style),
    but the doc description is misleading about what "0-indexed" means
    in this context.

  evidence:
    - file: contract.jl
      line: 52
      content: "dims .+ 1  # converting from 0-indexed to Julia 1-indexed"
    - file: docs/contract_tensors.md
      section: Parameters
      content: "dims: 0-indexed list"

  proposed_resolution: |
    Doc is technically correct but confusing. The source accepts
    0-indexed dims (Python convention) and internally converts to
    1-indexed for Julia. Doc should clarify this conversion.

  severity: major
```

### Resolution

```yaml
resolution:
  decision: clarify_doc
  resolved_by: doc-writer
  date: 2024-01-16

  action: |
    Updated doc to:
    "dims: 0-indexed dimension list (Python convention).
     Note: Source internally converts to 1-indexed for Julia operations."

  verification:
    - doc re-checked by translator: pass
    - oracle tests: pass
    - doc-source consistency: pass
```

## Benefits

1. **Error Detection**: Mistakes caught at intersection points
2. **Forced Understanding**: No agent can coast on others' work
3. **Audit Trail**: Every challenge is documented
4. **Quality Signal**: L3/L4 means survived multiple challenges
5. **No Silent Failures**: Disagreement is surfaced, not hidden

## Anti-Patterns

### ❌ Rubber Stamp

```
Translator: "Doc says X, I'll just implement X"
# WRONG: No verification against source
```

### ❌ Silent Override

```
Translator: "Doc says X but source does Y. I'll implement Y and not mention it."
# WRONG: Must raise challenge
```

### ❌ Trust Cascade

```
Verifier: "Translator already checked against doc, I'll just run tests"
# WRONG: Must independently verify all three edges
```

## Integration with Verification Levels

| Level | Triangular Status |
|-------|-------------------|
| L0 | Single point (no verification) |
| L1 | One edge verified (e.g., doc-source) |
| L2 | Two edges verified (e.g., doc-source, source-target) |
| L3 | All edges verified + adversarial |
| L4 | Full triangle + human confirmation |

## Summary

> **"In triangular confrontation, consensus is earned through surviving disagreement, not assumed through blind trust."**
