import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
result = model.generate_content("what is the capital of india")
print(result.text)