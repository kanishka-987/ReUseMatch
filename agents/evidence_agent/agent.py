import json
import re
from agents.common.base_agent import BaseAgent
from agents.common.llm import SharedLLM, MissingAPIKeyError, LLMGenerationError
from .schemas import DeviceInput, EvidenceResult

class EvidenceAgent(BaseAgent):
    """
    EvidenceAgent is responsible for analyzing device info, extracting evidence,
    separating user claims from observed evidence, and producing confidence scores.
    """
    def __init__(self, model_name: str = "default-vision-model"):
        super().__init__(name="EvidenceAgent")
        self.model_name = model_name
        self.llm = SharedLLM()

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

    def _filter_functional_claims(self, claims: list) -> list:
        """
        Filters statements to only keep those semantically related to functionality or condition.
        """
        functional_keywords = {
            "broken", "damage", "scratch", "wear", "crack", "tear", "defect", "repair", "functional",
            "working", "sturdy", "unusable", "usable", "condition", "grade", "turns on", "operates",
            "scratched", "damaged", "broken screen", "stains", "chipped", "dented", "perfect",
            "like new", "brand new", "good", "fair", "poor", "worn", "ripped", "stained", "table"
        }
        filtered = []
        for claim in claims:
            claim_str = str(claim)
            claim_lower = claim_str.lower()
            words = set(re.findall(r'\b\w+\b', claim_lower))

            # Check for exact word matches or multi-word phrase matching
            has_keyword = False
            for kw in functional_keywords:
                if " " in kw:
                    if kw in claim_lower:
                        has_keyword = True
                        break
                else:
                    if kw in words:
                        has_keyword = True
                        break
            if has_keyword:
                filtered.append(claim_str)
        return filtered

    def run(self, description: str, image_url: str = None) -> dict:
        """
        Execute the evidence extraction process.
        Tries to use LLM, otherwise falls back to mock rules.
        """
        # Validate inputs using Pydantic
        inputs = DeviceInput(description=description, image_url=image_url)
        desc_value = inputs.description
        img_value = inputs.image_url

        prompt = f"""
        Analyze the following description of an item (and optional image: {img_value}) to extract structured evidence.
        Provide your output as a raw JSON object with the following keys:
        - "observed_evidence": list of strings (physical attributes, materials, colors, observed state)
        - "user_claims": list of strings (what the user claims or states about the item)
        - "missing_information": list of strings (what details are missing, e.g. serial_number, model, brand)
        - "confidence_score": float between 0.0 and 1.0
        - "identified_name": string (a descriptive name of the item)
        - "category": string (e.g. Furniture, Electronics, Clothing, General)

        Item Description: {desc_value}
        """

        try:
            raw_response = self.llm.generate(prompt, require_json=True)
            data = json.loads(raw_response)

            # Normalize and validate response structure
            observed_evidence = data.get("observed_evidence")
            if not isinstance(observed_evidence, list):
                observed_evidence = [str(observed_evidence)] if observed_evidence else []
            observed_evidence = [str(x) for x in observed_evidence]

            user_claims = data.get("user_claims")
            if not isinstance(user_claims, list):
                user_claims = [str(user_claims)] if user_claims else []

            # Filter user claims semantically to claims about functionality/condition
            functional_claims = self._filter_functional_claims(user_claims)

            missing_info = data.get("missing_information")
            if not isinstance(missing_info, list):
                missing_info = [str(missing_info)] if missing_info else []
            missing_info = [str(x) for x in missing_info]

            try:
                confidence_score = float(data.get("confidence_score", 0.85))
            except (ValueError, TypeError):
                confidence_score = 0.85

            item_details = {
                "identified_name": str(data.get("identified_name", "Unknown Item")),
                "category": str(data.get("category", "General")),
                "detected_attributes": observed_evidence,
                "confidence": confidence_score
            }

            # Instantiate and validate EvidenceResult model
            result_model = EvidenceResult(
                observed_evidence=observed_evidence,
                functional_claims=functional_claims,
                missing_information=missing_info,
                confidence=confidence_score,
                source="llm",
                item_details=item_details
            )
            return result_model.model_dump()

        except (MissingAPIKeyError, LLMGenerationError, json.JSONDecodeError, KeyError) as e:
            # Graceful mock fallback
            item_details = self.identify_item(desc_value, img_value)
            mock_confidence = item_details.get("confidence", 0.85)

            # Filter input description semantically for fallback functional claims
            functional_claims = self._filter_functional_claims([desc_value])

            result_model = EvidenceResult(
                observed_evidence=item_details.get("detected_attributes", []),
                functional_claims=functional_claims,
                missing_information=["serial_number", "purchase_date"],
                confidence=mock_confidence,
                source="mock_fallback",
                item_details=item_details
            )
            return result_model.model_dump()
