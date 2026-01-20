## Now we create file with the name of app.py, here we write a code for streamlit UI.

import streamlit as st

from code_parser import parse_code

st.title("AI Code Reviewer")
code = st.text_area("Code:")

if st.button("Analyze"):
    if code:
        result = parse_code(code)

        if result["success"]:
            st.success("Parsed!")
        else:
            st.error(result["error"]["message"])
    else:
        st.warning("Please enter some code first!")
