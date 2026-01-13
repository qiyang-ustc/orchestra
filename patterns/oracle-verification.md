# Oracle Verification Pattern

## The Problem

How do you verify a code translation is correct?

Traditional approach:
- Write tests
- Hope they cover all cases
- Ship and pray

This fails because:
- Tests are incomplete by nature
- Edge cases are easy to miss
- "Works on my machine" syndrome

## The Insight

**The source implementation IS an oracle.**

If source code works, it defines correct behavior for all inputs:
```
oracle(x) = run source implementation with input x
```

Translation correctness becomes:
```
∀x: target(x) ≈ oracle(x)
```

## Implementation

### Step 1: Ground Truth Generation

Run source implementation on diverse inputs:

```
inputs = generate_test_inputs()
outputs = [source_impl(x) for x in inputs]
save_ground_truth(inputs, outputs)
```

### Step 2: Target Verification

Compare target against ground truth:

```python
def test_equivalence():
    for input, expected in load_ground_truth():
        actual = target_impl(input)
        assert_close(actual, expected, rtol=1e-10)
```

### Step 3: Exhaustive Coverage

Generate inputs systematically:
- Random (many seeds)
- Edge cases (zero, inf, nan)
- Boundary conditions (min, max sizes)
- Degenerate cases (singular matrices, etc.)

## Benefits

1. **Infinite test cases** — generate as many as needed
2. **No test maintenance** — oracle is always correct
3. **Catches subtle bugs** — numerical precision issues
4. **Documentation** — ground truth files document expected behavior

## Limitations

- Source must be runnable
- Non-deterministic code needs seeding
- External dependencies need mocking
- Very slow code limits test count

## Example

```python
# Ground truth generation (source language)
A = randn(10, 10)
Q, R = qrpos(A)
save("qrpos_test.npz", A=A, Q=Q, R=R)

# Verification (target language)
def test_qrpos():
    data = load("qrpos_test.npz")
    Q, R = qrpos(torch.from_numpy(data["A"]))
    assert_close(Q, data["Q"])
    assert_close(R, data["R"])
```
