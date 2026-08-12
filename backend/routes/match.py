from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.services.matching_service import MatchingService
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

@router.get("/{device_id}")
def get_device_matches(device_id: str, db: Session = Depends(get_db)):
    """
    Retrieves ranked recipient matches for a specific device by its UUID.
    Returns transparent match score and detailed reasons.
    """
    try:
        return MatchingService.match_device_to_recipients(device_id, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error matching device to recipients: {str(e)}"
        )
