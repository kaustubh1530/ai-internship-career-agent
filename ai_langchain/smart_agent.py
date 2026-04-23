def run_smart_agent(user_input):

    from ai_langchain.agent import get_main_agent

    agent = get_main_agent()

    result = agent.run(user_input)

    return result