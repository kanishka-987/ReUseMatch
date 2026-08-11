# Schemas for EvidenceAgent

# Placeholder structure for evidence data
evidence_schema = {
    "type": "object",
    "properties": {
        "observed_evidence": {"type": "array", "items": {"type": "string"}},
        "user_claims": {"type": "array", "items": {"type": "string"}},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "confidence_score": {"type": "number"}
    }
}
