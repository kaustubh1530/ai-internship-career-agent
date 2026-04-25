from ai_agents.state import AgentState


class AgentOrchestrator:
    """
    Controls execution of all agents with decision logic.
    """

    def __init__(self, agents: list):
        self.agents = agents

    def run(self, state: AgentState) -> AgentState:
        state.add_log("🚀 Starting intelligent multi-agent system")

        # Step 1: Resume Agent
        resume_agent = self.agents[0]
        state = resume_agent.run(state)

        # Step 2: Job Agent
        job_agent = self.agents[1]
        state = job_agent.run(state)

        # Step 3: Decision
        if state.has_jobs:
            advisor_agent = self.agents[2]
            state.add_log("📊 Jobs found → using AdvisorAgent")
            state = advisor_agent.run(state)
        else:
            strategy_agent = self.agents[3]
            state.add_log("📉 No jobs → using StrategyAgent")
            state = strategy_agent.run(state)

        state.add_log("✅ Intelligent pipeline completed")
        return state