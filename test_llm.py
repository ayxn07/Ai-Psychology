"""
Quick test script to verify LLM setup is working correctly.
Run this before running the full simulation.
"""

import sys
sys.path.insert(0, 'adaptive-multiagent-response-engine')

from app.config import Config
from app.llm.llm_manager import LLMManager

def test_llm():
    print("=" * 60)
    print("Testing LLM Setup")
    print("=" * 60)
    print()
    
    # Initialize
    config = Config()
    print()
    
    print("Initializing LLM Manager...")
    llm = LLMManager(config)
    print(f"✓ Active LLM: {llm.get_client_name()}")
    print()
    
    # Test prompt
    test_context = """THERAPY TRAINING SESSION:
(PRIMARY = Patient, Agents = Student Therapists)

PATIENT: I've been feeling really anxious lately
"""
    
    test_prompt = f"""You are a student therapist in a training session. Your role is to ask ONE brief therapeutic question.

{test_context}

Your learning focus: Explore their feelings and emotions

Based on what you just read, ask ONE natural, empathetic question that:
- Shows you're listening carefully
- Helps understand the patient better
- Is brief (under 15 words)
- Sounds conversational and genuine

Just write the question, nothing else:"""
    
    print("Testing question generation...")
    print("-" * 60)
    print("Context: Patient said 'I've been feeling really anxious lately'")
    print()
    
    try:
        response = llm.generate(test_prompt, max_new_tokens=40, temperature=0.7)
        print(f"Student Question: {response}")
        print()
        
        # Quality check
        if len(response) < 10:
            print("⚠ WARNING: Response too short")
        elif len(response.split()) > 20:
            print("⚠ WARNING: Response too long")
        elif not any(word in response.lower() for word in ['?', 'what', 'how', 'why', 'when', 'can', 'could', 'would', 'do', 'does']):
            print("⚠ WARNING: Doesn't look like a question")
        else:
            print("✓ Response looks good!")
        
        print()
        print("=" * 60)
        print("LLM Test Complete")
        print("=" * 60)
        print()
        
        if llm.get_client_name() == "FLAN-T5":
            print("⚠ WARNING: You're using FLAN-T5 (poor quality)")
            print()
            print("For better results:")
            print("  Set OPENROUTER_API_KEY environment variable")
            print("  Get key from: https://openrouter.ai/keys")
            print()
        else:
            print("✓ Setup looks good! Ready to run the simulation.")
            print()
            print("Run: python -m app.main")
            print()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        print("Troubleshooting:")
        print("  - Check your OpenRouter API key")
        print("  - Get key from: https://openrouter.ai/keys")
        print("  - Set: $env:OPENROUTER_API_KEY='sk-or-v1-...'")
        print()

if __name__ == "__main__":
    test_llm()
