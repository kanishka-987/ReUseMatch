import pytest
from pydantic import ValidationError
from agents.need_agent.agent import NeedAgent
from agents.need_agent.schemas import NeedInput, NeedResult

def test_need_agent_valid_laptop_match():
    """
    Test 1, 8, 9, 10, 11, 12: Verify that valid laptop input produces expected matches
    from the mock dataset, ranked by match score, and that output validates against NeedResult.
    """
    agent = NeedAgent()
    result = agent.run(category="laptop", condition_grade="Like New")
    
    assert "matches" in result
    matches = result["matches"]
    
    # We expect "Tech for All" (min Fair) and "Digital Divide Aid" (min Good)
    assert len(matches) == 2
    
    # Check ranking: "Digital Divide Aid" and "Tech for All" both have score 100.0 for Like New
    org_ids = [m["organization_id"] for m in matches]
    assert "org_004" in org_ids
    assert "org_005" in org_ids
    
    for match in matches:
        assert 0.0 <= match["match_score"] <= 100.0
        assert match["organization_id"] in ["org_004", "org_005"]
        assert "Category 'laptop' matches" in match["reason"]

def test_need_agent_valid_monitor_match():
    """
    Test 2: Verify monitor input matches "Tech for All".
    """
    agent = NeedAgent()
    result = agent.run(category="monitor", condition_grade="Good")
    
    matches = result["matches"]
    assert len(matches) == 1
    assert matches[0]["organization_id"] == "org_004"
    assert matches[0]["organization_name"] == "Tech for All"

def test_need_agent_category_mismatch():
    """
    Test 3: Category mismatch produces no matches.
    """
    agent = NeedAgent()
    result = agent.run(category="submarine", condition_grade="Like New")
    assert len(result["matches"]) == 0

def test_need_agent_condition_too_poor():
    """
    Test 4: Condition below minimum condition grade produces no match.
    """
    agent = NeedAgent()
    # Digital Divide Aid requires Good. Tech for All requires Fair.
    # Poor is below both, so should return 0 matches.
    result = agent.run(category="laptop", condition_grade="Poor")
    assert len(result["matches"]) == 0

def test_need_agent_missing_category():
    """
    Test 5: Missing category raises ValidationError.
    """
    agent = NeedAgent()
    with pytest.raises(ValidationError):
        agent.run(category=None, condition_grade="Good")  # type: ignore

def test_need_agent_missing_condition():
    """
    Test 6: Missing condition raises ValidationError.
    """
    agent = NeedAgent()
    with pytest.raises(ValidationError):
        agent.run(category="laptop", condition_grade=None)  # type: ignore

def test_need_agent_invalid_input_types():
    """
    Test 7: Invalid input types are handled by schema validation.
    """
    agent = NeedAgent()
    with pytest.raises(ValidationError):
        agent.run(category=123, condition_grade="Good")  # type: ignore
