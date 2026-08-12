from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class NeedInput(BaseModel):
    """
    Input schema for NeedAgent.
    """
    category: str = Field(..., description="The category of the item.")
    condition_grade: str = Field(..., description="The condition grade of the item.")

class NeedMatch(BaseModel):
    """
    Schema for a single matched organization.
    """
    organization_id: str = Field(..., description="Unique ID of the matched organization.")
    organization_name: str = Field(..., description="Name of the matched organization.")
    priority: Literal["High", "Medium", "Low"] = Field(..., description="Match priority grade.")
    match_score: float = Field(..., ge=0.0, le=100.0, description="Match score ranking from 0 to 100.")
    reason: str = Field(..., description="Plain explanation of why the match occurred.")
    location: Optional[str] = Field(None, description="Physical location of the organization.")
    missing_information: List[str] = Field(default_factory=list, description="Missing details that would refine this match.")

class NeedResult(BaseModel):
    """
    Output schema for NeedAgent.
    """
    matches: List[NeedMatch] = Field(default_factory=list, description="List of matched organizations.")
