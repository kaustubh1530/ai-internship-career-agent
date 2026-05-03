from ai_agents.base import BaseAgent
from ai_agents.state import AgentState


class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__("DecisionAgent")

    def run(self, state: AgentState) -> AgentState:

        # CHECK JOB QUALITY
        num_jobs = len(state.top_jobs)

        if num_jobs >= 3:
            job_quality = "good"
        elif num_jobs > 0:
            job_quality = "average"
        else:
            job_quality = "bad"

        # CHECK RECOMMENDATION QUALITY
        if state.final_answer and len(state.final_answer) > 200:
            recommendation_quality = "good"
        else:
            recommendation_quality = "weak"

        # FINAL DECISION
        decision = "accept"

        if job_quality == "bad":
            decision = "retry"

        if recommendation_quality == "weak":
            decision = "retry"

        # STORE IN STATE
        state.feedback["decision"] = decision
        state.feedback["job_quality"] = job_quality
        state.feedback["recommendation_quality"] = recommendation_quality

        # LOGGING
        self.log(
            state,
            f"Decision: {decision} | Jobs: {job_quality} | Recommendations: {recommendation_quality}"
        )

        return state