# NAJIKA WORLD - KREATUR-SYSTEM KONZEPT
**Erstellt:** 2026-02-08
**Status:** DESIGN-DOKUMENT - Basis für Implementation

---

## KERN-IDEE: 2 KREATUR-KATEGORIEN

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    2 KREATUR-KATEGORIEN                                       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   KATEGORIE 1: "LEBENDE" (Anime-Style NPCs)                                 ║
║   ═════════════════════════════════════════                                   ║
║   → Haben VERSTAND, Persönlichkeit, können sprechen                         ║
║   → Sind wie NPCs, nur nicht in Menschenform                                ║
║   → Der sprechende Goblin, der weise Baumgeist, der freche Feuerfuchs      ║
║   → Können ANGEWORBEN werden (Geld, Ruf, Schutz, Freundschaft)             ║
║   → Oder als Sklaven gehalten & zum Schuften gezwungen werden               ║
║   → Droppen SELTENE Ressourcen beim Töten                                   ║
║   → ABER: Willst du den süßen sprechenden Hasen wirklich töten              ║
║     für den Edelstein den du eh selten brauchst?                            ║
║   → Alternative: Stein länger farmen (dauert mehr, aber kein Töten)         ║
║                                                                               ║
║   KATEGORIE 2: "VIEH" (Minecraft-Style Tiere)                               ║
║   ═════════════════════════════════════════                                   ║
║   → Kein Verstand, einfache Tiere/Kreaturen                                ║
║   → Können GEZÄHMT werden (Füttern, Zeit, Geduld - KEIN Pokeball!)         ║
║   → Standard-Ressourcen (Fleisch, Leder, Milch, Eier, Wolle)              ║
║   → Kein moralisches Dilemma - normales Farming                            ║
║   → Wie Kühe, Hühner, Schafe in Minecraft                                  ║
║                                                                               ║
║   WARUM BEIDES?                                                              ║
║   ═════════════                                                              ║
║   Nur Kat.1 → Jeder Schritt = existenzielle Frage → ZU VIEL!              ║
║   Nur Kat.2 → Langweilig, keine Tiefe                                      ║
║   Beides   → Perfekte Balance! Normal farmen geht easy,                    ║
║              aber für seltene Drops: Farme ich länger                       ║
║              ODER töte ich den süßen Goblin?                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## KATEGORIE 1: LEBENDE KREATUREN (Anime-NPCs)

### Was macht sie besonders?
- Sie REDEN mit dir
- Sie haben NAMEN, PERSÖNLICHKEIT, ERINNERUNGEN
- Sie REAGIEREN auf dein Verhalten
- Sie können FREUND oder FEIND werden
- Sie können FÜR dich ARBEITEN oder als SKLAVEN gehalten werden
- Manche BITTEN um Hilfe, erzählen Geschichten, geben Quests
- Sie haben ein LEBEN - schlafen, essen, wandern umher

### Interaktionsmöglichkeiten

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INTERAKTION MIT LEBENDEN KREATUREN                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   FRIEDLICH:                                                                │
│   ──────────                                                                │
│   → REDEN - Dialog, Infos, Geschichten, Gerüchte                          │
│   → ANWERBEN - Mit Gold, gutem Ruf, Schutz-Versprechen                    │
│     → Angeworbene Kreatur ARBEITET für dich (freiwillig!)                  │
│     → Gibt regelmäßig seltene Ressourcen OHNE zu sterben                  │
│     → Kann kämpfen, sammeln, wachen, kochen etc.                          │
│   → HANDELN - Tauschen, kaufen, verkaufen                                 │
│   → BEFREUNDEN - Geschenke, Quests erfüllen, Ruf aufbauen                │
│                                                                              │
│   GEWALTSAM:                                                                │
│   ───────────                                                               │
│   → TÖTEN - Seltene Drops! Aber die Kreatur ist dann WEG                  │
│     → Andere lebende Kreaturen in der Nähe SEHEN das!                     │
│     → Dein Ruf leidet bei friedlichen Kreaturen                           │
│   → VERSKLAVEN - Zwangsarbeit, Kreatur hasst dich                        │
│     → Produziert weniger als angeworbene (unmotiviert)                    │
│     → Kann fliehen! (Fluchtversuch je nach Behandlung)                   │
│     → Andere NPCs/Kreaturen reagieren negativ                            │
│   → JAGEN - Auf dem Feld angreifen, Loot kassieren                       │
│                                                                              │
│   DAS MORALISCHE DILEMMA:                                                   │
│   ──────────────────────                                                    │
│   Der Edelstein-Goblin "Glimmer" sitzt friedlich vor seiner Höhle.        │
│   Er hat einen seltenen Kristall den du für dein Schwert brauchst.        │
│                                                                              │
│   Option A: Töte Glimmer → Kristall sofort! Aber Glimmer ist tot.        │
│   Option B: Freunde dich an → Glimmer gibt dir Kristalle über Zeit       │
│   Option C: Farm den Kristall in der Mine → 2 Stunden statt 5 Minuten   │
│   Option D: Versklave Glimmer → Er gräbt für dich, hasst dich aber      │
│                                                                              │
│   KEIN automatisches Gewissens-System!                                      │
│   Der Spieler entscheidet FREI. Die WELT reagiert.                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Aufstiegssystem (Nemesis-Style!)
- JEDE lebende Kreatur kann zum König aufsteigen!
- Ein Goblin der genug Kämpfe überlebt wird zum Goblin-König
- Ein Slime der stark genug wird kann andere Slimes anführen
- Funktioniert mit dem bestehenden Nemesis-System
- Spieler können Kreaturen beim Aufstieg HELFEN oder VERHINDERN

### Seltene Drops (NUR bei Kategorie 1!)

| Kreatur | Seltener Drop | Verwendung | Alternative Farm-Methode |
|---------|---------------|------------|--------------------------|
| Kristall-Goblin | Reiner Kristall | Waffen-Enchant | Tiefenhöhlen minen (2h) |
| Feuerfuchs | Flammenessenz | Feuer-Infuse | Magmaströme sammeln (1.5h) |
| Mooselefant | Lebensmoos | Heal-Potion+ | Samtmoos Kräuter (3h) |
| Singvogel-Fee | Melodie-Feder | Barden-Item | Quest-Belohnung |
| Eisenbart-Zwerg | Meisterstahl | Beste Waffen | Schmieden Lvl 40+ |

### Anwerben vs Töten (Wirtschaftlich)

```
TÖTEN:
  + Sofortige seltene Ressource
  + Schnell und einfach
  - Kreatur ist permanent weg (respawnt als NEUE Persönlichkeit)
  - Ruf beim GANZEN CLAN sinkt! (Gerüchte breiten sich aus!)
  - Überjagung → weniger Spawns → Ökosystem-Kettenreaktion
  - Clan wird feindlich nach zu vielen Kills → greifen DICH an!
  - Keine langfristige Ressourcen-Quelle

ANWERBEN:
  + Langfristige Ressourcen-Produktion
  + Kann kämpfen/arbeiten/wachen
  + Ruf bei anderen Kreaturen steigt
  - Kostet Gold/Zeit/Ruf zum Anwerben
  - Muss versorgt werden (Essen, Unterkunft)
  - Produziert WENIGER pro Einheit als Töten-Drop

VERSKLAVEN:
  + Keine Anwerbe-Kosten
  + Zwangsarbeit
  - Produziert am WENIGSTEN (unmotiviert)
  - Fluchtgefahr (je schlechter behandelt, desto höher)
  - Ruf-Katastrophe bei Entdeckung
  - Andere Spieler können Sklaven BEFREIEN
  - Funktioniert genauso wie bei menschlichen NPCs!
```

---

## KATEGORIE 2: VIEH-KREATUREN (Minecraft-Tiere)

### Was macht sie aus?
- Kein Verstand, keine Sprache
- Einfache Tiere / Fantasy-Vieh
- Reagieren nur auf Grundreize (Hunger, Gefahr, Paarung)
- Standard-Farming-Ressourcen
- Kein moralisches Dilemma beim Töten/Nutzen

### Zähmen (NICHT Fangen!)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ZÄHMEN (Kein Pokemon! Kein Pokeball!)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ABLAUF:                                                                   │
│   ────────                                                                  │
│   1. Kreatur in der Wildnis finden                                         │
│   2. Nähern (langsam! Rennen verscheucht!)                                 │
│   3. Füttern mit Lieblingsessen                                            │
│   4. Wiederholen über mehrere Tage → Vertrauen aufbauen                   │
│   5. Kreatur folgt dir → Gezähmt!                                         │
│   6. Zum Stall/Farm bringen                                                │
│                                                                              │
│   KEIN:                                                                     │
│   → Käfig werfen                                                           │
│   → Bewusstlos schlagen und mitnehmen                                     │
│   → Sofort-Fang-Mechanik                                                  │
│   → Pokeball oder ähnliches                                               │
│                                                                              │
│   FAKTOREN:                                                                 │
│   → Richtiges Futter (jede Art mag anderes)                               │
│   → Tageszeit (manche nur nachts/tags aktiv)                              │
│   → Geduld (1-7 Tage je nach Tier-Seltenheit)                            │
│   → Tier-Pflege Skill (Learning by Doing!)                                │
│   → Manche Tiere brauchen VERTRAUEN (können nicht beim                    │
│     ersten Mal gezähmt werden)                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Vieh-Nutzung

| Nutzung | Beschreibung |
|---------|--------------|
| **Fleisch** | Schlachten → Nahrung + Leder/Knochen |
| **Milch/Eier** | Regelmäßig ohne Töten |
| **Wolle/Federn** | Scheren/Sammeln |
| **Reittier** | Manche können geritten werden |
| **Lasttier** | Karawanen-Transport |
| **Zucht** | 2 gleiche Tiere → Nachwuchs! |

### Beispiel-Vieh pro Biom

| Biom | Vieh | Ressource |
|------|------|-----------|
| Samtmoos | Moos-Kuh, Pilz-Huhn | Milch, Eier, Pilzsporen |
| Heisse Dünen | Sand-Kamel, Dünen-Echse | Leder, Fleisch, Eier |
| Salzwind | Strand-Schaf, Fisch-Reiher | Wolle, Federn, Fisch |
| Magmaströme | Vulkan-Bock, Asche-Huhn | Feuer-Wolle, Hitze-Eier |
| Grünschlamm | Sumpf-Schwein, Moor-Ente | Fett, Federn, Moor-Eier |
| Blitzebene | Donner-Pferd, Sturm-Falke | Reittier!, Federn |
| Tiefenhöhlen | Kristall-Käfer, Höhlen-Fledermaus | Erze, Guano (Dünger!) |
| Reich der Drei | Stadtkatze, Hofhund | Companionship, Wache |

---

## MONSTER-ZAHLEN ZIEL

```
AKTUELL (Starter):
  8 Monster pro Biom × 8 Biome = 64 Kreaturen (Kategorie 1)
  + Götterfels Exklusive = 10
  = 74 Kategorie-1 Kreaturen

ZIEL (Endgame):
  64 Kreaturen pro Biom × 8 Biome = 512 Kategorie-1 Kreaturen
  + Götterfels Exklusive
  + Dungeon-Exklusive
  + Event-Exklusive
  = 600+ Kategorie-1 Kreaturen

  ~20 Vieh-Arten pro Biom × 8 Biome = 160 Kategorie-2 Kreaturen

  GESAMT ZIEL: ~760+ einzigartige Kreaturen!
```

---

## ZUSAMMENSPIEL MIT ANDEREN SYSTEMEN

### Fraktionssystem - LEBENDIGE KREATUR-CLANS!

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KREATUR-CLAN REPUTATION                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Jede Kat.1 Spezies bildet einen CLAN (= Mini-Fraktion!)                  │
│   → Goblin-Stamm, Feuerfuchs-Rudel, Baumgeist-Hain etc.                  │
│   → Clans haben EIGENEN Ruf-Wert zum Spieler                              │
│   → Clans REDEN untereinander! (Gerüchte breiten sich aus!)              │
│                                                                              │
│   BEISPIEL - GOBLIN-JAGD:                                                   │
│   ────────────────────────                                                  │
│   Tag 1: Du tötest 1 Goblin für seinen Kristall                           │
│     → Goblins in der Nähe SEHEN das → leicht misstrauisch                 │
│                                                                              │
│   Tag 3: Du tötest 3 weitere Goblins                                       │
│     → Goblin-Stamm wird VORSICHTIG → Goblins meiden dich                  │
│     → Du hörst Goblin-Flüstern: "Der da... der tötet unsere Brüder!"     │
│                                                                              │
│   Tag 7: Du hast 10+ Goblins getötet                                       │
│     → Goblin-Stamm ist FEINDLICH → Goblins greifen DICH an!              │
│     → Goblin-König stellt Kopfgeld auf DICH!                              │
│     → Andere Kreatur-Clans hören davon (Gerüchte!)                        │
│     → Feuerfüchse werden auch vorsichtiger                                │
│                                                                              │
│   UMGEKEHRT - FREUNDSCHAFT:                                                │
│   ─────────────────────────                                                 │
│   → Goblins helfen? → Stamm wird FREUNDLICH                               │
│   → Freundlicher Clan = bessere Handelspreise                              │
│   → Freundlicher Clan warnt dich vor Gefahren                             │
│   → Freundlicher Clan bietet Quests & seltene Items                       │
│   → Bei hohem Ruf: Clan-Mitglieder BIETEN sich zum Anwerben an!          │
│                                                                              │
│   GERÜCHTE-SYSTEM:                                                          │
│   ─────────────────                                                         │
│   → Goblins erzählen Feuerfüchsen dass du gefährlich bist                 │
│   → Feuerfüchse erzählen Baumgeistern                                     │
│   → Gerüchte breiten sich über ZEIT aus (nicht sofort!)                    │
│   → Gerüchte verfallen langsam (Vergessen nach Wochen)                    │
│   → Gute Taten überschreiben schlechte Gerüchte (langsam!)               │
│                                                                              │
│   ÖKOLOGISCHES GLEICHGEWICHT:                                               │
│   ───────────────────────────                                               │
│   → Überjagung einer Art → weniger Spawns in der Region!                  │
│   → Weniger Goblins → deren Feinde (Spinnen?) breiten sich aus            │
│   → Ökosystem reagiert auf Spieler-Aktionen                               │
│   → Population erholt sich über Wochen                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Wirtschaft
- Seltene Kreatur-Drops = Teil der Wirtschaft
- Angeworbene Kreaturen können als Händler arbeiten
- Vieh-Produkte = Basis-Wirtschaftsgüter
- Überjagung einer Region → Weniger Spawns → Preis steigt!

### Survival
- Vieh-Fleisch = Hunger stillen
- Reittiere = Schnelleres Reisen (weniger Überfälle?)
- Lasttiere = Mehr Handelskapazität
- Wach-Tiere = Reduzieren Überfall-Risiko beim Schlafen!

### Graue Moral (Wahre Freiheit!)
- Töte die süße Fee → Seltener Drop, aber Fee tot. KEIN Gewissensbiss!
- Versklave den Goblin → Billige Arbeit, aber Ruf leidet. KEIN Gewissensbiss!
- Die WELT reagiert (Fraktionen, NPCs, Preise, Kopfgeld)
- Der CHARAKTER nicht (wahre Freiheit!)

### Nemesis System
- Jede lebende Kreatur kann zum "Nemesis" werden
- Ein Goblin den du verwundet aber nicht getötet hast → kommt mit Narben zurück
- Wird stärker, hat Grudge, erinnert sich an dich
- Kann zum Goblin-KÖNIG aufsteigen!

### Character & Companion System
- Slime-Begleiter = separates System (nicht verwechseln!)
- Slime sieht aus WIE ein Kategorie-1 Monster, IST aber ein Slime
- Angeworbene Kreaturen ≠ Slime-Begleiter
- Angeworbene Kreaturen = Arbeiter/Kämpfer in deiner Siedlung

---

## SLIME vs ANGEWORBENE KREATUR vs GEZÄHMTES VIEH

```
┌────────────────────┬──────────────────┬──────────────────┬──────────────────┐
│                     │ SLIME-BEGLEITER  │ ANGEWORBENE      │ GEZÄHMTES VIEH  │
│                     │ (jeder Spieler)  │ KREATUR (Kat.1)  │ (Kat.2)         │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Was ist es?         │ Dein persönl.    │ NPC der für dich │ Tier auf deiner │
│                     │ Begleiter        │ arbeitet         │ Farm            │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Folgt dir?          │ IMMER            │ Optional (Befehl)│ Bleibt am Stall │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Kämpft?             │ JA (V-Pet)       │ JA (NPC-KI)      │ NEIN            │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Formenwechsel?      │ JA (Training)    │ NEIN             │ NEIN            │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Limit?              │ 1 pro Spieler    │ Abhängig von Ruf │ Abhängig v. Farm│
│                     │                  │ & Charisma       │ Größe           │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Ressourcen?         │ Keine direkt     │ Seltene Drops    │ Basis-Ressourcen│
│                     │                  │ (regelmäßig)     │ (Milch, Eier..) │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Verstand?           │ KI (LLM)        │ JA (NPC-KI)      │ NEIN            │
├────────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Kann sterben?       │ NEIN (unsterblich│ JA (permanent!)  │ JA              │
│                     │ aber kann krank  │                  │                  │
│                     │ werden)          │                  │                  │
└────────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

---

## IMPLEMENTATION PLAN

### Phase 1: Kategorie-System in monster_registry.js
- Jedes Monster bekommt `category: 'lebend'` oder `category: 'vieh'`
- Lebende Kreaturen: Persönlichkeit, Dialog, Anwerbe-Interface
- Vieh: Zähm-Mechanik, Farm-Produktion, Zucht

### Phase 2: Zähm-System (creature_taming.js)
- Kategorie-2 Vieh zähmen (Füttern → Vertrauen → Folgen → Farm)
- KEIN Pokeball! Geduldiges Anfreunden über Tage
- Tier-Pflege Skill (Learning by Doing)

### Phase 3: Anwerbe-System (creature_recruit.js)
- Kategorie-1 Kreaturen anwerben (Dialog, Bestechung, Ruf, Quests)
- Sklaven-Mechanik (wie bei menschlichen NPCs)
- Flucht-System für Sklaven
- Arbeits-Zuweisung (Mine, Farm, Wache, Kampf)

### Phase 4: Farm-System (creature_farm.js)
- Vieh-Ställe bauen (Integration mit Building System)
- Zucht-Mechanik (2 gleiche Tiere → Nachwuchs)
- Ressourcen-Produktion (täglich Milch, Eier etc.)
- Futter-Management

### Phase 5: Erweiterung auf 64 pro Biom
- Monster-Registry von 8 auf 64 pro Biom erweitern
- Vieh-Registry erstellen (20 pro Biom)
- Spawn-Tabellen anpassen
- Biom-spezifische Zucht-Kombinationen

---

## ARBEITSTEILUNG

| Task | Zuständig | Priorität |
|------|-----------|-----------|
| Konzept finalisieren (DIESES DOKUMENT) | DONE | - |
| `category` Feld zu monster_registry.js | OPUS-1 | P1 |
| Vieh-Kreaturen Registry | OPUS-1 | P1 |
| Zähm-System (creature_taming.js) | OPUS-1 | P1 |
| Anwerbe-System (creature_recruit.js) | OPUS-1 | P2 |
| Sklaven-Mechanik | OPUS-1 | P2 |
| Farm-System (creature_farm.js) | OPUS-1 | P2 |
| Kreatur-UI (Zähmen, Anwerben, Farm) | OPUS-2 | P2 |
| Monster auf 64/Biom erweitern | OPUS-1+2 | P3 |
| Vieh-Modelle (3D) | OPUS-2 | P3 |

---

*"Manche Monster verdienen es geliebt zu werden. Andere verdienen es gegessen zu werden. Der Spieler entscheidet." - Najika World Design Philosophy*
