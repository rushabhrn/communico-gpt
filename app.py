import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
DOCS_DIR = os.getenv("DOCS_DIR", "./Communication_Books")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MAX_PAGES = 50   # pages indexed per session, to keep embedding time short
TOP_K = 4        # chunks retrieved per question

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question using only the context below.
    If the answer is not in the context, say you don't know.

    <context>
    {context}
    </context>

    Question: {question}
    """
)


@st.cache_resource
def load_embeddings():
    """Load the embedding model once per server, not on every rerun."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def build_vector_store():
    """Load PDFs, split them into chunks, embed them and keep a FAISS index in the session."""
    if not os.path.isdir(DOCS_DIR):
        st.error(f"Folder not found: {DOCS_DIR}. Create it and add some PDFs.")
        return

    docs = PyPDFDirectoryLoader(DOCS_DIR).load()
    if not docs:
        st.error(f"No PDFs found in {DOCS_DIR}.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs[:MAX_PAGES])
    st.session_state.vectors = FAISS.from_documents(chunks, load_embeddings())
    st.success(f"Indexed {min(len(docs), MAX_PAGES)} pages as {len(chunks)} chunks.")


st.title("Communico GPT")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is not set. Add it to your .env file and restart.")
    st.stop()

llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=GROQ_MODEL)

if st.button("Documents Embedding"):
    with st.spinner("Embedding documents..."):
        build_vector_store()

question = st.text_input("Enter your question from documents")

if question:
    if "vectors" not in st.session_state:
        st.warning("Click 'Documents Embedding' first to index your PDFs.")
        st.stop()

    start = time.perf_counter()
    context_docs = st.session_state.vectors.similarity_search(question, k=TOP_K)
    context = "\n\n".join(doc.page_content for doc in context_docs)
    answer = llm.invoke(prompt.format_messages(context=context, question=question))
    elapsed = time.perf_counter() - start

    st.write(answer.content)
    st.caption(f"Response time: {elapsed:.2f} s")

    with st.expander("Source passages"):
        for doc in context_docs:
            source = os.path.basename(doc.metadata.get("source", "unknown"))
            page = doc.metadata.get("page")
            st.markdown(f"**{source}**" + (f", page {page + 1}" if page is not None else ""))
            st.write(doc.page_content)
            st.write("-----------------------")
