---
name: devdocs-progress-update
description: Automatically update DevDocs/progress.md after completing development steps. Use after any meaningful code change, test run, or decision. Ensures state survives context breaks and session boundaries.
---

# DevDocs Progress Update Skill

Maintain persistent working memory by updating progress.md after each meaningful step.

## Core Philosophy

1. **If it's not written, it didn't happen** - Context will break; files survive
2. **Progress.md is ground truth** - First thing read after any interruption
3. **Atomic updates** - Update immediately after each step, not in batches
4. **Test state is authoritative** - Always verify against pytest, not memory

## When to Use

- After any code change (successful or failed)
- After running tests
- After making a decision
- Before ending a session
- When context feels full
- After recovering from compaction

## Prerequisites

- `DevDocs/` folder exists in project root
- `DevDocs/progress.md` file exists (create from template if not)
- pytest or equivalent test runner configured

## Update Process

### Step 1: Capture Current State

Run tests and capture the output:

```bash
# Get test summary
pytest --tb=short -q 2>&1 | tail -15

# Get git state
git status --short
git diff --stat
```

### Step 2: Determine Update Type

| Situation | Update Scope |
|-----------|--------------|
| Tests now passing that weren't | Full update + move item to completed |
| Tests still failing | Update "Last Action" with what was tried |
| New tests added | Update test count + next steps |
| Decision made | Update + add to decisions.md |
| Session ending | Full checkpoint update |
| Recovering from compaction | Verify/correct progress.md against reality |

### Step 3: Update progress.md

#### Minimal Update (after small step)

Update only these fields:
- **Last Action:** What was just done
- **Test state:** X/Y passing
- **Next Steps:** Reorder if needed

#### Full Update (after milestone or session end)

Update all fields:
- Current Status section
- Last Action with details
- Next Steps (reordered)
- Session Log entry
- Blockers if any
- Failed Approaches if relevant

### Step 4: Commit Checkpoint (Optional)

If tests are passing and change is meaningful:

```bash
git add DevDocs/progress.md
git commit -m "docs: checkpoint progress"
```

## progress.md Structure

```markdown
# Progress Log

> ⚠️ Read this FIRST after any context break.

## Current Status

**Working on:** [Current task - one line]
**Test state:** X/Y passing
**Blocked:** No | Yes: [reason]

## Last Action

[What was just completed or attempted - 1-3 sentences]

## Next Steps

1. [ ] [Immediate next task]
2. [ ] [Following task]
3. [ ] [Then this]

## Session Log

### [YYYY-MM-DD HH:MM]

**Accomplished:**
- [Bullet points of what got done]

**Commits:**
- `abc1234` - [message]

---

## Blockers

| Issue | Status | Notes |
|-------|--------|-------|
| [Issue] | 🔴/🟡/🟢 | [Context] |

## Failed Approaches

| Approach | Why It Failed | Date |
|----------|---------------|------|
| [What was tried] | [Why it didn't work] | [Date] |
```

## Update Templates

### After Successful Test Run

```markdown
## Current Status

**Working on:** [unchanged or next item]
**Test state:** [NEW COUNT] passing
**Blocked:** No

## Last Action

Implemented [feature/fix]. Tests now passing for [specific functionality].

## Next Steps

1. [ ] [Next uncompleted item]
2. [ ] [Following item]
```

### After Failed Attempt

```markdown
## Current Status

**Working on:** [unchanged]
**Test state:** X/Y passing (N failing)
**Blocked:** No

## Last Action

Attempted [approach] for [goal]. Failed because [reason].
Error: `[key error message]`

## Next Steps

1. [ ] Try [alternative approach]
2. [ ] [Rest unchanged]

## Failed Approaches

| Approach | Why It Failed | Date |
|----------|---------------|------|
| [What was tried] | [Specific reason] | [Today] |
```

### Session End Checkpoint

```markdown
## Current Status

**Working on:** [Current task]
**Test state:** X/Y passing
**Blocked:** [Yes/No]

## Last Action

[Final action of session]

## Next Steps

1. [ ] [EXACTLY what to do first next session]
2. [ ] [Second priority]
3. [ ] [Third priority]

## Session Log

### [YYYY-MM-DD HH:MM]

**Accomplished:**
- [Everything done this session]
- [Be specific enough to not repeat work]

**Commits:**
- `abc1234` - [message]
- `def5678` - [message]

**Notes for next session:**
[Anything important that isn't captured above]
```

## Automation Commands

### Quick Status Update

```bash
# One-liner to append test state
echo "Test state: $(pytest --tb=no -q 2>&1 | tail -1)"
```

### Verify progress.md Accuracy

```bash
# Compare claimed test state vs actual
grep "Test state:" DevDocs/progress.md
pytest --tb=no -q 2>&1 | tail -1
```

## Integration with Recovery Protocol

This skill produces the artifact that the recovery protocol consumes:

```
[Session ends]
    → devdocs-progress-update runs
    → progress.md updated

[New session / compaction]
    → Recovery protocol runs
    → Reads progress.md
    → Verifies against pytest
    → Resumes from Next Steps
```

## Quality Checks

Before finalizing any progress.md update:

- [ ] Test state matches actual `pytest` output
- [ ] "Last Action" is specific enough to not repeat
- [ ] "Next Steps" has clear, actionable first item
- [ ] No stale information from previous sessions
- [ ] Blockers section reflects reality

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague "Last Action" | Can't tell what was done | Include specific files/functions |
| Outdated test count | Misleads recovery | Always run pytest before updating |
| Empty "Next Steps" | No guidance after break | Always have at least one item |
| Batching updates | State lost if interrupted | Update after each step |
| Skipping failed approaches | Will retry same thing | Document every failure |

## Example: Full Update Cycle

**Before coding:**
```
Test state: 3/5 passing
Next Steps:
1. [ ] Implement high budget warning
```

**After implementing (tests now pass):**
```
Test state: 4/5 passing
Last Action: Added high_budget_warning() to validators/budget.py.
             Test test_high_budget_triggers_warning now passes.
Next Steps:
1. [ ] Implement negative budget handling
2. [ ] Refactor validation return structure
```

**After session:**
```
## Session Log

### 2026-01-11 10:30

**Accomplished:**
- Implemented high budget warning (4/5 tests passing)
- Refactored return structure to use dataclass

**Commits:**
- `a1b2c3d` - feat: add high budget warning
- `e4f5g6h` - refactor: use ValidationResult dataclass

**Notes for next session:**
One test remaining: negative budget handling. See spec edge cases table.
```

## Pairing With Other Skills

| Skill | Integration |
|-------|-------------|
| `spec-writing` | Progress tracks completion against spec criteria |
| `test-generator-post-build` | Update progress after tests generated |
| `security-scan` | Note scan results in session log |
| Recovery Protocol (CLAUDE.md) | Consumes progress.md on session start |
