#!/usr/bin/env python3
"""
NAJIKA PROJECT ANALYZER
Analysiert hunderte Dokumente (TXT/PDF/MD) und speichert sie in ChromaDB für intelligente Suche

122 MILLIONEN ZEICHEN → Chunks → Embeddings → Retrieval-Augmented Generation
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib

# PDF Support
try:
    import pypdf
    PDF_AVAILABLE = True
except ImportError:
    print("⚠️  pypdf nicht installiert - PDF-Support deaktiviert")
    print("   Install: pip install pypdf")
    PDF_AVAILABLE = False

# ChromaDB für Embeddings
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    print("⚠️  chromadb nicht installiert")
    print("   Install: pip install chromadb")
    CHROMADB_AVAILABLE = False


class NajikaProjectAnalyzer:
    """Analysiert große Mengen an Projekt-Dokumentation"""

    def __init__(self, project_root: str = "C:\\Najika_World"):
        self.project_root = Path(project_root)
        self.chunk_size = 1000  # Zeichen pro Chunk
        self.chunk_overlap = 200  # Overlap für Kontext

        # ChromaDB Setup (V2 - ohne Training Data)
        if CHROMADB_AVAILABLE:
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.project_root / "backend" / "chroma_project_db_v2")
            )
            self.collection = self.chroma_client.get_or_create_collection(
                name="najika_project_docs",
                metadata={"description": "Najika World Projekt-Dokumentation (ohne Training Data)"}
            )
        else:
            self.chroma_client = None
            self.collection = None

        # Stats
        self.stats = {
            "files_scanned": 0,
            "files_indexed": 0,
            "total_chars": 0,
            "total_chunks": 0,
            "errors": []
        }

    def find_documents(self, search_paths: List[str] = None, scan_all: bool = True) -> List[Path]:
        """
        Findet alle relevanten Dokumente im Projekt

        Args:
            search_paths: Optionale Liste von Pfaden (relativ zu project_root)
            scan_all: Wenn True, scannt GESAMTEN Najika_World Ordner rekursiv
        """
        found_files = []
        extensions = {".txt", ".md", ".pdf", ".py", ".json"}  # ERWEITERT: Python + JSON!

        # SCAN ALL MODE: Gesamten Ordner durchsuchen!
        if scan_all:
            print(f"🔍 VOLLSTÄNDIGER SCAN: {self.project_root}")
            print("   Durchsuche ALLE Unterordner & Files...")

            exclude_dirs = {
                "node_modules", "__pycache__", ".git", ".venv", "venv",
                "chroma_db", "chroma_project_db", ".dart_tool", "build"
                # Training Data wird MIT gescannt!
            }

            for file in self.project_root.rglob("*"):
                # Skip excluded directories
                if any(excluded in file.parts for excluded in exclude_dirs):
                    continue

                if file.is_file() and file.suffix in extensions:
                    found_files.append(file)

            found_files = list(set(found_files))
            print(f"✅ {len(found_files)} Dokumente gefunden (VOLLSTÄNDIGER SCAN)")
            return found_files

        # SELECTIVE MODE: Nur bestimmte Pfade
        if search_paths is None:
            search_paths = [
                "alles wissen",
                "info material",
                "documentation",
                "docs",
                "*.md",
                "*.txt"
            ]

        print(f"🔍 Suche Dokumente in: {self.project_root}")

        for search_path in search_paths:
            search_full = self.project_root / search_path if not search_path.startswith("*") else self.project_root

            if search_path.startswith("*"):
                # Glob pattern (z.B. *.md)
                for file in self.project_root.rglob(search_path):
                    if file.is_file() and file.suffix in extensions:
                        found_files.append(file)
            elif search_full.is_dir():
                # Durchsuche Verzeichnis rekursiv
                for file in search_full.rglob("*"):
                    if file.is_file() and file.suffix in extensions:
                        found_files.append(file)
            elif search_full.is_file():
                found_files.append(search_full)

        # Deduplizieren
        found_files = list(set(found_files))
        print(f"✅ {len(found_files)} Dokumente gefunden")

        return found_files

    def read_file(self, file_path: Path) -> Tuple[str, bool]:
        """
        Liest Datei-Inhalt (TXT/MD/PDF)

        Returns:
            (content, success)
        """
        try:
            if file_path.suffix == ".pdf":
                if not PDF_AVAILABLE:
                    return "", False

                content = ""
                with open(file_path, "rb") as f:
                    pdf_reader = pypdf.PdfReader(f)
                    for page in pdf_reader.pages:
                        content += page.extract_text() + "\n"
                return content, True

            else:  # TXT, MD
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                return content, True

        except Exception as e:
            self.stats["errors"].append(f"{file_path.name}: {e}")
            return "", False

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Teilt Text in Chunks mit Overlap

        Returns:
            List of {"text": str, "metadata": dict}
        """
        chunks = []
        text_len = len(text)

        if text_len == 0:
            return chunks

        for i in range(0, text_len, self.chunk_size - self.chunk_overlap):
            chunk_text = text[i:i + self.chunk_size]

            chunk_data = {
                "text": chunk_text,
                "metadata": {
                    **(metadata or {}),
                    "chunk_index": len(chunks),
                    "char_start": i,
                    "char_end": min(i + self.chunk_size, text_len)
                }
            }
            chunks.append(chunk_data)

        return chunks

    def generate_doc_id(self, file_path: Path, chunk_index: int) -> str:
        """Generiert eindeutige ID für Chunk"""
        rel_path = file_path.relative_to(self.project_root)
        hash_input = f"{rel_path}:{chunk_index}"
        return hashlib.md5(hash_input.encode()).hexdigest()

    def index_document(self, file_path: Path) -> int:
        """
        Indiziert ein einzelnes Dokument in ChromaDB

        Returns:
            Anzahl der erstellten Chunks
        """
        if not CHROMADB_AVAILABLE:
            print("❌ ChromaDB nicht verfügbar!")
            return 0

        # Lese Datei
        content, success = self.read_file(file_path)
        if not success:
            return 0

        self.stats["total_chars"] += len(content)

        # Erstelle Chunks
        rel_path = file_path.relative_to(self.project_root)
        metadata = {
            "file_path": str(rel_path),
            "file_name": file_path.name,
            "file_type": file_path.suffix,
            "file_size": len(content)
        }

        chunks = self.chunk_text(content, metadata)

        if len(chunks) == 0:
            return 0

        # Füge zu ChromaDB hinzu
        try:
            ids = [self.generate_doc_id(file_path, i) for i in range(len(chunks))]
            texts = [chunk["text"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]

            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )

            self.stats["total_chunks"] += len(chunks)
            return len(chunks)

        except Exception as e:
            self.stats["errors"].append(f"{file_path.name} indexing: {e}")
            return 0

    def index_all_documents(self, search_paths: List[str] = None) -> Dict:
        """
        Indiziert alle Dokumente im Projekt

        Returns:
            Stats dictionary
        """
        print("\n" + "="*60)
        print("🧠 NAJIKA PROJECT ANALYZER - DOCUMENT INDEXING")
        print("="*60 + "\n")

        # Finde alle Dokumente
        files = self.find_documents(search_paths)
        self.stats["files_scanned"] = len(files)

        if len(files) == 0:
            print("❌ Keine Dokumente gefunden!")
            return self.stats

        print(f"\n📚 Indiziere {len(files)} Dokumente...\n")

        # Indiziere jedes Dokument
        for i, file_path in enumerate(files, 1):
            rel_path = file_path.relative_to(self.project_root)
            print(f"[{i}/{len(files)}] {rel_path}...", end=" ")

            chunks = self.index_document(file_path)

            if chunks > 0:
                print(f"✅ {chunks} chunks")
                self.stats["files_indexed"] += 1
            else:
                print("❌ Fehler")

        # Finale Stats
        print("\n" + "="*60)
        print("📊 INDEXING ABGESCHLOSSEN")
        print("="*60)
        print(f"✅ Dateien gefunden:   {self.stats['files_scanned']}")
        print(f"✅ Dateien indiziert:  {self.stats['files_indexed']}")
        print(f"✅ Gesamt-Zeichen:     {self.stats['total_chars']:,}")
        print(f"✅ Gesamt-Chunks:      {self.stats['total_chunks']:,}")

        if self.stats['errors']:
            print(f"\n⚠️  Fehler ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:  # Zeige erste 5
                print(f"   - {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... und {len(self.stats['errors']) - 5} weitere")

        print("="*60 + "\n")

        return self.stats

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Sucht relevante Dokument-Chunks für eine Query

        Returns:
            List of {"text": str, "metadata": dict, "distance": float}
        """
        if not CHROMADB_AVAILABLE or not self.collection:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })

            return formatted_results

        except Exception as e:
            print(f"❌ Search Error: {e}")
            return []

    def generate_project_summary(self) -> str:
        """
        Generiert eine Zusammenfassung des Projekts basierend auf allen Dokumenten

        WICHTIG: Das ist NICHT für Claude direkt - zu groß!
        Stattdessen: Schrittweise Analyse mit RAG
        """
        if not CHROMADB_AVAILABLE:
            return "ChromaDB nicht verfügbar"

        # Hole Stats
        count = self.collection.count()

        summary = f"""
📊 NAJIKA WORLD PROJEKT-ÜBERSICHT

Dokumente in Datenbank: {count:,} Chunks
Durchsuchbar via: analyzer.search("deine frage")

BEISPIEL-QUERIES:
- "Was ist Najika's Persönlichkeit?"
- "Wie funktioniert das Battle System?"
- "Welche APIs gibt es?"
- "Was ist die Projekt-Struktur?"

NÄCHSTER SCHRITT:
Nutze die search() Funktion um relevante Dokument-Teile zu finden,
dann analysiere diese Step-by-Step mit Claude Code!
"""
        return summary


# ===== CLI INTERFACE =====

def main():
    """CLI für Project Analyzer"""
    import sys

    analyzer = NajikaProjectAnalyzer()

    if len(sys.argv) < 2:
        print("""
🧠 NAJIKA PROJECT ANALYZER

BEFEHLE:
  python najika_project_analyzer.py index          - Indiziere alle Dokumente
  python najika_project_analyzer.py search "query" - Suche in Dokumenten
  python najika_project_analyzer.py stats          - Zeige Statistiken
""")
        return

    command = sys.argv[1]

    if command == "index":
        # Indiziere alle Dokumente
        stats = analyzer.index_all_documents()

    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Query fehlt!")
            print("   Beispiel: python najika_project_analyzer.py search \"Najika Persönlichkeit\"")
            return

        query = " ".join(sys.argv[2:])
        print(f"\n🔍 Suche: {query}\n")

        results = analyzer.search(query, n_results=5)

        if not results:
            print("❌ Keine Ergebnisse gefunden")
            return

        for i, result in enumerate(results, 1):
            print(f"\n{'='*60}")
            print(f"ERGEBNIS {i}")
            print(f"{'='*60}")
            print(f"Datei: {result['metadata']['file_path']}")
            print(f"Position: Zeichen {result['metadata']['char_start']}-{result['metadata']['char_end']}")
            if result['distance']:
                print(f"Relevanz: {1 - result['distance']:.2%}")
            print(f"\nText:\n{result['text'][:500]}...")

    elif command == "stats":
        count = analyzer.collection.count() if analyzer.collection else 0
        print(f"\n📊 STATISTIKEN")
        print(f"Chunks in Datenbank: {count:,}")

    else:
        print(f"❌ Unbekannter Befehl: {command}")


if __name__ == "__main__":
    main()
