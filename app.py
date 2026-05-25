import streamlit as st
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

from rag_pipeline import process_pdf, store_documents, get_rag_chain
from auth import login, logout, init_session, signup
from db import chat_collection

# ✅ MUST be first Streamlit command
st.set_page_config(page_title="RAG App", layout="wide")

# Init session
init_session()

# 🔐 Auth
if not st.session_state["logged_in"]:
    signup()
    login()
    st.stop()

logout()

st.title("📄 Chat with Your Documents (RAG)")

# -------------------------
# 📂 Upload PDFs
# -------------------------
uploaded_files = st.file_uploader(
    "Upload PDFs",
    type="pdf",
    accept_multiple_files=True
)

# -------------------------
# 🧠 Process Documents (ONLY ONCE)
# -------------------------
if uploaded_files and "vector_store" not in st.session_state:
    all_chunks = []

    for file in uploaded_files:
        file_path = f"temp_{file.name}"

        with open(file_path, "wb") as f:
            f.write(file.read())

        chunks = process_pdf(file_path)
        all_chunks.extend(chunks)

    st.success("Documents processed!")

    st.session_state.vector_store = store_documents(all_chunks)
    st.session_state.rag_chain = get_rag_chain(st.session_state.vector_store)

# -------------------------
# 💬 Chat UI
# -------------------------
if "rag_chain" in st.session_state:

    if "messages" not in st.session_state:
        st.session_state.messages = []

query = st.chat_input("Ask something about your documents...")

st.write("DEBUG QUERY:", query)
print("DEBUG QUERY:", query)
print(type(query))

if query and query.strip():

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # 🔥 FORCE STRING
    query = str(query)

    # Get answer
    answer = st.session_state.rag_chain.invoke(query)

    # Save AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # Save to MongoDB
    chat_collection.insert_one({
        "user": st.session_state["user"],
        "question": query,
        "answer": answer
    })
    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])