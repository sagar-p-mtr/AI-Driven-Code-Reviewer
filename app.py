import streamlit as st

st.title("AI-Driven Code Reviewer")
st.subheader("Paste your Python code below")

st.text_area(
    "Code Editor",
    height=350,
    placeholder="Paste your Python code here..."

)