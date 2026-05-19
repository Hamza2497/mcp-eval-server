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