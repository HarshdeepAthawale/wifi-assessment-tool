#!/usr/bin/env bash
set -e
echo "[*] This script installs system packages (Debian/Ubuntu) and Python deps."
echo "    You may need sudo for system packages."

# Install system deps (aircrack-ng and wireless-tools are optional — for real testing)
if command -v apt >/dev/null 2>&1; then
  sudo apt update
  sudo apt install -y python3-venv python3-pip wireless-tools net-tools
  echo "[*] Note: aircrack-ng not auto-installed. Install manually if you plan to use real cracking tools."
else
  echo "[*] Non-debian system detected. Install python3-venv and wireless tools manually."
fi

# Create venv and install pip deps
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Done. Activate with: source .venv/bin/activate"
