from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class AgentState:
    """
    Shared memory across all agents.
    Think of this as the brain storage.
    """

    # INPUT
    resume_text: Optional[str] = None

    # INTERMEDIATE
    extracted_skills: List[str] = field(default_factory=list)
    jobs: List[Dict[str, Any]] = field(default_factory=list)

    # OUTPUT
    recommendations: List[str] = field(default_factory=list)
    final_answer: Optional[str] = None

    # DEBUG / TRACE (VERY IMPORTANT)
    logs: List[str] = field(default_factory=list)

    def add_log(self, message: str):
        print(message)  # helpful for dev
        self.logs.append(message)