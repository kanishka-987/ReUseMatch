from orchestration.orchestrator import CoordinatorOrchestrator

def test_coordinator_matching_flow():
    """
    Test that the CoordinatorOrchestrator runs the sequential agent pipeline
    and returns properly formatted results.
    """
    orchestrator = CoordinatorOrchestrator()
    
    # Test submission containing the keyword 'table' to trigger specific mock paths
    result = orchestrator.process_item_submission(
        description="A dark wooden dining table with some scratches",
        location="123 Hope Lane"
    )
    
    assert "item_details" in result
    assert "matches" in result
    assert "status" in result
    
    item_details = result["item_details"]
    assert item_details["name"] == "Generic Wooden Table"
    assert item_details["category"] == "Furniture"
    assert item_details["condition"] == "Good"
    
    # Verify matches were found
    assert len(result["matches"]) > 0
    first_match = result["matches"][0]
    
    assert "recipient" in first_match
    assert "logistics" in first_match
    assert "score" in first_match
    
    assert first_match["recipient"]["organization_id"] is not None
    assert first_match["logistics"]["distance_km"] > 0
    assert first_match["score"] == 7.0
