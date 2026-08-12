import os
import json
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from ReUseMatch/.env unless running pytest
if "pytest" not in sys.modules and "pytest" not in sys.argv[0]:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dotenv_path = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_path=dotenv_path)



class MissingAPIKeyError(Exception):
    """Exception raised when neither OpenAI nor Gemini API keys are available."""
    pass

class LLMGenerationError(Exception):
    """Exception raised when LLM generation fails or returns malformed data."""
    pass

class SharedLLM:
    """
    Shared LLM interface wrapper for all agents.
    Communicates via REST requests to either OpenAI or Gemini.
    """
    def __init__(self, model_name: str = None):
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.gemini_key = os.environ.get("GEMINI_API_KEY")

        # Determine provider and model
        if self.openai_key:
            self.provider = "openai"
            self.model_name = model_name or os.environ.get("DEFAULT_AGENT_MODEL", "gpt-4o-mini")
        elif self.gemini_key:
            self.provider = "gemini"
            self.model_name = model_name or os.environ.get("DEFAULT_AGENT_MODEL", "gemini-1.5-flash")
        else:
            self.provider = "mock"
            self.model_name = "mock"

    def generate(self, prompt: str, require_json: bool = False, **kwargs) -> str:
        """
        Generates text using the available LLM provider.
        Raises MissingAPIKeyError if no key is configured.
        Raises LLMGenerationError if API fails or times out.
        """
        if self.provider == "mock":
            raise MissingAPIKeyError("No API keys found for OpenAI or Gemini in environment variables.")

        if self.provider == "openai":
            return self._call_openai(prompt, require_json, **kwargs)
        elif self.provider == "gemini":
            return self._call_gemini(prompt, require_json, **kwargs)

        raise LLMGenerationError("Invalid LLM provider configured.")

    def _call_openai(self, prompt: str, require_json: bool, **kwargs) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}"
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant that returns structured responses."},
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.1)
        }

        if require_json:
            payload["response_format"] = {"type": "json_object"}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            res_data = response.json()
            return res_data["choices"][0]["message"]["content"]
        except Exception as e:
            raise LLMGenerationError(f"OpenAI API call failed: {e}")

    def _call_gemini(self, prompt: str, require_json: bool, **kwargs) -> str:
        # If model name doesn't contain a slash, use models/ prefix
        model_path = self.model_name
        if "/" not in model_path:
            model_path = f"models/{model_path}"

        url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={self.gemini_key}"
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.1)
            }
        }

        if require_json:
            payload["generationConfig"]["responseMimeType"] = "application/json"

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            res_data = response.json()

            # Extract content from Gemini response structure
            candidates = res_data.get("candidates", [])
            if not candidates:
                raise LLMGenerationError("No candidates returned in Gemini response.")

            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                raise LLMGenerationError("No text parts returned in Gemini response.")

            return parts[0].get("text", "")
        except Exception as e:
            raise LLMGenerationError(f"Gemini API call failed: {e}")
