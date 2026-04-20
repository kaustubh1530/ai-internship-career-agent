from langchain.agents import initialize_agent, AgentType
from ai_langchain.utils.llm import get_llm
from tools.langchain_tools import get_tools

def get_main_agent():

    llm = get_llm()
    tools = get_tools()

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent
