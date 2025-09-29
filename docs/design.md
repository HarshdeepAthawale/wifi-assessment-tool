# Design: WiFi Security Assessment Tool

## Goals
- Provide an educational tool to scan WiFi networks and evaluate basic security.
- Demonstrate the concepts of encryption types, handshake capture, and dictionary checks.
- Default to simulation for unsafe operations.

## Components
- `scanner/` : uses nmcli to list SSIDs and parse security information.
- `capture/` : wrappers for handshake capture (simulated by default).
- `brute/` : simple dictionary simulation. Real cracking wrappers are optional.
- `report/` : generate JSON/HTML reports from found networks.
- `gui/` : optional Tkinter GUI.

## Notes
- Network capture requires root and system tools (airmon-ng, airodump-ng, etc.).
- Never run capture on networks you don't own.
