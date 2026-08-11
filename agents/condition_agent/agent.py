class ConditionAgent:
    """
    ConditionAgent is responsible for evaluating usability, structural condition,
    and classifying the item into a condition tier (New, Like New, Good, Fair, Poor).
    """
    def __init__(self):
        pass

    def evaluate_condition(self, description: str, detected_attributes: list = None) -> dict:
        """
        Analyzes the item's description and attributes to assign a quality tier.
        """
        # Placeholder evaluation logic
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
