from ai_langchain.smart_agent import run_smart_agent

response = run_smart_agent(
    "Find me backend jobs and tell me if I should apply"
)

print("\n--- FINAL ANSWER ---\n")
print(response)