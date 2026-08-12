from agents.common.base_agent import BaseAgent
from .schemas import LogisticsInput, LogisticsResult

class LogisticsAgent(BaseAgent):
    """
    LogisticsAgent is responsible for calculating distances, optimal transportation modes,
    routes, and estimating delivery costs between donor and recipient locations.
    """
    def __init__(self):
        super().__init__(name="LogisticsAgent")

    def evaluate_logistics(self, donor_location: str, recipient_location: str) -> dict:
        """
        Estimates travel route, distance, mode of transport, and associated costs.
        Preserved fallback mock calculations.
        """
        distance_km = 12.5  # mock value
        cost_est = round(distance_km * 1.5, 2)  # $1.50 per km
        
        return {
            "origin": donor_location,
            "destination": recipient_location,
            "distance_km": distance_km,
            "estimated_cost_usd": cost_est,
            "recommended_mode": "Local Pickup Courier" if distance_km < 30 else "Standard Shipping",
            "route_status": "optimal"
        }

    def run(self, donor_location: str, recipient_location: str) -> dict:
        """
        Execute logistics evaluation and validate inputs/outputs.
        """
        # Validate inputs using Pydantic
        inputs = LogisticsInput(donor_location=donor_location, recipient_location=recipient_location)

        # Evaluate using mock logic
        raw_result = self.evaluate_logistics(inputs.donor_location, inputs.recipient_location)

        # Validate outputs using Pydantic
        result_model = LogisticsResult(**raw_result)
        return result_model.model_dump()
