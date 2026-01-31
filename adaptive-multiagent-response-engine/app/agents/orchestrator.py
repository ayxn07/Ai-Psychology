from typing import List, Optional, Tuple
from app.agents.agent import Agent
from app.llm.flan import FlanClient
from app.llm.prompts import INTENT_CLASSIFICATION_PROMPT
from app.memory.store import ConversationStore
from app.memory.threads import ThreadInferencer
from app.utils.similarity import SimilarityChecker
from app.config import Config


class Orchestrator:
    def __init__(
        self,
        agents: List[Agent],
        flan_client: FlanClient,
        memory: ConversationStore,
        thread_inferencer: ThreadInferencer,
        similarity_checker: SimilarityChecker,
        config: Config
    ):
        self.agents = agents
        self.flan_client = flan_client
        self.memory = memory
        self.thread_inferencer = thread_inferencer
        self.similarity_checker = similarity_checker
        self.config = config
        self.round_robin_index = 0

    def classify_intent(self, text: str) -> str:
        prompt = INTENT_CLASSIFICATION_PROMPT.format(text=text)
        response = self.flan_client.generate(prompt, max_new_tokens=16, temperature=0.1)
        intent = response.strip().upper()

        valid_intents = [
            "INFORMATION", "EMOTIONAL_EXPRESSION", "REQUEST_REPEAT",
            "REQUEST_CLARIFICATION", "DEFENSIVE", "ELABORATION", "QUESTION"
        ]

        for valid in valid_intents:
            if valid in intent:
                return valid

        return "INFORMATION"

    def select_speaking_agent(self, context: str, intent: str) -> Agent:
        speak_agents = []
        wait_agents = []
        for agent in self.agents:
            if agent.decide_to_speak(context, intent):
                speak_agents.append(agent)
            else:
                wait_agents.append(agent)
        if speak_agents:
            # If last agent spoke and wants to follow up, let them go again
            last_agent_name = self.memory.last_agent
            for agent in speak_agents:
                if agent.name == last_agent_name:
                    return agent
            for i, agent in enumerate(self.agents):
                if agent in speak_agents:
                    idx = (self.round_robin_index + i) % len(self.agents)
                    if self.agents[idx] in speak_agents:
                        self.round_robin_index = (idx + 1) % len(self.agents)
                        return self.agents[idx]
            self.round_robin_index = (self.round_robin_index + 1) % len(self.agents)
            return speak_agents[0]
        selected = self.agents[self.round_robin_index]
        self.round_robin_index = (self.round_robin_index + 1) % len(self.agents)
        return selected

    def check_and_regenerate(
        self,
        agent: Agent,
        response: str,
        context: str,
        intent: str,
        strategy: str
    ) -> str:
        recent_outputs = self.memory.get_recent_agent_outputs()

        if self.similarity_checker.is_too_similar(response, recent_outputs):
            new_response = agent.generate_response(context, intent, strategy)
            return new_response

        return response

    def process_turn(self, primary_text: str) -> Tuple[str, str, str]:
        intent = self.classify_intent(primary_text)
        self.memory.add_primary_turn(primary_text, intent)
        self.thread_inferencer.update_if_needed(self.memory)
        context = self.memory.build_context(self.config.max_context_turns)
        selected_agent = self.select_speaking_agent(context, intent)
        strategy = selected_agent.select_strategy(context, intent)
        response = selected_agent.generate_response(context, intent, strategy)
        response = self.check_and_regenerate(selected_agent, response, context, intent, strategy)
        self.memory.add_agent_turn(selected_agent.name, response, strategy)
        # If strategy is FOLLOW_UP_QUESTION, allow same agent to speak again
        if strategy == "FOLLOW_UP_QUESTION":
            context = self.memory.build_context(self.config.max_context_turns)
            followup_agent = selected_agent
            followup_strategy = followup_agent.select_strategy(context, intent)
            followup_response = followup_agent.generate_response(context, intent, followup_strategy)
            followup_response = self.check_and_regenerate(followup_agent, followup_response, context, intent, followup_strategy)
            self.memory.add_agent_turn(followup_agent.name, followup_response, followup_strategy)
            return followup_agent.name, followup_strategy, followup_response
        return selected_agent.name, strategy, response

    def run_interaction(self, primary_text: str) -> None:
        agent_name, strategy, response = self.process_turn(primary_text)
        print(f"\n[{agent_name}] ({strategy}): {response}\n")
