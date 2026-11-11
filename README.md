# Communico GPT

A document question-answering app: load your own PDFs, ask questions in plain
English, and get answers grounded in the documents, with the source passages
shown alongside each answer. Built with a retrieval-augmented generation (RAG)
pipeline using LangChain, FAISS, Hugging Face embeddings and Groq.

## Tech stack

| Layer       | Choice                                                     |
|-------------|------------------------------------------------------------|
| UI          | Streamlit                                                  |
| Orchestration | LangChain (retrieval chain + "stuff documents" chain)    |
| Embeddings  | Hugging Face `sentence-transformers/all-MiniLM-L6-v2` (runs locally) |
| Vector store | FAISS (in memory)                                         |
| LLM         | Groq via `langchain-groq`                                  |
| Packaging   | Docker                                                     |

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
 Question ──► retrieve similar chunks ──► Groq LLM answers from that context
                                              │
                                              ▼
                              Answer + the source chunks it used
```

1. **Indexing:** clicking **Documents Embedding** loads every PDF in
   `Communication_Books/`, splits the pages into overlapping chunks, embeds them
   and builds a FAISS index.
2. **Retrieval:** each question is embedded and matched against the index to
   find the most relevant chunks.
3. **Answering:** the chunks are passed to the LLM with a prompt that tells it to
   answer only from the provided context. The app shows the answer, the response
   time and the retrieved passages, so you can check where the answer came from.

## Run it locally

1. Get a free Groq API key: https://console.groq.com/keys
2. Clone the repo and install dependencies:
   ```
   git clone https://github.com/rushabhrn/communico-gpt.git
   cd communico-gpt
   pip install -r requirements.txt
   ```
3. Add your own PDFs to a folder named `Communication_Books/` in the project root.
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

## Known limitations

- Only the first 50 pages loaded are indexed, to keep embedding time short.
- The FAISS index lives in memory and is rebuilt each session; it isn't saved to disk.
- Answers come from a single retrieval step with no reranking or citations by page number.

## What I'd build next

- Persist the FAISS index so documents are embedded once, not every session.
- Show page-level citations for each answer.
- Add a small evaluation set of questions with known answers to measure retrieval quality.
