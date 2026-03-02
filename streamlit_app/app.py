import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="EduAI Connect", page_icon="🎓", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🎓 EduAI Connect")
    st.caption("AI-Powered Education Analytics")
    st.divider()
    role = st.selectbox("Your Role", ["Teacher", "Administrator"])
    st.divider()
    st.caption("Powered by Amazon Bedrock + LangChain")
    st.caption("FERPA Compliant 🔒")

# Header
st.title("EduAI Connect")
st.subheader("AI-Powered Education Analytics Dashboard")

# Stat cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", "75")
col2.metric("At-Risk", "4", delta="-2", delta_color="inverse")
col3.metric("Avg Engagement", "72%")
col4.metric("Courses", "8")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Grading Analysis", "⚠️ At-Risk Students"])

with tab1:
    st.subheader("Ask about student performance")
    question = st.text_input("Type your question:", placeholder="e.g., Who needs help in Math?")
    if st.button("Ask", key="chat_btn", type="primary"):
        if question:
            with st.spinner("Analyzing student data..."):
                response = requests.post(f"{API_URL}/chat", json={"question": question})
                st.write(response.json()["answer"])

with tab2:
    st.subheader("Grade Analysis")
    grading_q = st.text_input("Ask about grades:", value="How are students doing in Math?")
    if st.button("Analyze Grades", key="grade_btn", type="primary"):
        if grading_q:
            with st.spinner("Running grading analysis..."):
                response = requests.post(f"{API_URL}/insights/grading", json={"question": grading_q})
                st.write(response.json()["analysis"])

with tab3:
    st.subheader("At-Risk Student Detection")
    risk_q = st.text_input("Ask about at-risk students:", value="Which students are at risk of failing?")
    if st.button("Find At-Risk Students", key="risk_btn", type="primary"):
        if risk_q:
            with st.spinner("Identifying at-risk students..."):
                response = requests.post(f"{API_URL}/insights/at-risk", json={"question": risk_q})
                st.write(response.json()["analysis"])