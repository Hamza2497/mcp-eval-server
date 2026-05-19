from mcp.server.fastmcp import FastMCP
from .models import Rubric, EvaluationResult

mcp = FastMCP("mcp-eval-server")

@mcp.tool()
def score_against_rubric(llm_output: str, rubric: Rubric) -> EvaluationResult:
    """
    Score an LLM output against a structured rubric.
    Returns a score, pass/fail, per-criterion feedback, and a human review flag.
    """
    # Placeholder logic — real judge model call goes here in Day 3
    criteria_scores = {c.name: 0.0 for c in rubric.criteria}
    
    return EvaluationResult(
        overall_score=0.0,
        passed=False,
        criteria_scores=criteria_scores,
        feedback="Evaluation not yet implemented — judge model coming in Day 3.",
        needs_human_review=True
    )

@mcp.tool()
def evaluate_factual_accuracy(llm_output: str, known_facts: list[str]) -> EvaluationResult:
    """
    Check whether the LLM output contradicts or misrepresents a set of known facts.
    Returns a score and flags any inaccuracies found.
    """
    criteria_scores = {"factual_accuracy": 0.0}

    return EvaluationResult(
        overall_score=0.0,
        passed=False,
        criteria_scores=criteria_scores,
        feedback="Factual accuracy evaluation not yet implemented — judge model coming in Day 3.",
        needs_human_review=True
    )

@mcp.tool()
def check_relevance(llm_output: str, user_query: str) -> EvaluationResult:
    """
    Check whether the LLM output actually addresses what the user asked.
    Returns a relevance score and explanation.
    """
    criteria_scores = {"relevance": 0.0}

    return EvaluationResult(
        overall_score=0.0,
        passed=False,
        criteria_scores=criteria_scores,
        feedback="Relevance check not yet implemented — judge model coming in Day 3.",
        needs_human_review=True
    )

@mcp.tool()
def check_logical_consistency(llm_output: str) -> EvaluationResult:
    """
    Check whether the LLM output contradicts itself internally.
    Returns a consistency score and flags any contradictions found.
    """
    criteria_scores = {"logical_consistency": 0.0}

    return EvaluationResult(
        overall_score=0.0,
        passed=False,
        criteria_scores=criteria_scores,
        feedback="Logical consistency check not yet implemented — judge model coming in Day 3.",
        needs_human_review=True
    )