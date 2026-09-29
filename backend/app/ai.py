import json
import os

from dotenv import load_dotenv
from google import genai

from .schemas import ExtractResponse


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")


client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"


def extract_tasks(notes: str) -> ExtractResponse:

    prompt = f"""
You extract actionable tasks from meeting notes.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "tasks": [
        {{
            "title": "task description",
            "assignee": "person or null",
            "due_date": "date mentioned or null"
        }}
    ]
}}

Rules:
1. Extract only actionable tasks.
2. Do not invent tasks.
3. Do not invent people.
4. If an assignee is not mentioned, use null.
5. If a due date is not mentioned, use null.
6. Keep the original meaning of the task.
7. Return an empty tasks array if there are no actionable tasks.

Meeting notes:

{notes}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    content = response.text

    if not content:
        raise ValueError("Gemini returned an empty response")

    content = content.strip()

    # Remove Markdown code fences if Gemini adds them
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        data = json.loads(content)
        return ExtractResponse.model_validate(data)

    except Exception as error:
        raise ValueError(f"Invalid Gemini response: {error}")