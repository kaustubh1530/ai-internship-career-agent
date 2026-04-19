from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_langchain.utils.llm import get_llm

from ai_langchain.prompts.job_prompt import job_prompt


def get_job_chain():
    llm = get_llm()

    chain = job_prompt | llm | StrOutputParser()

    return chain
