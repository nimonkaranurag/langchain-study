import streamlit as st

from assistants import init_env
from assistants.search_assistant.search_assistant_builder import (
    SearchAssistantBuilder,
)

st.set_page_config(page_title="Search Assistant", page_icon="🔍", layout="wide")

init_env()

st.title("🔍 Search Assistant")
st.caption(
    "A ReAct search agent with structured outputs, powered by Tavily Search. NOTE: This assistant does NOT maintain the context, the others do!"
)

st.divider()

if "search_assistant" not in st.session_state:
    with st.spinner("🏗️ Building Search Assistant..."):
        builder = SearchAssistantBuilder()
        st.session_state.search_assistant = builder.build()

if "search_messages" not in st.session_state:
    st.session_state.search_messages = []

for message in st.session_state.search_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                st.markdown(message["sources"])

if user_input := st.chat_input("Search the web!"):

    st.session_state.search_messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🔎 Searching..."):
            response = st.session_state.search_assistant.query(user_input)
            st.markdown(response.agent_response)

            if response.sources:
                with st.expander("📚 Sources"):
                    st.markdown(response.sources)

        st.session_state.search_messages.append(
            {
                "role": "assistant",
                "content": response.agent_response,
                "sources": response.sources,
            }
        )
