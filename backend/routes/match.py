from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from orchestration.orchestrator import CoordinatorOrchestrator

router = APIRouter(prefix="/matches", tags=["matching"])
orchestrator = CoordinatorOrchestrator()

class ItemSubmission(BaseModel):
    name: Optional[str] = "Unused Item"
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
    item_details: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None
    diagnosis: Optional[Dict[str, Any]] = None
    decision: Optional[Dict[str, Any]] = None
    need: Optional[Dict[str, Any]] = None
    logistics: Optional[Any] = None
    final_recommendation: Optional[Dict[str, Any]] = None

@router.post("/", response_model=MatchPipelineResult)
def trigger_matching(submission: ItemSubmission):
    """
    Triggers the 5-agent sequential pipeline:
    EvidenceAgent -> DiagnosisAgent -> DecisionAgent -> NeedAgent -> LogisticsAgent.
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
        "matches": result["matches"],
        "item_details": result["item_details"],
        "evidence": result["evidence"],
        "diagnosis": result["diagnosis"],
        "decision": result["decision"],
        "need": result["need"],
        "logistics": result["logistics"],
        "final_recommendation": result["final_recommendation"]
    }
