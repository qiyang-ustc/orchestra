# {{PROJECT_NAME}}: {{SOURCE_LANG}} → {{TARGET_LANG}} Translation

## Mission

Translate {{SOURCE_REPO}} to {{TARGET_LANG}} with {{N}}-way equivalence proof.

---

## Source & Target

```
SOURCE (READ-ONLY):
  {{SOURCE_PATH}}

TARGET:
  {{TARGET_PATH}}
```

---

## Equivalence Standard

For each module, prove equivalence across {{N}} dimensions:

| Check | Description | Verification Method |
|-------|-------------|---------------------|
| `C_S ≡ C_T` | Source code ≡ Target code | Output comparison |
| `T_S ≡ T_T` | Source test ≡ Target test | Same assertions |
| `D_S ≡ D_T` | Source doc ≡ Target doc | Semantic match |
| `C ↔ D` | Code-doc consistency | Doc describes code |
| `T ↔ D` | Test-doc consistency | Tests verify claims |

### Verification Levels

| Level | Name | Requirements |
|-------|------|--------------|
| **L0** | draft | Initial output, unverified |
| **L1** | cross-checked | Another agent confirmed, no challenges |
| **L2** | tested | Basic oracle tests pass |
| **L3** | adversarial | Survived adversarial attacks |
| **L4** | proven | Full triangle + adversarial + human review |

### Triangular Confrontation

```
        Doc (hypothesis)
         ↗️      ↖️
    challenge  challenge
       ↙️          ↘️
Source ←───oracle───→ Target
```

**Core rule: Later agents do NOT trust earlier outputs. Every claim must be independently verified.**

- Doc-Writer: generates hypothesis from source
- Translator: challenges doc against source while implementing
- Verifier: challenges all three edges

**A module is PROVEN only when all checks pass AND no unresolved challenges exist.**

---

## Orchestrator Protocol

**You are the ORCHESTRATOR. You dispatch tasks to sub-agents.**

### Session Start

```
@translation-planner status   → What's the current state? What should we do?
@human-review-gate            → Check resolved items (if any pending)
```

> **Note**: Use `/orchestra-init` skill for full environment verification (optional).

### Dispatch Rules

1. **Never block on human review** — skip and continue
2. **Parallelize aggressively** — same-level modules concurrent
3. **Document first, translate second** — understand before implement
4. **Triangular confrontation** — later agents challenge earlier outputs
5. **Atomic commits** — one function = one complete commit

### Human Review Protocol

When any agent encounters uncertainty:
```
1. Submit to queue (notes/human_review_queue.md)
2. Mark module as PENDING_HUMAN
3. IMMEDIATELY continue with next module
4. Report pending items at session end
```

---

## Sub-Agent Roster

| Category | Agent | Purpose |
|----------|-------|---------|
| orchestration | `translation-planner` | **Strategic brain**: conceptual map, verification state, failure propagation |
| orchestration | `session-init` | Environment check |
| orchestration | `progress-tracker` | Status tracking |
| orchestration | `human-review-gate` | Async human decisions |
| analysis | `codebase-scanner` | Build file index |
| analysis | `dependency-mapper` | Call graph + concept analysis |
| analysis | `legacy-archaeologist` | Analyze old code |
| preprocessing | `file-splitter` | Break large files |
| preprocessing | `refactor-advisor` | Identify cleanups |
| translation | `source-to-target` | Main translation (skeptical, challenges doc) |
| documentation | `doc-writer` | Generate hypothesis docs |
| verification | `equivalence-prover` | Adversarial attacker, prove correctness |
| debug | `code-verifier` | File state checks |

---

## Directory Structure

```
{{TARGET_PATH}}/
├── CLAUDE.md
├── {{PACKAGE_NAME}}/        # Translated code
├── tests/
│   ├── ground_truth/        # Source-generated reference data
│   └── test_*/              # Test modules
├── docs/
│   ├── {{SOURCE_LANG_LOWER}}/   # Source language docs
│   └── {{TARGET_LANG_LOWER}}/   # Target language docs
├── notes/
│   ├── human_review_queue.md
│   ├── decisions_log.md
│   └── module_status.yaml
└── scripts/
    └── generate_ground_truth.{{SOURCE_EXT}}
```

---

## Notes Protocol

### human_review_queue.md

```markdown
## PENDING
### [ID-XXX] file.ext - Brief description
- **Issue**: What's unclear
- **Options**: Possible decisions
- **Blocking**: What can't proceed
- **Status**: ⏸️ PENDING

## RESOLVED
### [ID-XXX] file.ext - Brief description
- **Decision**: What was decided
- **Date**: When
```

---

## Session Protocol

### START
```
@session-init
@progress-tracker
@human-review-gate
```

### DURING
- Dispatch parallel where possible
- Submit uncertainties immediately
- Update progress after each module

### END
```
@progress-tracker
Report: "X completed, Y pending, Z blocked"
```

---

## Do NOT

- Modify source files
- Block on human decisions
- Translate without understanding
- Skip equivalence checks

---

## Current Phase

`[ ] Phase 0: Setup & Analysis`

---

## Customization Notes

Replace these placeholders:
- `{{PROJECT_NAME}}`: Your project name
- `{{SOURCE_LANG}}`: Source language (Julia, MATLAB, etc.)
- `{{TARGET_LANG}}`: Target language (Python, Rust, etc.)
- `{{SOURCE_PATH}}`: Path to source repo
- `{{TARGET_PATH}}`: Path to target repo
- `{{N}}`: Number of equivalence dimensions (4, 6, etc.)
- `{{PACKAGE_NAME}}`: Python/target package name
- `{{SOURCE_EXT}}`: Source file extension (.jl, .m, etc.)
