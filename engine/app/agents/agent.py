from app.llm.prompts import RESPONSE_GENERATION_PROMPT


class Agent:
    def __init__(self, name: str, flan_client):
        self.name = name
        self.flan_client = flan_client

    def select_strategy(self, context: str, intent: str) -> str:
        strategy_map = {
            "INFORMATION": "PROBE_DETAILS",
            "EMOTIONAL_EXPRESSION": "PROBE_EMOTION",
            "REQUEST_REPEAT": "CLARIFY",
            "REQUEST_CLARIFICATION": "CLARIFY",
            "DEFENSIVE": "PROBE_EMOTION",
            "ELABORATION": "REQUEST_EXAMPLE",
            "QUESTION": "CLARIFY"
        }
        
        return strategy_map.get(intent, "PROBE_DETAILS")

    def generate_response(self, context: str, intent: str, strategy: str, language: str = "English") -> str:
        strategy_descriptions = {
            "CLARIFY": "Ask for clarification to understand better",
            "PROBE_DETAILS": "Ask about specific details they mentioned",
            "PROBE_EMOTION": "Explore their feelings and emotions",
            "CHALLENGE_ASSUMPTION": "Gently question their assumptions",
            "REQUEST_EXAMPLE": "Ask for a concrete example",
            "SUMMARIZE_CONFIRM": "Confirm your understanding",
            "FOLLOW_UP_QUESTION": "Follow up on what was just said"
        }
        
        strategy_desc = strategy_descriptions.get(strategy, "Ask a thoughtful question")
        
        try:
            prompt = RESPONSE_GENERATION_PROMPT.format(
                context=context,
                strategy=strategy_desc,
                language=language
            )
            response = self.flan_client.generate(prompt, max_new_tokens=40, temperature=0.9)
            
            response = response.strip()
            if not response:
                return "Can you tell me more about that?"
            
            if not response.endswith('?'):
                question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'can', 'could', 'would', 'do', 'does', 'did', 'is', 'are', 'was', 'were']
                first_word = response.split()[0].lower() if response.split() else ''
                if first_word in question_words:
                    response += '?'
            
            return response
        except Exception as e:
            print(f"\n⚠ Error in generate_response: {e}")
            return "How does that make you feel?"
