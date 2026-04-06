#AI Code Reviewer Application
#Main module for Streamlit-based code review interface.

import streamlit as st
import re
import time
import os
from dotenv import load_dotenv

from code_parser import parse_code
from error_detector import detect_errors
from ai_suggester import get_ai_suggestions

load_dotenv()

# Initialize session state
if "analyzed_code" not in st.session_state:
    st.session_state.analyzed_code = None


def stream_data(text):
    """
    Yields text word by word for the typewriter effect.
    
    Args:
        text (str): Text to stream word by word.
    
    Yields:
        str: Word with trailing space.
    """
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


def _extract_section(text, start_label, end_label=None):
    """Return the text between two section labels."""
    if end_label:
        pattern = rf"{re.escape(start_label)}\s*(.*?)(?=\n\s*{re.escape(end_label)}|\Z)"
    else:
        pattern = rf"{re.escape(start_label)}\s*(.*)"

    match = re.search(pattern, text, flags=re.S | re.I)
    return match.group(1).strip() if match else ""


def _strip_code_fences(text):
    """Remove markdown fences so code can be rendered in a code box."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:python)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _section_header_pattern(title):
    """Build a tolerant regex for section headings with optional numbering."""
    escaped = re.escape(title)
    # Allow optional trailing words after the base heading title,
    # e.g. "SUGGESTIONS FOR IMPROVEMENT" for title "SUGGESTIONS".
    return rf"^\s*(?:\d+\.\s*)?{escaped}(?:[^\n:]*)\s*:?[ \t]*$"


def _extract_section_by_title(text, start_title, end_title=None):
    """Extract a section using tolerant heading matching."""
    start_pattern = _section_header_pattern(start_title)
    if end_title:
        end_pattern = _section_header_pattern(end_title)
        pattern = rf"{start_pattern}\s*(.*?)(?=\n{end_pattern}|\Z)"
    else:
        pattern = rf"{start_pattern}\s*(.*)"

    match = re.search(pattern, text, flags=re.S | re.I | re.M)
    return match.group(1).strip() if match else ""


def _render_ai_review(review_text):
    """Render structured AI output with code boxes and copy buttons."""
    original_code = _strip_code_fences(
        _extract_section_by_title(
            review_text,
            "ORIGINAL CODE",
            "SUGGESTIONS"
        )
    )
    suggestions = _extract_section_by_title(
        review_text,
        "SUGGESTIONS",
        "CODING STYLE ANALYSIS (PEP8)"
    )
    analysis = _extract_section_by_title(
        review_text,
        "CODING STYLE ANALYSIS (PEP8)",
        "CORRECTED CODE"
    )
    corrected_code = _strip_code_fences(
        _extract_section_by_title(
            review_text,
            "CORRECTED CODE",
            "PEP8 COMPLIANCE SCORE AFTER CORRECTIONS"
        )
    )
    score = _extract_section_by_title(
        review_text,
        "PEP8 COMPLIANCE SCORE AFTER CORRECTIONS"
    )

    st.markdown("### Original Code")
    st.code(original_code or review_text, language="python")

    st.markdown("### Suggestions")
    if suggestions:
        st.markdown(suggestions)
    else:
        st.markdown("No suggestions available.")

    st.markdown("### Coding Style Analysis (PEP8)")
    if analysis:
        st.markdown(analysis)
    else:
        st.markdown("No analysis available.")

    st.markdown("### Corrected Code")
    st.code(corrected_code or review_text, language="python")

    if score:
        st.markdown("### PEP8 Compliance Score After Corrections")
        st.markdown(score)


def _render_ai_review_payload(payload):
    """Render structured review payload returned by the AI layer."""
    original_code = payload.get("original_code", "")
    corrected_code = payload.get("corrected_code", "")
    suggestions = payload.get("suggestions", {})
    analysis = payload.get("coding_style_analysis", {})
    pep8_score = payload.get("pep8_score_after_corrections", "N/A")

    st.markdown("### Original Code")
    st.code(original_code, language="python")

    st.markdown("### Suggestions")
    st.markdown(f"- Readability: {suggestions.get('readability', 'N/A')}")
    st.markdown(f"- Performance: {suggestions.get('performance', 'N/A')}")
    st.markdown(f"- Best Practices: {suggestions.get('best_practices', 'N/A')}")

    st.markdown("### Coding Style Analysis (PEP8)")
    st.markdown(f"- Naming Issues: {analysis.get('naming_issues', 'N/A')}")
    st.markdown(f"- Structure Issues: {analysis.get('structure_issues', 'N/A')}")
    st.markdown(f"- Logic & Type Issues: {analysis.get('logic_type_issues', 'N/A')}")
    st.markdown(f"- Score: {analysis.get('score', 'N/A')}")

    st.markdown("### Corrected Code")
    st.code(corrected_code, language="python")

    st.markdown("### PEP8 Compliance Score After Corrections")
    st.markdown(f"- Score: {pep8_score}")

st.set_page_config(
    page_title="AI Code Reviewer Application",
    page_icon="🤖",
    layout="wide"
)

st.image("logo.png", width=250)
st.title("AI Code Reviewer")

if st.button("Refresh"):
    st.rerun()

tab1, tab2 = st.tabs(["Code Suggested", "AI Suggestions"])

with tab1:
    st.markdown(
        "Paste your Python code below and click **Analyze** to get feedback "
        "on errors, style, and AI suggestions."
    )

    code = st.text_area("Code Input:", height=200)

    if st.button("Analyze", type="primary"):
        if not code:
            st.warning("Please enter some code first!")
        else:
            # Check if code parses successfully
            parse_result = parse_code(code)
            
            if parse_result["success"]:
                st.success("✓ Code parsed successfully!")
            
            # Display error detection results
            st.subheader("Error Detection Results")
            error_result = detect_errors(code)

            if error_result["success"]:
                if error_result["error_count"] == 0:
                    st.success("✓ No issues found! Your code looks clean.")
                else:
                    st.warning(
                        f"Found {error_result['error_count']} potential issue(s):"
                    )
                    for error in error_result["errors"]:
                        with st.expander(f"{error['type']}", expanded=True):
                            st.write(f"**Message:** {error['message']}")
                            st.info(f"**Suggestion:** {error['suggestion']}")
            else:
                st.error("Could not analyze code for errors")

           

            st.markdown("---")

            # Store code in session state for AI suggestions tab
            st.session_state.analyzed_code = code


with tab2:
    st.markdown("AI-powered suggestions and improvements for your code.")

    if st.session_state.analyzed_code:
        with st.spinner("Asking the AI for advice..."):
            suggestions = get_ai_suggestions(st.session_state.analyzed_code)

            for suggestion in suggestions:
                if suggestion["type"] == "AISuggestion":
                    with st.container(border=True):
                        if isinstance(suggestion.get("payload"), dict):
                            _render_ai_review_payload(suggestion["payload"])
                        else:
                            _render_ai_review(suggestion["message"])
                elif suggestion["type"] == "Error":
                    st.error(suggestion["message"])
    else:
        st.info("Analyze code in the 'Code Suggested' tab first to see AI suggestions.")


