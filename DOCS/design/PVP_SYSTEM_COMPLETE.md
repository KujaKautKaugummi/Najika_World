# PVP-SYSTEM - VOLLSTÄNDIGE DOKUMENTATION
**Quelle:** Chat-Verlauf "111" (Zeile 47-61)
**Stand:** 2025-11-05
**Status:** OFFIZIELLES DESIGN (aus ursprünglicher Dokumentation)

---

## ✅ WICHTIG: DIES IST DAS ORIGINALE SYSTEM

Diese Dokumentation basiert auf dem **ursprünglichen Design** aus den Chat-Verläufen.
Ich habe es NICHT neu erfunden - es war schon da!

---

## 🎯 ÜBERSICHT: 3 PVP-MODI

Das PvP-System hat **DREI verschiedene Modi**, abhängig vom Spielmodus des Spielers:

1. **Hardcore-PvP** - Höchstes Risiko, Mercy-Option verfügbar
2. **Normal-PvP** - Mittleres Risiko, 1 Item-Verlust
3. **Softy-PvP** - Kein Risiko, nur Ranking

---

## 🔥 1. HARDCORE-PvP

### Grundmechanik
- **Spieler-Modus**: Beide Spieler im Hardcore-Modus
- **Risiko**: PERMADEATH möglich
- **Besonderheit**: "Alles-abgeben-um-zu-leben" Mercy-Option

### Ablauf bei Niederlage

#### Phase 1: Lethaler Treffer
```
Verteidiger HP → 0
System prüft: Hardcore-Modus aktiv?
→ JA: Mercy-Fenster öffnet sich
```

#### Phase 2: Mercy-Angebot (OPTIONAL)
```
Verteidiger erhält Prompt:
┌─────────────────────────────────────┐
│  DU WURDEST BESIEGT!                │
│                                      │
│  Möchtest du dein Leben retten?     │
│                                      │
│  [Alles abgeben um zu leben]        │
│  [Sterben (Permadeath)]             │
│                                      │
│  WARNUNG: Bei Annahme verlierst du  │
│  ALLES und erhältst 7 Tage PvP-Sperre│
└─────────────────────────────────────┘
```

**Wenn Verteidiger ANNIMMT:**
→ Weiter zu Phase 3

**Wenn Verteidiger ABLEHNT oder TIMEOUT:**
→ Normaler Tod (Permadeath)
→ Slime-Rettung möglich (falls verfügbar)
→ Totem-Item greift (falls vorhanden)

#### Phase 3: Angreifer-Entscheidung
```
Angreifer erhält Prompt:
┌─────────────────────────────────────┐
│  DEIN GEGNER BITTET UM GNADE!       │
│                                      │
│  Er bietet dir ALLES an um zu leben:│
│  - Gesamtes Inventar                │
│  - Alle Ausrüstung                  │
│  - Alle Ressourcen                  │
│                                      │
│  [Gnade gewähren (Alles nehmen)]   │
│  [Ablehnen (Töten)]                 │
└─────────────────────────────────────┘
```

**Wenn Angreifer AKZEPTIERT:**
→ Weiter zu Phase 4

**Wenn Angreifer ABLEHNT:**
→ Verteidiger stirbt (Permadeath)
→ Slime-Rettung möglich (falls verfügbar)

#### Phase 4: Explizite Bestätigung (DOPPEL-JA)
```
Verteidiger muss ZWEIMAL "JA" eingeben:

Erste Bestätigung:
┌─────────────────────────────────────┐
│  BIST DU SICHER?                    │
│                                      │
│  Du verlierst ALLES:                │
│  - Inventar (komplett)              │
│  - Ausrüstung (alles angelegt)      │
│  - Ressourcen (alle)                │
│  - 7 Tage PvP-Sperre                │
│                                      │
│  Tippe "JA" zum Bestätigen:         │
│  [____________]                     │
└─────────────────────────────────────┘

Zweite Bestätigung:
┌─────────────────────────────────────┐
│  LETZTE WARNUNG!                    │
│                                      │
│  Dies ist UNWIDERRUFLICH!           │
│  Du kannst NICHT zurück!            │
│                                      │
│  Tippe nochmal "JA":                │
│  [____________]                     │
└─────────────────────────────────────┘
```

**Nach DOPPEL-JA:**
1. **Alle Items transferiert** zu Angreifer
2. **Alle Ausrüstung transferiert** zu Angreifer
3. **Alle Ressourcen transferiert** zu Angreifer
4. Verteidiger erhält **7 Tage PvP-Sperre**
5. Verteidiger **überlebt** (kein Permadeath)
6. Verteidiger spawnt an letztem Safe-Point

### Was wird übertragen?
```python
HARDCORE_PVP_TRANSFER = {
    "inventory": "ALL",  # Komplettes Inventar
    "equipment": "ALL",  # Alle angelegten Items
    "resources": "ALL",  # Alle Materialien
    "currency": "ALL",   # Alles Gold/Währung
    "quest_items": "PROTECTED",  # Quest-Items bleiben!
    "starter_weapon": "PROTECTED"  # Starter-Waffe bleibt!
}
```

### 7-Tage PvP-Sperre
```
Nach Mercy-Rettung:
- 7 Tage IRL = KEINE PvP-Teilnahme möglich
- Schutz vor weiteren Angriffen
- Kann PvE spielen
- Kann handeln/craften
- KEIN Arena-PvP
- KEIN Open-World-PvP
```

### Anti-Missbrauch
```python
ANTI_ABUSE_CHECKS = {
    "double_confirmation": True,  # MUSS 2x JA tippen
    "timeout": 30,  # 30 Sekunden zum Entscheiden
    "combat_log": True,  # Alle Aktionen geloggt
    "fake_offer_detection": True,  # Erkennt Fake-Angebote
    "transfer_verification": True  # Verifiziert Item-Transfer
}
```

---

## ⚔️ 2. NORMAL-PVP (NICHT-HARDCORE)

### Grundmechanik
- **Spieler-Modus**: Mindestens EINER ist NICHT im Hardcore-Modus
- **Risiko**: 1 Ausrüstungsteil verlieren
- **Kein Permadeath-Risiko**

### Ablauf bei Niederlage

#### Verlierer-Perspektive
```
HP → 0
System: "Du wurdest besiegt!"

Automatischer Ablauf:
1. Gewinner wählt 1 Item aus DEINEM Loadout
2. Item wird transferiert
3. Du respawnst am Safe-Point
4. KEINE PvP-Sperre
```

#### Gewinner-Perspektive
```
Gewinner erhält Prompt:
┌─────────────────────────────────────┐
│  DU HAST GEWONNEN!                  │
│                                      │
│  Wähle 1 Ausrüstungsteil:           │
│                                      │
│  [Helm: Steel Helmet +15 DEF]       │
│  [Brust: Leather Armor +20 DEF]     │
│  [Waffe: Iron Sword +30 ATK]        │
│  [Schild: Wooden Shield +10 DEF]    │
│  [Boots: Traveler Boots +5 SPD]     │
│                                      │
│  [Nichts nehmen]                    │
└─────────────────────────────────────┘

Zeit-Limit: 60 Sekunden
```

### Was kann gewählt werden?
```python
NORMAL_PVP_SELECTABLE = {
    "equipped_items": "YES",  # Alle angelegten Items
    "inventory_items": "NO",  # NICHT Inventar
    "quest_items": "NO",  # NICHT Quest-Items
    "starter_items": "NO",  # NICHT Starter-Items
    "legendary_items": "YES",  # JA, auch Legendaries!
    "cursed_items": "YES_WITH_CURSE"  # Ja, aber Curse überträgt sich!
}
```

### Item-Drop Transfer
```
Gewähltes Item wird:
1. Aus Verlierer-Loadout entfernt
2. In Gewinner-Inventar gelegt (NICHT auto-equipped!)
3. Verlierer erhält Notification
4. Item-Durability bleibt erhalten
5. Enchantments bleiben erhalten
6. Sockets bleiben erhalten
```

### Keine PvP-Sperre
```
Nach Normal-PvP Niederlage:
- KEINE PvP-Sperre
- Kann sofort wieder PvP spielen
- Kann verlorenes Item zurückholen (durch erneuten Sieg)
```

---

## 🛡️ 3. SOFTY-PVP

### Grundmechanik
- **Spieler-Modus**: Mindestens EINER im Softy-Modus
- **Risiko**: KEIN Item-Verlust
- **Nur Ranking-System**

### Ablauf bei Niederlage
```
HP → 0
System: "Du wurdest besiegt!"

Automatischer Ablauf:
1. Ranking-Punkte werden angepasst
2. Statistics werden geupdatet
3. Respawn am Safe-Point
4. KEINE Item-Verluste
5. KEINE PvP-Sperre
```

### Ranking-System
```python
SOFTY_PVP_RANKING = {
    "winner_points": +25,  # Gewinner erhält Punkte
    "loser_points": -10,   # Verlierer verliert weniger
    "draw_points": +5,     # Bei Draw beide +5
    "afk_penalty": -50,    # AFK = hohe Strafe
    "disconnect_penalty": -30  # Disconnect = mittlere Strafe
}
```

### Was wird NICHT verloren?
```
SOFTY-PVP garantiert:
✓ Alle Items bleiben
✓ Alle Ausrüstung bleibt
✓ Alle Ressourcen bleiben
✓ Kein Permadeath-Risiko
✓ Keine PvP-Sperre
✓ Nur EGO-Verlust 😄
```

---

## 🎮 PVP-MODI VERGLEICH

| Feature | Hardcore-PvP | Normal-PvP | Softy-PvP |
|---------|--------------|------------|-----------|
| **Item-Verlust** | ALLES (mit Mercy) | 1 Item | NICHTS |
| **Permadeath** | JA | NEIN | NEIN |
| **PvP-Sperre** | 7 Tage (bei Mercy) | KEINE | KEINE |
| **Mercy-Option** | JA | NEIN | NEIN |
| **Doppel-JA** | JA | NEIN | NEIN |
| **Ranking** | Optionalsearch (separates HC-Ranking) | JA | JA |
| **Slime-Rettung** | JA | NEIN | NEIN |
| **Totem-Item** | JA | NEIN | NEIN |

---

## 🔒 ANTI-MISSBRAUCH REGELN

### Hardcore-PvP Schutz
```python
HARDCORE_PROTECTION = {
    "no_guests": True,  # Keine Gäste in HC-Zonen
    "double_confirmation": True,  # Muss 2x JA tippen
    "timeout_window": 30,  # 30 Sek. Entscheidungszeit
    "combat_log": True,  # Vollständiges Kampf-Log
    "fake_offer_detection": True,  # Erkennt Fake-Mercy
    "transfer_verification": True,  # Verifiziert Transfer
    "cooldown_enforcement": True,  # 7-Tage Sperre wird durchgesetzt
    "zone_restrictions": True  # Hardcore-Zonen getrennt
}
```

### Normal-PvP Schutz
```python
NORMAL_PROTECTION = {
    "selection_timeout": 60,  # 60 Sek. zum Item wählen
    "item_binding_check": True,  # Bound Items nicht wählbar
    "quest_item_protection": True,  # Quest-Items geschützt
    "starter_protection": True,  # Starter-Items geschützt
    "minimum_level_check": True  # Nur Items ≥ Level 10
}
```

### Softy-PvP Schutz
```python
SOFTY_PROTECTION = {
    "no_item_transfer": True,  # Garantiert keine Verluste
    "afk_detection": True,  # Erkennt AFK
    "stat_padding_detection": True,  # Erkennt Stat-Padding
    "disconnect_penalty": True  # Bestraft Rage-Quits
}
```

---

## 🎯 IMPLEMENTIERUNGS-HINWEISE

### Python Backend Pseudo-Code

```python
class PvPSystem:
    """
    Vollständiges PvP-System mit 3 Modi
    """

    PVP_MODES = {
        "hardcore": "HARDCORE_PVP",
        "normal": "NORMAL_PVP",
        "softy": "SOFTY_PVP"
    }

    def determine_pvp_mode(self, player_a, player_b):
        """
        Bestimmt PvP-Modus basierend auf Spieler-Status
        """
        if player_a.mode == "hardcore" and player_b.mode == "hardcore":
            return "hardcore"
        elif player_a.mode == "softy" or player_b.mode == "softy":
            return "softy"
        else:
            return "normal"

    def handle_defeat_hardcore(self, loser, winner):
        """
        Hardcore-PvP Niederlage
        """
        # Phase 1: Prüfe Mercy-Verfügbarkeit
        if not loser.can_offer_mercy():
            return self.apply_permadeath(loser)

        # Phase 2: Mercy-Angebot
        loser_choice = loser.show_mercy_prompt(timeout=30)

        if loser_choice == "die":
            return self.apply_permadeath(loser)

        # Phase 3: Angreifer-Entscheidung
        winner_choice = winner.show_mercy_accept_prompt(
            loser_items=loser.get_all_items(),
            timeout=30
        )

        if winner_choice == "reject":
            return self.apply_permadeath(loser)

        # Phase 4: Doppel-Bestätigung
        confirm_1 = loser.ask_confirmation("JA", timeout=20)
        if not confirm_1:
            return self.apply_permadeath(loser)

        confirm_2 = loser.ask_confirmation("JA", timeout=20)
        if not confirm_2:
            return self.apply_permadeath(loser)

        # Transfer ALLES
        self.transfer_all_items(loser, winner)
        self.apply_pvp_cooldown(loser, days=7)
        loser.respawn_at_safe_point()

        return {
            "result": "mercy_granted",
            "loser_survived": True,
            "items_transferred": loser.get_all_items(),
            "pvp_cooldown": 7
        }

    def handle_defeat_normal(self, loser, winner):
        """
        Normal-PvP Niederlage
        """
        # Gewinner wählt 1 Item
        selectable = loser.get_equipped_items(
            exclude_quest=True,
            exclude_starter=True
        )

        chosen_item = winner.select_item_from_list(
            items=selectable,
            timeout=60
        )

        if chosen_item:
            self.transfer_item(loser, winner, chosen_item)

        loser.respawn_at_safe_point()

        return {
            "result": "normal_defeat",
            "item_lost": chosen_item.name if chosen_item else None
        }

    def handle_defeat_softy(self, loser, winner):
        """
        Softy-PvP Niederlage
        """
        # Nur Ranking anpassen
        loser.adjust_ranking(-10)
        winner.adjust_ranking(+25)
        loser.respawn_at_safe_point()

        return {
            "result": "softy_defeat",
            "ranking_change": -10
        }

    def transfer_all_items(self, from_player, to_player):
        """
        Transferiert ALLES (außer Quest-Items + Starter)
        """
        items = from_player.get_all_transferable_items()

        for item in items:
            if item.is_quest_item or item.is_starter:
                continue  # Skip protected items

            from_player.remove_item(item)
            to_player.add_item(item)

            # Log transfer
            self.log_transfer(from_player, to_player, item)
```

---

## 📝 ZUSAMMENFASSUNG

Das PvP-System bietet **3 klar getrennte Modi**:

1. **Hardcore-PvP**:
   - Höchstes Risiko (ALLES verlieren)
   - Mercy-System mit Doppel-Bestätigung
   - 7-Tage PvP-Sperre bei Rettung
   - Für ultimativen Nervenkitzel

2. **Normal-PvP**:
   - Moderates Risiko (1 Item verlieren)
   - Gewinner wählt Item
   - Keine PvP-Sperre
   - Balanciertes Risiko-Belohnung

3. **Softy-PvP**:
   - Kein Risiko (nur Ranking)
   - Perfekt zum Üben
   - Keine Item-Verluste
   - Casualfreundlich

**Kernphilosophie**:
"Jeder Spielmodus hat seinen eigenen PvP-Stil - vom entspannten Ranking-Kampf bis zum ultimativen Alles-oder-Nichts-Duell."

---

**Ende Dokumentation**

*Quelle: Chat-Verlauf "111" - Originales Design*
*Dokumentiert: 2025-11-05*
*Status: Offiziell*
