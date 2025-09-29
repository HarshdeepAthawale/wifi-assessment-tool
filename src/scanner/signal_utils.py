"""
signal_utils.py
- Helpers to work with RSSI/Signal values (simple demo).
"""
def signal_to_quality(signal_dbm: int) -> str:
    if signal_dbm >= 70:
        return "Excellent"
    if signal_dbm >= 50:
        return "Good"
    if signal_dbm >= 30:
        return "Fair"
    return "Weak"
