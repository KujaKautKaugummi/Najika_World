#!/usr/bin/env python3
"""
NAJIKA FINAL GRUNDSTEIN BUILDER
================================
SCHRITT 1: MASTER-KERN in 5 PDFs integrieren
SCHRITT 2: Diese 5 PDFs = BASIS
SCHRITT 3: neu neu/ Files = OPTIONAL
SCHRITT 4: zip/ Files = OPTIONAL

OUTPUT: Komplettes Projekt-Wissen
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
MASTER_KERN = Path("C:/Najika_World/NAJIKA_MASTER_KERN_KOMPLETT.md")
NEU_NEU_DIR = Path("C:/Users/0KKK0/Desktop/neu neu")
ZIP_DIR = Path("C:/Users/0KKK0/Desktop/zip")
OUTPUT_DIR = Path("C:/Najika_World/grundstein_output")
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

def read_text_file(file_path):
    """Liest Text-Datei"""
    try:
        return file_path.read_text(encoding='utf-8')
    except:
        try:
            return file_path.read_text(encoding='latin-1')
        except Exception as e:
            print(f"  [ERROR] {file_path.name}: {e}")
            return None

def collect_all_files(directory, description):
    """Sammelt alle Dateien aus einem Verzeichnis"""
    print(f"\n[SAMMLE] {description}")
    print("-"*80)

    files_data = []

    if not directory.exists():
        print(f"[SKIP] Verzeichnis nicht gefunden: {directory}")
        return files_data

    for file_path in directory.iterdir():
        if file_path.is_file():
            print(f"\n[FILE] {file_path.name}")

            content = None
            file_type = file_path.suffix.lower()

            if file_type == '.pdf':
                content = read_pdf(file_path)
            elif file_type in ['.txt', '.md']:
                content = read_text_file(file_path)
            else:
                print(f"  [SKIP] Unsupported type: {file_type}")
                continue

            if content:
                files_data.append({
                    'filename': file_path.name,
                    'type': file_type,
                    'content': content,
                    'size': len(content)
                })
                print(f"  ✓ {len(content)} Zeichen")

    print(f"\n✓ Gesamt {len(files_data)} Files aus {description}")
    return files_data

def build_final_grundstein():
    """Hauptfunktion"""

    print("="*80)
    print("NAJIKA FINAL GRUNDSTEIN BUILDER")
    print("="*80)

    # 1. MASTER-KERN laden
    print("\n[1/4] MASTER-KERN LADEN")
    print("-"*80)

    if not MASTER_KERN.exists():
        print(f"[ERROR] MASTER-KERN nicht gefunden: {MASTER_KERN}")
        return

    master_kern_text = MASTER_KERN.read_text(encoding='utf-8')
    print(f"✓ MASTER-KERN geladen ({len(master_kern_text)} Zeichen)")

    # 2. 5 BASIS-PDFs lesen + MASTER-KERN integrieren
    print("\n[2/4] 5 BASIS-PDFs LESEN + MASTER-KERN INTEGRIEREN")
    print("-"*80)

    basis_pdfs_data = []

    for pdf_name in BASIS_PDFS:
        pdf_path = PDF_DIR / pdf_name

        if not pdf_path.exists():
            print(f"\n[SKIP] {pdf_name} - nicht gefunden!")
            continue

        # Lese PDF
        pdf_content = read_pdf(pdf_path)
        if not pdf_content:
            continue

        # INTEGRIERE MASTER-KERN am Anfang
        integrated_content = f"""
{'='*80}
NAJIKA MASTER-KERN (INTEGRIERT)
{'='*80}

{master_kern_text}

{'='*80}
PROJEKT-DOKUMENTATION: {pdf_name}
{'='*80}

{pdf_content}
"""

        basis_pdfs_data.append({
            'filename': pdf_name,
            'type': 'pdf',
            'content': integrated_content,
            'original_size': len(pdf_content),
            'integrated_size': len(integrated_content),
            'has_master_kern': True
        })

        print(f"  ✓ MASTER-KERN integriert in {pdf_name}")

    print(f"\n✓ {len(basis_pdfs_data)} BASIS-PDFs mit MASTER-KERN erstellt")

    # 3. neu neu/ Files sammeln
    optional_neu_neu = collect_all_files(NEU_NEU_DIR, "neu neu/ Files (OPTIONAL)")

    # 4. zip/ Files sammeln
    optional_zip = collect_all_files(ZIP_DIR, "zip/ Files (OPTIONAL)")

    # 5. GRUNDSTEIN bauen
    print("\n[3/4] GRUNDSTEIN BAUEN")
    print("-"*80)

    grundstein = {
        'created': datetime.now().isoformat(),
        'description': 'Najika Final Grundstein - 5 PDFs (BASIS mit MASTER-KERN) + neu neu/ (OPTIONAL) + zip/ (OPTIONAL)',
        'master_kern': {
            'source': str(MASTER_KERN),
            'content': master_kern_text,
            'integrated_in_basis': True
        },
        'basis_pdfs': basis_pdfs_data,
        'optional_neu_neu': optional_neu_neu,
        'optional_zip': optional_zip,
        'statistics': {
            'basis_count': len(basis_pdfs_data),
            'optional_neu_neu_count': len(optional_neu_neu),
            'optional_zip_count': len(optional_zip),
            'total_files': len(basis_pdfs_data) + len(optional_neu_neu) + len(optional_zip)
        }
    }

    print(f"✓ BASIS: {len(basis_pdfs_data)} PDFs (mit MASTER-KERN)")
    print(f"✓ OPTIONAL neu neu/: {len(optional_neu_neu)} Files")
    print(f"✓ OPTIONAL zip/: {len(optional_zip)} Files")
    print(f"✓ GESAMT: {grundstein['statistics']['total_files']} Files")

    # 6. SPEICHERN
    print("\n[4/4] SPEICHERN")
    print("-"*80)

    # JSON
    json_output = OUTPUT_DIR / "NAJIKA_FINAL_GRUNDSTEIN.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(grundstein, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON: {json_output}")

    # Markdown (lesbar)
    md_output = OUTPUT_DIR / "NAJIKA_FINAL_GRUNDSTEIN.md"
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write("# NAJIKA FINAL GRUNDSTEIN\n\n")
        f.write(f"**Erstellt:** {grundstein['created']}\n\n")
        f.write("---\n\n")

        # MASTER-KERN
        f.write("# MASTER-KERN\n\n")
        f.write(grundstein['master_kern']['content'])
        f.write("\n\n---\n\n")

        # BASIS PDFs (mit MASTER-KERN integriert)
        f.write("# BASIS: 5 PDFs (MIT MASTER-KERN INTEGRIERT)\n\n")
        for i, pdf_data in enumerate(grundstein['basis_pdfs'], 1):
            f.write(f"## {i}. {pdf_data['filename']}\n\n")
            f.write(f"**Original:** {pdf_data['original_size']} Zeichen\n")
            f.write(f"**Mit MASTER-KERN:** {pdf_data['integrated_size']} Zeichen\n\n")
            f.write(pdf_data['content'][:3000] + "\n\n[... gekürzt ...]\n\n")
            f.write("---\n\n")

        # OPTIONAL neu neu/
        f.write("# OPTIONAL: neu neu/ Files\n\n")
        for i, file_data in enumerate(grundstein['optional_neu_neu'], 1):
            f.write(f"## {i}. {file_data['filename']}\n\n")
            f.write(f"**Typ:** {file_data['type']}\n")
            f.write(f"**Größe:** {file_data['size']} Zeichen\n\n")
            f.write(file_data['content'][:2000] + "\n\n[... gekürzt ...]\n\n")
            f.write("---\n\n")

        # OPTIONAL zip/
        f.write("# OPTIONAL: zip/ Files\n\n")
        for i, file_data in enumerate(grundstein['optional_zip'], 1):
            f.write(f"## {i}. {file_data['filename']}\n\n")
            f.write(f"**Typ:** {file_data['type']}\n")
            f.write(f"**Größe:** {file_data['size']} Zeichen\n\n")
            f.write(file_data['content'][:2000] + "\n\n[... gekürzt ...]\n\n")
            f.write("---\n\n")

    print(f"✓ MD: {md_output}")

    # STATS
    print("\n" + "="*80)
    print("FERTIG!")
    print("="*80)
    print(f"BASIS PDFs (mit MASTER-KERN): {len(basis_pdfs_data)}")
    print(f"OPTIONAL neu neu/: {len(optional_neu_neu)}")
    print(f"OPTIONAL zip/: {len(optional_zip)}")
    print(f"GESAMT: {grundstein['statistics']['total_files']} Files")
    print()

if __name__ == "__main__":
    build_final_grundstein()
