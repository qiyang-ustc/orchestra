# Orchestra

**A framework for provably correct code translation using multi-agent LLM orchestration.**

## What is Orchestra?

Orchestra is a methodology and template library for translating large codebases between programming languages using LLMs, with mathematical guarantees of correctness.

The key insight: **The bottleneck of LLM code translation is not "can it write code" but "how do we verify it's correct".**

Orchestra solves this through:
1. **Oracle-based verification**: Source implementation serves as ground truth
2. **N-way equivalence proofs**: Code, tests, and docs must all match
3. **Async human-in-the-loop**: Non-blocking human decisions via queue pattern
4. **Multi-agent decomposition**: Specialized agents for analysis, translation, verification

## Quick Start

1. Copy the templates to your project:
```bash
cp -r orchestra/templates/* /path/to/your/project/
cp -r orchestra/agents/* /path/to/your/project/.claude/agents/
```

2. Customize `CLAUDE.md` for your specific translation:
   - Set source and target paths
   - Define equivalence dimensions
   - Configure language-specific rules

3. Start Claude Code:
```bash
cd /path/to/your/project
claude --dangerously-skip-permissions
```

4. Say: "Start session, follow CLAUDE.md protocol"

## Directory Structure

```
orchestra/
├── README.md                 # This file
├── PHILOSOPHY.md             # Core principles and theory
│
├── templates/                # Base templates to customize
│   ├── CLAUDE_BASE.md        # Main orchestration config
│   ├── pyproject_base.toml   # Python project template
│   └── conftest_base.py      # Pytest configuration
│
├── agents/                   # Reusable agent definitions
│   ├── 00-orchestration/     # Session management
│   ├── 01-analysis/          # Code understanding
│   ├── 02-preprocessing/     # Refactoring, splitting
│   ├── 03-translation/       # Actual translation
│   ├── 04-documentation/     # Doc generation
│   ├── 05-verification/      # Equivalence proofs
│   └── 06-debug/             # Troubleshooting
│
├── patterns/                 # Design patterns
│   ├── oracle-verification.md
│   ├── async-human-review.md
│   ├── n-way-equivalence.md
│   └── progressive-translation.md
│
└── examples/                 # Complete examples
    ├── julia-to-pytorch/     # TeneT.jl translation
    └── matlab-to-python/     # Corboz TN translation
```

## Core Concepts

### The Orchestra Metaphor

- **Conductor** (Orchestrator): Dispatches tasks, doesn't write code directly
- **Musicians** (Sub-agents): Specialized performers (analyzer, translator, prover)
- **Score** (CLAUDE.md): The master plan defining the performance
- **Symphony** (Final output): Provably correct translated codebase

### N-Way Equivalence

For high-stakes translation, verify across multiple dimensions:

```
     Code_Source ←——————→ Code_Target
          ↑                    ↑
          ↓                    ↓
     Docs_Source ←——————→ Docs_Target
          ↑                    ↑
          ↓                    ↓
     Test_Source ←——————→ Test_Target
```

All arrows must hold. If any breaks, something is wrong.

### Async Human Review

When agents encounter uncertainty:
1. Submit to queue (don't block)
2. Skip the uncertain module
3. Continue with other work
4. Human reviews asynchronously
5. Next session picks up resolved items

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

## Examples

### Julia → PyTorch (TeneT.jl)
Tensor network library translation with gradient correctness verification.

### MATLAB → Python (Corboz TN)
15-year-old physics codebase with 6-way equivalence proofs and legacy code archaeology.

See `examples/` for complete configurations.

## Contributing

This is an evolving methodology. Contributions welcome:
- New agent templates for different scenarios
- Additional design patterns
- Examples from other language pairs
- Improvements to verification strategies

## License

MIT
