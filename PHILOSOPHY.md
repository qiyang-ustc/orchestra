# Orchestra: Philosophy of Provable Code Translation

## The Core Problem

LLMs can translate code. But how do you know the translation is correct?

Traditional approach:
```
Source code → LLM → Target code → Run tests → Hope it works
```

This fails for:
- Scientific computing (numerical precision matters)
- Legacy codebases (tests may not exist)
- Mission-critical systems (hope is not a strategy)

## The Only Truth: Oracle

**The source implementation IS the oracle. Its behavior is the ONLY golden standard.**

```
∀ valid input x:  target(x) ≈ source(x)
```

That's it. Nothing else defines correctness.

- If source has a "bug", we reproduce it faithfully
- If source has a trick we don't understand, we match its behavior
- Documentation helps us understand, but source behavior is truth

### Why Not Mathematical Properties?

You might think: "SVD should satisfy A = U @ S @ V.T, let's test that!"

No. Because:
- Source might have intentional deviations
- Source might use tricks we don't understand
- Our "mathematical understanding" might be wrong

**The source works. Match it exactly.**

## Oracle Testing

### Ground Truth Generation

Run source on diverse inputs, save outputs:

```julia
# Generate ground truth from source
inputs = [randn(10,10) for _ in 1:50]
outputs = [source_func(x) for x in inputs]
save("ground_truth.npz", inputs=inputs, outputs=outputs)
```

### Target Verification

```python
def test_oracle():
    for input, expected in load_ground_truth():
        actual = target_func(input)
        assert_close(actual, expected, rtol=1e-10)
```

### Adversarial Testing

Try to find inputs where `target(x) ≠ source(x)`:
- Boundary values (0, inf, nan, epsilon)
- Ill-conditioned inputs
- Edge dimensions (1x1, empty)
- Random stress testing

If all attacks fail → translation is robust.

## Documentation: For Understanding, Not Truth

Doc helps agents **understand** source behavior. It's a hypothesis.

```
Source (oracle) ─────────────────→ Target
       │                              │
       └── Doc (understanding) ───────┘
```

### Doc's Role

- Helps translator understand what source does
- If doc conflicts with source → source wins
- Doc tests verify our understanding, not correctness

### When Doc Tests Fail

```
Doc test fails + Oracle passes
  → Our understanding is wrong
  → Update doc, keep translation

Doc test fails + Oracle fails
  → Translation is wrong
  → Fix translation
```

## Verification Levels

| Level | Meaning | Requirement |
|-------|---------|-------------|
| **L0** | draft | Just written |
| **L1** | reviewed | Another agent checked |
| **L2** | tested | Oracle tests pass |
| **L3** | adversarial | Attacks failed to break oracle |
| **L4** | proven | + Human review |

**Only oracle tests determine L2/L3. Doc tests are for understanding.**

## Equivalence Types

Different functions need different comparison:

| Type | Definition | Example |
|------|------------|---------|
| **E5** | bit-identical | Integer operations |
| **E4** | within ε | Float math (rtol=1e-10) |
| **E3** | semantically same | Eigenvectors (up to phase) |
| **E2** | same behavior | Convergence paths may differ |
| **E1** | same distribution | Random functions |

Attacker uses equivalence type to know what "failure" means.

## The Conductor Model

```
┌─────────────────────────────────────────┐
│            CONDUCTOR (You)              │
│  - Dispatches to agents                 │
│  - Does NOT write code                  │
└─────────────────────────────────────────┘
         │         │         │
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │Doc     │ │Transl. │ │Verifier│
    │Writer  │ │        │ │        │
    └────────┘ └────────┘ └────────┘
```

Conductor orchestrates. Agents execute.

## Progressive Translation

Translate inside-out by conceptual layers:

```
Layer 0: Core math (svd, qr)      ← Must be L3 first
Layer 1: Building blocks (MPS)   ← After Layer 0 verified
Layer 2: Algorithms (VUMPS)      ← After Layer 1 verified
Layer 3: API                     ← Last
```

**Core must be solid. One bug there corrupts everything.**

## Async Human Review

When uncertain:
1. Submit to review queue
2. Continue with other work
3. Don't block

Human reviews in batches. Knowledge stored permanently.

## Atomic Commits

One function = one commit:
```
commit: "feat(linalg): translate svd [L3]"

├── code.py
├── test_code.py
└── report.yaml
```

Traceability. Bisectability. Rollbackability.

## Summary

| Traditional | Orchestra |
|-------------|-----------|
| Translate and hope | Prove equivalence via oracle |
| Trust LLM output | Oracle is only truth |
| Tests check properties | Tests compare against source |
| Doc defines correctness | Doc aids understanding |
| Bulk translation | One function at a time |
| Hope tests cover it | Adversarial attack |

**The result: Translations that match source behavior exactly.**
