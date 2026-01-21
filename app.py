# import streamlit as st

# from code_parser import parse_code
# from style_checker import show_style_corrected
# from error_detector import detect_errors
# from ai_suggester import get_ai_suggestions

# st.title("AI Code Reviewer")
# st.markdown("Paste your Python code below and click Analyze!")
# code = st.text_area("Code:")

# if st.button("Analyze"):
#     if not code:
#         st.warning("Please enter some code first!")
#     else:
#         st.info("Analyzing your code...")

#         parse_result = parse_code(code)
#         if not parse_result["success"]:
#             st.error("Your code has syntax errors!")
#             st.code(parse_result["error"]["message"])
#             st.stop()
        
#         st.success("Code parsed successfully!")

#         st.subheader("Error Detection Results")

#         error_result = detect_errors(code)

#         if error_result["success"]:
#             if error_result["error_count"] == 0:
#                 st.success("No error found! Your code looks good.")
#             else:
#                 st.warning(f"Found {error_result['error_count']} issue(s):")

#                 for error in error_result["errors"]:
#                     with st.expander(f" {error['type']}", expanded=True):
#                         st.write(f"**Message:** {error['message']}")
#                         st.info(f"**Suggestion:** {error['suggestion']}")
#         else:
#             st.error("Could not analyze code for errors")

#         st.subheader("Style-Corrected Version")

#         try:
#             style_result = show_style_corrected(code)

#             if style_result["success"]:
#                 st.code(style_result["corrected_code"], language="python")
#                 st.caption("This is how you code looks with proper formatting")
#             else:
#                 st.info("Style correction not available")
#         except Exception as e:
#             st.info("Style checking module not found")

#         st.subheader("Your Original Code")
#         st.code(code, language="python")

#         st.subheader("AI Suggestions")

#         suggest = get_ai_suggestions(code)
#         st.info(suggest[0]["message"])

        
"""
AI Code Reviewer Application
Main module for Streamlit-based code review interface.
"""
import streamlit as st
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

            # Display original code
            st.caption("Reference: Your Original Input")
            with st.expander("See Original Code"):
                st.code(code, language="python")

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
                    with st.chat_message("assistant"):
                        st.write_stream(stream_data(suggestion["message"]))
                elif suggestion["type"] == "Error":
                    st.error(suggestion["message"])
    else:
        st.info("Analyze code in the 'Code Suggested' tab first to see AI suggestions.")


