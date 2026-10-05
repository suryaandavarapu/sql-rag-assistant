import pandas as pd
import os
from dotenv import load_dotenv

# test pandas
df = pd.read_csv("data/superstore.csv", encoding="latin1")
print("✅ CSV loaded:", df.shape)

# test dotenv
load_dotenv(override=True)
key = os.getenv("GROQ_API_KEY")
print("Raw key value:", key)

if key:
    print("✅ API key loaded:", key[:6], "...")
else:
    print("❌ API key is None — .env not loading correctly")