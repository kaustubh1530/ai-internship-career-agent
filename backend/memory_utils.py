import json
import os

MEMORY_FILE = "backend/memory_store.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"history": []}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_memory_entry(entry):
    memory = load_memory()
    memory["history"].append(entry)
    save_memory(memory)


def get_recent_memory(limit=3):
    memory = load_memory()
    return memory["history"][-limit:]