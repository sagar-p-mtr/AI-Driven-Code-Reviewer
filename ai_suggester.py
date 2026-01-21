from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
import os

# Try to load from Streamlit secrets first, then fallback to .env
try:
    import streamlit as st
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    HF_TOKEN = os.getenv("HF_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id='Qwen/Qwen2.5-7B-Instruct',
    temperature=0.3,
    huggingfacehub_api_token=HF_TOKEN,
    max_new_tokens=1024,
    timeout=120
)

model = ChatHuggingFace(llm=llm)


def get_ai_suggestions(code_string):
    """
    WHAT IT DOES: Asks AI improvements ideas
    """
    prompt = f""" 
    Explain Why Suggestions Were Made: for examples-
    Not just: “Remove unused import”
    But: “Unused imports increase memory usage and reduce code readability.”

    Focused on Provide 2-3 brief suggestions for: 
    1. Code readability
    2. Performance
    3. Best practices
    .
    Follow the PEP8 standard coding guidelines for Coding Style Analysis: 
    ●   Highlight issues like improper indentation, naming conventions, or long functions.
    ●	Score submissions based on style compliance
    
    please strict to the answer in same format for every refresh,

    Code:
        {code_string}
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

