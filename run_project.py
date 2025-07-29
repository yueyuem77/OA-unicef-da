#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run_pipeline():
    print("🔄 Running data preparation pipeline...")
    subprocess.run(["python", str(ROOT / "scripts/clean_merge.py")], check=True)

def run_analysis():
    print("📊 Running weighted coverage analysis...")
    subprocess.run(["python", str(ROOT / "scripts/weighted_coverage.py")], check=True)

def export_report():
    print("📝 Exporting HTML report...")
    subprocess.run([
        "jupyter", "nbconvert",
        "--to", "html",
        "--no-input",
        str(ROOT / "notebooks/report.ipynb"),
        "--output-dir", str(ROOT / "outputs")
    ], check=True)
if __name__ == "__main__":
    run_pipeline()
    run_analysis()
    export_report()
    print("✅ All steps completed. Report generated.")
