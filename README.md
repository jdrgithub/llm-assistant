# 🧠 Local AI Personal Assistant

This project is a local-first AI personal assistant powered by a local LLM (via [Ollama](https://ollama.com)), vector search (via [ChromaDB](https://www.trychroma.com/)), and retrieval-augmented generation (RAG) using [LangChain](https://www.langchain.com/).

You can ask natural language questions about your notes, documents, or exported ChatGPT conversations — all without sending your data to the cloud.

---

## 📦 Project Structure

```
llm-assistant/
├── .venv/               # Python virtual environment (not committed)
├── data/                # Vector store files (ChromaDB)
├── docs/                # Your personal text, pdf, or ChatGPT files
├── src/
│   ├── load_docs.py     # Indexes and chunks your documents
│   └── chat.py          # CLI chat interface (asks questions over your vector DB)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## ⚙️ Tech Stack Overview

| Component     | Description |
|---------------|-------------|
| **Ollama**    | Runs a quantized local LLM (like `mistral`) on your CPU or GPU. No cloud needed. |
| **LangChain** | Connects your local LLM, document retriever, and embeddings into a chat-like interface |
| **ChromaDB**  | A lightweight, local vector database that stores chunked embeddings of your documents |
| **RecursiveCharacterTextSplitter** | Breaks long files into 500-token overlapping chunks to improve retrieval accuracy |
| **ChatOllama**| LangChain wrapper that lets you use Ollama models in your app |
| **OllamaEmbeddings** | Embeds your documents and queries for vector search using the same model you use for answering |

---

## ✅ How It Works (End to End)

1. **You add files to `docs/`**
   - Supported formats: `.txt`, `.md`, `.pdf`, and `conversations.json` (ChatGPT export)
   - Files can have or lack extensions

2. **You run** `python src/load_docs.py`
   - Loads all files
   - Splits long ones into manageable chunks
   - Embeds them using Ollama (e.g., Mistral)
   - Saves vectors to `data/chroma/`

3. **You run** `python src/chat.py`
   - Loads the vector store
   - Accepts natural language questions
   - Finds relevant chunks
   - Uses the local LLM to synthesize an answer

---

## 🚀 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/llm-assistant.git
cd llm-assistant

# Set up Python environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama and pull a model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral  # or llama3, gemma, etc.

# Add your files to the docs/ folder
# Then index them:
python src/load_docs.py

# Now chat with your assistant:
python src/chat.py
```

---

## 🧠 Example Questions to Try

```text
What AWS services are mentioned in my notes?
Do any files contain lyrics?
Summarize my notes on Terraform.
List all TODOs mentioned across my documents.
What did I write about DNS failover in Route 53?
```

---

## 💡 Notes

- All embeddings and responses are computed locally
- No internet connection is required after installation
- This is a simple RAG system — not a full memory agent (yet)

---

## 📚 Future Ideas

- Add TODO tracking and persistent memory
- Add support for audio (Whisper) or speech (TTS)
- Serve via web UI (e.g., Chainlit)
- Make it agent-like (tools + function calling)

---

MIT Licensed. Built by [you] for local-first AI productivity.
