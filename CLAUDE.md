# Orchestra Translation Project

Read `orchestra.yaml` for project declaration.

---

## CRITICAL RULES (MUST FOLLOW)

### 1. ONE FUNCTION AT A TIME

**DO NOT bulk translate.** Translate ONE function, verify it, commit it, then next.

```
❌ WRONG: Translate 20 functions → commit all → "done!"
✅ RIGHT: Translate svd() → verify to L2 → commit → translate qr() → verify → commit → ...
```

### 2. VERIFICATION GATES (BLOCKING)

**You CANNOT proceed to the next function until current one reaches required level.**

| Layer | Required Level | Gate |
|-------|----------------|------|
| Core math | **L3** | MUST pass adversarial before moving on |
| Building blocks | **L3** | MUST pass adversarial |
| Algorithms | L2 | Oracle tests sufficient |
| Utilities | L2 | Oracle tests sufficient |

**If you cannot reach the required level, STOP and ask human.**

### 3. ORACLE TESTS ARE MANDATORY

Tests must compare against SOURCE output, not just "runs without error".

```python
# ❌ WRONG: Only tests internal consistency
def test_svd():
    result = svd(A)
    assert result.shape == expected_shape  # This is NOT oracle test

# ✅ RIGHT: Compares against source implementation
def test_svd_oracle():
    A = load_test_input("svd_case_1")
    expected = load_julia_output("svd_case_1")  # Ground truth from Julia
    actual = svd(A)
    assert_close(actual, expected, rtol=1e-10)
```

### 4. CONCEPTUAL ORDER (INSIDE-OUT)

```
Layer 0: Core math (svd, qr, eig)     ← START HERE, ALL must reach L3
Layer 1: Building blocks (MPS, MPO)   ← Only after Layer 0 complete
Layer 2: Algorithms (VUMPS, DMRG)     ← Only after Layer 1 complete
Layer 3: API                          ← Last
```

**You CANNOT start Layer N until ALL of Layer N-1 reaches required level.**

---

## Workflow Per Function

```
1. DOCUMENT: Write doc for this function (hypothesis)
2. TRANSLATE: Write code (challenge doc against source if mismatch)
3. TEST: Write oracle test (compare against source output)
4. VERIFY: Run tests, check level reached
5. IF level < required: FIX or ASK HUMAN
6. COMMIT: Only after verification passes
7. NEXT: Move to next function
```

---

## Verification Levels

| Level | Name | Requirement |
|-------|------|-------------|
| L0 | draft | Just written |
| L1 | cross-checked | Another review, no contradictions |
| L2 | tested | **Oracle tests pass** (compare against source) |
| L3 | adversarial | Survives edge cases, boundary inputs |
| L4 | proven | + Human review |

---

## Source is READ-ONLY

**NEVER modify anything under `src` path.**

---

## When Stuck

1. Check `notes/knowledge_base.md`
2. If not found → ASK HUMAN
3. Record decision in knowledge_base.md

**DO NOT GUESS. DO NOT SKIP. ASK.**
