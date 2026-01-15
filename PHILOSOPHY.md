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

## The Oracle Insight

**The source implementation IS the oracle.**

If we have working source code, we have infinite test cases:
- Run source with input X → get output Y
- Run target with input X → must get output Y
- For ALL valid X

This transforms translation from "write and pray" to "prove equivalence".

```
∀ valid input x:  |f_target(x) - f_source(x)| < ε
```

## Trust Nothing: Triangular Confrontation

Multi-agent systems have a hidden failure mode: **agents trusting each other**.

If Doc-Writer makes a mistake, Translator copies it, Verifier validates against the wrong spec. The error propagates silently.

**Solution: No agent trusts another.**

```
        Doc (hypothesis)
         ↗️      ↖️
    challenge  challenge
       ↙️          ↘️
Source ←───oracle───→ Target
```

- Doc-Writer outputs a **hypothesis**, not truth
- Translator **challenges** doc against source while implementing
- Verifier **attacks** all three edges trying to break them

**Truth emerges from surviving disagreement, not from assumed agreement.**

## N-Way Equivalence

Single-dimension verification is fragile. Multi-dimension is robust.

### 2-Way (Basic)
```
Code_Source ≡ Code_Target
```
Problem: Bugs can hide in both.

### 4-Way (Better)
```
Code_Source ≡ Code_Target
Test_Source ≡ Test_Target
```
Problem: Tests might not cover edge cases.

### 6-Way (Robust)
```
Code_Source ←→ Code_Target
Docs_Source ←→ Docs_Target  
Test_Source ←→ Test_Target

Code ↔ Docs (both languages)
Test ↔ Docs (both languages)
```

Why docs matter:
- Forces LLM to **understand** before translating
- Creates semantic cross-check
- Produces valuable documentation as by-product

### N-Way (General)
Add more dimensions as needed:
- Type annotations
- Performance benchmarks
- Memory profiles
- API compatibility

More dimensions = higher confidence = slower progress.

Choose N based on criticality.

## The Async Human Pattern

LLMs encounter uncertainty. Two response strategies:

### Blocking (Bad)
```
Agent: "I'm not sure about this. What should I do?"
[WAITS INDEFINITELY]
Human: [Eventually responds hours later]
Agent: [Continues]
```

Problems:
- Wastes compute time
- Human may not be available
- Single uncertainty blocks all progress

### Non-Blocking (Good)
```
Agent: "I'm not sure about this."
Agent: [Submits to review queue]
Agent: [Marks module as PENDING_HUMAN]
Agent: [Immediately continues with OTHER modules]
...
Human: [Reviews queue when convenient]
Human: [Marks decision as RESOLVED]
...
Next Session:
Agent: [Finds resolved items]
Agent: [Continues previously blocked work]
```

Benefits:
- No wasted time
- Human reviews in batches (efficient)
- Progress continues on unblocked work
- Clear audit trail

## Agent Decomposition

### Why Multiple Agents?

Single LLM context limitations:
- Context window fills up
- Loses focus on long tasks
- Can't parallelize

Multiple specialized agents:
- Each has focused context
- Can work in parallel
- Composable expertise

### The Orchestra Model

```
┌─────────────────────────────────────────┐
│            CONDUCTOR (Orchestrator)      │
│  - Reads the score (CLAUDE.md)          │
│  - Dispatches to musicians              │
│  - Does NOT play instruments            │
└─────────────────────────────────────────┘
         │         │         │
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │Analyst │ │Transl. │ │Prover  │
    │        │ │        │ │        │
    │Reads   │ │Writes  │ │Verifies│
    │source  │ │target  │ │equality│
    └────────┘ └────────┘ └────────┘
```

Key principle: **Conductor dispatches, doesn't code.**

### Agent Categories

| Category | Purpose | Example Agents |
|----------|---------|----------------|
| Orchestration | Session management | init, progress, human-gate |
| Analysis | Understand source | scanner, mapper, archaeologist |
| Preprocessing | Prepare for translation | splitter, refactor-advisor |
| Translation | Write target code | translator, class-converter |
| Documentation | Generate docs | doc-writer, consistency-checker |
| Verification | Prove correctness | equivalence-prover, oracle |
| Debug | Fix issues | verifier, executor |

## Progressive Translation

### The Dependency Tree

Codebases have dependencies:
```
      optimizer.py
           │
     ┌─────┴─────┐
     │           │
  vumps.py   model.py
     │           │
  ┌──┴──┐        │
  │     │        │
env.py fix.py  ham.py
  │     │
  └──┬──┘
     │
 utils.py  ← LEAF (no dependencies)
```

### Translation Order

1. **Find leaves**: Modules with no internal dependencies
2. **Translate leaves**: They can be verified in isolation
3. **Move up**: Translate modules whose deps are done
4. **Repeat**: Until root is reached

Benefits:
- Each level verified before next
- Errors caught early
- Clear progress metric

### Parallel Opportunities

Same-level modules can translate in parallel:
```
Level 0: [utils.py]           → 1 agent
Level 1: [env.py, fix.py, ham.py] → 3 agents parallel
Level 2: [vumps.py, model.py]     → 2 agents parallel
Level 3: [optimizer.py]           → 1 agent
```

## The Queue as Interface

Human-agent communication via shared document:

```markdown
# Human Review Queue

## PENDING
- [ID-001] Issue X - waiting for decision
- [ID-002] Issue Y - waiting for decision

## RESOLVED  
- [ID-000] Issue Z - decided on 2024-01-14
```

Properties:
- **Persistent**: Survives session boundaries
- **Auditable**: Full decision history
- **Asynchronous**: No real-time requirement
- **Transparent**: Both sides see same state

## Verification Levels (L0-L4)

Every artifact carries a trust level:

| Level | Name | What it means |
|-------|------|---------------|
| L0 | draft | Just written, no verification |
| L1 | cross-checked | Another agent confirmed, no contradictions |
| L2 | tested | Oracle tests pass |
| L3 | adversarial | Attacker agent failed to break it |
| L4 | proven | Full verification + human review |

**Key rule: Any challenge immediately downgrades to L0.**

This creates pressure for quality — a single inconsistency resets progress.

## Equivalence Types (E0-E5)

Not all code can achieve the same level of "equal":

| Type | Definition | When achievable |
|------|------------|-----------------|
| E5 | bit-identical | Integer/boolean operations |
| E4 | within tolerance ε | Floating-point math |
| E3 | semantically same | Eigenvectors (up to phase) |
| E2 | same observable behavior | Convergence algorithms |
| E1 | same distribution | Random/stochastic functions |
| E0 | bounded difference | Intentional approximations |

**Why this matters for adversarial testing:**

The attacker agent must know what "failure" means:
- For E5: any bit difference = failure
- For E4: difference > ε = failure
- For E3: semantic invariant violated = failure
- For E1: distribution test failed = failure

Without this classification, attackers either miss real bugs (too lenient) or raise false alarms (too strict).

## Verification Testing Hierarchy

### Level 1: Output Equivalence
```
f_source(x) ≈ f_target(x)  for sampled x
```
Necessary but not sufficient.

### Level 2: Gradient Equivalence
```
∇f_source(x) ≈ ∇f_target(x)
```
Critical for ML/scientific code with autodiff.

### Level 3: Property Preservation
```
If f_source satisfies property P, f_target must too.
```
Examples: unitarity, canonicality, symmetry.

### Level 4: Edge Case Equivalence
```
f_source and f_target behave identically on:
- Zero input
- NaN/Inf
- Degenerate cases
- Boundary conditions
```

### Level 5: Adversarial Stress Testing
```
Attacker actively tries to find:
- Inputs where target ≠ source
- Properties doc claims but code violates
- Edge cases not covered by tests
```

Climb levels as confidence requirements increase.

## When This Fails

Orchestra is not magic. It fails when:

1. **No oracle available**: Source code doesn't run
2. **Non-deterministic code**: Random behavior, timing-dependent
3. **External dependencies**: Network calls, hardware-specific
4. **Proprietary formats**: Can't inspect intermediate states
5. **Insufficient human expertise**: Queue fills with unresolvable items

Mitigations:
- Mock external dependencies
- Seed random generators
- Focus on deterministic core first
- Build domain expertise incrementally

## Atomic Commits

Every translation unit produces exactly one commit containing:
- Target code
- Tests
- Documentation
- Verification report

```
commit: "feat(tensor): translate contract [L3]"
```

**Why atomic?**
1. **Traceability**: `git blame` shows who translated what
2. **Bisectability**: `git bisect` works at function level
3. **Reviewability**: Each commit is a complete, reviewable unit
4. **Rollbackability**: Revert one function without affecting others

## Knowledge Oracle

Human expertise is the most valuable and scarcest resource. Don't waste it.

### The Problem

Traditional approach:
```
Agent asks human → Human answers → Answer used once → Forgotten
Next session: Same question asked again
```

### The Solution

**Knowledge Oracle** — permanent memory for human expertise:

```
Agent asks → Oracle checks knowledge base
  → Found? Return answer
  → Not found? Ask human → Store permanently → Return answer
```

### What Gets Stored

| Category | Examples |
|----------|----------|
| **Conventions** | Index convention, sign convention, naming |
| **Domain Constraints** | Energy bounds, normalization, entropy limits |
| **Translation Decisions** | Why we chose A over B |
| **Gotchas** | Julia broadcast pitfalls, memory layout |

### Domain Constraints as Verification

Physical sanity checks become automated tests:

```python
# From knowledge_base.md:
# "Heisenberg ground state energy must be negative"

def test_vumps_heisenberg():
    result = vumps(heisenberg_hamiltonian())
    assert result.energy < 0  # Physical constraint
```

This captures **physics knowledge**, not just code correctness.

## Summary

Orchestra transforms code translation from art to engineering:

| Traditional | Orchestra |
|-------------|-----------|
| Translate and hope | Prove equivalence |
| Trust agent outputs | Triangular confrontation |
| Single LLM session | Multi-agent orchestration |
| Block on uncertainty | Async human review |
| All-at-once | Progressive by dependency |
| Tests as afterthought | Tests as verification |
| Docs optional | Docs as hypothesis to verify |
| Bulk commits | Atomic commits per function |
| Human answers once, forgotten | Knowledge Oracle, permanent memory |

The result: Translations you can trust, with full audit trail and preserved expertise.
