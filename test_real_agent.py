from ai_langchain.agent import get_main_agent
from ai_langchain.context import set_user_skills

# Simulate resume upload
set_user_skills(["Python", "FastAPI", "SQL"])

agent = get_main_agent()

response = agent.run(
    "Find backend jobs and tell me if I should apply"
)

print(response)