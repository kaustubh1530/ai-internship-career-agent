from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class AgentState:
    """
    Shared memory across all agents.
    Think of this as the brain storage of the system.
    """

    # -------------------------
    # INPUT
    # -------------------------
    resume_text: Optional[str] = None

    # -------------------------
    # INTERMEDIATE (PROCESSING)
    # -------------------------
    extracted_skills: List[str] = field(default_factory=list)

    # Raw jobs fetched
    jobs: List[Dict[str, Any]] = field(default_factory=list)

    # Scored jobs (job + score)
    match_scores: List[Dict[str, Any]] = field(default_factory=list)

    # Top filtered jobs (best matches)
    top_jobs: List[Dict[str, Any]] = field(default_factory=list)

    # -------------------------
    # OUTPUT
    # -------------------------
    recommendations: List[str] = field(default_factory=list)
    final_answer: Optional[str] = None

    # -------------------------
    # DECISION CONTROL (VERY IMPORTANT)
    # -------------------------
    has_jobs: bool = False
    needs_strategy: bool = False

    # -------------------------
    # DEBUG / TRACE
    # -------------------------
    logs: List[str] = field(default_factory=list)

    def add_log(self, message: str):
        print(message)  # helpful during development
        self.logs.append(message)