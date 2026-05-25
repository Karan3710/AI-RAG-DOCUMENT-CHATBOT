# AI-RAG-DOCUMENT-CHATBOT
An AI-powered Retrieval-Augmented Generation (RAG) chatbot built using Streamlit, LangChain, Chroma, MongoDB, and Ollama with the phi large language model.  The application allows users to upload multiple PDF documents and interact with them through a conversational AI interface.
The application allows users to upload multiple PDF documents and interact with them through a conversational AI interface. The system processes uploaded documents, generates embeddings, stores them in a vector database, retrieves relevant context, and produces intelligent responses using a local LLM.

🚀 Features
🔐 User Authentication (Signup/Login with password hashing)
📄 Upload and process multiple PDF documents
🧠 RAG (Retrieval-Augmented Generation) pipeline
💬 Conversational chat interface
📚 Semantic document search using embeddings
🗂️ Persistent vector storage with ChromaDB
🛢️ Chat history storage using MongoDB
🤖 Local AI inference using Ollama + Phi model
⚡ Streamlit-based responsive UI

🛠️ Tech Stack
Python
Streamlit
LangChain
ChromaDB
MongoDB
Ollama
Phi LLM
Sentence Transformers
HuggingFace Embeddings

📌 Workflow
User uploads PDF files
PDFs are processed and split into chunks
Embeddings are generated for document chunks
Chunks are stored in Chroma Vector Database
User asks questions in chat interface
Relevant context is retrieved from vector DB
Phi model generates contextual responses
Conversations are stored in MongoDB
🎯 Use Cases
AI Document Assistant
Research Paper Chatbot
PDF Knowledge Retrieval
Internal Company Knowledge Base
AI Study Assistant

▶️ Run Locally
pip install -r requirements.txt

ollama pull phi

ollama serve

streamlit run app.py
