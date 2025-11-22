"""
Streamlit frontend page for the Code Review Assistant
"""
import streamlit as st
from assistants.code_review_assistant.code_review_assistant_builder import CodeReviewAssistantBuilder

st.title("Code Review Assistant")

code = st.text_area("Enter Python code to review", height=300)

if st.button("Review"):
    if not code.strip():
        st.warning("Please provide some Python code to review.")
    else:
        builder = CodeReviewAssistantBuilder()
        assistant = builder.build()
        resp = assistant.query(code)

        st.subheader("Summary")
        st.write(resp.review_summary)

        st.subheader("Severity Score")
        sc = resp.severity_score
        if sc > 0.66:
            color = "red"
        elif sc > 0.33:
            color = "orange"
        else:
            color = "green"
        st.markdown(f"<div style='color:{color}'>**{sc:.2f}**</div>", unsafe_allow_html=True)

        st.subheader("Issues Found")
        for iss in resp.issues_found:
            with st.expander(f"{iss.severity.upper()} - {iss.message}"):
                st.write(f"Line: {iss.line_no}")
                if iss.suggestion:
                    st.write("**Suggestion:** ", iss.suggestion)
