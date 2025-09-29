import pytest
from src.scanner.wifi_scanner import parse_nmcli_output

def test_parse_nmcli_output_basic():
    raw = "SSID  SECURITY  SIGNAL\nHome  WPA2      71\nOpen  --        40\n"
    networks = parse_nmcli_output(raw)
    assert isinstance(networks, list)
    assert networks[0]["ssid"] == "Home"
    assert networks[0]["security"].strip() == "WPA2"
