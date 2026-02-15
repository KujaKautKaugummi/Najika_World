#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import chromadb
from datetime import datetime
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

client = chromadb.PersistentClient(path='C:/Najika_World/memory_db')
conv = client.get_collection('conversations')
results = conv.get(limit=2000, include=['metadatas', 'documents'])

# Filter SFW conversations from mid-Dec to Jan
convs = []
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

        # Mid December to January, skip NSFW
        if ((dt.year == 2025 and dt.month == 12 and dt.day >= 10) or
            (dt.year == 2026 and dt.month == 1)):
            text = doc[:500]
            # Skip NSFW and Kätzchen mode
            lower_text = text.lower()
            if ('schwanz' not in lower_text and
                'kaetzchen-modus' not in lower_text and
                'kätzchen' not in lower_text and
                'leckt' not in lower_text):
                convs.append((dt, meta.get('role', '?'), text))
    except:
        pass

convs.sort(key=lambda x: x[0])

print(f"\n✅ Gefunden: {len(convs)} normale SFW Conversations (Mitte Dez - Jan)\n")
print("="*80)

# Show conversations in pairs (user + najika)
i = 0
shown = 0
while i < len(convs) and shown < 20:
    dt, role, text = convs[i]

    # Try to find the response
    response = None
    if i+1 < len(convs):
        next_dt, next_role, next_text = convs[i+1]
        # If within 2 seconds, it's likely the response
        if (next_dt - dt).total_seconds() < 2:
            response = next_text
            i += 2
        else:
            i += 1
    else:
        i += 1

    print(f"\n{'─'*80}")
    print(f"📅 {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'─'*80}")
    print(f"👤 User: {text[:200]}")
    if response:
        print(f"\n🤖 Najika: {response[:400]}")
    print()

    shown += 1

print("="*80)
