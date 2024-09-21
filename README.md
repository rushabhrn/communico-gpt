# Communico GPT

Communico GPT is a Streamlit application that uses LangChain and Hugging Face embeddings to search through documents and provide accurate responses based on user queries. The application is designed to work with PDF documents and can embed, retrieve, and answer questions based on the content of these documents.

## Features

- **Document Loading**: Load PDF documents from a specified directory.
- **Text Splitting**: Split the documents into manageable chunks.
- **Embedding**: Use Hugging Face embeddings to create vector representations of the document chunks.
- **Retrieval**: Retrieve relevant document chunks based on user queries.
- **Question Answering**: Provide accurate responses based on the retrieved document chunks.

## Setup

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://github.com/hwchase17/langchain)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [dotenv](https://pypi.org/project/python-dotenv/)

### Code Overview

## Main Components
Document Loading: Uses PyPDFDirectoryLoader to load PDFs from the specified directory.
Text Splitting: Uses RecursiveCharacterTextSplitter to split the loaded documents into chunks.
Embedding: Uses HuggingFaceEmbeddings to create vector representations of the document chunks.
Retrieval: Uses FAISS to create a vector store and retrieve relevant chunks based on user queries.
Question Answering: Uses ChatGroq for generating responses based on the retrieved document chunks.

## Key Functions
vector_embedding(): Handles the loading, splitting, and embedding of documents.
create_stuff_documents_chain(): Creates a chain for combining document chunks.
create_retrieval_chain(): Creates a retrieval chain using the vector store and document chain.
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

