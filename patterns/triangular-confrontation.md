# Triangular Confrontation Pattern

## Problem

In multi-agent translation pipelines, errors propagate silently when agents trust each other's outputs.

## The Only Truth: Oracle

**Source implementation behavior is the ONLY golden standard.**

```
∀x: target(x) ≈ source(x)
```

- If source has a "bug", we reproduce it
- If source has a trick we don't understand, we match it
- Doc helps us understand, but source behavior is truth

## The Triangle

```
        Doc (hypothesis/understanding)
             ↗️      ↖️
        helps      informs
           ↙️          ↘️
    Source ←───oracle───→ Target
```

**Key insight: Only the bottom edge (source→target) determines correctness.**

Doc is for understanding, not verification. If doc conflicts with source → source wins.

## Agent Roles

### Doc-Writer (Hypothesis Generator)

```
INPUT:  Source code
OUTPUT: Documentation (hypothesis about source behavior)
STANCE: "I believe I understand the source"

MUST:
- Read source code directly
- Generate testable claims about source behavior
- Mark output as L0 (draft hypothesis)
- Mark uncertainties explicitly

MUST NOT:
- Claim certainty about source behavior
- Assume doc defines correctness
```

### Translator (Skeptical Implementer)

```
INPUT:  Source code + Doc (as understanding aid)
OUTPUT: Target code
STANCE: "Doc helps me understand, but source is truth"

MUST:
- Read source code independently
- Use doc to understand intent
- Follow SOURCE when doc conflicts
- Challenge doc if mismatch found

MUST NOT:
- Blindly follow doc over source
- Ignore source behavior
```

### Verifier (Oracle Tester)

```
INPUT:  Source + Target
OUTPUT: Verification report
STANCE: "Only oracle comparison matters"

MUST:
- Verify Target matches Source (oracle test)
- Generate diverse ground truth from source
- Run adversarial attacks against oracle comparison
- Mark verified items as L2/L3

MUST NOT:
- Use doc as verification standard
- Skip edge cases
- Accept without adversarial testing
```

## The Workflow

### Phase 1: Understanding (Doc)

```
Doc-Writer reads Source
  → Generates Doc (hypothesis about behavior)
  → Records uncertainty: "Source line 45 unclear, assumed X"
  → This is for UNDERSTANDING, not for defining correctness
```

### Phase 2: Translation (Following Source)

```
Translator reads Source + uses Doc for context
  → IF doc helps understand source: great
  → IF doc conflicts with source:
      CHALLENGE the doc
      → Follow SOURCE behavior anyway
      → Translation guided by source, not doc
```

### Phase 3: Oracle Verification

```
Verifier receives Source + Target
  → Generate ground truth from source
      FOR diverse inputs x:
        oracle_output = source(x)
        save to ground_truth file
  → Oracle test
      FOR each (x, expected) in ground_truth:
        actual = target(x)
        assert actual ≈ expected
  → Adversarial attack
      TRY to find x where target(x) ≠ source(x)
```

### Phase 4: Update Understanding (If needed)

```
IF oracle passes but doc test fails:
  → Our understanding was wrong
  → Update doc to match actual source behavior
  → Doc test should now pass
  → Translation is still correct (oracle passed)

IF oracle fails:
  → Translation is wrong
  → Fix translation to match source
```

## Doc's Role (Secondary)

Doc tests verify **our understanding**, not correctness:

```python
# Doc-based test: tests OUR UNDERSTANDING
def test_our_understanding_orthonormal():
    Q, R = qrpos(A)
    # If this fails, check source - maybe our understanding is wrong
    assert torch.allclose(Q.T @ Q, torch.eye(n))

# Oracle test: THE ONLY TRUTH
def test_oracle():
    expected = load_source_output("qrpos_case_1")
    actual = qrpos(input)
    assert torch.allclose(actual, expected)  # This determines correctness
```

**Decision Tree:**
```
Doc test fails + Oracle passes → Update doc (understanding was wrong)
Doc test fails + Oracle fails  → Fix translation
Doc test passes + Oracle passes → All good
Doc test passes + Oracle fails → Fix translation (doc test is irrelevant)
```

## Challenge Workflow

Challenges are about **doc accuracy**, not correctness:

```
Agent finds doc doesn't match source behavior
    │
    ▼
CHALLENGE RECORD
  - what: "Doc says X but source does Y"
  - where: file:line evidence
    │
    ▼
Update doc to match source behavior
```

## Benefits

1. **Clear truth** — Oracle is the only standard
2. **No confusion** — Doc is understanding, not spec
3. **Error detection** — Misunderstanding caught and fixed
4. **Quality signal** — L2/L3 means oracle verified

## Anti-Patterns

### ❌ Doc as Truth

```
"Doc says X, so translation must do X"
# WRONG: Source says Y, translation must do Y
```

### ❌ Mathematical Idealism

```
"SVD should satisfy A = U @ S @ V.T, let's test that"
# WRONG: Source might have tricks we don't understand
# Test against source output, not mathematical properties
```

### ❌ Skip Oracle

```
"Doc tests pass, so translation is correct"
# WRONG: Only oracle tests determine correctness
```

## Verification Levels

| Level | Requirement |
|-------|-------------|
| L0 | Just written |
| L1 | Another agent reviewed |
| L2 | Oracle tests pass |
| L3 | L2 + adversarial attacks fail |
| L4 | L3 + human review |

**Only oracle tests (source vs target) determine L2/L3.**

## Summary

> **"Source behavior is the only truth. Doc helps us understand it. Oracle tests verify we matched it."**
