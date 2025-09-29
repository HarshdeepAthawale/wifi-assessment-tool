"""
aircrack_wrapper.py

This wrapper demonstrates how you might call external cracking tools like `aircrack-ng`.
It intentionally DOES NOT call the tool directly. Instead it shows the command
you would run. If you choose to enable, ensure you have permission and installed tools.
"""
import shlex

def build_aircrack_cmd(cap_file: str, wordlist_file: str) -> str:
    # Example command string (do not auto-run without permission)
    cmd = f"aircrack-ng -w {shlex.quote(wordlist_file)} {shlex.quote(cap_file)}"
    return cmd
