# Setup und Installation

## Voraussetzungen

- Python 3.9 oder höher
- pip (Python Package Manager)

## Installation

### 1. Dependencies installieren

```bash
# Für normale Entwicklung
pip install -r requirements.txt

# Für vollständige Entwicklung (mit Testing-Tools)
pip install -r requirements-dev.txt

# Oder via pyproject.toml
pip install -e .
pip install -e ".[dev]"
```

### 2. Spiel starten

```bash
python run.py
```

oder via setuptools entry point:

```bash
airportgame
```

## Projektstruktur

```tree
AirportGame/
├── src/                    # Hauptquellcode
│   ├── __init__.py
│   ├── main.py            # Einstiegspunkt
│   ├── config.py          # Spielkonstanten
│   ├── core/              # Kern-Module (Logik, Renderer)
│   ├── entities/          # Datenmodelle (Aircraft, Airport, etc.)
│   ├── widgets/           # UI-Komponenten (Qt)
│   └── utils/             # Helper-Funktionen
├── assets/                # Spielressourcen
│   ├── images/
│   └── sounds/
├── tests/                 # Unit Tests
├── docs/                  # Dokumentation
├── pyproject.toml         # Projektmetadaten & Build-Config
├── requirements.txt       # Runtime Dependencies
├── requirements-dev.txt   # Development Dependencies
└── run.py                 # Launcher-Script
```

## Development Setup

### Pre-commit Hooks aktivieren

```bash
pre-commit install
```

### Code formatieren

```bash
black src/ tests/
isort src/ tests/
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
flake8 src/ tests/
```

### Tests ausführen

```bash
pytest
pytest -v              # Verbose
pytest --cov=src       # Mit Coverage Report
```

## Troubleshooting

### PyQt6 Installation fehlgeschlagen

Auf macOS mit Apple Silicon:

```bash
pip install --upgrade --force-reinstall PyQt6
```

### Pygame wird nicht erkannt

```bash
pip install --upgrade pygame
```
