from mcp.server.fastmcp import FastMCP
from .models import Rubric, EvaluationResult
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

mcp = FastMCP("mcp-eval-server")

@mcp.tool()
def score_against_rubric(llm_output: str, rubric: Rubric) -> EvaluationResult:
    """Score an LLM output against a structured rubric."""
    criteria_text = "\n".join(
        f"- {c.name} (weight {c.weight}): {c.description}"
        for c in rubric.criteria
    )
    prompt = f"""You are an LLM output evaluator. Score the following output against the rubric criteria.

Task goal: {rubric.task_goal}

Rubric criteria:
{criteria_text}

LLM output to evaluate:
{llm_output}

Return a JSON object with exactly these fields:
- overall_score: float between 0.0 and 1.0
- passed: boolean (true if overall_score >= {rubric.min_passing_score})
- criteria_scores: object mapping each criterion name to a float between 0.0 and 1.0
- feedback: string explaining the scores
- needs_human_review: boolean (true if overall_score is between 0.3 and 0.7)

Return only the JSON object, no other text."""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    result = json.loads(response.text.strip().removeprefix("```json").removesuffix("```").strip())
    return EvaluationResult(**result)

@mcp.tool()
def evaluate_factual_accuracy(llm_output: str, known_facts: list[str]) -> EvaluationResult:
    """Check whether the LLM output contradicts or misrepresents a set of known facts."""
    facts_text = "\n".join(f"- {fact}" for fact in known_facts)
    prompt = f"""You are an LLM output evaluator. Check whether the following output contradicts or misrepresents any of the known facts provided.

Known facts:
{facts_text}

LLM output to evaluate:
{llm_output}

Return a JSON object with exactly these fields:
- overall_score: float between 0.0 and 1.0 (1.0 means fully consistent with all facts, 0.0 means contradicts facts)
- passed: boolean (true if overall_score >= 0.7)
- criteria_scores: object with a single key "factual_accuracy" mapped to a float between 0.0 and 1.0
- feedback: string explaining which facts were consistent or contradicted
- needs_human_review: boolean (true if overall_score is between 0.3 and 0.7)

Return only the JSON object, no other text."""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    result = json.loads(response.text.strip().removeprefix("```json").removesuffix("```").strip())
    return EvaluationResult(**result)

@mcp.tool()
def check_relevance(llm_output: str, user_query: str) -> EvaluationResult:
    """Check whether the LLM output actually addresses what the user asked."""
    prompt = f"""You are an LLM output evaluator. Check whether the following output actually addresses the user's query.

User query:
{user_query}

LLM output to evaluate:
{llm_output}

Return a JSON object with exactly these fields:
- overall_score: float between 0.0 and 1.0 (1.0 means fully addresses the query, 0.0 means completely irrelevant)
- passed: boolean (true if overall_score >= 0.7)
- criteria_scores: object with a single key "relevance" mapped to a float between 0.0 and 1.0
- feedback: string explaining how well the output addresses the query
- needs_human_review: boolean (true if overall_score is between 0.3 and 0.7)

Return only the JSON object, no other text."""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    result = json.loads(response.text.strip().removeprefix("```json").removesuffix("```").strip())
    return EvaluationResult(**result)

@mcp.tool()
def check_logical_consistency(llm_output: str) -> EvaluationResult:
    """Check whether the LLM output contradicts itself internally."""
    prompt = f"""You are an LLM output evaluator. Check whether the following output contradicts itself internally.

LLM output to evaluate:
{llm_output}

Return a JSON object with exactly these fields:
- overall_score: float between 0.0 and 1.0 (1.0 means fully consistent, 0.0 means severely self-contradictory)
- passed: boolean (true if overall_score >= 0.7)
- criteria_scores: object with a single key "logical_consistency" mapped to a float between 0.0 and 1.0
- feedback: string explaining any contradictions found or confirming consistency
- needs_human_review: boolean (true if overall_score is between 0.3 and 0.7)

Return only the JSON object, no other text."""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    result = json.loads(response.text.strip().removeprefix("```json").removesuffix("```").strip())
    return EvaluationResult(**result)