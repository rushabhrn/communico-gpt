# **Communico GPT**

**Communico GPT** is a **Streamlit** application that uses **LangChain** and **Hugging Face embeddings** to search through documents and provide accurate responses based on user queries. The application is designed to work with PDF documents and can embed, retrieve, and answer questions based on the content of these documents.

## **Features**
- **Document Loading**: Load PDF documents from a specified directory.
- **Text Splitting**: Split the documents into manageable chunks for efficient processing.
- **Embedding**: Use **Hugging Face embeddings** to create vector representations of the document chunks.
- **Retrieval**: Retrieve relevant document chunks based on user queries using **FAISS**.
- **Question Answering**: Provide accurate responses based on the retrieved document chunks using **LangChain** and **ChatGroq**.

---

## **Setup**

### **Prerequisites**
Make sure you have the following software installed:
- **Python 3.8+**
- **Streamlit**
- **LangChain**
- **Hugging Face Transformers**
- **FAISS**
- **dotenv**

### **Deployment Instructions (Docker)**
You can also containerize this application using Docker for easier deployment.

**Docker Setup**
Build the Docker Image:

bash
docker build -t communico-gpt .

**Run the Docker Container**:

bash
docker run -p 8501:8501 communico-gpt
