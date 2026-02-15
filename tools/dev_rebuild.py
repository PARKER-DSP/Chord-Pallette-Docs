#!/usr/bin/env python3
"""
Tier 1 CI: Local dev rebuild + restart automation

Closes all running dev servers, rebuilds the project, and restarts 
mkdocs serve with hot reloading.

Usage:
    python tools/dev_rebuild.py
    
Or from VS Code: Tasks: Run Task > "Dev: Rebuild & Restart Server"
"""

import subprocess
import sys
import time
import platform
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_ACTIVATE = ROOT / '.venv' / 'Scripts' / 'Activate.ps1'

def log(msg: str, level: str = "INFO"):
    """Print colored log message."""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m",  # Green
        "WARN": "\033[93m",     # Yellow
        "ERROR": "\033[91m",    # Red
    }
    reset = "\033[0m"
    color = colors.get(level, "")
    print(f"{color}[{level}]{reset} {msg}")

def close_dev_servers():
    """Close all running Python/mkdocs processes."""
    log("Closing any running dev servers...")
    if platform.system() == "Windows":
        # Windows: use taskkill
        subprocess.run(
            ["taskkill", "/IM", "python.exe", "/F"],
            capture_output=True
        )
        log("Killed Python processes.", "SUCCESS")
    else:
        # Unix: use pkill
        subprocess.run(["pkill", "-f", "mkdocs"], capture_output=True)
        log("Killed mkdocs processes.", "SUCCESS")
    time.sleep(1)  # Wait for processes to fully close

def rebuild():
    """Run mkdocs build to regenerate static site."""
    log("Building static site with mkdocs build...")
    if platform.system() == "Windows":
        cmd = f". {VENV_ACTIVATE}; mkdocs build"
        result = subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=False,
            cwd=ROOT
        )
    else:
        cmd = f"source .venv/bin/activate && mkdocs build"
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=False,
            cwd=ROOT
        )
    
    if result.returncode != 0:
        log("Build failed!", "ERROR")
        return False
    
    log("Build complete.", "SUCCESS")
    return True

def restart_server():
    """Restart mkdocs serve in the background."""
    log("Restarting dev server with hot reload...")
    
    if platform.system() == "Windows":
        # PowerShell command to activate venv and start mkdocs serve
        cmd = f". {VENV_ACTIVATE}; mkdocs serve"
        # Start in background using Start-Process
        ps_cmd = f"""
        $ps = Start-Process powershell -ArgumentList @'-Command', '{cmd}' -NoNewWindow -PassThru
        Write-Output "Dev server PID: $($ps.Id)"
        """
        subprocess.Popen(
            ["powershell", "-Command", ps_cmd],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        # Unix: start mkdocs with nohup in background
        cmd = "source .venv/bin/activate && mkdocs serve"
        subprocess.Popen(
            cmd,
            shell=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    time.sleep(2)  # Wait for server to start
    log("Dev server started in background.", "SUCCESS")

def main():
    """Orchestrate rebuild + restart."""
    log("=" * 60)
    log("Dev Rebuild & Restart Automation", "INFO")
    log("=" * 60)
    
    try:
        close_dev_servers()
        time.sleep(1)
        
        if not rebuild():
            log("Rebuild failed. Aborting restart.", "ERROR")
            return 1
        
        time.sleep(1)
        restart_server()
        
        log("=" * 60)
        log("✅ Ready! Dev server running at http://localhost:8000", "SUCCESS")
        log("=" * 60)
        return 0
    
    except Exception as e:
        log(f"Error: {e}", "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())
