from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class AgentState:
    resume_text: Optional[str] = None

    extracted_skills: List[str] = field(default_factory=list)
    jobs: List[Dict[str, Any]] = field(default_factory=list)
    top_jobs: List[Dict[str, Any]] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)
    final_answer: Optional[str] = None

    has_jobs: bool = False
    needs_strategy: bool = False

    logs: List[str] = field(default_factory=list)

    # 🔥 NEW
    messages: List[Dict[str, str]] = field(default_factory=list)

    def add_log(self, message: str):
        print(message)
        self.logs.append(message)

    # 🔥 NEW
    def add_message(self, sender: str, receiver: str, content: str):
        msg = {
            "from": sender,
            "to": receiver,
            "content": content
        }
        self.messages.append(msg)
        self.logs.append(f"[MESSAGE] {sender} → {receiver}: {content}")

    # Feedback system
    feedback: dict = field(default_factory=dict)

    # Iteration control
    iteration_count: int = 0
    max_iterations: int = 2