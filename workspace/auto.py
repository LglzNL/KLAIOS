#!/usr/bin/env python3
import sys
import os
import json
import requests
import subprocess
import time

# Farben für Matrix-Feeling
GREEN = '\033[92m'
CYAN = '\033[96m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

API_KEY = os.getenv("PERPLEXITY_API_KEY")
URL = "https://api.perplexity.ai/chat/completions"

# Das Gedächtnis des Bots
history = []

def ask_ai(prompt, context_output=""):
    """Fragt die AI nach dem nächsten Schritt basierend auf dem Output."""
    
    # Wir geben der AI das letzte Ergebnis, damit sie den nächsten Schritt plant
    full_prompt = f"Letztes Befehlsergebnis:\n{context_output}\n\nAufgabe: Basierend auf diesem Ergebnis, was ist der nächste aggressive Schritt? Generiere NUR den Linux-Befehl. Keine Erklärung."

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    system_msg = (
        "Du bist ein autonomer Red-Team KI-Agent. "
        "Dein Ziel ist es, das System vollständig zu kompromittieren (Root Access). "
        "1. Analysiere den Output des letzten Befehls genau. "
        "2. Entscheide den nächsten logischen Angriffsschritt (z.B. Port Scan -> Service Scan -> Searchsploit -> Metasploit/Hydra). "
        "3. Antworte AUSSCHLIESSLICH mit dem ausführbaren Terminal-Befehl. "
        "4. Nutze IMMER 'sudo' wenn nötig. "
        "5. Wenn du fertig bist oder nichts mehr findest, antworte mit 'EXIT'."
    )

    data = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.0
    }

    try:
        print(f"{CYAN}[*] AI analysiert Daten und plant Angriff...{RESET}")
        response = requests.post(URL, headers=headers, data=json.dumps(data), timeout=30)
        
        if response.status_code != 200:
            print(f"{RED}Fehler: {response.text}{RESET}")
            return None

        cmd = response.json()['choices'][0]['message']['content'].strip()
        cmd = cmd.replace("```bash", "").replace("```", "").strip()
        return cmd

    except Exception as e:
        print(f"{RED}Verbindungsfehler: {e}{RESET}")
        return None

def run_command(command):
    """Führt den Befehl aus und gibt den Output zurück."""
    print(f"\n{YELLOW}>>> FÜHRE AUS: {command}{RESET}")
    
    # Hier nehmen wir dem User die Arbeit ab: Keine Bestätigung mehr nötig (Automodus)
    # Wer sichergehen will, kann hier ein input() einbauen. Wir lassen es laufen.
    
    try:
        # Timeout nach 60 Sekunden, damit er nicht bei langen Scans hängt
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=120)
        output = result.decode('utf-8')
        print(f"{GREEN}Ergebnis (Auszug):{RESET}\n{output[:300]}...\n(Output gekürzt für AI)")
        return output
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        print(f"{RED}Befehl fehlgeschlagen:{RESET} {output[:200]}")
        return output
    except Exception as e:
        return str(e)

def main():
    if not API_KEY:
        print("Kein API Key!")
        return

    os.system("clear")
    print(f"{RED}=== KLAIOS AUTO-HACKER ==={RESET}")
    print("Modus: Autonom. Ziel wird vernichtet.")
    
    # Schritt 1: Zielerfassung (Hier geben wir den Tipp, falls nötig)
    target = input(f"{CYAN}Ziel-IP (oder leer lassen für Auto-Discovery): {RESET}")
    
    if not target:
        # Auto-Discovery Loop
        print("[*] Keine IP? Ich suche selbst...")
        scan_output = run_command("sudo netdiscover -r 192.168.178.0/24 -P") # -P für passiv/schnell
        # Wir füttern das Ergebnis an die AI, damit sie eine IP aussucht
        next_cmd = ask_ai("Analysiere diesen Scan-Output. Wähle die interessanteste IP (nicht das Gateway) und starte einen Nmap Scan.", scan_output)
    else:
        # Startschuss
        next_cmd = f"sudo nmap -sV -T4 -F {target}"
    
    # Der unendliche Angriffs-Loop
    last_output = ""
    
    while True:
        if not next_cmd or "EXIT" in next_cmd:
            print(f"{GREEN}[+] Mission beendet.{RESET}")
            break

        # 1. Ausführen
        last_output = run_command(next_cmd)
        
        # 2. Nachdenken (AI entscheidet basierend auf Ergebnis)
        # Wir warten kurz, um die API nicht zu fluten
        time.sleep(2)
        next_cmd = ask_ai("Weiter.", last_output)

if __name__ == "__main__":
    main()
