import sqlite3

conn = sqlite3.connect("data/superstore.db")
cursor = conn.cursor()

queries = [
    ("Total Sales by Region",
     "SELECT region, ROUND(SUM(sales),2) as total_sales FROM orders GROUP BY region ORDER BY total_sales DESC"),

    ("Profit by Category",
     "SELECT category, ROUND(SUM(profit),2) as total_profit FROM orders GROUP BY category ORDER BY total_profit DESC"),

    ("Top 5 Loss Making Orders",
     "SELECT order_id, product_name, ROUND(sales,2) as sales, ROUND(profit,2) as profit FROM orders ORDER BY profit ASC LIMIT 5"),

    ("High Discount Orders above 40 percent",
     "SELECT order_id, product_name, discount, ROUND(profit,2) as profit FROM orders WHERE discount > 0.4 ORDER BY profit ASC LIMIT 5"),

    ("Sales by Segment",
     "SELECT segment, ROUND(SUM(sales),2) as total_sales, ROUND(SUM(profit),2) as total_profit FROM orders GROUP BY segment ORDER BY total_sales DESC"),
]

for title, query in queries:
    print(f"\n {title}")
    print("-" * 50)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()
print("\n Phase 2 Part 2 Complete!")