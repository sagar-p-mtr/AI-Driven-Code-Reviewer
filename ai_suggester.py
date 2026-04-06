from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os

# Try to load from Streamlit secrets first, then fallback to .env
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    GROQ_MODEL = st.secrets.get("GROQ_MODEL", "llama-3.1-8b-instant")
except:
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

model = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.3,
    timeout=120,
)


def get_ai_suggestions(code_string):
    """
    WHAT IT DOES: Asks AI improvements ideas
    """
    prompt = f""" 
    
            You are a strict Python code reviewer.

            Follow the EXACT response format below. Do NOT add extra explanations.

            1. ORIGINAL CODE:
            <the original code to review>

            2. SUGGESTIONS FOR IMPROVEMENT:
            - Readability:
            - Performance:
            - Best Practices:

            3. CODING STYLE ANALYSIS (PEP8):
            - Naming Issues:
            - Structure Issues:
            - Logic & Type Issues:
            - Score: X/10

            4. CORRECTED CODE:
            <only final corrected code>

            5. PEP8 COMPLIANCE SCORE AFTER CORRECTIONS:
            - Score: X/10

            RULES:
            - Do NOT explain anything outside the format.
            - Do NOT add extra paragraphs.
            - Keep suggestions strictly 2-3 lines total.
            - Always follow same headings and order.
            - Correct code must appear ONLY once at the end.

     
    """

    try: 
        response = model.invoke(
            [HumanMessage(content=prompt)]
        )

        ai_message = response.content
        print(ai_message)

        return [{
            "type": "AISuggestion",
            "message": ai_message,
            "severity": "Info"
        }]
    except Exception as e:
        return [{
            "type": "Error",
            "message": str(e),
            "severity": "Info"
        }]
