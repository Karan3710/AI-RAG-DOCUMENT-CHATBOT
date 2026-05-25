import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
from dotenv import load_dotenv

from langchain_community.llms import Ollama

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import SentenceTransformer
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    cache_folder="./models"
)
from langchain_community.llms import Ollama

# ✅ Load env
load_dotenv()


# -------- PDF Processing --------
def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    # ✅ Remove empty chunks
    cleaned_chunks = []

    for chunk in chunks:
        if chunk.page_content and chunk.page_content.strip():
            cleaned_chunks.append(chunk)

    return cleaned_chunks


# -------- Store Docs (CHROMA) --------
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

def store_documents(chunks):

    cleaned_chunks = [
        chunk for chunk in chunks
        if chunk.page_content
        and chunk.page_content.strip()
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=cleaned_chunks,
        embedding=embeddings
    )

    return vector_store


# -------- Create RAG Chain --------


def get_rag_chain(vector_store):

    llm = Ollama(model="phi")

    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Answer ONLY from the provided context.

Context:
{context}

Question:
{question}
""")

    def format_docs(docs):
        return "\n\n".join(
            doc.page_content
            for doc in docs
            if doc.page_content
        )

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain