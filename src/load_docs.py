from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from pathlib import Path
import json
import os

DOCS_PATH = "./docs"
CHROMA_PATH = "./data/chroma"

def load_chatgpt_conversations(path):
    print(f"Parsing ChatGPT export: {path}")
    docs = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for conv in data.get("conversations", []):
            title = conv.get("title", "Untitled")
            messages = conv.get("mapping", {})

            for msg_id, msg in messages.items():
                content = msg.get("message", {}).get("content", {})
                text = None

                if content.get("content_type") == "text":
                    parts = content.get("parts", [])
                    if parts:
                        text = "\n".join(parts)

                if text:
                    docs.append(Document(
                        page_content=text,
                        metadata={
                            "source": str(path),
                            "conversation_title": title,
                            "message_id": msg_id
                        }
                    ))

    except Exception as e:
        print(f"Failed to parse {path}: {e}")
    return docs

def load_supported_files():
    docs = []
    for path in Path(DOCS_PATH).rglob("*"):
        try:
            suffix = path.suffix.lower()

            if suffix in [".txt", ".md"]:
                loader = TextLoader(str(path), encoding="utf-8")
                docs.extend(loader.load())

            elif suffix == ".pdf":
                loader = PyPDFLoader(str(path))
                docs.extend(loader.load())

            elif path.name == "conversations.json":
                docs.extend(load_chatgpt_conversations(path))

            else:
                print(f"Skipping unsupported file: {path}")
        except Exception as e:
            print(f"Error loading {path}: {e}")
    return docs

def main():
    print(f"Scanning '{DOCS_PATH}' for documents...")
    raw_docs = load_supported_files()
    print(f"Loaded {len(raw_docs)} documents.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    documents = splitter.split_documents(raw_docs)
    print(f"Split into {len(documents)} chunks.")

    embeddings = OllamaEmbeddings(model="mistral")

    print("Saving to Chroma vector store...")
    db = Chroma.from_documents(documents, embeddings, persist_directory=CHROMA_PATH)
    db.persist()
    print("Vector store saved at:", CHROMA_PATH)

if __name__ == "__main__":
    main()

