import json
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from app.services.quiz_store import StoredQuestion, TOTAL_QUESTIONS


load_dotenv()

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")


class QuestionGenerationError(Exception):
    pass


def _build_prompt(topic: str, retry: bool = False) -> str:
    retry_suffix = (
        "Your previous response was invalid. Return ONLY valid JSON and strictly follow the schema."
        if retry
        else ""
    )
    return f"""
Generate exactly {TOTAL_QUESTIONS} multiple-choice quiz questions for the topic: "{topic}".
Each question must be clear, unique, and suitable for beginner to intermediate learners.

Return JSON with this exact shape:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_option_index": 0
    }}
  ]
}}

Rules:
- Return exactly {TOTAL_QUESTIONS} questions.
- Each question must have exactly 4 options.
- correct_option_index must be an integer from 0 to 3.
- Do not include markdown, code fences, or extra keys.
{retry_suffix}
""".strip()


def _parse_questions(content: str) -> List[StoredQuestion]:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise QuestionGenerationError("Model did not return valid JSON.") from exc

    raw_questions = payload.get("questions")
    if not isinstance(raw_questions, list) or len(raw_questions) != TOTAL_QUESTIONS:
        raise QuestionGenerationError("Model output must include exactly 10 questions.")

    parsed: List[StoredQuestion] = []
    for item in raw_questions:
        question_text = item.get("question")
        options = item.get("options")
        answer_index = item.get("correct_option_index")

        if not isinstance(question_text, str) or not question_text.strip():
            raise QuestionGenerationError("Each question must include non-empty text.")
        if not isinstance(options, list) or len(options) != 4 or not all(
            isinstance(opt, str) and opt.strip() for opt in options
        ):
            raise QuestionGenerationError("Each question must include exactly 4 text options.")
        if not isinstance(answer_index, int) or answer_index < 0 or answer_index > 3:
            raise QuestionGenerationError("correct_option_index must be an integer 0..3.")

        parsed.append(
            StoredQuestion(
                question=question_text.strip(),
                options=[opt.strip() for opt in options],
                correct_option_index=answer_index,
            )
        )
    return parsed


def _generate_once(topic: str, retry: bool = False) -> List[StoredQuestion]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise QuestionGenerationError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a quiz question generator that only outputs valid JSON.",
            },
            {"role": "user", "content": _build_prompt(topic, retry=retry)},
        ],
    )
    content = response.choices[0].message.content or ""
    return _parse_questions(content)


def generate_questions(topic: str) -> List[StoredQuestion]:
    try:
        return _generate_once(topic, retry=False)
    except QuestionGenerationError:
        try:
            return _generate_once(topic, retry=True)
        except QuestionGenerationError as exc:
            raise QuestionGenerationError(
                "Failed to generate a valid 10-question quiz after one retry."
            ) from exc
