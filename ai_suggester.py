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
    repo_id='mistralai/Mistral-7B-Instruct-v0.3',
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

        1. Display the original code first.

        2. Provide 2–3 lines brief suggestions focusing on:
        - Code readability
        - Performance
        - Best practices

        3. Follow the PEP8 standard coding guidelines for Coding Style Analysis:
            • Highlight issues like improper indentation, naming conventions, or long functions.
            • Score submissions based on style compliance
        
        4. Show the corrected full code only once at the end.

        5. Strictly follow the same response format for every execution.

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

