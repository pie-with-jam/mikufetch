import subprocess
import sys

def test_cli_runs():
    # Just check it doesn't crash
    ret = subprocess.run([sys.executable, "-m", "mikufetch", "--no-art", "--no-color"], capture_output=True)
    assert ret.returncode == 0
    assert b"OS:" in ret.stdout
