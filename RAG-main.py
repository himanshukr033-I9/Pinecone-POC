import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
import time
import openai
import json
import markdown
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("PINECONE_API_KEY")
# ------------- Configuration -------------
# Set your API keys and environment variables (ensure these are set in your environment)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Names for your three indexes
INDEX_NAMES = {
    "structured": "structured-markdown",
    "unstructured": "unstructured-markdown",
    "html": "scraped-html"
}

# The embedding dimension for OpenAI's text-embedding-ada-002 model is 1536
EMBEDDING_DIM = 1536

# Initialize Pinecone
pc = Pinecone(api_key=api_key)

# ------------- Helper Functions -------------

def create_index(index_name: str, dimension: int):
    """Create a Pinecone index if it doesn't exist already."""
    if index_name not in pc.list_indexes():
        print(f"Creating index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ),
            tags={
                "environment": "development"
            }
        )
        pc.create_index(index_name, dimension=dimension)
    else:
        print(f"Index '{index_name}' already exists.")
    return pc.Index(index_name)

def load_file(file_path: str) -> str:
    """Load the entire contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Splits text into chunks of approximately `chunk_size` words with optional `overlap`.
    Adjust the parameters based on your needs.
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
    """
    Get embedding for a given text using OpenAI embeddings.
    (Make sure your OpenAI API key is set.)
    """
    response = openai.Embedding.create(input=[text], model=model)
    embedding = response['data'][0]['embedding']
    return embedding

def index_document(index, doc_id: str, text: str):
    """
    Chunk the document, embed each chunk, and upsert the resulting vectors to the Pinecone index.
    Each vector is tagged with metadata containing the original text chunk.
    """
    chunks = chunk_text(text)
    vectors = []
    for i, chunk in enumerate(chunks):
        vector_id = f"{doc_id}_{i}"
        embedding = get_embedding(chunk)
        vectors.append((vector_id, embedding, {"text": chunk}))
    # Upsert vectors in batches (if needed, you can batch these up for large documents)
    index.upsert(vectors=vectors)
    print(f"Upserted {len(vectors)} vectors to index '{index.name}'.")

def query_index(index, query_embedding: list, top_k: int = 5) -> list:
    """
    Query a single Pinecone index using the provided query embedding.
    Returns a list of retrieved text chunks.
    """
    result = index.query(queries=[query_embedding], top_k=top_k, include_metadata=True)
    matches = result['results'][0]['matches']
    return [match['metadata']['text'] for match in matches]

def query_all_indexes(query: str, top_k: int = 5) -> list:
    """
    For a given query, embed it and query all three indexes.
    Returns combined retrieved chunks.
    """
    query_embedding = get_embedding(query)
    retrieved_chunks = []
    for name, idx in indexes.items():
        print(f"Querying index: {name}")
        chunks = query_index(idx, query_embedding, top_k=top_k)
        retrieved_chunks.extend(chunks)
    return retrieved_chunks

def generate_answer(query: str) -> str:
    """
    Retrieve relevant chunks from all indexes, combine them into context,
    and prompt an LLM (using OpenAI ChatCompletion) to generate an answer.
    """
    retrieved_chunks = query_all_indexes(query)
    context = "\n\n".join(retrieved_chunks)
    prompt = f"Using the following context, answer the question: '{query}'\n\nContext:\n{context}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response['choices'][0]['message']['content']

# ------------- Setup: Create Indexes and Ingest Data -------------

# Create separate indexes for each dataset
indexes = {}
for key, index_name in INDEX_NAMES.items():
    indexes[key] = create_index(index_name, EMBEDDING_DIM)

# Load your datasets (update the file paths as necessary)
structured_data = load_file("structured.md")      # e.g., structured markdown
unstructured_data = load_file("unstructured.md")  # e.g., unstructured markdown
html_data = load_file("scraped.html")               # e.g., scraped HTML content

# Upsert the documents into their respective indexes
index_document(indexes["structured"], "structured", structured_data)
index_document(indexes["unstructured"], "unstructured", unstructured_data)
index_document(indexes["html"], "html", html_data)

# ------------- Example: Query and Generate Answer -------------

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    answer = generate_answer(user_query)
    print("\nGenerated Answer:\n", answer)
