from ai_agents.state import AgentState
from ai_agents.agents.decision_agent import DecisionAgent


class AgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents

    def run(self, state: AgentState):

        state.add_log("🚀 Starting intelligent multi-agent system")

        while state.iteration_count < state.max_iterations:

            state.add_log(f"🔁 Iteration {state.iteration_count + 1}")

            # RUN MAIN AGENTS
            for agent in self.agents:
                state = agent.run(state)

            # DECISION AGENT
            decision_agent = DecisionAgent()
            state = decision_agent.run(state)

            # DECISION: SHOULD WE STOP?
            decision = state.feedback.get("decision", "retry")

            if decision == "accept":
                state.add_log("✅ Decision accepted → stopping iterations")
                break

            # IMPROVEMENT STEP (SMART RETRY)
            state.add_log("⚠️ Improving system for next iteration")

            # 🔥 Smarter refinement strategy
            if state.extracted_skills:
                state.add_log("🔧 Refining skills for better matching")

                state.extracted_skills = [
                    skill.strip().lower()
                    for skill in state.extracted_skills
                    if len(skill.strip()) > 3
                ][:5]

            # INCREMENT ITERATION
            state.iteration_count += 1

        state.add_log("✅ Intelligent pipeline completed")

        return state