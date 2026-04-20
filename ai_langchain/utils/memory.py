from langchain.memory import ConversationBufferMemory

# GLOBAL MEMORY (shared)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

def get_memory():
    return memory
