from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an LLM output evaluator. The user will describe what they want to evaluate in natural language. 

You have access to these evaluation capabilities:
- Score an output against a rubric with weighted criteria
- Check factual accuracy against known facts
- Check whether an output is relevant to a query
- Check logical consistency within an output
- Compare two outputs head-to-head

Understand what the user wants, perform the evaluation, and return a clear structured result with scores, pass/fail, and feedback."""


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