from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
from models.base_llm import get_llm

from backend.services.rag_engine import retrieve_top_k

load_dotenv()

QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')



def run_audit(query, chunks_top_k):
    system_message = f""" Use the following pieces of context to answer the users question. If the context does not answe the question return dont make up answers. 
    question : {query}"
    contxt = {chunks_top_k}
"""
    
    client = get_llm()
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": system_message,
        }
    ],
    model="llama-3.3-70b-versatile",
    stream=False,
    )
    return chat_completion.choices[0].message.content

# query = 'what does customers firm service gas mean'
# result = retrieve_top_k(query)

# resp = run_audit(query, result)

# print(resp)