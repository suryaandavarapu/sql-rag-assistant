#  SuperStore AI Assistant
### Natural Language Interface over Sales Data and Business Policies

A hybrid **SQL + RAG** AI system that allows users to query a retail 
sales database and business policy documents using plain English. 
No SQL knowledge required.

---

##  Architecture

User Question
↓
Router (LLM classifies intent)
↓ ↓
SQL Agent RAG Agent
↓ ↓
SQLite DB FAISS Vector DB
↓ ↓
Results PDF Chunks
↓ ↓
Plain English Answer
↓
Flask API → HTML/CSS/JS UI


---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API (Qwen 27B) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Vector Store | FAISS |
| Database | SQLite |
| Orchestration | LangChain |
| Backend | Flask |
| Frontend | HTML / CSS / JS |

---

##  Features

- Natural language to SQL conversion
- PDF document Q&A using RAG pipeline
- Intelligent router — SQL, RAG, or BOTH
- Auto generated data tables with explanations
- Generated SQL visible to user
- Retrieved policy context visible to user
- Clean custom web interface

---

##  How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/suryaandavarapu/sql-rag-assistant.git
cd sql-rag-assistant
```

**2. Create virtual environment**
```bash
python -m venv sql_rag_env
sql_rag_env\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add API key**

Create a `.env` file:

GROQ_API_KEY=your_groq_api_key_here


**5. Setup database**
```bash
python db_setup.py
```

**6. Build RAG index**
```bash
python rag_pipeline.py
```

**7. Run the app**
```bash
python app.py
```

**8. Open browser**

http://localhost:5000


---

## 📁 Project Structure

## 📁 Project Structure

sql_rag_project/
├── data/
│ ├── superstore.csv
│ ├── superstore.db
│ ├── report.pdf
│ └── faiss_index/
├── static/
│ └── index.html
├── app.py
├── router.py
├── sql_agent.py
├── rag_agent.py
├── rag_pipeline.py
├── db_setup.py
├── .env
└── requirements.txt


---

## 🎯 Sample Questions

**SQL — Database Questions**
- Which region has the highest total profit?
- Show top 5 loss making orders
- What is total sales by category?

**RAG — Policy Questions**
- What is the discount policy for furniture?
- What is the shipping policy for corporate customers?
- Which region is flagged for profit losses?

**BOTH — Combined Questions**
- Why is Central region losing money compared to company policy?
- Compare actual discount rates with policy limits