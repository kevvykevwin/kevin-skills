# Threat Patterns & Intelligence

Current attack patterns for e-commerce security audits.

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

### 2. BIN Attacks
**Pattern**: Testing cards from same BIN (first 6 digits) to find valid numbers.
**Indicators**:
- Multiple declines with same BIN
- Sequential or near-sequential card numbers
- Rapid submission rate

### 3. Gift Card Brute Force
**Pattern**: Automated testing of gift card number/PIN combinations.
**Indicators**:
- High volume of gift card balance checks
- Sequential or pattern-based gift card numbers
- API abuse on balance endpoints

### 4. Enumeration Attacks
**Pattern**: Testing email/username existence for account takeover.
**Indicators**:
- High volume of login/password reset requests
- Different responses for valid vs invalid emails
- Credential stuffing patterns

---

## Bot Signatures

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
AS13335 - Cloudflare
AS20473 - Vultr
AS63949 - Linode
AS14618 - AWS (alternate)
AS45102 - Alibaba Cloud
AS24940 - Hetzner
```
**Note**: Legitimate users may use VPNs. Challenge rather than block.

---

## Emerging Threats

### 1. AI-Powered Fraud
Fraudsters using AI for fake identities, CAPTCHA bypass, phishing content, automated social engineering. Counter with behavioral biometrics, multi-factor verification, transaction pattern analysis.

### 2. Residential Proxy Networks
Residential IPs that look clean but behave automated. Multiple unrelated accounts from same "residential" IP. Focus on behavior-based detection, not just IP reputation.

### 3. Mobile Emulation
Desktop bots emulating mobile devices. Mobile UA but desktop characteristics, touch events without actual touch, screen dimension mismatches. Counter with deep device fingerprinting.

### 4. Refund Fraud ("Refund as a Service")
Organized operations exploiting refund policies. Multiple refund requests from same address, high-value items with shipping "issues". Counter with refund velocity limits and photo evidence requirements.

---

## Resources
- abuse.ch (malware, botnet IPs)
- Spamhaus (spam/abuse IPs)
- AbuseIPDB (crowdsourced threat intel)
- GreyNoise (internet noise vs targeted attacks)
