from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

import streamlit as st # TO do this install streamit by run this command pip install streamlit

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

st.header('Research Tool')

user_input = st.text_input('Enter your prompt')

if st.button('Summarize'):
    result = model.invoke(user_input)
    st.write(result.content)