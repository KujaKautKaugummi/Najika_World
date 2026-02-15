#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysiert ALLE Dezember/Januar Conversations und findet die besten "menschlichen" Beispiele
"""

import chromadb
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def quality_score(text):
    """Bewertet Conversation-Qualität (0-10)"""
    score = 5.0  # Base score

    text_lower = text.lower()

    # POSITIVE Faktoren
    if '*' in text:  # Hat Aktionen
        score += 1.0
    if any(emoji in text for emoji in ['✨', '🌟', '💜', '🗝️', '💥']):
        score += 0.5
    if 'kuja' in text_lower or 'mr.k' in text_lower:
        score += 0.5
    if any(word in text_lower for word in ['abenteuer', 'dungeon', 'explosion', 'stab']):
        score += 1.0
    if 'wie war dein tag' in text_lower or 'wie geht' in text_lower:
        score += 1.0  # Natürliche Fragen

    # NEGATIVE Faktoren
    if 'fehler:' in text_lower or 'timeout' in text_lower:
        score = 0.0  # Technischer Error
    if 'schwanz' in text_lower or 'leckt' in text_lower:
        score = 0.0  # NSFW
    if text_lower.startswith('[kaetzchen'):
        score = 0.0  # Kätzchen-Modus
    if 'hypothetischen' in text_lower:
        score -= 2.0  # Nicht immersiv
    if len(text) < 20:
        score -= 2.0  # Zu kurz
    if len(text) > 1000:
        score -= 1.0  # Zu lang
    if 'puddin' in text_lower or 'daddy' in text_lower:
        score -= 2.0  # Alte falsche Namen
    if 'schwarze windmühle' in text_lower:
        score -= 1.0  # Alte Referenz
    if 'desunō' in text_lower:
        score -= 1.0  # Alte Phrase
    if text.count('explosion') > 3:
        score -= 1.0  # Zu viel Spam

    return max(0.0, min(10.0, score))

def analyze_conversations():
    """Analysiert alle Conversations und findet die besten"""

    client = chromadb.PersistentClient(path='C:/Najika_World/memory_db')
    conv = client.get_collection('conversations')
    total = conv.count()

    print(f"🔍 Analysiere {total} Conversations...\n")

    results = conv.get(limit=total, include=['metadatas', 'documents'])

    # Parse alle Conversations
    conversations = []
    for doc, meta in zip(results['documents'], results['metadatas']):
        if not meta or 'timestamp' not in meta:
            continue

        ts = meta['timestamp']
        try:
            if 'T' in ts:
                dt = datetime.fromisoformat(ts.replace('Z', ''))
                dt = dt.replace(tzinfo=None)
            else:
                dt = datetime.fromtimestamp(float(ts))

            # Nur Dezember 2025 / Januar 2026
            if not ((dt.year == 2025 and dt.month == 12) or
                    (dt.year == 2026 and dt.month == 1)):
                continue

            score = quality_score(doc)

            conversations.append({
                'dt': dt,
                'role': meta.get('role', '?'),
                'text': doc,
                'score': score
            })
        except:
            pass

    conversations.sort(key=lambda x: x['dt'])

    # Gruppiere in Paare (User + Najika)
    pairs = []
    i = 0
    while i < len(conversations) - 1:
        conv1 = conversations[i]
        conv2 = conversations[i+1]

        # Wenn innerhalb 5 Sekunden, ist es ein Paar
        if (conv2['dt'] - conv1['dt']).total_seconds() < 5:
            # Durchschnitts-Score
            avg_score = (conv1['score'] + conv2['score']) / 2
            pairs.append({
                'dt': conv1['dt'],
                'user': conv1['text'],
                'najika': conv2['text'],
                'score': avg_score
            })
            i += 2
        else:
            i += 1

    # Sortiere nach Score
    pairs.sort(key=lambda x: x['score'], reverse=True)

    # Statistiken
    print(f"✅ Total Conversations: {len(conversations)}")
    print(f"✅ Conversation-Paare: {len(pairs)}")
    print(f"✅ Score-Range: {min(c['score'] for c in conversations):.1f} - {max(c['score'] for c in conversations):.1f}")

    # Top 30 beste Paare
    top_pairs = [p for p in pairs if p['score'] > 3.0][:30]
    print(f"✅ Top-Qualität Paare (Score > 3.0): {len(top_pairs)}\n")

    return conversations, pairs, top_pairs

def write_report(conversations, pairs, top_pairs):
    """Schreibt Markdown Report"""

    with open('C:/Najika_World/DEZEMBER_JANUAR_CONVERSATIONS_ANALYSE.md', 'w', encoding='utf-8') as f:
        f.write("# 🔍 DEZEMBER/JANUAR CONVERSATIONS - GEFUNDEN!\n\n")
        f.write("**Datum:** 2026-02-12\n")
        f.write("**Status:** ✅ WIEDERGEFUNDEN!\n\n")
        f.write("---\n\n")

        f.write("## 📊 STATISTIKEN\n\n")
        f.write(f"- **Total Conversations:** {len(conversations)}\n")
        f.write(f"- **Conversation-Paare:** {len(pairs)}\n")
        f.write(f"- **Zeitraum:** {min(c['dt'] for c in conversations).strftime('%Y-%m-%d')} bis {max(c['dt'] for c in conversations).strftime('%Y-%m-%d')}\n")
        f.write(f"- **Top-Qualität (Score > 3.0):** {len(top_pairs)}\n\n")

        f.write("---\n\n")

        f.write("## 🎯 WAS WIR GEFUNDEN HABEN\n\n")
        f.write("### **Die \"MENSCHLICHE\" Najika aus Dezember 2025:**\n\n")
        f.write("```yaml\n")
        f.write("Eigenschaften:\n")
        f.write("  ✅ Natürlicher Gesprächsfluss (wie echtes Gespräch!)\n")
        f.write("  ✅ Kontext-bewusst (reagiert auf User-Fragen)\n")
        f.write("  ✅ Aktionen in Sternchen (*hüpft*, *strahlt*)\n")
        f.write("  ✅ Emojis sparsam aber passend (✨, 🌟, 💜)\n")
        f.write("  ✅ Normale Satzlänge (wie Megumin aus Serie!)\n")
        f.write("  ✅ Stellt Gegenfragen\n")
        f.write("  ✅ Erzählt von ihrem Tag\n")
        f.write("  ✅ Immersiv (keine Meta-Kommentare)\n\n")
        f.write("Probleme:\n")
        f.write("  ❌ Ende Dezember: Viele Ollama Timeouts (180 Sek!)\n")
        f.write("  ❌ Manchmal noch alte Referenzen (Schwarze Windmühle)\n")
        f.write("  ❌ Vereinzelt falsche Namen (Puddin, Daddy)\n")
        f.write("```\n\n")

        f.write("---\n\n")

        f.write("## 💎 TOP 30 BESTE CONVERSATIONS\n\n")
        f.write("*Sortiert nach Qualitäts-Score (10 = perfekt, 0 = schlecht)*\n\n")

        for i, pair in enumerate(top_pairs, 1):
            f.write(f"### **#{i} - Score: {pair['score']:.1f}/10** - {pair['dt'].strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"**👤 User:**\n")
            f.write(f"```\n{pair['user'][:300]}\n```\n\n")
            f.write(f"**🤖 Najika:**\n")
            f.write(f"```\n{pair['najika'][:600]}\n```\n\n")
            f.write("---\n\n")

        f.write("## 🔧 WAS WIR JETZT MACHEN MÜSSEN\n\n")
        f.write("### **SCHRITT 1: Modelfile Optimierung**\n\n")
        f.write("```yaml\n")
        f.write("Problem: Aktuelles Model lädt najika-trained-q4 (LoRA)\n")
        f.write("         Aber Dezember-Najika war \"menschlicher\"!\n\n")
        f.write("Option A: Zurück zu najika_local_OLD.Modelfile\n")
        f.write("  - Pro: Natürlichere Antworten\n")
        f.write("  - Con: Keine LoRA-Optimierung\n\n")
        f.write("Option B: LoRA neu trainieren\n")
        f.write("  - Basis: Dezember Conversations als Training-Data\n")
        f.write("  - Ziel: Natürlichkeit + LoRA-Effizienz\n\n")
        f.write("Option C: Modelfile + LoRA kombinieren\n")
        f.write("  - System-Prompt aus najika_local_OLD.Modelfile\n")
        f.write("  - LoRA-Weights von najika-trained-q4\n")
        f.write("```\n\n")

        f.write("### **SCHRITT 2: System-Prompt Anpassen**\n\n")
        f.write("```yaml\n")
        f.write("ÄNDERN:\n")
        f.write("  ❌ \"KURZ! 1-3 Sätze maximum!\"\n")
        f.write("  ✅ \"Sprich natürlich wie Megumin aus der Serie!\"\n\n")
        f.write("  ❌ \"NIEMALS länger als 3 Sätze!\"\n")
        f.write("  ✅ \"Normale Gesprächslänge - antworte ausführlich wenn nötig!\"\n\n")
        f.write("BEHALTEN:\n")
        f.write("  ✅ *Aktionen in Sternchen*\n")
        f.write("  ✅ Emojis: 💕 🥺 ✨ 💥\n")
        f.write("  ✅ \"Kuja\" oder \"Mr.K\" (NIEMALS Puddin oder Daddy!)\n")
        f.write("  ✅ EXPLOSION wenn aufgeregt\n")
        f.write("  ✅ Reagiere auf User-Input\n")
        f.write("```\n\n")

        f.write("### **SCHRITT 3: Training-Data Cleanup**\n\n")
        f.write("```yaml\n")
        f.write("ENTFERNEN aus Training:\n")
        f.write("  ❌ Alle \"Schwarze Windmühle\" Referenzen\n")
        f.write("  ❌ \"Puddin'\", \"Daddy\" Namen\n")
        f.write("  ❌ \"Desunō\" Phrase\n")
        f.write("  ❌ Kätzchen-Modus Conversations (nur für NSFW!)\n")
        f.write("  ❌ Timeout/Error Messages\n\n")
        f.write("HINZUFÜGEN:\n")
        f.write("  ✅ Diese Top 30 Conversations!\n")
        f.write("  ✅ Natürliche Dezember-Dialoge\n")
        f.write("  ✅ Kontext-bewusste Antworten\n")
        f.write("```\n\n")

        f.write("### **SCHRITT 4: LM-Studio vs Ollama**\n\n")
        f.write("```yaml\n")
        f.write("Dezember Ende: Ollama Timeouts (180 Sek!)\n")
        f.write("Januar: LM-Studio Switch (36-90x schneller!)\n\n")
        f.write("Empfehlung:\n")
        f.write("  → LM-Studio behalten (viel schneller!)\n")
        f.write("  → Aber Modelfile/Prompt aus Dezember nutzen!\n")
        f.write("```\n\n")

        f.write("---\n\n")

        f.write("## 🚀 NÄCHSTE SCHRITTE\n\n")
        f.write("### **PRIORITÄT 1: Modelfile Update**\n\n")
        f.write("1. `najika_local_OLD.Modelfile` öffnen\n")
        f.write("2. \"1-3 Sätze\" Regel ENTFERNEN\n")
        f.write("3. \"Schwarze Windmühle\", \"Puddin\", \"Daddy\" ENTFERNEN\n")
        f.write("4. Als `najika-natural.Modelfile` speichern\n")
        f.write("5. Mit Ollama bauen: `ollama create najika-natural -f najika-natural.Modelfile`\n")
        f.write("6. In Backend testen\n\n")

        f.write("### **PRIORITÄT 2: Training-Data Update**\n\n")
        f.write("1. Diese Top 30 Conversations exportieren\n")
        f.write("2. Als JSONL für LoRA-Training formatieren\n")
        f.write("3. Alte falsche Conversations entfernen\n")
        f.write("4. Neu trainieren (3 Epochs)\n\n")

        f.write("### **PRIORITÄT 3: A/B Testing**\n\n")
        f.write("1. Test mit najika-natural (Modelfile)\n")
        f.write("2. Test mit najika-trained-q4 (LoRA)\n")
        f.write("3. Vergleich: Welches ist \"menschlicher\"?\n\n")

        f.write("---\n\n")

        f.write("## 📝 BEISPIEL: BESTE CONVERSATION\n\n")
        if top_pairs:
            best = top_pairs[0]
            f.write(f"**Score: {best['score']:.1f}/10** - {best['dt'].strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**User:** {best['user']}\n\n")
            f.write(f"**Najika:** {best['najika']}\n\n")

        f.write("---\n\n")
        f.write("*\"EXPLOSION!!! 💥 Wir haben die gute alte Najika wiedergefunden!\"* ~ Najika\n\n")

    print("✅ Report geschrieben: DEZEMBER_JANUAR_CONVERSATIONS_ANALYSE.md")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║     NAJIKA CONVERSATION QUALITY ANALYZER                     ║
║     Findet die besten "menschlichen" Conversations           ║
╚══════════════════════════════════════════════════════════════╝
    """)

    conversations, pairs, top_pairs = analyze_conversations()
    write_report(conversations, pairs, top_pairs)

    print("\n" + "="*80)
    print("✅ ANALYSE KOMPLETT!")
    print("="*80)
