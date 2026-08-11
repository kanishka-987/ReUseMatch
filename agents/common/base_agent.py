from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in ReUseMatch.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Main execution method for the agent.
        Must be implemented by subclasses.
        """
        pass
