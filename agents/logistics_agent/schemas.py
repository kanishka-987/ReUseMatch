from pydantic import BaseModel, Field

class LogisticsInput(BaseModel):
    """
    Input schema for LogisticsAgent.
    """
    donor_location: str = Field(..., min_length=1, description="Physical location of the donor (origin).")
    recipient_location: str = Field(..., min_length=1, description="Physical location of the recipient (destination).")

class LogisticsResult(BaseModel):
    """
    Output schema for LogisticsAgent.
    """
    origin: str = Field(..., min_length=1, description="Donor origin address.")
    destination: str = Field(..., min_length=1, description="Recipient destination address.")
    distance_km: float = Field(..., ge=0.0, description="Estimated distance in kilometers.")
    estimated_cost_usd: float = Field(..., ge=0.0, description="Estimated transport cost in USD.")
    recommended_mode: str = Field(..., min_length=1, description="Recommended mode of transport.")
    route_status: str = Field(..., min_length=1, description="Status of the route calculation (e.g. optimal).")
