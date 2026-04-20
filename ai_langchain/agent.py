from langchain.agents import initialize_agent, AgentType
from ai_langchain.utils.llm import get_llm
from tools.langchain_tools import get_tools
from ai_langchain.chains.reasoning_chain import get_reasoning_chain


def get_main_agent():

    llm = get_llm()
    tools = get_tools()

    base_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    reasoning_chain = get_reasoning_chain()

    return base_agent, reasoning_chain
