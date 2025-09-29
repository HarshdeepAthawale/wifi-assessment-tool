"""
encryption_parser.py
- Small utilities to interpret security strings into categories.
"""
from typing import Dict

def classify_security(security_str: str) -> str:
    s = (security_str or "").upper()
    if "WPA3" in s:
        return "WPA3"
    if "WPA2" in s:
        return "WPA2"
    if "WPA" in s:
        return "WPA"
    if "WEP" in s:
        return "WEP"
    if "WPA" not in s and ("WEP" not in s) and ("WPA2" not in s) and s.strip() == "":
        return "UNKNOWN"
    return s
