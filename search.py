import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os

# --- Load environment variables (Groq API key) ---
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Load saved index and data ---
print("Loading index and data...")
index = faiss.read_index('product_index.faiss')
df = pd.read_pickle('products.pkl')

# --- Load embedding model (same one used to build the index) ---
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')

def search_products(query, top_k=5):
    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    results = df.iloc[indices[0]]
    return results

def ask_llm(query, results):
    # Build context from retrieved products
    context = ""
    for _, row in results.iterrows():
        context += f"- {row['product_name']} | Category: {row['main_category']} | Brand: {row['brand']} | Price: Rs {row['discounted_price']} | {row['description'][:200]}\n"

    prompt = f"""You are a helpful shopping assistant for an e-commerce site.
A user asked: "{query}"

Here are the most relevant products found in the catalog:
{context}

Based ONLY on these products, give a helpful, concise recommendation. Mention specific product names and prices. If none of these products truly fit the query, say so honestly."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("\n=== AI Shopping Assistant ===")
    print("Type 'quit' to exit\n")

    while True:
        query = input("You: ")
        if query.lower() == 'quit':
            break

        results = search_products(query, top_k=5)
        answer = ask_llm(query, results)
        print(f"\nAssistant: {answer}\n")