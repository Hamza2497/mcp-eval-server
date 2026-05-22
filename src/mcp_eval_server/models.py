from pydantic import BaseModel, Field
from typing import Optional


class RubricCriteria(BaseModel):
    """A single criterion within a rubric.
    
    Attributes:
        name: Short identifier for this criterion (e.g. "accuracy", "clarity").
        description: What this criterion measures.
        weight: Relative importance, between 0.0 and 1.0.
    """
    name: str
    description: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)


class Rubric(BaseModel):
    """A structured rubric for evaluating an LLM output.
    
    Attributes:
        task_goal: What the LLM was supposed to accomplish.
        criteria: List of criteria to evaluate against.
        min_passing_score: Minimum overall score required to pass, between 0.0 and 1.0.
    """
    task_goal: str
    criteria: list[RubricCriteria]
    min_passing_score: float = Field(default=0.7, ge=0.0, le=1.0)


class EvaluationResult(BaseModel):
    """The result of an evaluation performed by the judge model.
    
    Attributes:
        overall_score: Aggregate score between 0.0 and 1.0.
        passed: Whether the output met the minimum passing score.
        criteria_scores: Per-criterion scores, keyed by criterion name.
        feedback: Human-readable explanation of the scores.
        needs_human_review: True if the score is borderline (between 0.3 and 0.7).
    """
    overall_score: float
    passed: bool
    criteria_scores: dict[str, float]
    feedback: str
    needs_human_review: bool