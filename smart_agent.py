from ai_agents.state import AgentState
from ai_agents.orchestrator import AgentOrchestrator

# Import REAL agents (Day 51 structure)
from ai_agents.agents.resume_agent import ResumeAgent
from ai_agents.agents.job_agent import JobAgent
from ai_agents.agents.advisor_agent import AdvisorAgent
from ai_agents.agents.strategy_agent import StrategyAgent


def run_multi_agent_system(resume_text: str) -> AgentState:
    """
    Main entry point for the AI Career Intelligence System.

    Flow:
    Resume → Job → (Advisor OR Strategy)
    """

    # -------------------------
    # 1. INITIALIZE STATE
    # -------------------------
    state = AgentState()
    state.resume_text = resume_text
    state.add_log("📄 Resume received")

    # -------------------------
    # 2. CREATE AGENT PIPELINE
    # -------------------------
    orchestrator = AgentOrchestrator([
        ResumeAgent(),
        JobAgent(),
        AdvisorAgent(),
        StrategyAgent()
    ])

    # -------------------------
    # 3. RUN SYSTEM
    # -------------------------
    final_state = orchestrator.run(state)

    return final_state