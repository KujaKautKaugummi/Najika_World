# Neues System: Gewicht, Wagen, Arbeiter & Logistik

## Status: DESIGN - Noch nicht implementiert

## Kernprinzipien
- Items haben GEWICHT (Ressourcen, Loot, Holz, Erze, etc.)
- Überladung = langsamer laufen, schneller erschöpft
- KEINE PFERDE - Monster/Kreaturen oder Sklaven ziehen Wagen
- Tod = alles verloren (Roguelike), daher Wagen selten & wertvoll (Oregon Trail Charm)

## Gewichtssystem
- Jedes Item hat Gewicht (kg)
- Spieler hat Tragekapazität basierend auf STR/VIT
- Überladung:
  - >80% Kapazität = Bewegung -20%
  - >100% = Bewegung -50%, Ausdauer sinkt doppelt
  - >120% = kann nicht mehr laufen
- 100 Bäume fällen = kann man NICHT ins Inventar stecken → braucht Wagen

## Wagensystem
- **Planwagen** (groß): Viel Kapazität, langsam, braucht Zugtier
- **Kleiner Karren**: Weniger Kapazität, schneller, 1 Kreatur reicht
- **Handkarren**: Kleinste Option, Spieler zieht selbst

### Wagen bekommen:
- **Selbst bauen** (Holz + Räder + Handwerk-Skill)
- **Kaufen** (teuer)
- **Mieten** (pro Strecke/Zeit)
- **Stehlen** → Zeugen → Kopfgeld → Jäger kommen

### Zugtiere:
- Monster/Kreaturen aus Taming-System
- Sklaven können auch Wagen ziehen
- KEINE Pferde (Designentscheidung)

## Arbeitersystem (Jobs & Aufträge)
Spieler kann andere beauftragen statt alles selbst zu machen:

### Beispiel: 100 Bäume fällen
- Option A: Selbst fällen (kostenlos, zeitaufwändig, braucht eigenen Wagen)
- Option B: Holzfäller-Trupp anheuern (Kosten: Gold pro Baum)
  - Braucht: Holzfäller (x3-5), Wache (x1-2), Kutscher (x1)
  - Waren werden geliefert
- Option C: Eigene Sklaven/Rekruten von der Farm schicken
  - Spart Gold, riskiert Verlust bei Überfall

### Job-Rollen:
- **Holzfäller** - Ressourcen sammeln
- **Wache** - Schutz für Transporte und Städte
- **Kutscher** - Fährt Wagen
- **Minenarbeiter** - Erze abbauen
- **Jäger** - Pelze, Fleisch
- **Fischer** - Fisch

### Selbst arbeiten:
- Spieler kann jede Rolle selbst übernehmen
- Spart Geld, dauert länger
- Kann z.B. selbst Wache + Transport übernehmen

## Stadt-Wachsystem
- Städte brauchen Wachen für Sicherheit
- Kreaturen/NPCs arbeiten als Wachen (Schichten)
- Spieler kann:
  - Schicht übernehmen (bezahlt)
  - Zusätzlich zur Kreatur-Wache kommen
  - Eigene Kreaturen als Wachen einsetzen
- Immer genug Wachen = Stadt ist sicher
- Zu wenig Wachen = Überfälle, Diebstahl

## Kopfgeld-System (bei Diebstahl)
- Wagen stehlen → Zeugen melden es
- Kopfgeld steigt mit Schwere des Verbrechens
- Kopfgeldjäger spawnen und jagen den Spieler
- In Hardcore-Welt = extrem gefährlich
- Kopfgeld kann bezahlt werden (Bestechung) oder verfällt über Zeit

## Diebstahl-Mechanik
- Im gestohlenen Wagen gesehen werden → Alarm
- Nachts stehlen = weniger Zeugen
- Verkleidung hilft
- Gestohlene Waren haben "gestohlen" Tag
- Händler kaufen gestohlene Waren nur zu 30% Preis (Hehler-System)

## Tod & Verlust
- Bei Tod: ALLES in der Welt verloren (Inventar, Wagen, Waren)
- Andere Spieler können Leiche looten
- Motiviert vorsichtiges Spielen
- Wagen sind wertvoll → nicht leichtfertig riskieren
- Oregon Trail Feeling: Jede Reise ist ein Risiko

## Notizen für später:
- Dice Monsters System komplett neu designen (aus Spiel entfernt)
