from orchestration.orchestrator import CoordinatorOrchestrator
from unittest.mock import patch, MagicMock

def test_coordinator_matching_flow():
    """
    Test 1, 5, 6, 8: Complete end-to-end workflow (Evidence -> Diagnosis -> Decision -> Need -> Logistics).
    Verifies location mapping and mock recipient containment.
    """
    orchestrator = CoordinatorOrchestrator()

    # Test submission containing 'table' to trigger matches
    result = orchestrator.process_item_submission(
        description="A dark wooden dining table with some scratches",
        location="123 Hope Lane"
    )

    assert result["status"] == "matched"
    assert "item_details" in result
    assert "matches" in result

    item_details = result["item_details"]
    assert item_details["name"] == "Generic Wooden Table"
    assert item_details["category"] == "Furniture"
    assert item_details["condition"] == "Good"

    # Verify matches were found and contain expected mock organizations
    assert len(result["matches"]) > 0
    first_match = result["matches"][0]

    assert "recipient" in first_match
    assert "logistics" in first_match
    assert "score" in first_match

    assert first_match["recipient"]["organization_id"] in ["org_001", "org_002", "org_003"]
    assert first_match["logistics"]["distance_km"] > 0
    assert first_match["score"] == 7.0

def test_coordinator_missing_inputs():
    """
    Test 2: Verify missing/incomplete description or location returns error status.
    """
    orchestrator = CoordinatorOrchestrator()

    # Missing description
    res_no_desc = orchestrator.process_item_submission(description="", location="123 Hope Lane")
    assert res_no_desc["status"] == "error"
    assert "description" in res_no_desc["missing_information"]

    # Missing location
    res_no_loc = orchestrator.process_item_submission(description="A wooden table", location="")
    assert res_no_loc["status"] == "error"
    assert "location" in res_no_loc["missing_information"]

def test_coordinator_no_matching_organization():
    """
    Test 3: No matching organization returns no_match_found.
    """
    orchestrator = CoordinatorOrchestrator()

    # Category "submarine" has no matches
    result = orchestrator.process_item_submission(
        description="A yellow submarine model",
        location="123 Hope Lane"
    )

    assert result["status"] == "no_match_found"
    assert len(result["matches"]) == 0

@patch("agents.decision_agent.agent.DecisionAgent.run")
def test_coordinator_recycle_decision_path(mock_decision_run):
    """
    Test 4: Verify RECYCLE decision bypasses Need/Logistics matching and returns recycle status.
    """
    orchestrator = CoordinatorOrchestrator()

    # Mock DecisionAgent to return RECYCLE
    mock_decision_run.return_value = {
        "best_lifecycle_action": "RECYCLE",
        "reasoning": "Device is completely broken and unrepairable.",
        "alternatives": [],
        "confidence_score": 1.0,
        "source": "llm"
    }

    result = orchestrator.process_item_submission(
        description="A completely smashed broken wooden table",
        location="123 Hope Lane"
    )

    assert result["status"] == "recycle"
    assert result["decision_reasoning"] == "Device is completely broken and unrepairable."
    assert len(result["matches"]) == 0

def test_no_deprecated_imports():
    """
    Test 7: Verify that deprecated ObjectAgent and ConditionAgent are not imported/used.
    """
    # Simply import orchestrator to ensure it collects without module errors
    from orchestration.orchestrator import CoordinatorOrchestrator
    orchestrator = CoordinatorOrchestrator()
    assert hasattr(orchestrator, "evidence_agent")
    assert hasattr(orchestrator, "diagnosis_agent")
    assert not hasattr(orchestrator, "object_agent")
    assert not hasattr(orchestrator, "condition_agent")
