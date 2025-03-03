from pinecone import Pinecone
import time
from dotenv import load_dotenv
import os
import json
import markdown
import csv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone with the API key
pc = Pinecone(api_key=api_key)

# Define a single index name
index_name = "integrated-poc-index"

# Function to create an index if it doesn't exist
def create_index(index_name):
    existing_indexes_info = pc.list_indexes()
    existing_index_names = [index['name'] for index in existing_indexes_info]
    if index_name not in existing_index_names:
        pc.create_index_for_model(
            name=index_name,
            cloud="aws",
            region="us-east-1",
            embed={
                "model": "multilingual-e5-large",
                "field_map": {"text": "chunk_text"}
            }
        )
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

# Create the index
create_index(index_name)

# Function to read JSON data
def read_json_data(file_path):
    print("entered read json")
    with open(file_path, 'r', encoding='utf-8') as file:
        print("file read")
        return json.load(file)

# Function to read and convert Markdown data
def read_markdown_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return markdown.markdown(text)

# Function to flatten JSON data
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Function to upsert data into an index with batch processing
def upsert_data(index_name, namespace, records, batch_size=96):
    index = pc.Index(index_name)
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        index.upsert_records(namespace, batch)
        time.sleep(10)  # Optional: Add a small delay between batches
    print(f"Data upserted into '{index_name}' under namespace '{namespace}' successfully.")

def chunk_json_data(json_data):
    # Example: Chunk by top-level keys or specific fields
    chunks = []
    for key, value in json_data.items():
        if isinstance(value, str):
            chunks.append((key, value))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                chunks.append((f"{key}_{i}", str(item)))
    return chunks

# Ingest JSON files with chunking
json_records = []
json_directory = './Data/JSON'
# for filename in os.listdir(json_directory):
#     if filename.endswith('.json'):
#         file_path = os.path.join(json_directory, filename)
#         json_data = read_json_data(file_path)
#         chunks = chunk_json_data(json_data)
#         for chunk_id, chunk_text in chunks:
#             json_records.append({
#                 "_id": f"{json_data.get('employer_id')}_{chunk_id}",
#                 "chunk_text": chunk_text,
#                 "category": json_data.get('organizationName'),
#             })

# upsert_data(index_name, "json-chunked-namespace", json_records)

# Ingest Markdown files
markdown_records = []
markdown_directory = './Data/New-Markdown'
for filename in os.listdir(markdown_directory):
    if filename.endswith('.md'):
        file_path = os.path.join(markdown_directory, filename)
        markdown_data = read_markdown_data(file_path)
        markdown_records.append({
            "_id": filename.split('.')[0],  # Use filename as ID
            "chunk_text": markdown_data,
            "category": "markdown"
        })

upsert_data(index_name, "new-markdown-namespace", markdown_records)


# Function to query the index
def query_index(index_name, namespace, query):
    index = pc.Index(index_name)
    response = index.search_records(
        namespace=namespace,
        query={
            "inputs":{"text":query},
            "top_k":3
        },
        # include_values=False,
        # include_metadata=True,
    )
    return response

# Load queries from query_bank.json
query_bank = read_json_data('Data/Query Bank/query_bank.json')
queries = query_bank.get("queries", [])

# Prepare CSV file for results
with open('query_results_new_markdown.csv', 'w', newline='') as csvfile:
    fieldnames = ['query', 'markdown_result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    # Run each query for both JSON and Markdown
    for query in queries:
        # json_result = query_index(index_name, "json-chunked-namespace", query)
        markdown_result = query_index(index_name, "new-markdown-namespace", query)
        

        # Write results to CSV
        writer.writerow({
            'query': query,
            # 'json_result': json_result,
            'markdown_result': markdown_result
        })
