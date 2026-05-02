from ai_agents.state import AgentState
from ai_agents.orchestrator import AgentOrchestrator

# Agents
from ai_agents.agents.resume_agent import ResumeAgent
from ai_agents.agents.job_agent import JobAgent
from ai_agents.agents.advisor_agent import AdvisorAgent
from ai_agents.agents.strategy_agent import StrategyAgent

# 🔥 IMPORT MEMORY FIRST (IMPORTANT)
from backend.memory_utils import add_memory_entry


def run_multi_agent_system(resume_text: str) -> AgentState:

    # 1. INITIALIZE STATE
    state = AgentState()
    state.resume_text = resume_text
    state.add_log("📄 Resume received")

    # 2. PIPELINE
    orchestrator = AgentOrchestrator([
        ResumeAgent(),
        JobAgent(),
        AdvisorAgent(),
        StrategyAgent()
    ])

    # 3. RUN SYSTEM
    final_state = orchestrator.run(state)

    # 4. STORE MEMORY
    add_memory_entry({
        "skills": final_state.extracted_skills,
        "top_jobs": [
            job.get("title") for job in final_state.top_jobs
        ],
        "feedback": final_state.feedback
    })

    return final_state