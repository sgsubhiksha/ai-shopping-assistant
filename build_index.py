import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# --- Step 1: Load data ---
print("Loading CSV...")
df = pd.read_csv('archive/flipkart_com-ecommerce_sample.csv')

# --- Step 2: Clean data ---
df = df.dropna(subset=['product_name', 'description'])
df['brand'] = df['brand'].fillna('Unknown')
df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce')
df['discounted_price'] = pd.to_numeric(df['discounted_price'], errors='coerce')
df = df.dropna(subset=['retail_price'])
df = df.reset_index(drop=True)

print(f"Cleaned dataset: {len(df)} products")

# --- Step 3: Build a clean category column ---
# product_category_tree looks like: ["Furniture >> Living Room >> Sofas"]
def clean_category(cat_str):
    try:
        cat_str = cat_str.strip('["]')
        return cat_str.split(">>")[0].strip()
    except:
        return "Unknown"

df['main_category'] = df['product_category_tree'].apply(clean_category)

# --- Step 4: Combine fields into one text block per product (this is what gets embedded) ---
df['combined_text'] = (
    "Product: " + df['product_name'].astype(str) +
    ". Category: " + df['main_category'].astype(str) +
    ". Brand: " + df['brand'].astype(str) +
    ". Price: Rs " + df['discounted_price'].astype(str) +
    ". Description: " + df['description'].astype(str)
)

# --- Step 5: Generate embeddings on GPU ---
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')

print("Generating embeddings... (this may take a few minutes)")
embeddings = model.encode(
    df['combined_text'].tolist(),
    show_progress_bar=True,
    batch_size=64,
    convert_to_numpy=True
)

print(f"Embeddings shape: {embeddings.shape}")

# --- Step 6: Build FAISS index ---
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))

print(f"FAISS index built with {index.ntotal} vectors")

# --- Step 7: Save everything ---
faiss.write_index(index, 'product_index.faiss')
df.to_pickle('products.pkl')

print("Done! Saved 'product_index.faiss' and 'products.pkl'")