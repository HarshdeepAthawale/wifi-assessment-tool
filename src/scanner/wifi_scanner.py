"""
wifi_scanner.py
- Primary scanner uses `nmcli` to list available WiFi networks.
- Falls back to returning a simulated list if nmcli not available.
"""
import subprocess
import re
from typing import List, Dict

def _nmcli_scan() -> str:
    """Return raw nmcli output or raise."""
    return subprocess.check_output(
        ["nmcli", "-f", "SSID,SECURITY,SIGNAL", "dev", "wifi"], universal_newlines=True
    )

def parse_nmcli_output(raw: str) -> List[Dict]:
    """Parse nmcli output into structured dicts."""
    lines = raw.strip().splitlines()
    networks = []
    # nmcli output often has a header line - detect and skip if present
    start = 0
    if len(lines) > 0 and "SSID" in lines[0] and "SECURITY" in lines[0]:
        start = 1
    for line in lines[start:]:
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 3:
            ssid, security, signal = parts[0], parts[1], parts[2]
            try:
                signal_int = int(signal)
            except Exception:
                signal_int = 0
            networks.append({"ssid": ssid or "<hidden>", "security": security or "UNKNOWN", "signal": signal_int})
    return networks

def scan_networks() -> List[Dict]:
    try:
        raw = _nmcli_scan()
        return parse_nmcli_output(raw)
    except FileNotFoundError:
        # nmcli not available — return simulated list
        return [
            {"ssid": "Home_WiFi", "security": "WPA2", "signal": 72},
            {"ssid": "Old_WEP", "security": "WEP", "signal": 34},
            {"ssid": "Cafe_FreeWiFi", "security": "OPEN", "signal": 60},
        ]
    except subprocess.CalledProcessError as exc:
        return [{"ssid": "(error)", "security": "(none)", "signal": 0, "error": str(exc)}]
