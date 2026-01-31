# 🧠 Therapy Training Simulation

AI-powered therapy training where student therapists learn to ask therapeutic questions. You play the patient, AI students practice questioning skills.

## 🚀 Quick Start

### 1. Get OpenRouter API Key

Get free key: https://openrouter.ai/keys

### 2. Set API Key

Create a `.env` file in the `adaptive-multiagent-response-engine` folder:

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 3. Install & Run

```bash
cd adaptive-multiagent-response-engine
pip install -r requirements.txt
python -m app.main
```

### 4. Speak as a Patient

```
[PATIENT]: I've been feeling really anxious lately
[STUDENT 1]: What's been making you feel anxious?
[PATIENT]: Work has been really stressful
[STUDENT 2]: Can you tell me more about what's stressful at work?
```

## 🎯 Available Models

Edit `app/config.py` to change model:

```python
# Best quality (recommended)
openrouter_model: str = "anthropic/claude-3.5-sonnet"

# Other options:
# openrouter_model: str = "openai/gpt-4-turbo"
# openrouter_model: str = "openai/gpt-3.5-turbo"  # Fastest, cheapest
# openrouter_model: str = "meta-llama/llama-3.1-70b-instruct"  # Free
# openrouter_model: str = "google/gemini-pro-1.5"
```

See all models: https://openrouter.ai/models

## ⚙️ Configuration

Edit `app/config.py`:

```python
num_agents: int = 3  # Number of student therapists
use_intent_classification: bool = False  # Set True for more sophisticated responses
silence_threshold: float = 200.0  # Audio sensitivity (lower = more sensitive)
```

## 💰 Cost

- **Claude 3.5 Sonnet**: ~$0.003 per interaction
- **GPT-4 Turbo**: ~$0.01 per interaction  
- **GPT-3.5 Turbo**: ~$0.0005 per interaction
- **Llama 3.1 70B**: Free (rate limited)

$5 credit = hundreds of interactions.

## 🔧 Troubleshooting

**Gibberish responses?**

Make sure `.env` file exists in `adaptive-multiagent-response-engine` folder with:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Audio not detected?**
- Check microphone permissions
- Adjust `silence_threshold` in config.py (try 150.0)

**Too slow?**
- Set `use_intent_classification = False` in config.py
- Use faster model: `openai/gpt-3.5-turbo`

---

**Get started**: Create `.env` file with your key and run `python -m app.main`
