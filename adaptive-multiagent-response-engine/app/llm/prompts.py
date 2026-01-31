INTENT_CLASSIFICATION_PROMPT = """Classify this statement:
{text}

Choose one: INFORMATION, EMOTIONAL_EXPRESSION, REQUEST_REPEAT, REQUEST_CLARIFICATION, DEFENSIVE, ELABORATION, QUESTION

Answer:"""


AGENT_TURN_DECISION_PROMPT = """Should {agent_name} respond now?

Recent conversation:
{context}

Answer SPEAK or WAIT:"""


RESPONSE_STRATEGY_PROMPT = """What should the agent ask about?

{context}

Choose one: CLARIFY, PROBE_DETAILS, PROBE_EMOTION, CHALLENGE_ASSUMPTION, REQUEST_EXAMPLE, SUMMARIZE_CONFIRM, FOLLOW_UP_QUESTION

Answer:"""


RESPONSE_GENERATION_PROMPT = """Conversation:
{context}

Strategy: {strategy}

Generate one short question based on what the primary speaker just said:

Question:"""
