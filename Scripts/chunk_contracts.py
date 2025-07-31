from backend.services.extractor import extract_text_from_pdf, chunk_text, save_chunks_to_jsonl
from backend.services.rag_engine import embedd_doc, upsert_chunks
from dotenv import load_dotenv
import os
import cohere
import json
load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')

def load_embedding_model(api_key):
    co = cohere.ClientV2(api_key = COHERE_API_KEY)
    return co

folder_path = 'Data/raw'
docs_ls = os.listdir(folder_path)

for doc in docs_ls:
    doc_path = os.path.join(folder_path, doc)
    pdf_text, pdf_text_joined = extract_text_from_pdf(doc_path)
    chunk_data = chunk_text(pdf_text_joined)
    chunk_jsonl = save_chunks_to_jsonl(chunk_data)
    #print(len(chunk_jsonl))

    embedded_doc = embedd_doc(chunk_jsonl=chunk_jsonl)

    chunk_jsonl_copy = []
    for idx, chunk_json in enumerate(chunk_jsonl):
        chunk_json["vector"] = embedded_doc[idx]
        chunk_jsonl_copy.append(chunk_json)
    #print("Embeddings:", len(embedded_doc))
    upsert_chunks(chunk_jsonl=chunk_jsonl, embeddings=embedded_doc)

    out_dir = 'Data/processed'
    output_path = os.path.join(out_dir, f"{doc}_embeddings.jsonl")
    with open(output_path, "w", encoding="utf-8") as f:
        for item in chunk_jsonl_copy:
            f.write(json.dumps(item)+"\n")

    

