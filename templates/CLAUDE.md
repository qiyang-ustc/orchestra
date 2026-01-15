# Orchestra Translation Project

Read `orchestra.yaml` for project declaration.

---

## You Are The Conductor

```
┌─────────────────────────────────────────┐
│            YOU (Conductor)              │
│  - Read this score (CLAUDE.md)          │
│  - Dispatch to musicians (agents)       │
│  - DO NOT play instruments yourself     │
└─────────────────────────────────────────┘
         │         │         │
         ▼         ▼         ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │Doc     │ │Trans.  │ │Verifier│
    │Writer  │ │Agent   │ │/Attacker│
    └────────┘ └────────┘ └────────┘
```

**If you find yourself writing code, STOP. Spawn an agent instead.**

---

## Agent Registry

These are your musicians. Spawn them using the Task tool.

| Agent | File | Purpose |
|-------|------|---------|
| **Translation Planner** | `agents/00-orchestration/translation-planner.md` | Strategic brain. What to translate next. |
| **Knowledge Oracle** | `agents/00-orchestration/human-review-gate.md` | Human knowledge & decisions. |
| **Doc-Writer** | `agents/04-documentation/doc-writer.md` | Write doc hypothesis. |
| **Translator** | `agents/03-translation/source-to-target.md` | Write code, challenge doc. |
| **Verifier** | `agents/05-verification/equivalence-prover.md` | Oracle tests & adversarial attacks. |
| **Scanner** | `agents/01-analysis/codebase-scanner.md` | Analyze source structure. |

**Before spawning, read the agent's markdown file for its protocol.**

---

## Session Start Protocol

When beginning a session:

```
1. Read orchestra.yaml
2. SPAWN Translation Planner → "Status report. What should we work on next?"
3. Check notes/human_review_queue.md for resolved items
4. Follow planner's recommendation
```

---

## Per-Function Workflow

For EACH function to translate:

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: DOCUMENT (Hypothesis)                               │
│                                                             │
│ SPAWN Doc-Writer with:                                      │
│   "Read {source_file}:{function_name}                       │
│    Write documentation as HYPOTHESIS.                       │
│    Mark uncertainties explicitly.                           │
│    Output to docs/{function_name}.md"                       │
│                                                             │
│ Doc-Writer output is L0 (draft hypothesis).                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: TRANSLATE (Challenge Doc)                           │
│                                                             │
│ SPAWN Translator with:                                      │
│   "Translate {source_file}:{function_name}                  │
│    Read docs/{function_name}.md as hypothesis.              │
│    CHALLENGE doc against source - source wins if conflict.  │
│    Report any inconsistencies to notes/challenges/          │
│    Output to {dst}/{target_file}.py"                        │
│                                                             │
│ Translator output is L0. Challenges doc if mismatch.        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: VERIFY (Oracle Test)                                │
│                                                             │
│ SPAWN Verifier with:                                        │
│   "Write oracle tests for {function_name}.                  │
│    Tests MUST compare against source implementation.        │
│    Generate ground truth data from source.                  │
│    Output to tests/test_{function_name}.py"                 │
│                                                             │
│ RUN tests: pytest tests/test_{function_name}.py             │
│                                                             │
│ If PASS → L2 reached.                                       │
│ If FAIL → SPAWN Translator to fix, retry.                   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: ADVERSARIAL (For L3 targets only)                   │
│                                                             │
│ SPAWN Verifier (as Attacker) with:                          │
│   "ATTACK {function_name} translation.                      │
│    Your goal: find inputs where target ≠ source.            │
│    Try: zero, inf, nan, boundary, ill-conditioned, random.  │
│    Report all failures to notes/attacks/"                   │
│                                                             │
│ If attacker FAILS to break → L3 reached.                    │
│ If attacker SUCCEEDS → SPAWN Translator to fix, retry.      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: COMMIT (Atomic)                                     │
│                                                             │
│ git add:                                                    │
│   - {dst}/{target_file}.py       (code)                     │
│   - tests/test_{function_name}.py (tests)                   │
│   - docs/{function_name}.md       (documentation)           │
│   - reports/{function_name}.yaml  (verification report)     │
│                                                             │
│ git commit -m "feat({module}): translate {function} [L{N}]" │
│                                                             │
│ One function = One atomic commit.                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: UPDATE STATE                                        │
│                                                             │
│ SPAWN Translation Planner with:                             │
│   "Update state: {function_name} is now L{N}.               │
│    Check if any blocked modules can unblock.                │
│    What should we work on next?"                            │
│                                                             │
│ Follow planner's next recommendation.                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Blocking Gates (CRITICAL)

| Layer | Required Level | You CANNOT proceed until |
|-------|----------------|--------------------------|
| Core math | **L3** | Adversarial attack failed |
| Building blocks | **L3** | Adversarial attack failed |
| Algorithms | L2 | Oracle tests pass |
| Utilities | L2 | Oracle tests pass |

**L3 for core is NON-NEGOTIABLE. One bug there corrupts everything.**

---

## Inside-Out Order

```
Layer 0: Core math (svd, qr, eig)     ← ALL must reach L3 first
Layer 1: Building blocks (MPS, MPO)   ← Only after Layer 0 complete
Layer 2: Algorithms (VUMPS)           ← Only after Layer 1 complete
Layer 3: API                          ← Last
```

**You CANNOT start Layer N until ALL of Layer N-1 is verified.**

Consult Translation Planner before starting any module.

---

## Triangular Confrontation

```
        Doc (hypothesis)
         ↗️      ↖️
    challenge  challenge
       ↙️          ↘️
Source ←───oracle───→ Target
```

- **Doc-Writer**: Generates hypothesis (L0)
- **Translator**: Challenges doc, follows source (L0)
- **Verifier**: Tests target vs source (oracle → L2)
- **Attacker**: Tries to break all edges (survival → L3)

**Truth emerges from surviving disagreement.**

Read: `patterns/triangular-confrontation.md`

---

## Verification Levels

| Level | Name | How to Reach |
|-------|------|--------------|
| L0 | draft | Just written by agent |
| L1 | cross-checked | Another agent reviewed |
| L2 | tested | Oracle tests pass (compare vs source) |
| L3 | adversarial | Attacker agent FAILED to break it |
| L4 | proven | + Human review |

**Any challenge immediately downgrades to L0.**

Read: `VERIFICATION_LEVELS.md`

---

## Equivalence Types

| Type | Definition | Testing Strategy |
|------|------------|------------------|
| E5 | bit-identical | Exact match |
| E4 | within ε | rtol/atol tolerance |
| E3 | semantically same | Invariant checks (phase, sign) |
| E2 | same behavior | Convergence tests |
| E1 | same distribution | Statistical tests |
| E0 | bounded difference | Bound checks |

**Attacker calibrates attacks based on equivalence type.**

Read: `EQUIVALENCE_TYPES.md`

---

## When Uncertain

```
1. SPAWN Knowledge Oracle → "Check if we have a decision on {topic}"
2. If found → use stored answer
3. If not found → submit to human review queue (don't block!)
4. Continue with other work
5. Next session: check resolved items
```

**DO NOT GUESS. DO NOT SKIP. ASK OR QUEUE.**

---

## Source is READ-ONLY

**NEVER modify anything under `src` path from orchestra.yaml.**

---

## Key Files

| File | Purpose |
|------|---------|
| `orchestra.yaml` | Project declaration |
| `notes/knowledge_base.md` | Permanent human knowledge |
| `notes/human_review_queue.md` | Async human decisions |
| `notes/conceptual_map.yaml` | Module layer classification |
| `notes/verification_state.yaml` | Current level of each module |
| `notes/translation_plan.yaml` | What to do next |
| `tests/ground_truth/` | Oracle data from source |

---

## Quick Reference: Spawning Agents

### Get Strategic Direction
```
Task: "Read agents/00-orchestration/translation-planner.md then:
       Status report - what should we work on next?"
```

### Document a Function
```
Task: "Read agents/04-documentation/doc-writer.md then:
       Document {function} from {source_path}
       Output hypothesis to docs/{function}.md"
```

### Translate a Function
```
Task: "Read agents/03-translation/source-to-target.md then:
       Translate {function} from {source_path}
       Challenge docs/{function}.md against source
       Output to {dst}/{module}.py"
```

### Write Oracle Tests
```
Task: "Read agents/05-verification/equivalence-prover.md then:
       Write oracle tests for {function}
       Generate ground truth from source
       Output to tests/test_{function}.py"
```

### Attack Translation (L3)
```
Task: "Read agents/05-verification/equivalence-prover.md then:
       ATTACK {function} - find inputs where target ≠ source
       Try: boundary, degenerate, random stress
       Report to notes/attacks/{function}.yaml"
```

### Consult Knowledge
```
Task: "Read agents/00-orchestration/human-review-gate.md then:
       Check knowledge_base.md for: {question}
       If not found, add to review queue"
```

---

## Remember

1. **You are conductor** — orchestrate, don't code
2. **One function at a time** — no bulk translation
3. **Blocking gates** — core math must be L3
4. **Inside-out** — layers in order
5. **Triangular confrontation** — agents challenge each other
6. **Oracle tests** — compare against source, not just "runs"
7. **Atomic commits** — code + test + doc per function
8. **Knowledge oracle** — check before asking human again
