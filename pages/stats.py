import streamlit as st

def show_stats(chat_history):
    st.header("Chat Statistics Dashboard")
    total_messages = len(chat_history)
    assistants = [msg.get("role") for msg in chat_history if msg.get("role") != "user"]
    most_used_assistant = max(set(assistants), key=assistants.count) if assistants else "N/A"
    avg_messages = total_messages / (st.session_state.get("session_count", 1))
    st.write(f"Total messages: {total_messages}")
    st.write(f"Most used assistant: {most_used_assistant}")
    st.write(f"Average messages per session: {avg_messages:.2f}")
    timestamps = [msg.get("timestamp") for msg in chat_history if "timestamp" in msg]
    if timestamps:
        st.write(f"First message: {timestamps[0]}")
        st.write(f"Last message: {timestamps[-1]}")
