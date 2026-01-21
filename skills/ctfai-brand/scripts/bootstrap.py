#!/usr/bin/env python3
"""
Bootstrap script for ctfai-brand skill.
Creates a local virtual environment and installs dependencies.
Uses only Python stdlib - no external dependencies required.
"""
import subprocess
import sys
from pathlib import Path


def main():
    skill_dir = Path(__file__).parent.parent.resolve()
    venv_dir = skill_dir / ".venv"

    # Determine pip/python paths based on OS
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip"
        python_path = venv_dir / "Scripts" / "python"
    else:
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"

    # Create venv if it doesn't exist
    if not venv_dir.exists():
        print(f"Creating virtual environment at {venv_dir}")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    else:
        print(f"Virtual environment already exists at {venv_dir}")

    # Install dependencies directly (not editable install)
    print("Installing dependencies...")
    subprocess.run([
        str(pip_path), "install",
        "jinja2>=3.0",
        "weasyprint>=60.0",
        "pyyaml>=6.0"
    ], check=True)

    print("\nBootstrap complete!")
    print(f"To render PDFs, use: {python_path} scripts/render_pdf.py --help")


if __name__ == "__main__":
    main()
