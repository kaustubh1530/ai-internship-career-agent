from ai_agents.base import BaseAgent
from ai_agents.state import AgentState
from ai_langchain.utils.llm import get_llm


class StrategyAgent(BaseAgent):
    def __init__(self):
        super().__init__("StrategyAgent")
        self.llm = get_llm()

    def run(self, state: AgentState) -> AgentState:
        prompt = f"""
        The user has the following skills:
        {state.extracted_skills}

        No relevant jobs were found.

        Provide:
        1. Skills they should improve
        2. Career strategy for next 3 months
        3. How to become job-ready
        """

        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",  # or whatever you're using
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        state.final_answer = response.choices[0].message.content

        self.log(state, "Generated long-term strategy (no jobs scenario)")

        return state