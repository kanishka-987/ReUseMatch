from agents.common.base_agent import BaseAgent

class EvidenceAgent(BaseAgent):
    """
    EvidenceAgent is responsible for analyzing device info, extracting evidence,
    separating user claims from observed evidence, and producing confidence scores.
    """
    def __init__(self, model_name: str = "default-vision-model"):
        super().__init__(name="EvidenceAgent")
        self.model_name = model_name

    def identify_item(self, description: str, image_url: str = None) -> dict:
        """
        Preserved from ObjectAgent.
        Parses item information and outputs metadata about what the item is.
        """
        return {
            "identified_name": "Generic Wooden Table" if "table" in description.lower() else "Unknown Item",
            "category": "Furniture" if "table" in description.lower() else "General",
            "detected_attributes": ["wood", "brown"] if "table" in description.lower() else [],
            "confidence": 0.85
        }

    def run(self, description: str, image_url: str = None) -> dict:
        """
        Execute the evidence extraction process.
        """
        # Call the preserved function for backward compatibility
        item_details = self.identify_item(description, image_url)
        
        return {
            "observed_evidence": item_details.get("detected_attributes", []),
            "user_claims": [description],
            "missing_information": ["serial_number", "purchase_date"],
            "confidence_score": item_details.get("confidence", 0.85),
            "item_details": item_details
        }
