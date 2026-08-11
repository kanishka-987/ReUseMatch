# Schemas for DecisionAgent

# Placeholder structure for decision data
decision_schema = {
    "type": "object",
    "properties": {
        "best_lifecycle_action": {"type": "string", "enum": ["REUSE", "REPAIR", "DONATE", "RESELL", "RECYCLE"]},
        "reasoning": {"type": "string"},
        "alternatives": {"type": "array", "items": {"type": "string"}},
        "confidence_score": {"type": "number"}
    }
}
