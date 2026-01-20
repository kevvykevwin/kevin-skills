# Threat Intelligence Reference (2025)

Current attack patterns and mitigations for e-commerce security.

---

## Carding Attack Patterns

### 1. Classic Card Testing
**Pattern**: High volume of small transactions ($1-5) to validate stolen cards.

**Indicators**:
- Spike in $1.00 or round-number transactions
- Same IP/device, different cards
- Sequential card numbers (BIN attacks)
- Immediate transaction after account creation
- Mismatched AVS/BIN geography

**Mitigation**:
- Minimum transaction amounts
- Velocity limits per IP/device
- AVS enforcement
- 3DS on first transactions

### 2. BIN Attacks
**Pattern**: Testing cards from same BIN (first 6 digits) to find valid numbers.

**Indicators**:
- Multiple declines with same BIN
- Sequential or near-sequential card numbers
- Rapid submission rate

**Mitigation**:
- Rate limit by BIN
- Block after 3+ failures from same BIN
- Alert on BIN concentration

### 3. Gift Card Brute Force
**Pattern**: Automated testing of gift card number/PIN combinations.

**Indicators**:
- High volume of gift card balance checks
- Sequential or pattern-based gift card numbers
- API abuse on balance endpoints

**Mitigation**:
- Rate limit balance checks
- CAPTCHA after failed attempts
- Velocity limits per session

### 4. Enumeration Attacks
**Pattern**: Testing email/username existence for account takeover.

**Indicators**:
- High volume of login/password reset requests
- Different responses for valid vs invalid emails
- Credential stuffing patterns

**Mitigation**:
- Consistent response times
- Generic error messages
- Rate limiting on auth endpoints

---

## Bot Signatures (2025)

### Known Malicious User Agents
```
curl/*
python-requests/*
wget/*
Java/*
Go-http-client/*
Apache-HttpClient/*
"" (empty)
Postman*
Thunder Client/*
```

### Suspicious Characteristics
- Missing or incorrect `Accept-Language` header
- No `Referer` header on internal navigation
- TLS fingerprint mismatches (JA3/JA4)
- WebDriver detected (`navigator.webdriver = true`)
- Missing browser APIs (notifications, permissions)
- Headless browser indicators
- Datacenter IP ranges

### Known Bad ASNs (VPNs/Proxies/Datacenters)
```
AS14061 - DigitalOcean
AS16509 - AWS
AS15169 - Google Cloud
AS8075  - Microsoft Azure
AS13335 - Cloudflare (ironically, used for proxying)
AS20473 - Vultr
AS63949 - Linode
AS14618 - AWS (alternate)
AS45102 - Alibaba Cloud
AS24940 - Hetzner
```

**Note**: Legitimate users may use VPNs. Challenge rather than block.

---

## Emerging Threats (2025)

### 1. AI-Powered Fraud
**Trend**: Fraudsters using AI to:
- Generate realistic fake identities
- Bypass CAPTCHA systems
- Create convincing phishing content
- Automate social engineering

**Mitigation**:
- Behavioral biometrics (can't be faked by AI yet)
- Multi-factor verification
- Transaction pattern analysis
- Human review for high-risk

### 2. Residential Proxy Networks
**Trend**: Using residential IPs to avoid datacenter detection.

**Indicators**:
- IP reputation looks clean
- But behavior is automated
- Multiple unrelated accounts from same "residential" IP

**Mitigation**:
- Focus on behavior, not just IP
- Device fingerprinting
- Session analysis

### 3. Mobile Emulation
**Trend**: Desktop bots emulating mobile devices.

**Indicators**:
- Mobile user agent but desktop characteristics
- Touch events without actual touch
- Screen dimensions don't match device

**Mitigation**:
- Deep device fingerprinting
- Accelerometer/gyroscope challenges
- Mobile-specific verification

### 4. Refund Fraud Evolution
**Trend**: Organized "refund as a service" operations.

**Indicators**:
- Multiple refund requests from same address
- High-value items with shipping "issues"
- Pattern of "item not as described" claims

**Mitigation**:
- Refund velocity limits
- Require photo evidence
- Flag repeat refund requesters

---

## Detection Queries

### Elasticsearch/OpenSearch

```json
// Carding attack detection
{
  "query": {
    "bool": {
      "must": [
        { "range": { "@timestamp": { "gte": "now-1h" } } },
        { "term": { "event_type": "payment_attempt" } },
        { "term": { "outcome": "declined" } }
      ]
    }
  },
  "aggs": {
    "by_ip": {
      "terms": { "field": "ip_address", "min_doc_count": 5 }
    },
    "by_device": {
      "terms": { "field": "device_fingerprint", "min_doc_count": 3 }
    }
  }
}
```

```json
// BIN attack detection
{
  "query": {
    "bool": {
      "must": [
        { "range": { "@timestamp": { "gte": "now-15m" } } },
        { "term": { "outcome": "declined" } }
      ]
    }
  },
  "aggs": {
    "by_bin": {
      "terms": { 
        "field": "card_bin", 
        "min_doc_count": 5,
        "order": { "_count": "desc" }
      }
    }
  }
}
```

### SQL (for relational databases)

```sql
-- Find potential carding attacks (last hour)
SELECT 
  ip_address,
  COUNT(*) as attempts,
  COUNT(DISTINCT card_fingerprint) as unique_cards,
  SUM(CASE WHEN outcome = 'declined' THEN 1 ELSE 0 END) as declines
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY ip_address
HAVING COUNT(*) > 10 AND COUNT(DISTINCT card_fingerprint) > 3
ORDER BY attempts DESC;

-- Find velocity violations
SELECT 
  device_fingerprint,
  COUNT(*) as attempts,
  MIN(created_at) as first_attempt,
  MAX(created_at) as last_attempt,
  EXTRACT(EPOCH FROM (MAX(created_at) - MIN(created_at))) as duration_seconds
FROM payment_attempts
WHERE created_at > NOW() - INTERVAL '10 minutes'
GROUP BY device_fingerprint
HAVING COUNT(*) > 5
ORDER BY attempts DESC;
```

---

## Response Playbooks

### Playbook 1: Active Carding Attack

**Trigger**: >50 declines in 10 minutes OR >20 unique cards from single IP/device

**Immediate Actions** (0-5 min):
1. Enable Cloudflare "Under Attack" mode
2. Reduce velocity limits to 3 attempts per IP per 10 min
3. Enable 3DS on all transactions
4. Alert on-call

**Investigation** (5-30 min):
1. Identify attack source (IP range, ASN, fingerprints)
2. Check for successful transactions from same source
3. Review any accounts created during attack window

**Blocking** (ongoing):
1. Add identified IPs to WAF blocklist
2. Block identified device fingerprints
3. Report to payment processor

**Post-Incident**:
1. Analyze attack patterns
2. Update detection rules
3. Document in incident log

### Playbook 2: Account Takeover Attempt

**Trigger**: >10 failed logins for single account OR credential stuffing pattern detected

**Immediate Actions**:
1. Lock affected account
2. Invalidate all sessions
3. Send notification to account owner
4. Enable step-up auth for account

**Investigation**:
1. Check for successful logins during attack window
2. Review any changes made to account
3. Check for orders placed

**Recovery**:
1. Force password reset
2. Review and revert unauthorized changes
3. Monitor account for follow-up attempts

### Playbook 3: Successful Fraudulent Transaction

**Trigger**: Chargeback received OR fraud flag from processor

**Immediate Actions**:
1. Block associated card/device/IP
2. Hold any pending orders from same source
3. Preserve all transaction data

**Investigation**:
1. Full transaction timeline
2. All associated accounts
3. Delivery status (stop if possible)

**Recovery**:
1. Document for chargeback response
2. Update fraud rules
3. Report to law enforcement if significant

---

## Resources

### Threat Intelligence Feeds
- abuse.ch (malware, botnet IPs)
- Spamhaus (spam/abuse IPs)
- AbuseIPDB (crowdsourced threat intel)
- GreyNoise (internet noise vs. targeted attacks)

### Industry Reports
- Sift Digital Trust & Safety Index
- LexisNexis True Cost of Fraud
- Juniper Research Online Payment Fraud
- HUMAN Security Bot Threat Reports

### Communities
- OWASP
- Merchant Risk Council
- r/fraudprevention
- Payment processor security blogs (Stripe Radar, Braintree)
