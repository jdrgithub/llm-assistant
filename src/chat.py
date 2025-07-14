from langchain.chat_models import ChatOllama
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA

CHROMA_PATH = "./data/chroma"

def main():
    print("Loading model and vector store...")
    llm = ChatOllama(model="mistral")
    embeddings = OllamaEmbeddings(model="mistral")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    print("Assistant ready. Ask a question (Ctrl+C to quit):")
    while True:
        try:
            query = input("\nYou: ")
            result = qa_chain(query)
            print("\nAnswer:\n", result["result"])
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()


