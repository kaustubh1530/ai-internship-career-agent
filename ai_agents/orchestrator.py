from ai_agents.state import AgentState


class AgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents

    def run(self, state):

        state.add_log("🚀 Starting intelligent multi-agent system")

        while state.iteration_count < state.max_iterations:

            state.add_log(f"🔁 Iteration {state.iteration_count + 1}")

            # -------------------------
            # RUN MAIN AGENTS
            # -------------------------
            for agent in self.agents:
                state = agent.run(state)

            # -------------------------
            # RUN FEEDBACK AGENT
            # -------------------------
            from ai_agents.agents.feedback_agent import FeedbackAgent

            feedback_agent = FeedbackAgent()
            state = feedback_agent.run(state)

            # -------------------------
            # DECISION: SHOULD WE STOP?
            # -------------------------
            jobs_quality = state.feedback.get("jobs_quality", "unknown")

            if jobs_quality == "good":
                state.add_log("✅ Jobs are good → stopping iterations")
                break

            # -------------------------
            # IMPROVEMENT STEP
            # -------------------------
            state.add_log("⚠️ Improving system for next iteration")

            # Simple refinement strategy
            if state.extracted_skills:
                state.extracted_skills = state.extracted_skills[:3]

            # -------------------------
            # INCREMENT ITERATION
            # -------------------------
            state.iteration_count += 1

        state.add_log("✅ Intelligent pipeline completed")

        return state