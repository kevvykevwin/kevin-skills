#!/bin/bash

# Security Quick Scan Script
# Run before every deploy to catch critical issues
# Usage: ./quick-scan.sh [project_path] [--verbose]

set -e

PROJECT_PATH="${1:-.}"
VERBOSE="${2:-}"
ISSUES_FOUND=0
CRITICAL_FOUND=0

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
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
    
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
    
    if [ "$severity" = "CRITICAL" ]; then
        CRITICAL_FOUND=$((CRITICAL_FOUND + 1))
        echo -e "${RED}🔴 CRITICAL${NC} [$category] $message"
    elif [ "$severity" = "HIGH" ]; then
        echo -e "${YELLOW}🟠 HIGH${NC} [$category] $message"
    else
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

# Summary
echo ""
echo "========================================"
echo "📊 Scan Summary"
echo "========================================"
echo "Total issues found: $ISSUES_FOUND"
echo "Critical issues: $CRITICAL_FOUND"
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
