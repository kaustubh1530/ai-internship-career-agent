from langchain.agents import initialize_agent, AgentType
from ai_langchain.utils.llm import get_llm
from tools.job_tools import get_tools


def get_main_agent():

    llm = get_llm()
    tools = get_tools()

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        max_iterations=3,   # 🔥 LIMIT LOOP
        early_stopping_method="generate"
    )

    return agent
