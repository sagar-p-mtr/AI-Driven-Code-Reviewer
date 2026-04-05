from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
import json
import re

from dotenv import load_dotenv


def _get_openrouter_api_key():
    """Load OPENROUTER_API_KEY from Streamlit secrets first, then .env."""
    try:
        import streamlit as st
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        load_dotenv()
        return os.getenv("OPENROUTER_API_KEY")


def _build_model(api_key):
    """Create an OpenRouter client for code suggestions."""
    return ChatOpenAI(
        model="qwen/qwen3-coder:free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3,
        max_tokens=2048,
        model_kwargs={"response_format": {"type": "json_object"}},
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI Code Reviewer",
        },
    )


def _parse_json_response(text):
    """Parse model output into JSON, tolerating wrappers/fences."""
    raw = text.strip()

    # Truncate if too long (safety measure for length limit errors)
    MAX_LEN = 8000
    if len(raw) > MAX_LEN:
        raw = raw[:MAX_LEN]

    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        first = raw.find("{")
        last = raw.rfind("}")
        if first == -1 or last == -1 or last <= first:
            raise
        return json.loads(raw[first:last + 1])


def get_ai_suggestions(code_string):
    """
    WHAT IT DOES: Asks AI improvements ideas
    """
    prompt = f"""
You are a strict Python code reviewer.

Return ONLY valid JSON with this exact schema and no extra text:
{{
    "original_code": "string",
    "suggestions": {{
        "readability": "string (1-2 sentences)",
        "performance": "string (1-2 sentences)",
        "best_practices": "string (1-2 sentences)"
    }},
    "coding_style_analysis": {{
        "naming_issues": "string (concise)",
        "structure_issues": "string (concise)",
        "logic_type_issues": "string (concise)",
        "score": "X/10"
    }},
    "corrected_code": "string (complete runnable code)",
    "pep8_score_after_corrections": "X/10"
}}

IMPORTANT - Response must be concise:
- Keep all string values brief (1-3 sentences max, except corrected_code).
- Do NOT include examples or explanations beyond what's required.
- Do not wrap JSON in markdown fences.
- Preserve newlines in code strings as \\n.
- corrected_code must contain full runnable corrected Python code.

Code:
{code_string}
"""

    try:
        api_key = _get_openrouter_api_key()
        if not api_key:
            return [{
                "type": "Error",
                "message": "OPENROUTER_API_KEY is missing. Add it to .env or Streamlit secrets.",
                "severity": "Info"
            }]

        model = _build_model(api_key)
        response = model.invoke(
            [HumanMessage(content=prompt)]
        )

        ai_message = response.content if isinstance(response.content, str) else str(response.content)

        def _validate_payload(parsed_json):
            required_top = [
                "original_code",
                "suggestions",
                "coding_style_analysis",
                "corrected_code",
                "pep8_score_after_corrections",
            ]
            for key in required_top:
                if key not in parsed_json:
                    raise ValueError(f"Missing required key: {key}")

            if not isinstance(parsed_json["suggestions"], dict):
                raise ValueError("'suggestions' must be an object")
            if not isinstance(parsed_json["coding_style_analysis"], dict):
                raise ValueError("'coding_style_analysis' must be an object")

            for key in ["readability", "performance", "best_practices"]:
                if key not in parsed_json["suggestions"]:
                    raise ValueError(f"Missing suggestions.{key}")

            for key in ["naming_issues", "structure_issues", "logic_type_issues", "score"]:
                if key not in parsed_json["coding_style_analysis"]:
                    raise ValueError(f"Missing coding_style_analysis.{key}")

            return parsed_json

        try:
            parsed = _validate_payload(_parse_json_response(ai_message))
        except Exception:
            # AI-only retry: ask the model to repair its own output into valid JSON.
            repair_prompt = f"""
Convert the following content into valid JSON that matches this exact schema.
Return ONLY JSON, no markdown, no extra text. Keep all values concise.

Schema:
{{
  "original_code": "string",
  "suggestions": {{
    "readability": "string (1-2 sentences)",
    "performance": "string (1-2 sentences)",
    "best_practices": "string (1-2 sentences)"
  }},
  "coding_style_analysis": {{
    "naming_issues": "string (concise)",
    "structure_issues": "string (concise)",
    "logic_type_issues": "string (concise)",
    "score": "X/10"
  }},
  "corrected_code": "string (complete runnable code)",
  "pep8_score_after_corrections": "X/10"
}}

Important:
- Escape newlines inside JSON string values as \\n.
- Ensure every string is properly closed with double quotes.
- Keep all descriptions brief and focused.
- Do NOT include explanations beyond the schema fields.

Content to convert:
{ai_message}
"""
            repaired = model.invoke([HumanMessage(content=repair_prompt)])
            repaired_message = repaired.content if isinstance(repaired.content, str) else str(repaired.content)
            parsed = _validate_payload(_parse_json_response(repaired_message))

        payload = parsed

        return [{
            "type": "AISuggestion",
            "message": json.dumps(payload, ensure_ascii=False, indent=2),
            "payload": payload,
            "severity": "Info"
        }]
    except Exception as e:
        return [{
            "type": "Error",
            "message": str(e),
            "severity": "Info"
        }]
