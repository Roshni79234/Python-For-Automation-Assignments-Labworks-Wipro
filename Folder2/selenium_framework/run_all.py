"""Run ALL tests (pytest + unittest style) in ONE pytest run, then open the HTML report.

Usage:  python run_all.py
"""
import os
import subprocess
import sys
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(ROOT, "reports", "report.html")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    code = subprocess.call(
        [sys.executable, "-m", "pytest", "tests", f"--html={REPORT}", "--self-contained-html"],
        cwd=ROOT,
    )
    if os.path.exists(REPORT):
        print(f"\nReport: {REPORT}")
        webbrowser.open("file:///" + REPORT.replace("\\", "/"))
    sys.exit(code)