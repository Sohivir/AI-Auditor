from fastapi import FastAPI
from routes.audit import router as audit_router  # adjust path if needed

app = FastAPI()

# Register your route
app.include_router(audit_router)