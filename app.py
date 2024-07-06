import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv

load_dotenv()

os.environ['HuggingFace_API_KEY'] = os.getenv("HuggingFace_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

st.title("Communico GPT")

llm = ChatGroq(groq_api_key = groq_api_key,
               model_name="Llama3-8b-8192")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on provided context.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}
    """
)

def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Load documents
        st.session_state.loader = PyPDFDirectoryLoader("./Communication_Books")
        st.session_state.docs = st.session_state.loader.load()
        
        # Debugging statement
        st.write(f"Number of documents loaded: {len(st.session_state.docs)}")
        
        # Split documents
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
        
        # Debugging statement
        st.write(f"Number of document chunks created: {len(st.session_state.final_documents)}")
        
        # Create vector store
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

prompt1 = st.text_input("Enter your question from documents")

if st.button("Documents Embedding"):
    vector_embedding()
    st.write("Vector Store DB is ready!")

import time    

if prompt1:
    start = time.process_time()
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({'input': prompt1})
    st.write(f"Response time: {time.process_time() - start}")
    st.write(response['answer'])
    
    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-----------------------")