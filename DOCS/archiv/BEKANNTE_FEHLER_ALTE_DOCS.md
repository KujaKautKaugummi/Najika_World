# BEKANNTE FEHLER IN ALTEN DOKUMENTATIONEN
**Stand:** 2026-02-21
**Zweck:** Warnung fuer alle Models die alte MDs lesen

---

## WARUM DIESES DOKUMENT?

Das alte AI-Model auf dem alten PC hat "zum Schluss nur Scheisse gemacht und vieles
vertauscht" (Zitat Kuja). Viele Dokumentations-Dateien enthalten dadurch FALSCHE
Informationen. Dieses Dokument listet die haeufigsten Fehler.

---

## FALSCHE BEHAUPTUNGEN IN ALTEN DOCS

### 1. "12 Backend-Module fehlen"
**Steht in:** COMPLETE_CODE_AUDIT_2026-02-15.md, MISSING_DEPENDENCIES_AUDIT_2026-02-16.md,
SESSION_SONNET_2026-02-16_ROUND3_FINAL.md, OPUS_KOMPLETTES_WISSEN_2026-02-17.md
**Wahrheit:** ALLE 12 Module existieren und haben hunderte/tausende Zeilen Code!
Das alte Model hat nie `ls` oder `find` ausgefuehrt um die Dateien zu pruefen.

### 2. "Port 8001" oder "Port 5000"
**Steht in:** CLAUDE.md (alt), diverse Session-Logs
**Wahrheit:** Port 8000. Immer gewesen. najika_server.py Zeile 364.

### 3. "ChromaDB hat 2556 Eintraege"
**Steht in:** CLAUDE.md (alt)
**Wahrheit:** ~95 Eintraege in 2 Collections (najika_personalities: 83, najika_core: 12)

### 4. "Flask + FastAPI Dual Server"
**Steht in:** Diverse Architektur-Docs
**Wahrheit:** Ein einziger Server: najika_server.py mit ThreadingHTTPServer.
main_fastapi.py existiert aber wird NICHT gestartet.

### 5. "LoRA/Fine-Tuning aktiv"
**Steht in:** CLAUDE.md (alt), MASTER_TODO_TEAM.md
**Wahrheit:** Keine LoRA, kein Fine-Tuning. Nur Ollama Modelfiles mit Few-Shot.

### 6. "Qwen2.5-7B" oder "qwen2-instruct:latest"
**Steht in:** CLAUDE.md (alt), diverse Docs
**Wahrheit:** qwen2:7b (Chat), dolphin3:8b (NSFW), keine "2.5" oder "instruct" Varianten.

### 7. "4 separate Persoenlichkeiten"
**Steht in:** Aeltere Persoenlichkeits-Docs
**Wahrheit:** 1 Persoenlichkeit (Megumin) mit 4 situativen Facetten.
Siehe: NAJIKA_IDENTITAET_DEFINITION.md (kanonisch!)

### 8. "Slime Evolution V2"
**Steht in:** Aeltere Slime-Docs
**Wahrheit:** V3 ist aktiv. Evolution/Synthese entfernt. Formwandler-System.
Siehe: SLIME_SYSTEM_V3_DOKUMENTATION.md

### 9. "8 Gebote V2"
**Steht in:** CLAUDE.md (alt)
**Wahrheit:** V3 ist aktuell (2026-02-17). Wesentliche Aenderungen:
- Friendly Fire AN (war OFF)
- NSFW Remote fuer Kuja (war nur lokal)
- Wissensdatenbank statt Privacy-Paranoia
- "Keine halben Sachen" statt "Offline-First"

---

## WELCHE DOCS SIND VERTRAUENSWUERDIG?

### Sicher korrekt (Stand 2026-02-21):
- CLAUDE.md (NEU GESCHRIEBEN 2026-02-21)
- NAJIKA_KOMPLETT_UEBERSICHT.md (NEU 2026-02-21)
- MASTER_TODO.md (NEU 2026-02-21)
- 01_8_GEBOTE_V3_2026-02-17.md
- NAJIKA_IDENTITAET_DEFINITION.md (2026-02-06)
- SLIME_SYSTEM_V3_DOKUMENTATION.md (2026-02-04)
- PERSONALITY_ENGINE_PSYCHOLOGIE_FINAL.md (2026-02-12)

### Mit Vorsicht lesen (teilweise korrekt):
- Session-Logs (korrekte Aktionen aber falsche Analysen)
- MASTER_TODO_TEAM.md (Tasks korrekt, technische Details teilweise falsch)
- FEATURES_KOMPLETT_STATUS.md (Status-Checks veraltet)
- BACKEND_COMPLETE_API_REFERENCE.md (API-Struktur ggf. veraltet)

### NICHT vertrauen (nachweislich falsch):
- COMPLETE_CODE_AUDIT_2026-02-15.md (behauptet Module fehlen)
- MISSING_DEPENDENCIES_AUDIT_2026-02-16.md (gleiches Problem)
- OPUS_KOMPLETTES_WISSEN_2026-02-17.md (~40% falsch)
- Alle Docs die Port 8001/5000 nennen
- Alle Docs die ChromaDB >100 Eintraege nennen
- Alle Docs die LoRA/Fine-Tuning erwaehnen

---

## REGEL FUER NEUE MODELS

**IMMER Code pruefen vor Behauptungen!**
- `ls` ausfuehren bevor "Datei fehlt" gesagt wird
- `grep` nutzen bevor "Funktion existiert nicht" gesagt wird
- Port im Code pruefen (najika_server.py Zeile 364)
- ChromaDB mit check_chromadb.py pruefen

---

**Letzte Aktualisierung:** 2026-02-21
