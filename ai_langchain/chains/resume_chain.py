from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from ai_langchain.utils.llm import get_llm
from ai_langchain.prompts.resume_prompt import resume_prompt


def get_resume_chain():
    llm = get_llm()

    chain = resume_prompt | llm | StrOutputParser()

    return chain
