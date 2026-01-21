# ------------------------------------------------------------------------------
# KLAIOS MASTER IMAGE - FINAL VERSION
# ------------------------------------------------------------------------------
# Basis: Das offizielle Kali Linux (Rolling Release)
FROM kalilinux/kali-rolling:latest

# Verhindert Fragen während der Installation
ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------------------------------------------------------
# 1. SYSTEM & HACKING SUITE INSTALLIEREN
# ------------------------------------------------------------------------------
# Hier installieren wir ALLES in einem Block.
# Achte auf die Liste: nmap, metasploit, dos2unix - alles da.
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Basis Tools ---
    sudo \
    curl \
    wget \
    git \
    nano \
    unzip \
    procps \
    # --- Netzwerk Diagnose ---
    net-tools \
    iputils-ping \
    dnsutils \
    iproute2 \
    mtr-tiny \
    traceroute \
    tcpdump \
    whois \
    jq \
    # --- WICHTIG: REPARATUR TOOL ---
    dos2unix \
    # --- Python Umgebung ---
    python3 \
    python3-pip \
    python3-venv \
    # --- WAFFEN (Hacking Tools) ---
    metasploit-framework \
    nmap \
    # --- Aufräumen ---
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------------------
# 2. PYTHON BIBLIOTHEKEN (Für AI Helper & Mail)
# ------------------------------------------------------------------------------
# dnspython = Für Phishing Mail Check
RUN pip3 install --break-system-packages \
    requests \
    dnspython

# ------------------------------------------------------------------------------
# 3. BENUTZER & RECHTE
# ------------------------------------------------------------------------------
RUN useradd -m -s /bin/bash researcher
# Gib dem Nutzer sudo Rechte ohne Passwort (für Nmap Scans wichtig)
RUN echo "researcher ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# ------------------------------------------------------------------------------
# 4. DATEIEN KOPIEREN & REPARIEREN
# ------------------------------------------------------------------------------
COPY start.sh /start.sh
COPY ai_helper.py /usr/local/bin/ai

# Hier wenden wir dos2unix an (das Tool haben wir oben in Schritt 1 installiert)
RUN dos2unix /start.sh
RUN dos2unix /usr/local/bin/ai

# Ausführbar machen
RUN chmod +x /start.sh
RUN chmod +x /usr/local/bin/ai

# ------------------------------------------------------------------------------
# 5. START
# ------------------------------------------------------------------------------
USER researcher
WORKDIR /home/researcher
CMD ["/start.sh"]
