from langchain.chains import LLMChain
from ai_langchain.utils.llm import get_llm
from ai_langchain.prompts.reasoning_prompt import reasoning_prompt

def get_reasoning_chain():
    llm = get_llm()

    return LLMChain(
        llm=llm,
        prompt=reasoning_prompt,
        verbose=True
    )