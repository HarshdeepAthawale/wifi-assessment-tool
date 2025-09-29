#!/usr/bin/env python3
"""
CLI entrypoint for the WiFi Security Assessment Tool.
Modes:
  --scan         : perform nmcli scan (safe)
  --report <path>: save report (json/html)
  --simulate-capture : run capture in simulation mode (default)
  --unsafe-allow-capture : enable potentially dangerous capture (requires confirmation)
"""
import argparse
from src.scanner.wifi_scanner import scan_networks
from src.report.report_generator import generate_report
from src.utils.config import load_config
from src.capture.handshake_capture import capture_handshake_simulated

def main():
    parser = argparse.ArgumentParser(description="WiFi Security Assessment Tool")
    parser.add_argument("--scan", action="store_true", help="Scan nearby WiFi networks")
    parser.add_argument("--report", type=str, help="Save report to given file (JSON/HTML)")
    parser.add_argument("--simulate-capture", action="store_true", help="Simulate handshake capture")
    parser.add_argument("--unsafe-allow-capture", action="store_true", help="Enable real capture (requires confirmation)")
    args = parser.parse_args()

    cfg = load_config()
    networks = []

    if args.scan:
        networks = scan_networks()
        print("Found networks:")
        for n in networks:
            print(f"  - {n['ssid']!r} | {n['security']} | signal={n.get('signal')}")

    if args.simulate_capture:
        # simulated: will not perform real capture
        for n in networks:
            capture_handshake_simulated(n, cfg)
    if args.unsafe_allow_capture:
        print("WARNING: You asked to allow real capture. Make sure you own the target networks.")
        confirm = input("Type 'I_HAVE_PERMISSION' to continue: ").strip()
        if confirm != "I_HAVE_PERMISSION":
            print("Confirmation not provided. Aborting unsafe capture.")
        else:
            # Real capture code must be enabled by developer manually.
            print("Unsafe capture acknowledged. To enable, implement capture.handshake_capture.perform_real_capture()")
    if args.report:
        generate_report(networks, args.report)
        print(f"Report saved to {args.report}")

if __name__ == "__main__":
    main()
