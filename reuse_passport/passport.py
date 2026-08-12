from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from .passport_status import PassportStatus

class StatusHistoryEntry(BaseModel):
    """
    Tracks state modifications over the lifetime of the reuse passport.
    """
    status: PassportStatus = Field(..., description="Target lifecycle state")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="ISO timestamp when the transition occurred"
    )
    description: str = Field(..., description="Audit log narrative of what triggered the status change")

class DigitalReusePassport(BaseModel):
    """
    Standardized Digital Reuse Passport record detailing quality, parts recovery,
    reusability ratings, recommendations, and chain-of-custody lifecycle history.
    """
    passport_id: str = Field(..., description="Unique passport identifier: RM-PASS-YYYY-XXXXXX")
    item_id: str = Field(..., description="Item ID matching the main submission record")
    device_name: str = Field(..., description="Readable brand/model name")
    category: str = Field(..., description="Category classification")
    brand: str = Field(..., description="Manufacturer brand")
    model: str = Field(..., description="Model designator")
    estimated_age: float = Field(..., description="Device age in years")
    
    # Condition parameters
    physical_condition: str = Field(..., description="Physical state")
    functional_condition: str = Field(..., description="Functional state")
    damage_description: Optional[str] = Field(None, description="Detailed damages notes")
    repairability_score: float = Field(..., ge=0.0, le=100.0, description="Repair score")
    
    # Components list
    reusable_components: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Catalog of components and salvage state"
    )
    component_recovery: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Estimated component recovery potential assessments"
    )
    
    # Sustainability / Impact
    reuse_score: float = Field(..., ge=0.0, le=100.0, description="Reuse score")
    reuse_level: str = Field(..., description="Reuse tier name")
    estimated_remaining_life: str = Field(..., description="Useful life duration tier")
    recyclability_status: str = Field(..., description="Recyclability assessment status")
    
    # Recommendation details
    recommended_reuse_path: str = Field(..., description="Target circular route (e.g. DIRECT_REUSE, REPAIR)")
    possible_recipients: List[str] = Field(
        default_factory=list, 
        description="Suggested target segments or non-profits"
    )
    
    # Lifecycle settings
    current_status: PassportStatus = Field(PassportStatus.ANALYZED, description="Active status")
    analysis_date: str = Field(..., description="ISO timestamp of initial analyzer run")
    last_updated_date: str = Field(..., description="ISO timestamp of last update")
    
    # Verification parameters
    analysis_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence metric of calculations")
    validation_status: str = Field("PENDING", description="Passport integrity verification status")
    
    # Lifecycle history
    status_history: List[StatusHistoryEntry] = Field(
        default_factory=list, 
        description="Sequential list of status changes"
    )
