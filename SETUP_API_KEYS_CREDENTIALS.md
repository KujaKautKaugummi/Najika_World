# 🔑 API Keys & Credentials Setup Guide

**Purpose:** Configure all necessary API keys and credentials for Najika Backend

---

## 📋 Overview - What Keys Do We Need?

| Service | Purpose | Cost | Priority |
|---------|---------|------|----------|
| **OpenAI API** | Najika's AI Brain (GPT-4) | ~$0.03/1K tokens | 🔥 CRITICAL |
| **Anthropic Claude** | Alternative AI (better conversations) | ~$0.015/1K tokens | ⚠️ Optional |
| **OpenAI Whisper** | Voice-to-Text (Speech Recognition) | ~$0.006/min | 🔥 CRITICAL |
| **ElevenLabs** | Text-to-Speech (Najika Voice) | $5-22/month | ⚠️ Optional |
| **Cloudflare** | Tunnel (Remote Access) | FREE | 🔥 CRITICAL |

---

## 1️⃣ OpenAI API Key Setup (CRITICAL)

### Why?
- Powers Najika's conversations (GPT-4)
- Whisper API for voice transcription
- Most reliable AI service

### Cost?
**Pay-as-you-go:**
- GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
- GPT-3.5-turbo: $0.0005/1K input tokens, $0.0015/1K output tokens
- Whisper: $0.006/minute

**Estimated monthly cost (moderate use):**
- 100 conversations/day: ~$10-30/month
- Voice chat 1hr/day: ~$10/month
- **Total: ~$20-40/month**

### Step 1: Create OpenAI Account

1. Go to: https://platform.openai.com/signup
2. Sign up with email/Google
3. Verify email
4. Add payment method (credit card required)

### Step 2: Set Spending Limit

**Important: Set budget to avoid surprise bills!**

1. Go to: https://platform.openai.com/account/billing/limits
2. Set **Monthly budget limit**: $50 (or your preference)
3. Enable email alerts at 50%, 75%, 90%

### Step 3: Generate API Key

1. Go to: https://platform.openai.com/api-keys
2. Click: **"Create new secret key"**
3. Name: `Najika Backend`
4. Permissions: `All` (or `Read & Write`)
5. **Copy the key immediately!** (You won't see it again)

**Format:** `sk-proj-...` (starts with `sk-`)

**SAVE IT SECURELY!**

### Step 4: Test API Key

```powershell
# Test with curl (Windows)
curl https://api.openai.com/v1/models `
  -H "Authorization: Bearer YOUR_API_KEY_HERE"
```

**Expected:** List of available models (gpt-4, gpt-3.5-turbo, etc.)

---

## 2️⃣ Anthropic Claude API (OPTIONAL)

### Why?
- Alternative to OpenAI (often better for conversations)
- More natural dialogue
- Better context understanding
- Cheaper ($0.015/1K tokens vs $0.03)

### Cost?
- Claude 3.5 Sonnet: $3/M input tokens, $15/M output tokens
- **Cheaper than GPT-4!**

### Setup:

1. Go to: https://console.anthropic.com/
2. Sign up
3. Add payment method
4. Generate API Key
5. Copy key (starts with `sk-ant-`)

**In Backend:** Choose OpenAI OR Claude (or support both!)

---

## 3️⃣ OpenAI Whisper Setup (Voice-to-Text)

### Option A: OpenAI Whisper API (Cloud)

**Pros:**
- ✅ Easy setup (same as OpenAI API key)
- ✅ No local GPU needed
- ✅ Fast processing
- ✅ Automatic updates

**Cons:**
- ❌ Costs $0.006/minute ($0.36/hour)
- ❌ Requires internet
- ❌ Privacy concern (audio sent to OpenAI)

**Setup:** Use same OpenAI API key from Step 1!

**No additional setup needed** ✅

---

### Option B: Local Whisper (whisper.cpp)

**Pros:**
- ✅ FREE (after setup)
- ✅ Privacy (audio stays local)
- ✅ Works offline
- ✅ Unlimited use

**Cons:**
- ❌ Requires GPU (RTX 2060+ recommended)
- ❌ Complex setup
- ❌ Slower than cloud (2-5x slower)

**Setup Guide:**

#### 1. Install Dependencies

**Install Python Whisper:**
```powershell
pip install openai-whisper
```

**Or faster whisper.cpp:**
```powershell
# Download from: https://github.com/ggerganov/whisper.cpp/releases
# Extract to: C:\whisper.cpp\
```

#### 2. Download Model

```powershell
# Small model (462 MB, fast, decent quality)
whisper --model small --download

# Medium model (1.5 GB, better quality)
whisper --model medium --download

# Large model (2.9 GB, best quality, slow)
whisper --model large --download
```

**Recommended:** Medium (good balance)

#### 3. Configure Backend

**In:** `backend/najika_server.py`

```python
# Choose Whisper mode
WHISPER_MODE = "local"  # or "api"
WHISPER_MODEL_PATH = "C:/whisper.cpp/models/ggml-medium.bin"
```

---

## 4️⃣ Text-to-Speech Setup (OPTIONAL)

### Option A: ElevenLabs (Best Quality)

**Pros:**
- ✅ Realistic voice
- ✅ Emotional expression
- ✅ Voice cloning (can sound like anime character)

**Cons:**
- ❌ $5-22/month subscription
- ❌ Rate limits

**Setup:**

1. Go to: https://elevenlabs.io/
2. Sign up
3. Free tier: 10,000 characters/month
4. Paid: $5/month (30K chars) or $22/month (100K chars)
5. API Key: Dashboard → Profile → API Key

**Cost estimate:**
- 100 messages/day × 50 chars = 5,000 chars/day
- = 150K chars/month
- **= $22/month plan needed**

---

### Option B: Local TTS (FREE)

**Windows Built-in:**
```python
import pyttsx3
engine = pyttsx3.init()
engine.say("Hello, I am Najika!")
engine.runAndWait()
```

**Pros:**
- ✅ FREE
- ✅ Offline
- ✅ Fast

**Cons:**
- ❌ Robotic voice (not anime-like)
- ❌ No emotion

**Recommended:** Use ElevenLabs for Najika, pyttsx3 as fallback

---

## 5️⃣ Environment Variables Setup (.env File)

### Create .env File

**Location:** `C:\Najika_World\backend\.env`

**Content:**
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=2000

# Whisper Configuration
WHISPER_MODE=api
# WHISPER_MODE=local
# WHISPER_MODEL_PATH=C:/whisper.cpp/models/ggml-medium.bin

# Anthropic Claude (Optional)
# ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
# ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# ElevenLabs TTS (Optional)
# ELEVENLABS_API_KEY=your_key_here
# ELEVENLABS_VOICE_ID=najika_voice_id

# Cloudflare Tunnel (Auto-configured)
CLOUDFLARE_TUNNEL_TOKEN=auto

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG_MODE=True

# Database (JSON for now)
DATABASE_TYPE=json
DATABASE_PATH=saves/

# Security
SECRET_KEY=your_random_secret_key_here_change_this
SESSION_TIMEOUT=3600

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
MAX_VOICE_MINUTES_PER_DAY=120

# Logging
LOG_LEVEL=INFO
LOG_FILE=najika_server.log
```

---

## 6️⃣ Load Environment Variables in Backend

### Update najika_server.py

**Add at top of file:**

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
WHISPER_MODE = os.getenv("WHISPER_MODE", "api")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in .env file!")

# Initialize OpenAI client
import openai
openai.api_key = OPENAI_API_KEY
```

### Install python-dotenv

```powershell
cd C:\Najika_World\backend
pip install python-dotenv
```

---

## 7️⃣ Secure Your Credentials

### ⚠️ IMPORTANT: Never commit .env to Git!

**Update .gitignore:**

```
# Add to C:\Najika_World\.gitignore
.env
*.env
.env.local
backend/.env
backend/*.env
```

**Verify:**
```powershell
cd C:\Najika_World
git status
# .env should NOT appear in untracked files
```

---

## 8️⃣ Create .env.example Template

**For other developers/web model:**

**Create:** `C:\Najika_World\backend\.env.example`

```env
# Copy this to .env and fill in your keys

OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
OPENAI_MODEL=gpt-4-turbo-preview
WHISPER_MODE=api
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG_MODE=True
```

**This IS safe to commit** (no actual keys)

---

## 9️⃣ Test Configuration

### Test Script

**Create:** `C:\Najika_World\backend\test_api_keys.py`

```python
import os
from dotenv import load_dotenv
import openai

load_dotenv()

def test_openai():
    try:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            print("❌ OPENAI_API_KEY not found in .env")
            return False

        openai.api_key = key

        # Test API call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API Key Works!'"}],
            max_tokens=10
        )

        print(f"✅ OpenAI API: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return False

def test_whisper():
    try:
        mode = os.getenv("WHISPER_MODE", "api")
        print(f"✅ Whisper Mode: {mode}")

        if mode == "local":
            model_path = os.getenv("WHISPER_MODEL_PATH")
            if os.path.exists(model_path):
                print(f"✅ Whisper Model Found: {model_path}")
            else:
                print(f"❌ Whisper Model Not Found: {model_path}")
                return False
        return True
    except Exception as e:
        print(f"❌ Whisper Error: {e}")
        return False

if __name__ == "__main__":
    print("=== API Keys Test ===\n")

    openai_ok = test_openai()
    whisper_ok = test_whisper()

    print("\n=== Results ===")
    if openai_ok and whisper_ok:
        print("✅ All API keys configured correctly!")
    else:
        print("❌ Some API keys need configuration")
```

**Run:**
```powershell
cd C:\Najika_World\backend
python test_api_keys.py
```

---

## 🔟 Monitor API Usage

### OpenAI Dashboard

1. Go to: https://platform.openai.com/usage
2. View daily/monthly usage
3. Check costs

**Set up alerts:**
- Email when 50% budget used
- Email when 90% budget used
- Auto-stop at 100% (optional, but risky if needed)

---

## 📊 Cost Optimization Tips

### 1. Use GPT-3.5-turbo for Simple Tasks
- 10x cheaper than GPT-4
- Good for basic conversations
- Switch to GPT-4 only for complex reasoning

### 2. Implement Caching
- Cache common responses
- Reduce redundant API calls
- Save ~30-50% costs

### 3. Limit Token Usage
- Set `max_tokens=1000` (don't let model ramble)
- Use shorter system prompts
- Trim conversation history

### 4. Local Whisper = FREE
- If you have GPU, use local Whisper
- Save $10-20/month on voice transcription

---

## 🎯 Recommended Setup (Budget Tiers)

### 💰 Budget Tier ($5-10/month)
- GPT-3.5-turbo for conversations
- Local Whisper (whisper.cpp)
- No TTS (text only)
- Cloudflare Tunnel (free)

### 💵 Standard Tier ($20-40/month)
- GPT-4 Turbo for conversations
- OpenAI Whisper API
- ElevenLabs TTS ($5 plan)
- Cloudflare Tunnel (free)

### 💎 Premium Tier ($50-100/month)
- GPT-4 for all conversations
- OpenAI Whisper API
- ElevenLabs TTS ($22 plan)
- Custom voice cloning
- Cloud hosting (optional)

---

## ✅ Checklist

Before starting backend:

- [ ] OpenAI API key obtained
- [ ] Spending limit set ($50)
- [ ] .env file created with API key
- [ ] .env added to .gitignore
- [ ] python-dotenv installed
- [ ] test_api_keys.py passed ✅
- [ ] Whisper mode chosen (api or local)
- [ ] (Optional) Cloudflare Tunnel configured
- [ ] (Optional) ElevenLabs account created

---

## 📝 Next Steps

1. ✅ Complete this setup
2. ✅ Test with test_api_keys.py
3. ✅ Start backend: `python najika_server.py`
4. ✅ Verify API calls in logs
5. ✅ Monitor usage in OpenAI dashboard

**Done!** 🎉

Your backend is now ready with AI-powered Najika!
