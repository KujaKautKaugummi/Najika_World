# NAJIKA WORLD - API DOKUMENTATION

**Erstellt:** 2026-02-02
**Autor:** Claude Code (OPUS-1)
**Server:** `http://127.0.0.1:8000`

---

## ÜBERSICHT - NEUE SYSTEME (2026-02-02)

| System | Datei | APIs | Status |
|--------|-------|------|--------|
| Söldner/Eskorte | najika_eskorte_system.py | 13 | ✅ FERTIG |
| Cheater-Hinrichtung | najika_cheater_hinrichtung.py | 8 | ✅ FERTIG |
| Gruppen-Disconnect | najika_gruppe_disconnect.py | 9 | ✅ FERTIG |
| Slime Spezialisierung | najika_slime_spezialisierung.py | 9 | ✅ FERTIG |
| Alchemy | najika_alchemy_system.py | 6 | ✅ FERTIG |

**GESAMT: ~45 neue API-Endpoints**

---

## 1. SÖLDNER/ESKORTE SYSTEM

### GET Endpoints

#### `GET /api/soeldner/status`
Gibt System-Status und Preisliste zurück.

**Response:**
```json
{
  "enabled": true,
  "stats": {
    "abbilder_registriert": 5,
    "soeldner_online": 2,
    "aktive_eskorten": 1
  },
  "preisliste": {...}
}
```

#### `GET /api/soeldner/preise`
Gibt Preisliste für alle Eskorte-Dienste zurück.

#### `GET /api/soeldner/rang/{spieler_id}`
Gibt Rang und Taten eines Spielers zurück.

**Response:**
```json
{
  "spieler_id": "player1",
  "rang": "besungen",
  "taten": {
    "gesamt": 15,
    "kampf": 8,
    "bosse": 3
  },
  "kann_eskortieren": true,
  "kann_retten": false
}
```

#### `GET /api/soeldner/abbilder?region=...`
Sucht verfügbare AI-Abbilder (optional nach Region).

#### `GET /api/soeldner/online?region=...&dienst=...`
Sucht online verfügbare echte Söldner.

### POST Endpoints

#### `POST /api/soeldner/verfuegbar`
Spieler meldet sich als Söldner verfügbar.

**Request:**
```json
{
  "spieler_id": "player1",
  "name": "Held",
  "level": 50,
  "regionen": ["samtmoos_tiefwald"],
  "dienste": ["eskorte", "rettung"]
}
```

#### `POST /api/soeldner/nicht-verfuegbar`
Spieler meldet sich als Söldner ab.

#### `POST /api/soeldner/abbild/erstellen`
Erstellt/aktualisiert AI-Abbild eines Spielers.

**Request:**
```json
{
  "spieler_id": "player1",
  "name": "Held",
  "level": 50,
  "stats": {"hp": 1000, "atk": 150},
  "ausruestung": {},
  "kampfstil": "balanced"
}
```

#### `POST /api/soeldner/eskorte/buchen`
Bucht eine Eskorte.

**Request:**
```json
{
  "auftraggeber_id": "client1",
  "soeldner_id": "player1",
  "typ": "ai_abbild",
  "start_ort": "Samtmoos-Tiefwald",
  "ziel_ort": "Götterfels",
  "mit_rueckweg": false
}
```

#### `POST /api/soeldner/rettung/buchen`
Bucht eine Rettung (nur Legendär-Spieler!).

#### `POST /api/soeldner/session/status`
Aktualisiert Status einer Eskorte-Session.

#### `POST /api/soeldner/tod`
Meldet Tod eines Söldners während Eskorte.

#### `POST /api/soeldner/tat/registrieren`
Registriert eine Tat für Rang-Aufstieg.

---

## 2. CHEATER-HINRICHTUNGS SYSTEM

### GET Endpoints

#### `GET /api/cheater/status`
Gibt System-Status und Statistiken zurück.

#### `GET /api/cheater/hall-of-shame?limit=50`
Gibt Hall of Shame zurück (ewige Schande!).

**Response:**
```json
{
  "hall_of_shame": [
    {
      "spieler_id": "cheater123",
      "spieler_name": "H4ck3rM4n",
      "cheat_typ": "damage_hack",
      "hinrichtungs_datum": 1706889600,
      "hinrichtungs_methode": "Göttlicher Blitz",
      "zuschauer_anzahl": 42
    }
  ],
  "count": 1,
  "nachricht": "Ewige Schande für Betrüger!"
}
```

#### `GET /api/cheater/hinrichtungen`
Gibt anstehende Hinrichtungs-Events zurück.

#### `GET /api/cheater/ist-gebannt/{spieler_id}`
Prüft ob Spieler gebannt ist.

### POST Endpoints

#### `POST /api/cheater/report`
Erstellt manuellen Cheat-Report.

**Request:**
```json
{
  "reporter_id": "honest_player",
  "verdaechtiger_id": "suspicious_guy",
  "verdaechtiger_name": "SuspiciousGuy",
  "cheat_typ": "damage_hack",
  "beschreibung": "Hat 99999 Schaden gemacht",
  "beweise": []
}
```

#### `POST /api/cheater/zuschauer`
Meldet sich als Zuschauer für Hinrichtung an.

#### `POST /api/cheater/einspruch`
Reicht Einspruch gegen Verurteilung ein.

### ADMIN Endpoints

#### `POST /api/admin/cheater/review/start`
Startet Review eines Reports.

#### `POST /api/admin/cheater/review/entscheiden`
Beendet Review mit Entscheidung.

#### `POST /api/admin/cheater/hinrichtung/durchfuehren`
Führt Hinrichtung durch.

#### `POST /api/admin/cheater/einspruch/entscheiden`
Entscheidet über Einspruch.

---

## 3. GRUPPEN-DISCONNECT SYSTEM

### GET Endpoints

#### `GET /api/gruppe/disconnect/stats`
Gibt System-Statistiken zurück.

#### `GET /api/gruppe/disconnect/spieler/{spieler_id}`
Gibt Disconnect-Statistik eines Spielers zurück.

#### `GET /api/gruppe/disconnect/cooldown/{spieler_id}?gruppe=...`
Prüft ob Spieler Cooldown hat.

### POST Endpoints

#### `POST /api/gruppe/erstellen`
Erstellt eine neue Gruppe.

**Request:**
```json
{
  "gruppe_id": "gruppe123",
  "mitglieder": ["tank", "healer", "dps1", "dps2"]
}
```

#### `POST /api/gruppe/boss/start`
Startet Boss-Kampf für Gruppe.

**Request:**
```json
{
  "gruppe_id": "gruppe123",
  "boss_id": "boss_dragon",
  "boss_hp": 100000
}
```

#### `POST /api/gruppe/disconnect`
Meldet Disconnect eines Spielers.

**Request:**
```json
{
  "spieler_id": "tank",
  "gruppe_id": "gruppe123",
  "kampf_kontext": {
    "in_kampf": true,
    "gegner_typ": "boss",
    "spieler_hp_prozent": 45,
    "boss_hp_prozent": 60,
    "boss_aktion": "spezial_angriff"
  }
}
```

**Response:**
```json
{
  "typ": "gruppe",
  "aktion": "abstimmung",
  "nachricht": "[tank] hat Verbindung verloren!",
  "pause_dauer": 5,
  "abstimmung": {
    "abstimmung_id": "vote_...",
    "optionen": {...}
  }
}
```

#### `POST /api/gruppe/reconnect`
Meldet Reconnect eines Spielers.

#### `POST /api/gruppe/abstimmung/stimme`
Gibt Stimme bei Disconnect-Abstimmung ab.

**Request:**
```json
{
  "abstimmung_id": "vote_...",
  "spieler_id": "healer",
  "wahl": "warten"
}
```

#### `POST /api/gruppe/boss/ende`
Beendet Boss-Kampf.

---

## 4. SLIME SPEZIALISIERUNG

### GET Endpoints

#### `GET /api/slime/spec/status/{slime_id}`
Gibt Spezialisierungs-Status zurück.

#### `GET /api/slime/spec/kampf-boni/{slime_id}?level=20`
Berechnet aktuelle Kampf-Boni.

**Response:**
```json
{
  "effizienz": 1.0,
  "zweig": "damage",
  "boni": {
    "attack_bonus": 1.0,
    "crit_chance": 0.4
  },
  "skills": ["schleim_schlag", "gift_spucke"]
}
```

#### `GET /api/slime/spec/utility-boni/{slime_id}?level=20`
Berechnet aktuelle Utility-Boni.

#### `GET /api/slime/spec/stats`
Gibt System-Statistiken zurück.

### POST Endpoints

#### `POST /api/slime/spec/waehlen`
Wählt Haupt-Spezialisierung (ab Slime Level 10).

**Request:**
```json
{
  "slime_id": "slime123",
  "slime_level": 15,
  "spezialisierung": "kampf"
}
```

#### `POST /api/slime/spec/zweig`
Wählt Sub-Zweig (ab Spec-Level 5).

**Request:**
```json
{
  "slime_id": "slime123",
  "zweig_typ": "kampf",
  "zweig": "damage"
}
```

#### `POST /api/slime/spec/skill/lernen`
Lernt oder upgraded einen Skill.

**Request:**
```json
{
  "slime_id": "slime123",
  "skill_id": "schleim_schlag"
}
```

#### `POST /api/slime/spec/training/start`
Startet Spezialisierungs-Training.

**Request:**
```json
{
  "slime_id": "slime123",
  "training_typ": "kampf",
  "dauer_minuten": 60
}
```

#### `POST /api/slime/spec/training/beenden`
Beendet Training und gibt Belohnungen.

---

## 5. ALCHEMY SYSTEM

### GET Endpoints

#### `GET /api/alchemy/stats`
Gibt System-Statistiken zurück.

**Response:**
```json
{
  "zutaten_verfuegbar": 20,
  "rezepte_gesamt": 20,
  "spieler_aktiv": 5,
  "produkte_hergestellt_gesamt": 150,
  "meisterwerke_gesamt": 12,
  "explosionen_gesamt": 47
}
```

#### `GET /api/alchemy/spieler/{spieler_id}`
Gibt Spieler-Alchemie-Status zurück.

#### `GET /api/alchemy/rezepte/{spieler_id}`
Gibt alle bekannten Rezepte zurück.

#### `GET /api/alchemy/inventar/{spieler_id}`
Gibt Zutaten-Inventar zurück.

### POST Endpoints

#### `POST /api/alchemy/sammeln`
Sammelt eine Zutat.

**Request:**
```json
{
  "spieler_id": "player1",
  "zutat_id": "heilkraut",
  "menge": 3,
  "slime_bonus": 0.2
}
```

#### `POST /api/alchemy/herstellen`
Stellt ein Alchemie-Produkt her.

**Request:**
```json
{
  "spieler_id": "player1",
  "rezept_id": "kleiner_heiltrank",
  "slime_qualitaet_bonus": 0.1
}
```

**Response:**
```json
{
  "erfolg": true,
  "produkt": {
    "name": "Kleiner Heiltrank",
    "qualitaet": 4,
    "qualitaet_name": "GUT",
    "effekte": [{"typ": "heilung", "wert": 62}]
  },
  "exp_gewinn": 15,
  "ist_meisterwerk": false,
  "nachricht": "Gut gemacht! Kleiner Heiltrank (GUT) hergestellt."
}
```

#### `POST /api/alchemy/experimentieren`
Experimentiert mit Zutaten um Rezepte zu entdecken.

**Request:**
```json
{
  "spieler_id": "player1",
  "zutat_ids": ["schwefel", "schwefel", "salz"]
}
```

**Response (Erfolg):**
```json
{
  "erfolg": true,
  "entdeckt": true,
  "rezept": {
    "rezept_id": "kleine_bombe",
    "name": "Kleine Bombe"
  },
  "exp_gewinn": 55,
  "nachricht": "ENTDECKUNG! Du hast 'Kleine Bombe' entdeckt! 🎉"
}
```

**Response (Fehlschlag):**
```json
{
  "erfolg": true,
  "entdeckt": false,
  "fehlschlag": {
    "typ": "explosion",
    "nachricht": "PUFF! Dein Experiment explodiert in einer Rauchwolke..."
  },
  "exp_gewinn": 9
}
```

---

## FEHLER-CODES

| Code | Bedeutung |
|------|-----------|
| 200 | Erfolg |
| 400 | Ungültige Anfrage (fehlende Parameter) |
| 500 | Server-Fehler |
| 503 | System nicht verfügbar |

---

## ALLGEMEINE HINWEISE

1. **Alle Endpoints** erwarten/liefern JSON (UTF-8)
2. **spieler_id** fällt auf `STATE["user"]["id"]` zurück wenn nicht angegeben
3. **Slime-Boni** können bei Alchemy und Gathering angewendet werden
4. **Cooldowns** werden in Sekunden zurückgegeben
5. **Zeitstempel** sind Unix-Timestamps (float)

---

## BEISPIEL: KOMPLETTER ALCHEMY-WORKFLOW

```bash
# 1. Zutaten sammeln
POST /api/alchemy/sammeln
{"zutat_id": "heilkraut", "menge": 5}

# 2. Rezepte anschauen
GET /api/alchemy/rezepte/player1

# 3. Heiltrank herstellen
POST /api/alchemy/herstellen
{"rezept_id": "kleiner_heiltrank"}

# 4. Mit unbekannten Zutaten experimentieren
POST /api/alchemy/experimentieren
{"zutat_ids": ["schwefel", "feuerlilie", "feuer_essenz"]}

# 5. Status checken
GET /api/alchemy/spieler/player1
```

---

*"EXPLOSION!!! Diese APIs sind mächtiger als meine Magie!" - Najika* 💥
