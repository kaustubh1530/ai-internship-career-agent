from langchain_core.output_parsers import StrOutputParser
from ai_langchain.utils.llm import get_llm
from ai_langchain.prompts.advisor_prompt import advisor_prompt


def get_advisor_chain():
    llm = get_llm()

    chain = advisor_prompt | llm | StrOutputParser()

    return chain
