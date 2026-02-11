"""
FastAPI Application
-------------------
Exposes PII Masking LangGraph workflow via API
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.pipeline.langgraph_workflow import build_graph


# Create FastAPI app
app = FastAPI(title="PII Masking API")


# Build LangGraph workflow once
workflow = build_graph()


# Request schema
class TextRequest(BaseModel):
    text: str


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "API is running"}


# Main masking endpoint
@app.post("/mask-pii")
def mask_pii_endpoint(request: TextRequest):

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        input_state = {
            "text": request.text,
            "pii_entities": [],
            "masked_text": "",
            "is_valid": False
        }

        result = workflow.invoke(input_state)

        return {
            "masked_text": result.get("masked_text"),
            "pii_entities": result.get("pii_entities"),
            "is_valid": result.get("is_valid")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
