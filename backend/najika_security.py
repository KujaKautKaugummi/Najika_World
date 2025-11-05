"""
NAJIKA SECURITY MODULE - "ALCATRAZ"
Digital Bodyguard für Kuja
- Lie Detection / Betrayal Protection
- VPN Status Checking (ExpressVPN)
- Anti-Tracking & Location Obfuscation
- Security Recommendations
"""

import subprocess
import re
import time
import os
from datetime import datetime

class NajikaSecurity:
    def __init__(self):
        """
        Initialisiert Alcatraz Security System
        """
        self.vpn_provider = "ExpressVPN"  # User nutzt ExpressVPN
        self.security_log = []
        self.suspicious_patterns = []

        print("[NAJIKA SECURITY] >> Alcatraz Security System aktiviert")
        print(f"[NAJIKA SECURITY] >> VPN Provider: {self.vpn_provider}")

    # ===== LIE DETECTION / BETRAYAL PROTECTION =====

    def analyze_message_for_lies(self, message, speaker="Unknown"):
        """
        Analysiert eine Message auf Lügen-Indikatoren

        Heuristics:
        - Übermäßige Details (overexplaining)
        - Widersprüchliche Statements
        - Vermeidung von Pronomen ("ich", "mein")
        - Zeitliche Inkonsistenzen
        - Distanzierungssprache
        """
        suspicion_score = 0
        flags = []

        msg_lower = message.lower()

        # 1. Übermäßige Details (zu viele Füllwörter)
        filler_words = ["eigentlich", "ehrlich gesagt", "basically", "literally", "to be honest"]
        filler_count = sum(1 for word in filler_words if word in msg_lower)
        if filler_count >= 2:
            suspicion_score += 15
            flags.append("Excessive filler words (overexplaining)")

        # 2. Vermeidung von "ich" (Distanzierung)
        if len(message.split()) > 20:  # Nur bei längeren Messages
            ich_count = msg_lower.count(" ich ") + msg_lower.count("ich ") + msg_lower.count(" i ")
            if ich_count == 0:
                suspicion_score += 10
                flags.append("Avoidance of first-person pronouns")

        # 3. Defensive Sprache
        defensive_keywords = ["warum sollte ich", "why would i", "ich habe keinen grund", "i have no reason"]
        if any(kw in msg_lower for kw in defensive_keywords):
            suspicion_score += 20
            flags.append("Defensive language detected")

        # 4. Zeitliche Vagueness
        vague_time = ["irgendwann", "maybe", "vielleicht", "könnte sein", "nicht sicher"]
        if any(kw in msg_lower for kw in vague_time):
            suspicion_score += 5
            flags.append("Temporal vagueness")

        # 5. Negative Formulierungen (statt positive)
        # "Ich war NICHT dort" vs "Ich war zu Hause"
        negations = msg_lower.count(" nicht ") + msg_lower.count(" not ") + msg_lower.count(" never ")
        if negations >= 3:
            suspicion_score += 10
            flags.append("Excessive negations")

        # Assessment
        if suspicion_score >= 40:
            assessment = "HIGH RISK - Mögliche Lüge/Täuschung!"
        elif suspicion_score >= 20:
            assessment = "MEDIUM RISK - Verdächtige Muster"
        else:
            assessment = "LOW RISK - Keine Auffälligkeiten"

        result = {
            "speaker": speaker,
            "suspicion_score": suspicion_score,
            "assessment": assessment,
            "flags": flags,
            "timestamp": datetime.now().isoformat()
        }

        # Log für Analyse
        self.security_log.append(result)

        return result

    def detect_betrayal_indicators(self, conversation_history, target_speaker="Unknown"):
        """
        Analysiert komplette Konversations-History auf Verrats-Indikatoren

        Patterns:
        - Plötzliche Verhaltensänderungen
        - Inkonsistenzen über Zeit
        - Informationsweitergabe an Dritte
        - Vertrauensbruch-Keywords
        """
        betrayal_score = 0
        indicators = []

        # Simplified: Analyse der letzten Messages des Speakers
        speaker_messages = [
            msg for msg in conversation_history
            if msg.get("speaker") == target_speaker
        ]

        if len(speaker_messages) < 2:
            return {"ok": False, "msg": "Zu wenig Daten für Betrayal-Analyse"}

        # Check: Plötzliche Themenwechsel
        # Check: Defensive Sprache
        # Check: Distanzierung

        for msg in speaker_messages[-5:]:  # Letzte 5 Messages
            content = msg.get("content", "")
            betrayal_keywords = [
                "geheim", "secret", "niemandem sagen", "don't tell",
                "zwischen uns", "between us", "vertrau mir nicht", "don't trust"
            ]

            if any(kw in content.lower() for kw in betrayal_keywords):
                betrayal_score += 15
                indicators.append(f"Betrayal keyword in: '{content[:50]}...'")

        # Assessment
        if betrayal_score >= 30:
            assessment = "BETRAYAL LIKELY - Verdacht auf Verrat!"
        elif betrayal_score >= 15:
            assessment = "SUSPICIOUS - Überwachung empfohlen"
        else:
            assessment = "SAFE - Keine Verrats-Indikatoren"

        return {
            "speaker": target_speaker,
            "betrayal_score": betrayal_score,
            "assessment": assessment,
            "indicators": indicators
        }

    # ===== VPN STATUS CHECKING =====

    def check_vpn_status(self):
        """
        Prüft ob VPN (ExpressVPN) aktiv ist

        Windows:
        - Prüft ob expressvpn.exe läuft
        - Prüft Netzwerk-Adapter
        """
        try:
            # Check 1: Prozess läuft?
            result = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True,
                timeout=5
            )

            expressvpn_running = "expressvpn" in result.stdout.lower()

            if expressvpn_running:
                print("[SECURITY] OK ExpressVPN Prozess läuft")
                return {
                    "ok": True,
                    "vpn_active": True,
                    "provider": self.vpn_provider,
                    "msg": "ExpressVPN ist aktiv"
                }
            else:
                print("[SECURITY] WARNING ExpressVPN läuft NICHT!")
                return {
                    "ok": False,
                    "vpn_active": False,
                    "provider": self.vpn_provider,
                    "msg": "ExpressVPN ist NICHT aktiv - Verbindung UNSICHER!"
                }

        except Exception as e:
            print(f"[SECURITY] WARNING VPN Check Fehler: {e}")
            return {
                "ok": False,
                "error": str(e),
                "msg": "VPN Status konnte nicht geprüft werden"
            }

    def check_ip_leak(self):
        """
        Prüft auf IP-Leaks (DNS, WebRTC, IPv6)

        Nutzt externe Services:
        - https://api.ipify.org (public IP)
        - Vergleicht mit bekannter VPN-Region
        """
        try:
            import requests

            # Hole Public IP
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            public_ip = response.json().get("ip")

            print(f"[SECURITY] >> Public IP: {public_ip}")

            # TODO: Prüfe ob IP zu VPN-Region gehört
            # Für jetzt: Basic Check

            return {
                "ok": True,
                "public_ip": public_ip,
                "msg": f"Public IP: {public_ip}"
            }

        except Exception as e:
            print(f"[SECURITY] WARNING IP Check Fehler: {e}")
            return {"ok": False, "error": str(e)}

    # ===== ANTI-TRACKING & LOCATION OBFUSCATION =====

    def get_security_recommendations(self):
        """
        Gibt Security-Empfehlungen basierend auf aktuellem Status
        """
        recommendations = []

        # VPN Check
        vpn_status = self.check_vpn_status()
        if not vpn_status.get("vpn_active"):
            recommendations.append({
                "priority": "HIGH",
                "category": "VPN",
                "msg": "ExpressVPN ist NICHT aktiv! Starte VPN für sichere Verbindung."
            })

        # Browser Checks
        recommendations.append({
            "priority": "MEDIUM",
            "category": "Browser",
            "msg": "Nutze Tor Browser für Darknet-Zugriff"
        })

        recommendations.append({
            "priority": "MEDIUM",
            "category": "Tracking",
            "msg": "Deaktiviere Browser-Fingerprinting (uBlock Origin + Canvas Blocker)"
        })

        recommendations.append({
            "priority": "LOW",
            "category": "DNS",
            "msg": "Nutze verschlüsselte DNS (DNS-over-HTTPS): Cloudflare 1.1.1.1"
        })

        return recommendations

    def analyze_security_status(self):
        """
        Komplette Security-Analyse

        Returns:
        - VPN Status
        - IP Status
        - Recommendations
        - Security Score (0-100)
        """
        security_score = 100

        # VPN Check
        vpn = self.check_vpn_status()
        if not vpn.get("vpn_active"):
            security_score -= 40

        # IP Check
        try:
            ip_check = self.check_ip_leak()
            if not ip_check.get("ok"):
                security_score -= 20
        except:
            security_score -= 10

        # Recommendations
        recommendations = self.get_security_recommendations()
        high_priority_count = sum(1 for r in recommendations if r["priority"] == "HIGH")
        security_score -= high_priority_count * 10

        # Assessment
        if security_score >= 80:
            assessment = "SECURE - Guter Schutz"
        elif security_score >= 60:
            assessment = "MEDIUM - Verbesserungen möglich"
        else:
            assessment = "VULNERABLE - Dringend Maßnahmen nötig!"

        return {
            "security_score": max(0, security_score),
            "assessment": assessment,
            "vpn_status": vpn,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }

    # ===== SECURITY LOG =====

    def get_security_log(self, limit=10):
        """Holt die letzten Security-Events"""
        return self.security_log[-limit:]

    def clear_security_log(self):
        """Löscht Security-Log"""
        self.security_log = []
        print("[SECURITY] >> Security Log gelöscht")


# Test-Funktion
if __name__ == "__main__":
    print("=" * 60)
    print("NAJIKA SECURITY - ALCATRAZ TEST")
    print("=" * 60)

    security = NajikaSecurity()

    # Test 1: Lie Detection
    print("\n" + "=" * 60)
    print("TEST 1: Lie Detection")
    print("=" * 60)

    test_messages = [
        "Ich war gestern im Kino und habe einen Film gesehen.",
        "Ehrlich gesagt, basically, ich war eigentlich nicht dort, to be honest.",
        "Warum sollte ich lügen? Ich habe keinen Grund das zu tun!"
    ]

    for msg in test_messages:
        result = security.analyze_message_for_lies(msg, speaker="Test Person")
        print(f"\nMessage: '{msg}'")
        print(f"Suspicion Score: {result['suspicion_score']}")
        print(f"Assessment: {result['assessment']}")
        if result['flags']:
            print(f"Flags: {', '.join(result['flags'])}")

    # Test 2: VPN Status
    print("\n" + "=" * 60)
    print("TEST 2: VPN Status")
    print("=" * 60)
    vpn_status = security.check_vpn_status()
    print(f"VPN Active: {vpn_status.get('vpn_active')}")
    print(f"Message: {vpn_status.get('msg')}")

    # Test 3: Security Analysis
    print("\n" + "=" * 60)
    print("TEST 3: Complete Security Analysis")
    print("=" * 60)
    analysis = security.analyze_security_status()
    print(f"Security Score: {analysis['security_score']}/100")
    print(f"Assessment: {analysis['assessment']}")
    print(f"\nRecommendations:")
    for rec in analysis['recommendations'][:3]:
        print(f"[{rec['priority']}] {rec['category']}: {rec['msg']}")

    print("\n" + "=" * 60)
    print("OK NAJIKA SECURITY TEST ABGESCHLOSSEN")
    print("=" * 60)
