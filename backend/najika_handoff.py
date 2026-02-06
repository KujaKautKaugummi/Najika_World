#!/usr/bin/env python3
"""
NAJIKA → CLAUDE HANDOFF SYSTEM
Najika analysiert große Dateien und erstellt Summaries für Claude

Usage:
    python najika_handoff.py <files/folders> --output <summary.md>

Beispiel:
    python najika_handoff.py "C:/Najika_World/*.py" --output claude_summary.md
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import glob

class NajikaHandoff:
    """Erstellt Summaries für Claude"""

    def __init__(self):
        self.files_processed = 0
        self.total_lines = 0
        self.total_chars = 0
        self.summaries = []

    def process_pattern(self, pattern):
        """Verarbeitet File-Pattern (z.B. *.py)"""
        files = []

        # Glob-Pattern
        if '*' in pattern:
            files = list(Path().glob(pattern))
        else:
            # Einzelne Datei oder Ordner
            path = Path(pattern)
            if path.is_file():
                files = [path]
            elif path.is_dir():
                files = list(path.rglob('*.*'))

        for file in files:
            if file.is_file():
                self.process_file(file)

    def process_file(self, file_path):
        """Verarbeitet einzelne Datei"""
        try:
            # Lese Datei
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            self.total_lines += len(lines)
            self.total_chars += len(content)
            self.files_processed += 1

            # Erstelle Summary
            summary = self.create_file_summary(file_path, content, lines)
            self.summaries.append(summary)

            print(f"✅ {file_path.name} ({len(lines)} Zeilen)")

        except Exception as e:
            print(f"⚠️  Fehler bei {file_path}: {e}")

    def create_file_summary(self, file_path, content, lines):
        """Erstellt Summary für eine Datei"""
        summary = {
            'path': str(file_path),
            'name': file_path.name,
            'lines': len(lines),
            'chars': len(content),
            'extension': file_path.suffix
        }

        # Erstelle Preview
        if len(lines) <= 50:
            # Kleine Datei: Komplett zeigen
            summary['preview'] = content
            summary['preview_type'] = 'full'
        else:
            # Große Datei: Anfang + Ende
            preview_lines = []
            preview_lines.append("# [ANFANG DER DATEI]")
            preview_lines.extend(lines[:20])
            preview_lines.append("\n# ... (gekürzt) ...\n")
            preview_lines.extend(lines[-10:])
            preview_lines.append("# [ENDE DER DATEI]")

            summary['preview'] = '\n'.join(preview_lines)
            summary['preview_type'] = 'truncated'

        # Extrahiere Key-Infos
        summary['key_info'] = self.extract_key_info(file_path, content, lines)

        return summary

    def extract_key_info(self, file_path, content, lines):
        """Extrahiert wichtige Infos aus Datei"""
        info = {}

        ext = file_path.suffix.lower()

        if ext == '.py':
            # Python: Funktionen, Klassen
            info['functions'] = []
            info['classes'] = []

            for line in lines:
                stripped = line.strip()
                if stripped.startswith('def '):
                    func_name = stripped.split('(')[0].replace('def ', '')
                    info['functions'].append(func_name)
                elif stripped.startswith('class '):
                    class_name = stripped.split('(')[0].split(':')[0].replace('class ', '')
                    info['classes'].append(class_name)

        elif ext in ['.md', '.txt']:
            # Markdown/Text: Überschriften
            info['headings'] = []
            for line in lines:
                if line.startswith('#'):
                    info['headings'].append(line.strip())

        elif ext == '.json':
            # JSON: Top-Level Keys
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    info['keys'] = list(data.keys())
            except:
                pass

        return info

    def create_markdown_summary(self):
        """Erstellt Markdown-Summary für Claude"""
        md_lines = []

        # Header
        md_lines.append("# NAJIKA → CLAUDE HANDOFF")
        md_lines.append(f"**Erstellt:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

        # Statistik
        md_lines.append("## 📊 STATISTIK")
        md_lines.append("")
        md_lines.append(f"- **Dateien analysiert:** {self.files_processed}")
        md_lines.append(f"- **Total Zeilen:** {self.total_lines:,}")
        md_lines.append(f"- **Total Zeichen:** {self.total_chars:,}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

        # File Summaries
        md_lines.append("## 📄 DATEIEN")
        md_lines.append("")

        for summary in self.summaries:
            md_lines.append(f"### `{summary['name']}`")
            md_lines.append("")
            md_lines.append(f"**Pfad:** `{summary['path']}`")
            md_lines.append(f"**Zeilen:** {summary['lines']}")
            md_lines.append(f"**Typ:** {summary['extension']}")
            md_lines.append("")

            # Key Info
            if summary.get('key_info'):
                key_info = summary['key_info']

                if key_info.get('functions'):
                    md_lines.append(f"**Funktionen:** {', '.join(key_info['functions'][:10])}")
                    if len(key_info['functions']) > 10:
                        md_lines.append(f"... und {len(key_info['functions']) - 10} weitere")

                if key_info.get('classes'):
                    md_lines.append(f"**Klassen:** {', '.join(key_info['classes'])}")

                if key_info.get('headings'):
                    md_lines.append("**Überschriften:**")
                    for heading in key_info['headings'][:5]:
                        md_lines.append(f"  - {heading}")

                if key_info.get('keys'):
                    md_lines.append(f"**JSON Keys:** {', '.join(key_info['keys'][:10])}")

                md_lines.append("")

            # Preview
            if summary['preview_type'] == 'full':
                md_lines.append("**Inhalt:**")
            else:
                md_lines.append("**Preview:**")

            md_lines.append("```" + summary['extension'].replace('.', ''))
            md_lines.append(summary['preview'])
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")

        # Footer
        md_lines.append("## 🎯 NÄCHSTE SCHRITTE")
        md_lines.append("")
        md_lines.append("**An Claude:**")
        md_lines.append("1. Lies diese Summary")
        md_lines.append("2. Verstehe den Context")
        md_lines.append("3. Implementiere die gewünschte Funktion")
        md_lines.append("")
        md_lines.append("**Token-Ersparnis:** ~" + f"{self.total_chars // 4:,} Tokens")
        md_lines.append("")
        md_lines.append("✨ **Generiert von Najika für Claude** ✨")

        return '\n'.join(md_lines)

    def save_summary(self, output_file):
        """Speichert Summary als Markdown"""
        markdown = self.create_markdown_summary()

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding='utf-8')

        print()
        print("=" * 70)
        print(f"✅ SUMMARY ERSTELLT: {output_path}")
        print("=" * 70)
        print()
        print(f"📊 {self.files_processed} Dateien → {self.total_lines:,} Zeilen")
        print(f"💾 Token-Ersparnis: ~{self.total_chars // 4:,} Tokens")
        print()
        print("🎯 Gib diese Datei an Claude:")
        print(f"   claude: 'Lies {output_path.name} und...'")
        print()


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("NAJIKA → CLAUDE HANDOFF")
        print("=" * 70)
        print()
        print("Usage:")
        print("  python najika_handoff.py <pattern> --output <file.md>")
        print()
        print("Beispiele:")
        print("  python najika_handoff.py '*.py' --output summary.md")
        print("  python najika_handoff.py 'C:/Najika_World/saves' --output saves_summary.md")
        print("  python najika_handoff.py 'najika_server.py' --output server_summary.md")
        print()
        return

    pattern = sys.argv[1]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "najika_summary.md"

    print()
    print("=" * 70)
    print("NAJIKA → CLAUDE HANDOFF")
    print("=" * 70)
    print()
    print(f"Pattern: {pattern}")
    print(f"Output: {output_file}")
    print()

    handoff = NajikaHandoff()
    handoff.process_pattern(pattern)
    handoff.save_summary(output_file)


if __name__ == "__main__":
    main()
