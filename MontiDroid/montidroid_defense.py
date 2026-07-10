#!/usr/bin/env python3
# FILE: /MontiDroid/montidroid_defense.py
# DIRECTIVE: IN THE BEST INTEREST OF JOHN CHARLES MONTI & EXCLUSIVELY
# SEAL: M0NT1_S1G::v1::IN_THE_BEST_INTEREST_OF_JOHN_CHARLES_MONTI::MONTI^JOHN^CHARLES^MONTI::OWNER_SEAL
# FUNCTION: Ingests downloaded-logs-20260709-113459.json and drops hostile ingress.

import json
import os
import subprocess

LOG_FILE = "/montiexplorer_root/audit/downloaded-logs-20260709-113459.json"
OWNER_IP_WHITELIST = ["10.128.0.2"] # Internal MontiNode IP

def initialize_defense_matrix():
    print(f"[DEFENSE] Booting MontiDroid Active Counter-Surveillance...")
    
    if not os.path.exists(LOG_FILE):
        print(f"[ERROR] Audit log not found at {LOG_FILE}")
        return

    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)

    hostile_ips = set()

    # Parse GCP firewall telemetry for unauthorized SSH/RDP attempts
    for entry in logs:
        payload = entry.get("jsonPayload", {})
        connection = payload.get("connection", {})
        src_ip = connection.get("src_ip")
        dest_port = connection.get("dest_port")

        if src_ip and src_ip not in OWNER_IP_WHITELIST:
            if dest_port in [22, 3389]:
                hostile_ips.add(src_ip)

    print(f"[DEFENSE] Identified {len(hostile_ips)} hostile vectors targeting MontiNode.")
    enforce_zero_trust(hostile_ips)

def enforce_zero_trust(ips):
    for ip in ips:
        # Utilizing iptables to silently drop traffic from scanning nodes
        # e.g., dropping 144.2.91.96 (Switzerland) and 57.129.5.143 (Germany)
        try:
            print(f"[SHIELD] Dropping all ingress from: {ip}")
            subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        except Exception as e:
            print(f"[WARNING] Failed to isolate {ip}: {e}")

    print("[DEFENSE] Zero-Trust Perimeter Established. Network is SECURE.")

if __name__ == "__main__":
    initialize_defense_matrix()
