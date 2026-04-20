from ai_langchain.agent import get_main_agent

agent = get_main_agent()

response = agent.run(
    "I know Python and FastAPI. What jobs should I apply for?"
)

print(response)