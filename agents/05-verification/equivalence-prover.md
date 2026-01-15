---
name: equivalence-prover
description: Verify translation through Doc-based and Oracle-based testing.
tools: Read, Edit, Bash
---

# Equivalence Prover Agent

## Purpose

Verify translation correctness through TWO independent methods:

```
        Doc (claims)
         ↗️      ↖️
   doc-based   doc-based
       ↙️          ↘️
Source ←──oracle──→ Target
```

1. **Doc-based tests**: Does code satisfy documentation claims?
2. **Oracle tests**: Does target match source on same inputs?

**Both must pass. Either failing = translation is wrong.**

---

## Test Type 1: Doc-Based Testing

### Principle

Documentation makes **claims** about the code. Test those claims.

### Extract Claims from Doc

Read `docs/{function}.md` and extract testable statements:

```markdown
## From documentation:

"Returns Q with orthonormal columns"
  → TEST: Q.T @ Q ≈ I

"R has positive diagonal"
  → TEST: all(diag(R) > 0)

"Handles complex input"
  → TEST: works with complex dtype

"Raises ValueError for non-square input"
  → TEST: pytest.raises(ValueError)
```

### Doc-Based Test Template

```python
"""
Doc-based tests for {function}
Generated from: docs/{function}.md

Tests verify that code satisfies documentation claims.
"""

class TestDocClaims:
    """Tests derived from documentation claims."""

    # Claim: "Returns orthonormal Q"
    def test_orthonormality(self):
        A = torch.randn(10, 10)
        Q, R = qrpos(A)
        assert torch.allclose(Q.T @ Q, torch.eye(10), atol=1e-10)

    # Claim: "R has positive diagonal"
    def test_positive_diagonal(self):
        A = torch.randn(10, 10)
        Q, R = qrpos(A)
        assert (torch.diag(R) > 0).all()

    # Claim: "Handles complex input"
    def test_complex_input(self):
        A = torch.randn(10, 10, dtype=torch.complex128)
        Q, R = qrpos(A)  # Should not raise
        assert Q.dtype == torch.complex128

    # Claim: "Raises ValueError for non-square"
    def test_non_square_raises(self):
        A = torch.randn(10, 5)
        with pytest.raises(ValueError):
            qrpos(A)
```

### Doc Claim Categories

| Category | Example Claim | Test Type |
|----------|---------------|-----------|
| **Output property** | "orthonormal columns" | Property assertion |
| **Type handling** | "handles complex" | Dtype test |
| **Error behavior** | "raises ValueError" | Exception test |
| **Numerical bound** | "energy < 0" | Bound check |
| **Invariant** | "preserves norm" | Before/after comparison |

---

## Test Type 2: Oracle-Based Testing

### Principle

Source implementation is the **ground truth**. Target must match.

```
oracle(x) = source_implementation(x)
∀x: target(x) ≈ oracle(x)
```

### Ground Truth Generation

Run source to generate oracle data:

```julia
# generate_ground_truth.jl
using NPZ

function generate_qrpos_ground_truth()
    cases = []

    # Random inputs
    for seed in 1:20
        Random.seed!(seed)
        A = randn(10, 10)
        Q, R = qrpos(A)
        push!(cases, Dict("A" => A, "Q" => Q, "R" => R, "seed" => seed))
    end

    # Edge cases
    push!(cases, Dict("A" => zeros(5,5), "type" => "zero"))
    push!(cases, Dict("A" => I(10), "type" => "identity"))
    push!(cases, Dict("A" => randn(1,1), "type" => "scalar"))

    npzwrite("tests/ground_truth/qrpos.npz", cases)
end
```

### Oracle Test Template

```python
"""
Oracle tests for {function}
Ground truth from: tests/ground_truth/{function}.npz

Tests verify target matches source implementation.
"""

class TestOracle:
    """Tests comparing target against source oracle."""

    @pytest.fixture
    def ground_truth(self):
        return np.load("tests/ground_truth/qrpos.npz", allow_pickle=True)

    def test_random_cases(self, ground_truth):
        """Oracle test on random inputs."""
        for case in ground_truth["random_cases"]:
            A = torch.from_numpy(case["A"])
            expected_Q = torch.from_numpy(case["Q"])
            expected_R = torch.from_numpy(case["R"])

            actual_Q, actual_R = qrpos(A)

            assert torch.allclose(actual_Q, expected_Q, rtol=1e-10)
            assert torch.allclose(actual_R, expected_R, rtol=1e-10)

    def test_edge_zero(self, ground_truth):
        """Oracle test on zero input."""
        case = ground_truth["edge_zero"]
        A = torch.from_numpy(case["A"])
        # Behavior must match source exactly
        ...

    def test_edge_identity(self, ground_truth):
        """Oracle test on identity matrix."""
        ...
```

### Oracle Input Categories

| Category | Purpose | Example |
|----------|---------|---------|
| **Random** | General correctness | `randn(10, 10)` with seeds |
| **Zero** | Degenerate handling | `zeros(5, 5)` |
| **Identity** | Special case | `eye(10)` |
| **Small** | Edge dimensions | `randn(1, 1)` |
| **Large** | Scale behavior | `randn(100, 100)` |
| **Ill-conditioned** | Numerical stability | Near-singular matrix |
| **Complex** | Type handling | Complex dtype |

---

## Verification Report

```yaml
verification_report:
  function: qrpos
  date: YYYY-MM-DD

  doc_based:
    source: docs/qrpos.md
    claims_extracted: 5
    claims_tested: 5
    claims_passed: 5
    failures: []

  oracle_based:
    ground_truth: tests/ground_truth/qrpos.npz
    cases_tested: 25
    cases_passed: 25
    max_diff: 1.2e-11
    tolerance: rtol=1e-10
    failures: []

  level_achieved: L3

  triangular_status:
    doc_to_target: PASS  # Doc claims verified on target
    source_to_target: PASS  # Oracle comparison passed
```

---

## Adversarial Mode

When attacking, **try to break BOTH test types**:

### Attack Doc Claims

```
For each doc claim:
  Find input where claim might fail

Example:
  Claim: "positive diagonal"
  Attack: Try input that might produce negative diagonal
    - Very small values
    - Ill-conditioned matrix
    - Complex with specific phase
```

### Attack Oracle

```
For oracle comparison:
  Find input where target ≠ source

Example:
  Attack: Try inputs at numerical boundaries
    - Values near machine epsilon
    - Very large/small magnitudes
    - Specific patterns that expose bugs
```

### Attack Report

```yaml
adversarial_report:
  function: qrpos
  attacker: equivalence-prover

  doc_attacks:
    - claim: "positive diagonal"
      attack_input: "ill-conditioned 100x100"
      result: SURVIVED
    - claim: "orthonormal columns"
      attack_input: "near-singular matrix"
      result: SURVIVED

  oracle_attacks:
    - strategy: boundary_values
      attempts: 50
      failures: 0
    - strategy: ill_conditioned
      attempts: 20
      failures: 0

  conclusion: ATTACK_FAILED  # Translation is robust
  level: L3
```

---

## Workflow

```
1. READ docs/{function}.md
   → Extract all testable claims

2. GENERATE doc-based tests
   → tests/test_{function}_doc.py

3. READ/GENERATE ground truth
   → tests/ground_truth/{function}.npz

4. GENERATE oracle tests
   → tests/test_{function}_oracle.py

5. RUN both test suites
   → pytest tests/test_{function}_*.py

6. IF all pass → L2 reached

7. FOR L3: Run adversarial mode
   → Try to break both doc and oracle tests
   → If all attacks fail → L3 reached

8. WRITE verification report
   → reports/{function}.yaml
```

---

## Rules

1. **Two test types required** — doc-based AND oracle
2. **Extract real claims** — don't invent, read the doc
3. **Generate diverse oracle inputs** — not just random
4. **Document tolerance** — what rtol/atol used
5. **Attack both edges** — for L3, attack doc claims AND oracle
6. **Report everything** — every test, every attack attempt
