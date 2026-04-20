from langchain.chains import LLMChain
from ai_langchain.utils.llm import get_llm
from ai_langchain.prompts.resume_prompt import resume_prompt
from ai_langchain.utils.memory import get_memory

llm = get_llm()
memory = get_memory()

# CREATE ONCE
resume_chain = LLMChain(
    llm=llm,
    prompt=resume_prompt,
    memory=memory,
    verbose=True
)

def get_resume_chain():
    return resume_chain
