import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_query(query):
    prompt = f"""
You are a query classifier for a retail analytics system.
Given a user question, classify it as exactly one of these:

SQL - if the question asks about numbers, totals, comparisons, 
      rankings, filters, aggregations from sales data
      Examples: "Which region has highest profit?", 
                "Show top 5 loss making orders",
                "What is total sales by category?"

RAG - if the question asks about policies, rules, guidelines,
      strategy, shipping rules, discount rules, business context
      Examples: "What is the discount policy for furniture?",
                "What is the shipping policy for corporate customers?",
                "Which region is flagged for profit losses?"

BOTH - if the question needs both sales data AND policy context
       Examples: "Why is Central region losing money compared to policy?",
                 "Compare actual discount rates with the policy limits"

Question: {query}

Reply with only one word: SQL, RAG, or BOTH
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a query classifier. Reply with only one word: SQL, RAG, or BOTH."},
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content.strip()

    # clean up in case model adds extra text
    if "SQL" in result:
        return "SQL"
    elif "RAG" in result:
        return "RAG"
    elif "BOTH" in result:
        return "BOTH"
    else:
        return "SQL"  # default to SQL if unclear

# Test the router
if __name__ == "__main__":
    test_queries = [
        "Which region has the highest total profit?",
        "What is the discount policy for furniture?",
        "What is total sales by category?",
        "What is the shipping policy for corporate customers?",
        "Why is Central region losing money compared to company policy?",
        "Show me top 5 loss making orders",
        "Which segment is flagged for review in the policy document?",
    ]

    print("🧪 Testing Router")
    print("-" * 50)

    for query in test_queries:
        route = classify_query(query)
        print(f"Query: {query}")
        print(f"Route: {route}")
        print()

    print("✅ Phase 5 Complete!")