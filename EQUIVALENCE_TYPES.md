# Equivalence Types

Not all translations can achieve the same level of equivalence. This document defines what "equivalent" means at different levels.

## The Equivalence Hierarchy

```
E5: Strict        ← bit-identical outputs (rare)
E4: Numerical     ← within tolerance ε
E3: Semantic      ← same meaning, different form
E2: Behavioral    ← same observable behavior
E1: Statistical   ← same distribution (for random functions)
E0: Approximate   ← intentionally different but acceptable
```

Higher is stricter. **Always aim for the highest achievable level.**

## Level Definitions

### E5: Strict Equivalence

```
∀x: f_target(x) == f_source(x)  (bit-identical)
```

**When achievable**:
- Integer arithmetic
- String operations
- Boolean logic
- Deterministic algorithms with exact arithmetic

**Example**:
```python
# Source (Julia)
function factorial(n)
    n <= 1 ? 1 : n * factorial(n-1)
end

# Target (Python) - E5 achievable
def factorial(n: int) -> int:
    return 1 if n <= 1 else n * factorial(n - 1)
```

### E4: Numerical Equivalence

```
∀x: |f_target(x) - f_source(x)| < ε
```

**When achievable**:
- Floating-point arithmetic
- Linear algebra (with same algorithms)
- Numerical optimization
- Most scientific computing

**Example**:
```python
# E4: outputs differ by ~1e-15 due to FP ordering
# Source: sum(a .* b)
# Target: (a * b).sum()
# Different reduction order → different rounding → E4 not E5
```

**Tolerance specification**:
```yaml
equivalence:
  type: E4
  rtol: 1e-10
  atol: 1e-12
  justification: "Standard double precision tolerance"
```

### E3: Semantic Equivalence

```
∀x: meaning(f_target(x)) == meaning(f_source(x))
```

**When achievable**:
- Eigenvectors (up to phase)
- Unordered results (sets, dictionaries)
- Numerically equivalent but symbolically different

**Example**:
```python
# E3: Eigenvectors equivalent up to phase e^(iθ)
# Source may return v, target may return -v or e^(iπ/4)*v
# Semantically same eigenvector, numerically different

def assert_eigenvector_equivalent(v1, v2):
    # Compare projectors |v><v| instead of vectors
    proj1 = outer(v1, conj(v1))
    proj2 = outer(v2, conj(v2))
    assert_close(proj1, proj2)
```

**Documentation requirement**:
```yaml
equivalence:
  type: E3
  semantic_rule: "eigenvector_up_to_phase"
  comparison_method: "projector_comparison"
```

### E2: Behavioral Equivalence

```
∀x: observable_behavior(f_target(x)) == observable_behavior(f_source(x))
```

**When achievable**:
- Stateful operations (iteration count may differ)
- Convergence algorithms (path may differ, result same)
- Caching/memoization (same outputs, different internals)

**Example**:
```python
# E2: Both converge to same result, but...
# Source: 47 iterations to converge
# Target: 52 iterations to converge (different precision handling)
# Observable output identical, internal path different

equivalence:
  type: E2
  observable: "converged_result"
  allowed_differences:
    - iteration_count
    - intermediate_states
```

### E1: Statistical Equivalence

```
distribution(f_target(x)) == distribution(f_source(x))
```

**When achievable**:
- Random number generation
- Monte Carlo methods
- Stochastic algorithms

**Example**:
```python
# E1: Same statistical properties, different realizations
# Source and target use different RNG implementations
# Cannot compare individual outputs, only distributions

def test_statistical_equivalence():
    source_samples = [source_random() for _ in range(10000)]
    target_samples = [target_random() for _ in range(10000)]

    # KS test for distribution equality
    statistic, pvalue = ks_2samp(source_samples, target_samples)
    assert pvalue > 0.05, "Distributions differ"
```

**Specification**:
```yaml
equivalence:
  type: E1
  test: kolmogorov_smirnov
  samples: 10000
  significance: 0.05
```

### E0: Approximate Equivalence

```
f_target(x) ≈ f_source(x) with documented differences
```

**When necessary**:
- Platform-specific optimizations
- Intentional algorithm changes
- Performance vs accuracy tradeoffs

**Example**:
```python
# E0: Target uses faster but less accurate algorithm
# Source: Full SVD decomposition
# Target: Truncated randomized SVD
# Intentionally different for performance

equivalence:
  type: E0
  reason: "Performance optimization"
  max_difference: "5% relative error on singular values"
  tradeoff: "10x speedup for 5% accuracy loss"
  approval: "REQUIRES_HUMAN_REVIEW"
```

## Function Classification

Before translating, classify each function:

```yaml
function: contract_tensors
classification:
  deterministic: true
  floating_point: true
  has_phase_ambiguity: false
  has_ordering_ambiguity: false
  has_randomness: false

  achievable_equivalence: E4
  target_tolerance:
    rtol: 1e-10
    atol: 1e-12
```

### Decision Tree

```
Is output deterministic?
├── NO → Is it random?
│        ├── YES → E1 (Statistical)
│        └── NO → E2 (Behavioral)
└── YES → Is output exact (integer/boolean)?
          ├── YES → E5 (Strict)
          └── NO → Does output have ambiguity (phase/order)?
                   ├── YES → E3 (Semantic)
                   └── NO → E4 (Numerical)
```

## Adversarial Testing by Equivalence Type

| Type | Attack Strategy | Pass Criterion |
|------|-----------------|----------------|
| E5 | Exhaustive comparison | bit-identical |
| E4 | Numerical edge cases | within tolerance |
| E3 | Semantic invariant tests | invariant preserved |
| E2 | Behavioral observation | same observable output |
| E1 | Statistical tests | distribution match |
| E0 | Documented bounds | within stated bounds |

### E4 Adversarial Examples

```python
adversarial_inputs = [
    torch.zeros(10, 10),                    # Zero matrix
    torch.eye(10) * 1e-15,                  # Near-zero
    torch.eye(10) * 1e15,                   # Large values
    torch.randn(10, 10) + 1j * 1e-16,       # Tiny imaginary
    create_ill_conditioned(10, cond=1e14),  # Near-singular
]
```

### E3 Adversarial Examples

```python
# For eigenvector equivalence, attack the projector comparison
adversarial_inputs = [
    create_matrix_with_degenerate_eigenvalues(),  # Multiple same eigenvalues
    create_matrix_with_near_degenerate(),         # Eigenvalues differ by 1e-10
]
```

## Reporting Equivalence Type

Every verification report must include:

```yaml
equivalence_proof:
  function: function_name

  classification:
    type: E4
    justification: "Floating-point linear algebra without ambiguity"

  specification:
    rtol: 1e-10
    atol: 1e-12

  adversarial:
    attacks_for_type: [numerical_edge_cases, ill_conditioned]
    attacks_run: 50
    failures: 0

  conclusion:
    achieved: E4
    confidence: HIGH
```

## Downgrade Protocol

If target cannot achieve expected equivalence:

1. **Document why** — what prevents higher level?
2. **State achieved level** — what CAN be guaranteed?
3. **Human review required** — E0 always needs approval
4. **Update classification** — for future reference

```yaml
downgrade:
  expected: E4
  achieved: E3
  reason: |
    Julia's eig() returns eigenvectors in different order than
    PyTorch's linalg.eig(). Order is not specified in either
    language's documentation.
  mitigation: |
    Compare unordered sets of eigenpairs instead of ordered vectors.
  approval: pending_human_review
```

## Summary Table

| Type | Comparison | Tolerance | Ambiguity | Randomness | Human Review |
|------|------------|-----------|-----------|------------|--------------|
| E5 | `==` | None | None | None | No |
| E4 | `≈` | ε | None | None | No |
| E3 | semantic | ε | Handled | None | Maybe |
| E2 | behavioral | N/A | Handled | None | Maybe |
| E1 | statistical | p-value | N/A | Expected | Maybe |
| E0 | bounded | stated | N/A | N/A | **Required** |
