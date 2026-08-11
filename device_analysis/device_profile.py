from pydantic import BaseModel, Field
from typing import List, Optional

class DeviceProfile(BaseModel):
    """
    DeviceProfile defines the structured representation of a device submitted for reuse.
    It contains hardware characteristics, current status, physical/functional condition,
    and lists of damaged/missing/reusable components.
    """
    item_id: str = Field(..., description="Unique identifier for the item")
    item_name: str = Field(..., description="Name or title of the submitted device")
    category: str = Field(..., description="High-level category (e.g., Laptop, Desktop, Monitor, Smartphone)")
    subcategory: Optional[str] = Field(None, description="Detailed subcategory (e.g., Gaming Laptop, Office Monitor)")
    brand: str = Field(..., description="Manufacturer brand of the device")
    model: str = Field(..., description="Model identifier of the device")
    serial_number: Optional[str] = Field(None, description="Optional, privacy-safe serial identifier")
    estimated_age: float = Field(..., ge=0, description="Estimated age of the device in years")
    purchase_year: Optional[int] = Field(None, ge=1900, description="Optional year of initial purchase")
    
    # Power and basic status
    working_status: bool = Field(..., description="Is the device operational at a basic level")
    power_status: bool = Field(..., description="Does the device turn on and hold power")
    
    # Condition strings
    physical_condition: str = Field(..., description="Physical state: EXCELLENT, GOOD, FAIR, POOR, NON_FUNCTIONAL")
    functional_condition: str = Field(..., description="Functional state: EXCELLENT, GOOD, FAIR, POOR, NON_FUNCTIONAL")
    
    # Component status lists
    visible_damage: List[str] = Field(default_factory=list, description="List of visible physical damages")
    damaged_components: List[str] = Field(default_factory=list, description="Components that are broken or faulty")
    reusable_components: List[str] = Field(default_factory=list, description="Components identified as salvageable")
    missing_components: List[str] = Field(default_factory=list, description="Components that are absent")
