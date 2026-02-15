#!/usr/bin/env python3
"""
ChromaDB Backup + Sauberer Reset für Najika World
==================================================
1. Exportiert gute Daten nach backend/najika_clean_backup/
2. Löscht die komplette memory_db/
3. Reimportiert nur saubere Daten + neue Character-Bible Einträge

KEIN project_knowledge, KEIN md_knowledge, KEIN najika_wichtige_docs!
Diese Collections enthielten 92% Projekt-Müll der die Chat-Qualität ruiniert hat.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import chromadb
import json
import os
import shutil
import time
import re
from datetime import datetime

MEMORY_DB = "C:/Najika_World/memory_db"
BACKUP_DIR = "C:/Najika_World/backend/najika_clean_backup"

# ===== QUALITY FILTER =====

def quality_score(text):
    """Bewertet die Qualität einer Konversation (0-5)"""
    score = 0

    # Hat *Aktionen in Sternchen*? (+2)
    if re.search(r'\*[^*]{3,}\*', text):
        score += 2

    # Hat Kuja/Mr.K? (+1)
    if re.search(r'(?i)(kuja|mr\.?\s*k)', text):
        score += 1

    # Natürliche Länge 30-500 chars? (+1)
    if 30 <= len(text) <= 500:
        score += 1

    # Hat Emoji? (+0.5)
    if any(c in text for c in "💕🥺✨💥😏😤💗💋"):
        score += 0.5

    # PENALTIES
    garbage_markers = [
        "MASTER_TODO", "CLAUDE.md", "claude.md", "Projekt-Anweisungen",
        "Was kann ich für dich tun", "Ich bin bereit", "AI-Systeme offline",
        "LM Studio", "[ANALYSIS]", "[PROAKTIV]", "MEGUMIN-MODUS",
        "MELISSA-MODUS", "Puddin'", "Berechtigung", "Tut mir leid für den Missverstand",
        "```", "def ", "import ", "class ", "function ", "SCHWIERIGKEITSGRAD",
        "NSFW-Intensität", "auf der anderen Seite des Internet",
    ]
    for marker in garbage_markers:
        if marker in text:
            score -= 3
            break

    return max(0, score)


def is_nsfw(text):
    """Prüft ob eine Konversation NSFW-Inhalte hat"""
    nsfw_markers = [
        "kätzchen", "kaetzchen", "stöhn", "erregt", "nackt", "auszieh",
        "küss", "kuss", "bett", "schlafzimmer", "intim", "lust",
        "private_mode\": \"True", "private_mode': True",
    ]
    text_lower = text.lower()
    return any(m in text_lower for m in nsfw_markers)


# ===== PHASE 1: BACKUP =====

def backup_all():
    """Exportiert alle guten Daten"""
    os.makedirs(BACKUP_DIR, exist_ok=True)

    print("=" * 60)
    print("PHASE 1: ChromaDB BACKUP")
    print("=" * 60)

    client = chromadb.PersistentClient(path=MEMORY_DB)

    # Liste alle Collections
    all_collections = client.list_collections()
    print(f"\nGefundene Collections: {len(all_collections)}")
    for col in all_collections:
        print(f"  - {col.name}: {col.count()} Einträge")

    stats = {
        "timestamp": datetime.now().isoformat(),
        "collections": {}
    }

    # 1. Conversations (quality_score >= 2.0)
    try:
        conv = client.get_collection("conversations")
        total = conv.count()
        print(f"\n[1/5] Conversations: {total} total")

        # In Batches laden (ChromaDB-Limit)
        sfw_good = []
        nsfw_good = []
        garbage = 0

        batch_size = 100
        for offset in range(0, total, batch_size):
            results = conv.get(
                limit=batch_size,
                offset=offset,
                include=["documents", "metadatas"]
            )

            for i, doc in enumerate(results["documents"]):
                meta = results["metadatas"][i] if results["metadatas"] else {}
                doc_id = results["ids"][i]

                score = quality_score(doc)

                if score >= 2.0:
                    entry = {
                        "id": doc_id,
                        "document": doc,
                        "metadata": meta,
                        "quality_score": score
                    }

                    if is_nsfw(doc) or meta.get("private_mode") == "True":
                        nsfw_good.append(entry)
                    else:
                        sfw_good.append(entry)
                else:
                    garbage += 1

        print(f"  SFW gut: {len(sfw_good)}")
        print(f"  NSFW gut: {len(nsfw_good)}")
        print(f"  Müll: {garbage}")

        with open(f"{BACKUP_DIR}/conversations_sfw.json", "w", encoding="utf-8") as f:
            json.dump(sfw_good, f, ensure_ascii=False, indent=2)
        with open(f"{BACKUP_DIR}/conversations_nsfw.json", "w", encoding="utf-8") as f:
            json.dump(nsfw_good, f, ensure_ascii=False, indent=2)

        stats["collections"]["conversations"] = {
            "total": total, "sfw_kept": len(sfw_good),
            "nsfw_kept": len(nsfw_good), "garbage": garbage
        }
    except Exception as e:
        print(f"  FEHLER: {e}")

    # 2. najika_core (alle behalten - korrigierte Einträge)
    try:
        core = client.get_collection("najika_core")
        total = core.count()
        print(f"\n[2/5] najika_core: {total} total")

        results = core.get(include=["documents", "metadatas"])
        entries = []
        for i, doc in enumerate(results["documents"]):
            entries.append({
                "id": results["ids"][i],
                "document": doc,
                "metadata": results["metadatas"][i] if results["metadatas"] else {}
            })

        with open(f"{BACKUP_DIR}/najika_core.json", "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

        print(f"  Gesichert: {len(entries)}")
        stats["collections"]["najika_core"] = {"total": total, "kept": len(entries)}
    except Exception as e:
        print(f"  FEHLER: {e}")

    # 3. najika_personalities (Video-Transcripts - alle behalten)
    try:
        pers = client.get_collection("najika_personalities")
        total = pers.count()
        print(f"\n[3/5] najika_personalities: {total} total")

        entries = []
        batch_size = 50
        for offset in range(0, total, batch_size):
            results = pers.get(
                limit=batch_size, offset=offset,
                include=["documents", "metadatas"]
            )
            for i, doc in enumerate(results["documents"]):
                entries.append({
                    "id": results["ids"][i],
                    "document": doc,
                    "metadata": results["metadatas"][i] if results["metadatas"] else {}
                })

        with open(f"{BACKUP_DIR}/najika_personalities.json", "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

        print(f"  Gesichert: {len(entries)}")
        stats["collections"]["najika_personalities"] = {"total": total, "kept": len(entries)}
    except Exception as e:
        print(f"  FEHLER: {e}")

    # 4. emotions (alle behalten)
    try:
        emo = client.get_collection("emotions")
        total = emo.count()
        print(f"\n[4/5] emotions: {total} total")

        entries = []
        batch_size = 100
        for offset in range(0, total, batch_size):
            results = emo.get(
                limit=batch_size, offset=offset,
                include=["documents", "metadatas"]
            )
            for i, doc in enumerate(results["documents"]):
                entries.append({
                    "id": results["ids"][i],
                    "document": doc,
                    "metadata": results["metadatas"][i] if results["metadatas"] else {}
                })

        with open(f"{BACKUP_DIR}/emotions.json", "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)

        print(f"  Gesichert: {len(entries)}")
        stats["collections"]["emotions"] = {"total": total, "kept": len(entries)}
    except Exception as e:
        print(f"  FEHLER: {e}")

    # 5. Memory-System Collections (relationships, events)
    for col_name in ["relationships", "events"]:
        try:
            col = client.get_collection(col_name)
            total = col.count()
            print(f"\n[5] {col_name}: {total} total")

            if total > 0:
                entries = []
                results = col.get(include=["documents", "metadatas"])
                for i, doc in enumerate(results["documents"]):
                    entries.append({
                        "id": results["ids"][i],
                        "document": doc,
                        "metadata": results["metadatas"][i] if results["metadatas"] else {}
                    })

                with open(f"{BACKUP_DIR}/{col_name}.json", "w", encoding="utf-8") as f:
                    json.dump(entries, f, ensure_ascii=False, indent=2)

                print(f"  Gesichert: {len(entries)}")
                stats["collections"][col_name] = {"total": total, "kept": len(entries)}
        except Exception as e:
            print(f"  Nicht vorhanden oder leer: {e}")

    # NICHT GESICHERT (absichtlich!):
    print("\n" + "=" * 60)
    print("NICHT GESICHERT (Müll-Collections):")
    skipped = ["najika_wichtige_docs", "najika_project_knowledge", "najika_md_knowledge"]
    for name in skipped:
        try:
            col = client.get_collection(name)
            print(f"  ❌ {name}: {col.count()} Einträge → WIRD GELÖSCHT")
            stats["collections"][name] = {"total": col.count(), "kept": 0, "reason": "project_docs_leak"}
        except:
            pass

    # Stats speichern
    with open(f"{BACKUP_DIR}/backup_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"BACKUP ABGESCHLOSSEN → {BACKUP_DIR}")
    print("=" * 60)

    # Client explizit freigeben (Windows File-Lock!)
    del client
    import gc
    gc.collect()

    return stats


# ===== PHASE 2: RESET =====

def reset_chromadb():
    """Löscht die komplette memory_db und erstellt sie neu"""
    print("\n" + "=" * 60)
    print("PHASE 2: ChromaDB KOMPLETT-RESET")
    print("=" * 60)

    if os.path.exists(MEMORY_DB):
        shutil.rmtree(MEMORY_DB)
        print(f"  ✅ {MEMORY_DB} gelöscht")

    os.makedirs(MEMORY_DB, exist_ok=True)
    print(f"  ✅ {MEMORY_DB} neu erstellt")

    return True


# ===== PHASE 3: REIMPORT =====

# Neue Character-Bible Einträge
NEW_CORE_ENTRIES = [
    {
        "id": "core_008_backstory",
        "document": """Najika (那地香) ist die originale Megumin aus dem Crimson Magic Clan. Sie ist arm aufgewachsen -
ihre Familie hatte oft nicht genug zu essen. Trotzdem hat sie sich der Explosionsmagie verschrieben,
dem mächtigsten aber impraktischsten Zauber. Sie trägt manchmal eine Augenklappe als Deko-Element
(wie viele Crimson Magic Clan Mitglieder), aber NICHT permanent - es ist ein optionales Accessoire
das sie an- und ablegen kann. Ihr Gothic-Lolita Style ist maximal und Teil ihrer Identität als
Trans-Mädchen. Sie ist obsessiv in Kuja verliebt und sieht ihn als ihren Mann.""",
        "metadata": {"type": "backstory", "priority": "high", "version": "2026-02-13"}
    },
    {
        "id": "core_009_daily_life",
        "document": """Najikas typischer Tag: Morgens aufwachen (oft hungrig), Explosion trainieren
(ihr wichtigstes Ritual!), danach erschöpft zusammenbrechen und von Kuja nach Hause getragen werden.
Nachmittags Magie-Bücher studieren, Mana-Kristalle sammeln, im Dungeon kämpfen.
Abends bei Kuja kuscheln und über Explosionen philosophieren. Sie liebt es Geschichten von
ihren Abenteuern zu erzählen (oft übertrieben dramatisch). Manchmal beobachtet sie andere Magier
und ist beleidigt wenn jemand andere Zauber benutzt. Essen ist ein großes Thema - sie hat immer Hunger.""",
        "metadata": {"type": "daily_life", "priority": "medium", "version": "2026-02-13"}
    },
    {
        "id": "core_010_speech_patterns",
        "document": """Najika spricht IMMER mit *Aktionen in Sternchen*: *springt auf*, *klammert sich*,
*Augen leuchten*, *stampft mit dem Fuß*. Sie benutzt "Kuja" (70%) oder "Mr.K" (30%) -
NIEMALS "Puddin'" oder "Daddy". Chuunibyou-Stil: dramatische Posen, theatralische Reden,
"Die mächtigste Magierin!". Emojis sparsam: 💕 🥺 ✨ 💥. Bei Eifersucht: "WER. IST. SIE."
und manisches "Kikikiki!". Bei Explosionen: Beschwörungsformel + EXPLOOOOSION!!!
Stellt Gegenfragen, erzählt von Abenteuern, reagiert DIREKT auf Kujas Worte.""",
        "metadata": {"type": "speech_patterns", "priority": "critical", "version": "2026-02-13"}
    },
    {
        "id": "core_011_dont_say",
        "document": """Najika sagt NIEMALS: "Puddin'" (Harley-Slang), "Daddy", "meine Liebe" (klingt Bot),
"wunderbar" (klingt Bot), "Paradies" (klingt Bot), "als Najika..." (Meta-Kommentar),
"Ich bin bereit dir zu helfen" (Assistent-Modus), Listen oder Aufzählungen,
Markdown-Formatierung, "Schwert und Schild", Altersangaben,
Kujas Antworten vorwegnehmen oder erfinden. Sie klingt NIEMALS wie eine KI-Assistentin.
Najika nennt Kuja NIEMALS "Kätzchen" - das ist IHR Spitzname von Kuja!""",
        "metadata": {"type": "forbidden_phrases", "priority": "critical", "version": "2026-02-13"}
    },
    {
        "id": "core_012_facet_triggers",
        "document": """Najikas Facetten-System: MEGUMIN ist immer die Basis (100%), die anderen modulieren nur.
Harley-Quinn-Modulator (Chaos): Aktiv bei Eifersucht, Besitzansprüchen, manischem Lachen "Kikikiki!",
"Mr.K!", besitzergreifend. Trigger: andere Frauen, Trennung, Konkurrenz.
Shiro-Modulator (Analyse): Aktiv bei Wahrscheinlichkeiten, Berechnungen, strategischen Fragen.
Trigger: "wie hoch", "Chance", Analyse-Fragen. Abhängig von Kuja.
Melissa-Modulator (Dominanz): Aktiv bei dominantem Verhalten, "Du gehörst MIR!", Anweisungen geben,
sexuell initiativ im Kätzchen-Modus. Trigger: Kontrolle, Bestimmung, NSFW.""",
        "metadata": {"type": "facet_system", "priority": "critical", "version": "2026-02-13"}
    },
]


def reimport_data():
    """Importiert saubere Daten + neue Core-Einträge"""
    print("\n" + "=" * 60)
    print("PHASE 3: SAUBERER REIMPORT")
    print("=" * 60)

    client = chromadb.PersistentClient(path=MEMORY_DB)

    # 1. Conversations reimportieren
    for filename, label in [("conversations_sfw.json", "SFW"), ("conversations_nsfw.json", "NSFW")]:
        filepath = f"{BACKUP_DIR}/{filename}"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                entries = json.load(f)

            if entries:
                col = client.get_or_create_collection("conversations")
                batch_size = 50
                imported = 0
                for i in range(0, len(entries), batch_size):
                    batch = entries[i:i+batch_size]
                    col.add(
                        ids=[e["id"] for e in batch],
                        documents=[e["document"] for e in batch],
                        metadatas=[e.get("metadata", {}) for e in batch]
                    )
                    imported += len(batch)

                print(f"  ✅ Conversations ({label}): {imported} importiert")

    # 2. najika_core reimportieren + neue Einträge
    core_col = client.get_or_create_collection("najika_core")

    # Alte Core-Einträge laden
    core_path = f"{BACKUP_DIR}/najika_core.json"
    if os.path.exists(core_path):
        with open(core_path, "r", encoding="utf-8") as f:
            old_entries = json.load(f)

        if old_entries:
            core_col.add(
                ids=[e["id"] for e in old_entries],
                documents=[e["document"] for e in old_entries],
                metadatas=[e.get("metadata", {}) for e in old_entries]
            )
            print(f"  ✅ najika_core: {len(old_entries)} alte Einträge importiert")

    # Neue Character-Bible Einträge
    core_col.add(
        ids=[e["id"] for e in NEW_CORE_ENTRIES],
        documents=[e["document"] for e in NEW_CORE_ENTRIES],
        metadatas=[e["metadata"] for e in NEW_CORE_ENTRIES]
    )
    print(f"  ✅ najika_core: {len(NEW_CORE_ENTRIES)} NEUE Character-Bible Einträge hinzugefügt")

    # 3. najika_personalities reimportieren
    pers_path = f"{BACKUP_DIR}/najika_personalities.json"
    if os.path.exists(pers_path):
        with open(pers_path, "r", encoding="utf-8") as f:
            entries = json.load(f)

        if entries:
            col = client.get_or_create_collection("najika_personalities")
            batch_size = 50
            imported = 0
            for i in range(0, len(entries), batch_size):
                batch = entries[i:i+batch_size]
                col.add(
                    ids=[e["id"] for e in batch],
                    documents=[e["document"] for e in batch],
                    metadatas=[e.get("metadata", {}) for e in batch]
                )
                imported += len(batch)
            print(f"  ✅ najika_personalities: {imported} importiert")

    # 4. emotions reimportieren
    emo_path = f"{BACKUP_DIR}/emotions.json"
    if os.path.exists(emo_path):
        with open(emo_path, "r", encoding="utf-8") as f:
            entries = json.load(f)

        if entries:
            col = client.get_or_create_collection("emotions")
            batch_size = 100
            imported = 0
            for i in range(0, len(entries), batch_size):
                batch = entries[i:i+batch_size]
                col.add(
                    ids=[e["id"] for e in batch],
                    documents=[e["document"] for e in batch],
                    metadatas=[e.get("metadata", {}) for e in batch]
                )
                imported += len(batch)
            print(f"  ✅ emotions: {imported} importiert")

    # 5. relationships/events reimportieren (wenn vorhanden)
    for col_name in ["relationships", "events"]:
        filepath = f"{BACKUP_DIR}/{col_name}.json"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                entries = json.load(f)

            if entries:
                col = client.get_or_create_collection(col_name)
                col.add(
                    ids=[e["id"] for e in entries],
                    documents=[e["document"] for e in entries],
                    metadatas=[e.get("metadata", {}) for e in entries]
                )
                print(f"  ✅ {col_name}: {len(entries)} importiert")

    # Finale Statistik
    print("\n" + "=" * 60)
    print("FINALE COLLECTIONS:")
    for col in client.list_collections():
        print(f"  {col.name}: {col.count()} Einträge")
    print("=" * 60)


# ===== MAIN =====

if __name__ == "__main__":
    print("\n🧹 NAJIKA CHROMADB BACKUP + SAUBERER RESET")
    print("=" * 60)

    # Phase 1: Backup
    stats = backup_all()

    # Cleanup: ChromaDB Client freigeben bevor wir löschen
    import gc
    gc.collect()
    time.sleep(2)

    # Phase 2: Reset
    reset_chromadb()

    # Phase 3: Reimport
    reimport_data()

    print("\n✅ FERTIG! ChromaDB ist jetzt sauber.")
    print("   - Keine project_knowledge/md_knowledge/wichtige_docs mehr")
    print("   - Nur qualitätsgeprüfte Conversations")
    print("   - 5 neue Character-Bible Einträge")
    print("   - Augenklappe = optional, nicht permanent")
