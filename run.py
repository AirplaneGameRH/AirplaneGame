"""
Projekt-Entrypoint für lokalen Start.

Dieses Skript ermöglicht das Starten des Spiels per
`python3 run.py` aus dem Projekt-Root, ohne relative Importprobleme.
"""

from src.main import main


if __name__ == "__main__":
    raise SystemExit(main())
