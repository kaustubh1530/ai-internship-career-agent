from langchain_openai import ChatOpenAI


def get_llm():
    return ChatOpenAI(
        temperature=0.3,
        model="gpt-4o-mini"  # or "gpt-3.5-turbo"
    )