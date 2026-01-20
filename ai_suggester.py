from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='Qwen/Qwen2.5-7B-Instruct',
    temperature=0.3
)

model = ChatHuggingFace(llm=llm)


def get_ai_suggestions(code_string):
    """
    WHAT IT DOES: Asks AI improvements ideas
    """
    prompt = f"""
    Review this Python code and suggest improvements: 
    {code_string}. 
    Provide 2-3 brief suggestions for: 
    1. Code readability
    2. Performance
    3. Best practices
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
            "message": e,
            "severity": "Info"
        }]

