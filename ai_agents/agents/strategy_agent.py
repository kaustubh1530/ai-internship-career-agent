from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.utils.llm import get_llm


class StrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__("StrategyAgent")
        self.llm = get_llm()

    def run(self, state: AgentState) -> AgentState:

        # READ MESSAGES
        for msg in state.messages:
            if msg.get("to") == self.name:
                self.log(state, f"Received message: {msg.get('content')}")

        prompt = f"""
        The user has the following skills:
        {state.extracted_skills}

        No relevant jobs were found.

        Provide:
        1. Skills they should improve
        2. Career strategy for next 3 months
        3. How to become job-ready
        """

        # ✅ NOW THIS WILL WORK
        response = self.llm.invoke(prompt)

        state.final_answer = response.content

        self.log(state, "Generated long-term strategy")

        return state