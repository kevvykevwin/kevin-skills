---
name: adversarial-spec
description: Iteratively refine product specs through multi-model debate until consensus. Claude actively participates alongside GPT, Gemini, Grok, and other models. Includes interview mode, early agreement verification, and session persistence.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Adversarial Spec Development

Refine product specifications through structured debate among multiple LLMs until consensus emerges. Claude actively participates as a critic and contributor, not merely orchestrating external models.

## Core Philosophy

A single LLM reviewing a spec will miss things. Multiple LLMs debating a spec will catch gaps, challenge assumptions, and surface edge cases.

## Requirements

- Python 3.10+
- `litellm` package (`pip install litellm`)
- API keys for at least one supported provider

## Supported Providers

| Provider | Environment Variable | Example Models |
|----------|---------------------|----------------|
| OpenAI | `OPENAI_API_KEY` | gpt-4o, gpt-4-turbo, o1 |
| Google | `GEMINI_API_KEY` | gemini/gemini-2.0-flash |
| xAI | `XAI_API_KEY` | xai/grok-3, xai/grok-beta |
| Mistral | `MISTRAL_API_KEY` | mistral/mistral-large |
| Groq | `GROQ_API_KEY` | groq/llama-3.3-70b-versatile |
| Deepseek | `DEEPSEEK_API_KEY` | deepseek/deepseek-chat |
| Zhipu | `ZHIPUAI_API_KEY` | zhipu/glm-4 |

Check available providers:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py providers
```

## Document Types

**PRD (Product Requirements Document)** - For product managers, stakeholders, designers
- Executive Summary, Problem Statement, User Personas
- User Stories, Functional/Non-Functional Requirements
- Success Metrics, Scope Boundaries, Dependencies, Risks

**Technical Specification** - For developers and architects
- System Architecture, Component Design, API Contracts
- Data Models, Infrastructure, Security Considerations
- Error Handling, Performance SLAs, Deployment Strategy

## Process Overview

### Step 0: Gather Input & Interview Option

Ask the user:
1. Document type: PRD or Technical Specification?
2. Starting point: existing file path OR describe the product concept?
3. Interview mode: conduct in-depth requirements gathering? (optional)

If interview mode is selected, ask probing questions about:
- Problem context and user pain points
- Target users and stakeholders
- Core functional requirements
- Technical constraints and preferences
- UI/UX considerations
- Known tradeoffs and risks
- Success criteria and metrics

### Step 1: Load or Generate Initial Document

If user provided a file path:
```bash
cat /path/to/existing/spec.md
```

If user described a concept, generate a complete initial specification following the appropriate document type structure. Present the draft and ask for approval before proceeding.

### Step 2: Model Selection

Check available API keys and present models as options:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py providers
```

Ask user to select opponent models (can be multiple). More models = stricter convergence.

### Step 3: Opponent Critique

Run the critique with selected models:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models MODEL1,MODEL2 \
  --doc-type prd|tech \
  < current_spec.md
```

### Step 4: Active Participation & Iteration

After receiving opponent critiques, Claude MUST:

1. **Review opponent feedback** - Evaluate each critique for validity
2. **Provide independent critique** - Find issues opponents missed
3. **State agreement/disagreement** - Explicitly agree or disagree with specific points
4. **Synthesize revisions** - Incorporate valid feedback into the spec
5. **Explain reasoning** - Document why changes were made or rejected

Track contributions clearly:
- Issues accepted from each model
- Claude's independent findings
- Rejected feedback with justification
- User clarifications needed

If models agree too early (rounds 1-2), apply skepticism:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models MODEL \
  --doc-type prd|tech \
  --press \
  < current_spec.md
```

### Step 5: Convergence Loop

Continue until ALL models AND Claude agree the spec is production-ready.

Convergence rules:
- Maximum 10 rounds per cycle
- ALL participants must agree
- No premature agreement accepted
- Quality over speed

### Step 6: Finalization

When consensus is reached:
1. Perform final quality checks (completeness, consistency, clarity, actionability)
2. Output polished document to terminal
3. Save to `spec-output.md` or `tech-spec-output.md`

### Step 7: User Review Period

Present the finalized document and ask:
1. **Accept** - Document is ready for implementation
2. **Request changes** - Iterate without full debate cycle
3. **Run another cycle** - Additional debate with same or different models

### Step 8: PRD to Tech Spec (Optional)

If completing a PRD, offer to generate and debate a corresponding Technical Specification.

## Advanced Features

### Focus Areas

Direct models to prioritize specific concerns:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --focus security \
  < spec.md
```

Available focus areas:
- `security` - Auth, input validation, encryption, vulnerabilities
- `scalability` - Horizontal scaling, sharding, caching, load balancing
- `performance` - Latency targets, throughput, optimization
- `ux` - User journeys, accessibility, error states
- `reliability` - Failure modes, circuit breakers, SLAs
- `cost` - Infrastructure costs, efficiency, resource utilization

### Model Personas

Request critiques from specific professional perspectives:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --persona security-engineer \
  < spec.md
```

Available personas:
- `security-engineer` - Thinks like an attacker, paranoid about edge cases
- `oncall-engineer` - Cares about observability and debugging at 3am
- `junior-developer` - Flags ambiguity and tribal knowledge assumptions
- `qa-engineer` - Identifies missing test scenarios and edge cases
- `site-reliability` - Focuses on operational concerns
- `product-manager` - Reviews user value and success metrics
- `data-engineer` - Examines data models and ETL implications
- `mobile-developer` - API design from mobile perspective
- `accessibility-specialist` - WCAG compliance and inclusive design
- `legal-compliance` - Data privacy and regulatory compliance

### Context Injection

Include existing documents that the spec must align with:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --context existing-api.md,data-schema.sql \
  < spec.md
```

### Session Persistence

Save and resume debate sessions:
```bash
# Start with session name
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --session my-feature \
  < spec.md

# Resume later
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --resume my-feature
```

Checkpoints are saved automatically in `.adversarial-spec-checkpoints/`

### Preserve Intent Mode

Protect intentional unconventional choices:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --preserve-intent \
  < spec.md
```

This requires models to:
- Quote exact text they want to remove/change
- Justify concrete harms, not mere preferences
- Distinguish errors from stylistic differences

### Cost Tracking

View token usage and costs during debate:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o,gemini/gemini-2.0-flash \
  --doc-type tech \
  < spec.md
```

Costs are displayed per-model after each round.

### Saved Profiles

Save frequently used configurations:
```bash
# Save a profile
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py save-profile strict-security \
  --models gpt-4o,gemini/gemini-2.0-flash \
  --focus security \
  --doc-type tech

# Use a profile
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --profile strict-security \
  < spec.md

# List profiles
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py profiles
```

### Diff Between Rounds

Compare spec versions:
```bash
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py diff \
  --previous round1.md \
  --current round2.md
```

### Export Tasks

Extract actionable items from finalized specs:
```bash
# Human-readable format
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py export-tasks \
  --doc-type prd \
  < spec.md

# JSON for issue trackers
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py export-tasks \
  --doc-type prd \
  --json \
  < spec.md
```

### AWS Bedrock Support

Route all calls through Bedrock for enterprise compliance:
```bash
# Enable Bedrock
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py bedrock enable --region us-east-1

# Add models
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py bedrock add-model claude-3-sonnet

# Check status
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py bedrock status

# Disable
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py bedrock disable
```

### Telegram Integration (Optional)

Enable real-time notifications:
```bash
# Setup
python3 ~/.claude/skills/adversarial-spec/scripts/telegram_bot.py setup

# Use with debate
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --telegram \
  < spec.md
```

Set environment variables:
- `TELEGRAM_BOT_TOKEN` - From @BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID

## Quick Reference

```bash
# Check available providers
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py providers

# Basic critique
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type prd \
  < spec.md

# Multi-model with focus
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o,gemini/gemini-2.0-flash,xai/grok-3 \
  --doc-type tech \
  --focus security \
  < spec.md

# With persona and context
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique \
  --models gpt-4o \
  --doc-type tech \
  --persona oncall-engineer \
  --context existing-api.md \
  < spec.md

# Resume session
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py critique --resume my-session

# List all options
python3 ~/.claude/skills/adversarial-spec/scripts/debate.py --help
```

## Output

Final documents are:
- Complete and fully structured per document type
- Verified through unanimous model consensus
- Production-ready for stakeholder distribution
- Available in terminal and saved to file

Debate summaries include:
- Rounds completed
- Participating models
- Claude's specific contributions
- Total costs
- Key refinements achieved
