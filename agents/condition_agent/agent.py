import os

class ConditionAgent:
    """
    ConditionAgent / DiagnosisAgent evaluates structural condition, usability,
    repairability, and quality grade.
    """
    def __init__(self):
        pass

    def evaluate_condition(self, description: str, detected_attributes: list = None) -> dict:
        """
        Legacy condition evaluation method.
        """
        desc_lower = description.lower()
        
        if "destroy" in desc_lower or "beyond repair" in desc_lower or "recycl" in desc_lower:
            condition_grade = "Poor"
            score = 2.0
        elif "damaged" in desc_lower or "broken" in desc_lower:
            condition_grade = "Fair"
            score = 4.0
        elif "scratch" in desc_lower or "wear" in desc_lower:
            condition_grade = "Good"
            score = 7.0
        else:
            condition_grade = "Like New"
            score = 9.0

        return {
            "condition_grade": condition_grade,
            "usability_score": score,
            "requires_repair": "broken" in desc_lower or "scratch" in desc_lower or "damaged" in desc_lower,
            "notes": "Assessed via condition heuristics."
        }

    def run_diagnosis(self, description: str, detected_attributes: list = None) -> dict:
        """
        Runs DiagnosisAgent analysis returning structured diagnostic parameters.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        source = "llm" if api_key else "mock_fallback"

        cond = self.evaluate_condition(description, detected_attributes)
        score = cond["usability_score"]
        grade = cond["condition_grade"]

        desc_lower = description.lower()
        if grade in ["Like New", "Good"]:
            repairability = "High"
            reuse_potential = "High"
            likely_repairs = ["Cosmetic buffing & cleaning"]
            risks = ["Minor aesthetic blemish"]
        elif grade == "Fair":
            repairability = "Medium"
            reuse_potential = "Moderate"
            likely_repairs = ["Component replacement", "Port repair"]
            risks = ["Intermittent electrical fault"]
        else:
            repairability = "Low"
            reuse_potential = "Low (Salvage)"
            likely_repairs = ["Full board disassembly for parts"]
            risks = ["Unviable repair cost exceeding device value"]

        return {
            "status": "Success",
            "condition_score": score,
            "condition_grade": grade,
            "repairability": repairability,
            "reuse_potential": reuse_potential,
            "likely_repairs": likely_repairs,
            "risks": risks,
            "confidence_score": 0.85,
            "condition_notes": cond["notes"],
            "requires_repair": cond["requires_repair"]
        }

class DiagnosisAgent(ConditionAgent):
    def run(self, description: str, detected_attributes: list = None) -> dict:
        return self.run_diagnosis(description, detected_attributes)

class DecisionAgent:
    """
    DecisionAgent determines the optimal lifecycle action:
    REUSE / REPAIR / DONATE / RESELL / RECYCLE
    """
    def run(self, description: str, diagnosis_info: dict) -> dict:
        desc_lower = description.lower()
        grade = diagnosis_info.get("condition_grade", "Good")
        score = diagnosis_info.get("condition_score", 7.0)

        if "recycle" in desc_lower or "beyond repair" in desc_lower or grade == "Poor":
            best_action = "RECYCLE"
            reasoning = "Device is severely degraded or explicitly flagged for component breakdown and material recycling."
            alternatives = ["SALVAGE_PARTS"]
        elif "repair" in desc_lower or diagnosis_info.get("requires_repair"):
            best_action = "REPAIR"
            reasoning = "Device retains high core functional value but requires component repair before redistribution."
            alternatives = ["REUSE", "DONATE"]
        elif score >= 8.0:
            best_action = "DONATE"
            reasoning = "High usability score makes device ideal for direct donation to educational or non-profit recipients."
            alternatives = ["REUSE", "RESELL"]
        else:
            best_action = "REUSE"
            reasoning = "Item is in good working order suitable for direct community reuse."
            alternatives = ["DONATE", "REPAIR"]

        return {
            "status": "Success",
            "best_lifecycle_action": best_action,
            "reasoning": reasoning,
            "alternatives": alternatives,
            "confidence_score": 0.90
        }
