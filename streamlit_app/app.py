import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="EduAI Connect", layout="wide")
st.title("EduAI Connect")
st.subheader("AI-Powered Education Analytics")

tab1, tab2, tab3 = st.tabs(["Chat", "Grading Analysis", "At-Risk Students"])

with tab1:
    question = st.text_input("Ask a question about student performance:")
    if st.button("Ask", key="chat_btn"):
        if question:
            response = requests.post(f"{API_URL}/chat", json={"question": question})
            st.write(response.json()["answer"])

with tab2:
    grading_q = st.text_input("Ask about grades:", value="How are students doing in Math?")
    if st.button("Analyze Grades", key="grade_btn"):
        if grading_q:
            response = requests.post(f"{API_URL}/insights/grading", json={"question": grading_q})
            st.write(response.json()["analysis"])

with tab3:
    risk_q = st.text_input("Ask about at-risk students:", value="Which students are at risk?")
    if st.button("Find At-Risk Students", key="risk_btn"):
        if risk_q:
            response = requests.post(f"{API_URL}/insights/at-risk", json={"question": risk_q})
            st.write(response.json()["analysis"])
