Shop Assistant — RAG-Powered AI Shopping Assistant

A conversational shopping assistant that retrieves real products from a catalog and answers naturally, grounded in retrieval rather than hallucinated knowledge. Built for the Flipkart GRiD 8.0 — AI Engineering track.

What it does

Ask it things like:


running shoes under 2000
show me cheaper ones (it remembers context from your last message)
kids toys for 5 year old


It retrieves the most relevant products from a real e-commerce catalog using semantic search, applies price filtering when you mention a budget, and uses an LLM to generate a grounded, honest recommendation — including telling you when nothing in the catalog actually fits, instead of making something up.

Architecture

User query
   ↓
Price constraint extraction (regex)
   ↓
Query embedding (sentence-transformers, GPU-accelerated)
   ↓
FAISS similarity search → top-K candidate products
   ↓
Price filtering on candidates
   ↓
LLM (Groq / Llama 3.1) generates grounded answer using retrieved context + conversation history
   ↓
Streamlit chat UI

This is a RAG (Retrieval-Augmented Generation) pipeline: the LLM never relies on its own training data for product facts — it only ever answers from products actually retrieved from the catalog, which keeps it grounded and prevents hallucinated product names or prices.

Tech stack

ComponentToolEmbeddingssentence-transformers (all-MiniLM-L6-v2), GPU-accelerated via CUDAVector searchFAISSLLMGroq API (Llama 3.1 8B)BackendFastAPIFrontendStreamlitDataFlipkart Products dataset (Kaggle)

Features


Semantic retrieval — understands intent, not just keyword matches
Price-aware filtering — "under 2000" actually filters by price, not just hopes semantics align with budget
Conversational memory — follow-up questions like "show cheaper ones" work without restating the original query
Grounded answers — the LLM is instructed to only recommend from retrieved products, and explicitly says so when nothing fits, rather than inventing results
GPU-accelerated embeddings for fast retrieval


Setup

1. Clone the repo

bashgit clone https://github.com/sgsubhiksha/ai-shopping-assistant.git
cd ai-shopping-assistant

2. Create a virtual environment

bashpython -m venv venv
venv\Scripts\activate      # Windows

3. Install dependencies

bashpip install -r requirements.txt

4. Get the dataset

Download the Flipkart Products dataset from Kaggle, unzip it, and place the CSV inside a folder named archive/ in the project root:

ai-shopping-assistant/
└── archive/
    └── flipkart_com-ecommerce_sample.csv

5. Get a Groq API key

Sign up free at console.groq.com → API Keys → Create API Key.

Create a .env file in the project root:

GROQ_API_KEY=your_key_here

6. Build the FAISS index

bashpython build_index.py

This generates product_index.faiss and products.pkl.

7. Run the backend

bashuvicorn api:app --reload

8. Run the frontend (in a separate terminal)

bashstreamlit run app.py

Open http://localhost:8501 in your browser.

Example interaction


You: kids toys for 5 year old
Assistant: Recommends age-appropriate toys from the catalog, explicitly excluding ones outside the right age range.




You: gaming console PS5
Assistant: Correctly states no PS5 exists in the catalog, rather than inventing one — and instead offers genuinely related gaming accessories that do exist.



Future improvements


Hybrid search (keyword + semantic re-ranking)
Evaluation harness for hallucination/groundedness scoring
Product images in the UI
Multi-category structured filters (brand, rating, category) alongside free-text price parsing