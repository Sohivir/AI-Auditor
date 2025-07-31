import requests

payload = {
    "contract_id": "001",
    "question": "Summarize the confidentiality clause."
}

response = requests.post("http://localhost:8000/audit", json=payload)
print(response.json())