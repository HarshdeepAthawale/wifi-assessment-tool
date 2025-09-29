"""
config.py - small loader for environment-based configuration.
"""
import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    cfg = {
        "DEFAULT_INTERFACE": os.getenv("DEFAULT_INTERFACE", "wlan0"),
        "CAPTURE_FOLDER": os.getenv("CAPTURE_FOLDER", "data/captured_handshakes"),
        "SIMULATE_CAPTURE": os.getenv("SIMULATE_CAPTURE", "true").lower() in ("1","true","yes"),
    }
    return cfg

# For easier imports
def load_config_from_env():
    return load_config()
