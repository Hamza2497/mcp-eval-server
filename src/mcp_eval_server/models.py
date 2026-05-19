from pydantic import BaseModel, Field
from typing import Optional

class RubricCriteria(BaseModel):
    name: str
    description: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)

class Rubric(BaseModel):
    task_goal: str
    criteria: list[RubricCriteria]
    min_passing_score: float = Field(default=0.7, ge=0.0, le=1.0)

class EvaluationResult(BaseModel):
    overall_score: float
    passed: bool
    criteria_scores: dict[str, float]
    feedback: str
    needs_human_review: bool