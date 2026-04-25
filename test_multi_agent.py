from smart_agent import run_multi_agent_system

resume_text = "I am a computer science student skilled in Python, FastAPI, and AI."

result = run_multi_agent_system(resume_text)

print("\nFINAL OUTPUT:\n")
print(result.final_answer)

print("\nLOGS:\n")
for log in result.logs:
    print(log)
