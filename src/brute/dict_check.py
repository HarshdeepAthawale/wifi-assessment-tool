"""
dict_check.py

Simple dictionary check simulator. The module expects a `check_function`
that simulates verifying a password for an SSID. This is for demo only
and does not perform any network authentication attempts.
"""
from typing import Callable, List

def simple_dict_check(ssid: str, password_list: List[str], check_function: Callable[[str], bool]) -> str:
    """
    Iterate through password_list and return the first password where check_function returns True.
    check_function should be a simulated validator in demos. Return None if not found.
    """
    print(f"[DEMO] Starting dictionary check simulation for SSID: {ssid} (items={len(password_list)})")
    for pwd in password_list:
        if check_function(pwd):
            print(f"[DEMO] Found password: {pwd}")
            return pwd
    print("[DEMO] No password found in provided wordlist (simulation).")
    return None
