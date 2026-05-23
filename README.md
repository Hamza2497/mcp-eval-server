# MCP Eval Server

An LLM output evaluation tool with two ways to use it — a live web app you can try instantly, or a Claude Desktop plugin you can install locally.

**[Try the live web app →](https://llm-eval-dmpf.onrender.com)**

---

## What it does

LLM outputs are hard to evaluate at scale. This project exposes five evaluation tools that use a judge model to score outputs against rubrics, check factual accuracy, assess relevance, detect logical contradictions, and compare responses head-to-head.

## Two ways to use it

### 1. Web app (no setup required)
Visit **[llm-eval-dmpf.onrender.com](https://llm-eval-dmpf.onrender.com)** and describe what you want to evaluate in plain English, or use Guided mode to fill in structured fields. Powered by Gemini.

### 2. Claude Desktop plugin (local, no API key needed)
Install the MCP server and call the evaluation tools directly from any Claude Desktop conversation. Claude itself acts as the judge — no external API key required.

---

## Tools

- **`score_against_rubric`** — Score an LLM output against a custom rubric with weighted criteria and a passing threshold
- **`evaluate_factual_accuracy`** — Check whether an output contradicts a set of known facts
- **`check_relevance`** — Check whether an output actually addresses the user's query
- **`check_logical_consistency`** — Detect internal contradictions in an output
- **`compare_outputs`** — Compare two LLM responses to the same query and determine which is better and why

---

## Claude Desktop plugin setup

### Prerequisites
- Python 3.12+
- [Claude Desktop](https://claude.ai/download)

### Install

```bash
git clone https://github.com/Hamza2497/mcp-eval-server.git
cd mcp-eval-server
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Connect to Claude Desktop

Add this to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-eval-server": {
      "command": "/path/to/mcp-eval-server/.venv/bin/python",
      "args": ["-m", "mcp_eval_server"]
    }
  }
}
```

Replace `/path/to/mcp-eval-server/` with the actual path where you cloned the repo. Restart Claude Desktop — the server will appear in your connectors list.

### Example

Ask Claude Desktop:

> Use score_against_rubric to evaluate "A for loop lets you repeat a block of code for each item in a list." against a rubric with task goal "Explain what a for loop does", criteria: accuracy (weight 0.8) and clarity (weight 0.6), min passing score 0.7.

---

## Running the web app locally

```bash
pip install -e .
cp .env.example .env  # add your GEMINI_API_KEY
uvicorn webapp.main:app --reload
```

Then open `http://localhost:8000`.

---

## Tech stack

- [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework
- [FastAPI](https://fastapi.tiangolo.com) + Jinja2 — web app backend
- [Google Gemini](https://ai.google.dev) (`gemini-3.1-flash-lite`) — judge model for web app
- Claude — judge model for the Desktop plugin (no API key needed)
- [Pydantic](https://docs.pydantic.dev) — typed data validation
- Python 3.12
- Deployed on [Render](https://render.com)

---

## Running tests

```bash
pytest tests/ -v
```