import streamlit as st
from agent import query_agent

st.set_page_config(page_title="Weather Chatbot", page_icon="🌤️")
st.title("🌤️ Weather Data Chatbot")
st.markdown("Ask questions about your weather data stored in Databricks Delta tables.")

question = st.text_input("Ask me anything (e.g., average temperature in Delhi last week):")

if question:
    with st.spinner("Thinking..."):
        answer = query_agent(question)
        st.success(answer)
