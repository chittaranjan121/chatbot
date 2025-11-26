import streamlit as st
from db.conversations import (
    create_conversation,
    add_message,
    get_conversation,
    get_all_conversations
)

from app.chat_logic import get_ai_response

st.set_page_config(page_title="LangChain Chat", page_icon="💬")

st.title("🤖 LangChain + OpenAI + Mongo Chat")

# Sidebar: list conversations
with st.sidebar:
    st.header("Conversations")
    convos = get_all_conversations()

    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None

    for c in convos:
        if st.button(c["_id"]):
            st.session_state.conversation_id = c["_id"]

# Main screen logic
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

cid = st.session_state.conversation_id

# Show old messages
if cid:
    data = get_conversation(cid)
    for msg in data["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Input box
user_input = st.chat_input("Type a message...")

if user_input:
    if cid is None:
        # Create new conversation
        cid = create_conversation(user_input)
        st.session_state.conversation_id = cid
    else:
        add_message(cid, "user", user_input)

    with st.chat_message("user"):
        st.write(user_input)

    # AI Response
    output = get_ai_response(cid)
    with st.chat_message("assistant"):
        st.write(output)
