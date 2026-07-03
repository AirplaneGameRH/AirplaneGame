"""
Entrypoint für das Paket `src`.

Ermöglicht das Starten mit `python -m src`.
"""

from .main import main

if __name__ == "__main__":
    raise SystemExit(main())
