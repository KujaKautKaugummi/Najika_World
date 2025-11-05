# 🍓 RASPBERRY PI 5 - NAJIKA 24/7 SERVER SETUP

## 🎯 ZIEL
Raspberry Pi 5 als 24/7 Najika-Server, damit die App auch funktioniert wenn dein PC aus ist.

---

## 🛒 SHOPPING LISTE

### 📦 PAKET 1: RASPBERRY PI 5 STARTER KIT (Empfohlen)

**Option A: Offizielles Raspberry Pi 5 Kit (€120-140)**
```
Enthält:
✅ Raspberry Pi 5 (8GB RAM) - Hauptgerät
✅ Offizielles Netzteil (27W USB-C) - Stromversorgung
✅ Aktiver Kühler - Für Dauerbetrieb wichtig!
✅ microSD-Karte (32GB) - Betriebssystem
✅ Micro-HDMI Kabel - Display-Anschluss
✅ Gehäuse - Schutz & Kühlung

Kaufen bei:
- Amazon.de: "Raspberry Pi 5 8GB Starter Kit"
- Reichelt.de
- BerryBase.de
```

**Option B: Einzelteile kaufen (€100-120, flexibler)**
```
1. Raspberry Pi 5 - 8GB RAM: €80-90
2. Offizielles 27W USB-C Netzteil: €12
3. Aktiver Kühler: €5-8
4. microSD-Karte 64GB (SanDisk Extreme): €12
5. Gehäuse mit Lüfter: €10-15
6. Micro-HDMI zu HDMI Kabel: €5
```

---

### 🔌 PAKET 2: ZUBEHÖR FÜR 24/7 BETRIEB

**Notwendig:**
```
1. USV (Unterbrechungsfreie Stromversorgung): €40-60
   - Modell: APC Back-UPS BX700UI
   - Schutz bei Stromausfall (15-30 Min Überbrückung)
   - Wichtig für sauberes Herunterfahren!

2. Netzwerk-Kabel (Cat6, 2m): €5
   - Für stabile LAN-Verbindung
   - Schneller als WiFi

3. Externe SSD (optional, empfohlen): €30-50
   - Samsung T7 500GB
   - Schneller als microSD
   - Längere Lebensdauer bei 24/7 Betrieb
```

**Optional (Nice-to-Have):**
```
4. Raspberry Pi PoE+ HAT: €25
   - Power-over-Ethernet (Strom über LAN-Kabel)
   - Reduziert Kabel-Chaos
   - Benötigt PoE-fähigen Switch

5. Mini-Display (3.5" Touch): €20
   - Status-Anzeige ohne Monitor
   - Zeigt CPU, RAM, Temperatur

6. Zusätzliche Kühlung (Heatsinks): €5
   - Für maximale Stabilität bei Dauerlast
```

---

## 💰 KOSTEN ÜBERSICHT

### MINIMUM-SETUP (funktioniert):
```
Raspberry Pi 5 8GB Kit:     €120
USV (APC BX700UI):          €50
Netzwerk-Kabel:             €5
-----------------------------------
GESAMT:                     €175
```

### EMPFOHLENES SETUP (optimal):
```
Raspberry Pi 5 8GB Kit:     €120
USV (APC BX700UI):          €50
Externe SSD 500GB:          €40
Netzwerk-Kabel:             €5
-----------------------------------
GESAMT:                     €215
```

### PREMIUM-SETUP (maximale Performance):
```
Raspberry Pi 5 8GB (einzeln): €85
Offizielles Netzteil:         €12
Aktiver Kühler + Heatsinks:   €10
Argon NEO 5 Gehäuse (Premium):€25
Samsung T7 SSD 1TB:           €70
USV (APC BX700UI):            €50
Cat6 Kabel 3m:                €5
Mini Touch-Display:           €20
-----------------------------------
GESAMT:                       €277
```

---

## 🔧 TECHNISCHE SPECS - RASPBERRY PI 5

```yaml
CPU: Broadcom BCM2712 (Quad-Core Cortex-A76 @ 2.4GHz)
RAM: 8GB LPDDR4X
GPU: VideoCore VII (OpenGL ES 3.1, Vulkan 1.2)
Storage: microSD + NVMe SSD support (via HAT)
Network: Gigabit Ethernet + WiFi 6 (802.11ac)
USB: 2x USB 3.0, 2x USB 2.0
Power: 27W USB-C (5V/5A)
GPIO: 40-Pin Header
```

**Perfekt für Najika:**
- ✅ 8GB RAM: Genug für Ollama Llama 3.2 3B Model
- ✅ 2.4GHz CPU: Schnell genug für AI-Inferenz
- ✅ Gigabit LAN: Niedrige Latenz für Mobile App
- ✅ Sehr stromsparend: ~15W im Betrieb (€3-5/Monat Strom)

---

## 📥 WO KAUFEN?

### Deutschland:
```
1. BerryBase.de - Raspberry Pi Spezialist
   ✅ Beste Verfügbarkeit
   ✅ Deutsches Lager (schneller Versand)

2. Reichelt.de - Elektronik-Versand
   ✅ Große Auswahl Zubehör
   ✅ Oft günstigere Bundles

3. Amazon.de
   ✅ Prime Versand
   ⚠️ Achte auf offiziellen Verkäufer!

4. Conrad.de
   ✅ Filialen für Abholung
   ✅ Gute Beratung
```

### Empfohlene Bundles (Stand 2025):
```
BerryBase: "Raspberry Pi 5 8GB Premium Kit"
- Enthält alles + Premium Gehäuse
- €139

Reichelt: "Raspberry Pi 5 Starter Set"
- Basic aber komplett
- €119

Amazon: "GeeekPi Raspberry Pi 5 Kit"
- Mit SSD-Adapter
- €145
```

---

## 🚀 SETUP-ABLAUF (SPÄTER)

Nach dem Kauf (wenn angekommen):

**Phase 1: Hardware-Setup (30 Min)**
1. Raspberry Pi zusammenbauen
2. Kühler montieren
3. OS auf microSD flashen (Raspberry Pi OS Lite)
4. LAN-Kabel + Strom anschließen

**Phase 2: Software-Setup (1-2 Stunden)**
1. SSH aktivieren
2. Python 3.11+ installieren
3. Ollama für ARM64 installieren
4. NajikaCore übertragen
5. Autostart konfigurieren

**Phase 3: Optimierung (1 Stunde)**
1. Overclocking (optional, für mehr Performance)
2. Swap-File vergrößern (für AI-Models)
3. Monitoring-Dashboard (CPU/RAM/Temp)
4. Backup-System einrichten

---

## ⚡ STROMVERBRAUCH & KOSTEN

```
Raspberry Pi 5 (8GB):
- Idle: ~5W
- Last: ~12W
- Maximum: ~15W (mit USB-Geräten)

Kosten pro Monat (24/7):
- 15W × 24h × 30d = 10.8 kWh
- 10.8 kWh × €0.35/kWh = €3.78/Monat
- €45/Jahr

Zum Vergleich:
- Gaming-PC (24/7): ~€150-300/Jahr
- Laptop (24/7): ~€80-120/Jahr
- Raspberry Pi: €45/Jahr ✅
```

---

## 🔒 SICHERHEIT

**USV-Schutz wichtig wegen:**
```
1. microSD-Korruption bei Stromausfall
2. Datenbank-Inkonsistenz (ChromaDB)
3. Ollama-Model-Cache Fehler
```

**Mit USV (15-30 Min Backup-Zeit):**
- Server fährt sauber herunter
- Keine Datenverluste
- SD-Karte bleibt gesund

---

## 📊 PERFORMANCE-VERGLEICH

```
                    PC (Ryzen/Intel)  Raspberry Pi 5    Xiaomi 11T Pro
─────────────────────────────────────────────────────────────────────
Ollama Llama 3B     15 tokens/s       3-5 tokens/s      2-3 tokens/s
Stromverbrauch      150-300W          10-15W            5-10W (Akku)
Dauerbetrieb        Laut, heiß        ✅ Leise, kühl    ❌ Akku-Tod
Kosten/Jahr         €300+             €45               €0 (aber stirbt)
Mobilität           ❌ Standort       ✅ Kompakt        ✅ Mobil
─────────────────────────────────────────────────────────────────────

BESTE STRATEGIE:
1. PC: Hauptnutzung (schnellste AI)
2. Raspberry Pi: 24/7 Backup (immer erreichbar)
3. Xiaomi: Mobile App (unterwegs)
```

---

## 🎯 MODELL-EMPFEHLUNG FÜR RASPBERRY PI

**Ollama auf Raspberry Pi 5 (8GB RAM):**

```yaml
# Kleine, schnelle Modelle (3-5 tokens/s):
1. Llama 3.2 3B (empfohlen)
   - Size: 2GB
   - Quality: Sehr gut für Chat
   - Speed: ~5 tokens/s

2. Phi-3 Mini (3.8B)
   - Size: 2.3GB
   - Quality: Gut für kurze Antworten
   - Speed: ~4 tokens/s

3. TinyLlama 1.1B (Notfall-Fallback)
   - Size: 637MB
   - Quality: Basic
   - Speed: ~8 tokens/s

# NICHT empfohlen (zu groß):
❌ Llama 3.1 8B - Zu langsam (~1 token/s)
❌ Mistral 7B - Läuft, aber sehr langsam
```

---

## 📝 QUICK-START BESTELLUNG

**Für sofortigen Start - bestelle jetzt:**

### Option 1: Amazon Prime (1-2 Tage)
```
1. "Raspberry Pi 5 8GB Official Kit" - €135
   https://amazon.de/...

2. "APC Back-UPS BX700UI" - €55
   https://amazon.de/...

3. "Cat6 Kabel 2m" - €5
   https://amazon.de/...
```

### Option 2: BerryBase (2-3 Tage, günstiger)
```
1. Raspberry Pi 5 Premium Bundle - €139
   https://berrybase.de/...

2. USV + Zubehör von Amazon/Reichelt
```

---

## ❓ FAQ

**Q: Reicht 4GB RAM?**
A: Nein! Für Ollama mit Najika-Persona brauchst du 8GB. 4GB ist zu knapp.

**Q: Brauche ich wirklich eine USV?**
A: Bei 24/7-Betrieb: JA! Ohne USV kann ein Stromausfall die SD-Karte zerstören.

**Q: Kann ich meine alte microSD verwenden?**
A: Nur wenn sie schnell genug ist (U3/A2). Empfohlen: SanDisk Extreme 64GB.

**Q: SSD notwendig oder optional?**
A: Optional, aber SEHR empfohlen für Dauerbetrieb. SD-Karten sterben schneller.

**Q: Passt das in mein Regal?**
A: Ja! Raspberry Pi 5 ist nur 85x56x17mm (Kreditkartengröße).

**Q: Wie laut ist es?**
A: Mit aktivem Kühler: Leises Summen (kaum hörbar). Ohne: Lautlos.

**Q: Kann ich später aufrüsten?**
A: Ja! RAM ist fest, aber du kannst SSD, Kühlung, Gehäuse upgraden.

---

## 🔗 HILFREICHE LINKS

```
Offizielle Raspberry Pi Docs:
https://www.raspberrypi.com/documentation/

Ollama ARM64 Installation:
https://ollama.com/download/linux

NajikaCore GitHub (später):
https://github.com/your-username/najikacore

Raspberry Pi Forum (Deutsch):
https://forum-raspberrypi.de/
```

---

**Erstellt**: 2025-10-18
**Budget**: €175-280
**Stromkosten**: ~€4/Monat
**Lautstärke**: Leise (< 30dB)
**Setup-Zeit**: 2-3 Stunden
**Wartung**: Minimal (monatliches Update)

🍓 **BEREIT ZUM BESTELLEN? GIB MIR BESCHEID!** 🚀
