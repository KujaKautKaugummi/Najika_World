#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NAJIKA SESSION KNOWLEDGE EXTRACTOR
Extrahiert Wissen aus allen Claude Code Sessions
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
from pathlib import Path
from datetime import datetime
import re

SESSIONS_DIR = Path(r"C:\Users\0KKK0\.claude\projects\C--Najika-World")
OUTPUT_FILE = Path(r"C:\Najika_World\SESSION_KNOWLEDGE_SUMMARY.md")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def extract_key_info_from_session(session_file, max_lines=5000):
    """Extrahiert wichtige Infos aus einer Session"""
    info = {
        "file": session_file.name,
        "size_kb": session_file.stat().st_size / 1024,
        "modified": datetime.fromtimestamp(session_file.stat().st_mtime),
        "files_edited": set(),
        "files_created": set(),
        "commands_run": [],
        "key_decisions": [],
        "bugs_fixed": [],
        "features_added": []
    }

    if info["size_kb"] < 1:
        return None  # Skip empty sessions

    try:
        with open(session_file, 'r', encoding='utf-8', errors='replace') as f:
            line_count = 0
            for line in f:
                line_count += 1
                if line_count > max_lines:
                    break

                try:
                    data = json.loads(line)

                    # Extract tool calls
                    if "content" in data:
                        content = str(data.get("content", ""))

                        # Files edited/created
                        edit_matches = re.findall(r'Edit.*?file_path["\s:]+([^"]+\.(?:py|js|html|json|md))', content)
                        for m in edit_matches:
                            info["files_edited"].add(Path(m).name)

                        write_matches = re.findall(r'Write.*?file_path["\s:]+([^"]+\.(?:py|js|html|json|md))', content)
                        for m in write_matches:
                            info["files_created"].add(Path(m).name)

                        # Bash commands
                        bash_matches = re.findall(r'"command":\s*"([^"]+)"', content)
                        for cmd in bash_matches[:10]:  # Max 10 commands
                            if len(cmd) < 200:
                                info["commands_run"].append(cmd[:100])

                        # Bug fixes (look for patterns)
                        if "fix" in content.lower() or "gefixt" in content.lower():
                            fix_context = content[:200].replace('\n', ' ')
                            if fix_context not in info["bugs_fixed"]:
                                info["bugs_fixed"].append(fix_context[:150])

                        # Features added
                        if "implementiert" in content.lower() or "hinzugefuegt" in content.lower() or "added" in content.lower():
                            feat_context = content[:200].replace('\n', ' ')
                            if feat_context not in info["features_added"]:
                                info["features_added"].append(feat_context[:150])

                except json.JSONDecodeError:
                    continue

    except Exception as e:
        log(f"  Error reading {session_file.name}: {e}")
        return None

    # Convert sets to lists
    info["files_edited"] = list(info["files_edited"])[:20]
    info["files_created"] = list(info["files_created"])[:20]
    info["commands_run"] = info["commands_run"][:10]
    info["bugs_fixed"] = info["bugs_fixed"][:5]
    info["features_added"] = info["features_added"][:5]

    return info

def main():
    log("=" * 70)
    log("NAJIKA SESSION KNOWLEDGE EXTRACTOR")
    log("=" * 70)

    # Find all main sessions (not agents)
    all_sessions = list(SESSIONS_DIR.glob("*.jsonl"))
    main_sessions = [s for s in all_sessions if not s.name.startswith("agent-")]

    log(f"\nGefunden: {len(main_sessions)} Haupt-Sessions")

    # Sort by modification time (newest first)
    main_sessions.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # Extract info from sessions
    session_infos = []
    for i, session in enumerate(main_sessions[:20]):  # Top 20 sessions
        log(f"Analysiere {i+1}/20: {session.name[:20]}...")
        info = extract_key_info_from_session(session)
        if info:
            session_infos.append(info)

    # Generate summary markdown
    log("\nGeneriere Summary...")

    summary = f"""# 📊 NAJIKA SESSION KNOWLEDGE SUMMARY

**Generiert:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Sessions analysiert:** {len(session_infos)}

---

## 🕐 NEUESTE SESSIONS

| Datum | Groesse | Session ID |
|-------|---------|------------|
"""

    for info in session_infos[:10]:
        summary += f"| {info['modified'].strftime('%Y-%m-%d %H:%M')} | {info['size_kb']:.0f}KB | {info['file'][:36]}... |\n"

    summary += """

---

## 📝 BEARBEITETE DATEIEN (letzte Sessions)

"""

    all_edited = set()
    all_created = set()
    for info in session_infos:
        all_edited.update(info["files_edited"])
        all_created.update(info["files_created"])

    summary += f"**Editiert ({len(all_edited)}):** "
    summary += ", ".join(sorted(all_edited)[:30]) + "\n\n"

    summary += f"**Erstellt ({len(all_created)}):** "
    summary += ", ".join(sorted(all_created)[:30]) + "\n\n"

    summary += """
---

## 🐛 BUGS GEFIXT

"""

    all_bugs = []
    for info in session_infos:
        all_bugs.extend(info["bugs_fixed"])

    for bug in all_bugs[:15]:
        summary += f"- {bug}...\n"

    summary += """

---

## ✨ FEATURES HINZUGEFUEGT

"""

    all_features = []
    for info in session_infos:
        all_features.extend(info["features_added"])

    for feat in all_features[:15]:
        summary += f"- {feat}...\n"

    summary += """

---

## 💻 HAEUFIGE COMMANDS

"""

    all_commands = []
    for info in session_infos:
        all_commands.extend(info["commands_run"])

    # Count command frequency
    cmd_counts = {}
    for cmd in all_commands:
        cmd_short = cmd[:50]
        cmd_counts[cmd_short] = cmd_counts.get(cmd_short, 0) + 1

    sorted_cmds = sorted(cmd_counts.items(), key=lambda x: x[1], reverse=True)

    for cmd, count in sorted_cmds[:10]:
        summary += f"- `{cmd}` ({count}x)\n"

    summary += """

---

*Dieses Summary wird automatisch generiert aus Claude Code Session-Logs.*
"""

    # Save summary
    OUTPUT_FILE.write_text(summary, encoding='utf-8')
    log(f"\n✅ Summary gespeichert: {OUTPUT_FILE}")

    # Print summary
    print("\n" + "=" * 70)
    print(summary[:3000])
    print("..." if len(summary) > 3000 else "")

if __name__ == "__main__":
    main()
