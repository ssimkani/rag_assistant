from utils.vector_store import *
from utils.chat_helper import *
from utils.embedder import *
from utils.build_prompt import *
from utils.config import *
import streamlit as st
import time

st.set_page_config(page_title=APP_TITLE, layout="wide")

# === User Authentication Check ===
if "uid" not in st.session_state:
    st.warning("Please log in to access chat feature.")
    time.sleep(1)
    st.switch_page("login.py")
    st.stop()

st.title(APP_TITLE)
st.markdown(
    "<style>" + open("./style/style.css").read() + "</style>", unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    with st.expander("## 🤖 About RAG Assistant"):
        st.markdown(
        """
This chatbot, powered by Gemini 2.5 Flash, is a Retrieval-Augmented Generation (RAG) assistant 
designed to help you retrieve and understand information from your personal notes. This assistant can provide accurate and contextually relevant answers based the content of your notes.
        """
    )

    for _ in range(25):
        st.write("")

    if st.button("🆕 New Chat"):
        st.session_state["messages"] = []
        st.rerun()

    if st.button("🔓 Log Out"):
        st.session_state["reset_chat"] = True
        for key in ["email", "uid", "id_token"]:
            st.session_state.pop(key, None)
        st.rerun()


# === Session State Initialization ===
if st.session_state.get("reset_chat", False):
    st.session_state["messages"] = []
    load_llm.clear()
    st.session_state["reset_chat"] = False

# Ensure messages is initialized if not set or was cleared above
if "messages" not in st.session_state or not st.session_state["messages"]:
    st.session_state["messages"] = []

# Previous Messages
for i, msg in enumerate(st.session_state.messages):
    with st.container():
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Set uid
uid = st.session_state["uid"]

# Chat Input
if user_input := st.chat_input("Ask anything"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a message before submitting.")
        st.stop()

    # Show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # RAG Search
            context_chunks = search_top_k(uid, user_input)
            prompt = build_prompt(user_input, context_chunks)
            response = generate_response(prompt)
            st.markdown(response)
    # Append to messages
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Source documents
    with st.expander("📚 Relevant Notes"):
        for i, doc in enumerate(context_chunks):
            st.markdown(
                f"""
                <div class=\"source-chunk\">
                    <div class=\"chunk-title\">#{i+1}</div>
                    <div class=\"chunk-body\">{doc.strip()}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
