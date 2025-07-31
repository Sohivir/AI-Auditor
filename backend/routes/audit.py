from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.rag_engine import retrieve_top_k
from backend.services.audit_agent import run_audit


router = APIRouter()

class AuditRequest(BaseModel):
    contract_id : str
    question : str

@router.post("/audit")
async def audit_contract(request: AuditRequest):
    top_chunks = retrieve_top_k(request.question)
    response = run_audit(request, top_chunks)

    response_json = {
        "resp": response
    }
    return response_json


