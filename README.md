# 🏦 AskRBI — Chat with India's Central Bank Report

A RAG-powered chatbot that lets you ask questions about the RBI Annual Report 2024-25 in plain English. Every answer is grounded in the actual document — no hallucinations, no guessing.

**[🚀 Live Demo](https://askrbi-chat-with-india-s-central-bank-report-krmkwurjazrq5fkav.streamlit.app/)**

---

## What is RAG?

Retrieval-Augmented Generation (RAG) grounds LLM responses in a specific document, preventing hallucination by forcing the model to answer only from retrieved context.

Instead of asking Llama 3.1 *"What was India's GDP growth?"* from memory, the pipeline first searches the actual RBI report, retrieves the relevant passage, and sends it to the LLM along with the question.

```
User Question
     ↓
[Embedding Model] → converts question to vector
     ↓
[FAISS Vector Search] → finds top-k similar chunks from RBI PDF
     ↓
[Context + Question] → sent to Llama 3.1 via Groq API
     ↓
Grounded Answer + Source Passages
```

---

## Features

- **Ask anything** about the RBI Annual Report 2024-25 in plain English
- **Source passages shown** — every answer displays the exact chunks it was derived from
- **No hallucinations** — model is instructed to only use retrieved context
- **Fast responses** via Groq's high-speed inference API
- **Fully deployed** — no setup needed, runs in the browser

---

## Tech Stack

| Component | Tool |
|-----------|------|
| PDF Parsing | PyMuPDF (`fitz`) |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| LLM | Llama 3.1 8B via Groq API |
| LLM Framework | LangChain |
| UI | Streamlit |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
askrbi-chatbot/
│
├── app.py              # Streamlit UI
├── ingest.py           # Load + chunk + embed PDF → FAISS
├── retriever.py        # Query FAISS, fetch relevant chunks
├── chain.py            # Connect retriever + LLM into pipeline
├── requirements.txt
├── README.md
│
├── data/
│   └── rbi_annual_report.pdf    # Not pushed to GitHub
│
└── vectorstore/
    └── rbi_index/               # FAISS index files
        ├── index.faiss
        └── index.pkl
```

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/simrxn56/AskRBI-Chat-with-India-s-Central-Bank-Report.git
cd AskRBI-Chat-with-India-s-Central-Bank-Report
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Groq API key**

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_key_here
```
Get a free API key at [console.groq.com](https://console.groq.com)

**5. Add the RBI PDF**

Download the RBI Annual Report 2024-25 from [rbi.org.in](https://rbi.org.in) and place it at:
```
data/rbi_annual_report.pdf
```

**6. Build the vector store**
```bash
python ingest.py
```

**7. Run the app**
```bash
streamlit run app.py
```

---

## How It Works

### Step 1 — Chunking
The RBI Annual Report is split into overlapping chunks of 500 words with 50-word overlap. Overlap ensures no information is lost at chunk boundaries.

### Step 2 — Embeddings
Each chunk is converted to a 384-dimensional vector using `all-MiniLM-L6-v2`. Two semantically similar passages will have vectors close together in this space — enabling meaning-based search rather than keyword matching.

### Step 3 — FAISS Vector Store
All chunk vectors are stored in a FAISS index. When a question is asked, FAISS finds the top-4 most semantically similar chunks in milliseconds.

### Step 4 — Grounded Generation
The retrieved chunks + the user's question are sent to Llama 3.1 8B with a strict prompt instructing it to answer only from the provided context. Source passages are returned alongside the answer for transparency.

---

## Sample Questions

- What was India's GDP growth rate in 2024-25?
- What is RBI's inflation target?
- How did the rupee perform in 2024?
- What are the key risks to the Indian economy?
- What measures did RBI take to control inflation?

---

## Limitations

- Answers are limited to content covered in the RBI Annual Report 2024-25
- Very specific numerical questions may be missed if they fall at chunk boundaries
- Scanned/image-based PDFs would require OCR preprocessing

---

## Author

**Simranjit Singh**  
BCA Student | Aspiring Data Scientist  
[GitHub](https://github.com/simrxn56) · [LinkedIn](https://linkedin.com/in/simrxn56)
