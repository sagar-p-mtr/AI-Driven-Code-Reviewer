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
        model="qwen/qwen3.6-plus:free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.3,
        max_tokens=1024,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI Code Reviewer",
        },
    )


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
        "readability": "string",
        "performance": "string",
        "best_practices": "string"
    }},
    "coding_style_analysis": {{
        "naming_issues": "string",
        "structure_issues": "string",
        "logic_type_issues": "string",
        "score": "X/10"
    }},
    "corrected_code": "string",
    "pep8_score_after_corrections": "X/10"
}}

Rules:
- Do not wrap JSON in markdown fences.
- Preserve newlines in code strings.
- corrected_code must contain full runnable corrected Python code.
- Keep suggestions concise.

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

        # Try strict parse first; if model adds wrapper text, extract JSON object.
        try:
            parsed = json.loads(ai_message)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", ai_message, flags=re.S)
            if not match:
                raise ValueError("Model response is not valid JSON")
            parsed = json.loads(match.group(0))

        payload = {
            "original_code": parsed.get("original_code", code_string),
            "suggestions": parsed.get("suggestions", {}),
            "coding_style_analysis": parsed.get("coding_style_analysis", {}),
            "corrected_code": parsed.get("corrected_code", code_string),
            "pep8_score_after_corrections": parsed.get("pep8_score_after_corrections", "N/A")
        }

        return [{
            "type": "AISuggestion",
            "message": ai_message,
            "payload": payload,
            "severity": "Info"
        }]
    except Exception as e:
        return [{
            "type": "Error",
            "message": str(e),
            "severity": "Info"
        }]
