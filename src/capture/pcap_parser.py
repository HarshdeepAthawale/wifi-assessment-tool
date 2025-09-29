"""
pcap_parser.py
- Lightweight parser to check for a simulated 'handshake' marker in .cap files.
- For real-world parsing use scapy or pyshark.
"""
from typing import Dict
import os

def pcap_contains_handshake(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, "r", errors="ignore") as f:
            data = f.read(2048)
            if "SIMULATED HANDSHAKE" in data:
                return True
    except Exception:
        return False
    return False
