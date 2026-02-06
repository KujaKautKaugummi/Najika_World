#!/usr/bin/env python3
"""
NAJIKA GRUNDSTEIN UI - Terminal mit Buttons
============================================
Filtert OPTIONAL-Teile aus dem Grundstein

STEUERUNG:
- Pfeiltasten: Navigation
- Enter: Details anzeigen
- D: OPTIONAL-Teil löschen
- K: OPTIONAL-Teil behalten (markieren)
- A: Alle OPTIONAL markieren
- X: Alle OPTIONAL löschen
- 0-3: Filter (0=Alle, 1=FEST, 2=BASIS, 3=OPTIONAL)
- S: Speichern & Fortfahren
- Q: Beenden ohne Speichern
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Curses für Terminal UI
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    print("[ERROR] curses nicht verfügbar!")
    print("Windows: pip install windows-curses")
    sys.exit(1)

# ===== CONFIG =====

GRUNDSTEIN_FILE = Path("C:/Najika_World/grundstein_output/NAJIKA_GRUNDSTEIN.json")
OUTPUT_DIR = Path("C:/Najika_World/grundstein_output")

# ===== GRUNDSTEIN UI =====

class GrundsteinUI:
    """Terminal UI mit Curses"""

    def __init__(self, stdscr, grundstein):
        self.stdscr = stdscr
        self.grundstein = grundstein
        self.current_index = 0
        self.scroll_offset = 0
        self.filter_status = None  # None = alle, "FEST", "BASIS", "OPTIONAL"

        # Markierungen für OPTIONAL (keep = True, delete = False)
        self.optional_decisions = {}  # {index: True/False}

        # Alle Items als Liste
        self.all_items = self._build_items_list()

        # Farben
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # FEST
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # BASIS
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # OPTIONAL
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Ausgewählt
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)     # Zu löschen
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Zu behalten

    def _build_items_list(self):
        """Baut Liste aller Items"""
        items = []

        # MASTER-KERN (FEST)
        items.append({
            'type': 'FEST',
            'title': 'MASTER-KERN (FEST)',
            'content': self.grundstein['master_kern']['content'],
            'source': self.grundstein['master_kern']['source'],
            'index': 0
        })

        # PDF BASIS
        for i, (pdf_name, pdf_data) in enumerate(self.grundstein['pdf_basis'].items(), 1):
            items.append({
                'type': 'BASIS',
                'title': f'PDF BASIS: {pdf_name}',
                'content': pdf_data['content'],
                'source': pdf_name,
                'index': i
            })

        # NAJIKA OPTIONAL
        for i, najika in enumerate(self.grundstein['najika_optional'], len(items)):
            items.append({
                'type': 'OPTIONAL',
                'title': f'Najika-Teil aus {najika["source"]}',
                'content': najika['content'],
                'source': najika['source'],
                'index': i
            })

        return items

    def get_filtered_items(self):
        """Gibt gefilterte Items zurück"""
        if self.filter_status:
            return [item for item in self.all_items if item['type'] == self.filter_status]
        return self.all_items

    def get_color(self, item, is_current):
        """Gibt Farbe für Item zurück"""
        if is_current:
            return curses.color_pair(4) | curses.A_BOLD

        # Check ob OPTIONAL mit Entscheidung
        if item['type'] == 'OPTIONAL':
            idx = item['index']
            if idx in self.optional_decisions:
                if self.optional_decisions[idx]:
                    return curses.color_pair(6)  # Grün = behalten
                else:
                    return curses.color_pair(5)  # Rot = löschen

        # Standard-Farben
        if item['type'] == 'FEST':
            return curses.color_pair(1)
        elif item['type'] == 'BASIS':
            return curses.color_pair(2)
        else:
            return curses.color_pair(3)

    def draw_header(self):
        """Zeichnet Header"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Titel
        title = "NAJIKA GRUNDSTEIN UI - OPTIONAL FILTERN"
        self.stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)

        # Stats
        fest_count = sum(1 for i in self.all_items if i['type'] == 'FEST')
        basis_count = sum(1 for i in self.all_items if i['type'] == 'BASIS')
        optional_count = sum(1 for i in self.all_items if i['type'] == 'OPTIONAL')

        keep_count = sum(1 for v in self.optional_decisions.values() if v)
        delete_count = sum(1 for v in self.optional_decisions.values() if not v)

        stats = f"FEST: {fest_count} | BASIS: {basis_count} | OPTIONAL: {optional_count} (Behalten: {keep_count}, Löschen: {delete_count})"
        self.stdscr.addstr(1, 1, stats[:width-2])

        # Filter
        filter_text = f"Filter: {self.filter_status or 'ALLE'}"
        self.stdscr.addstr(2, 1, filter_text)

        # Trennlinie
        self.stdscr.addstr(3, 0, "=" * width)

        # Controls
        controls = "[↑↓] Nav | [Enter] Details | [D]elete [K]eep | [A]ll Keep [X]All Delete | [0-3] Filter | [S]ave [Q]uit"
        self.stdscr.addstr(height - 2, 0, "=" * width)
        self.stdscr.addstr(height - 1, 1, controls[:width-2])

    def draw_list(self):
        """Zeichnet Items-Liste"""
        height, width = self.stdscr.getmaxyx()
        items = self.get_filtered_items()

        # Verfügbare Zeilen
        list_start = 4
        list_height = height - 6

        # Scroll-Logik
        if self.current_index < self.scroll_offset:
            self.scroll_offset = self.current_index
        if self.current_index >= self.scroll_offset + list_height:
            self.scroll_offset = self.current_index - list_height + 1

        # Items zeichnen
        for i in range(list_height):
            index = self.scroll_offset + i
            if index >= len(items):
                break

            item = items[index]
            y = list_start + i
            is_current = (index == self.current_index)

            # Marker
            marker = ">" if is_current else " "

            # Decision marker für OPTIONAL
            decision_marker = " "
            if item['type'] == 'OPTIONAL':
                idx = item['index']
                if idx in self.optional_decisions:
                    decision_marker = "K" if self.optional_decisions[idx] else "X"

            # Status-Badge
            status_badge = f"[{item['type']}]"

            # Title (gekürzt)
            title = item['title'][:50] if len(item['title']) > 50 else item['title']

            # Content preview
            content_preview = item['content'][:30].replace('\n', ' ')

            # Zeile
            line = f"{marker}{decision_marker} {status_badge:12} {title:52} | {content_preview}"

            # Farbe
            color = self.get_color(item, is_current)

            try:
                self.stdscr.addstr(y, 0, line[:width-1], color)
            except:
                pass

    def show_details(self, item):
        """Zeigt Details eines Items"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Header
        self.stdscr.addstr(0, 1, "ITEM DETAILS", curses.A_BOLD)
        self.stdscr.addstr(1, 0, "=" * width)

        # Details
        self.stdscr.addstr(3, 1, f"Type: {item['type']}")
        self.stdscr.addstr(4, 1, f"Title: {item['title']}")
        self.stdscr.addstr(5, 1, f"Source: {item['source']}")

        if item['type'] == 'OPTIONAL':
            idx = item['index']
            if idx in self.optional_decisions:
                decision = "BEHALTEN" if self.optional_decisions[idx] else "LÖSCHEN"
                self.stdscr.addstr(6, 1, f"Entscheidung: {decision}")

        self.stdscr.addstr(7, 0, "-" * width)

        # Content (scrollbar)
        content_start = 8
        content_height = height - 10

        lines = item['content'].split('\n')
        for i, line in enumerate(lines[:content_height]):
            try:
                self.stdscr.addstr(content_start + i, 1, line[:width-2])
            except:
                pass

        # Footer
        self.stdscr.addstr(height - 2, 0, "=" * width)
        self.stdscr.addstr(height - 1, 1, "[Beliebige Taste] Zurück")

        self.stdscr.refresh()
        self.stdscr.getch()

    def show_message(self, message, wait=True):
        """Zeigt Nachricht an"""
        height, width = self.stdscr.getmaxyx()
        msg_y = height // 2
        msg_x = (width - len(message)) // 2

        # Box
        self.stdscr.addstr(msg_y - 1, msg_x - 2, " " * (len(message) + 4), curses.A_REVERSE)
        self.stdscr.addstr(msg_y, msg_x - 2, f"  {message}  ", curses.A_REVERSE)
        self.stdscr.addstr(msg_y + 1, msg_x - 2, " " * (len(message) + 4), curses.A_REVERSE)

        self.stdscr.refresh()

        if wait:
            curses.napms(1500)

    def save_and_exit(self):
        """Speichert gefilterten Grundstein"""
        # Entferne gelöschte OPTIONAL-Teile
        filtered_optional = []

        for i, najika in enumerate(self.grundstein['najika_optional']):
            # Original-Index aus all_items finden
            original_idx = None
            for item in self.all_items:
                if item['type'] == 'OPTIONAL' and item['source'] == najika['source']:
                    if item['content'] == najika['content']:
                        original_idx = item['index']
                        break

            # Check Entscheidung
            if original_idx in self.optional_decisions:
                if self.optional_decisions[original_idx]:  # Behalten
                    filtered_optional.append(najika)
            else:
                # Keine Entscheidung = behalten
                filtered_optional.append(najika)

        # Update Grundstein
        self.grundstein['najika_optional'] = filtered_optional
        self.grundstein['filtered_at'] = datetime.now().isoformat()
        self.grundstein['optional_kept'] = len(filtered_optional)
        self.grundstein['optional_deleted'] = len(self.optional_decisions) - sum(self.optional_decisions.values())

        # Speichern
        output = OUTPUT_DIR / "NAJIKA_GRUNDSTEIN_FILTERED.json"
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(self.grundstein, f, indent=2, ensure_ascii=False)

        return output

    def run(self):
        """Hauptschleife"""
        while True:
            self.draw_header()
            self.draw_list()
            self.stdscr.refresh()

            key = self.stdscr.getch()
            items = self.get_filtered_items()

            # Navigation
            if key == curses.KEY_UP:
                if self.current_index > 0:
                    self.current_index -= 1

            elif key == curses.KEY_DOWN:
                if self.current_index < len(items) - 1:
                    self.current_index += 1

            # Details
            elif key == ord('\n') or key == curses.KEY_ENTER:
                if items:
                    self.show_details(items[self.current_index])

            # OPTIONAL markieren/löschen
            elif key == ord('d') or key == ord('D'):
                if items and items[self.current_index]['type'] == 'OPTIONAL':
                    idx = items[self.current_index]['index']
                    self.optional_decisions[idx] = False
                    self.show_message("Markiert zum LÖSCHEN")

            elif key == ord('k') or key == ord('K'):
                if items and items[self.current_index]['type'] == 'OPTIONAL':
                    idx = items[self.current_index]['index']
                    self.optional_decisions[idx] = True
                    self.show_message("Markiert zum BEHALTEN")

            # Alle OPTIONAL
            elif key == ord('a') or key == ord('A'):
                for item in self.all_items:
                    if item['type'] == 'OPTIONAL':
                        self.optional_decisions[item['index']] = True
                self.show_message("Alle OPTIONAL markiert zum BEHALTEN")

            elif key == ord('x') or key == ord('X'):
                for item in self.all_items:
                    if item['type'] == 'OPTIONAL':
                        self.optional_decisions[item['index']] = False
                self.show_message("Alle OPTIONAL markiert zum LÖSCHEN")

            # Filter
            elif key == ord('0'):
                self.filter_status = None
                self.current_index = 0
                self.scroll_offset = 0

            elif key == ord('1'):
                self.filter_status = "FEST"
                self.current_index = 0
                self.scroll_offset = 0

            elif key == ord('2'):
                self.filter_status = "BASIS"
                self.current_index = 0
                self.scroll_offset = 0

            elif key == ord('3'):
                self.filter_status = "OPTIONAL"
                self.current_index = 0
                self.scroll_offset = 0

            # Speichern & Fortfahren
            elif key == ord('s') or key == ord('S'):
                output = self.save_and_exit()
                self.show_message(f"Gespeichert: {output.name}")
                return True

            # Beenden
            elif key == ord('q') or key == ord('Q'):
                return False

# ===== MAIN =====

def main(stdscr):
    """Main Entry Point"""
    curses.curs_set(0)
    stdscr.keypad(True)

    # Grundstein laden
    if not GRUNDSTEIN_FILE.exists():
        stdscr.addstr(0, 0, f"[ERROR] Grundstein nicht gefunden: {GRUNDSTEIN_FILE}")
        stdscr.addstr(2, 0, "Bitte erst najika_build_grundstein.py ausführen!")
        stdscr.getch()
        return

    with open(GRUNDSTEIN_FILE, 'r', encoding='utf-8') as f:
        grundstein = json.load(f)

    # UI starten
    ui = GrundsteinUI(stdscr, grundstein)
    success = ui.run()

    # Abschluss
    stdscr.clear()
    if success:
        stdscr.addstr(0, 0, "GRUNDSTEIN GEFILTERT!")
        stdscr.addstr(2, 0, "Gespeichert: NAJIKA_GRUNDSTEIN_FILTERED.json")
        stdscr.addstr(4, 0, "Nächster Schritt: neu neu/ Files hinzufügen")
    else:
        stdscr.addstr(0, 0, "Abgebrochen - keine Änderungen gespeichert")

    stdscr.addstr(6, 0, "Drücke eine Taste...")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
