from ai_agents.state import AgentState
from ai_agents.orchestrator import AgentOrchestrator

from ai_langchain.chains.resume_chain import get_resume_chain
from ai_langchain.chains.job_chain import get_job_chain
from ai_langchain.chains.advisor_chain import get_advisor_chain


def run_multi_agent_system(resume_text: str):

    # -------------------
    # STATE
    # -------------------
    state = AgentState()
    state.resume_text = resume_text
    state.add_log("📄 Resume received")

    # -------------------
    # RESUME AGENT
    # -------------------
    class ResumeAgent:
        name = "ResumeAgent"

        def run(self, state):

            chain = get_resume_chain()
            result = chain.run(state.resume_text)

            state.extracted_skills = result.get("skills", [])
            state.add_log(f"Skills extracted: {state.extracted_skills}")

            return state

    # -------------------
    # JOB AGENT
    # -------------------
    class JobAgent:
        name = "JobAgent"

        def run(self, state):

            chain = get_job_chain()
            result = chain.run(state.extracted_skills)

            state.jobs = result.get("jobs", [])
            state.add_log(f"Jobs found: {len(state.jobs)}")

            return state

    # -------------------
    # ADVISOR AGENT
    # -------------------
    class AdvisorAgent:
        name = "AdvisorAgent"

        def run(self, state):

            chain = get_advisor_chain()
            result = chain.run(
                state.resume_text,
                state.jobs
            )

            state.recommendations = result.get("recommendations", [])
            state.final_answer = result.get("summary", "")

            state.add_log("Final recommendations generated")

            return state

    # -------------------
    # ORCHESTRATOR
    # -------------------
    orchestrator = AgentOrchestrator([
        ResumeAgent(),
        JobAgent(),
        AdvisorAgent()
    ])

    final_state = orchestrator.run(state)

    return final_state
