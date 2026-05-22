# MCP Eval Server

An MCP (Model Context Protocol) server that evaluates LLM outputs using a Gemini judge model. Connect it to Claude Desktop and use natural language to run structured evaluations on any LLM response.

## What it does

LLM outputs are hard to evaluate at scale. This server exposes four evaluation tools that use Gemini as a judge model to score outputs against rubrics, check factual accuracy, assess relevance, and detect logical contradictions — all callable directly from Claude Desktop.

## Tools

- **`score_against_rubric`** — Score an LLM output against a custom rubric with weighted criteria and a passing threshold
- **`evaluate_factual_accuracy`** — Check whether an output contradicts a set of known facts
- **`check_relevance`** — Check whether an output actually addresses the user's query
- **`check_logical_consistency`** — Detect internal contradictions in an output
- **`compare_outputs`** — Compare two LLM responses to the same query and determine which is better and why

Each tool returns a structured result with an overall score, per-criterion scores, pass/fail, feedback, and a flag for outputs that need human review.

## Setup

### Prerequisites
- Python 3.12+
- A [Google AI Studio](https://aistudio.google.com) API key
- [Claude Desktop](https://claude.ai/download)

### Install

```bash
git clone https://github.com/Hamza2497/mcp-eval-server.git
cd mcp-eval-server
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Configure API key

Create a `.env` file in the project root:
GEMINI_API_KEY=your_api_key_here

### Connect to Claude Desktop

Add this to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-eval-server": {
      "command": "/path/to/mcp-eval-server/.venv/bin/python",
      "args": ["-m", "mcp_eval_server"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Restart Claude Desktop. The server will appear in your connectors list.

## Example

Ask Claude Desktop:

> Use score_against_rubric to evaluate "A for loop lets you repeat a block of code for each item in a list." against a rubric with task goal "Explain what a for loop does", criteria: accuracy (weight 0.8) and clarity (weight 0.6), min passing score 0.7.

Returns:
Overall Score: 0.775
Passed: Yes
Accuracy: 0.75 — correct but incomplete (works on any iterable, not just lists)
Clarity: 0.8 — easy to understand for a beginner
Needs Human Review: No

## Tech stack

- [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework
- [Google Gemini](https://ai.google.dev) (`gemini-3.1-flash-lite`) — judge model
- [Pydantic](https://docs.pydantic.dev) — typed data validation
- Python 3.12
