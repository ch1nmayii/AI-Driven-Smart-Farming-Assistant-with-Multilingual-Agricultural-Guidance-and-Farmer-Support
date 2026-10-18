import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.core.rag_engine import rag_engine

router = APIRouter(prefix="/api/chat", tags=["Farmer Chat"])

CONVERSATION_LOGS = []

@router.post("", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty")

    result = await rag_engine.process_query(
        query=request.message,
        language=request.language,
        location=request.location or "Uttar Pradesh",
        session_id=request.session_id or "farmer-session-default"
    )

    log_entry = {
        "id": str(uuid.uuid4()),
        "session_id": request.session_id,
        "query": request.message,
        "response": result["response_text"],
        "language": result["language"],
        "intent": result["intent"],
        "confidence": result["confidence_score"],
        "flagged": result["flagged_for_review"],
        "status": "pending" if result["flagged_for_review"] else "resolved",
        "timestamp": datetime.utcnow().isoformat(),
        "reviewer_notes": None
    }
    CONVERSATION_LOGS.append(log_entry)

    return ChatResponse(
        response_text=result["response_text"],
        language=result["language"],
        intent=result["intent"],
        intent_confidence=result.get("intent_confidence", 0.92),
        confidence_score=result["confidence_score"],
        flagged_for_review=result["flagged_for_review"],
        sources=result["sources"],
        entities=result.get("entities", [])
    )
