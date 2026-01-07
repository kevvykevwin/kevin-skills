---
name: test-generator
description: Generate executable test files from spec test cases. Use after build is complete and spec contains a Test Cases section. Reads spec, detects test framework from codebase, generates and runs tests.
---

# Test Generator Skill

Convert spec test cases into executable, runnable tests.

## Core Philosophy

1. **Spec is truth** - Tests verify the spec, not implementation details
2. **Tests must run** - Generated tests are executed immediately to confirm they work
3. **Match the codebase** - Use whatever test framework already exists
4. **Minimal mocking** - Prefer integration tests over heavily mocked unit tests

## When to Use

- After build is complete
- Spec has a `## Test Cases` section with input/output tables
- Before running verification-loop (tests become part of verification)

## Prerequisites

- Spec file with `## Test Cases` section
- Completed implementation to test against
- Test framework installed (or install it)

## Test Generation Process

### Step 1: Detect Test Framework

Check codebase for existing test setup:

| Check | Framework |
|-------|-----------|
| `jest.config.*` or `"jest"` in package.json | Jest |
| `vitest.config.*` or `"vitest"` in package.json | Vitest |
| `pytest.ini` or `pyproject.toml` with pytest | Pytest |
| `*_test.go` files | Go testing |
| `Cargo.toml` with `[dev-dependencies]` | Rust (cargo test) |

If no framework exists:
- JavaScript/TypeScript → install Vitest (lighter than Jest)
- Python → install Pytest
- Ask user for preference if ambiguous

### Step 2: Parse Test Cases from Spec

Extract from spec's `## Test Cases` section:

```markdown
### User Authentication
| Input | Expected Output | Notes |
|-------|-----------------|-------|
| valid email + valid password | session token returned | Happy path |
| invalid password | 401 error, no token | |
| malformed email | 400 error, validation message | |
```

Becomes structured data:
```
Feature: User Authentication
Cases:
  - input: valid email + valid password
    expected: session token returned
    type: happy_path
  - input: invalid password
    expected: 401 error, no token
    type: error
  - input: malformed email
    expected: 400 error, validation message
    type: validation
```

### Step 3: Generate Test File

#### Naming Convention
- `[feature].test.ts` / `[feature].test.js` (JS/TS)
- `test_[feature].py` (Python)
- `[feature]_test.go` (Go)

#### Test Structure

```typescript
// Example: auth.test.ts

describe('User Authentication', () => {
  describe('happy path', () => {
    it('returns session token for valid credentials', async () => {
      const result = await login('user@example.com', 'validpass');
      expect(result.token).toBeDefined();
    });
  });

  describe('error cases', () => {
    it('returns 401 for invalid password', async () => {
      await expect(login('user@example.com', 'wrongpass'))
        .rejects.toThrow(/401/);
    });

    it('returns 400 for malformed email', async () => {
      await expect(login('not-an-email', 'password'))
        .rejects.toThrow(/400/);
    });
  });
});
```

### Step 4: Run Tests

Execute immediately after generation:

```bash
# JS/TS
npm test -- --testPathPattern="[feature]"

# Python
pytest test_[feature].py -v

# Go
go test -run [Feature] -v
```

### Step 5: Fix Failing Tests

If tests fail on first run:
1. Check if test logic matches spec intent
2. Check if implementation actually meets spec
3. Distinguish test bug vs implementation bug

Report back which:
- Tests pass (implementation works)
- Tests fail due to implementation gap (verification-loop will catch)
- Tests fail due to test bug (fix the test)

## Test Generation Prompt (for subagent)

```
You are a test generator. Create executable tests from spec test cases.

SPEC FILE: [path]
CODEBASE: [relevant paths]
TEST FRAMEWORK: [detected or specified]

Instructions:
1. Read the ## Test Cases section from the spec
2. Generate ONE test file covering all cases
3. Use descriptive test names matching the spec language
4. Group by feature/function as defined in spec
5. Include setup/teardown if needed
6. Do NOT test implementation details not in spec

Output:
1. The test file content
2. Command to run the tests
3. Any dependencies that need installing
```

## Test Quality Checks

Before finalizing generated tests:
- [ ] Every spec test case has a corresponding test
- [ ] Test names are descriptive (readable as documentation)
- [ ] Happy path tested first, then errors
- [ ] No implementation details tested (only spec behaviors)
- [ ] Tests actually run (no syntax errors)
- [ ] Tests are deterministic (no flaky timing issues)

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Testing private methods | Couples to implementation | Test public behavior only |
| Over-mocking | Tests don't catch real bugs | Prefer integration tests |
| Ignoring spec edge cases | Incomplete coverage | One test per spec row |
| Copy-pasting test logic | DRY violation | Extract test helpers |
| Testing framework, not code | Wasted effort | Only test your code |

## Output Template

After generating tests, report:

```markdown
## Test Generation Complete

**File created:** `[path/to/test/file]`
**Framework:** [Jest/Vitest/Pytest/etc.]

### Test Coverage
| Spec Test Case | Test Function | Status |
|----------------|---------------|--------|
| [case from spec] | [test name] | ✅ Generated |

### Run Command
\`\`\`bash
[command to run tests]
\`\`\`

### Dependencies Added
- [any new packages installed]

### Run Results
- Total: X tests
- Passing: Y
- Failing: Z

### Failing Tests (if any)
| Test | Failure Reason | Likely Cause |
|------|----------------|--------------|
| [name] | [error] | Test bug / Implementation gap |
```

## Integration

Pairs with:
- `spec-writing` skill - Provides the Test Cases section this reads
- `verification-loop` skill - Can run generated tests as verification method
- `code-review` - Reviewer can check test quality
