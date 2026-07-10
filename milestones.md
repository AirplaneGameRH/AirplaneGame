# Meilensteine – AirportGame

Jeder Meilenstein ist ein abgeschlossener, testbarer Schritt. Reihenfolge empfohlen.
Status-Legende: `[ ]` offen · `[~]` in Arbeit · `[x]` erledigt.

---

## M1 – Datenmodelle lebendig machen
**Ziel:** Die Stub-Methoden in `entities/` bekommen echte Logik; `data_models.py` dokumentiert sie.

- [ ] `Aircraft`: `refuel()`, `board_passengers()`, `repair()`, `start_flight()/land()`,
      `enter_maintenance()`, `update()` mit echten Zustandsänderungen (fuel, condition, status).
- [ ] `Airport`: `add_aircraft/remove_aircraft`, `add_flight/remove_flight`,
      `open_gate/close_gate`, `schedule_maintenance`, `update()`.
- [ ] `Flight`: `start()/cancel()/complete()`, `update_progress()` (Fortschritt 0→1),
      `revenue`/`operating_cost` sinnvoll setzen.
- [ ] `Player`: `add_money/spend_money`, `add_aircraft/remove_aircraft`,
      `unlock_aircraft`, `update_stats`, `save_state/load_state`.
- [ ] `tests/test_entities.py` erweitern, sodass Methoden-Verhalten geprüft wird.

**Abnahme:** `pytest` grün; Flugzeug kann betankt/repariert werden und Zustand ändert sich.

---

## M2 – Wirtschafts- & Idle-Logik (GameLogic)
**Ziel:** `GameLogic` wird der spielbare Kern mit `update(dt)`-Tick.

- [ ] `GameLogic` hält `Player` + `Airport` und initialisiert Startwerte aus `config.py`
      (`STARTING_MONEY`, `STARTING_FUEL`).
- [ ] Flug-Lifecycle: Flug planen → `start` → `update_progress` (Idle-Tick) → `complete`,
      dabei Geld/Reputation anpassen (Einnahmen − Treibstoff − Wartung).
- [ ] Treibstoff- & Reparatur-Kosten aus `config.py` (`DEFAULT_FUEL_CONSUMPTION`,
      `REPAIR_COST_PER_DAMAGE`) verwenden.
- [ ] Werbung: Methode, die Passagier-/Frequenzmultiplikator erhöht (ggf. zeitbegrenzt).
- [ ] `GameLogic.update(dt)` als einheitlicher Tick; Signale/Callbacks für UI-Updates.
- [ ] Unit-Tests für Wirtschaftsberechnungen (Einnahme, Kosten, Werbung).

**Abnahme:** Ein simulierter Flug erhöht das Geld des Spielers korrekt; `pytest` grün.

---

## M3 – Tower-Live-Renderer (AirportRenderer)
**Ziel:** Sichtbares Live-Fenster mit Flughafen und Flugzeugen.

- [ ] `AirportRenderer` zeichnet Flughafen-Layout (Runways, Gates, Hangar) via PyQt6
      (`QPainter`/`QGraphicsScene` oder `QWidget.paintEvent`).
- [ ] Flugzeuge werden abhängig vom `Aircraft.status` dargestellt (parked, in-air, maintenance).
- [ ] Animation von Start/Landung anhand des `Flight`-Fortschritts aus M2.
- [ ] Renderer wird aus dem UI-Loop regelmäßig aktualisiert.

**Abnahme:** Man sieht im Tower-Fenster Flugzeuge, die starten/landen.

---

## M4 – Spiel-UI-Widgets
**Ziel:** `Dashboard`, `ControlPanel`, `StatusPanel` werden gebaut und ins UI eingehängt.

- [ ] `DashboardWidget`: zeigt Geld, Treibstoff, bestes Flugzeug, Flottenübersicht (aus `GameLogic`).
- [ ] `ControlPanelWidget`: Buttons/Inputs für Flugzeug kaufen, Treibstoff kaufen,
      reparieren, Werbung, Flug planen – verbunden mit `GameLogic`.
- [ ] `StatusPanelWidget`: laufende Flüge, Wartungsstatus, Flughafen-Events.
- [ ] Widgets aktualisieren sich über `GameLogic`-Callbacks (kein Polling im Widget selbst).
- [ ] Multi-Language: alle neuen Texte über `i18n`/`config`-Strings.

**Abnahme:** Hauptansicht zeigt Live-Statistiken und Aktionen wirken sich sofort aus.

---

## M5 – Neues Spiel / Spiel laden (Flow)
**Ziel:** Die Platzhalter-Buttons im Menü werden funktional.

- [ ] Menü-Buttons verbinden statt Platzhalter: `new_game` startet `GameLogic` + UI,
      `load_game` lädt gespeicherten Stand.
- [ ] Speicherstand via `Player.save_state/load_state` + `to_dict()` serialisieren
      (JSON-Datei, z. B. `savegame.json`).
- [ ] Pause/Resume und „Zurück zum Menü“ sauber umsetzen (Timer stoppen).

**Abnahme:** Neues Spiel startet spielbar; Stand kann gespeichert und neu geladen werden.

---

## M6 – Flughafen-Generierung & Balancing
**Ziel:** Abwechslungsreicher Startzustand und ausgewogene Zahlen.

- [ ] Zufällige Flughafen-Generierung (Gates, Runways, Hangars, Startflotte) beim New Game.
- [ ] Zufällige Ziel-Destinationen mit sinnvollen Distanzen/Preisen.
- [ ] Balancing der Wirtschaft (StartGeld, Kosten, Werbe-Effekt) gegen spielbare Kurve.
- [ ] Edge Cases: Insolvenz (Geld < 0), volle Flotte, kein Treibstoff.

**Abnahme:** Jeder Neustart liefert anderen, spielbaren Flughafen; keine soft-locks.

---

## M7 – Politur & Build
**Ziel:** Release-fähig machen.

- [ ] Feinschliff Tower-Textur/Bildschirme, Sounds bei Aktionen (optional).
- [ ] `requirements.txt`/Build (`setup.py`, `setup.bat`, `pyproject.toml`) prüfen.
- [ ] `README.md`/`docs/SETUP.md` auf aktuellen Stand bringen.
- [ ] Vollständiger `pytest`-Durchlauf + manueller Smoke-Test des ganzen Flows.

**Abnahme:** Spiel ist über `run.py` startbar und durchspielbar.
