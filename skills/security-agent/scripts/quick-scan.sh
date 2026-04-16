#!/bin/bash

# Security Quick Scan Script
# Run before every deploy to catch critical issues
# Usage: ./quick-scan.sh [project_path] [--verbose] [--with-helpers]

set -e

VERBOSE=""
WITH_HELPERS=""
ISSUES_FOUND=0
CRITICAL_FOUND=0
MANUAL_REVIEW_FOUND=0

# If first arg is a flag, default PROJECT_PATH to "." and parse all args as flags.
# Otherwise take first arg as path and parse the rest.
if [[ "${1:-}" == --* ]]; then
    PROJECT_PATH="."
    FLAG_ARGS=("$@")
else
    PROJECT_PATH="${1:-.}"
    FLAG_ARGS=("${@:2}")
fi

for arg in "${FLAG_ARGS[@]}"; do
    if [ "$arg" = "--verbose" ]; then
        VERBOSE=1
    elif [ "$arg" = "--with-helpers" ]; then
        WITH_HELPERS=1
    fi
done

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "🔒 Security Quick Scan"
echo "========================================"
echo "Project: $PROJECT_PATH"
echo "Date: $(date)"
echo "----------------------------------------"

# Function to log findings
log_finding() {
    local severity=$1
    local category=$2
    local message=$3
    local location=$4

    if [ "$severity" = "CRITICAL" ]; then
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
        CRITICAL_FOUND=$((CRITICAL_FOUND + 1))
        echo -e "${RED}🔴 CRITICAL${NC} [$category] $message"
    elif [ "$severity" = "HIGH" ]; then
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
        echo -e "${YELLOW}🟠 HIGH${NC} [$category] $message"
    elif [ "$severity" = "MANUAL-REVIEW" ]; then
        MANUAL_REVIEW_FOUND=$((MANUAL_REVIEW_FOUND + 1))
        echo -e "${BLUE}🔵 MANUAL-REVIEW${NC} [$category] $message"
    else
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
        echo -e "🟡 MEDIUM [$category] $message"
    fi

    if [ -n "$location" ]; then
        echo "   Location: $location"
    fi
}

# Check 1: Secrets in code
echo ""
echo "📋 Check 1: Secrets Detection"
echo "----------------------------------------"

SECRETS_PATTERN='(password|passwd|secret|api_key|apikey|api-key|token|private_key|privatekey|aws_access|aws_secret|stripe_sk|sk_live_|sk_test_|gh_token|github_token)'

# Exclude common false positives
SECRETS_RESULTS=$(grep -rniE "$SECRETS_PATTERN" "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" \
    --include="*.py" --include="*.go" --include="*.rb" --include="*.php" \
    --include="*.json" --include="*.yaml" --include="*.yml" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor \
    --exclude-dir=__pycache__ --exclude-dir=.next --exclude-dir=dist \
    --exclude="*.lock" --exclude="package-lock.json" \
    2>/dev/null || true)

if [ -n "$SECRETS_RESULTS" ]; then
    # Filter out likely false positives (config keys, schema definitions)
    FILTERED=$(echo "$SECRETS_RESULTS" | grep -viE '(schema|type:|interface |class |function |def |const.*=.*\{|example|sample|placeholder|your_|YOUR_|xxx|CHANGEME)' || true)

    if [ -n "$FILTERED" ]; then
        while IFS= read -r line; do
            log_finding "CRITICAL" "Secrets" "Potential secret in code" "$line"
        done <<< "$FILTERED"
    else
        echo -e "${GREEN}✓ No obvious secrets found${NC}"
    fi
else
    echo -e "${GREEN}✓ No secrets patterns detected${NC}"
fi

# Check 2: Dangerous functions
echo ""
echo "📋 Check 2: Dangerous Functions"
echo "----------------------------------------"

# JavaScript/TypeScript
JS_DANGEROUS=$(grep -rniE '(eval\s*\(|dangerouslySetInnerHTML|innerHTML\s*=|document\.write\s*\(|new\s+Function\s*\()' "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
    2>/dev/null || true)

if [ -n "$JS_DANGEROUS" ]; then
    while IFS= read -r line; do
        log_finding "HIGH" "Code Safety" "Dangerous function usage" "$line"
    done <<< "$JS_DANGEROUS"
else
    echo -e "${GREEN}✓ No dangerous JS functions found${NC}"
fi

# Python
PY_DANGEROUS=$(grep -rniE '(eval\s*\(|exec\s*\(|os\.system\s*\(|subprocess\.call.*shell\s*=\s*True|pickle\.loads)' "$PROJECT_PATH" \
    --include="*.py" \
    --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=venv --exclude-dir=.venv \
    2>/dev/null || true)

if [ -n "$PY_DANGEROUS" ]; then
    while IFS= read -r line; do
        log_finding "HIGH" "Code Safety" "Dangerous Python function" "$line"
    done <<< "$PY_DANGEROUS"
fi

# Check 3: SQL Injection Risk
echo ""
echo "📋 Check 3: SQL Injection Risk"
echo "----------------------------------------"

SQL_CONCAT=$(grep -rniE '(\+\s*["\x27].*SELECT|\+\s*["\x27].*INSERT|\+\s*["\x27].*UPDATE|f["\x27].*SELECT|f["\x27].*INSERT|\$\{.*\}.*SELECT)' "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" --include="*.py" \
    --exclude-dir=node_modules --exclude-dir=.git \
    2>/dev/null || true)

if [ -n "$SQL_CONCAT" ]; then
    while IFS= read -r line; do
        log_finding "CRITICAL" "Injection" "Potential SQL injection" "$line"
    done <<< "$SQL_CONCAT"
else
    echo -e "${GREEN}✓ No obvious SQL injection patterns${NC}"
fi

# Check 4: .env file exposure
echo ""
echo "📋 Check 4: Environment File Security"
echo "----------------------------------------"

# Check if .env is gitignored
if [ -f "$PROJECT_PATH/.gitignore" ]; then
    if grep -q "\.env" "$PROJECT_PATH/.gitignore"; then
        echo -e "${GREEN}✓ .env is in .gitignore${NC}"
    else
        log_finding "HIGH" "Configuration" ".env not in .gitignore"
    fi
else
    log_finding "MEDIUM" "Configuration" "No .gitignore file found"
fi

# Check for .env in git
if [ -d "$PROJECT_PATH/.git" ]; then
    ENV_IN_GIT=$(git -C "$PROJECT_PATH" ls-files | grep -E "^\.env$|\.env\.local$|\.env\.production$" 2>/dev/null || true)
    if [ -n "$ENV_IN_GIT" ]; then
        log_finding "CRITICAL" "Secrets" ".env file tracked in git" "$ENV_IN_GIT"
    fi
fi

# Check 5: Dependency vulnerabilities
echo ""
echo "📋 Check 5: Dependency Vulnerabilities"
echo "----------------------------------------"

# Node.js
if [ -f "$PROJECT_PATH/package.json" ]; then
    echo "Running npm audit..."
    cd "$PROJECT_PATH"

    # Run npm audit and capture output
    AUDIT_OUTPUT=$(npm audit --audit-level=high 2>&1 || true)

    if echo "$AUDIT_OUTPUT" | grep -q "found 0 vulnerabilities"; then
        echo -e "${GREEN}✓ No high/critical npm vulnerabilities${NC}"
    elif echo "$AUDIT_OUTPUT" | grep -qE "(high|critical)"; then
        log_finding "HIGH" "Dependencies" "npm audit found high/critical vulnerabilities"
        if [ -n "$VERBOSE" ]; then
            echo "$AUDIT_OUTPUT"
        fi
    else
        echo -e "${GREEN}✓ npm audit passed${NC}"
    fi

    cd - > /dev/null
fi

# Python
if [ -f "$PROJECT_PATH/requirements.txt" ] || [ -f "$PROJECT_PATH/pyproject.toml" ]; then
    if command -v pip-audit &> /dev/null; then
        echo "Running pip-audit..."
        PIP_AUDIT=$(pip-audit -r "$PROJECT_PATH/requirements.txt" 2>&1 || true)

        if echo "$PIP_AUDIT" | grep -q "No known vulnerabilities"; then
            echo -e "${GREEN}✓ No Python vulnerabilities found${NC}"
        elif echo "$PIP_AUDIT" | grep -qE "(HIGH|CRITICAL)"; then
            log_finding "HIGH" "Dependencies" "pip-audit found vulnerabilities"
        fi
    else
        echo "pip-audit not installed, skipping Python check"
    fi
fi

# Check 6: Security headers (if URL provided)
if [ -n "$CHECK_URL" ]; then
    echo ""
    echo "📋 Check 6: Security Headers"
    echo "----------------------------------------"

    HEADERS=$(curl -sI "$CHECK_URL" 2>/dev/null || true)

    if [ -n "$HEADERS" ]; then
        # Check HSTS
        if echo "$HEADERS" | grep -qi "strict-transport-security"; then
            echo -e "${GREEN}✓ HSTS enabled${NC}"
        else
            log_finding "HIGH" "Headers" "Missing Strict-Transport-Security header"
        fi

        # Check CSP
        if echo "$HEADERS" | grep -qi "content-security-policy"; then
            echo -e "${GREEN}✓ CSP enabled${NC}"
        else
            log_finding "MEDIUM" "Headers" "Missing Content-Security-Policy header"
        fi

        # Check X-Frame-Options
        if echo "$HEADERS" | grep -qi "x-frame-options"; then
            echo -e "${GREEN}✓ X-Frame-Options set${NC}"
        else
            log_finding "MEDIUM" "Headers" "Missing X-Frame-Options header"
        fi
    fi
fi

# Check 7: Helper File Triage (opt-in via --with-helpers)
if [ -n "$WITH_HELPERS" ]; then
    echo ""
    echo "📋 Check 7: Helper File Triage (--with-helpers)"
    echo "----------------------------------------"

    HELPER_DIRS=("utils" "helpers" "lib" "common" "shared")

    # Parallel arrays (bash 3.2 compatible, no associative arrays)
    HELPER_CAT_NAMES=(sanitizer crypto merge_clone url_fetch deserialization path auth random redirect template)
    HELPER_CAT_REGEX=(
        "(sanitize|escape|clean|strip)"
        "(hash|encrypt|decrypt|generateToken|randomToken|timingSafeCompare)"
        "(deepMerge|deepAssign|deepExtend|deepClone|cloneDeep)"
        "(fetchUrl|downloadFile|proxyRequest|sendRequest|httpGet)"
        "(parseYaml|parseJson|unpickle|deserialize)"
        "(readUserFile|resolveUserPath|joinUserPath)"
        "(requireAuth|verifyJwt|checkPermission|assertOwner)"
        "(generateUUID|randomToken|generateNonce|generateId)"
        "(redirectTo|sendRedirect|handleReturnUrl)"
        "(renderUnsafe|dangerousRender|rawHtml)"
    )

    HELPER7_ANY_FOUND=0
    i=0
    while [ $i -lt ${#HELPER_CAT_NAMES[@]} ]; do
        category="${HELPER_CAT_NAMES[$i]}"
        REGEX="${HELPER_CAT_REGEX[$i]}"

        for dir in "${HELPER_DIRS[@]}"; do
            SEARCH_PATH="$PROJECT_PATH/$dir"
            [ -d "$SEARCH_PATH" ] || continue

            # Match exported/top-level function definitions
            MATCHES=$(grep -rniE "^(export (const|function)|function|def|public)\s+${REGEX}" "$SEARCH_PATH" \
                --include="*.js" --include="*.ts" --include="*.py" \
                --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ \
                --exclude-dir=venv --exclude-dir=.venv \
                2>/dev/null || true)

            if [ -n "$MATCHES" ]; then
                HELPER7_ANY_FOUND=1
                while IFS= read -r line; do
                    log_finding "MANUAL-REVIEW" "Helper Triage" "Category: $category" "$line"
                done <<< "$MATCHES"
            fi
        done
        i=$((i + 1))
    done

    if [ "$HELPER7_ANY_FOUND" -eq 0 ]; then
        echo -e "${GREEN}✓ No helper security-sensitive functions found in util dirs${NC}"
    fi
fi

# Check 8: AI/ML Code P1 Patterns (ALWAYS-ON)
echo ""
echo "📋 Check 8: AI/ML Code P1 Patterns"
echo "----------------------------------------"

CHECK8_ANY_FOUND=0

# 8a: trust_remote_code=True
TRUST_REMOTE=$(grep -rniE 'trust_remote_code\s*=\s*True' "$PROJECT_PATH" \
    --include="*.py" --include="*.ipynb" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ \
    --exclude-dir=venv --exclude-dir=.venv \
    2>/dev/null || true)

if [ -n "$TRUST_REMOTE" ]; then
    CHECK8_ANY_FOUND=1
    while IFS= read -r line; do
        log_finding "CRITICAL" "AI/ML" "trust_remote_code=True (RCE via remote code execution)" "$line"
    done <<< "$TRUST_REMOTE"
fi

# 8b: yaml.load without safe_load
# Match yaml.load( NOT preceded by safe_ (captures yaml.load, rejects yaml.safe_load).
# Known limitation: aliased imports (`from yaml import load as x`) won't be caught; document as manual-review.
YAML_UNSAFE=$(grep -rniE '(^|[^a-zA-Z_.])yaml\.load\s*\(' "$PROJECT_PATH" \
    --include="*.py" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ \
    --exclude-dir=venv --exclude-dir=.venv \
    2>/dev/null || true)

if [ -n "$YAML_UNSAFE" ]; then
    CHECK8_ANY_FOUND=1
    while IFS= read -r line; do
        log_finding "CRITICAL" "AI/ML" "yaml.load without safe_load (deserialization RCE)" "$line"
    done <<< "$YAML_UNSAFE"
fi

# 8c: pickle.loads
PICKLE_LOADS=$(grep -rniE 'pickle\.loads\s*\(' "$PROJECT_PATH" \
    --include="*.py" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ \
    --exclude-dir=venv --exclude-dir=.venv \
    2>/dev/null || true)

if [ -n "$PICKLE_LOADS" ]; then
    CHECK8_ANY_FOUND=1
    while IFS= read -r line; do
        log_finding "CRITICAL" "AI/ML" "pickle.loads (deserialization RCE)" "$line"
    done <<< "$PICKLE_LOADS"
fi

# 8d: torch.load without weights_only
TORCH_LOADS=$(grep -rniE 'torch\.load\s*\(' "$PROJECT_PATH" \
    --include="*.py" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ \
    --exclude-dir=venv --exclude-dir=.venv \
    2>/dev/null || true)

if [ -n "$TORCH_LOADS" ]; then
    while IFS= read -r line; do
        if ! echo "$line" | grep -q 'weights_only'; then
            CHECK8_ANY_FOUND=1
            log_finding "CRITICAL" "AI/ML" "torch.load without weights_only=True (CVE-2026-24747 class)" "$line"
        fi
    done <<< "$TORCH_LOADS"
fi

if [ "$CHECK8_ANY_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✓ No AI/ML P1 patterns found${NC}"
fi

# Check 9: Weak Randomness in Security Context
echo ""
echo "📋 Check 9: Weak Randomness in Security Context"
echo "----------------------------------------"

RANDOM_FILES=$(grep -rlE 'Math\.random\s*\(\)' "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
    2>/dev/null || true)

CHECK9_ANY_FOUND=0
if [ -n "$RANDOM_FILES" ]; then
    while IFS= read -r f; do
        [ -z "$f" ] && continue
        if echo "$f" | grep -qiE '(token|auth|session|nonce|password|reset|uuid|crypto)' \
           || grep -qiE '(token|auth|session|nonce|password|reset)' "$f" 2>/dev/null; then
            LINE=$(grep -nE 'Math\.random\s*\(\)' "$f" 2>/dev/null | head -1)
            CHECK9_ANY_FOUND=1
            log_finding "HIGH" "Crypto" "Math.random() in security context (use crypto.randomBytes / crypto.randomUUID)" "$f: $LINE"
        fi
    done <<< "$RANDOM_FILES"
fi

if [ "$CHECK9_ANY_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✓ No weak randomness in security-sensitive files${NC}"
fi

# Check 10: JWT Algorithm Configuration
echo ""
echo "📋 Check 10: JWT Algorithm Configuration"
echo "----------------------------------------"

CHECK10_ANY_FOUND=0

# 10a: algorithms: none (downgrade attack)
JWT_NONE=$(grep -rniE "algorithms['\"]?\s*[:=]\s*\[?\s*['\"]?none" "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" --include="*.py" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=__pycache__ \
    2>/dev/null || true)

if [ -n "$JWT_NONE" ]; then
    CHECK10_ANY_FOUND=1
    while IFS= read -r line; do
        log_finding "CRITICAL" "JWT" "JWT algorithm set to 'none' (algorithm downgrade attack)" "$line"
    done <<< "$JWT_NONE"
fi

# 10b: jwt.verify without algorithm whitelist
JWT_VERIFY_FILES=$(grep -rlE 'jwt\.verify\s*\(' "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
    2>/dev/null || true)

if [ -n "$JWT_VERIFY_FILES" ]; then
    while IFS= read -r f; do
        [ -z "$f" ] && continue
        if ! grep -qE 'algorithms:\s*\[' "$f" 2>/dev/null; then
            CHECK10_ANY_FOUND=1
            LINE=$(grep -nE 'jwt\.verify\s*\(' "$f" 2>/dev/null | head -1)
            log_finding "HIGH" "JWT" "jwt.verify without algorithm whitelist (algorithm-confusion risk)" "$f: $LINE"
        fi
    done <<< "$JWT_VERIFY_FILES"
fi

if [ "$CHECK10_ANY_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✓ No JWT algorithm configuration issues found${NC}"
fi

# Check 11: Expanded Env & AI-Tool Config Leakage
echo ""
echo "📋 Check 11: Expanded Env & AI-Tool Config Leakage"
echo "----------------------------------------"

CHECK11_ANY_FOUND=0

# 11a: Additional env-file variants tracked in git
if [ -d "$PROJECT_PATH/.git" ]; then
    EXTRA_ENV_IN_GIT=$(git -C "$PROJECT_PATH" ls-files \
        | grep -E '^(\.env\.local|\.env\.production|\.env\.development|\.env\..*\.local)$' \
        2>/dev/null || true)
    if [ -n "$EXTRA_ENV_IN_GIT" ]; then
        CHECK11_ANY_FOUND=1
        while IFS= read -r f; do
            log_finding "CRITICAL" "Secrets" "Env-file variant tracked in git" "$f"
        done <<< "$EXTRA_ENV_IN_GIT"
    fi
fi

# 11b: MCP/AI-tool config files containing inline credentials
for cfg in ".mcp.json" ".cursor/mcp.json" ".claude/settings.local.json"; do
    if [ -f "$PROJECT_PATH/$cfg" ]; then
        if grep -qE '(sk-[a-zA-Z0-9_-]{10,}|sk_live_|ANTHROPIC_API_KEY\s*[:=]|OPENAI_API_KEY\s*[:=])' "$PROJECT_PATH/$cfg" 2>/dev/null; then
            CHECK11_ANY_FOUND=1
            log_finding "CRITICAL" "Secrets" "AI-tool config contains inline credentials" "$PROJECT_PATH/$cfg"
        fi
    fi
done

if [ "$CHECK11_ANY_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✓ No expanded env or AI-tool config leakage found${NC}"
fi

# Check 12: Prototype Pollution Sinks
echo ""
echo "📋 Check 12: Prototype Pollution Sinks"
echo "----------------------------------------"

MERGE_FILES=$(grep -rlE 'function\s+(deepMerge|deepAssign|deepExtend|deepClone|merge)\s*\(' "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
    2>/dev/null || true)

CHECK12_ANY_FOUND=0
if [ -n "$MERGE_FILES" ]; then
    while IFS= read -r f; do
        [ -z "$f" ] && continue
        if ! grep -qE '(__proto__|constructor|prototype)' "$f" 2>/dev/null; then
            CHECK12_ANY_FOUND=1
            LINE=$(grep -nE 'function\s+(deepMerge|deepAssign|deepExtend|deepClone|merge)\s*\(' "$f" 2>/dev/null | head -1)
            log_finding "MEDIUM" "Prototype Pollution" "Deep-merge helper without __proto__/constructor/prototype guard" "$f: $LINE"
        fi
    done <<< "$MERGE_FILES"
fi

if [ "$CHECK12_ANY_FOUND" -eq 0 ]; then
    echo -e "${GREEN}✓ No unguarded deep-merge helpers found${NC}"
fi

# Check 13: Open Redirect Patterns
echo ""
echo "📋 Check 13: Open Redirect Patterns"
echo "----------------------------------------"

REDIRECT_HITS=$(grep -rniE 'res(ponse)?\.redirect\s*\(\s*req\.(query|params)\.' "$PROJECT_PATH" \
    --include="*.js" --include="*.ts" \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=dist \
    2>/dev/null || true)

if [ -n "$REDIRECT_HITS" ]; then
    while IFS= read -r line; do
        log_finding "HIGH" "Open Redirect" "Redirect to unvalidated user-controlled URL" "$line"
    done <<< "$REDIRECT_HITS"
else
    echo -e "${GREEN}✓ No open redirect patterns found${NC}"
fi

# Check 14: AI/LLM Dependency Detection (informational)
echo ""
echo "📋 Check 14: AI/LLM Dependency Detection"
echo "----------------------------------------"

AI_PATTERN='(anthropic|openai|langchain|llama-index|@modelcontextprotocol|transformers|torch|huggingface-hub)'
AI_MATCH=""
for manifest in "package.json" "requirements.txt" "pyproject.toml" "Pipfile"; do
    if [ -f "$PROJECT_PATH/$manifest" ]; then
        if grep -qiE "$AI_PATTERN" "$PROJECT_PATH/$manifest" 2>/dev/null; then
            AI_MATCH="$AI_MATCH $manifest"
        fi
    fi
done

if [ -n "$AI_MATCH" ]; then
    echo "AI_DEPS_DETECTED=1"
    echo "   Dependencies found in:$AI_MATCH"
    echo "   (Full Audit will dispatch ai-code-reviewer sub-agent)"
else
    echo -e "${GREEN}✓ No LLM dependencies detected${NC}"
fi

# Summary
echo ""
echo "========================================"
echo "📊 Scan Summary"
echo "========================================"
echo "Total issues found: $ISSUES_FOUND"
echo "Critical issues: $CRITICAL_FOUND"
if [ "$MANUAL_REVIEW_FOUND" -gt 0 ]; then
    echo "Manual-review items: $MANUAL_REVIEW_FOUND"
fi
echo ""

if [ $CRITICAL_FOUND -gt 0 ]; then
    echo -e "${RED}❌ SCAN FAILED - Critical issues must be fixed before deploy${NC}"
    exit 1
elif [ $ISSUES_FOUND -gt 0 ]; then
    echo -e "${YELLOW}⚠️  SCAN PASSED WITH WARNINGS - Review issues before deploy${NC}"
    exit 0
else
    echo -e "${GREEN}✅ SCAN PASSED - No issues found${NC}"
    exit 0
fi
