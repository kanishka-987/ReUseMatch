import pytest
from pydantic import ValidationError
from agents.logistics_agent.agent import LogisticsAgent
from agents.logistics_agent.schemas import LogisticsResult

def test_logistics_agent_valid_locations():
    """
    Verify logistics evaluation with valid donor and recipient locations.
    Checks output schema validation, distance bounds, and transport mode logic.
    """
    agent = LogisticsAgent()
    result = agent.run(donor_location="123 Hope Lane", recipient_location="456 Charity Way")
    
    # Assert validation matches LogisticsResult schema structure
    assert result["origin"] == "123 Hope Lane"
    assert result["destination"] == "456 Charity Way"
    assert result["distance_km"] >= 0.0
    assert result["estimated_cost_usd"] >= 0.0
    assert result["recommended_mode"] in ["Local Pickup Courier", "Standard Shipping"]
    assert result["route_status"] == "optimal"

def test_logistics_agent_missing_donor():
    """
    Verify that missing donor location raises ValidationError.
    """
    agent = LogisticsAgent()
    with pytest.raises(ValidationError):
        agent.run(donor_location=None, recipient_location="456 Charity Way")  # type: ignore

def test_logistics_agent_missing_recipient():
    """
    Verify that missing recipient location raises ValidationError.
    """
    agent = LogisticsAgent()
    with pytest.raises(ValidationError):
        agent.run(donor_location="123 Hope Lane", recipient_location=None)  # type: ignore

def test_logistics_agent_empty_donor():
    """
    Verify that empty donor location raises ValidationError.
    """
    agent = LogisticsAgent()
    with pytest.raises(ValidationError):
        agent.run(donor_location="", recipient_location="456 Charity Way")

def test_logistics_agent_empty_recipient():
    """
    Verify that empty recipient location raises ValidationError.
    """
    agent = LogisticsAgent()
    with pytest.raises(ValidationError):
        agent.run(donor_location="123 Hope Lane", recipient_location="")

def test_logistics_agent_invalid_input_types():
    """
    Verify that invalid input types raise ValidationError.
    """
    agent = LogisticsAgent()
    with pytest.raises(ValidationError):
        agent.run(donor_location=123, recipient_location="456 Charity Way")  # type: ignore
