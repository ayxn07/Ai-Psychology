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

## 🔊 Text-to-Speech (Optional)

Add realistic voice output to AI therapist responses using ElevenLabs.

### Setup TTS

**1. Get ElevenLabs API Key**

Sign up at https://elevenlabs.io and get your API key from the profile page.

**2. Configure TTS**

Add to your `.env` file in `adaptive-multiagent-response-engine`:

```
ELEVENLABS_API_KEY=sk_your-elevenlabs-api-key-here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

**3. Choose a Voice**

Browse voices at https://elevenlabs.io/voice-library

Copy the Voice ID and update `ELEVENLABS_VOICE_ID` in your `.env` file.

Default voice: Rachel (21m00Tcm4TlvDq8ikWAM)

### Enable/Disable TTS

Edit `app/config.py`:

```python
enable_tts: bool = True  # Set False to disable voice output
```

TTS is enabled by default when API key is configured. The system automatically falls back to text-only mode if TTS encounters errors.

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

**TTS not working?**
- Verify `ELEVENLABS_API_KEY` is set in `.env` file
- Check API key is valid at https://elevenlabs.io
- Ensure `pygame` is installed: `pip install pygame`
- Check console for TTS error messages
- Set `enable_tts = False` in config.py to disable TTS

**TTS audio quality issues?**
- Try a different voice ID from https://elevenlabs.io/voice-library
- Check your internet connection (TTS requires API calls)
- Verify audio output device is working

**TTS causing delays?**
- Normal: 1-3 seconds for audio generation
- If longer, check network connection
- System continues with text if TTS times out (10s)

---

**Get started**: Create `.env` file with your key and run `python -m app.main`
