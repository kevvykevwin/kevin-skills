# AI / LLM Code Threat Playbook

Sub-agent trigger: LLM deps detected (anthropic, openai, langchain, llama-index, @modelcontextprotocol, transformers, torch, huggingface-hub). Read flagged files, apply each section below, return structured findings.

---

## Prompt-Injection Sinks

User-controlled input reaching a prompt string is the #1 LLM vuln. Indirect injection (RAG, tool output, fetched pages) is equally dangerous.

- f-strings / `.format()` / template-literals `${}` that interpolate `req.body`, `req.query`, `req.params`, form fields, or cookie values directly into a prompt
- RAG retrieval piped to prompt without content filtering or sanitization (attacker poisons the vector store)
- System prompts built from DB rows, fetched URLs, or user-supplied config files
- `ChatPromptTemplate.from_template(user_input)` or equivalent in LangChain / LlamaIndex
- Multi-turn history appended verbatim without role validation (role confusion: attacker injects `\nAssistant:` token)
- `tool_result` content echoed back into the next prompt without escaping

**What to grep:**
```
prompt.*req\.|f".*{request|user_input|query|row|content}|template\.format\(|PromptTemplate.*{
```

---

## LLM Output Handling

Treat every LLM response as untrusted user input. Trace the response object through to every sink.

- `innerHTML =` / `dangerouslySetInnerHTML` / `v-html` fed LLM text → stored or reflected XSS
- LLM output concatenated into SQL string (even inside an ORM raw-query escape hatch)
- LLM output passed to `subprocess.run(...)`, `os.system(...)`, `exec(...)`, `eval(...)`, `shell=True`
- LLM-generated file path used in `open(path, 'w')` without `os.path.abspath` + prefix containment check
- LLM-generated JSON deserialized with `pickle` or `yaml.load` (non-safe) instead of `json.loads`
- Response streamed directly to a browser `<script>` tag or server-side template without escaping

**What to grep:**
```
innerHTML.*completion|dangerouslySetInnerHTML.*response|subprocess.*llm|shell=True|exec\(.*result|open\(.*llm|yaml\.load\(
```

---

## Model-Loading & Pickle RCE

Loading model weights executes arbitrary code if trust is granted or the format allows it.

- `from_pretrained(..., trust_remote_code=True)` — **always P1**; executes arbitrary Python from the repo
- `torch.load(path)` without `weights_only=True` — pickle-based RCE; CVE-2026-24747 class
- `pickle.loads(data)` where `data` originates from any path not under the repo's own control
- `yaml.load(stream)` without `Loader=yaml.SafeLoader` (or `yaml.safe_load`)
- `from_pretrained("org/model")` without a pinned commit hash (`revision="abc1234"`) — supply-chain drift on every pull
- Model files fetched from non-official registries (any URL not under `huggingface.co`, `pytorch.org`, or an internal registry with checksum verification)
- `joblib.load(...)` / `dill.loads(...)` on externally sourced files

**What to grep:**
```
trust_remote_code=True|torch\.load\((?!.*weights_only=True)|pickle\.loads|yaml\.load\([^)]*\)|from_pretrained\("[^"]+"\)(?!.*revision=)|joblib\.load|dill\.loads
```

---

## MCP / Agentic Tool-Use

Agentic systems expand the blast radius: a single injected instruction can chain across every registered tool.

- Credentials passed as flat strings to all tool calls — no per-tool scope restriction
- Tools that execute side effects (write files, send email, call APIs) without `require_approval: true` or equivalent human-in-the-loop gate
- Tool descriptions or system prompts built with f-strings or user-controlled input (allows tool-description injection / "line-jumping")
- `subprocess` calls inside agent tool handlers without explicit argument whitelisting (no shell metachar stripping)
- SSRF via agent: `requests.get(url)` / `fetch(url)` where `url` is LLM-generated and not validated against an allowlist
- `.mcp.json` / `.cursor/mcp.json` committed to the repo with embedded `sk-`, `sk_live_`, or `ANTHROPIC_API_KEY` values
- Agent loops with no iteration cap or no exit condition validation (infinite-loop amplification of malicious instructions)
- Tool output fed back into the next prompt without sanitization (secondary injection)

**What to grep:**
```
require_approval|\.mcp\.json|ANTHROPIC_API_KEY|OPENAI_API_KEY|requests\.get\(.*llm|fetch\(.*generated|subprocess.*tool|shell=True.*agent
```

---

## AI-Supply-Chain & Slopsquat

LLMs hallucinate package names; attackers squat those names on PyPI/npm with malicious payloads.

**Known hallucinated / squatted names — flag on sight:**
- `huggingface-cli` (real package: `huggingface-hub`)
- `gradio-ssh`
- `tensorflow-pro`
- `pytorch-utils`
- `openai-helper`
- `langchain-community-tools` (varies; verify exact canonical name)
- Any `*-sdk` or `*-utils` suffix on a well-known ML brand name

**Dependency hygiene:**
- Wildcard (`*`) or unpinned caret (`^x.y`) ranges on LLM SDK versions in `requirements.txt`, `pyproject.toml`, `package.json`
- Missing `requirements.txt.lock` / `poetry.lock` / `package-lock.json` — no integrity hash
- LiteLLM, vLLM, Ollama client libs unpinned — these proxy model calls; compromise = full prompt/response interception
- `pip install` of any package registered on PyPI fewer than 14 days ago in a crypto, auth, or ML import path
- `--extra-index-url` or `--find-links` pointing to non-official registries without hash pinning

**What to grep:**
```
huggingface-cli|gradio-ssh|tensorflow-pro|pytorch-utils|openai-helper|requirements.*\*|"anthropic": "\^|"openai": "\^|--extra-index-url
```

---

## Committed Dev-Tool Leakage

Secrets in tracked files are exfiltrated by any clone, fork, or CI log exposure.

- `.env`, `.env.local`, `.env.production`, `.env.development` tracked in git (not in `.gitignore`)
- `.mcp.json`, `.cursor/mcp.json`, `.claude/settings.local.json` containing `sk-`, `sk_live_`, `ANTHROPIC_API_KEY=`, `OPENAI_API_KEY=`, or `CLAUDE_API_KEY=`
- System prompt strings hardcoded in source files containing credentials, internal URLs, or PII
- Jupyter notebooks (`.ipynb`) with API key values in cell outputs or metadata
- `config.yaml` / `settings.json` with `api_key:` values not referencing env vars
- Private model weights or fine-tune checkpoints accidentally committed (`.bin`, `.safetensors`, `.ckpt` > 10 MB in git history)

**What to grep:**
```
ANTHROPIC_API_KEY=|OPENAI_API_KEY=|sk-[A-Za-z0-9]{20,}|sk_live_|\.env\.production|settings\.local\.json
```

---

## Rate Limiting & Cost Controls

Unguarded LLM endpoints are trivially exploited for cost exhaustion or data exfiltration via long prompts.

- LLM-calling routes without a rate-limit decorator (`@ratelimit`, `express-rate-limit`, `slowapi`, nginx `limit_req`)
- No per-user or per-session token budget — single user can exhaust quota
- No request body size cap — attacker sends 100k-token prompt, billing spikes
- Streaming endpoints without a max-token response cap (`max_tokens` not set or set to an unreasonably high value)
- No retry backoff ceiling — runaway retry loops multiply cost on transient errors
- No alerting / spend threshold on the provider dashboard (out-of-band, but flag as advisory)

**What to grep:**
```
client\.chat\.|anthropic\.messages\.|openai\.chat\.|llm\.invoke\(|chain\.run\(
```
Then verify each callsite has `max_tokens=` set and sits behind a rate-limit layer.

---

## Output Format

Return each finding as:

```
file:line | risk-class | severity | broken-invariant | fix-suggestion
```

**risk-class values:** `prompt-injection` / `output-handling` / `model-load` / `mcp` / `supply-chain` / `leakage` / `rate-limit`

**severity values:** `P1` (critical, block deploy) / `P2` (high, fix before merge) / `P3` (medium, fix in sprint) / `P4` (low/advisory)

Example:
```
src/chat.py:42 | prompt-injection | P1 | user req.body interpolated directly into system prompt f-string | Use a structured message API; never concatenate user input into prompt strings
models/loader.py:17 | model-load | P1 | trust_remote_code=True grants arbitrary code execution on model load | Remove flag; audit model repo; pin revision hash
```

Group findings by risk-class. List P1s first within each group.
