"""
Quick test to verify OpenRouter is working
"""
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Check if key is loaded
key = os.getenv("OPENROUTER_API_KEY")
if not key:
    print("❌ OPENROUTER_API_KEY not found in .env file")
    print("Create a .env file with:")
    print("OPENROUTER_API_KEY=sk-or-v1-your-key-here")
    exit(1)

print(f"✓ API key loaded: {key[:20]}...")

# Test OpenRouter client
from app.llm.openrouter_client import OpenRouterClient

print("\nTesting OpenRouter connection...")
client = OpenRouterClient(model="openai/gpt-3.5-turbo")  # Use cheap model for testing

if not client.available:
    print("❌ OpenRouter client not available")
    exit(1)

print("✓ OpenRouter client initialized")

# Test generation
print("\nTesting question generation...")
test_prompt = """You are a student therapist. A patient just said: "I've been feeling anxious."

Ask ONE brief therapeutic question (under 15 words):"""

response = client.generate(test_prompt, max_new_tokens=30, temperature=0.7)
print(f"\nGenerated question: {response}")

if len(response) > 10 and ('?' in response or any(word in response.lower() for word in ['what', 'how', 'why'])):
    print("\n✅ OpenRouter is working correctly!")
    print("\nYou can now run: python -m app.main")
else:
    print("\n⚠ Response seems unusual, but connection works")
