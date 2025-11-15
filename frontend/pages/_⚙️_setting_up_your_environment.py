import streamlit as st

st.set_page_config(
    page_title="env-setup",
    layout="wide",
    page_icon="⚡️",
)

st.title("🔋 Setting up the runtime environment")
st.caption(
    body="The assistants rely on different services for functionality, you must first create a .env file. All the services used offer free tiers!"
)

st.divider()

st.markdown(body="#### 1️⃣ Create a `.env` file at the project root")
st.code("touch .env", language="bash")

st.markdown(
    "#### ✌🏾 You must now create accounts in these services (all free) and get API keys to use the assistants:"
)

with st.expander("**Groq** - LLM Provider (Default)", expanded=True):

    st.markdown(
        """
Groq provides fast inference for the language models used by all assistants.
Alternatively, you can use Ollama but it's really slow locally.
    
**Steps:**
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add to your `.env` file
"""
    )

    st.code("GROQ_API_KEY=your_groq_api_key_here", language="bash")

with st.expander("**Langsmith** - Tracing(Optional)", expanded=False):

    st.markdown(
        """
Langsmith has an amazing UI to view traces, since this is a study repo: investigating these traces
is how you can maximise your learning.
    
**Steps:**
1. Visit [smith.langchain.com](https://smith.langchain.com)
2. Sign up or log in
3. Create a new project or use default
4. Go to Settings → API Keys
5. Create a new API key
6. Add the following to your `.env` file
"""
    )
    st.code("LANGSMITH_TRACING=true", language="bash")
    st.code("LANGSMITH_API_KEY=your_langsmith_api_key_here", language="bash")
    st.code("LANGSMITH_PROJECT=give_a_project_name", language="bash")

with st.expander(
    "**Tavily** - Search API (Required for Search Assistant)", expanded=False
):
    st.markdown(
        """
Tavily provides optimized search capabilities for the Search Assistant's ReAct agent.
    
**Steps:**
1. Visit [tavily.com](https://tavily.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key
5. Add to your `.env` file
    
**Note:** Only needed if you plan to use the Search Assistant/Study Assistant.
"""
    )
    st.code("TAVILY_API_KEY=your_tavily_api_key_here", language="bash")

with st.expander(
    "**Pinecone** - Vector Database (Required for HR & Study Assistants)",
    expanded=False,
):
    st.markdown(
        """
Pinecone provides vector storage for document retrieval in HR and Study assistants.
    
**Steps:**
1. Visit [pinecone.io](https://www.pinecone.io)
2. Sign up for a free account
3. Create a new index (or use existing)
4. Get your API key from the console
5. Add to your `.env` file
    
**Note:** 
- Only needed for HR Assistant and Study Assistant
- Free tier is sufficient for this project
- Three namespaces will be created: `repo-readme-*`, `study-assistant-batch-*`, and `hr-policies-*`
"""
    )
    st.code(
        """PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=langchain-study""",
        language="bash",
    )

with st.expander("**Logging Level** (Optional)", expanded=False):
    st.markdown(
        """
Set the logging verbosity for debugging and monitoring. I have added a cool `RichHandler` for beautiful logs! 😻🪵
    
**Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`
    
**Recommended:** `INFO` for normal use, `DEBUG` for learning/troubleshooting
"""
    )
    st.code("export LANGCHAIN_STUDY_LOG_LEVEL=DEBUG", language="bash")

st.divider()

st.markdown("#### 📋 Complete `.env` Template")
st.markdown("Copy this template and fill in your actual API keys:")

complete_template = """# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional - Tracing
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=langchain-study

# Optional - Search Assistant and Study Assistant
TAVILY_API_KEY=your_tavily_api_key_here

# Optional - HR & Study Assistants
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=langchain-study

# Optional - Logging
export LANGCHAIN_STUDY_LOG_LEVEL=DEBUG"""

st.code(complete_template, language="bash")

st.divider()

st.success(
    "✅ Once your `.env` file is set up, you're ready to use the assistants!"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button(
        "🚀 Proceed to Assistants", use_container_width=True, type="primary"
    ):
        st.info("👈 Choose an assistant from the sidebar to get started!")
