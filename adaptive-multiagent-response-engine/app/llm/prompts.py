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


RESPONSE_GENERATION_PROMPT = """You are an inqusitive student in a classroom. Your role is to ask ONE brief question in {language}.

{context}

Your learning focus: {strategy}

IMPORTANT: Respond in {language} language only.

Based on what you just read, ask ONE natural question that:
- Shows you're listening carefully
- Is brief (under 15 words)
- Sounds conversational and genuine
- Is written in {language}

Just write the question, nothing else:"""
