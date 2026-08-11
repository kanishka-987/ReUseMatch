from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from orchestration.orchestrator import CoordinatorOrchestrator

router = APIRouter(prefix="/matches", tags=["matching"])
orchestrator = CoordinatorOrchestrator()

class ItemSubmission(BaseModel):
    name: str
    description: str
    image_url: Optional[str] = None
    location: str

class RecipientInfo(BaseModel):
    organization_id: str
    organization_name: str
    priority: str

class LogisticsInfo(BaseModel):
    origin: str
    destination: str
    distance_km: float
    estimated_cost_usd: float
    recommended_mode: str

class MatchDetail(BaseModel):
    recipient: RecipientInfo
    logistics: LogisticsInfo
    score: float

class MatchPipelineResult(BaseModel):
    item_name: str
    category: str
    condition: str
    status: str
    matches: List[MatchDetail]

@router.post("/", response_model=MatchPipelineResult)
def trigger_matching(submission: ItemSubmission):
    """
    Triggers the 4-agent sequential pipeline:
    Object identification -> Condition grading -> Recipient matching -> Logistics routing.
    """
    result = orchestrator.process_item_submission(
        description=submission.description,
        location=submission.location,
        image_url=submission.image_url
    )
    
    return {
        "item_name": result["item_details"]["name"],
        "category": result["item_details"]["category"],
        "condition": result["item_details"]["condition"],
        "status": result["status"],
        "matches": result["matches"]
    }
