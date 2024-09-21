Communico GPT
Communico GPT is a Streamlit application that uses LangChain and Hugging Face embeddings to search through documents and provide accurate responses based on user queries. The application is designed to work with PDF documents and can embed, retrieve, and answer questions based on the content of these documents.

Features
Document Loading: Load PDF documents from a specified directory.
Text Splitting: Split the documents into manageable chunks for efficient processing.
Embedding: Use Hugging Face embeddings to create vector representations of the document chunks.
Retrieval: Retrieve relevant document chunks based on user queries using FAISS.
Question Answering: Provide accurate responses based on the retrieved document chunks using LangChain and ChatGroq.
Setup
Prerequisites
Make sure you have the following software installed:

Python 3.8+
Streamlit
LangChain
Hugging Face Transformers
FAISS
dotenv
Installation Steps
Clone the Repository:

bash
git clone https://github.com/yourusername/communico-gpt.git
cd communico-gpt
Install Required Libraries: Install the required Python libraries listed in the requirements.txt file:

bash
pip install -r requirements.txt
Set Up Environment Variables: Create a .env file and add your API keys. Here's an example:

bash
HuggingFace_API_KEY=your-huggingface-api-key
GROQ_API_KEY=your-groq-api-key
Run the Application: Start the Streamlit app by running:

bash
streamlit run app.py
Access the App: Once the app is running, access it at http://localhost:8501 in your web browser.

Code Overview
Main Components
Document Loading:

Uses PyPDFDirectoryLoader to load PDFs from the specified directory.
Example:
st.session_state.loader = PyPDFDirectoryLoader("./Communication_Books")
st.session_state.docs = st.session_state.loader.load()
Text Splitting:

Uses RecursiveCharacterTextSplitter to split the loaded documents into smaller, manageable chunks for embedding.
Example:
st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
Embedding:

Uses HuggingFaceEmbeddings to create vector representations of document chunks for efficient retrieval.
Example:
python
Copy code
st.session_state.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
Retrieval:

Uses FAISS to store and retrieve document vectors based on user queries.
Example:
st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
retriever = st.session_state.vectors.as_retriever()
Question Answering:

Uses LangChain and ChatGroq to generate responses based on retrieved document chunks.
Example:
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({'input': prompt1})
Key Functions
vector_embedding(): Handles the document loading, splitting, and embedding process.
create_stuff_documents_chain(): Combines document chunks into a chain for processing.
create_retrieval_chain(): Creates a retrieval chain that integrates document embeddings and question-answering capabilities.
Usage Instructions
Uploading Documents:
Users can upload PDF documents via the file uploader on the Streamlit interface.
Asking Questions:
After uploading documents, users can input questions related to the document content in the text box.
Viewing Results:
The app provides the most relevant document segments alongside the generated answers. Users can expand the "View Retrieved Document Segments" section to view the content.
Deployment Instructions (Docker)
You can also containerize this application using Docker for easier deployment.

Docker Setup
Build the Docker Image:

bash
docker build -t communico-gpt .
Run the Docker Container:

bash
docker run -p 8501:8501 communico-gpt
This will make the app available at http://localhost:8501 in your web browser.

Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push the branch (git push origin feature-branch).
Open a pull request.
