# Schemas for DiagnosisAgent

# Placeholder structure for diagnosis data
diagnosis_schema = {
    "type": "object",
    "properties": {
        "condition_score": {"type": "number"},
        "repairability": {"type": "boolean"},
        "reuse_potential": {"type": "boolean"},
        "likely_repairs": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "confidence_score": {"type": "number"}
    }
}
