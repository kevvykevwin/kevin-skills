# /security-deep-audit — Scaffold (Not Yet Implemented)

## Status
Deferred. This skill is designed but not built. See trigger criteria below.

## Purpose
Commercial-SAST-grade security audit for pre-release, quarterly, and post-refactor use. Opt-in, heavyweight install. Complements the lightweight `/security-agent` skill (which is always-runnable with zero deps).

## When to Build
Build this skill if `/security-agent` (lightweight) misses findings that mattered across ≥3 separate incidents. Until then: YAGNI. Ship `/security-agent` changes first, run for 4-6 weeks, see which gaps are real.

Explicit trigger scenarios:
- A real vulnerability shipped that lightweight grep would never catch (e.g., taint flow through a helper chain)
- A client/compliance requirement mandates SARIF output
- Cost of false negatives > cost of install friction

## Deferred Components

### Shell-out pipeline
- Semgrep (`--config=p/default --config=p/secrets --config=p/owasp-top-ten`)
- Gitleaks (`protect --staged` for precommit, `git --log-opts=...` for prepush, full history for audit)
- OSV-Scanner (skip at precommit, `--lockfile=` at prepush, `scan source` at audit)
- modelscan + picklescan ≥0.0.31 (CVE 10155/10156/10157 fix) + fickling
- sarif-tools for aggregation

### Tiered performance targets (post cache-warm)
- `--tier=precommit`: <2s, staged files only, p/ci pack + gitleaks --staged
- `--tier=prepush`: <10s, diff vs origin/main, full packs + OSV lockfile + gitleaks 50 commits
- `--tier=audit`: no bound, full tree + sub-agent triage

### Infrastructure
- `tools.lock` with pinned versions + Cosign/Sigstore signature verification where shipped
- `scripts/install-tools.sh` per-tool resolver (venv → command -v → global → install), fail-open on missing, cache-warm final step
- `references/helper-categories.yaml` as single source of truth (id, name, regex, severity, semgrep-rule-id, p1 bool)
- Output to `~/.cache/security-deep-audit/<project-path-hash>/merged.sarif` — never pollute project tree

### Sub-agent pipeline over SARIF
- `helper-reviewer` consumes SARIF + helper-categories.yaml
- `ai-code-reviewer` conditional on LLM deps
- `supply-chain-reviewer` consumes OSV SARIF + lockfile diff
- `platform-auditor` + conditional `anticarding-auditor` + `threat-analyst` for e-comm
- Pre-filter SARIF to top-20 findings per category before sub-agent dispatch (token budget guard)
- Each sub-agent required to emit structured output: `file:line`, `broken-invariant`, `example-bypass-input`, `confidence`

### Fixture repo (`~/Projects/security-agent-fixture/`)
- Semgrep rule tests — good+bad pair per rule via `.test.yaml` (Semgrep native)
- `fixtures/p1-bypass-suite/` — 15+ variants per P1 rule (whitespace, multiline, comments, dicts, f-strings)
- `fixtures/triage-regression/` — 5-10 canonical helpers with expected LLM verdicts
- `fixtures/e2e-project/` — miniature repo for full `--tier=audit` integration test

### Safety + edge cases
- `.security-ignore` file + `// nosec rule-id` comment suppression
- Monorepo lockfile discovery (`**/package-lock.json` etc.)
- Git-less + `--no-follow-symlinks` safety pre-flight
- Giant-repo file-count caps per tier
- Degraded-run policy: any tool exit ≠ 0 blocks sub-agents from emitting "clean"
- `--refresh-tools` flag for emergent-CVE cache invalidation

## Avoid
**Trivy** — two supply-chain compromises March 2026. Prefer OSV-Scanner + Grype fallback.

## Research Sources
Gathered during DEEPEN pass, 2026-04-15:
- Semgrep vs CodeQL — Konvu 2026 comparison
- Gitleaks vs TruffleHog — AppSec Santa
- OSV-Scanner vs npm-audit — Jit
- ModelScan (Protect AI) — github.com/protectai/modelscan
- Fickling (Trail of Bits) — blog.trailofbits.com 2025-09
- PickleScan CVEs 10155/10156/10157 — TheHackerNews 2025-12
- SARIF 2.1.0 spec — OASIS
- OWASP DevSecOps pre-commit guidance
- Veracode 2025-2026 GenAI Code Security reports
- Lasso Security slopsquat research

## Decision Log
- 2026-04-15: Lightweight-vs-heavy scope assessed at 8/10 over-engineering. Decision: ship lightweight `/security-agent` expansion, scaffold this heavy skill for later.
