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
[Use one of these quality labels based on the score:
- Excellent (0.9 - 1.0)
- Good (0.75 - 0.89)
- Acceptable (0.6 - 0.74)
- Poor (0.4 - 0.59)
- Failing (0.0 - 0.39)
Include the numeric score e.g. "Good (0.82)"]

## Scores
[A simple table or list of scores per criterion]

## Feedback
[2-4 sentences explaining the result clearly]

## Needs Human Review
[Yes or No, with a one-line reason. Recommend human review for scores between 0.4 and 0.75]"""


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
        error = str(e)
        if "429" in error or "RESOURCE_EXHAUSTED" in error:
            return "The evaluator is receiving too many requests right now. Please wait a moment and try again."
        return f"Evaluation failed: {error}"