from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

class DeviceInput(BaseModel):
    """
    Input schema for EvidenceAgent.run() containing only the fields consumed today.
    """
    description: str = Field(..., description="User-provided description of the item.")
    image_url: Optional[str] = Field(None, description="Optional URL to an image of the item.")

class EvidenceResult(BaseModel):
    """
    Output schema for EvidenceAgent representing the validated output.
    """
    observed_evidence: List[str] = Field(default_factory=list, description="Extracted physical attributes and evidence.")
    functional_claims: List[str] = Field(default_factory=list, description="User claims mapped to functional statements.")
    missing_information: List[str] = Field(default_factory=list, description="Explicitly identified missing device info.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the extraction.")
    source: Literal["llm", "mock_fallback"] = Field(..., description="Indicates if the result came from 'llm' or 'mock_fallback'.")
    item_details: Dict[str, Any] = Field(..., description="Embedded item details to preserve backward compatibility.")
