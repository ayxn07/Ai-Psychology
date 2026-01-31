from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Turn:
    speaker: str
    text: str
    role: str


class ConversationStore:
    def __init__(self, similarity_window: int = 5):
        self.turns: List[Turn] = []
        self.active_threads: List[str] = []
        self.last_agent: Optional[str] = None
        self.last_primary_intent: Optional[str] = None
        self.recent_agent_outputs: List[str] = []
        self.similarity_window = similarity_window

    def add_primary_turn(self, text: str, intent: str) -> None:
        turn = Turn(speaker="PRIMARY", text=text, role="primary")
        self.turns.append(turn)
        self.last_primary_intent = intent

    def add_agent_turn(self, agent_name: str, text: str, strategy: str) -> None:
        turn = Turn(speaker=agent_name, text=text, role="agent")
        self.turns.append(turn)
        self.last_agent = agent_name
        self.recent_agent_outputs.append(text)
        if len(self.recent_agent_outputs) > self.similarity_window:
            self.recent_agent_outputs.pop(0)

    def update_threads(self, threads: List[str]) -> None:
        self.active_threads = threads

    def get_recent_agent_outputs(self) -> List[str]:
        return self.recent_agent_outputs.copy()

    def build_context(self, max_turns: int) -> str:
        recent_turns = self.turns[-max_turns:] if len(self.turns) > max_turns else self.turns

        context_parts = ["THERAPY TRAINING SESSION:"]
        context_parts.append("(PRIMARY = Patient, Agents = Student Therapists)")
        context_parts.append("")
        
        for turn in recent_turns:
            if turn.speaker == "PRIMARY":
                context_parts.append(f"PATIENT: {turn.text}")
            else:
                context_parts.append(f"STUDENT {turn.speaker}: {turn.text}")

        if not recent_turns:
            context_parts.append("(Session just started)")

        return "\n".join(context_parts)

    def get_turn_count(self) -> int:
        return len(self.turns)

    def get_primary_turn_count(self) -> int:
        return sum(1 for turn in self.turns if turn.role == "primary")
