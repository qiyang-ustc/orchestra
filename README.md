# Orchestra

**A framework for provably correct code translation using multi-agent LLM orchestration.**

## What is Orchestra?

Orchestra is a methodology and template library for translating large codebases between programming languages using LLMs, with mathematical guarantees of correctness.

The key insight: **The bottleneck of LLM code translation is not "can it write code" but "how do we verify it's correct".**

Orchestra solves this through:

1. **Triangular Confrontation**: Agents don't trust each other — they challenge
2. **Verification Levels (L0-L4)**: Every artifact carries trust status
3. **Equivalence Types (E0-E5)**: Clear definition of what "equal" means
4. **Atomic Commits**: One function = one complete, traceable commit
5. **Async Human Review**: Non-blocking decisions via queue pattern

## Quick Start

1. Create `orchestra.yaml` in your project:

```yaml
src: ../TeneT.jl            # Source (read-only)
dst: ./tenet_py             # Target (local, read-write)
framework: julia -> pytorch

notes: |
  Tensor network library for quantum simulations.

  Key things:
  - Julia 1-indexed → Python 0-indexed
  - Ground state energy should be negative
  - Start with core linalg, then MPS, then VUMPS

  Watch out for:
  - Phase ambiguity in eigenvectors
  - Sign convention in QR
```

2. Say: `/orchestra` or "start orchestra"

That's it. Put your domain knowledge in `notes`, LLM handles the rest.

## Directory Structure

```
orchestra/
├── README.md                    # This file
├── PHILOSOPHY.md                # Core principles and theory
├── VERIFICATION_LEVELS.md       # L0-L4 trust levels
├── EQUIVALENCE_TYPES.md         # E0-E5 what "equal" means
├── ATOMIC_COMMIT.md             # Commit conventions
│
├── templates/                   # Base templates to customize
│   ├── CLAUDE_BASE.md           # Main orchestration config
│   ├── pyproject_base.toml      # Python project template
│   └── conftest_base.py         # Pytest + adversarial testing
│
├── agents/                      # Reusable agent definitions
│   ├── 00-orchestration/        # Session management
│   ├── 01-analysis/             # Code understanding
│   ├── 02-preprocessing/        # Refactoring, splitting
│   ├── 03-translation/          # Actual translation
│   ├── 04-documentation/        # Doc generation
│   ├── 05-verification/         # Equivalence proofs
│   └── 06-debug/                # Troubleshooting
│
└── patterns/                    # Design patterns
    ├── oracle-verification.md
    ├── async-human-review.md
    ├── n-way-equivalence.md
    ├── progressive-translation.md
    └── triangular-confrontation.md
```

## Core Concepts

### The Onion Model (Inside-Out Translation)

Translation follows **human understanding order**, not dependency graph:

```
┌─────────────────────────────────────┐
│  Edge: IO, CLI (L2 ok)              │
├─────────────────────────────────────┤
│  API: Public interfaces (L2 ok)     │
├─────────────────────────────────────┤
│  Algorithm: Domain logic (L2→L3)    │
├─────────────────────────────────────┤
│  Building Blocks: Structures (L3)   │
├─────────────────────────────────────┤
│  Core Math: SVD, contract (L3+)     │  ← Start here
└─────────────────────────────────────┘
```

**Core math must be L3+ before anything else.** One bug there corrupts everything.

### Triangular Confrontation

No agent trusts another. Every output is a hypothesis to be challenged.

```
        Doc (hypothesis)
         ↗️      ↖️
    challenge  challenge
       ↙️          ↘️
Source ←───oracle───→ Target
```

- **Doc-Writer**: Generates hypothesis from source
- **Translator**: Challenges doc while implementing (follows source when conflict)
- **Verifier**: Attacks all three edges, tries to break the translation

### Translation Planner

The **strategic brain** that maintains:
- **Conceptual map**: Which layer is each module?
- **Verification state**: What level is each module at?
- **Failure propagation**: When high-level fails, upgrade core requirements

### Knowledge Oracle

The **permanent memory** that manages:
- **Knowledge Base**: All human decisions and domain expertise
- **Domain Constraints**: Physical sanity checks (energy bounds, normalization)
- **Consultation**: Other agents query before asking humans again

Human expertise is captured once, reused forever.

### Verification Levels

Every code/test/doc fragment carries a trust level:

| Level | Name | Meaning |
|-------|------|---------|
| **L0** | draft | Just written, unverified |
| **L1** | cross-checked | Another agent confirmed |
| **L2** | tested | Oracle tests pass |
| **L3** | adversarial | Survived attacks |
| **L4** | proven | Full verification + human review |

**Any challenge immediately downgrades to L0.**

### Equivalence Types

Not all code can achieve the same level of "equal":

| Type | Meaning | Example |
|------|---------|---------|
| **E5** | bit-identical | Integer arithmetic |
| **E4** | within ε | Floating-point math |
| **E3** | semantically same | Eigenvectors (up to phase) |
| **E2** | same behavior | Convergence (different paths) |
| **E1** | same distribution | Random functions |
| **E0** | bounded difference | Intentional approximations |

**Attacker agent uses equivalence type to calibrate attacks.**

### Atomic Commits

Every translation unit produces one commit with:

```
commit: "feat(tensor): translate contract [L3]"

├── tenet_py/contract.py           # Code
├── tests/test_contract.py         # Tests
├── docs/contract.md               # Documentation
└── reports/contract.yaml          # Verification report
```

Full traceability. `git bisect` works at function level.

## When to Use Orchestra

✅ **Good fit:**
- Large legacy codebases (10k+ lines)
- Mission-critical scientific code
- Code where correctness matters more than speed
- Translations requiring domain expertise

❌ **Not ideal for:**
- Small scripts (just translate directly)
- Prototypes where correctness isn't critical
- Languages with existing automated transpilers

## Key Documents

| Document | Purpose |
|----------|---------|
| [PHILOSOPHY.md](PHILOSOPHY.md) | Theory and principles |
| [VERIFICATION_LEVELS.md](VERIFICATION_LEVELS.md) | L0-L4 detailed spec |
| [EQUIVALENCE_TYPES.md](EQUIVALENCE_TYPES.md) | E0-E5 detailed spec |
| [TRANSLATION_ORDER.md](TRANSLATION_ORDER.md) | Which function to translate when |
| [ATOMIC_COMMIT.md](ATOMIC_COMMIT.md) | Commit conventions |
| [patterns/triangular-confrontation.md](patterns/triangular-confrontation.md) | The core verification pattern |

## Contributing

This is an evolving methodology. Contributions welcome:
- New agent templates for different scenarios
- Additional design patterns
- Improvements to verification strategies
- Better adversarial attack strategies

## License

MIT
