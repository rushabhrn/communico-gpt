# Communico GPT

A document question-answering app: load your own PDFs, ask questions in plain
English, and get answers grounded in the documents, with the source passages
(file and page) shown alongside each answer. Built as a retrieval-augmented
generation (RAG) pipeline using LangChain components, FAISS, Hugging Face
embeddings and Groq.

## Tech stack

| Layer        | Choice                                                               |
|--------------|----------------------------------------------------------------------|
| UI           | Streamlit                                                            |
| Loading      | LangChain `PyPDFDirectoryLoader` + `RecursiveCharacterTextSplitter`  |
| Embeddings   | Hugging Face `sentence-transformers/all-MiniLM-L6-v2` (runs locally) |
| Vector store | FAISS (in memory)                                                    |
| LLM          | Groq (`llama-3.1-8b-instant` by default, configurable via `GROQ_MODEL`) |
| Packaging    | Docker                                                               |

## How it works

```
 PDFs in ./Communication_Books
      │  PyPDFDirectoryLoader
      ▼
 Split into 1,000-character chunks (200 overlap)
      │  all-MiniLM-L6-v2 embeddings
      ▼
 FAISS vector index (kept in the Streamlit session)
      │
 Question ──► top 4 similar chunks ──► Groq LLM answers from that context only
                                              │
                                              ▼
                       Answer + response time + source passages (file, page)
```

1. **Indexing:** clicking **Documents Embedding** loads the PDFs, splits the
   pages into overlapping chunks, embeds them and builds a FAISS index. The
   embedding model is cached, so it loads once per server.
2. **Retrieval:** each question is embedded and matched against the index to
   find the 4 most similar chunks.
3. **Answering:** the chunks are passed to the LLM with a prompt that tells it to
   answer only from the context and to say when it doesn't know. The retrieval
   step is written out explicitly rather than hidden inside a prebuilt chain.
4. **Transparency:** the app shows the response time and the exact passages used,
   with their file name and page number.

## Run it locally

1. Get a free Groq API key: https://console.groq.com/keys
2. Clone the repo and install dependencies:
   ```
   git clone https://github.com/rushabhrn/communico-gpt.git
   cd communico-gpt
   pip install -r requirements.txt
   ```
3. Create a folder named `Communication_Books/` in the project root and add your
   own PDFs. It's ignored by Git, so documents are never committed.
4. Create a `.env` file:
   ```
   GROQ_API_KEY=your_groq_key
   ```
5. Start the app and open http://localhost:8501:
   ```
   streamlit run app.py
   ```
6. Click **Documents Embedding**, then type a question.

### With Docker

```
docker build -t communico-gpt .
docker run -p 8501:8501 --env-file .env -v "$(pwd)/Communication_Books:/app/Communication_Books" communico-gpt
```

On Windows PowerShell, use `-v "${PWD}/Communication_Books:/app/Communication_Books"`.

### Configuration

| Variable       | Required | Default                 | Purpose                    |
|----------------|----------|-------------------------|----------------------------|
| `GROQ_API_KEY` | Yes      | —                       | Groq API key               |
| `GROQ_MODEL`   | No       | `llama-3.1-8b-instant`  | Groq model used to answer  |
| `DOCS_DIR`     | No       | `./Communication_Books` | Folder of PDFs to index    |

## Known limitations

- Only the first 50 pages loaded are indexed, to keep embedding time short.
- The FAISS index lives in memory and is rebuilt each session; it isn't saved to disk.
- Retrieval is a single similarity search with no reranking.

## What I'd build next

- Persist the FAISS index so documents are embedded once, not every session.
- Rerank retrieved chunks before answering.
- Add a small evaluation set of questions with known answers to measure retrieval quality.
