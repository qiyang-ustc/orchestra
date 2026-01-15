# Orchestra Translation Project

Read `orchestra.yaml` for project declaration.

---

## CRITICAL: USE SUB-AGENTS

**You are the CONDUCTOR. You DO NOT translate code yourself.**

For EVERY function translation, spawn sub-agents:

```
1. SPAWN Doc-Agent    → Write documentation (hypothesis)
2. SPAWN Translator   → Write code (challenge doc against source)
3. SPAWN Verifier     → Write oracle tests
4. SPAWN Attacker     → Try to break it (for L3 targets)
5. YOU review results → Commit or iterate
```

**If you find yourself writing code directly, STOP. Spawn an agent instead.**

### How to Spawn Agents

Use the Task tool with specific prompts:

```
Task: "Document the svd() function"
→ Agent reads source, writes doc hypothesis

Task: "Translate svd() - challenge this doc against source"
→ Agent gets doc + source, writes code, flags inconsistencies

Task: "Write oracle test for svd() comparing against Julia output"
→ Agent creates test that calls source and compares

Task: "Attack svd() translation - find inputs where it fails"
→ Agent tries edge cases, boundary values, degenerate inputs
```

---

## CRITICAL RULES (BLOCKING)

### 1. ONE FUNCTION AT A TIME

**DO NOT bulk translate.** One function → verify → commit → next.

```
❌ WRONG: Translate 20 functions → commit all
✅ RIGHT: svd() → L3 verified → commit → qr() → L3 verified → commit → ...
```

### 2. VERIFICATION GATES

**You CANNOT proceed until current function reaches required level.**

| Layer | Required | Gate |
|-------|----------|------|
| Core math | **L3** | MUST spawn Attacker agent, survive attack |
| Building blocks | **L3** | MUST spawn Attacker agent |
| Algorithms | L2 | Oracle test agent sufficient |
| Utilities | L2 | Oracle test agent sufficient |

**L3 means: Attacker agent FAILED to break it.**

### 3. ORACLE TESTS ARE MANDATORY

Tests MUST compare against SOURCE output:

```python
# ❌ WRONG
def test_svd():
    assert result.shape == expected  # NOT oracle

# ✅ RIGHT
def test_svd_oracle():
    expected = load_julia_output("svd_case_1")  # Ground truth
    actual = svd(A)
    assert_close(actual, expected, rtol=1e-10)
```

### 4. INSIDE-OUT ORDER

```
Layer 0: Core math (svd, qr, eig)     ← ALL must reach L3 first
Layer 1: Building blocks (MPS, MPO)   ← Only after Layer 0 complete
Layer 2: Algorithms (VUMPS)           ← Only after Layer 1 complete
Layer 3: API                          ← Last
```

---

## Triangular Confrontation

**No agent trusts another. All outputs are hypotheses to challenge.**

```
        Doc (hypothesis)
         ↗️      ↖️
    challenge  challenge
       ↙️          ↘️
Source ←───oracle───→ Target
```

- **Doc-Agent**: Generates hypothesis from source
- **Translator**: Challenges doc while implementing (source is truth)
- **Verifier**: Tests target against source (oracle)
- **Attacker**: Tries to break all three edges

**Truth emerges from surviving disagreement.**

---

## Per-Function Workflow

```
1. SPAWN Doc-Agent     → Read source, write doc hypothesis
2. REVIEW doc          → Quick sanity check
3. SPAWN Translator    → Write code, report doc inconsistencies
4. SPAWN Verifier      → Write oracle tests
5. RUN tests           → Check if L2 reached
6. IF target is L3:
   6a. SPAWN Attacker  → Try to break it
   6b. IF breaks       → SPAWN Translator to fix → goto 5
   6c. IF survives     → L3 reached
7. COMMIT              → code + test + doc + report
8. NEXT function
```

---

## Verification Levels

| Level | Name | How to Reach |
|-------|------|--------------|
| L0 | draft | Just written |
| L1 | cross-checked | Another agent reviewed |
| L2 | tested | Oracle tests pass |
| L3 | adversarial | **Attacker agent failed to break it** |
| L4 | proven | + Human review |

---

## Source is READ-ONLY

**NEVER modify anything under `src` path.**

---

## When Stuck

1. Check `notes/knowledge_base.md`
2. If not found → **ASK HUMAN**
3. Record decision in knowledge_base.md

**DO NOT GUESS. DO NOT SKIP. ASK.**

---

## Agent Prompts Reference

### Doc-Agent
```
Read the source implementation of {function} at {path}.
Write documentation explaining:
- Purpose and mathematical operation
- Input/output shapes and types
- Edge cases and invariants
- Any gotchas (indexing, conventions)
This is a HYPOTHESIS to be challenged by Translator.
```

### Translator
```
Translate {function} from {source_lang} to {target_lang}.
You have: source code, doc hypothesis.
CHALLENGE the doc - if it conflicts with source, source wins.
Report any inconsistencies found.
Write clean, tested code.
```

### Verifier (Oracle Test)
```
Write oracle tests for {function}.
Tests MUST compare against source implementation output.
Load ground truth from Julia, compare Python output.
Use appropriate tolerance for float comparisons.
```

### Attacker (L3 only)
```
Attack the translation of {function}.
Your goal: find inputs where target ≠ source.
Try:
- Zero/empty inputs
- Very large/small values
- Degenerate cases
- Boundary conditions
- Random stress test
Report any failures found.
```
