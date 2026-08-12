import json
from agents.common.base_agent import BaseAgent
from agents.common.llm import SharedLLM, MissingAPIKeyError, LLMGenerationError

class DiagnosisAgent(BaseAgent):
    """
    DiagnosisAgent is responsible for evaluating usability, structural condition,
    and classifying the item's diagnosis details based on extracted evidence.
    """
    def __init__(self):
        super().__init__(name="DiagnosisAgent")
        self.llm = SharedLLM()

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
        Tries to use LLM, otherwise falls back to mock rules.
        """
        prompt = f"""
        Analyze the condition of the following item using description and attributes.
        Provide your output as a raw JSON object with the following keys:
        - "condition_grade": string (New, Like New, Good, Fair, Poor)
        - "condition_score": float/int (from 0.0 to 10.0 indicating usability score)
        - "repairability": boolean (true if item can be repaired or doesn't need repair)
        - "reuse_potential": boolean (true if item is usable or repairable for reuse)
        - "likely_repairs": list of strings (needed repairs/touch-ups)
        - "risks": list of strings (potential defects or structural concerns)
        - "confidence_score": float (from 0.0 to 1.0)
        - "notes": string

        Item Description: {description}
        Detected Attributes: {detected_attributes}
        """

        try:
            raw_response = self.llm.generate(prompt, require_json=True)
            data = json.loads(raw_response)

            try:
                condition_score = float(data.get("condition_score", 5.0))
            except (ValueError, TypeError):
                condition_score = 5.0

            try:
                confidence_score = float(data.get("confidence_score", 0.90))
            except (ValueError, TypeError):
                confidence_score = 0.90

            repairability = bool(data.get("repairability", True))
            reuse_potential = bool(data.get("reuse_potential", True))

            likely_repairs = data.get("likely_repairs")
            if not isinstance(likely_repairs, list):
                likely_repairs = [str(likely_repairs)] if likely_repairs else []
            likely_repairs = [str(x) for x in likely_repairs]

            risks = data.get("risks")
            if not isinstance(risks, list):
                risks = [str(risks)] if risks else []
            risks = [str(x) for x in risks]

            condition_info = {
                "condition_grade": str(data.get("condition_grade", "Like New")),
                "usability_score": condition_score,
                "requires_repair": not repairability,
                "notes": str(data.get("notes", "Assessed via LLM condition analysis."))
            }

            return {
                "condition_score": condition_score,
                "repairability": repairability,
                "reuse_potential": reuse_potential,
                "likely_repairs": likely_repairs,
                "risks": risks,
                "confidence_score": confidence_score,
                "condition_info": condition_info,
                "source": "llm"
            }

        except (MissingAPIKeyError, LLMGenerationError, json.JSONDecodeError, KeyError) as e:
            # Graceful mock fallback
            condition_info = self.evaluate_condition(description, detected_attributes)
            return {
                "condition_score": condition_info.get("usability_score", 5.0),
                "repairability": not condition_info.get("requires_repair", False),
                "reuse_potential": True if condition_info.get("usability_score", 0.0) >= 5.0 else False,
                "likely_repairs": ["cosmetic touchups"] if condition_info.get("requires_repair") else [],
                "risks": ["unknown internal wear"],
                "confidence_score": 0.90,
                "condition_info": condition_info,
                "source": "mock_fallback"
            }
