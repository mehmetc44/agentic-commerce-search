"""
AgenticCommerce — Servis Başlatıcı

Tüm servisleri sırayla ayağa kaldırır:
  1. catalog-api   (Port: 8001)
  2. assistant-api (Port: 8000)
  3. frontend      (Port: 3000)
"""

import subprocess
import sys
import os
import time
import signal

processes = []


def start_service(name: str, cwd: str, command: list, port: int):
    print(f"\n{'='*50}")
    print(f"  {name} başlatılıyor (Port: {port})...")
    print(f"{'='*50}")
    proc = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    processes.append((name, proc))
    time.sleep(2)
    return proc


def shutdown(signum, frame):
    print("\n\nServisleri kapatıyor...")
    for name, proc in reversed(processes):
        print(f"  {name} durduruluyor...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    print("Tüm servisler durduruldu.")
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

ROOT = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":

    # 1. catalog-api
    start_service(
        name="catalog-api",
        cwd=os.path.join(ROOT, "catalog-api"),
        command=[
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload",
        ],
        port=8001,
    )

    # 2. assistant-api
    start_service(
        name="assistant-api",
        cwd=os.path.join(ROOT, "assistant-api"),
        command=[
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
        ],
        port=8000,
    )

    # 3. frontend (Python built-in HTTP server)
    start_service(
        name="frontend",
        cwd=os.path.join(ROOT, "frontend"),
        command=[
            sys.executable, "-m", "http.server", "3000",
        ],
        port=3000,
    )

    print("\n" + "="*50)
    print("  Tüm servisler çalışıyor:")
    print("  catalog-api   → http://localhost:8001")
    print("  assistant-api → http://localhost:8000")
    print("  frontend      → http://localhost:3000")
    print("="*50)
    print("\nDurdurmak için Ctrl+C\n")

    try:
        for name, proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        shutdown(None, None)
