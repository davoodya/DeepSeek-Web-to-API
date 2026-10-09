# DeepSeek API — Free LLM Access Through Your Own Account

> Turn the DeepSeek chat website into a programmable API — no API key, no billing, no paid plan required.

This project wraps the free [chat.deepseek.com](https://chat.deepseek.com) experience behind two clean interfaces, so you can talk to DeepSeek from your own code using nothing more than the account you already have.

**Unofficial project.** Not affiliated with, endorsed by, or connected to DeepSeek. It automates the consumer web experience for personal use — please use it responsibly and stay within DeepSeek's terms of service.

---

## A Note on Origin & Extensions

This project was originally started by [**sums001**](https://github.com/sums001) as [`Deepseek-API`](https://github.com/sums001/Deepseek-API). The foundation — the auth flow, the browser bridge, the PoW solver, and the OpenAI-compatible server — comes from that work.

On top of that base, I've been extending the project with additional capabilities, including:

- **Tool calling** support
- **Structured output** handling
- **Code optimization** across the codebase
- **Agent-compatible API** surface for use with LLM agent frameworks
- …and more features on the way

---

## What You Get

There are two ways to use it, depending on what fits your workflow:

### 🐍 As a Python library
Import it and call `client.chat("Hi")` directly. Streaming and multi-turn conversations are supported out of the box.

### 🔌 As a local OpenAI-compatible server
Run a server on `http://localhost:8000/v1` that speaks the OpenAI API format. Any tool, SDK, or app built for OpenAI works with it as a drop-in — you just point `base_url` at `localhost` instead of OpenAI.

In both cases, you sign in **once** through a browser with your DeepSeek account. After that, the session is saved and refreshed automatically.

---

## Table of Contents

- [Why Use This?](#why-use-this)
- [Requirements](#requirements)
- [Setup (2 Minutes)](#setup-2-minutes)
- [Usage 1 — As a Python Library](#usage-1--as-a-python-library)
- [Usage 2 — As an OpenAI-Compatible Server](#usage-2--as-an-openai-compatible-server)
- [Command Line](#command-line)
- [Human-Check & Proof-of-Work](#human-check--proof-of-work)
- [Models, DeepThink & Web Search](#models-deepthink--web-search)
- [Concurrency](#concurrency)
- [Rate Limiting](#rate-limiting)
- [Project Layout](#project-layout)
- [Notes & Limitations](#notes--limitations)
- [License](#license)

---

## Why Use This?

- **It's free.** Uses your existing signed-in DeepSeek account — no API billing, no credits to buy.
- **It speaks OpenAI.** Point any OpenAI client at `localhost` and it works without code changes.
- **Everything DeepSeek offers.** Choose between the fast and expert models, and toggle DeepThink reasoning or web search per request.
- **Streaming and threads.** Get token-by-token output, and keep conversations going by passing a `conversation_id`.

---

## Requirements

- **Python 3.9 or newer**
- A **DeepSeek account** (the free one you already use on chat.deepseek.com)
- Runs on **Windows**, **macOS**, and **Linux**

---

## Setup (2 Minutes)

**Step 1 — Clone the repository**

```bash
git clone https://github.com/sums001/Deepseek-API.git
cd "Deepseek-API"
```

**Step 2 — Create and activate a virtual environment**

On **macOS / Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

On **Windows (PowerShell)**:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> On Windows, you may need to allow script execution once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. In `cmd.exe`, use `venv\Scripts\activate.bat` instead.

**Step 3 — Install dependencies and sign in**

```bash
pip install -r requirements.txt       # Install dependencies
playwright install chromium           # One-time browser install for Playwright
python -m deepseek.auth               # Sign in once; a browser window opens
```

A login window opens so you can sign in manually and clear the human-check once. From then on, your session (bearer token + cookies) is stored under `session/` — which is git-ignored and never shared — and reused on every run. The cached session refreshes automatically, so your first request works right away.

> For local single-user use, this step is optional: the server can open the login window for you on demand the first time it needs a session.

---

## Usage 1 — As a Python Library

The simplest path if your code is already Python.

```python
from deepseek import DeepSeekClient

client = DeepSeekClient()                # loads your signed-in session

# Get a full reply
reply = client.chat("Say hello in one short sentence.")
print(reply.text)

# Continue the SAME conversation — pass the id back
reply2 = client.chat("And now in French?", conversation_id=reply.conversation_id)
print(reply2.text)

# Stream the answer as it's typed
for chunk in client.stream("Tell me a short joke"):
    print(chunk, end="", flush=True)
```

`chat()` returns the full text along with a `conversation_id`. Pass that id back to keep the thread going, or leave it out to start a new one. `stream()` yields the reply piece by piece as it's generated.

👉 More examples: [01_direct_chat.py](examples/01_direct_chat.py) · [02_direct_conversation.py](examples/02_direct_conversation.py) · [03_direct_stream.py](examples/03_direct_stream.py)

---

## Usage 2 — As an OpenAI-Compatible Server

Start a local server that speaks the OpenAI API. Existing OpenAI tools and SDKs work with it unchanged.

```bash
python app.py
# -> DeepSeek OpenAI-compatible API on http://127.0.0.1:8000
```

Then point any OpenAI client at it. The API key is required by the SDK but is ignored:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(resp.choices[0].message.content)
```

Or call it with plain HTTP / `curl`:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hello!"}]}'
```

**Available endpoints**

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/v1/chat/completions` | Chat. Supports `"stream": true`, plus optional `"conversation_id"`, `"thinking"`, `"search"` |
| `GET`  | `/v1/models` | Lists the available models |
| `GET`  | `/healthz` | Health check (exempt from rate limiting) |

> To change the bind address, use environment variables: `HOST=0.0.0.0 PORT=8080 python app.py`. Or run it directly with Uvicorn: `uvicorn server.api:app --host 0.0.0.0 --port 8080`.

👉 More examples: [04_server_http.py](examples/04_server_http.py) · [05_server_stream.py](examples/05_server_stream.py) · [06_server_openai_sdk.py](examples/06_server_openai_sdk.py)

---

## Command Line

```bash
python -m deepseek.auth          # sign in and save the session
```

---

## Human-Check & Proof-of-Work

DeepSeek's chat sits behind two gates. Both are handled for you automatically:

- **AWS WAF human-check.** Access requires a signed-in browser session that has cleared the "verify you're human" check. Running `python -m deepseek.auth` opens a real browser so you can sign in and solve it once. The resulting token and cookies are cached under `session/` and reused for every request afterward.
- **Proof-of-work.** Every completion is gated by a PoW challenge. The bridge solves it by running DeepSeek's own `sha3_wasm_bg.wasm` module — the same one the browser loads — inside a `wasmtime` sandbox. Nothing extra is needed on your end.

A cached session stays valid for roughly **6 hours** and is refreshed headlessly from your saved Chrome profile whenever possible. Only a full expiry sends you back to the browser.

---

## Models, DeepThink & Web Search

The `model` field selects **which model** answers. DeepThink and web search are **not** models — they're independent toggles you pass per request.

| Model | DeepSeek Mode | Notes |
| --- | --- | --- |
| `deepseek-chat` | Instant | Fast default model |
| `deepseek-expert` | Expert | Stronger, slower |

To enable DeepThink reasoning and/or web search, pass `thinking: true` and/or `search: true` in the request body — or through the OpenAI SDK's `extra_body`:

```python
resp = client.chat.completions.create(
    model="deepseek-expert",
    messages=[{"role": "user", "content": "What changed in the news today?"}],
    extra_body={"thinking": True, "search": True},
)
```

`conversation_id`, `thinking`, and `search` are non-OpenAI extras. A thread's model is locked in at creation, so `model` **cannot** be combined with `conversation_id` when resuming. Unknown model names return a `404` — there's no silent fallback. See [server/config.py](server/config.py).

---

## Concurrency

The server bridges a **single** signed-in DeepSeek account behind one shared client. Because the PoW solver's `wasmtime` store isn't reentrant, upstream calls are **serialized** — parallel HTTP requests queue behind a lock and run one at a time (see [server/api.py](server/api.py)).

This is intentional. Throughput is sequential, not parallel. Keep concurrent in-flight requests low, and please don't hammer your account.

---

## Rate Limiting

In addition to serialization, the bridge applies a self-imposed rate limit using a dependency-free sliding-window limiter ([server/ratelimit.py](server/ratelimit.py)). It caps accepted requests **per client IP** and returns a standard `429` with a `Retry-After` header when you exceed the limit. `/healthz` is exempt.

| Env var | Default | Meaning |
| --- | --- | --- |
| `RATE_LIMIT_PER_MINUTE` | `30` | Requests per minute accepted per client IP |

```bash
RATE_LIMIT_PER_MINUTE=60 python app.py   # raise the limit
```

**On the client side, use exponential backoff.** Transient `429`s clear if you retry with growing delays (e.g., 1s → 2s → 4s). The official `openai` SDK does this automatically and honors `Retry-After`; if you're using plain HTTP, add a few retries yourself.

---

## Project Layout

| Path | What it does |
| --- | --- |
| [deepseek/](deepseek/) | Core library: `DeepSeekClient`, browser sign-in ([auth.py](deepseek/auth.py)), HTTP driver ([client.py](deepseek/client.py)), and PoW solver ([pow.py](deepseek/pow.py)) |
| [server/](server/) | The FastAPI OpenAI-compatible server |
| [examples/](examples/) | Runnable examples for every feature ([examples/README.md](examples/README.md)) |
| [app.py](app.py) | Entry point that starts the server |

---

## Notes & Limitations

- **Sign in once, then forget about it.** The cached session refreshes automatically — you only re-sign-in if it fully expires.
- **Be reasonable.** Use it in moderation. Don't spam it or hammer it with automated bulk requests.
- **No real token counts.** The `usage` field in responses is a rough estimate based on ~4 characters per token.
- **Most OpenAI parameters are accepted but ignored.** `temperature`, `top_p`, and `max_tokens` do nothing. Only `model`, `messages`, `stream`, `conversation_id`, `thinking`, and `search` have an effect.
- **Vision is deferred.** It would require image-upload plumbing that isn't built yet.
- **Your session stays private.** Everything in `session/` (cookies + token) lives on your machine and is git-ignored.

---

## License

Released under the [MIT License](LICENSE).

Because this is an unofficial project, you remain responsible for complying with DeepSeek's terms of service.

---