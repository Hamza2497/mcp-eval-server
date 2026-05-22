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

def test_score_against_rubric_returns_prompt():
    result = score_against_rubric(
        "A for loop repeats a block of code for each item in an iterable.",
        simple_rubric()
    )
    assert isinstance(result, str)
    assert "for loop" in result
    assert "accuracy" in result
    assert "clarity" in result

def test_score_against_rubric_empty_output():
    result = score_against_rubric("", simple_rubric())
    assert "Error" in result
    assert "empty" in result.lower()

def test_score_against_rubric_empty_criteria():
    rubric = Rubric(task_goal="Test", criteria=[], min_passing_score=0.7)
    result = score_against_rubric("Some output", rubric)
    assert "Error" in result
    assert "criterion" in result.lower()


# --- evaluate_factual_accuracy ---

def test_factual_accuracy_returns_prompt():
    result = evaluate_factual_accuracy(
        "The Earth orbits the Sun.",
        ["The Earth orbits the Sun"]
    )
    assert isinstance(result, str)
    assert "The Earth orbits the Sun" in result

def test_factual_accuracy_empty_output():
    result = evaluate_factual_accuracy("", ["Some fact"])
    assert "Error" in result
    assert "empty" in result.lower()

def test_factual_accuracy_empty_facts():
    result = evaluate_factual_accuracy("Some output", [])
    assert "Error" in result
    assert "empty" in result.lower()


# --- check_relevance ---

def test_relevance_returns_prompt():
    result = check_relevance(
        "Photosynthesis is how plants convert sunlight into glucose.",
        "How do plants make food?"
    )
    assert isinstance(result, str)
    assert "How do plants make food?" in result
    assert "Photosynthesis" in result

def test_relevance_empty_output():
    result = check_relevance("", "Some query")
    assert "Error" in result
    assert "empty" in result.lower()

def test_relevance_empty_query():
    result = check_relevance("Some output", "")
    assert "Error" in result
    assert "empty" in result.lower()


# --- check_logical_consistency ---

def test_logical_consistency_returns_prompt():
    result = check_logical_consistency(
        "All mammals are warm-blooded. Whales are mammals. Therefore whales are warm-blooded."
    )
    assert isinstance(result, str)
    assert "warm-blooded" in result

def test_logical_consistency_empty_output():
    result = check_logical_consistency("")
    assert "Error" in result
    assert "empty" in result.lower()


# --- compare_outputs ---

def test_compare_outputs_returns_prompt():
    result = compare_outputs(
        output_a="A dictionary in Python is a collection of key-value pairs.",
        output_b="A dictionary is a thing in Python.",
        user_query="What is a Python dictionary?"
    )
    assert isinstance(result, str)
    assert "Response A" in result
    assert "Response B" in result
    assert "Python dictionary" in result

def test_compare_outputs_empty_output_a():
    result = compare_outputs("", "Some response", "Some query")
    assert "Error" in result

def test_compare_outputs_empty_output_b():
    result = compare_outputs("Some response", "", "Some query")
    assert "Error" in result

def test_compare_outputs_empty_query():
    result = compare_outputs("Response A", "Response B", "")
    assert "Error" in result