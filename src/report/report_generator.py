"""
report_generator.py

Generates JSON or HTML reports for a list of network dicts.
A minimal Jinja2 template is supported for HTML output.
"""
import json
from jinja2 import Template
from typing import List, Dict
import os

DEFAULT_HTML_TEMPLATE = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>WiFi Assessment Report</title></head>
<body>
  <h1>WiFi Assessment Report</h1>
  <ul>
  {% for n in networks %}
    <li><strong>{{n.ssid}}</strong> — Security: {{n.security}} — Signal: {{n.signal}}</li>
  {% endfor %}
  </ul>
</body>
</html>
"""

def generate_report(networks: List[Dict], outfile: str = "report.json"):
    if outfile.endswith(".json"):
        with open(outfile, "w") as fh:
            json.dump({"networks": networks}, fh, indent=2)
        return outfile
    if outfile.endswith(".html"):
        tpl = Template(DEFAULT_HTML_TEMPLATE)
        html = tpl.render(networks=networks)
        with open(outfile, "w") as fh:
            fh.write(html)
        return outfile
    # fallback to json
    with open(outfile, "w") as fh:
        json.dump({"networks": networks}, fh, indent=2)
    return outfile
