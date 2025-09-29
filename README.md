# WiFi Security Assessment Tool (Starter)

**Purpose:** educational WiFi security assessment tool (scan, simulate handshake capture, dictionary checks, and generate reports).

**Important (ethics & legality):**
- ONLY run capture/cracking code on networks you own or where you have **explicit written permission**.
- This code is provided for education and authorized testing only.
- By default, capture/crack operations are simulated. To perform real capture tools you'd need to modify/enable those modules manually and ensure legal permission.

## Quickstart
1. Create venv & install deps:
   ```bash
   ./scripts/setup.sh
   source .venv/bin/activate
   ```
2. Scan nearby networks:
   ```bash
   python -m src.main --scan
   ```
3. Generate report:
   ```bash
   python -m src.main --scan --report report.html
   ```
4. See `docs/` for design and ethics.

## Project layout
See the `docs/design.md` file for architecture details.

## Contributing
This is a student/demo project. Please keep `data/captured_handshakes/` and full wordlists out of git.
