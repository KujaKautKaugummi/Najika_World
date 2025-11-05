# ☁️ NAJIKA CLOUD-FALLBACK SYSTEM

## 🎯 KONZEPT

**Problem**: Mobile App braucht Najika auch wenn PC/Server aus ist
**Lösung**: Cloud-AI als Fallback, aber nur mit User-Freigabe

---

## 🔐 SICHERHEITS-ARCHITEKTUR

### **3-Stufen-Fallback:**

```
1. PRIMÄR: Ollama auf PC/Raspberry Pi (lokal)
   ✅ Volle Najika-Persönlichkeit
   ✅ Kostenlos
   ✅ Privat
   ❌ Nur wenn PC/Server läuft

2. FALLBACK: Cloud-AI (Claude/OpenAI)
   ✅ Immer verfügbar
   ✅ Volle Najika-Persönlichkeit
   ⚠️ Kostet Geld (API-Calls)
   🔒 Nur nach Freigabe

3. NOTFALL: On-Device (Gemini Nano auf Handy)
   ✅ Immer verfügbar
   ✅ Kostenlos
   ⚠️ Reduzierte Persönlichkeit (kleines Modell)
```

---

## 🎮 USER-FREIGABE-SYSTEM

### **Option A: App-Button (Empfohlen)**

```dart
// In Mobile App
Widget buildCloudFallbackToggle() {
  return Switch(
    value: cloudFallbackEnabled,
    onChanged: (bool value) async {
      if (value) {
        // User aktiviert Cloud-Fallback
        bool confirmed = await showConfirmDialog(
          'Cloud-Fallback aktivieren?',
          'Najika nutzt Claude API wenn PC offline ist.\n'
          'Kosten: ~€0.01-0.05 pro Chat.\n'
          'Datenschutz: Verschlüsselt, keine Speicherung.'
        );

        if (confirmed) {
          await enableCloudFallback();
        }
      } else {
        await disableCloudFallback();
      }
    },
  );
}
```

**UI-Mockup:**
```
┌─────────────────────────────────────┐
│ ⚙️  EINSTELLUNGEN                   │
├─────────────────────────────────────┤
│                                     │
│ 🤖 AI-EINSTELLUNGEN                 │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Cloud-Fallback          [ON/OFF]│ │
│ │                                 │ │
│ │ Status: PC OFFLINE ❌           │ │
│ │ Aktuell: Claude API ☁️          │ │
│ │                                 │ │
│ │ Kosten heute: €0.12             │ │
│ │ (4 Chats)                       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ⚠️  Cloud nur bei PC-Ausfall       │
│ ℹ️  Daten verschlüsselt, temporär  │
└─────────────────────────────────────┘
```

---

### **Option B: Automatisch mit Bestätigung**

```dart
Future<String> getChatResponse(String message) async {
  // 1. Versuche PC/Server
  try {
    return await serverAPI.chat(message);
  } catch (e) {
    // PC offline!

    // 2. Prüfe Cloud-Freigabe
    if (cloudFallbackEnabled) {
      return await cloudAPI.chat(message);
    }

    // 3. Frage User
    bool useCloud = await showDialog(
      'PC offline. Cloud-Fallback nutzen?',
      buttons: ['Ja, Claude nutzen', 'Nein, On-Device AI']
    );

    if (useCloud) {
      return await cloudAPI.chat(message);
    } else {
      return await onDeviceAI.chat(message);
    }
  }
}
```

---

## 🔧 SERVER-IMPLEMENTIERUNG

### **Neues Endpoint: `/api/mobile/fallback`**

```python
# In najika_server.py hinzufügen:

# Globals für Mobile-Fallback
MOBILE_CLOUD_ENABLED = False  # User muss freigeben
MOBILE_CLOUD_LIMIT = 100      # Max 100 Requests/Tag

MOBILE_STATS = {
    "cloud_requests_today": 0,
    "last_reset": datetime.now().date(),
    "total_cost_estimate": 0.0
}

def reset_mobile_stats_if_needed():
    """Reset Counter jeden Tag"""
    today = datetime.now().date()
    if MOBILE_STATS["last_reset"] != today:
        MOBILE_STATS["cloud_requests_today"] = 0
        MOBILE_STATS["last_reset"] = today

# In do_POST():
if self.path == "/api/mobile/fallback/enable":
    # User aktiviert Cloud-Fallback via App
    data = json.loads(body.decode("utf-8"))
    auth_token = data.get("token", "")

    # Simple Auth-Check (später: JWT Token)
    if auth_token != os.getenv("MOBILE_AUTH_TOKEN", ""):
        self.send_error(401, "Unauthorized")
        return

    globals()["MOBILE_CLOUD_ENABLED"] = True
    log("INFO", "Mobile Cloud-Fallback aktiviert", "MOBILE")

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps({"ok": True}).encode())
    return

if self.path == "/api/mobile/fallback/disable":
    globals()["MOBILE_CLOUD_ENABLED"] = False
    log("INFO", "Mobile Cloud-Fallback deaktiviert", "MOBILE")

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps({"ok": True}).encode())
    return

if self.path == "/api/mobile/fallback/stats":
    # Kosten-Statistiken für User
    reset_mobile_stats_if_needed()

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps({
        "cloud_enabled": MOBILE_CLOUD_ENABLED,
        "requests_today": MOBILE_STATS["cloud_requests_today"],
        "limit": MOBILE_CLOUD_LIMIT,
        "cost_estimate": MOBILE_STATS["total_cost_estimate"]
    }).encode())
    return
```

---

### **Modifizierter Chat-Endpoint für Mobile:**

```python
# In /api/chat hinzufügen:

# Prüfe ob Request von Mobile App kommt
is_mobile = self.headers.get("User-Agent", "").startswith("NajikaApp/")

# Versuche Ollama (lokal)
try:
    if AI_PROVIDER == "ollama":
        out = call_ollama(prompt, use_wizard=private_trigger)
    else:
        # Cloud schon aktiv
        out = call_cloud_ai(prompt)

except Exception as e:
    # Ollama offline!
    log("WARNING", f"Ollama offline: {e}", "AI")

    # Mobile-Fallback nur wenn aktiviert
    if is_mobile and MOBILE_CLOUD_ENABLED:
        # Prüfe Limit
        reset_mobile_stats_if_needed()
        if MOBILE_STATS["cloud_requests_today"] >= MOBILE_CLOUD_LIMIT:
            out = "⚠️ Cloud-Limit erreicht (100/Tag). Najika ist müde... 💤"
        else:
            # Nutze Cloud-API
            out = call_cloud_ai(prompt)
            MOBILE_STATS["cloud_requests_today"] += 1
            MOBILE_STATS["total_cost_estimate"] += 0.02  # ~€0.02 pro Request
            log("INFO", f"Cloud-Fallback genutzt ({MOBILE_STATS['cloud_requests_today']}/100)", "MOBILE")
    else:
        # Kein Fallback: Error
        out = "❌ PC offline & Cloud-Fallback nicht aktiviert. Nutze On-Device AI!"
```

---

## 💰 KOSTEN-KONTROLLE

### **API-Kosten (2025):**

```yaml
Claude API (Anthropic):
  Modell: claude-3-haiku-20240307 (schnell & günstig)
  Input: €0.00025 / 1K tokens
  Output: €0.00125 / 1K tokens

  Durchschnittlicher Chat:
    Input: ~500 tokens (Najika-Persona + Kontext)
    Output: ~150 tokens (Antwort)
    = €0.00125 + €0.0001875 ≈ €0.0014 pro Chat

OpenAI API:
  Modell: gpt-3.5-turbo (günstig)
  Input: €0.0005 / 1K tokens
  Output: €0.0015 / 1K tokens
  ≈ €0.0025 pro Chat

Google Gemini API:
  Modell: gemini-1.5-flash (kostenlos bis 1500 req/Tag!)
  Kosten: €0 😍

EMPFEHLUNG: Gemini Flash (kostenlos + schnell)
```

### **Budget-Limits:**

```dart
// In App konfigurierbar
class CloudFallbackSettings {
  int maxRequestsPerDay = 100;      // Max 100 Chats/Tag
  double maxCostPerMonth = 5.0;     // Max €5/Monat
  bool autoDisableOnLimit = true;   // Auto-Disable bei Limit

  // Warnung bei Schwellenwerten
  double warningThreshold = 0.7;    // Warnung bei 70%
}
```

---

## 🔒 DATENSCHUTZ & SICHERHEIT

### **Was wird an Cloud gesendet?**

```python
def call_cloud_ai(prompt):
    """Cloud-AI mit Datenschutz"""

    # 1. Anonymisierung
    safe_prompt = anonymize_prompt(prompt)

    # 2. Ende-zu-Ende Verschlüsselung (optional)
    encrypted_prompt = encrypt(safe_prompt)

    # 3. API-Call
    response = anthropic.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.8,
        messages=[{"role": "user", "content": encrypted_prompt}]
    )

    # 4. Keine Speicherung bei Anthropic
    # (Claude speichert nur 30 Tage, dann gelöscht)

    return response.content[0].text

def anonymize_prompt(prompt):
    """Entfernt persönliche Daten"""
    # Ersetze Namen, Adressen, etc.
    safe = prompt.replace("Kuja", "[USER]")
    safe = safe.replace("Mr.K", "[USER]")
    # ... weitere Anonymisierung
    return safe
```

### **Transparenz:**

```
App zeigt IMMER an:
- Welche AI gerade genutzt wird (PC/Cloud/On-Device)
- Kosten für heutigen Tag
- Anzahl Cloud-Requests
```

---

## 📱 MOBILE APP INTEGRATION

### **Vollständiger Flow:**

```dart
class NajikaAI {
  enum AISource { PC, Cloud, OnDevice }

  Future<ChatResponse> sendMessage(String message) async {
    AISource source;
    String response;

    // 1. Versuche PC/Server (primär)
    try {
      response = await pcAPI.chat(message);
      source = AISource.PC;
    } catch (e) {
      // PC offline

      // 2. Prüfe Cloud-Fallback
      if (settings.cloudFallbackEnabled) {
        try {
          response = await cloudAPI.chat(message);
          source = AISource.Cloud;

          // Update Statistiken
          stats.cloudRequestsToday++;
          stats.costToday += 0.0014; // Claude Haiku
        } catch (e2) {
          // Cloud auch offline (kein Internet?)
          response = await onDeviceAI.chat(message);
          source = AISource.OnDevice;
        }
      } else {
        // Cloud nicht freigegeben → On-Device
        response = await onDeviceAI.chat(message);
        source = AISource.OnDevice;
      }
    }

    // 3. Return mit Meta-Info
    return ChatResponse(
      text: response,
      source: source,
      timestamp: DateTime.now(),
    );
  }
}

// UI zeigt Source an:
Widget buildChatBubble(ChatResponse msg) {
  String sourceIcon;
  switch (msg.source) {
    case AISource.PC:
      sourceIcon = '🖥️';
      break;
    case AISource.Cloud:
      sourceIcon = '☁️';
      break;
    case AISource.OnDevice:
      sourceIcon = '📱';
      break;
  }

  return Container(
    child: Column(
      children: [
        Text(msg.text),
        Text('$sourceIcon ${msg.source.name}', style: small),
      ],
    ),
  );
}
```

---

## ⚙️ .ENV CONFIGURATION

```env
# Bestehende Cloud-Config
CLOUD_ENABLED=false
CLOUD_PIN=dein-geheimes-pin
ANTHROPIC_API_KEY=sk-ant-xxx...
OPENAI_API_KEY=sk-xxx...

# NEU: Mobile-Fallback Config
MOBILE_CLOUD_ENABLED=false
MOBILE_AUTH_TOKEN=secure-random-token-hier
MOBILE_CLOUD_LIMIT=100
MOBILE_CLOUD_PROVIDER=gemini  # gemini, claude, openai
GEMINI_API_KEY=xxx...  # Kostenlos!
```

---

## 🚀 SETUP-ANLEITUNG

### **1. Google Gemini API (KOSTENLOS)**

```bash
1. Gehe zu: https://ai.google.dev/
2. "Get API Key" klicken
3. Kostenloses Konto erstellen
4. API Key kopieren
5. In .env einfügen:
   GEMINI_API_KEY=your-key-here
```

**Limits (Free Tier):**
```
- 1500 Requests pro Tag (mehr als genug!)
- 1 Million Tokens/Monat
- Rate: 60 Requests/Minute
```

### **2. Server vorbereiten**

```python
# Install Gemini SDK
pip install google-generativeai

# In najika_server.py:
import google.generativeai as genai

def call_gemini(prompt):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0.8,
            'max_output_tokens': 300,
        }
    )

    return response.text
```

### **3. Mobile App Update**

```dart
// Füge Cloud-Fallback Toggle in Settings hinzu
// Implementiere AISource-Detection
// Zeige Kosten-Statistiken
```

---

## 📊 MONITORING & LOGS

```python
# Server loggt automatisch:
[INFO] Mobile Cloud-Fallback aktiviert
[INFO] Cloud-Fallback genutzt (12/100)
[WARNING] Cloud-Limit erreicht (100/100)
[INFO] PC wieder online - zurück zu Ollama
```

**App Dashboard:**
```
┌─────────────────────────────────────┐
│ 📊 AI-STATISTIKEN (HEUTE)           │
├─────────────────────────────────────┤
│ PC (Ollama):        42 Chats ✅     │
│ Cloud (Gemini):      8 Chats ☁️     │
│ On-Device:           0 Chats 📱     │
│ ───────────────────────────────────│
│ Gesamt:             50 Chats        │
│ Kosten:           €0.00 (Gemini!)   │
│ Durchschn. Latenz:  1.2s            │
└─────────────────────────────────────┘
```

---

## ✅ ZUSAMMENFASSUNG

**Vorteile:**
- ✅ Najika IMMER verfügbar (PC, Cloud, On-Device)
- ✅ User hat volle Kontrolle (Freigabe-System)
- ✅ Kostenlos mit Gemini API!
- ✅ Transparente Kosten-Anzeige
- ✅ Automatischer Fallback-Chain

**Sicherheit:**
- 🔒 Cloud nur nach Freigabe
- 🔒 Anonymisierung persönlicher Daten
- 🔒 Ende-zu-Ende Verschlüsselung möglich
- 🔒 Keine permanente Speicherung

**Kosten (wenn Gemini genutzt):**
- **€0/Monat!** 🎉

---

**Erstellt**: 2025-10-18
**Status**: Bereit zur Implementierung
**Empfehlung**: Gemini Flash (kostenlos + schnell)
