from fastapi import FastAPI
from pydantic import BaseModel
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(title="AI Shopping Assistant API")

print("Loading index and data...")
index = faiss.read_index('product_index.faiss')
df = pd.read_pickle('products.pkl')
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
print("Ready.")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    history: list[dict] = []

class ProductResult(BaseModel):
    product_name: str
    main_category: str
    brand: str
    discounted_price: float

class QueryResponse(BaseModel):
    answer: str
    products: list[ProductResult]

def extract_price_limit(query):
    """Extract a max price constraint from natural language."""
    patterns = [
        r'under\s*(?:rs\.?|₹)?\s*(\d+)',
        r'below\s*(?:rs\.?|₹)?\s*(\d+)',
        r'less than\s*(?:rs\.?|₹)?\s*(\d+)',
        r'(?:rs\.?|₹)\s*(\d+)\s*or less',
    ]
    for pattern in patterns:
        match = re.search(pattern, query.lower())
        if match:
            return float(match.group(1))
    return None

def search_products(query, top_k=5):
    price_limit = extract_price_limit(query)
    fetch_k = top_k * 4 if price_limit else top_k

    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    distances, indices = index.search(query_embedding, fetch_k)
    results = df.iloc[indices[0]].copy()

    if price_limit:
        results = results[results['discounted_price'] <= price_limit]

    return results.head(top_k)

def ask_llm(query, results, history=[]):
    context = ""
    for _, row in results.iterrows():
        context += f"- {row['product_name']} | Category: {row['main_category']} | Brand: {row['brand']} | Price: Rs {row['discounted_price']} | {row['description'][:200]}\n"

    system_msg = """You are a helpful shopping assistant for an e-commerce site.
Use the retrieved products below to answer. If the user is following up on a previous question 
(e.g. "show cheaper ones", "what about in blue"), use the conversation history to understand context.
Only recommend from the retrieved products. If none fit, say so honestly."""

    messages = [{"role": "system", "content": system_msg}]
    messages.extend(history[-6:])
    messages.append({
        "role": "user",
        "content": f'User question: "{query}"\n\nRetrieved products:\n{context}'
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

@app.get("/")
def root():
    return {"status": "AI Shopping Assistant API is running"}

@app.post("/search", response_model=QueryResponse)
def search(request: QueryRequest):
    results = search_products(request.query, top_k=request.top_k)
    answer = ask_llm(request.query, results, history=request.history)

    products = [
        ProductResult(
            product_name=row['product_name'],
            main_category=row['main_category'],
            brand=row['brand'],
            discounted_price=float(row['discounted_price']) if pd.notna(row['discounted_price']) else 0.0
        )
        for _, row in results.iterrows()
    ]

    return QueryResponse(answer=answer, products=products)