import pandas as pd
import sqlite3

# 1. Load CSV
df = pd.read_csv("data/superstore.csv", encoding="latin1")
print(" CSV loaded:", df.shape)

# 2. Clean column names
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("-", "_"))

print("\n Columns after cleaning:")
for col in df.columns:
    print(" -", col)

# 3. Connect to SQLite and save
conn = sqlite3.connect("data/superstore.db")
df.to_sql("orders", conn, if_exists="replace", index=False)
print("\n Database created: data/superstore.db")

# 4. Verify
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM orders")
print(" Total rows in DB:", cursor.fetchone()[0])

conn.close()
print("\n Phase 2 Complete!")