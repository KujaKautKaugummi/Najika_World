#!/usr/bin/env python3
"""
NAJIKA GRUNDSTEIN BUILDER
=========================
Fusioniert MASTER-KERN mit 5 PDFs

ABLAUF:
1. Liest 5 Basis-PDFs komplett
2. Extrahiert KI/Najika-Beschreibungen → OPTIONAL
3. Fügt MASTER-KERN ein → FEST
4. Alles andere bleibt → BASIS

OUTPUT: NAJIKA_GRUNDSTEIN.json + .md
"""

import json
import os
from pathlib import Path
from datetime import datetime

# PDF Support
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    print("[ERROR] PyPDF2 nicht installiert!")
    print("Installiere mit: pip install PyPDF2")
    PDF_AVAILABLE = False
    exit(1)

# ===== CONFIG =====

PDF_DIR = Path("C:/Users/0KKK0/Desktop/neu neu")
MASTER_KERN = Path("C:/NajikaCore/NAJIKA_MASTER_KERN_KOMPLETT.md")
OUTPUT_DIR = Path("C:/NajikaCore/grundstein_output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Die 5 Basis-PDFs
BASIS_PDFS = [
    "Projekt Najika – Allumfassende Übersicht.pdf",
    "Najika Projekt – Umfassende Detailübersicht.pdf",
    "Umfassende detaillierte Projektübersicht.pdf",
    "Umfassende Projektübersicht und Replizierungsanleitung.pdf",
    "Projektübersicht __Najika__ – Technik & Konzept.pdf"
]

# ===== FUNCTIONS =====

def read_pdf(pdf_path):
    """Liest PDF komplett"""
    print(f"\n[PDF] {pdf_path.name}")
    text = ""

    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)

            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text += page_text + "\n\n"

                if i % 10 == 0:
                    print(f"  -> Seite {i}/{total_pages}")

            print(f"  ✓ {len(text)} Zeichen gelesen")
            return text

    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def extract_najika_descriptions(text, source_name):
    """
    Extrahiert Najika/KI-Beschreibungen aus Text
    Einfacher Keyword-basierter Filter
    """
    import re

    najika_parts = []

    # Teile Text in Absätze
    paragraphs = text.split('\n\n')

    # Keywords die auf Najika-Beschreibungen hindeuten
    najika_keywords = [
        'najika', 'persönlichkeit', 'ki', 'charakterzug',
        'megumin', 'harley', 'shiro', 'melissa', 'sakura',
        'gothic lolita', 'trans', 'anatomie', 'kätzchen',
        '11 jahre', 'explosion', 'beziehung zu kuja'
    ]

    for para in paragraphs:
        para_lower = para.lower()

        # Checke ob Keywords vorkommen
        if any(keyword in para_lower for keyword in najika_keywords):
            if len(para.strip()) > 50:  # Mindestlänge
                najika_parts.append({
                    'text': para.strip(),
                    'source': source_name
                })

    print(f"  ✓ {len(najika_parts)} Najika-Beschreibungen gefunden")
    return najika_parts

def build_grundstein():
    """Hauptfunktion"""

    print("="*80)
    print("NAJIKA GRUNDSTEIN BUILDER")
    print("="*80)

    # 1. MASTER-KERN laden
    print("\n[1/3] MASTER-KERN LADEN")
    print("-"*80)

    if not MASTER_KERN.exists():
        print(f"[ERROR] MASTER-KERN nicht gefunden: {MASTER_KERN}")
        return

    master_kern_text = MASTER_KERN.read_text(encoding='utf-8')
    print(f"✓ MASTER-KERN geladen ({len(master_kern_text)} Zeichen)")

    # 2. PDFs lesen
    print("\n[2/3] 5 BASIS-PDFs LESEN")
    print("-"*80)

    pdf_contents = {}
    all_najika_parts = []

    for pdf_name in BASIS_PDFS:
        pdf_path = PDF_DIR / pdf_name

        if not pdf_path.exists():
            print(f"\n[SKIP] {pdf_name} - nicht gefunden!")
            continue

        # Lese PDF
        text = read_pdf(pdf_path)
        if not text:
            continue

        # Speichere Volltext
        pdf_contents[pdf_name] = text

        # Extrahiere Najika-Teile
        najika_parts = extract_najika_descriptions(text, pdf_name)
        all_najika_parts.extend(najika_parts)

    print(f"\n✓ Gesamt {len(all_najika_parts)} Najika-Beschreibungen aus allen PDFs")

    # 3. GRUNDSTEIN bauen
    print("\n[3/3] GRUNDSTEIN BAUEN")
    print("-"*80)

    grundstein = {
        'created': datetime.now().isoformat(),
        'description': 'Najika Grundstein - MASTER-KERN (FEST) + 5 PDFs (BASIS) + PDF-Najika (OPTIONAL)',
        'master_kern': {
            'status': 'FEST',
            'source': str(MASTER_KERN),
            'content': master_kern_text
        },
        'pdf_basis': {},
        'najika_optional': []
    }

    # PDFs als BASIS
    for pdf_name, content in pdf_contents.items():
        # Entferne Najika-Beschreibungen aus Content
        clean_content = content
        for najika_part in all_najika_parts:
            if najika_part['source'] == pdf_name:
                clean_content = clean_content.replace(najika_part['text'], '')

        grundstein['pdf_basis'][pdf_name] = {
            'status': 'BASIS',
            'content': clean_content,
            'original_size': len(content),
            'cleaned_size': len(clean_content)
        }

    # Najika-Teile als OPTIONAL
    for najika_part in all_najika_parts:
        grundstein['najika_optional'].append({
            'status': 'OPTIONAL',
            'source': najika_part['source'],
            'content': najika_part['text']
        })

    print(f"✓ MASTER-KERN: FEST")
    print(f"✓ {len(pdf_contents)} PDFs: BASIS")
    print(f"✓ {len(all_najika_parts)} Najika-Teile: OPTIONAL")

    # 4. SPEICHERN
    print("\n[4/4] SPEICHERN")
    print("-"*80)

    # JSON
    json_output = OUTPUT_DIR / "NAJIKA_GRUNDSTEIN.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(grundstein, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON: {json_output}")

    # Markdown (lesbar)
    md_output = OUTPUT_DIR / "NAJIKA_GRUNDSTEIN.md"
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("# NAJIKA GRUNDSTEIN\n\n")
        f.write(f"**Erstellt:** {grundstein['created']}\n\n")
        f.write("---\n\n")

        # MASTER-KERN (FEST)
        f.write("# MASTER-KERN (FEST)\n\n")
        f.write(grundstein['master_kern']['content'])
        f.write("\n\n---\n\n")

        # PDF-BASIS
        f.write("# PDF BASIS\n\n")
        for pdf_name, pdf_data in grundstein['pdf_basis'].items():
            f.write(f"## {pdf_name}\n\n")
            f.write(f"**Status:** {pdf_data['status']}\n\n")
            f.write(pdf_data['content'][:5000] + "\n\n[... gekürzt ...]\n\n")
            f.write("---\n\n")

        # NAJIKA OPTIONAL
        f.write("# NAJIKA BESCHREIBUNGEN (OPTIONAL)\n\n")
        for i, najika in enumerate(grundstein['najika_optional'], 1):
            f.write(f"## Najika-Teil {i} (aus {najika['source']})\n\n")
            f.write(f"**Status:** {najika['status']}\n\n")
            f.write(najika['content'])
            f.write("\n\n---\n\n")

    print(f"✓ MD: {md_output}")

    # STATS
    print("\n" + "="*80)
    print("FERTIG!")
    print("="*80)
    print(f"MASTER-KERN: FEST (1 Teil)")
    print(f"PDF BASIS: {len(grundstein['pdf_basis'])} PDFs")
    print(f"NAJIKA OPTIONAL: {len(grundstein['najika_optional'])} Teile")
    print()

if __name__ == "__main__":
    build_grundstein()
