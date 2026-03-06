import streamlit as st
from chain import build_chain

st.set_page_config(
    page_title="RBI Report Chatbot",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 RBI Annual Report Chatbot")
st.caption("Ask any quesion about the RBI Annual Report 2024-25")

@st.cache_resource
def get_chain():
    return build_chain()

result = get_chain()
chain = result[0]
retriever = result[1]

# Example questions to guide others
st.markdown("**Try asking:**")
col1, col2 = st.columns(2)
with col1:
    st.code("What was India's GDP growth rate?")
    st.code("What is RBIS's inflation target?")
with col2:
    st.code("How did the rupee perform in 2024?")
    st.code("What are the key risks to the economy?")

# Input
question = st.text_input("Your question:", placeholder="Type your question here...")

if question:
    with st.spinner("Searching the report..."):
        answer = chain.invoke(question)
        sources = retriever.invoke(question)

    # Answer
    st.markdown("### Answer")
    st.write(answer)

    # Source chunks — this is the trust factor
    with st.expander("📄 Source passages from the report"):
        for i, doc in enumerate(sources):
            st.markdown(f"**Passage {i+1}:**")
            st.caption(doc.page_content)
            st.divider()


