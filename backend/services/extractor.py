import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from  PIL import Image
import pytesseract 
from dotenv import load_dotenv
load_dotenv()
import os
import requests

OCR_SPACE_API_KEY = 'K85797547088957'

def extract_text_from_pdf(path):
    pdf_text = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            pdf_text.append(text)
    pdf_text_joined = [" ".join(pdf_text)]
    return pdf_text, pdf_text_joined

import io, requests, pdfplumber
from PIL import Image

def ocrspace_image(pil_img, api_key, lang="eng"):
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    files = {"file": ("page.png", buf, "image/png")}
    data = {"apikey": api_key, "language": lang, "isOverlayRequired": False, "OCREngine": 2}
    r = requests.post("https://api.ocr.space/parse/image", files=files, data=data, timeout=120)
    r.raise_for_status()
    j = r.json()
    if j.get("IsErroredOnProcessing"):
        raise RuntimeError(j.get("ErrorMessage") or j.get("ErrorDetails"))
    return j["ParsedResults"][0].get("ParsedText", "")

def extract_text_from_scanned_pdf(path, api_key, dpi=100, lang="eng"):
    texts = []
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[3]
        img = page.to_image(resolution=dpi).original.convert("L")
        texts.append(ocrspace_image(img, api_key, lang=lang))
        # for page in pdf.pages:
        #     img = page.to_image(resolution=dpi).original.convert("L")
        #     texts.append(ocrspace_image(img, api_key, lang=lang))
    return texts

def chunk_text(pdf_text_arr):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 100
    )
    chunk_data = []
    for i in range(len(pdf_text_arr)):
        chunk = text_splitter.split_text(pdf_text_arr[i])
        page_no = i+1
        chunk_info = [page_no, chunk]
        chunk_data.append(chunk_info)
    
    return chunk_data

def save_chunks_to_jsonl(chunk_data):
    chunk_jsonl = []
    for page_data in chunk_data:
        page_no, chunk_ls = page_data
        for chunk in chunk_ls:
            chunk_json ={
                "page_no" : page_no,
                "chunk" : chunk
            }
            chunk_jsonl.append(chunk_json)
    return chunk_jsonl

print(OCR_SPACE_API_KEY)
path = 'Data/raw/sample_contract_amc_cleaning.pdf'
img_ls = extract_text_from_scanned_pdf(path, OCR_SPACE_API_KEY)
print(img_ls[0])

# arr = ['abc abc abc', 'def def def', 'ghi ghi ghi']
# arr_joined = [" ".join(arr)]
# chunk_arr = chunk_text(arr)
# chunk_jsonl = save_chunks_to_jsonl(chunk_arr)
# print(chunk_jsonl[2])