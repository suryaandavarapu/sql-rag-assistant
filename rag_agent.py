import os
from groq import Groq
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load the vector store
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

def get_rag_answer(question, vectorstore):
    print(f"\n❓ Question: {question}")

    # Step 1 — Retrieve relevant chunks
    print("\n🔍 Retrieving relevant chunks...")
    results = vectorstore.similarity_search(question, k=3)

    context = "\n\n".join([doc.page_content for doc in results])
    print(f"\n📄 Retrieved Context:\n{context}")

    # Step 2 — Generate answer from context
    prompt = f"""
You are a helpful business analyst assistant.
Use the following context from the company policy document to answer the question.
If the answer is not in the context, say "This information is not available in the policy document."

Context:
{context}

Question: {question}

Give a clear and concise answer based only on the context provided.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful business analyst. Answer only from the provided context."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    print(f"\n💡 Answer:\n{answer}")
    return context, answer

# Test the RAG agent
if __name__ == "__main__":
    print("🧪 Testing RAG Agent")
    print("-" * 50)

    # Load vectorstore once
    print("Loading vector store...")
    vectorstore = load_vectorstore()
    print("✅ Vector store loaded")

    questions = [
        "What is the discount policy for furniture?",
        "What is the shipping policy for corporate customers?",
        "Which region is flagged for profit losses?",
    ]

    for question in questions:
        get_rag_answer(question, vectorstore)
        print("\n" + "=" * 60)

    print("\n✅ Phase 7 Complete!")