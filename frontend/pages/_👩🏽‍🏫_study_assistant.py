from datetime import datetime

import streamlit as st

from assistants import init_env
from assistants.study_assistant.main import STUDY_ASSISTANT_TEMPLATE
from assistants.study_assistant.study_assistant_builder import (
    StudyAssistantBuilder,
)
from assistants.study_assistant.study_material_ingestor import (
    LangChainNotesIngestionPipeline,
    LangChainNotesIngestor,
)
from assistants.study_assistant.tools import (
    get_langchain_documentation,
    get_repo_readme,
)

st.set_page_config(page_title="Study Assistant", page_icon="📚", layout="wide")

init_env()

st.title("📚 Study Assistant")
st.caption(
    "Ask questions about LangChain concepts or navigate this repository(how to set up through CLI, etc.)."
)

st.divider()

if "docs_ingested" not in st.session_state:
    st.session_state.docs_ingested = False

if not st.session_state.docs_ingested:

    st.info(
        "📥 First time setup: Ingest documents into your Pinecone vector store"
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🚀 Ingest Documents", use_container_width=True, type="primary"
        ):

            with st.spinner("📄 Ingesting README ..."):

                readme_ingestor = LangChainNotesIngestor(
                    langchain_notes_path="./README.md",
                    notes_namespace=f"repo-readme-{datetime.today().date().isoformat()}",
                )
                readme_pipeline = LangChainNotesIngestionPipeline(
                    ingestor=readme_ingestor
                )

                try:

                    readme_pipeline.run()
                    st.success("✅ README ingested successfully!")

                except Exception as e:
                    st.error(f"❌ README ingestion failed: {e}")

            with st.spinner(
                "📚 Ingesting LangChain documentation... (this may take a few minutes)"
            ):

                docs_ingestor = LangChainNotesIngestor()
                docs_pipeline = LangChainNotesIngestionPipeline(
                    ingestor=docs_ingestor
                )

                try:

                    docs_pipeline.run()
                    st.success("✅ LangChain docs ingested successfully!")

                except Exception as e:

                    st.error(f"❌ LangChain docs ingestion failed: {e}")

            st.session_state.docs_ingested = True
            st.rerun()

        if st.button(
            "⏭️ Skip (Already Ingested)",
            help="I have already ingested my docs, I want to use the assistant!",
            use_container_width=True,
            type="secondary",
        ):
            st.session_state.docs_ingested = True
            st.rerun()

    st.stop()

st.success("✅ Documents are ingested and ready!")

if "study_assistant" not in st.session_state:
    with st.spinner("🏗️ Building Study Assistant..."):

        builder = StudyAssistantBuilder(
            raw_system_instructions=STUDY_ASSISTANT_TEMPLATE,
            tools=[get_langchain_documentation, get_repo_readme],
        )
        st.session_state.study_assistant = builder.build()


if "study_messages" not in st.session_state:
    st.session_state.study_messages = []

for message in st.session_state.study_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 Sources"):
                st.markdown(message["sources"])

if user_input := st.chat_input(
    "Try asking about langchain or this repository!"
):

    st.session_state.study_messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.study_assistant.query(user_input)
            st.markdown(response.agent_response)

            if response.sources:
                with st.expander("📚 Sources"):
                    st.markdown(response.sources)

        st.session_state.study_messages.append(
            {
                "role": "assistant",
                "content": response.agent_response,
                "sources": response.sources,
            }
        )
