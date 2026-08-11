import os

class SharedLLM:
    """
    Shared LLM interface wrapper for all agents.
    Loads API configurations from environment variables.
    """
    def __init__(self, model_name: str = None):
        self.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.model_name = model_name or os.environ.get("DEFAULT_AGENT_MODEL", "gemini-1.5-flash")

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Placeholder generation call.
        To be implemented when LLM logic is added.
        """
        # Place real integration here later
        return f"Mock response for prompt: {prompt[:30]}..."
