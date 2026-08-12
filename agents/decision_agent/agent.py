import json
from agents.common.base_agent import BaseAgent
from agents.common.llm import SharedLLM, MissingAPIKeyError, LLMGenerationError

class DecisionAgent(BaseAgent):
    """
    DecisionAgent is responsible for determining the best lifecycle action
    (REUSE, REPAIR, DONATE, RESELL, RECYCLE) and providing reasoning.
    """
    def __init__(self):
        super().__init__(name="DecisionAgent")
        self.llm = SharedLLM()

    def run(self, condition_score: float, repairability: bool, reuse_potential: bool, **kwargs) -> dict:
        """
        Execute the decision assessment.
        Tries to use LLM, otherwise falls back to mock rules.
        """
        prompt = f"""
        Given the following information about an item, determine the best lifecycle action.
        Choose from: REUSE, REPAIR, DONATE, RESELL, RECYCLE.
        Provide your output as a raw JSON object with the following keys:
        - "best_lifecycle_action": string (REUSE, REPAIR, DONATE, RESELL, RECYCLE)
        - "reasoning": string
        - "alternatives": list of strings (possible alternative actions)
        - "confidence_score": float (from 0.0 to 1.0)

        Condition Score: {condition_score}
        Repairability: {repairability}
        Reuse Potential: {reuse_potential}
        Extra Details: {kwargs}
        """

        try:
            raw_response = self.llm.generate(prompt, require_json=True)
            data = json.loads(raw_response)

            action = data.get("best_lifecycle_action", "REUSE")
            if action not in ["REUSE", "REPAIR", "DONATE", "RESELL", "RECYCLE"]:
                action = "REUSE"

            try:
                confidence_score = float(data.get("confidence_score", 0.85))
            except (ValueError, TypeError):
                confidence_score = 0.85

            alternatives = data.get("alternatives")
            if not isinstance(alternatives, list):
                alternatives = [str(alternatives)] if alternatives else []
            alternatives = [str(x) for x in alternatives]

            return {
                "best_lifecycle_action": action,
                "reasoning": str(data.get("reasoning", "Determined by LLM lifecycle decision analysis.")),
                "alternatives": alternatives,
                "confidence_score": confidence_score,
                "source": "llm"
            }

        except (MissingAPIKeyError, LLMGenerationError, json.JSONDecodeError, KeyError) as e:
            # Graceful mock fallback
            if reuse_potential:
                action = "REUSE"
            elif repairability:
                action = "REPAIR"
            else:
                action = "RECYCLE"

            return {
                "best_lifecycle_action": action,
                "reasoning": "Determined by structural rules based on condition & repairability.",
                "alternatives": ["DONATE" if action == "REUSE" else "RECYCLE"],
                "confidence_score": 0.85,
                "source": "mock_fallback"
            }
