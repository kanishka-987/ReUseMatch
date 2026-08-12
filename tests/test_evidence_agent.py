import pytest
import json
from unittest.mock import MagicMock, patch
from pydantic import ValidationError
from agents.evidence_agent.agent import EvidenceAgent
from agents.evidence_agent.schemas import DeviceInput, EvidenceResult

def test_evidence_agent_mock_fallback_valid_input():
    """
    Verify EvidenceAgent fallback mode behaves correctly for valid input,
    returns the expected output structure with Literal "mock_fallback",
    and ensures confidence is in [0.0, 1.0].
    """
    agent = EvidenceAgent()
    result = agent.run(description="A wooden table", image_url="http://example.com/image.jpg")

    assert result["source"] == "mock_fallback"
    assert "wood" in result["observed_evidence"]
    assert result["functional_claims"] == ["A wooden table"]
    assert "serial_number" in result["missing_information"]
    assert 0.0 <= result["confidence"] <= 1.0

def test_evidence_agent_invalid_input_type():
    """
    Verify description of invalid type raises ValidationError.
    """
    agent = EvidenceAgent()
    with pytest.raises(ValidationError):
        agent.run(description=12345)  # type: ignore

def test_evidence_agent_missing_description():
    """
    Verify missing description raises ValidationError.
    """
    agent = EvidenceAgent()
    with pytest.raises(ValidationError):
        agent.run(description=None)  # type: ignore

def test_evidence_agent_no_hallucinated_evidence():
    """
    Verify that mock-fallback evidence is traceable to input
    and unsupported facts are NOT invented (i.e. empty observed_evidence for unknown items).
    """
    agent = EvidenceAgent()

    # 1. Unknown item input: should not invent evidence
    result_unknown = agent.run(description="Hello world")
    assert result_unknown["source"] == "mock_fallback"
    assert result_unknown["observed_evidence"] == []  # Not invented

    # 2. Known item input: should return evidence traceable to 'table'
    result_table = agent.run(description="I have a broken table")
    assert result_table["source"] == "mock_fallback"
    assert "wood" in result_table["observed_evidence"]  # Traceable to 'table'

def test_evidence_agent_semantic_functional_claims_filtering():
    """
    Verify that unrelated user statements are not classified as functional claims,
    and only statements about condition/functionality are mapped.
    """
    agent = EvidenceAgent()

    # 1. Unrelated statement: should be filtered out
    result_unrelated = agent.run(description="Hello, I am writing from New York.")
    assert result_unrelated["functional_claims"] == []

    # 2. Statement with functional/condition keyword: should be preserved
    result_related = agent.run(description="The table is broken and scratched.")
    assert result_related["functional_claims"] == ["The table is broken and scratched."]

@patch("agents.common.llm.requests.post")
def test_evidence_agent_llm_path_valid(mock_post):
    """
    Successful LLM extraction path matching EvidenceResult layout.
    """
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"}):
        agent = EvidenceAgent()

        mock_response_content = {
            "observed_evidence": ["aluminum", "silver"],
            "user_claims": ["Broken screen but turns on", "Unrelated greeting hello"],
            "missing_information": ["model_number"],
            "confidence_score": 0.95,
            "identified_name": "iPhone 13",
            "category": "Electronics"
        }

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps(mock_response_content)
                }
            }]
        }
        mock_post.return_value = mock_resp

        result = agent.run(description="Broken iPhone 13 screen but turns on")

        assert result["source"] == "llm"
        assert "aluminum" in result["observed_evidence"]
        # Only the related claim is preserved; unrelated greeting is filtered out
        assert result["functional_claims"] == ["Broken screen but turns on"]
        assert result["missing_information"] == ["model_number"]
        assert result["confidence"] == 0.95

@patch("agents.common.llm.requests.post")
def test_evidence_agent_llm_malformed_json_fallback(mock_post):
    """
    Verify that if the LLM returns malformed JSON, the agent gracefully falls back to mock.
    """
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"}):
        agent = EvidenceAgent()

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{
                "message": {
                    "content": "Not a JSON string"
                }
            }]
        }
        mock_post.return_value = mock_resp

        result = agent.run(description="A wooden table")
        assert result["source"] == "mock_fallback"
        assert "wood" in result["observed_evidence"]
