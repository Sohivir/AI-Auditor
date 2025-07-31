import cohere
from qdrant_client.models import PointStruct
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
load_dotenv()

QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

def load_embedding_model(api_key):
    co = cohere.ClientV2(api_key = COHERE_API_KEY)
    return co

def embedd_doc(chunk_jsonl):
    
    text_inputs = [
        {
            "content": [{"type": "text", "text": chunk_json["chunk"]}]
        }
        for chunk_json in chunk_jsonl
    ]
    
    cohere_client = load_embedding_model(api_key=COHERE_API_KEY)

    response = cohere_client.embed(
        inputs=text_inputs,
        model="embed-v4.0",
        input_type="classification",
        embedding_types=["float"],
    )
    return response.embeddings.float

def embed_query(query):
    cohere_query_client = load_embedding_model(api_key=COHERE_API_KEY)
    content = {
        "type": "text",
        "text": query
    }
    text_inputs = [
        {
            "content": content
        },
    ]
    response = cohere_query_client.embed(
        inputs = text_inputs,
        model = "embed-v4.0",
        input_type = "classification",
        embedding_types = ["float"],
    )

    query_vec = response.embeddings.float

    return query_vec

def upsert_chunks(chunk_jsonl, embeddings):
    client = QdrantClient(api_key=QDRANT_API_KEY, 
                          url="https://3fa6dcd0-abb6-4990-9086-b629688151ad.eu-central-1-0.aws.cloud.qdrant.io")
    points = []

    for idx, (chunk, vector) in enumerate(zip(chunk_jsonl, embeddings)):
        points.append(PointStruct(
            id=idx,
            vector=vector,
            payload={
                "page_no": chunk["page_no"],
                "chunk": chunk["chunk"]
            }
        ))

    client.upsert(
        collection_name='contracts_chunks',
        wait=True,
        points=points
    )

def retrieve_top_k(query, top_k=5):
    query_vec = embed_query(query)[0]
    client = QdrantClient(api_key=QDRANT_API_KEY,
                          url="https://3fa6dcd0-abb6-4990-9086-b629688151ad.eu-central-1-0.aws.cloud.qdrant.io")
    results = client.query_points(
        collection_name="contracts_chunks",
        query=query_vec,
        limit=top_k,
        with_payload=True
    ).points
    return results[0].payload['chunk']

query = 'what does customers firm service gas mean'

# result = retrieve_top_k(query)
# result = result[0].payload['chunk']  #result[0].payload contains 2 keys : chunk and page_no
# print(result)