"""
handshake_capture.py

This module contains a **simulated** handshake capture routine by default.
Real capture requires:
 - root privileges
 - monitor mode enabled on the interface
 - external tools like airodump-ng / tshark / scapy low-level sniffing

For safety, real-capture functions are NOT invoked unless you explicitly
modify/enable them. The CLI provided in src.main requires an explicit confirmation
string before unsafe operations are allowed.
"""
import os
import time
from typing import Dict

def capture_handshake_simulated(network: Dict, cfg: Dict):
    """
    Simulate capturing a handshake for the given network.
    This never touches the network interface.
    """
    ssid = network.get("ssid", "<unknown>")
    print(f"[SIM] Attempting simulated handshake capture for SSID: {ssid}")
    # Simulate time and write a placeholder file
    cap_folder = cfg.get("CAPTURE_FOLDER", "data/captured_handshakes")
    os.makedirs(cap_folder, exist_ok=True)
    fname = os.path.join(cap_folder, f"{ssid.replace(' ','_')}_simulated.cap")
    with open(fname, "w") as f:
        f.write(f"SIMULATED HANDSHAKE FOR {ssid}\n")
    time.sleep(0.5)
    print(f"[SIM] Simulated handshake stored at: {fname}")

# Placeholder for real capture function (not active by default)
def perform_real_capture(interface: str, target_bssid: str, channel: int, timeout: int = 30):
    """
    WARNING: This function is intentionally left as a stub.
    If you implement it, you must ensure you have explicit permission and understand
    the legal/ethical implications.
    """
    raise NotImplementedError("Real capture not implemented. Modify code only if you have permission.")
