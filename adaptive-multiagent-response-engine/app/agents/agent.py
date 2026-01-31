from app.llm.flan import FlanClient
from app.llm.prompts import (
    AGENT_TURN_DECISION_PROMPT,
    RESPONSE_STRATEGY_PROMPT,
    RESPONSE_GENERATION_PROMPT
)


class Agent:
    def __init__(self, name: str, flan_client: FlanClient):
        self.name = name
        self.flan_client = flan_client

    def decide_to_speak(self, context: str, intent: str) -> bool:
        prompt = AGENT_TURN_DECISION_PROMPT.format(
            agent_name=self.name,
            context=context,
            intent=intent
        )
        response = self.flan_client.generate(prompt, max_new_tokens=8, temperature=0.1)
        decision = response.strip().upper()
        return "SPEAK" in decision

    def select_strategy(self, context: str, intent: str) -> str:
        prompt = RESPONSE_STRATEGY_PROMPT.format(
            context=context,
            intent=intent
        )
        response = self.flan_client.generate(prompt, max_new_tokens=16, temperature=0.1)
        strategy = response.strip().upper()

        valid_strategies = [
            "CLARIFY", "PROBE_DETAILS", "PROBE_EMOTION",
            "CHALLENGE_ASSUMPTION", "REQUEST_EXAMPLE",
            "SUMMARIZE_CONFIRM", "FOLLOW_UP_QUESTION"
        ]

        for valid in valid_strategies:
            if valid in strategy:
                return valid

        return "FOLLOW_UP_QUESTION"

    def generate_response(self, context: str, intent: str, strategy: str) -> str:
        prompt = RESPONSE_GENERATION_PROMPT.format(
            context=context,
            intent=intent,
            strategy=strategy
        )
        response = self.flan_client.generate(prompt, max_new_tokens=50, temperature=0.3)
        return response.strip()
