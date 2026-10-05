import os
import sqlite3
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Database schema — tells LLM what columns exist
SCHEMA = """
Table: orders
Columns:
- order_id: unique order identifier
- order_date: date of order
- ship_mode: shipping method (First Class, Second Class, Standard Class)
- customer_name: name of customer
- segment: customer segment (Consumer, Corporate, Home Office)
- region: sales region (West, East, Central, South)
- category: product category (Furniture, Office Supplies, Technology)
- sub_category: product sub category
- product_name: name of product
- sales: revenue from order (float)
- quantity: number of items ordered (int)
- discount: discount applied (float, 0 to 1)
- profit: profit from order (float, can be negative)
"""

def generate_sql(question):
    prompt = f"""
You are a SQL expert working with SQLite database.

Database schema:
{SCHEMA}

Generate a SQL query to answer this question:
{question}

Rules:
- Return only raw SQL query
- No markdown, no backticks, no explanation
- Use ROUND() for decimal numbers
- Always include ORDER BY for ranking questions
- Use LIMIT 5 for top/bottom questions unless specified
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a SQL expert. Return only raw SQL queries. No markdown, no backticks, no explanation."},
            {"role": "user", "content": prompt}
        ]
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def execute_sql(sql):
    conn = sqlite3.connect("data/superstore.db")
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return columns, rows
    except Exception as e:
        conn.close()
        return None, str(e)

def explain_results(question, sql, columns, rows):
    prompt = f"""
You are a data analyst. A user asked this question:
"{question}"

The SQL query used was:
{sql}

The results are:
Columns: {columns}
Data: {rows}

Give a clear, concise answer in 2-3 sentences explaining what the data shows.
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful data analyst. Give clear concise answers."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def get_sql_answer(question):
    print(f"\n❓ Question: {question}")

    # Step 1 — Generate SQL
    sql = generate_sql(question)
    print(f"\n📝 Generated SQL:\n{sql}")

    # Step 2 — Execute SQL
    columns, rows = execute_sql(sql)

    if columns is None:
        print(f"❌ SQL Error: {rows}")
        return None, None, None

    print(f"\n📊 Raw Results:")
    print(f"Columns: {columns}")
    for row in rows:
        print(row)

    # Step 3 — Explain results
    explanation = explain_results(question, sql, columns, rows)
    print(f"\n💡 Explanation:\n{explanation}")

    return sql, rows, explanation

# Test the SQL agent
if __name__ == "__main__":
    print("🧪 Testing SQL Agent")
    print("-" * 50)

    questions = [
        "Which region has the highest total profit?",
        "Show me top 5 loss making orders",
        "What is total sales by category?",
    ]

    for question in questions:
        get_sql_answer(question)
        print("\n" + "=" * 60)

    print("\n✅ Phase 6 Complete!")