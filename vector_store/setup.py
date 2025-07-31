from qdrant_client import QdrantClient
from qdrant_client.http import models as rest 
from qdrant_client.http.models import VectorParams, Distance

from dotenv import load_dotenv
import os

load_dotenv()

COLLECTION_NAME = "contracts_chunks"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url="https://3fa6dcd0-abb6-4990-9086-b629688151ad.eu-central-1-0.aws.cloud.qdrant.io", 
    api_key=QDRANT_API_KEY,
)

collection_name = "contracts_chunks"

if collection_name in [c.name for c in client.get_collections().collections]:
    client.delete_collection(collection_name=collection_name)
    print(f"🗑️ Deleted existing collection: {collection_name}")

client.create_collection(
    collection_name="contracts_chunks",  # This is the collection name
    vectors_config=VectorParams(
        size=1536,              # match your embedding model
        distance=Distance.COSINE
    )
)

#print(client.get_collections())
