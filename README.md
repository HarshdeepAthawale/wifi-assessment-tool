

---

# WiFi Security Assessment Tool 

An **educational WiFi security assessment tool** that can:

* Scan nearby WiFi networks (using `nmcli` if available, otherwise simulated).
* Simulate handshake capture (safe by default).
* Perform demo dictionary checks.
* Generate JSON/HTML reports.
* Provide a **modern GUI** (built with Tkinter + [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)).

⚠️ **Ethics & Legality**
This tool is for **education and authorized testing only**.
Never attempt to capture or crack WiFi traffic on networks you don’t own or don’t have **explicit written permission** to test. By default, all capture/cracking operations here are simulated.

---

## 📦 Installation

### 1. Clone / extract the repo

```bash
cd ~/Documents/cybersec
unzip wifi-assessment-tool.zip -d .
cd wifi-assessment-tool
```

### 2. Create conda environment (recommended)

```bash
conda create -n wifi-tool python=3.11 -y
conda activate wifi-tool
```

### 3. Install dependencies

```bash
conda install -y pandas jinja2 scapy python-dotenv psutil
pip install ttkbootstrap   # for modern GUI look
```

(If tkinter is missing: `sudo pacman -S tk` on Arch, or `sudo apt install python3-tk` on Debian/Ubuntu.)

---

## 🚀 Usage

### CLI Mode

Run from project root:

```bash
# Scan networks
python -m src.main --scan

# Simulate handshake capture
python -m src.main --scan --simulate-capture

# Generate report
python -m src.main --scan --report report.html
xdg-open report.html   # open in browser
```

### GUI Mode (with ttkbootstrap)

```bash
python -m src.gui.app
```

The GUI provides:

* **Scan Networks** — show list of available WiFi networks.
* **Simulate Capture** — generate fake `.cap` handshake files safely.
* **Generate Report** — export to HTML/JSON.
* **Open Last Report** — view in browser.
* **Activity Log** — real-time updates.

You can change the theme by editing `src/gui/app.py`:

```python
root = tb.Window(themename="darkly")  # try "cosmo", "flatly", "superhero", etc.
```

---

## 📂 Project Layout

```
wifi-assessment-tool/
├── src/
│   ├── main.py            # CLI entrypoint
│   ├── gui/app.py         # Modern GUI (Tkinter + ttkbootstrap)
│   ├── scanner/           # WiFi scanning utilities
│   ├── capture/           # Handshake simulation
│   ├── brute/             # Demo dictionary checks
│   ├── report/            # Report generator
│   └── utils/             # Config & logging
├── data/                  # Wordlists & captured handshakes
├── docs/                  # Design & ethics notes
├── tests/                 # Unit tests
├── requirements.txt
└── README.md
```

---

## 🛠 Development

* Run tests:

  ```bash
  pytest -q
  ```
* Update dependencies:

  ```bash
  conda update --all
  ```

---

