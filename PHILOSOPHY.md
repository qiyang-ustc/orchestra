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

## Verification Hierarchy

Not all verification is equal:

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

### Level 5: Stress Testing
```
Both handle:
- Maximum size inputs
- Numerical instability
- Memory pressure
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

## Summary

Orchestra transforms code translation from art to engineering:

| Traditional | Orchestra |
|-------------|-----------|
| Translate and hope | Prove equivalence |
| Single LLM session | Multi-agent orchestration |
| Block on uncertainty | Async human review |
| All-at-once | Progressive by dependency |
| Tests as afterthought | Tests as verification |
| Docs optional | Docs as cross-check |

The result: Translations you can trust.
