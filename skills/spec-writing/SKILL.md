---
name: spec-writing
description: Create verifiable software specifications with testable acceptance criteria. Use before building any feature, bug fix, or refactor. Ensures specs are structured for automated verification by QA subagents.
---

# Spec Writing Skill

Write specs that a verification agent can objectively check against.

## Core Philosophy

1. **If you can't test it, you can't spec it** - Every requirement must be verifiable
2. **Ambiguity is debt** - Unclear specs create rework; invest upfront
3. **Done means done** - Explicit completion criteria, not vibes
4. **Edge cases are requirements** - If it could happen, spec the behavior

## When to Use

- Before any new feature build
- Before bug fixes (spec the expected behavior)
- Before refactors (spec what must remain true)
- When inheriting unclear requirements

## Spec Writing Process

### Step 1: Clarify Scope

Before writing, answer:
- What problem does this solve?
- What is explicitly OUT of scope?
- Who/what will consume the output?

### Step 2: Define Acceptance Criteria

Each criterion must be:
- **Binary** - Pass or fail, no "partially done"
- **Observable** - Can be checked without reading code internals
- **Specific** - Numbers, states, or exact behaviors

Bad: "Page loads quickly"
Good: "Page renders in <2s on 3G throttle"

Bad: "Form validates input"
Good: "Form shows inline error within 200ms when email lacks @ symbol"

### Step 3: Enumerate Edge Cases

For each feature, explicitly document:
- Empty/null inputs
- Boundary values (0, 1, max, max+1)
- Error states and recovery
- Concurrent/race conditions (if applicable)
- Permission/auth edge cases

### Step 4: Define Done

Write a checklist that answers: "How does a verification agent confirm this is complete?"

## Spec Template

```markdown
# Spec: [Feature/Fix Name]

## Problem Statement
[1-2 sentences: What problem does this solve? Why now?]

## Out of Scope
- [Explicitly list what this does NOT include]

## Acceptance Criteria

### [Criterion 1: Descriptive Name]
- [ ] [Testable statement]
- [ ] [Testable statement]

### [Criterion 2: Descriptive Name]
- [ ] [Testable statement]

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| [Empty input] | [Specific response] |
| [Max value exceeded] | [Specific response] |
| [Unauthorized user] | [Specific response] |

## Definition of Done
All boxes checked = done. No exceptions.

- [ ] All acceptance criteria pass
- [ ] Edge cases handled per table above
- [ ] [Any additional: tests written, docs updated, etc.]

## Verification Notes
[Optional: Hints for the verification agent on how to test]

## Implementation Log
### Phase 1: [Status: Complete]
- Decision: Used X approach because Y
- Deviation: Changed Z per conversation on [date]
- Files created: list
```

3. **Then compact or start a new session.** Your next prompt can be:
```
Continue implementing [spec name]. Read the spec - the Implementation Log has context from previous sessions. We're starting Phase 2.
```

## Quality Checks

Before finalizing a spec:
- [ ] Every acceptance criterion is binary (pass/fail)
- [ ] No subjective words: "fast", "clean", "user-friendly", "properly"
- [ ] Edge cases enumerated (minimum 3)
- [ ] Out of scope section exists
- [ ] Definition of Done is a checkable list
- [ ] A stranger could verify completion without asking questions

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "Should work correctly" | Not testable | Specify exact behavior |
| Missing edge cases | Bugs ship | Enumerate boundaries |
| Scope creep in criteria | Never "done" | Use Out of Scope section |
| Implementation details | Over-constrains solution | Spec behavior, not code |
| Vague done definition | Rework loops | Checklist with binary items |

## Integration

Pairs with:
- `test-generator` skill - Converts Test Cases into executable tests post-build
- `verification-loop` skill - Subagent verifies against this spec
- `code-review` - Reviewers check code against acceptance criteria
