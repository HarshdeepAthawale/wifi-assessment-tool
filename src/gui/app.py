"""
GUI for WiFi Security Assessment Tool.

Usage:
    python src/gui/app.py

UI Controls:
- Scan Networks: list nearby networks (uses nmcli if available, else simulated)
- Simulate Capture: simulate handshake capture for selected networks (writes .cap)
- Generate Report: create report.html (or report.json) from the displayed networks
- Clear Log: clear the console log panel
"""
import threading
import queue
import os
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as tb


from src.scanner.wifi_scanner import scan_networks
from src.capture.handshake_capture import capture_handshake_simulated
from src.report.report_generator import generate_report
from src.utils.config import load_config

LOG_POLL_INTERVAL_MS = 200

class GuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Assessment Tool - GUI")
        self.cfg = load_config()
        self.log_q = queue.Queue()
        self.networks = []  # last scanned networks

        self._build_ui()
        # start log pump
        self.root.after(LOG_POLL_INTERVAL_MS, self._pump_log)

    def _build_ui(self):
        # Top frame: buttons
        top = ttk.Frame(self.root, padding=8)
        top.pack(side="top", fill="x")

        self.btn_scan = ttk.Button(top, text="Scan Networks", command=self._on_scan)
        self.btn_scan.pack(side="left", padx=4)

        self.btn_capture = ttk.Button(top, text="Simulate Capture", command=self._on_simulate_capture)
        self.btn_capture.pack(side="left", padx=4)

        self.btn_report = ttk.Button(top, text="Generate Report", command=self._on_generate_report)
        self.btn_report.pack(side="left", padx=4)

        self.btn_open_report = ttk.Button(top, text="Open Last Report", command=self._on_open_report)
        self.btn_open_report.pack(side="left", padx=4)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=6)

        # Middle: networks tree and details
        middle = ttk.Frame(self.root, padding=(8,0))
        middle.pack(fill="both", expand=True)

        # Treeview for networks
        cols = ("ssid", "security", "signal")
        self.tree = ttk.Treeview(middle, columns=cols, show="headings", selectmode="extended", height=10)
        self.tree.heading("ssid", text="SSID")
        self.tree.heading("security", text="Security")
        self.tree.heading("signal", text="Signal")
        self.tree.column("ssid", width=260)
        self.tree.column("security", width=120)
        self.tree.column("signal", width=80, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        vsb = ttk.Scrollbar(middle, orient="vertical", command=self.tree.yview)
        vsb.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Right-side quick info
        right = ttk.Frame(middle, padding=(8,0))
        right.pack(side="left", fill="y")

        ttk.Label(right, text="Selected Network Info:", font=("Segoe UI", 10, "bold")).pack(anchor="nw")
        self.info_text = tk.Text(right, width=36, height=8, wrap="word", state="disabled")
        self.info_text.pack(pady=(4,8))

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Bottom: log area
        ttk.Label(self.root, text="Activity Log:").pack(anchor="w", padx=12)
        self.logbox = ScrolledText(self.root, height=10, state="disabled", wrap="word")
        self.logbox.pack(fill="both", expand=False, padx=8, pady=(0,8))

        bottom_buttons = ttk.Frame(self.root)
        bottom_buttons.pack(fill="x", padx=8, pady=(0,8))
        ttk.Button(bottom_buttons, text="Clear Log", command=self._clear_log).pack(side="right")

        # status bar
        self.status = ttk.Label(self.root, text="Ready", relief="sunken", anchor="w")
        self.status.pack(side="bottom", fill="x")

        # last report path
        self.last_report = None

    # --- UI actions ---
    def _on_scan(self):
        self._set_status("Scanning networks...")
        self._log("Starting network scan...")
        self._set_buttons_state(disabled=True)
        thread = threading.Thread(target=self._scan_worker, daemon=True)
        thread.start()

    def _scan_worker(self):
        try:
            nets = scan_networks()
            self.networks = nets
            self._log(f"Scan finished — {len(nets)} networks found.")
            # update UI in main thread via queue
            self.log_q.put(("update_tree", nets))
        except Exception as e:
            self._log(f"[ERROR] Scan failed: {e}")
        finally:
            self.log_q.put(("scan_done", None))

    def _on_simulate_capture(self):
        selected = self._get_selected_networks()
        if not selected:
            messagebox.showinfo("No selection", "Please select one or more networks in the list to simulate capture.")
            return
        self._set_status("Simulating capture...")
        self._log(f"Simulating handshake capture for {len(selected)} network(s)...")
        self._set_buttons_state(disabled=True)
        thread = threading.Thread(target=self._simulate_capture_worker, args=(selected,), daemon=True)
        thread.start()

    def _simulate_capture_worker(self, selected_networks):
        try:
            for net in selected_networks:
                ssid = net.get("ssid")
                self._log(f"[SIM] Capturing handshake for: {ssid}")
                capture_handshake_simulated(net, self.cfg)
                self._log(f"[SIM] Done for: {ssid}")
            self._log("[SIM] All selected captures finished.")
        except Exception as e:
            self._log(f"[ERROR] Simulated capture failed: {e}")
        finally:
            self.log_q.put(("capture_done", None))

    def _on_generate_report(self):
        if not self.networks:
            messagebox.showinfo("No data", "No networks to report. Scan first.")
            return
        # ask for file name/location
        filetypes = [("HTML report", "*.html"), ("JSON report", "*.json")]
        default = os.path.join(os.getcwd(), "report.html")
        path = filedialog.asksaveasfilename(title="Save report as", defaultextension=".html",
                                            initialfile="report.html", initialdir=os.getcwd(), filetypes=filetypes)
        if not path:
            return
        self._set_status("Generating report...")
        self._log(f"Generating report: {path}")
        self._set_buttons_state(disabled=True)
        thread = threading.Thread(target=self._generate_report_worker, args=(path,), daemon=True)
        thread.start()

    def _generate_report_worker(self, path):
        try:
            generate_report(self.networks, path)
            self.last_report = path
            self._log(f"Report saved to: {path}")
            self.log_q.put(("open_report_prompt", path))
        except Exception as e:
            self._log(f"[ERROR] Report generation failed: {e}")
        finally:
            self.log_q.put(("report_done", None))

    def _on_open_report(self):
        if not self.last_report or not os.path.exists(self.last_report):
            messagebox.showinfo("No report", "No report generated yet. Create a report first.")
            return
        webbrowser.open(f"file://{os.path.abspath(self.last_report)}")

    def _on_tree_select(self, event):
        sel = self._get_selected_networks()
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        if sel:
            for net in sel:
                txt = f"SSID: {net.get('ssid')}\nSecurity: {net.get('security')}\nSignal: {net.get('signal')}\n\n"
                self.info_text.insert("end", txt)
        else:
            self.info_text.insert("end", "No network selected.")
        self.info_text.configure(state="disabled")

    # --- helpers ---
    def _get_selected_networks(self):
        items = self.tree.selection()
        selected = []
        for iid in items:
            try:
                idx = int(iid)
                if idx < len(self.networks):
                    selected.append(self.networks[idx])
            except Exception:
                pass
        return selected

    def _set_buttons_state(self, disabled=False):
        state = "disabled" if disabled else "normal"
        self.btn_scan.config(state=state)
        self.btn_capture.config(state=state)
        self.btn_report.config(state=state)
        self.btn_open_report.config(state=state)

    def _set_status(self, text):
        self.status.config(text=text)

    def _log(self, message):
        # enqueue log to be displayed in main thread
        self.log_q.put(("log", str(message)))

    def _clear_log(self):
        self.logbox.configure(state="normal")
        self.logbox.delete("1.0", "end")
        self.logbox.configure(state="disabled")

    # Pump messages from worker threads into UI
    def _pump_log(self):
        try:
            while True:
                item = self.log_q.get_nowait()
                if not item:
                    continue
                what, payload = item
                if what == "log":
                    self.logbox.configure(state="normal")
                    self.logbox.insert("end", f"{payload}\n")
                    self.logbox.see("end")
                    self.logbox.configure(state="disabled")
                elif what == "update_tree":
                    self._populate_tree(payload)
                elif what == "scan_done":
                    self._set_status("Scan complete.")
                    self._set_buttons_state(disabled=False)
                elif what == "capture_done":
                    self._set_status("Capture simulation finished.")
                    self._set_buttons_state(disabled=False)
                elif what == "report_done":
                    self._set_status("Report generation finished.")
                    self._set_buttons_state(disabled=False)
                elif what == "open_report_prompt":
                    # payload is path
                    self.last_report = payload
                    # optionally auto-open or prompt; we'll prompt
                    if messagebox.askyesno("Report Ready", f"Report saved to:\n{payload}\n\nOpen now?"):
                        webbrowser.open(f"file://{os.path.abspath(payload)}")
                else:
                    # unknown message
                    pass
        except queue.Empty:
            pass
        # schedule next poll
        self.root.after(LOG_POLL_INTERVAL_MS, self._pump_log)

    def _populate_tree(self, networks):
        # clear tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        # insert new network rows and use index as iid
        for idx, n in enumerate(networks):
            ssid = n.get("ssid", "<hidden>")
            sec = n.get("security", "")
            sig = n.get("signal", "")
            self.tree.insert("", "end", iid=str(idx), values=(ssid, sec, sig))

def main():
    root = tb.Window(themename="darkly")  # modern themed window
    root.geometry("900x650")
    app = GuiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
