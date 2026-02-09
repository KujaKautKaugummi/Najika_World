#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick ChromaDB checker"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import chromadb
import os

dbs = [
    ('C:/Najika_World/chroma_db', 'NajikaCore'),
    ('C:/Najika_World/memory_db', 'NajikaFinal'),
]

for path, name in dbs:
    if os.path.exists(path):
        try:
            client = chromadb.PersistentClient(path=path)
            collections = client.list_collections()
            print(f'\n=== {name} ({path}) ===')
            print(f'Collections: {len(collections)}')
            for col in collections:
                count = col.count()
                print(f'  - {col.name}: {count} entries')
        except Exception as e:
            print(f'{name}: ERROR - {e}')
    else:
        print(f'{name}: Path not found')
