from src.report.report_generator import generate_report
import os
def test_generate_json(tmp_path):
    outfile = tmp_path / "out.json"
    networks = [{"ssid":"A","security":"WPA2","signal":50}]
    path = generate_report(networks, str(outfile))
    assert os.path.exists(path)
