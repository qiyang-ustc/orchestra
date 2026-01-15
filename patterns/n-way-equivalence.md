# N-Way Equivalence Pattern

## The Problem

Single-dimension verification is fragile:
- Code matches? But tests might not cover edge cases
- Tests pass? But docs might describe different behavior
- Everything seems fine? But gradient might be wrong

## The Pattern

Verify across N independent dimensions. If all agree, confidence is high.

## Dimensions

### 2-Way (Basic)
```
Code_Source ≡ Code_Target
```

### 4-Way (Standard)
```
Code_Source ≡ Code_Target
Test_Source ≡ Test_Target
```

### 6-Way (Robust)
```
Code_Source ←→ Code_Target
Docs_Source ←→ Docs_Target
Test_Source ←→ Test_Target

Plus cross-checks:
Code ↔ Docs (both languages)
Test ↔ Docs (both languages)
```

### 8-Way (Paranoid)
Add:
- Type annotations equivalence
- Performance characteristics match

## Implementation

### Status Tracking

```yaml
module: path/to/module
equivalence:
  code: verified | pending | failed
  test: verified | pending | failed  
  docs: verified | pending | failed
  code_docs_source: verified | pending
  code_docs_target: verified | pending
  test_docs: verified | pending
proven: false  # true only when ALL pass
```

### Verification Matrix

```
         Source    Target
Code       ✓ ←——————→ ✓
           ↕          ↕
Docs       ✓ ←——————→ ✓
           ↕          ↕
Test       ✓ ←——————→ ✓
```

All arrows must hold.

## Why Docs Matter

Documentation is not optional decoration. It:

1. **Forces understanding** — can't document what you don't understand
2. **Creates semantic check** — docs must match code
3. **Catches mismatches** — if Python doc differs from MATLAB doc, something is wrong
4. **Preserves knowledge** — valuable by-product

## Choosing N

| Scenario | Recommended N |
|----------|---------------|
| Quick prototype | 2 |
| Production code | 4 |
| Scientific computing | 6 |
| Safety-critical | 8+ |

More N = higher confidence = slower progress.

## Failure Modes

If any check fails:
- Code_S ≢ Code_T → Translation bug
- Test_S ≢ Test_T → Test logic differs
- Docs_S ≢ Docs_T → Understanding differs
- Code ≢ Docs → Doc is wrong OR code is wrong

Each failure type has different debugging approach.

## Related Concepts

- **Equivalence Types (E0-E5)**: What does "≡" mean? See [EQUIVALENCE_TYPES.md](../EQUIVALENCE_TYPES.md)
- **Verification Levels (L0-L4)**: How verified is each check? See [VERIFICATION_LEVELS.md](../VERIFICATION_LEVELS.md)
- **Triangular Confrontation**: How agents challenge each other. See [triangular-confrontation.md](./triangular-confrontation.md)
