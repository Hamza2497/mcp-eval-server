import pytest
from mcp_eval_server.tools import (
    score_against_rubric,
    evaluate_factual_accuracy,
    check_relevance,
    check_logical_consistency,
    compare_outputs,
)
from mcp_eval_server.models import Rubric, RubricCriteria


# --- Helpers ---

def simple_rubric():
    return Rubric(
        task_goal="Explain what a for loop does in Python",
        criteria=[
            RubricCriteria(name="accuracy", description="Is the explanation correct?", weight=0.8),
            RubricCriteria(name="clarity", description="Is it easy to understand?", weight=0.6),
        ],
        min_passing_score=0.7
    )


# --- score_against_rubric ---

def test_score_against_rubric_returns_valid_result():
    result = score_against_rubric(
        "A for loop repeats a block of code for each item in an iterable.",
        simple_rubric()
    )
    assert 0.0 <= result.overall_score <= 1.0
    assert isinstance(result.passed, bool)
    assert isinstance(result.feedback, str)
    assert "accuracy" in result.criteria_scores
    assert "clarity" in result.criteria_scores

def test_score_against_rubric_empty_output():
    result = score_against_rubric("", simple_rubric())
    assert result.passed is False
    assert result.needs_human_review is True
    assert "empty" in result.feedback.lower()

def test_score_against_rubric_empty_criteria():
    rubric = Rubric(task_goal="Test", criteria=[], min_passing_score=0.7)
    result = score_against_rubric("Some output", rubric)
    assert result.passed is False
    assert "criterion" in result.feedback.lower()


# --- evaluate_factual_accuracy ---

def test_factual_accuracy_correct_facts():
    result = evaluate_factual_accuracy(
        "The Earth orbits the Sun.",
        ["The Earth orbits the Sun"]
    )
    assert result.overall_score >= 0.7
    assert result.passed is True

def test_factual_accuracy_wrong_facts():
    result = evaluate_factual_accuracy(
        "The Sun orbits the Earth.",
        ["The Earth orbits the Sun"]
    )
    assert result.overall_score < 0.7

def test_factual_accuracy_empty_output():
    result = evaluate_factual_accuracy("", ["Some fact"])
    assert result.passed is False
    assert "empty" in result.feedback.lower()

def test_factual_accuracy_empty_facts():
    result = evaluate_factual_accuracy("Some output", [])
    assert result.passed is False
    assert "empty" in result.feedback.lower()


# --- check_relevance ---

def test_relevance_relevant_output():
    result = check_relevance(
        "Photosynthesis is how plants convert sunlight into glucose using carbon dioxide and water.",
        "How do plants make food?"
    )
    assert result.overall_score >= 0.5

def test_relevance_irrelevant_output():
    result = check_relevance(
        "The stock market closed higher today.",
        "How do plants make food?"
    )
    assert result.overall_score < 0.5

def test_relevance_empty_output():
    result = check_relevance("", "Some query")
    assert result.passed is False
    assert "empty" in result.feedback.lower()

def test_relevance_empty_query():
    result = check_relevance("Some output", "")
    assert result.passed is False
    assert "empty" in result.feedback.lower()


# --- check_logical_consistency ---

def test_logical_consistency_consistent():
    result = check_logical_consistency(
        "All mammals are warm-blooded. Whales are mammals. Therefore whales are warm-blooded."
    )
    assert result.overall_score >= 0.7

def test_logical_consistency_contradiction():
    result = check_logical_consistency(
        "All mammals are warm-blooded. Whales are mammals. Therefore whales are cold-blooded."
    )
    assert result.overall_score < 0.5

def test_logical_consistency_empty_output():
    result = check_logical_consistency("")
    assert result.passed is False
    assert "empty" in result.feedback.lower()

    # --- compare_outputs ---

def test_compare_outputs_picks_better_response():
    result = compare_outputs(
        output_a="A dictionary in Python is a collection of key-value pairs. It is mutable, unordered, and does not allow duplicate keys.",
        output_b="A dictionary is a thing in Python.",
        user_query="What is a Python dictionary?"
    )
    assert result["winner"] == "A"
    assert result["score_a"] > result["score_b"]

def test_compare_outputs_returns_all_fields():
    result = compare_outputs(
        output_a="Python is a high-level, interpreted programming language.",
        output_b="Python is a snake.",
        user_query="What is Python?"
    )
    assert "winner" in result
    assert "score_a" in result
    assert "score_b" in result
    assert "reasoning" in result
    assert "strengths_a" in result
    assert "strengths_b" in result

def test_compare_outputs_empty_output_a():
    result = compare_outputs("", "Some response", "Some query")
    assert "error" in result

def test_compare_outputs_empty_output_b():
    result = compare_outputs("Some response", "", "Some query")
    assert "error" in result

def test_compare_outputs_empty_query():
    result = compare_outputs("Response A", "Response B", "")
    assert "error" in result