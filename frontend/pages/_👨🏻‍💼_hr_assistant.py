import streamlit as st
import json
import os

from assistants import __root_dir__, init_env
from assistants.logger import get_logger
from assistants.hr_assistant.hr_policies_ingestor import (
    HRPoliciesIngestor,
    HRPoliciesIngestionPipeline,
)
from assistants.hr_assistant.hr_assistant_builder import HRAssistantBuilder
from assistants.hr_assistant.tools import (
    get_relevant_company_policies,
    request_time_off,
)
from assistants.hr_assistant.main import load_system_instructions

init_env()

st.set_page_config(
    page_title="HR Assistant",
    page_icon="👔",
    layout="wide"
)
st.caption("Ask about company policies for Nimo Inc. or request time off for: `nimo@ibm.com`!")

st.divider()

if "hr_docs_ingested" not in st.session_state:
    st.session_state.hr_docs_ingested = False

if not st.session_state.hr_docs_ingested:

    st.info("📥 First time setup: Ingest HR policies into your Pinecone vector store")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:

        if st.button("🚀 Ingest HR Policies", use_container_width=True, type="primary"):
            with st.spinner("📄 Ingesting HR policies ... (might take a minute or two)"):
                
                try:

                    hr_ingestor = HRPoliciesIngestor()
                    hr_pipeline = HRPoliciesIngestionPipeline(ingestor=hr_ingestor)
                    hr_pipeline.run()

                    st.success("✅ HR policies ingested successfully!")

                    st.session_state.hr_docs_ingested = True

                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Ingestion failed: {e}")
    
        if st.button("⏭️ Skip (Already Ingested)", use_container_width=True, type="secondary"):
            
            st.session_state.hr_docs_ingested = True
            st.rerun()
    
    st.stop()

st.success("✅ HR policies are ready!")

st.cache_data(load_system_instructions)

if "hr_assistant" not in st.session_state:

    with st.spinner("🏗️ Building HR Assistant..."):

        raw_instructions, instruction_vars = load_system_instructions()
        
        builder = HRAssistantBuilder(
            raw_system_instructions=raw_instructions,
            system_instruction_variables=instruction_vars,
            tools=[request_time_off, get_relevant_company_policies],
        )
        st.session_state.hr_assistant = builder.build()

if "hr_messages" not in st.session_state:
    st.session_state.hr_messages = []

for message in st.session_state.hr_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if user_input := st.chat_input("Ask about company policies or request time off!"):

    st.session_state.hr_messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):
            response = st.session_state.hr_assistant.query(user_input)
            st.markdown(response)
        
        st.session_state.hr_messages.append({
            "role": "assistant",
            "content": response
        })