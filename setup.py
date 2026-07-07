import subprocess
import sys
import os


subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

__import__("dotenv").load_dotenv(".env")  # Lädt die Umgebungsvariablen aus der .env-Datei

if os.environ.get("DEVELOPMENT_MODE") == "1":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])