from ai_langchain.chains.resume_chain import get_resume_chain

resume_text = """
Python developer with experience in FastAPI, SQL, and AI projects.
Built job matching systems and RAG pipelines.
"""

chain = get_resume_chain()

result = chain.invoke({"resume_text": resume_text})

print(result.content)