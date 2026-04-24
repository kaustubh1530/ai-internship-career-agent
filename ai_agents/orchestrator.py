from ai_agents.state import AgentState


class AgentOrchestrator:
    """
    Controls execution of all agents.
    """

    def __init__(self, agents: list):
        self.agents = agents

    def run(self, state: AgentState) -> AgentState:
        state.add_log("🚀 Starting multi-agent pipeline")

        for agent in self.agents:
            state.add_log(f"➡️ Running {agent.name}")
            state = agent.run(state)

        state.add_log("✅ Pipeline completed")
        return state