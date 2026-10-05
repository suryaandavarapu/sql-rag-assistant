import os
from groq import Groq
from dotenv import load_dotenv
import sqlite3

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test 1 — Basic response
print("🧪 Test 1 — Basic LLM Response")
print("-" * 50)

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a helpful data analyst assistant."},
        {"role": "user", "content": "What is profit margin and why does it matter in retail?"}
    ]
)
print(response.choices[0].message.content)

# Test 2 — SQL Generation
print("\n🧪 Test 2 — SQL Generation from Plain English")
print("-" * 50)

schema = """
Table: orders
Columns: order_id, order_date, ship_mode, customer_name, segment, 
         region, category, sub_category, product_name, 
         sales, quantity, discount, profit
"""

question = "Which region has the highest total profit?"

prompt = f"""
You are a SQL expert. Given this database schema:
{schema}

Generate a SQL query to answer this question:
{question}

Return only the raw SQL query, no markdown, no backticks, no explanation.
"""

response2 = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a SQL expert. Return only raw SQL, no markdown, no backticks, no explanation."},
        {"role": "user", "content": prompt}
    ]
)

sql = response2.choices[0].message.content.strip()
sql = sql.replace("```sql", "").replace("```", "").strip()

print("Question:", question)
print("\nGenerated SQL:")
print(sql)

# Test 3 — Execute the generated SQL
print("\n🧪 Test 3 — Execute Generated SQL on Real Database")
print("-" * 50)

conn = sqlite3.connect("data/superstore.db")
cursor = conn.cursor()

try:
    cursor.execute(sql)
    rows = cursor.fetchall()
    print("✅ Query executed successfully!")
    print("Result:")
    for row in rows:
        print(row)
except Exception as e:
    print("❌ Error:", e)

conn.close()
print("\n✅ Phase 3 Complete!")