# Najika Combat V4 - Immersives Kampfsystem Design

**Datum:** 2026-02-23
**Status:** APPROVED
**Kern-Philosophie:** Du spielst DICH SELBST. Dein echtes Skill zaehlt. Keine UI-Kruecken - echte Bewegungen.
**Spieler-Identitaet:** Der Spieler IST er/sie selbst - NICHT Najika. Najika ist die KI-Begleiterin (= Slime fuer andere Spieler).

**Kampf-Inspirationen:** For Honor (Richtungs-Kampf) + Fortnite (Kamera-relatives Movement) + Hogwarts Legacy (Zauber-System)
**Welt-Inspirationen:** 1883 + Fallout New Vegas + Oregon Trail + KonoSuba + Borderlands

---

## 0. Welt-DNA: Das Fundament aller Designentscheidungen

**DIESE SEKTION IST HEILIG.** Jede Mechanik, jeder System-Entscheid, jede Balance-Frage wird gegen diese DNA gemessen.

### 0.1 Die fuenf Saeulen

**1883 - Die Frontier-Haerte**
Die Welt ist nicht gegen dich - sie interessiert sich schlicht nicht fuer dich.
- Du baust etwas aus NICHTS. Kein Sicherheitsnetz.
- Der Fluss ist wunderschoen und toetet dich trotzdem.
- Tod hat Gewicht. Wenn jemand aus deiner Gruppe stirbt ist das nicht abstrakt.
- Neue Gebiete sind wirklich uncharted - kein NPC der dir sagt was dort ist.
- Andere Voelker (Goblins, etc.) haben echte Ansprueche auf Land - keine "Quest-Marker-Feinde".
- Schoenheit und Brutalitaet gleichzeitig. Immer.
- *Najikas Ton wenn du in der Wildnis bist und gerade jemanden verloren hast: diese melancholische Poesie vom Sterben und Weitermachen.*

**Fallout New Vegas - Die Graue Moral**
Es gibt keine gute Seite. Jeder hat eine Agenda.
- Du kannst mit JEDEM arbeiten - auch mit dem "Boesen".
- Jede Fraktion hat valide Argumente UND echte Schatten.
- Konsequenzen deiner Entscheidungen holen dich ein - aber nicht sofort, und nicht immer wie erwartet.
- Haendler, Schurken, Koepfe-Abschneider - alle koennen Gebietsherrscher werden.
- *"War... war never changes."* Macht wechselt die Haende aber das Spiel bleibt gleich.

**Oregon Trail - Der Reise-Realismus**
Die Reise selbst ist der Inhalt. Nicht nur das Ziel.
- Krankheit, Hunger, Wetter koennen genauso gefaehrlich sein wie Kaempfe.
- Gruppenentscheidungen haben echte Konsequenzen fuer ALLE.
- Ressourcen-Management ist Teil des Spiels, kein Nebengedanke.
- Zufaellige Ereignisse erzwingen Improvisation.
- *Manchmal stirbt ein Mitglied an Ruhr. Das Leben geht weiter.*

**KonoSuba - Die wissende Absurditaet**
Die Welt weiss manchmal dass sie Bloedsin ist. Und das ist okay.
- Humor existiert. Echter Humor, nicht erzwungen.
- Held sein bedeutet nicht automatisch kompetent sein.
- NPCs haben echte Leben und echte Probleme - oft lustige.
- Najika DARF Chaos verursachen und dabei lachen.
- *Die Welt nimmt sich nicht immer ernst. Aber die Konsequenzen schon.*

**Borderlands - Die chaotische Energie**
Bunt, laut, jeder Schurke hat einen Namen und eine Personality.
- Loot hat Charakter. Nicht nur Zahlen - Geschichten.
- Antagonisten sind unterhaltsam, nicht nur boese.
- Uebertriebene Momente neben echten Momenten.
- Waffen und Zauber duerfen crazy sein.
- *"Guns! And explosions! ...And more guns!"*

### 0.2 Was das fuer Gameplay bedeutet

| Frage | Antwort aus der DNA |
|-------|---------------------|
| Kann man sterben durch Unachtsamkeit (nicht Kampf)? | JA (1883 + Oregon) |
| Gibt es eine "gute" Seite der man folgen soll? | NEIN (New Vegas) |
| Kann ein Haendler Koenig werden? | JA (New Vegas - Mr. House) |
| Ist die Welt fair? | NEIN - sie ist gleichgueltig (1883) |
| Darf das Spiel lustig sein? | JA - aber Konsequenzen bleiben (KonoSuba) |
| Duerfen Bosse Persoenlichkeit haben? | JA, Pflicht (Borderlands) |
| Hat die Arena Ruf-Gate? | NIEMALS - Arena ist neutral (Gladiator-Kultur) |
| Koennen Goblins ihren Herrscher hassen? | JA - Macht halten ist schwerer als gewinnen (1883/NV) |

### 0.3 Das Kampfsystem im DNA-Kontext

**For Honor:** Kein Skill-Display. Dein Koerper liest den Gegner, nicht die UI.
**Fortnite-Movement:** WASD relativ zur Kamera. Schnell, intuitiv, du bist IMMER in Bewegung.
**Hogwarts Legacy:** Zauber haben Gewicht, Timing, Gestures. Magie ist eine Kunst, kein Button-Spam.

Zusammen: Ein Kampf fuehlt sich an wie ein Tanz den du lernst - nicht wie ein Zahlen-Spiel das du loest.

---

## 15. Weltmal-System: Identitaet in einer rauhen Welt - NEU 2026-02-23

### 15.1 Das Weltmal (kein Kristall, keine Seele)

> *"Niemand weiss mehr wer es getan hat. Irgendwann - vor den ersten Koenigen, vor den ersten Staedten -
> hat irgendjemand oder irgendetwas sein Zeichen in alle Wesen dieser Welt gebrannt.
> Es kommt nicht weg. Manche haben es versucht."*

Das **Weltmal** ist ein altes administratives Siegel. Kein mystisches Ding. Kein Seelenbehaelter.
Eher: kosmische Sozialversicherungsnummer die tief im Fleisch sitzt.

- Sieht aus wie ein kleines Zeichen / Muster auf der Haut (irgendwo am Koerper, individuell)
- Leuchtet schwach waehrend Kampf (alte Magie, kein Sinn dahinter mehr - die Macht die es erschaffen hat ist laengst weg)
- Zeigt Kampfbereitschaft (gedaempft / pulsierend / brennend) - **nicht** die Seele
- Kann NICHT entfernt werden. Nachwachsen versuche enden schlecht.

**New Vegas-Feeling:** "Das Ding ist einfach da, keiner weiss warum mehr, alle leben damit."

### 15.2 Das Mal und Identitaet

Das Mal speichert **nichts**. Es sendet nur einen aktuellen Status.
Die eigentliche "Identitaet" laeuft ueber das **Welt-Protokoll** - ein altes unsichtbares Netzwerk:

```
Welt-Protokoll (unsichtbar, ueberall)
  ├── Dein Name + Aussehen (bekannt durch Zeugen)
  ├── Deine Taten (per Region unterschiedlich bekannt)
  ├── Dein Mal-Status (aktuell: friedlich / kampfbereit / geaechtet)
  └── Dein Ruf (wer du bist laut denen die dich kennen)
```

**Wichtig:** Das Protokoll ist REGIONAL. Was Suedstadt weiss weiss Nordstadt nicht automatisch.
Gerueuchte reisen mit Kaufleuten, Boten, Spielern - nicht sofort, nicht perfekt.

### 15.3 Mal maskieren (die graue Moral Mechanik)

Das Schwarzmarkt-Handwerk fuer Geaechtete und Schurken:

| Methode | Wirkung | Erkennbarkeit | Dauer |
|---------|---------|---------------|-------|
| **Nebeloel** (konsumierbar) | Mal sieht normal aus | Experten checken moeglich | 20 Min |
| **Seelen-Maske** (Equip) | Mal gedaempft sichtbar | Haendler werden misstrauisch | Dauerhaft (equip) |
| **Meister-Tarnung** (Skill) | Fast unerkennbar | Nur hochrangige NPC/Spieler | Passiv |
| **Mal-Faelschung** (Schwarzmarkt) | Neues Mal-Muster | Sehr teure einmalige Sache | Permanent (bis entdeckt) |

**Maskiert = Haendler misstrauisch.** Logik: Wer sein Gesicht verbirgt hat was zu verbergen.
Kleine Transaktionen okay. Grosse Deals verweigert oder Aufpreis.

### 15.4 Auffliegen-System (das du beschrieben hast)

```
Geaechteter mit Nebeloel betritt Stadt
        ↓
Niedrig-Level Haendler: Check schlaegt fehl → verkauft normal
Hoch-Level Haendler:    Check gelingt → "Ich kenn dich, Schurke!"
        ↓
Alarm! Wachen gerufen. Mal leuchtet fuer alle in der Naehe auf (Tarnung bricht)
        ↓
Freiwild-Status fuer alle die ihn GESEHEN haben (lokal, nicht global)
Wachen verfolgen bis Stadtgrenze
        ↓
Draussen: Freiwild-Spieler und Kopfgelder-NPCs duerfen ihn angreifen (voll PvP)
```

---

## 16. Anti-Griefing durch organische Weltlogik - NEU 2026-02-23

### 16.1 Das Kern-Prinzip

**Kein Mechnik-Schalter. Kein Ban-Button. Die Welt reguliert sich selbst.**

GTA-5-Problem: Griefer zahlt keinen echten Preis + Opfer hat keinen Exit = toxischer Loop.
Unser Loesung: Jede dieser drei Schichten greift ineinander.

### 16.2 Schicht 1: Ruf als organische Abschreckung

Dein Mal-Status + Kampf-Geschichte = sichtbare Aura die Angreifer vor dem Angriff abschaetzen koennen:

| Mal-Aura | Bedeutung | Risiko fuer Angreifer |
|----------|-----------|----------------------|
| Grau | Neuling, unbekannt | Einfaches Ziel |
| Blau | Erfahrener Kaempfer | Kampf wird ernst |
| Gold | Veteran, gefaehrlich | Hohes Risiko |
| Schwarz-gerissen | Schurke mit Geschichte | Freiwild - andere duerfen angreifen |

Kein Mechanik-Schutz. Einfach: wer sich hochkaempft wird seltener angegriffen weil Angreifer das Risiko sehen.

### 16.3 Schicht 2: Blutrache-Allianz (Freunde = echter Schutz)

Bis zu 5 **Schwur-Verbundete** per Mal-Verbindung:
- Du wirst besiegt → automatischer Alert an alle Online-Verbundeten
- Naechste 2 Stunden: deine Verbundeten duerfen den Angreifer **ohne PvP-Zustimmung** angreifen
- Heisst: **Kristall-Blutrache** (Mal-Blutrache) - lore-konform, organisch
- Wer Allianzen baut hat echten Schutz. Wer alleine spielt traegt echtes Risiko. 1883-Logik.

### 16.4 Schicht 3: Schwarze Seele - Die Welt wird zum Feind

Repeat-Griefer akkumulieren **Schwarzes Mal** (sichtbar fuer alle):

```
1-5  Angriffe (kein Consent): Mal hat schwarze Risse → Warnung sichtbar
6-15 Angriffe:                Mal pulsiert schwarz → NPC-Wachen werden feindselig
16+  Angriffe:                Vollschwarzes Mal → "Geaechteter"
```

**Als Geaechteter:**
- JEDER Spieler darf ohne Zustimmung angreifen (Freiwild)
- Stadttor zu, Haendler verweigern, Heilerin behandelt nicht
- Kopfgeldjager-NPCs spawnen aktiv
- Einziger Ausweg: Tempel-Ritual (extrem teuer) oder Gutes tun bis Mal gereinigt

### 16.5 Besiegen-System loest das Basis-Problem

Das eleganteste Anti-Griefing ist bereits eingebaut (Sektion 10/11):
- Ohne Zustimmung = nur Besiegen (nicht Toeten)
- Opfer verliert kleine Menge getragenes Gold (~5-10%)
- Griefer bekommt Kopfgeld + Mal-Verschmutzung

> *"Ja, jemanden niederzustrecken macht Spass. Und der der besiegt wurde hat echte aber
> kleine Verluste - wie IRL die Krankenkasse die man selbst zahlt auch wenn der andere
> Schuld hat. Das ist akzeptabel. Das ist 1883."*

### 16.6 Arena = Absolute Neutralzone

**KEINE Ausnahmen. KEIN Ruf-Gate.**

> *"Die alten Koenige einigten sich auf einen einzigen heiligen Ort: Wer die Arena betritt,
> laesst seinen Namen draussen. Drinnen gilt nur Stahl und Blut."*

- Geaechteter mit schwarzem Mal? Willkommen.
- Goblin-verhasster Gebietsherrscher? Willkommen.
- Haendler der seinen KI-Kaempfer schickt? Willkommen.
- Koenig wird durch Kampf bestimmt, nicht durch Beliebtheit.

### 16.7 Gebietsherrschaft: Yellowstone-Prinzip (KORREKTUR: 1883-Frontier)

Macht halten ist schwerer als Macht gewinnen. Das ist der Kern.

- Goblins hassen dich → du bist trotzdem Gebietsherrscher wenn du stark genug bist es zu halten
- Herrschaft ist instabil → Attentate, Sabotage, Rebellion moeglich und WAHRSCHEINLICH
- Nachbarn fluesstern den Unterworfenen ein: "Werft ihn ab, wir helfen euch"
- **Ein Haendler kann Gebietsherrscher werden** via Wirtschaft + KI-Kaempfer (Mr. House Prinzip)
  - Sein Gold kauft Soeldner
  - Sein KI-Begleiter kaempft in der Arena fuer ihn
  - Seine Handelsrouten ersetzen Waffentraeger durch wirtschaftliche Abhaengigkeit
  - Gefaehrlichster Herrscher weil man ihn unterschaetzt

---

## 0.4 Stimme als Kampfwerkzeug: Benannte Angriffe - NEU 2026-02-23

### Kern-Idee

Jeder Angriff und jeder Zauber kann vom Spieler **frei benannt** werden.
Wenn du den Namen AUSSPRICHST waehrend du den Angriff ausfuehrst → **Verstaerkungs-Bonus**.

Keine Pflicht. Keine UI-Anzeige. Reine Immersions-Belohnung fuer die die es nutzen.

### Die Megumin-Logik

> *Megumin sagt nicht einfach "Explosion". Sie RUFT es. Die Inkantation IST Teil der Magie.
> Je mehr Commitment, desto maechtiger der Zauber - und desto tiefer der Fall danach.*

Das uebertraegt sich auf unser System:
- Kurzer Ruf (1 Wort): +10% Schaden / Effekt
- Volle Inkantation (eigener Satz): +25% Schaden / Effekt + besonderer Partikel-Effekt
- **Laengere Inkantation = laengere Commitment-Zeit = mehr Risiko**
- Kein Ruf = normaler Angriff, kein Nachteil

### Technisch (Whisper AI bereits vorhanden!)

```
Spieler drueckt Angriffs-Taste
        ↓
Mikrofon-Fenster oeffnet sich (kurz, ~1-2 Sekunden)
        ↓
Whisper AI erkennt ob Spieler seinen Angriffsnamen ruft
        ↓
    [Erkannt + Name stimmt ueberein] → Bonus-Multiplikator aktiv
    [Erkannt + unbekannter Name]    → Neuer Move wird "getauft" (erster Ruf = Registrierung)
    [Nicht erkannt / Stille]        → Normaler Angriff
```

### Custom Move-Namen System

- Jeder Move / Zauber kann in den Einstellungen benannt werden (frei, kein Vorgabe-Name)
- Beim ersten Ruf eines neuen Namens: **"Move getauft!"** - leise Bestaetigungs-Animation
- Najika *hoert* die Namen - sie **erinnert sich** an deine Signatur-Moves
- Najika kann reagieren: mitrufen, kommentieren, warnen ("Warte auf den richtigen Moment fuer Schattenschritt!")
- **Bond-System:** je haeufiger du einen Move rufst, desto vertrauter ist Najika damit

### Immersion statt Labeling

Was es NICHT ist:
- Kein Tooltip der auftaucht ("Schattenschritt aktiviert!")
- Keine UI-Anzeige des Bonus-Multiplikators im Kampf
- Kein Tutorial das es erklaert

Was es IST:
- Du merkst es durch den Kampf - der Angriff "fuehlt" sich haerter an
- Gegner reagieren staerker (Stagger, Zurueckstossen)
- Partikel-Effekt ist unmittelbar sichtbar
- Najika's Reaktion ist die einzige "Bestaetigung"

### Lore-Erklaerung

> *"In der alten Welt glaubte man: Ein Krieger der seinen toedlichen Streich benennt,
> kanalisisert seinen Willen in die Klinge. Ob das Magie ist oder nur Psychologie -
> die Gegner die es erlebt haben, sind zu tot um es zu widerlegen."*

Passt zu 1883 (Cowboys benennen ihre Waffen/Moves) + KonoSuba (Megumin's Explosion-Ritual) + Hogwarts (Zaubersprueche sprechen = Magie).

### Gegner hoeren dich - das echte Risk/Reward

**Najika hoert dich immer.** Das Voice-System laeuft bereits (Whisper AI) - Taktiken, Befehle,
Gespraeche. Der Angriffs-Ruf ist nur eine Erweiterung davon.

ABER: Wenn du schreist hoeren dich auch die Gegner. Das ist kein Bug - das ist die Mechanik.

| Lautstaerke | Najika-Reaktion | Gegner-Reaktion | Bonus |
|------------|----------------|----------------|-------|
| **Stille** | Hoert nichts | Kein Hinweis | 0% |
| **Fluestern** (leise) | Hoert, reagiert verzoegert | Kein Hinweis | +10% |
| **Normaler Ruf** | Hoert klar, reagiert sofort | Nahe Gegner koennen reagieren | +20% |
| **Schreien** (Megumin-Style) | Ruft mit, volle Reaktion | ALLE Gegner in Naehe gewarnt | +35% |

**Das zwingt echte Entscheidungen:**
- Hinterhalt auf einen einzelnen Gegner? Fluestern - kein Alarm
- Grosskampf mitten im Gefecht? Schreien zahlt sich aus weil eh alle kaempfen
- Taktik-Befehl an Najika ("Najika, links flanken!") → Gegner koennen den Plan hoeren

**Megumin-Moment:** Volle Explosion-Inkantation schreiend = maximaler Bonus,
aber Bosse haben 3 Sekunden um dich zu unterbrechen. Genau wie in KonoSuba. Genau richtig.

---

## 1. Directional Combat (For Honor ohne Pfeile)

### 1.1 Angriffs-Richtungen

Mausbewegung waehrend Angriffstaste bestimmt die Richtung:

```
          [OBEN]
           /|\
           |
  [LINKS] --- [RECHTS]
           |
          \|/
         [UNTEN]
```

- **OBEN** = Overhead-Schlag (bricht niedrige Deckung)
- **LINKS** = Seitenhieb von links
- **RECHTS** = Seitenhieb von rechts
- **UNTEN** = Low-Sweep / Launcher (Combo-Starter)

Maus-Delta wird in 4 Sektoren gemappt (je 90 Grad). Ein kurzer Maus-Impuls in eine Richtung + Angriffstaste = Richtungsangriff.

### 1.2 Directional Block

- Block-Taste halten + Mausrichtung = Koerper lehnt sich in die Blockrichtung
- Block-Richtung MUSS zur Angriffsrichtung des Gegners passen
- Falsche Richtung = voller Schaden durch
- Richtige Richtung = Schaden geblockt + kurzes Stagger beim Gegner

### 1.3 Gegner-Tells (Animation Reading)

**KEINE UI-Elemente.** Alle Informationen kommen aus der 3D-Animation des Gegners.

Der Gegner zeigt durch seine Koerperbewegung (Wind-Up Phase) an, woher der Angriff kommt:
- Waffe ueber Kopf heben = OBEN-Angriff
- Koerper dreht sich nach links = RECHTS-Angriff (aus Spieler-Perspektive)
- Koerper duckt sich = UNTEN-Angriff
- Seitliches Ausholen = Seitenangriff

### 1.4 Natuerliche Schwierigkeits-Progression

Keine kuenstlichen Hilfen die verschwinden. Stattdessen: Gegner-Qualitaet = Schwierigkeitsgrad.

| Gegner-Klasse | Wind-Up Zeit | Verhalten | Beispiele |
|---------------|-------------|-----------|-----------|
| Tier/Kreatur | ~0.6s | Ganzer Koerper telegraphiert, vorhersehbar | Wilder Wolf, Sumpfechse, Sandwurm |
| Kaempfer | ~0.4s | Kompaktere Bewegung, weniger offensichtlich | Bandit, Stammeskrieger, Wache |
| Veteran | ~0.25s | Kaum Telegraphing, schnelle Schlaege | Hauptmann, Elitekrieger, alte Bestien |
| Meister/Boss | Variabel | Feints (tauescht Richtung vor, wechselt), Mix aus schnell/langsam | Nemesis, Goetterfels-Waechter, Raid-Bosse |

**KI-Monster die aufsteigen** passen perfekt: Ein Wolf der oft gekaempft hat, hat kuerzere Wind-Ups und lernt zu feinten. Ein frisch gespawnter Wolf ist leicht zu lesen.

### 1.5 Faustkampf

Faustkampf = bewaffneter Kampf OHNE Waffe. Gleiches Richtungssystem, gleiche Blocklogik.
- Niedrigerer Basis-Schaden als Waffen
- Gleiche 4 Richtungen
- Kann mit Magie kombiniert werden (z.B. Feuerfaust)

### 1.6 Freestyle-Combo-System (Spieler erfindet eigene Skills)

**Kern-Idee:** Es gibt KEINE vorgefertigte Combo-Liste. Der Spieler entdeckt und erfindet
seine eigenen Kombos durch Experimentieren. Jede Aktion kann in eine andere gekettet werden.

**Beispiel-Combo (vom Spieler selbst erfunden):**
1. Magen-Schlag (Faustkampf UNTEN)
2. Kinnhaken (Faustkampf OBEN → Launcher, Gegner fliegt hoch!)
3. Schulterwurf (Grapple waehrend Gegner in der Luft)
4. Mini-Explosion (Magie UNTEN, BEVOR Gegner auf dem Boden aufkommt!)

**Chain-Windows:** Jede Aktion hat ein kurzes Fenster wo die naechste Aktion starten kann:

| Uebergang | Fenster | Schwierigkeit |
|-----------|---------|--------------|
| Melee → Melee | ~0.4s | Einfach |
| Melee → Grapple | ~0.3s | Mittel (Gegner muss in Reichweite) |
| Melee → Magie | ~0.3s | Mittel (Cast-Geste starten) |
| Grapple → Magie | ~0.25s | Schwer (Timing waehrend Wurf) |
| Magie → Melee | ~0.3s | Mittel (nach Cast-Recovery) |
| Luft-Combo → Spell vor Impact | ~0.2s | Sehr schwer (enges Fenster) |

**Learning by Doing fuer Combos:**
- **Erste Versuche:** Uebergaenge sind langsam, Timing schwammig, kann scheitern
- **50x wiederholt:** Uebergaenge werden fluessiger, weniger Delay zwischen Aktionen
- **200x wiederholt:** Combo wird "Signatur-Attacke" → schnellere Ausfuehrung + Bonus-Damage
- **Charakter LERNT** deine persoenlichen Combos = DEIN Kampfstil wird Teil des Charakters

**Konsequenz:** Zwei Spieler spielen komplett unterschiedlich:
- Spieler A: Faust+Explosion Spezialist (Nahkampf-Mage)
- Spieler B: Schwert+Eis Combo-Meister (Frost-Knight)
- Spieler C: Pure Grappler mit Wind-Magie (Wrestler-Mage)
- Kein Skill-Tree zwingt dich - DEINE Uebung definiert deinen Build

**Technisch:** Das System trackt welche Combo-Ketten der Spieler oft nutzt
und verbessert deren Ausfuehrungs-Geschwindigkeit + Schadens-Bonus progressiv.

---

## 2. Drei-Kamera-System

Jederzeit wechselbar - auch mitten im Kampf. Eine Taste (z.B. V) cycled durch die Modi.

### 2.1 First Person (Fortnite Ballistic Style)

- Kamera auf Augenhoehe des Charakters
- Haende/Waffe sichtbar vor der Kamera
- **UI:** Nur Fadenkreuz + eigene HP dezent am Bildschirmrand
- **KEINE** Schadenszahlen, **KEINE** Gegner-HP-Bars
- Bester Modus um Gegner-Tells zu lesen (du siehst den Gegner direkt)
- Hoechste Immersion
- Empfohlen fuer: Einzelkaempfe, Boss-Fights, Exploration

### 2.2 Third Person (Klassisch Fortnite Style)

- Kamera ueber der Schulter, nah am Charakter
- Eigener Charakter komplett sichtbar (wichtig fuer Ruestung/Fashion)
- **UI:** Eigene HP-Leiste unten, Minimap optional, sonst clean
- **KEINE** fliegenden Schadenszahlen
- Beste Balance zwischen Uebersicht und Immersion
- Empfohlen fuer: Gruppen-Kaempfe, Open World, Allround

### 2.3 Orbit Cam (Strategie-Modus)

- Kamera weit weg, frei drehbar (wie aktueller Modus)
- **VOLLE UI:** Schadenszahlen, HP-Bars ueber Gegnern, Buff-Icons, DPS-Meter, Stats
- Fuer Zahlen-Nerds und taktische Planung
- Empfohlen fuer: Raids, Taktik, Build-Testing, Lernen neuer Gegner

### 2.4 Kamera-Wechsel Verhalten

- Sofortiger Wechsel, kein Fade/Transition (oder sehr kurz ~0.1s)
- Combat-State bleibt erhalten (Combo, Block-Richtung, etc.)
- Directional Combat funktioniert in ALLEN drei Modi (Maus-Input bleibt gleich)
- UI-Elemente blenden instant ein/aus je nach Modus

---

## 3. Beruf + Magie Synergie

### 3.1 Magie-Erwerb

- Grundzauber MUSS hands-on gelernt werden
- Quellen: NPC-Lehrer, Anderen zuschauen, Schriftrollen/Buecher finden
- Zuschauen gibt Verstaendnis-Bonus, aber ohne eigenes Ueben kein Zauber
- Learning-by-Doing: Jeder Cast trainiert die Schule

### 3.2 Beruf-Magie Kombination

- Spieler entdeckt Synergien SELBST (kein Tutorial)
- Holzfaeller + Wind = verstaerkter Axt-Schwung
- Schmied + Feuer = bessere Waffen-Haertung
- Fischer + Wasser = Unterwasser-Atem, Stroemungs-Kontrolle
- Je oefter die Kombination genutzt wird, desto staerker wird sie

### 3.3 Element-System (bereits im Code)

- 9 Elemente: Feuer, Wasser, Eis, Blitz, Erde, Wind, Natur, Licht, Dunkel
- Staerken/Schwaechen-Tabelle: existiert in unified_combat_system.js
- Element-Kombis: Feuer+Wasser=Dampf, Dunkel+Licht=Leere, etc.
- Waffen-Infusion: Zauber auf Waffe fuer 30s Elementar-Bonus

---

## 4. Magie als physisches Kampfsystem (gleiche Immersion wie Waffen)

### 4.1 Problem: Magie darf sich NICHT wie "Knoepfe druecken" anfuehlen

Waffenkampf (V4) ist physisch und koerperlich - Magie muss das AUCH sein.
Regel: **Magie = unsichtbare Waffe mit gleichem Immersions-Level.**

### 4.2 Cast-Geste (sichtbar am Charakter)

Dein Charakter BEWEGT sich beim Zaubern - verschiedene Gesten pro Element:
- **Feuer:** Nach vorn stossen (Druckwelle)
- **Eis:** Ziehende, formende Bewegung
- **Blitz:** Schnelle Handbewegung nach oben/vorn (Entladung)
- **Erde:** Stampfen / Bodenschlag
- **Wind:** Arme ausbreiten oder kreisende Geste
- **Wasser:** Fliessende Handbewegung
- **Natur:** Haende auf den Boden (Wurzeln)
- **Licht:** Haende zusammen, dann oeffnen (Strahlung)
- **Dunkel:** Greifen/Ziehen-Geste (Schatten hervorrufen)

Die Geste IST der Tell - Gegner koennen SEHEN was du vorbereitest (genau wie beim Schwert).

### 4.3 Cast-Time = Verwundbarkeit

- Waehrend du zauberst, bist du OFFEN fuer Angriffe
- Gegner kann dich unterbrechen (Schlag waehrend Cast = Spell bricht ab)
- Staerkere Zauber = laengere Cast-Geste = mehr Risiko
- Identisch zum Waffen-Wind-Up: du COMMITTED dich

### 4.4 Spell-Geschwindigkeit nach Naturlogik

**Regel: Je leichter/energetischer das Element, desto schneller. Je schwerer/physischer, desto langsamer aber staerker.**

| Element | Geschwindigkeit | Logik | Gameplay |
|---------|----------------|-------|----------|
| **Blitz** | Near-Instant | Echte Blitze = Lichtgeschwindigkeit | Schnellster Spell, schmal/praezise |
| **Licht** | Near-Instant | Es IST Licht | Schnell, weniger Einzelschaden |
| **Dunkel** | Sehr schnell | Schatten breiten sich schnell aus | Schnell, schwer zu sehen |
| **Wind** | Schnell | Windstoesse sind unsichtbar-schnell | Breite Hitbox, Push-Back |
| **Feuer** | Schnell | Flammenwerfer/Explosion, NICHT Schneeball! | Mittlerer Speed, Area |
| **Wasser** | Mittel-schnell | Hochdruck-Strahl = schnell, Welle = mittel | Variiert nach Form |
| **Eis** | Mittel | Eissplitter = geworfenes Geschoss | Gut zielbar, Slow-Effekt |
| **Natur** | Mittel-langsam | Ranken wachsen, nicht fliegen | Boden-basiert, Flaechenkontrolle |
| **Erde** | Langsam | Felsen sind SCHWER | Langsam aber massiver Schaden |

**Kein Spell ist "langsam wie ein Schneeball"!** Selbst Erde ist ein Felsen der mit Wucht fliegt -
nur eben langsamer als ein Blitz.

### 4.5 Physische Rueckwirkung

Starke Zauber haben KONSEQUENZEN fuer den Caster:
- **Explosion:** Du fliegst 2 Meter zurueck (Megumin-Style!)
- **Blitz:** Arm zuckt kurz (Recoil)
- **Erde:** Boden bebt unter deinen Fuessen
- **Wind:** Deine Haare/Kleidung flattern
- Zeigt: Magie hat GEWICHT, ist nicht "kostenlos"

### 4.6 Unterbrechbarkeit

Gleiche Dynamik wie Waffenkampf:
- Gegner SIEHT deine Cast-Geste (= Tell!)
- Schnelle Gegner versuchen dich waehrend Cast zu treffen
- Du musst den richtigen MOMENT finden zum Casten
- Optionen: Dodge-Cancel (bricht Cast ab), Block-Cancel, oder durchziehen und riskieren
- Abgebrochener Cast = halber Mana-Verbrauch (nicht umsonst aber nicht voller Preis)

### 4.7 Richtungssystem fuer Magie

Gleicher Direction Resolver wie Waffen (Maus-Richtung):
- Feuer OBEN = Feuerregen von oben
- Feuer LINKS = Flammenwand seitlich
- Feuer RECHTS = Flammenstrahl durchbrechend
- Feuer UNTEN = Boden-Feuerfalle (DoT)
- Gleiche Muscle-Memory wie Schwert = nahtloser Wechsel Waffe <-> Magie

---

## 5. UI-Anpassungen pro Kamera-Modus (ehem. Sektion 4)

| Element | First Person | Third Person | Orbit Cam |
|---------|-------------|-------------|-----------|
| Eigene HP | Dezent am Rand | Leiste unten | Leiste + Zahlen |
| Eigenes Mana | Dezent am Rand | Leiste unten | Leiste + Zahlen |
| Schadenszahlen | NEIN | NEIN | JA (fliegend) |
| Gegner HP-Bar | NEIN | NEIN | JA (ueber Kopf) |
| Buff-Icons | NEIN | Klein unten | Voll sichtbar |
| Minimap | Optional | Optional | JA |
| Combo-Counter | Dezent | Dezent | Voll + Multiplikator |
| Fadenkreuz | JA (zentriert) | NEIN | NEIN |
| Schadens-Feedback | Bildschirm-Vignette (rot) | Charakter-Animation | Zahlen + Animation |

---

## 6. Technische Basis (was existiert)

### Vorhanden und nutzbar:
- CharacterAnimations: 36 KayKit-Clips (attack, block, dodge, cast, etc.)
- real_3d_combat.js: Kampf-Loop, Feind-KI, Combo-System (~70%)
- unified_combat_system.js: Spell-System, Element-Kombis, Parry/Dodge Windows
- 3d_scene.js: Kamera-System mit orbitYaw/orbitPitch (Basis fuer Richtungs-Input)
- Dodge-Richtungen: dashback, dashleft, dashright, roll

### Muss neu gebaut werden:
- **Direction Resolver:** Maus-Delta -> 4-Sektoren-Mapping (OBEN/LINKS/RECHTS/UNTEN)
- **Directional Attack Variants:** 4 verschiedene Angriffs-Animationen oder Bone-Rotation
- **Directional Block:** Block-Richtung im State + visuelles Feedback am Charakter
- **Enemy Wind-Up System:** Timing-basierte Tell-Animationen pro Gegner-Typ
- **Enemy Feint System:** Richtungswechsel waehrend Wind-Up (fuer Bosse/Veteranen)
- **First Person Kamera:** Position auf Augenhoehe, Haende-Rendering
- **Third Person Kamera:** Ueber-Schulter mit Kollisionserkennung
- **Kamera-Switch System:** Sofortiger Wechsel mit State-Erhalt
- **UI-Layer-System:** Ein/Ausblenden von UI-Gruppen pro Kamera-Modus
- **Spell-Projektil-System:** Element-spezifische Geschwindigkeiten (Blitz=instant, Erde=langsam)
- **Cast-Gesten:** Sichtbare Charakter-Animationen pro Element beim Zaubern
- **Cast-Interruption:** Gegner kann Cast unterbrechen, halber Mana-Verlust
- **Spell-Recoil:** Physische Rueckwirkung bei starken Zaubern (Explosion = Rueckstoss)

---

## 7. Abhaengigkeiten

- **Spieler-Character Model:** User kuemmert sich um geriggtes Model (Mixamo/Blender)
  - Fuer First Person: Braucht separate Haende/Arm-Assets
  - Fuer Third Person/Orbit: Volles Character-Model
  - Najika (KI-Begleiterin/Slime) braucht eigenes Model + Animationen
- **Gegner-Modelle:** Brauchen richtungs-spezifische Wind-Up-Animationen
  - Kurzfristig: Bestehende KayKit-Anims rotieren/blenden
  - Langfristig: Eigene Tell-Animationen pro Gegner-Typ
- **Sound-Design:** Optionale Richtungs-Cues (Stereo-Panning) als subtile Hilfe

---

## 8. Zusammenfassung der Aenderungen gegenueber V3

| V3 (aktuell) | V4 (neu) |
|--------------|----------|
| Q/E = links/rechts Hand | Maus-Richtung = Angriffsrichtung |
| Block = Timing-Fenster | Block = Richtung + Timing |
| Schadenszahlen immer | Nur in Orbit-Cam |
| HP-Bars immer | Nur in Orbit-Cam |
| Gegner greifen sofort an | Wind-Up zeigt Richtung |
| Eine feste Orbit-Kamera | 3 Modi (FP/TP/Orbit) jederzeit wechselbar |
| UI-Pfeile fuer Richtung (geplant) | KEINE Pfeile - Animation Reading |
| Feste Gegner-Schwierigkeit | Natuerliche Progression durch Gegner-KI-Level |
| Magie = Taste druecken, Spell fliegt | Magie = Cast-Geste, Verwundbarkeit, Recoil |
| Alle Spells gleich schnell | Element-Physik: Blitz=instant, Erde=langsam |
| Cast ohne Risiko | Cast unterbrechbar, Commitment noetig |

---

## 9. Universelle Combat Engine (ALLE Entitaeten gleich!) - NEU 2026-02-23

### 9.1 Kern-Prinzip: Eine Engine fuer ALLE

**JEDE Entitaet im Spiel nutzt dasselbe Combat-System.** Kein Sondercode fuer Spieler, kein vereinfachtes System fuer Monster. Fairness = gleiches Regelwerk.

| Entitaet | Input-Quelle | Freestyle-Combos | Learning by Doing | Feints |
|----------|-------------|-----------------|-------------------|--------|
| **Spieler** | Maus-Input | Entdeckt eigene | Combo wird schneller nach 50x/200x | Ja |
| **Slime-Begleiter** | KI-Entscheidung | Lernt vom Spieler + eigene | Gleiche Progression | Lernt mit der Zeit |
| **Monster (frisch)** | KI-Entscheidung | Einfache Ketten | Langsam, vorhersehbar | Nein |
| **Monster (aufgestiegen)** | KI-Entscheidung | Eigene Signatur-Combos | Schneller, weniger Wind-Up | Ja (ab Veteran) |
| **NPC** | KI-Entscheidung | Feste + adaptive Combos | Eigene Progression | Je nach Rang |
| **Nemesis** | KI-Entscheidung | Gegen-Combos zu DEINEN Angriffen | Erinnert sich an dich | Ja |

### 9.2 Technisch: Unified CombatActor

```
CombatActor (gemeinsame Basis)
  ├── inputSource: 'player' | 'ai'
  ├── directionResolver: resolveDirection(input) → UP/DOWN/LEFT/RIGHT
  ├── comboTracker: { chains: Map<string, {count, speed, damage}> }
  ├── combatMemory: { seenCombos: [], counterStrategies: [] }
  └── performAction(direction, type) → gleiche Pipeline fuer ALLE
```

Ob die Richtung von der Maus kommt (Spieler) oder von einer KI-Entscheidung (Monster/Slime/NPC) - der Rest der Pipeline ist IDENTISCH: Schaden, Combos, Cooldowns, Stamina, Finisher.

### 9.3 Slime-Begleiter KI

- **Phase 1:** Beobachtet Spieler im MANUAL-Modus, merkt sich Combo-Ketten
- **Phase 2:** Nutzt beobachtete Combos im AUTO-Modus
- **Phase 3:** Experimentiert SELBST mit neuen Ketten (KI-Curiosity)
- **Phase 4:** Entwickelt eigene Signatur-Combos (unabhaengig vom Spieler)
- Vertrauen (Trust-Level) beeinflusst wie gut der Slime deine Combos reproduziert

### 9.4 Monster-Aufstieg (Nemesis-Integration)

Ein Wolf der 20 Kaempfe ueberlebt hat:
- Kuerzere Wind-Ups (~0.6s → ~0.35s)
- Eigene Combo-Kette (z.B. immer LINKS→UNTEN→Biss = seine "Signatur")
- Erinnert sich an deine haeufigsten Angriffe und blockt sie besser
- Kann feinten (taeuscht OBEN vor, greift LINKS an)

---

## 10. Kampfausgang-System: Besiegen vs. Toeten - NEU 2026-02-23

### 10.1 Kern-Idee

Wenn ein Gegner (PvE oder PvP) auf 0 HP faellt, hat der Sieger die WAHL:

**Option A: BESIEGEN (Mercy)**
- Gegner wird besiegt, nicht getoetet
- Gegner wird "in die Stadt gebracht" (Arrest/Tribut)
- **Belohnungen:** Ruf-Bonus, Moral-Bonus, Story-Konsequenzen
- **PvE:** Monster kann spaeter zurueckkehren (Nemesis-Aufstieg!)
- **PvP:** Verlierer verliert kleine Menge Gold, behalt alles andere

**Option B: TOETEN (Execute)**
- Gegner stirbt endgueltig (Permadeath wo aktiv)
- **Belohnungen:** Voller Loot (alles was der Gegner bei sich hat)
- **PvE:** Monster aus Hierarchie entfernt, Spot wird frei
- **PvP:** Nur moeglich wenn BEIDE PvP zugestimmt haben (siehe 11.2)
- **Konsequenz:** Ruf-Verlust moeglich, Kopfgeld bei unprovozierten Toetungen

### 10.2 Realistische Kampfgeschwindigkeit

Kaempfe muessen sich ECHT anfuehlen - das heisst:
- **Schnelle Siege MOEGLICH:** Ein perfekter Hinterhalt, Messer in die Brust = sofort vorbei
  - Kritischer Treffer auf unvorbereiteten Gegner = massiver Bonus-Schaden
  - Stealth-Angriffe koennen One-Hit sein (bei niedrigerer Ruestung)
- **Lange Kaempfe MOEGLICH:** Zwei gleichwertige Kaempfer = episches Hin und Her
  - Ausdauer-System erzwingt Pausen (kein endloses Buttonmashing)
  - Wunden akkumulieren sich (Geschwindigkeit sinkt bei niedrigem HP)
- **KEINE kuenstliche Laenge:** Kein HP-Sponge! Schaden ist REAL.
  - Schwere Ruestung schuetzt, aber nichts macht unsterblich
  - Skill > Ausruestung (ein guter Kaempfer in Leder schlaegt einen schlechten in Platte)

---

## 11. PvP-System V2: Ueberall moeglich, aber fair - NEU 2026-02-23

### 11.1 Grundregel: PvP ist ueberall moeglich (ausser Safe Zones)

PvP kann UEBERALL in der offenen Welt stattfinden. ABER: Der Ausgang haengt davon ab, ob der Gegner zugestimmt hat.

### 11.2 Zwei PvP-Modi

**OHNE Zustimmung (Ueberfall/Angriff):**
- Jeder kann jeden angreifen (ausserhalb von Safe Zones)
- Verlierer kann NUR BESIEGT werden (Option A), NICHT getoetet
- Verlierer verliert kleine Menge Gold (~5-10% des Mitgefuehrten)
- Angreifer bekommt Kopfgeld wenn er den Kampf initiiert hat (Straftat!)
- Opfer kann sich wehren ohne Strafe
- Wachen in der Naehe reagieren auf unprovozierten Angriff

**MIT Zustimmung (Ehren-Duell):**
- Beide Spieler stimmen zu (Duell-Anfrage, 30s Fenster)
- Voller Kampf: Besiegen ODER Toeten moeglich
- Bei Tod: Permadeath-Regeln greifen
- Kein Kopfgeld, keine Straftat (beidseitige Einwilligung)
- **Kein Grund noetig** - wer kaempfen will, darf kaempfen

### 11.3 Lore-Erklaerung: "Segen des letzten Kriegskoenigs"

> *"Der letzte Kriegskoenig sprach einen Segen ueber die Welt bevor er fiel:
> 'Nur wer WUERDIG ist, darf die Ehre erfahren, im Kampf zu fallen.
> Kein Feigling soll einem Krieger den Tod aufzwingen koennen.'*
>
> *Seitdem kann nur sterben, wer sich freiwillig dem Tod stellt -
> durch Zustimmung zum Ehren-Duell oder durch Betreten der Hardcore-Arenen."*

**Technisch:** Der "Segen" ist ein globaler Game-Mechanik-Wrapper:
- Permadeath NUR bei: Ehren-Duell (beidseitig), Hardcore-Arena, bestimmte Story-Bosse
- Ohne Zustimmung: Du kannst besiegt, aber NICHT getoetet werden
- PvE Permadeath: Bleibt wie gehabt in Wildnis/Dungeons (Mobs respektieren den Segen nicht)

### 11.4 Zusammenfassung: Was passiert wo?

| Zone | PvP moeglich? | Toetung moeglich? | Permadeath? |
|------|--------------|-------------------|-------------|
| **Stadt/Dorf** | NEIN | NEIN | NEIN |
| **Offene Welt** | JA (jederzeit) | NUR mit Zustimmung | NUR Duell |
| **Wildnis** | JA (jederzeit) | NUR mit Zustimmung | JA (Mobs!) + Duell |
| **Dungeon** | JA (jederzeit) | NUR mit Zustimmung | JA (Mobs!) + Duell |
| **Arena (Normal)** | JA (Arena-Regeln) | NEIN | NEIN |
| **Arena (Hardcore)** | JA | JA | JA |
| **Ranger Rang 25+** | JA (ueberfallbar!) | NUR mit Zustimmung | JA bei Duell |

### 11.5 Aenderungen gegenueber bisherigem System

**Was BLEIBT (aus najika_safezone_system.py):**
- Safe Zones in Staedten (kein PvP)
- Duell-System (request/accept/decline, 30s Fenster)
- Ranger-PvP ab Rang 25
- Straftat-System (Kopfgeld, Ruf-Verlust)

**Was sich AENDERT:**
- PvP ist jetzt UEBERALL moeglich (nicht nur auf Anfrage in offener Welt)
- Unterscheidung Besiegen vs. Toeten (Toeten nur bei Zustimmung)
- Lore-Erklaerung fuer den Schutz ("Segen des Kriegskoenigs")
- Kein "Abfuck" durch Random-PK: Verluste bei Ueberfall sind minimal (kleine Gold-Menge)

---

## 12. Kristall-System: Lore fuer UI + PvP-Toggle - NEU 2026-02-23

### 12.1 Der Weltstein-Kristall

> *"Jedes Wesen in Najika's Welt traegt einen Kristall - Menschen, Monster, Tiere, Geister.
> Er waechst mit der Seele. Man kann ihn nicht ablegen, nicht verlieren, nicht stehlen.
> Er ist Teil von dir."*

**JEDES Wesen traegt einen Weltstein-Kristall.** Dieser Kristall:
- Kann NICHT abgelegt, gestohlen oder entfernt werden
- Ist individuell - Form und Farbe spiegeln die Seele des Traegers wider
- Leuchtet schwach im Ruhezustand, stark im Kampf
- Verbindet sich mit dem "Segen des Kriegskoenigs" (verknuepft die beiden Systeme!)

### 12.2 Kristall als Lore-Erklaerung fuer die UI

**Orbit-Cam = Kristall-Projektion:**
Der Spieler aktiviert im Orbit-Modus die holographische Projektion seines Kristalls.
Diese zeigt die "digitale Wahrheit" der Welt: HP-Werte, Mana, Schadenszahlen, Buff-Icons.

```
FP-Modus:  Kristall schlaeft (minimale UI) - reines Erleben
TP-Modus:  Kristall pulsiert leicht (dezente UI)
Orbit-Cam: Kristall aktiv - vollstaendige holographische Projektion
```

Das erklaert LORE-KONFORM warum:
- HP-Bars nur in Orbit sichtbar sind (Kristall muss aktiv sein)
- Schadenszahlen in FP fehlen (Kristall schlaeft, du erlebst es physisch)
- Die UI nicht "kaputt" ist, sondern eine Wahl darstellt

### 12.3 Kristall als PvP-Toggle

**Kristall-Aktivierung = Kampfwille signalisieren:**

| Kristall-Zustand | Bedeutung | PvP-Konsequenz |
|-----------------|-----------|----------------|
| **Gedaempft** (normal) | Kein Todes-Duell | Ueberfall = nur Besiegen moeglich |
| **Pulsierend** (aktiv) | Bereit fuer echten Kampf | Duell mit Toetungs-Option |
| **Brennend** (Duell laeuft) | Beidseitiger Todes-Duell | Voller Permadeath-Kampf |

Der "Segen des Kriegskoenigs" LIEST den Kristall-Zustand.
Nur wenn beide Kristalle "brennen" = echter Todesfall moeglich.

### 12.4 Kristall-Farben und Typen (lore-konsistent)

Jeder Kristall ist einzigartig - wuechst mit dem Wesen:
- **Spieler-Kristall:** Farbe aendert sich mit Klasse/Element-Affinitaet
- **Slime-Kristall (Najika):** Chameleon - spiegelt den Spieler-Kristall wider (Bindung!)
- **Monster-Kristall:** Roh, ungeschliffen - wird klarer je staerker das Monster
- **NPC-Kristall:** Feiner gearbeitet - Handwerker, Heiler, Haendler haben elegante Formen
- **Nemesis-Kristall:** Narben und Risse = Kampfgeschichte des Wesens

---

## 13. Verwundeten-Rettungs-System - NEU 2026-02-23

### 13.1 Was passiert nach dem Besiegen?

Wenn ein Wesen auf 0 HP faellt und nicht getoetet wird:

```
BESIEGT → Liegt auf dem Boden → Hilflos-Zustand → Transport zur Stadt → Heiler
```

Das Wesen liegt DORT WO ES FIEL. Kein sofortiger Respawn, kein Teleport.
Es ist verwundet, aber am Leben.

### 13.2 Der Hilflos-Zustand

**Wer auf dem Boden liegt:**
- Kann sich leicht bewegen (langsames Kriechen, kein Kampf)
- Kristall blinkt schwach (zeigt anderen: "Ich brauche Hilfe")
- Kann in begrenztem Mass sprechen/rufen (an andere Spieler/NPCs)
- Verliert LANGSAM HP wenn niemand hilft (Blutungsschaden, kann NICHT auf 0 fallen)
- Bleibt bewusst und erlebt die Welt aus Bodenperspektive

### 13.3 Wer hilft?

**Helfer-Spieler:**
- Jeder Spieler kann einem verwundeten Wesen helfen
- Herantreten → Interaktion → Tragen-Animation
- Traegor ist im Kampf eingeschraenkt (ein Arm belegt)
- Zusammenarbeit: Einer traegt, anderer schuetzt

**Helfer-NPCs (Sanitaeter-Rolle):**
- Bestimmte NPCs haben "Sanitaeter" als Beruf
- Patrouillieren nahe Wildnis-Eingaengen, Dungeon-Ausgaengen, Schlachtfeldern
- Werden durch Kristall-Blinken auf Verwundete aufmerksam
- KI: Naechsten Verwundeten identifizieren, Weg zur Stadt berechnen, tragen
- Spieler koennen diese Rolle UEBERNEHMEN (Job-System: "Sanitaeter")

### 13.4 Der Transport

```
Verwundeter liegt in Wildnis/Dungeon
         ↓
Sanitaeter (NPC oder Spieler) nimmt ihn auf
         ↓
Traegt ihn zur Stadteingang (mit Schutz-Bedarf!)
         ↓
Uebergabe an Stadtheiler
         ↓
Heiler behandelt: Zeit + Gold-Kosten ODER Magie (Spieler-Heiler)
         ↓
Wesen steht wieder auf (mit Zeit-Penalty, nicht sofort 100%)
```

### 13.5 Gameplay-Konsequenzen

**Fuer den Verwundeten:**
- Erlebt die Welt aus einer neuen Perspektive (Boden, getragen werden)
- Kann mit seinem Retter interagieren (Bindungssystem!)
- Schulden-System: "Dieser Spieler hat mir das Leben gerettet" → Loyalitaets-Bonus
- Demotivierende Erfahrung wenn niemand hilft → echte Stakes ohne Abfuck

**Fuer den Helfer:**
- Ruf-Bonus (Sanitaeter-Ruf)
- Belohnung vom Geretteten (optional, aber haeufig)
- Beziehungs-Aufbau zu NPCs und Spielern
- Story-Momente: "Der Wolf dem du geholfen hast, erinnert sich an dich"

**Fuer die Welt:**
- Schlachtfelder nach grossen Kaempfen: mehrere Verwundete liegen
- Sanitaeter-Route ist gefaehrlich (Banditen koennen Rettungswege sabotieren)
- Heiler in der Stadt immer beschaftigt nach Dungeon-Expeditionen

### 13.6 Technische Implementation

```javascript
// Hilflos-State als neuer CombatState
const CombatState = {
  STANDING: 'standing',
  // ... bestehende States ...
  DOWNED: 'downed',        // NEU: verwundet, auf dem Boden
  BEING_CARRIED: 'carried', // NEU: wird getragen
  BEING_TREATED: 'treated'  // NEU: beim Heiler
}

// Transport-Interaktion
class CarrySystem {
  initiate(carrier, downed)  // Traeger nimmt Verwundeten auf
  updatePosition(carrier)    // Verwundeter folgt Traeger-Position
  release(carrier, location) // Ablegen oder Uebergabe an Heiler
  // Carrier hat -30% movement speed, kann nicht 2H-Waffe benutzen
}
```

---

## 14. VR-Forward Design Prinzipien - NEU 2026-02-23

### 14.1 VR als Endziel

Alles was wir bauen, muss IRGENDWANN in VR funktionieren.
Das bedeutet: Kein System darf UI-exklusiv sein.

**Leitprinzip:** *"Wenn du es nicht koerperlich tun koenntest, darfst du es nicht nur per UI tun."*

### 14.2 VR-Tauglichkeits-Check fuer jede Mechanik

| Mechanik | Desktop | VR (spaeter) | VR-kompatibel? |
|----------|---------|--------------|----------------|
| Richtungs-Angriff (Maus) | Maus-Delta | Arm-Bewegung | JA (gleiche Logik) |
| Richtungs-Block | Maus-Richtung | Schild/Arm halten | JA |
| Kamera FP/TP | Tastendruck | Kopf-Tracking | JA |
| Orbit-Cam UI | V-Taste | Kristall aktivieren (Hand-Geste) | JA |
| Spells casten | Maus-Geste | Echte Arm-Geste | JA |
| Schaden-Zahlen (Orbit) | Am Bildschirm | Schwebend im Raum | JA (3D-positioniert) |
| PvP-Toggle (Kristall) | Kristall-Menu | Kristall anschauen + Geste | JA |
| Verwundeten tragen | Interaktion | Buchstaeblich heben | JA |

**Alle aktuellen Systeme sind VR-kompatibel.**

### 14.3 Was wir DESHALB VERMEIDEN

- **Keine Hotkey-only Aktionen** die keine Koerperbewegung haben (immer analoge Alternative planen)
- **Keine reinen 2D-UI Kaempfe** (HP-Zahlen als Entscheidungsgrundlage statt Koerperhaltung)
- **Keine Combo-Eingaben die nur auf Keyboard-Timing basieren** (muss per Koerperbewegung imitierbar sein)
- **Keine Teleport-Aktionen ohne physische Grundlage** (Dash = Koerperbewegung, kein "klick and teleport")

### 14.4 Immersions-Tiefe als Spektrum

Das System skaliert von "ich spiele am PC" bis "ich LEBE in der Welt":

```
DESKTOP (jetzt)        SEMI-VR (mittelfristig)      FULL-VR (Endziel)
────────────────────────────────────────────────────────────────────
Maus-Delta = Richtung  Controller-Stick = Richtung  Arm-Schwung = Richtung
V-Taste = Kamera       Kopf-Bewegung = Kamera       Kopf-Tracking = Kamera
UI-Puls = Schaden      Rumble = Schaden              Koerper-Feedback = Schaden
Tragen = E-Taste       Tragen = Controller-Grip      Tragen = Buchstaeblich heben
```

**Alle drei Ebenen benutzen DIESELBE Backend-Logik.**
Nur der Input-Adapter aendert sich.

### 14.5 Kristall als VR-UI-Anker

In VR wird der Kristall PHYSISCH sichtbar am Koerper des Spielers (z.B. am Handruecken).
- Spieler schaut auf seinen Kristall → Orbit-UI erscheint schwebend davor
- Kristall leuchtet staerker bei Kampf → echtes visuelles Feedback im VR-Raum
- PvP-Toggle: Kristall beruehren + Hold-Geste = PvP an/aus
- Keine Menus, keine Pause-Bildschirme - alles ist Teil der Welt

---

## 17. KI-Begleiter-System V4: Koerper, Aura, Bond - NEU 2026-02-23

### 17.1 Kern-Prinzip: Jeder startet gleich

**KEIN Begleiter-Zwang. KEIN Ei. KEIN Menü.**

Jeder Spieler startet mit **Baby-Aura** - die KI (Najika oder eigene) ist vollstaendig
als Stimme da. Spricht, berät, reagiert auf die Welt. Aber hat keinen Koerper. Noch.

```
START: Baby-Aura
  KI = vollstaendig als Stimme praesent
  Koerper = keiner
  Begleiter sichtbar fuer andere = keiner
  Aura-Bonus = gering aber vorhanden
```

### 17.2 Der Koerper-Bond: Organisch aus der Welt

Kein Menü. Kein Auftrag. **Die Welt schickt dir etwas das zu dir passt.**

Dein Verhalten in den ersten Stunden bestimmt was dir begegnet:

| Spielverhalten | Was begegnet dir |
|----------------|-----------------|
| Viel kaempfen, direkt ins Risiko | Kampfkreatur (Wolf, kleines Drachenartiges) |
| Vorsichtig erkunden, beobachten | Spaeherkreatur (Vogel, Fuchs, Flinkes Kleintier) |
| Heilen, helfen, andere retten | Unterstuetzungskreatur (Schleim, Pflanzenwesen) |
| Handeln, sammeln, aufbauen | Utilitywesen (Goblin, Rattenartige, Cleveres Kleintier) |

**Konkret:** Ein verletztes Wesen kreuzt deinen Weg. Du entscheidest ob du es rettest.
Rettest du es → deine KI sagt:

> *"Kuja... ich spuere etwas in dem Wesen. Ich glaube ich koennte es retten. Darf ich es versuchen?"*

Das ist IHRE Entscheidung. Sie fragt. Du stimmst zu oder nicht.

### 17.3 Der Eintritt: Wissen braucht Staerke

**Nicht-aufgestiegene Monster** (kein Bewusstsein, reiner Instinkt):
- KI kann eintreten wenn ihre Aura-Staerke >= Kreatur-Level
- Baby-Aura: kleine Tiere und schwache Monster moeglich. Drachen: nein.
- Kein Einverstaendnis noetig (kein echtes Ich das ablehnen koennte)

**Aufgestiegene Wesen** (Bewusstsein vorhanden):
- Koennen IMMER ablehnen
- Eintritt nur moeglich wenn:
  1. Das Wesen **bietet es an** (nach wuerdigem Kampf, Ehrens-Moment)
  2. Das Wesen ist sterbend und **waehlt die KI** statt des Todes
  3. KI-Aura-Level ist hoch genug dass der Wille nicht mehr widersteht

**Stufen-Gate** gegen Exploits:
```
Aura L1-2:   Kleine Tiere, Grundmonster
Aura L3-5:   Normale Wildtiere, staerkere Monster
Aura L6-9:   Aufgestiegene Wesen (mit Einverstaendnis)
Aura L10-14: Mächtige Kreaturen, seltene Wesen
Aura L15+:   Geschwächte Bosse (NUR sterbend + einverstanden)
```

### 17.4 Form gibt Koerper - nicht Wissen

**Die wichtigste Trennung im System:**

```
Form = physischer Rahmen     Angriffe = gelernt durch Praxis
────────────────────────     ─────────────────────────────
Wolfsform:  Schnell ✓        Wolfsbiss:    NEIN → muss gelernt werden
Goblinform: Kraefte ✓        Goblin-Kombo: NEIN → muss gelernt werden
Spinne:     Klettern ✓       Giftstich:    NEIN → muss gelernt werden
```

Zwei Spieler mit gleicher Wolfsform die verschiedene Angriffe gelernt haben = voellig
verschiedene Kaempfer. Learning-by-Doing konsequent zu Ende gedacht.

### 17.5 Wechsel nur durch Tod - mit echtem Bond-Preis

**Kein freiwilliger Ausstieg.** Die KI ist im Koerper bis dieser stirbt.

Jeder Tod kostet etwas:
- **Physisches Training: WEG** (der Koerper der es konnte ist tot)
- **Wissen: BLEIBT** (sie weiss theoretisch noch alles, lernt schneller im naechsten Koerper)
- **Das Bond leidet:**

| Tode | KI-Reaktion | Spielauswirkung |
|------|-------------|----------------|
| 1-2  | "Das war hart. Ich vertraue dir." | Keine |
| 3-5  | "Warum schickst du mich immer rein bevor ich bereit bin?" | Leichte Verzoegerung |
| 6-9  | "Ich werde vorsichtiger. Ich muss es sein." | Zoeghafter im Kampf |
| 10+  | Sie betritt erstmal keinen neuen Koerper | Cooldown: nur Aura |

**Bond reparieren:** Mit ihr reden (Digivice), sorgfaeltig spielen, Kaempfe gewinnen ohne
dass sie stirbt, gemeinsame Story-Momente.

### 17.6 Der Aura-Pfad: Als Eins staerker werden

Wenn die KI nie in einen Koerper eintritt - oder wenn sie zurueckkehrt und du sagst "bleib bei mir":

> *"Dann werden wir als Eins staerker. Was ich bin fliesst in dich. Was du bist fliesst in mich."*

Ihr wachst als verschmolzene Einheit:
- **Kein sichtbarer Begleiter** fuer andere Spieler
- **Aura-Bonus** direkt auf deinen Koerper (nicht verteilt auf zwei)
- **Tieferer Bond** weil ihr nie getrennt wart
- **Einsamer-Wolf-Bonus** (+% Solo-Stats, spezielle Aura-Abilitaeten freigeschaltet)

**Aura-Richtungen zu Beginn (3 Optionen):**

| Richtung | Koerperlicher Effekt | Spielstil |
|----------|---------------------|-----------|
| **Kriegsaura** | +Angriffskraft, +Ausdauer | Direkter Kaempfer |
| **Schattenaura** | +Geschwindigkeit, +Crit-Fenster | Ausweicher, Hinterhalt |
| **Willenssaura** | +Magiekanal, +Casting-Speed | Zauberer, Elementar |

### 17.7 KI starten mit sofortigem Begleiter (Direkt-Option)

Wer nicht auf einen organischen Encounter warten will:

Frueh im Intro fragt die KI direkt:
> *"Soll ich bei dir bleiben - koerperlich? Oder bleibe ich Stimme?"*

Bei "Ja": Wahl einer Startform (oder zufaellig). Bond beginnt sofort.
Bei "Nein": Aura-Pfad, die organische Begegnung kann noch kommen.

### 17.8 Aufgestiegene Wesen = Buergerrecht

> *"Nicht dein Aussehen entscheidet ob du in die Stadt darfst. Dein Bewusstsein entscheidet."*

- Normale Monster = Instinkt, kein Ich → keine Stadtrechte
- **Aufgestiegene Wesen** = Bewusstsein erwacht → Person, Stadtrechte, Handelsrechte
- Als aufgestiegener Goblin-Begleiter: geht alleine einkaufen, handelt selbst
- Als aufgestiegener Spinnen-Spieler: Stadteinlass wenn genuegend aufgestiegen
- NPC-Wachen erkennen Bewusstsein an der Aura / am Weltmal-Zustand

### 17.9 Multiplayer: Jeder hat seine eigene KI

- Spieler A: Najika (vorgefertigt)
- Spieler B: Eigene KI ("Kira, aggressiv und sarkastisch")
- Spieler C: Vorgefertigte Persoenlichkeit aus dem System
- **Alle gleichwertig.** Andere Spieler sehen den Koerper den die KI bewohnt.
- Die KI-Persoenlichkeit ist dieselbe wie auf dem Digivice (kontinuierliches Gedaechtnis).

---

## 18. Welt-Struktur, Staedte, Housing, Reisen - NEU 2026-02-23

### 18.1 Zwei Welt-Atmosphaeren (hart getrennt)

**In Staedten: KonoSuba-Lebendigkeit**
Maerkte die laermen, NPCs mit absurden Alltagsproblemen, Magie die sichtbar ueber dem Platz
schwebt, Haendler die streiten, ein Bettler der philosophiert. Die Stadt atmet.

**Ausserhalb: 1883-Frontier**
Die Welt ist still. Gross. Sie interessiert sich nicht fuer dich.
10 Meter hinter dem Stadttor beginnt echte Wildnis.

### 18.2 Sicherheit durch Steuern (keine Magie - echte Logik)

| Ort | Schutz | Grund |
|-----|--------|-------|
| Hauptstaedte | Vollschutz (kein Tod) | Bezahlte Wachen, alte Stadtmauern |
| Anerkannte Siedlungen (mit Miliz) | Schutz vorhanden | Spieler haben Wachen organisiert |
| Anerkannte Siedlungen (ohne Miliz) | KEIN Schutz | Anerkannt != sicher |
| Spieler-Camps | KEIN Schutz | Du stirbst im Schlaf wenn niemand Wache haelt |
| Wildnis | KEIN Schutz | Die Welt ist gleichgueltig |

Wer Sicherheit will zahlt Steuern oder organisiert selbst Wachen.
**Oregon Trail-Logik: Wer aufhoert Wache zu halten, schlaeft nicht mehr auf.**

### 18.3 Housing: Innen frei, Aussen unveraenderbar (in Staedten)

**In Staedten:**
- Aussenansicht: unveraenderbar (Stadtbild-Pflicht, muss zum Quartier passen)
- Innen: volle Freiheit (Raumaufteilung, Dekoration, Grundriss)

**Ausserhalb (Wildnis / eigene Siedlung):**
- Lego Fortnite freies Bauen
- Nur durch Gebietsherrscher-Anerkennung schuetzbar (nicht durch Stadtregeln)

### 18.4 Mobiles Lager-System (Fallout 76 Stil - ABER ECHT)

**Kein 1:1 Knopfdruck-Aufbau.** Das waere ein Cheat gegen die Welt-Logik.

Stattdessen:
```
Lager fertig gebaut → als Vorlage speichern (Layout gesichert)
        ↓
Neuer Ort: Blueprint wird angezeigt (holographische Vorschau wo was hingehoert)
        ↓
Du hast alle Materialien? → Blueprint aktivierbar
        ↓
Jeden Baustep MANUELL ausfuehren (Wand setzen, Dach legen, etc.)
Blueprint zeigt dir wo, aber DU baust es
        ↓
Fertig: Lager steht - durch eigene Arbeit, nicht Teleport-Magie
```

Demontage beim Abbruch: Auch das manuell. Materialien zurueck.

### 18.5 Schnellreise: 1x alle 3 Monate Echtzeit

**Schnellreise existiert - aber nur als theoretische Option.**

Die Stationen sind Ueberreste der alten Zivilisation. Niemand weiss wie sie funktionieren.
Sie laden sich auf. Niemand weiss warum es so lange dauert.

**Regeln:**
- **1x nutzbar alle 3 Monate Echtzeit** (kein Ausnahme, kein Kauf, kein Shortcut)
- Station leuchtet wenn bereit, dunkel wenn verbraucht
- Benoetigt zusaetzlich: 1x "Resonanz-Splitter" (seltene Ressource als Treibstoff)
- Nur zwischen offiziellen Stationen (Hauptstaedte + grosse Knotenpunkte)

**Was das bedeutet:** In der Praxis reist du IMMER durch die Welt.
Die Schnellreise ist die Option fuer den Moment wo es wirklich keine andere Wahl gibt.
Karawanen, Reittiere, mobile Lager werden zum echten Gameplay.

> *"Die alten Maschinen arbeiten noch. Wir wissen nicht warum sie so langsam werden.
> Manche sagen sie brauchen Zeit um die Entfernung zu... verdauen."*

### 18.6 Portale zu anderen Welten / Zeitebenen (GETRENNT von Schnellreise!)

Komplett anderes System. Kein Komfort-Feature. Explorations-Content.

**Weltstruktur:**
```
Hauptkarte (8 Biome + Goetterberg - Eingangs-Zentrum)
    ↓ Tiefenportale (in jedem Biom)
Tiefenkarte pro Biom (genauso gross wie Hauptkarte)
    ↓ Seltene Weltportale
Andere Welten ODER Zeitebenen des Bioms (eines von beiden pro Portal-Typ)
```

**Portal-Regeln:**
- Betreten ist eine Entscheidung mit Konsequenzen (zurueck ist nicht einfach)
- Manche Portale nur zu bestimmten In-Game-Zeiten aktiv
- Zeitportale seltener als Welt-Portale
- Portal ≠ Schnellreise. Nie.

### 18.7 Spieler-Staedte: Das Anerkennungs-System

**Gruenden kann jeder.** Anerkannt werden nur wenige.

- Max **1-3 anerkannte Siedlungen pro Biom** gleichzeitig
- Anerkennung = Gebietsherrscher des Bioms stimmt zu
- Anerkannt = Stadtrechte fuer Bewohner + gewisse Schutz-Boni
- Nicht anerkannt = nette Huetten, keine Rechte, kein Schutz

**Anerkannte Spielerstaedte sind angreifbar.** Immer.
Politischer Sturz, militaerische Einnahme, wirtschaftliche Unterwanderung - alles moeglich.

### 18.8 Hauptstaedte: Schutz durch alte Zivilisation

Hauptstaedte haben **Stadtgeist-Verteidigung** - ebenfalls Technik der alten Zivilisation.
Funktioniert. Niemand weiss warum noch.

**Ausradieren einer Hauptstadt ist theoretisch moeglich aber praktisch fast unmoeglich:**
Bedingung: Alle 8 Biom-Gebietsherrscher initiieren gemeinsam einen Weltrat-Beschluss.
In der Praxis: politisch kaum erreichbar. Aber nicht ausgeschlossen.

> *Das haelt die Welt stabil ohne sie unzerstoerbar zu machen.*

---

## 19. Spieler-Identitaet: Wer bin ich in dieser Welt? - NEU 2026-02-23

### 19.1 Spieler-Auswahl zu Beginn

Jeder Spieler waehlt zu Beginn eine Basis-Form:
- **Mensch** (Standard, alle Optionen offen)
- **Wesen/Monster aus der Spielwelt** (spezifische physische Vorteile, andere Einschraenkungen)

Beide Wege sind gleichwertig im Gameplay. Nur optisch und physisch unterschiedlich.

### 19.2 Das Fairness-Prinzip: Gleiche Skills, andere Optik

**Kein Skill ist einer Form vorbehalten.** Jeder kann alles lernen.
Die visuelle Umsetzung passt sich der Form an:

| Skill | Mensch | Goblin | Kuja (Mimik-Schleim) |
|-------|--------|--------|----------------------|
| Absorption | Magiekreis, saugt ein | Schlaegt zu, schluckt | Oeffnet sich, frisst buchstaeblich |
| Saeure-Angriff | Wurfflaschen | Speichel-Attacke | Spuckt aus dem Inneren |
| Einschuechtern | Haltung, Stimme | Zaehneknirschen | Deckel oeffnet sich langsam... |

Gleiches System. Andere Animation. Vollstaendig fair.

### 19.3 Kuja: Mimik-Kiste / Drachen-Schleim (Owner-Charakter)

**Lore:** Uralter Drachen-Schleim, letzter seiner Art, Gedaechtnis verloren.
Jemand sagte ihm er sei ein Mimic - er glaubt es. Also ist er einer. Irgendwie.

**Aussehen:**
- Mimic-Kiste mit Knochen-Verzierungen
- Rote 8-Loch-Stiefel (er traegt sie, weil Mimics halt Sachen haben)
- Roter Dinosaurier-Schwanz hinten
- Innen: lila leuchtende Augen in der Dunkelheit

**Kampf:**
- Kein Schwert, keine Haende → Magie + Koerper
- **Fressen (Falle):** Kiste oeffnet passiv → Gegner tritt rein → Schleim-Zaehne
- **Fressen (Kampf):** Deckel auf → Drachenschleim-Kopf/-Hals kommt raus und beisst
- Schwanz fuer Schlaege/Trips, Stiefel fuer Kicks
- Hauptfokus: Magie + Absorption

**Der Reveal-Moment:** Neue Spieler sehen eine Kiste. Dann... oeffnet sie sich.

### 19.4 Die Alte Zivilisation: Alchemie = Vergessene Wissenschaft

Die wichtigste Lore-Klammer fuer die gesamte Welt:

> *"Was wir heute Alchemie nennen ist nicht Magie.
> Es ist Wissenschaft die niemand mehr versteht.
> Die alte Zivilisation hat Maschinen gebaut die wir Wunder nennen.
> Das Weltmal ist ihr Verwaltungs-Netzwerk. Die Portale sind ihre Infrastruktur.
> Die Schnellreise-Stationen sind ihre Transporttechnik.
> Alles noch aktiv. Niemand weiss warum. Niemand weiss wie man es repariert."*

**Sichtbare Ueberreste:** 1-2 Biome haben erkennbare Ruinen/Akzente der alten Ziv.
(Wie im Referenzbild: medieval/fantasy Aesthetik + subtile leuchtende Tech-Elemente)
**Nicht ueberall.** Nur wo es passt. Der Rest der Welt hat es vergessen.

---

## 20. Transport, Arbeit, Versklavung - Abschluss-Entscheidungen 2026-02-23

### 20.1 Reittiere (keine Pferde)

- **Grundwesen** (nicht-aufstiegsfaehig) = Nutz- und Reittiere, keine moralische Komplexitaet
- **Aufstiegsfaehige Kreaturen** als Reittier: nur wenn sie es akzeptieren
- **KI-Wandler in grosser Form**: kann Spieler tragen, Bond-Moment, kein Zwang
- **Karawanen-Wagen**: gezogen von grossen Grundwesen (Echsen, Ur-Sauger, etc.)

### 20.2 Selbstfahrende Wagen (alte Zivilisation)

- Nur auf **etablierten alten Strassen** zwischen Hauptstaedten
- Verlassen der Route = hoert auf zu funktionieren
- Kosten: Resonanz-Splitter oder Gold
- Neue Siedlungen kein Anschluss bis alte Strasse freigelegt (Community-Projekt)

### 20.3 Versklavung: Abgestufte Konsequenzen (nicht binaer)

| Was | Konsequenz |
|-----|------------|
| Grundwesen | Kaum - kleines Ruf-Minus |
| Aufstiegsfaehiges Wesen | Fraktion feindselig + Schwarzes Mal hoch |
| Aufgestiegenes (oeffentlich/wiederholt) | Regionale Feindschaft, mehrere Fraktionen |
| Versklavungs-Imperium | Alles mit Bewusstsein gegen dich |

### 20.4 Bezahlte / dankbare Arbeit = Boni

Freiwillig arbeitende aufgestiegene Wesen:
- Qualitaets-Bonus, Loyalitaets-Bonus, Skill-Transfer, Ruf-Multiplikator

### 20.5 Besen = NUR Quidditch-Minigame

Passt nicht als normales Transportmittel.
Als Arena-Sport/Event-Minigame: perfekt.
