from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3
import warnings
warnings.filterwarnings("ignore")

from groq import Groq
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
load_dotenv()

app = Flask(__name__, static_folder="static")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SCHEMA = """
Table: orders
Columns:
- order_id, order_date, ship_mode, customer_name
- segment (Consumer, Corporate, Home Office)
- region (West, East, Central, South)
- category (Furniture, Office Supplies, Technology)
- sub_category, product_name
- sales (float), quantity (int)
- discount (float 0-1), profit (float)
"""

# ─── Load Vector Store once at startup ─────────────────
print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "data/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
print("✅ Vector store loaded")

# ─── Router ────────────────────────────────────────────
def classify_query(query):
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a query classifier. Reply with only one word: SQL, RAG, or BOTH."},
            {"role": "user", "content": f"""
Classify this question:
- SQL: numbers, totals, rankings, filters from sales data
- RAG: policies, rules, guidelines, business strategy
- BOTH: needs both data and policy context

Question: {query}
Reply with only: SQL, RAG, or BOTH"""}
        ]
    )
    result = response.choices[0].message.content.strip()
    if "BOTH" in result: return "BOTH"
    elif "RAG" in result: return "RAG"
    else: return "SQL"

# ─── SQL Agent ─────────────────────────────────────────
def get_sql_answer(question):
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a SQL expert. Return only raw SQL. No markdown, no backticks."},
            {"role": "user", "content": f"Schema: {SCHEMA}\nQuestion: {question}\nReturn only raw SQL."}
        ]
    )
    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    conn = sqlite3.connect("data/superstore.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
    except Exception as e:
        conn.close()
        return {"error": str(e), "sql": sql}

    response2 = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a data analyst. Give clear concise answers in 2-3 sentences."},
            {"role": "user", "content": f"Question: {question}\nSQL: {sql}\nColumns: {columns}\nData: {rows}\nExplain what the data shows."}
        ]
    )
    explanation = response2.choices[0].message.content.strip()
    return {
        "sql": sql,
        "columns": columns,
        "rows": rows,
        "explanation": explanation
    }

# ─── RAG Agent ─────────────────────────────────────────
def get_rag_answer(question):
    results = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a business analyst. Answer only from the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return {
        "answer": response.choices[0].message.content.strip(),
        "context": context
    }

# ─── API Routes ────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        route = classify_query(question)
        result = {"route": route}

        if route == "SQL":
            result["sql_data"] = get_sql_answer(question)
        elif route == "RAG":
            result["rag_data"] = get_rag_answer(question)
        elif route == "BOTH":
            result["sql_data"] = get_sql_answer(question)
            result["rag_data"] = get_rag_answer(question)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500