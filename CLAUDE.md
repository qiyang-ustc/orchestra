# Orchestra Translation Project

Read `orchestra.yaml` for project declaration.

## Rules

1. **Source is READ-ONLY** — Never modify files under `src`
2. **Target is local** — All writes go to `dst`
3. **Notes contain human knowledge** — Consult before making decisions

## Workflow

1. Read `orchestra.yaml` to understand the project
2. Analyze source code structure
3. Plan translation order (core math first, then building blocks, then algorithms)
4. For each module:
   - Document first (hypothesis)
   - Translate (challenge doc against source)
   - Verify (oracle + adversarial for core)
   - Commit atomically (code + test + doc)

## Verification Standards

- **Core math**: Must pass adversarial testing (L3)
- **Building blocks**: Must pass adversarial testing (L3)
- **Algorithms**: Oracle testing sufficient initially (L2)
- **Edge utilities**: Oracle testing sufficient (L2)

## When Uncertain

1. Check `notes/knowledge_base.md` first
2. If not found, ask human
3. Record decision for future

## Key Principle

**Triangular Confrontation**: Doc, Source, Target must all agree. Challenge inconsistencies.
