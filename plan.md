# Plan: 2D Flugzeug-Idle-Game (AirportGame)

## 0. Status quo (Stand des aktuellen Codes)

Der aktuelle Code ist eine **funktionierende App-Hülle** auf Basis von Python + PyQt6.
Folgende Teile sind bereits real implementiert und lauffähig:

- **Start/Launcher** (`run.py`): Qt-App-Setup, High-DPI, Windows-Taskbar-Icon, `pythonw`-Launch.
- **Ladebildschirm** (`loading_screen.py`): Fortschrittsbalken + StatusTexte, mehrsprachig.
- **Menü & Einstellungen** (`menu_screen.py`): Hauptmenü, Sprachumschaltung (DE/EN/…), Lautstärke-Regler (Master/Musik), Vollbild.
- **i18n** (`i18n.py`, `config.py`): Übersetzungssystem mit mehreren Sprachen.
- **Audio** (`audio_manager.py`): Hintergrundmusik in Dauerschleife mit Lautstärke-Steuerung.
- **Asset-Verwaltung** (`asset_manager.py`, `core/assets.py`): Laden von Bildern/Sounds.
- **UI-Grundgerüst** (`ui_manager.py`): `UIManager`-Fenster, `BackgroundWidget` mit Wallpaper, Stacked-Layout.
- **Konfiguration** (`config.py`): Zentrale Konstanten (`STARTING_MONEY=10000`, `STARTING_FUEL=5000`, `AUTO_UPDATE_INTERVAL`, Renderer-Größe, Repair-Kosten usw.).
- **Datenmodelle als Gerüst** (`entities/*.py`): `Aircraft`, `Airport`, `Flight`, `Player` mit vollständigen Attributen und `to_dict()`-Serialisierung. **Methoden sind noch Stubs** (geben `None` zurück).

Folgende Teile sind **noch nicht implementiert** (Stubs / Platzhalter):

- `core/game_logic.py` (`GameLogic`): komplett leer.
- `core/renderer.py` (`AirportRenderer`): komplett leer – kein Flughafen-Live-Render.
- `widgets/control_panel.py`, `widgets/dashboard.py`, `widgets/status_panel.py`: leere Klassen – keine Spiel-UI.
- `data_models.py`: nur Docstring-Platzhalter.
- **Neues Spiel / Spiel laden** (`main.py`): Buttons zeigen nur Platzhalter-Text, kein echter Flow.
- **Kein Save/Load-System**, keine Wirtschafts-/Idle-Logik, keine Flug-Simulation.

> Ziel der nächsten Phasen: Aus der Hülle ein spielbares Idle-Management-Spiel machen.

---

## 1. Spielkonzept (unverändert)

2D-Flugzeug-Idle-Game: Der Spieler verwaltet einen Flughafen vom Tower aus, verdient Geld
mit Flügen (Ziel, Passagiere, Flugzeugtyp, Klasse) und trägt Kosten (Treibstoff, Reparatur,
Wartung). Mischung aus Idle-Mechanik und Management-Simulation.

## 2. Geplante Kernkomponenten

### 2.1 Tower-View (visuell)

- Statische Tower-Textur als Hintergrund.
- Bildschirme mit Statistiken.
- Frontales Live-Fenster mit startenden/landenden Flugzeugen (via `AirportRenderer`).

### 2.2 Spielmechaniken

- Flughafen-Generierung beim Spielstart.
- Flug-Management: Einnahmen (Ziel, Passagiere, Typ, Klasse) / Ausgaben (Treibstoff, Reparatur, Wartung).
- Flugzeug-Management: Kauf, Reparatur, Treibstoff.
- Wirtschaftssystem: Geld verdienen/ausgeben.
- Werbung: Passagier- / Frequenzsteigerung.

### 2.3 UI

- Statistik-Dashboard: Geld, Treibstoff, bestes Flugzeug, Flottenübersicht.
- Control-Panel: Flugzeuge kaufen, Treibstoff kaufen, reparieren, Werbung, Flüge planen.

## 3. Technische Architektur

Vorhandene Module (reale Basis):

- `run.py` → `main.py` (`main(app)`) → baut `UIManager` + Ladebildschirm.
- `core/game_logic.py` (`GameLogic`): **noch zu füllen**.
- `core/renderer.py` (`AirportRenderer`): **noch zu füllen**.
- `entities/` (`Aircraft`, `Airport`, `Flight`, `Player`): Datenmodelle, Methoden implementieren.
- `widgets/` (`ControlPanel`, `Dashboard`, `StatusPanel`): **noch zu bauen**.
- `ui_manager.py`, `asset_manager.py`, `i18n.py`, `audio_manager.py`, `config.py`: vorhanden.

Geplanter Datenfluss:
`UIManager` (Widgets) ⇄ `GameLogic` (Zustand/Wirtschaft) → `AirportRenderer` (Live-View).
`GameLogic` tickt per `QTimer` im `AUTO_UPDATE_INTERVAL` (100 ms) und meldet Änderungen zurück ans UI.

## 4. Spiel-Loop / Event-Handling

- `QTimer` ruft `GameLogic.update(dt)` auf.
- Innerhalb `update`: Zeit, Flug-Simulation (Start/Landung, Einnahmen/Ausgaben), Statistik-Update.
- UI-Widgets lösen Aktionen (Kauf, Reparatur, Werbung, Flug planen) aus → `GameLogic` verarbeitet.
- `AirportRenderer` zeichnet laufenden Zustand ins Live-Fenster.

## 5. Nächste Schritte

Siehe `milestones.md` – dort sind die konkreten, abzuarbeitenden Meilensteine definiert.
