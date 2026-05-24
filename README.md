# mcp-eval-server

> **Structured LLM output evaluation — as an MCP plugin for Claude Desktop, and as a live web app**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-llm--eval--dmpf.onrender.com-58a6ff?style=flat&logo=render)](https://llm-eval-dmpf.onrender.com)
[![Tests](https://img.shields.io/badge/Tests-19%20passing-brightgreen?style=flat&logo=pytest)](https://github.com/Hamza2497/mcp-eval-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Five evaluation tools for scoring, fact-checking, relevance, consistency, and output comparison — usable directly inside Claude Desktop with no API key, or via a Gemini-powered web app with no setup at all.

Draws on my LLM evaluation work at Invisible Technologies.

---

## ✨ Features

- **5 evaluation tools** — rubric scoring, factual accuracy, relevance, logical consistency, output comparison
- **Dual-mode architecture** — install as a Claude Desktop MCP plugin (Claude acts as judge, no API key needed) or use the web app (Gemini-powered, zero setup)
- **Chat-style web UI** — free text or guided structured input, your choice per evaluation
- **Graduated scoring** — numeric scores with pass/fail thresholds, detailed feedback, and human-review flags
- **Shareable links** — copy a link to any evaluation result and share it
- **Session history** — every evaluation in the current session is logged and browsable
- **Dark / light mode** — toggle available, preference persisted across sessions
- **19 passing tests** — full pytest suite covering all tools and edge cases

---

## 🏗️ Architecture

```
┌─────────────────────────────┐      ┌──────────────────────────────┐
│   Claude Desktop (MCP)      │      │   Web App (Render)           │
│   Claude acts as judge      │      │   Gemini acts as judge       │
│   No API key needed         │      │   No setup needed            │
└────────────┬────────────────┘      └──────────────┬───────────────┘
             │                                       │
             └───────────────┬───────────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │  FastMCP / FastAPI   │
                  │  Python 3.12         │
                  │  Pydantic models     │
                  └──────────────────────┘
```

---

## 🔧 The 5 Tools

| Tool | What it does |
|------|-------------|
| `score_against_rubric` | Score an LLM output against a custom rubric with weighted criteria and a passing threshold |
| `evaluate_factual_accuracy` | Check whether an output contradicts or misrepresents a set of known facts |
| `check_relevance` | Check whether an output actually addresses what the user asked |
| `check_logical_consistency` | Detect internal contradictions within an output |
| `compare_outputs` | Compare two LLM responses to the same query and determine which is better and why |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| MCP server | Python 3.12 · FastMCP · Pydantic |
| Web app | FastAPI · Jinja2 · Vanilla JS |
| AI judge (web) | Google Gemini (`gemini-2.0-flash-lite`) |
| AI judge (MCP) | Claude (via Claude Desktop — no API key) |
| Deployment | Render |
| Tests | pytest · 19 passing |

---

## 🚀 Quick Start

### Option A — Web app (no setup)

→ **[llm-eval-dmpf.onrender.com](https://llm-eval-dmpf.onrender.com)**

Type what you want to evaluate in plain English, or switch to Guided mode to fill in structured fields. No account, no API key.

---

### Option B — Claude Desktop MCP plugin

**Prerequisites:** Claude Desktop, Python 3.12+

```bash
git clone https://github.com/Hamza2497/mcp-eval-server.git
cd mcp-eval-server
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mcp-eval-server": {
      "command": "/absolute/path/to/mcp-eval-server/.venv/bin/python",
      "args": ["-m", "mcp_eval_server"]
    }
  }
}
```

Replace the path with wherever you cloned the repo. Restart Claude Desktop — the 5 eval tools will appear automatically.

---

### Option C — Run the web app locally

```bash
pip install -e .
cp .env.example .env  # add your GEMINI_API_KEY
uvicorn webapp.main:app --reload
# → http://localhost:8000
```

---

## 🧪 Tests

```bash
pytest tests/ -v
# 19 passed
```

---

## 📁 Project Structure

```
mcp-eval-server/
├── src/mcp_eval_server/   # MCP server — 5 eval tools
├── webapp/                # FastAPI web app + Jinja2 templates
├── tests/                 # pytest suite (19 tests)
├── pyproject.toml
├── requirements.txt
├── render.yaml
└── .env.example
```

---

## 🌐 Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Web app | Render | [llm-eval-dmpf.onrender.com](https://llm-eval-dmpf.onrender.com) |

`GEMINI_API_KEY` is set as an environment variable on Render. Everything else is in `render.yaml`.

---

## 👤 Author

**Hamza Assaf** — [hamza2497.github.io](https://hamza2497.github.io) · [LinkedIn](https://linkedin.com/in/hamzah-assaf)
