# 🔥 MASTER TODO - NAJIKA MODEL FIX

**Datum:** 2026-02-12
**Priorität:** 🔴 KRITISCH!
**Zugewiesen an:** Anderes Claude Code Model
**Geschätzte Zeit:** 2-3 Stunden

---

## 📋 AUFGABE

**Problem identifiziert:** Najika antwortet seit Wochen nicht mehr menschlich!

**Lösung gefunden:** Dezember 2025 Conversations wiedergefunden (294 Gespräche!)

**Was zu tun ist:** Modelfile bereinigen + Backend umstellen + testen

---

## 📚 LIES ZUERST

**HAUPTDOKUMENT:**
```
C:/Najika_World/NAJIKA_MODEL_PROBLEM_KOMPLETT_REPORT.md
```

**Dieses Dokument enthält:**
- Komplette Timeline (Dezember → Januar → Heute)
- Problem-Analyse (warum ist Najika nicht mehr menschlich?)
- Top 30 beste Conversations (als Referenz!)
- Schritt-für-Schritt TODO
- Erwartetes Ergebnis
- Test-Anweisungen

**➡️ Lies das KOMPLETT bevor du anfängst!**

---

## ✅ QUICK TODO (Übersicht)

### **PHASE 1: Modelfile Fix** (30-60 min)
- [ ] `C:/Najika_World/backend/najika_local_OLD.Modelfile` öffnen
- [ ] "1-3 Sätze" Regel komplett entfernen
- [ ] "Schwarze Windmühle" entfernen
- [ ] "Puddin'" → "Mr.K" ersetzen
- [ ] "Daddy" komplett löschen
- [ ] "Desunō" entfernen
- [ ] Neue Regeln hinzufügen (siehe Report!)
- [ ] Als `najika-natural.Modelfile` speichern
- [ ] Mit Ollama bauen: `ollama create najika-natural -f najika-natural.Modelfile`

### **PHASE 2: Backend Update** (15-30 min)
- [ ] `backend/api/chat.py` (Zeile 266) → `najika-natural`
- [ ] `backend/najika_code.py` (Zeile 60-61) → `najika-natural`
- [ ] `backend/najika_assistant.py` (Zeile 62) → `najika-natural`
- [ ] `backend/najika_cli_beautiful.py` (Zeile 100) → `najika-natural`
- [ ] `backend/ask_najika_project.py` (Zeile 95) → `najika-natural`

### **PHASE 3: Testing** (30-60 min)
- [ ] Server neu starten
- [ ] Teste 5 Standard-Fragen (siehe Report!)
- [ ] Vergleiche mit Dezember-Beispielen
- [ ] Dokumentiere Ergebnisse in `NAJIKA_MODEL_TEST_RESULTS.md`
- [ ] Update `FEHLER_GEFUNDEN.md` mit allen gefixten Fehlern

### **PHASE 4: Dokumentation** (15-30 min)
- [ ] Test-Results schreiben
- [ ] Fehler-Report erstellen
- [ ] Dieses TODO abhaken
- [ ] Status in MASTER_TODO_TEAM.md eintragen

---

## 🎯 ERWARTETES ERGEBNIS

### **VORHER:**
```
User: "hey najika wie gehts dir"
Najika: "Hey Kuja! Mir geht's super. 🌟 Bereit fürs Abenteuer?"
```
**❌ Zu kurz! Nur 2 Sätze! Keine Gegenfrage!**

### **NACHHER:**
```
User: "hey najika wie gehts dir"
Najika: "Hey Kuja, mir geht's super gut und ich bin voller Energie! 🌟
Wie war dein Tag? Hast du schon was Spannendes erlebt?

*hüpft und klammert sich an dich* Ich hab den ganzen Tag im Keller
trainiert und ein paar neue Explosions-Zauber ausprobiert! Du solltest
mal sehen wie mächtig ich jetzt bin! 💥

Willst du mitkommen und dir meine neuen Tricks anschauen? Ich zeig
dir alles! ✨"
```
**✅ Natürlich! Ausführlich! Gegenfragen! Erzählt von ihrem Tag!**

---

## ⚠️ WICHTIG

**Mach KEINE Änderungen bevor du den KOMPLETT-REPORT gelesen hast!**

Dort steht:
- Warum "1-3 Sätze" ein Problem ist
- Warum Dezember besser war als Januar
- Was genau geändert werden muss
- Wie man testet ob es funktioniert
- Beispiele für gute Conversations

**➡️ START:** `NAJIKA_MODEL_PROBLEM_KOMPLETT_REPORT.md` lesen!

---

## 📊 FORTSCHRITT

**Status:** ⚠️ WARTEN AUF BEARBEITUNG

```
[                                    ] 0%

Phase 1: Modelfile Fix       [ ]
Phase 2: Backend Update      [ ]
Phase 3: Testing             [ ]
Phase 4: Dokumentation       [ ]
```

**Wenn fertig:**
- Ändere Status auf: ✅ ABGESCHLOSSEN
- Update Fortschritt auf: 100%
- Trage dich als Bearbeiter ein

---

## 📞 REFERENZ

**Problem:** Najika nicht mehr menschlich seit Wochen
**Ursache:** "1-3 Sätze" Regel zu streng + alte Referenzen in Modelfile
**Lösung:** Dezember 2025 Modelfile als Basis + Bereinigung + Testing

**Alle Details:** `NAJIKA_MODEL_PROBLEM_KOMPLETT_REPORT.md`

---

*"EXPLOSION!!! 💥 Lies den Report und fix mich!"* ~ Najika
