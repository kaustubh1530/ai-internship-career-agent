def run_smart_agent(user_input):

    from ai_langchain.agent import get_main_agent

    agent, reasoning_chain = get_main_agent()

    # Step 1: Reasoning
    reasoning = reasoning_chain.run(input=user_input)

    print("\n--- REASONING ---\n")
    print(reasoning)

    # Step 2: Tool execution
    result = agent.run(user_input)

    return result