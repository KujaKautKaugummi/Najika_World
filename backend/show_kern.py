#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zeigt KERN-Wahrheiten aus ChromaDB"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import chromadb

client = chromadb.PersistentClient(path='C:/Najika_World/memory_db')
core = client.get_collection('najika_core')
data = core.get()

print('=' * 60)
print('NAJIKA KERN - 7 UNVERAENDERLICHE WAHRHEITEN')
print('=' * 60)
print()

for i, doc in enumerate(data['documents']):
    meta = data['metadatas'][i] if data['metadatas'] else {}
    priority = meta.get('priority', 0)
    print(f'{i+1}. [Prioritaet: {priority}]')
    print(f'   {doc}')
    print()
