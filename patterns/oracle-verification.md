# Oracle Verification Pattern

## The Only Truth

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

## Implementation

### Step 1: Ground Truth Generation

Run source implementation on diverse inputs:

```julia
# generate_ground_truth.jl
inputs = [generate_random_input(seed) for seed in 1:50]
outputs = [source_func(x) for x in inputs]
save("ground_truth/func.npz", inputs=inputs, outputs=outputs)
```

### Step 2: Oracle Test

Compare target against ground truth:

```python
def test_oracle():
    """THE ONLY TEST THAT MATTERS"""
    for input, expected in load_ground_truth():
        actual = target_func(input)
        assert_close(actual, expected, rtol=1e-10)
```

### Step 3: Adversarial Attack

Try to find inputs where `target(x) ≠ source(x)`:

```python
strategies = [
    "boundary_values",    # 0, inf, nan, epsilon
    "ill_conditioned",    # Near-singular, high condition number
    "edge_dimensions",    # 1x1, empty, rectangular
    "random_stress",      # Many random seeds
]
```

If all attacks fail → translation is robust.

## Input Categories

Generate ground truth for ALL these:

| Category | Purpose | Examples |
|----------|---------|----------|
| **Random** | General correctness | 50+ seeds, various sizes |
| **Zero** | Degenerate case | All zeros |
| **Identity** | Special structure | Identity matrix |
| **Small** | Edge dimensions | 1x1, 2x2 |
| **Large** | Scale | 100x100, 500x500 |
| **Ill-conditioned** | Numerical edge | Near-singular |
| **Complex** | Type handling | Complex dtype |

## Doc-Based Tests (Secondary)

Doc helps us **understand** source, not define truth:

```python
# Tests OUR UNDERSTANDING, not ground truth
# If fails but oracle passes → update doc
def test_our_understanding_orthonormal():
    Q, R = qrpos(A)
    # If this fails, check source - maybe our understanding is wrong
    assert torch.allclose(Q.T @ Q, torch.eye(n))
```

### When Doc Tests Fail

```
Doc test fails + Oracle passes → Our understanding is wrong → Update doc
Doc test fails + Oracle fails  → Translation is wrong → Fix translation
```

## Verification Levels

| Level | Requirement |
|-------|-------------|
| **L2** | Oracle tests pass (target ≈ source) |
| **L3** | L2 + adversarial attacks fail |

**Doc-based tests are for understanding, not for level assignment.**

## Benefits

1. **Infinite test cases** — generate as many as needed from source
2. **No test maintenance** — oracle is always correct
3. **Catches subtle bugs** — numerical precision issues revealed
4. **Clear standard** — no ambiguity about what "correct" means

## Example

```julia
# Ground truth generation (Julia source)
Random.seed!(42)
A = randn(10, 10)
Q, R = qrpos(A)
npzwrite("ground_truth/qrpos.npz", Dict("A" => A, "Q" => Q, "R" => R))
```

```python
# Oracle test (Python target)
def test_qrpos_oracle():
    data = np.load("ground_truth/qrpos.npz")
    A = torch.from_numpy(data["A"])
    expected_Q = torch.from_numpy(data["Q"])
    expected_R = torch.from_numpy(data["R"])

    actual_Q, actual_R = qrpos(A)

    assert torch.allclose(actual_Q, expected_Q, rtol=1e-10)
    assert torch.allclose(actual_R, expected_R, rtol=1e-10)
```

## Summary

> **"The source works. Match it exactly. That's the only test that matters."**
