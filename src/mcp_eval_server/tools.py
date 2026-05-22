from mcp.server.fastmcp import FastMCP
from .models import Rubric
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("mcp-eval-server")


@mcp.tool()
def score_against_rubric(llm_output: str, rubric: Rubric) -> str:
    """Score an LLM output against a structured rubric."""
    if not llm_output.strip():
        return "Error: llm_output cannot be empty."
    if not rubric.criteria:
        return "Error: Rubric must have at least one criterion."

    criteria_text = "\n".join(
        f"- {c.name} (weight {c.weight}): {c.description}"
        for c in rubric.criteria
    )
    return f"""Please evaluate the following LLM output against this rubric and provide a structured assessment.

Task goal: {rubric.task_goal}

Rubric criteria:
{criteria_text}

Minimum passing score: {rubric.min_passing_score}

LLM output to evaluate:
{llm_output}

Provide:
- An overall score (0.0 to 1.0)
- Whether it passed (score >= {rubric.min_passing_score})
- A score for each criterion
- Feedback explaining the scores
- Whether it needs human review (if score is between 0.3 and 0.7)"""


@mcp.tool()
def evaluate_factual_accuracy(llm_output: str, known_facts: list[str]) -> str:
    """Check whether the LLM output contradicts or misrepresents a set of known facts."""
    if not llm_output.strip():
        return "Error: llm_output cannot be empty."
    if not known_facts:
        return "Error: known_facts cannot be empty."

    facts_text = "\n".join(f"- {fact}" for fact in known_facts)
    return f"""Please check whether the following LLM output contradicts or misrepresents any of the known facts provided.

Known facts:
{facts_text}

LLM output to evaluate:
{llm_output}

Provide:
- An overall factual accuracy score (0.0 to 1.0, where 1.0 means fully consistent)
- Whether it passed (score >= 0.7)
- Which facts were correctly represented and which were contradicted or misrepresented
- Whether it needs human review (if score is between 0.3 and 0.7)"""


@mcp.tool()
def check_relevance(llm_output: str, user_query: str) -> str:
    """Check whether the LLM output actually addresses what the user asked."""
    if not llm_output.strip():
        return "Error: llm_output cannot be empty."
    if not user_query.strip():
        return "Error: user_query cannot be empty."

    return f"""Please check whether the following LLM output actually addresses the user's query.

User query:
{user_query}

LLM output to evaluate:
{llm_output}

Provide:
- A relevance score (0.0 to 1.0, where 1.0 means fully addresses the query)
- Whether it passed (score >= 0.7)
- An explanation of how well the output addresses the query
- Whether it needs human review (if score is between 0.3 and 0.7)"""


@mcp.tool()
def check_logical_consistency(llm_output: str) -> str:
    """Check whether the LLM output contradicts itself internally."""
    if not llm_output.strip():
        return "Error: llm_output cannot be empty."

    return f"""Please check whether the following LLM output contradicts itself internally.

LLM output to evaluate:
{llm_output}

Provide:
- A logical consistency score (0.0 to 1.0, where 1.0 means fully consistent)
- Whether it passed (score >= 0.7)
- Any contradictions found, or confirmation that the output is consistent
- Whether it needs human review (if score is between 0.3 and 0.7)"""


@mcp.tool()
def compare_outputs(output_a: str, output_b: str, user_query: str) -> str:
    """Compare two LLM outputs for the same query and determine which is better."""
    if not output_a.strip():
        return "Error: output_a cannot be empty."
    if not output_b.strip():
        return "Error: output_b cannot be empty."
    if not user_query.strip():
        return "Error: user_query cannot be empty."

    return f"""Please compare these two LLM responses to the same user query and determine which is better.

User query:
{user_query}

Response A:
{output_a}

Response B:
{output_b}

Provide:
- Which response is better (A, B, or tie)
- A score for each response (0.0 to 1.0)
- Reasoning for your decision
- Key strengths of each response"""