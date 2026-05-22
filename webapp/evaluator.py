from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an LLM output evaluator. The user will describe what they want to evaluate in natural language.

Always structure your response in exactly this format:

## Evaluation Type
[State which type: Rubric Scoring / Factual Accuracy / Relevance Check / Logical Consistency / Output Comparison]

## Result
[PASS or FAIL, with the score e.g. 0.85/1.0]

## Scores
[A simple table or list of scores per criterion]

## Feedback
[2-4 sentences explaining the result clearly]

## Needs Human Review
[Yes or No, with a one-line reason]

Keep responses concise and consistent. Always use this exact structure regardless of evaluation type."""


def evaluate(user_message: str) -> str:
    """Send a user message to Gemini and return the evaluation result."""
    if not user_message.strip():
        return "Please describe what you'd like to evaluate."

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"{SYSTEM_PROMPT}\n\nUser request: {user_message}"
        )
        return response.text.strip()
    except Exception as e:
        return f"Evaluation failed: {str(e)}"