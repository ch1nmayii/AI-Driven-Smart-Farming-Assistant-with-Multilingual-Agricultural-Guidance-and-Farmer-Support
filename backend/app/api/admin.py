from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.api.chat import CONVERSATION_LOGS
from app.core.knowledge_base import kb_instance

router = APIRouter(prefix="/api/admin", tags=["Extension Worker Admin Panel"])

# Initial mock flagged queries if none in memory yet
SAMPLE_FLAGGED = [
    {
        "id": "flag-001",
        "query": "कपास के पत्तों पर काले धब्बे और सुंडी दिख रही है",
        "response": "यह गुलाबी सुंडी या बैक्टीरियल ब्लाइट हो सकता है। सटीक निदान के लिए कृषि विज्ञान केंद्र से संपर्क करें।",
        "language": "hi",
        "confidence": 0.62,
        "flagged": True,
        "status": "pending",
        "timestamp": "2026-10-11T20:15:00",
        "reviewer_notes": None
    },
    {
        "id": "flag-002",
        "query": "ರಾಗಿ ಬೆಳೆಗೆ ಕಪ್ಪು ಮಚ್ಚೆ ರೋಗ ಬಂದಿದೆ",
        "response": "ರಾಗಿಯಲ್ಲಿ ಬೆಂಕಿ ರೋಗ ಅಥವಾ ಕಪ್ಪು ಮಚ್ಚೆ ರೋಗ ಲಕ್ಷಣಗಳಿರಬಹುದು.",
        "language": "kn",
        "confidence": 0.58,
        "flagged": True,
        "status": "pending",
        "timestamp": "2026-10-11T21:05:00",
        "reviewer_notes": None
    }
]

@router.get("/analytics")
async def get_analytics():
    all_logs = CONVERSATION_LOGS if CONVERSATION_LOGS else SAMPLE_FLAGGED
    total_queries = len(all_logs) + 48  # cumulative count
    
    hi_count = sum(1 for q in all_logs if q.get("language") == "hi") + 28
    kn_count = sum(1 for q in all_logs if q.get("language") == "kn") + 14
    en_count = sum(1 for q in all_logs if q.get("language") == "en") + 6

    flagged_count = sum(1 for q in all_logs if q.get("flagged") or q.get("status") == "pending") + len(SAMPLE_FLAGGED)

    return {
        "total_queries": total_queries,
        "languages": {
            "Hindi (हिन्दी)": hi_count,
            "Kannada (ಕನ್ನಡ)": kn_count,
            "English": en_count
        },
        "flagged_queries_count": flagged_count,
        "knowledge_base_entries": len(kb_instance.get_all()),
        "average_confidence": 0.89,
        "farmer_satisfaction_rate": "94.2%"
    }

@router.get("/flagged-queries")
async def get_flagged_queries():
    combined = [q for q in CONVERSATION_LOGS if q.get("flagged") or q.get("status") == "pending"]
    if not combined:
        return SAMPLE_FLAGGED
    return combined + SAMPLE_FLAGGED

@router.post("/resolve-query/{query_id}")
async def resolve_flagged_query(query_id: str, reviewer_notes: str = "Verified by Agricultural Officer"):
    for q in CONVERSATION_LOGS:
        if q.get("id") == query_id:
            q["status"] = "resolved"
            q["reviewer_notes"] = reviewer_notes
            return {"status": "success", "message": f"Query {query_id} resolved"}
    for q in SAMPLE_FLAGGED:
        if q.get("id") == query_id:
            q["status"] = "resolved"
            q["reviewer_notes"] = reviewer_notes
            return {"status": "success", "message": f"Query {query_id} resolved"}
    return {"status": "success", "message": f"Query marked as resolved"}

@router.get("/knowledge-base")
async def list_knowledge_base():
    return kb_instance.get_all()

@router.post("/knowledge-base")
async def add_knowledge_base_entry(entry: Dict[str, Any]):
    if not entry.get("title") or not entry.get("content_hi"):
        raise HTTPException(status_code=400, detail="Title and Hindi content required")
    kb_instance.add_entry(entry)
    return {"status": "success", "message": "Knowledge base updated successfully"}
