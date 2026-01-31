INTENT_CLASSIFICATION_PROMPT = """Classify what the patient just said into ONE category:

Patient said: "{text}"

Categories:
- INFORMATION: Sharing facts or information
- EMOTIONAL_EXPRESSION: Expressing feelings
- REQUEST_REPEAT: Asking to repeat something
- REQUEST_CLARIFICATION: Asking for clarification
- DEFENSIVE: Being defensive
- ELABORATION: Adding more details
- QUESTION: Asking a question

Answer with just the category name:"""


RESPONSE_GENERATION_PROMPT = """You are a student therapist in a training session. Your role is to ask ONE brief therapeutic question.

{context}

Your learning focus: {strategy}

Based on what you just read, ask ONE natural, empathetic question that:
- Shows you're listening carefully
- Helps understand the patient better
- Is brief (under 15 words)
- Sounds conversational and genuine

Just write the question, nothing else:"""
