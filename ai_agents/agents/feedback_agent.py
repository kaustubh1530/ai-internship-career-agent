from ai_agents.base import BaseAgent
from ai_agents.state import AgentState


class FeedbackAgent(BaseAgent):
    def __init__(self):
        super().__init__("FeedbackAgent")

    def run(self, state: AgentState) -> AgentState:

        feedback = {}

        # CHECK JOB QUALITY
        if not state.top_jobs or len(state.top_jobs) < 3:
            feedback["jobs_quality"] = "low"
            self.log(state, "Feedback: Job quality is LOW")
        else:
            feedback["jobs_quality"] = "good"
            self.log(state, "Feedback: Job quality is GOOD")

        # CHECK SKILLS
        if not state.extracted_skills:
            feedback["skills_quality"] = "low"
            self.log(state, "Feedback: Skills extraction is LOW")
        else:
            feedback["skills_quality"] = "good"
            self.log(state, "Feedback: Skills extraction is GOOD")

        state.feedback = feedback

        return state