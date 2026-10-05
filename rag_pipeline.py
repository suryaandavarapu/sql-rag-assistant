from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
def build_rag_pipeline(pdf_path="data/report.pdf"):
    # Step 1 — Load PDF
    print("Step 1 — Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f" PDF loaded: {len(documents)} pages")

    # Step 2 — Split into chunks
    print("\nStep 2 — Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f" Total chunks created: {len(chunks)}")
    print("\nSample chunk:")
    print(chunks[0].page_content)

    # Step 3 — Create embeddings and store in FAISS
    print("\nStep 3 — Creating embeddings (this takes 1-2 mins first time)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("data/faiss_index")
    print(" Vector store saved: data/faiss_index")

    # Step 4 — Test retrieval
    print("\nStep 4 — Testing retrieval...")
    query = "What is the discount policy for furniture?"
    results = vectorstore.similarity_search(query, k=2)
    print(f"\nQuery: {query}")
    print("\nTop matching chunks:")
    for i, doc in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        print(doc.page_content)

    print("\n Phase 4 Complete!")
    return vectorstore

if __name__ == "__main__":
    build_rag_pipeline()