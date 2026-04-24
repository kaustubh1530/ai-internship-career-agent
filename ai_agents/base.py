from abc import ABC, abstractmethod
from ai_agents.state import AgentState


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state: AgentState) -> AgentState:
        pass

    def log(self, state: AgentState, message: str):
        state.add_log(f"[{self.name}] {message}")