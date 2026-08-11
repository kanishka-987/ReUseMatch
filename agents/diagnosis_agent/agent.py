from agents.common.base_agent import BaseAgent

class DiagnosisAgent(BaseAgent):
    """
    DiagnosisAgent is responsible for evaluating usability, structural condition,
    and classifying the item's diagnosis details based on extracted evidence.
    """
    def __init__(self):
        super().__init__(name="DiagnosisAgent")

    def evaluate_condition(self, description: str, detected_attributes: list = None) -> dict:
        """
        Preserved from ConditionAgent.
        Analyzes the item's description and attributes to assign a quality tier.
        """
        desc_lower = description.lower()
        
        if "scratch" in desc_lower or "wear" in desc_lower:
            condition_grade = "Good"
            score = 7.0
        elif "damaged" in desc_lower or "broken" in desc_lower:
            condition_grade = "Fair"
            score = 4.0
        else:
            condition_grade = "Like New"
            score = 9.0

        return {
            "condition_grade": condition_grade,
            "usability_score": score,
            "requires_repair": "broken" in desc_lower,
            "notes": "Assessed via condition heuristics."
        }

    def run(self, description: str, detected_attributes: list = None) -> dict:
        """
        Execute the device diagnosis process.
        """
        condition_info = self.evaluate_condition(description, detected_attributes)
        
        return {
            "condition_score": condition_info.get("usability_score", 5.0),
            "repairability": not condition_info.get("requires_repair", False),
            "reuse_potential": True if condition_info.get("usability_score", 0.0) >= 5.0 else False,
            "likely_repairs": ["cosmetic touchups"] if condition_info.get("requires_repair") else [],
            "risks": ["unknown internal wear"],
            "confidence_score": 0.90,
            "condition_info": condition_info
        }
