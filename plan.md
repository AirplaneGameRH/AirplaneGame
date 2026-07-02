# Analyse des Spielkonzepts und der Architektur für ein 2D Flugzeug-Idle-Game

## 1. Überblick über das Spielkonzept

Das Ziel ist die Entwicklung eines 2D Flugzeug-Idle-Games, bei dem der Spieler seinen eigenen Flughafen von einem Tower aus verwaltet. Der Spieler verdient Geld durch Flüge, die in Abhängigkeit von verschiedenen Faktoren (Ziel, Passagierzahl, Flugzeugtyp, Klasse) variieren. Gleichzeitig fallen Kosten für Treibstoff, Reparaturen und andere Betriebsausgaben an. Das Spiel soll eine Mischung aus Idle-Mechaniken und Management-Simulation bieten.

## 2. Kernkomponenten und Funktionalitäten

### 2.1. Visuelle Darstellung (Tower View)

*   **Tower-Textur**: Eine statische Hintergrundtextur, die den Innenraum eines Towers darstellt.
*   **Bildschirme**: Über die Tower-Textur gerenderte Bildschirme, die Spielstatistiken anzeigen.
*   **Frontales Fenster**: Ein Bereich, der einen Live-Render des Flughafens mit startenden und landenden Flugzeugen zeigt.

### 2.2. Spielmechaniken

*   **Flughafen-Generierung**: Zufällige Generierung des Flughafens zu Beginn des Spiels.
*   **Flug-Management**: 
    *   **Einnahmen**: Basierend auf Ziel, Passagierzahl, Flugzeugtyp, Klasse.
    *   **Ausgaben**: Treibstoff, Reparaturen, Wartung.
*   **Flugzeug-Management**: 
    *   Kauf neuer Flugzeuge.
    *   Reparatur beschädigter Flugzeuge.
    *   Treibstoffmanagement.
*   **Wirtschaftssystem**: Geld verdienen und ausgeben.
*   **Werbung**: Investitionen in Werbung zur Steigerung der Passagierzahlen oder Flugfrequenzen.

### 2.3. Benutzeroberfläche (UI)

*   **Statistik-Anzeige**: Geld, Treibstoff, bestes Flugzeug, alle Flugzeuge (Liste/Übersicht).
*   **Hauptkontroll-UI**: Ein interaktives UI-Panel für Aktionen wie:
    *   Flugzeuge kaufen.
    *   Treibstoff kaufen.
    *   Flugzeuge reparieren.
    *   Werbung schalten.
    *   Flüge planen/starten (impliziert durch Idle-Mechanik, aber mit Spielerentscheidungen).

## 3. Technische Architektur (Python & PyQt6)

### 3.1. Hauptmodule

*   **`main.py`**: Startpunkt der Anwendung, Initialisierung des PyQt6-Fensters und der Hauptspiel-Logik.
*   **`game_logic.py`**: Beinhaltet die Kernlogik des Spiels (Wirtschaft, Flug-Simulation, Event-Handling).
*   **`ui_manager.py`**: Verwaltet die PyQt6-Widgets, Layouts und Interaktionen.
*   **`airport_renderer.py`**: Verantwortlich für das Rendern des Flughafens und der Flugzeuge im Live-Fenster (könnte Pygame oder eine andere 2D-Grafikbibliothek verwenden, die in PyQt6 integriert wird).
*   **`data_models.py`**: Definition von Datenstrukturen für Flugzeuge, Flüge, Flughafen, Spielerstatistiken.
*   **`asset_manager.py`**: Lädt und verwaltet Spiel-Assets (Bilder, Texturen, Sounds).

### 3.2. Datenhaltung

*   **Flugzeuge**: Typ, Kapazität, Geschwindigkeit, Treibstoffverbrauch, Zustand (Reparatur nötig), Kosten, Wert.
*   **Flüge**: Ziel, Dauer, Passagiere, Einnahmen, Kosten.
*   **Flughafen**: Start- und Landebahnen, Gates, Hangar.
*   **Spieler**: Geld, Treibstoffbestand, Liste der Flugzeuge.

### 3.3. UI/UX Überlegungen

*   **Responsive Design**: Anpassung der UI an verschiedene Fenstergrößen.
*   **Interaktive Elemente**: Buttons, Slider, Textfelder für Management-Aktionen.
*   **Informationsfluss**: Klare und übersichtliche Darstellung der Statistiken.

## 4. Spiel-Loop und Event-Handling

Das Spiel wird einen Haupt-Loop haben, der regelmäßig aktualisiert wird (z.B. alle Sekunde oder schneller). Innerhalb dieses Loops werden folgende Aktionen ausgeführt:

*   **Zeit-Update**: Fortschreiten der Spielzeit.
*   **Flug-Simulation**: Starten und Landen von Flugzeugen, Berechnung von Einnahmen und Ausgaben.
*   **Statistik-Update**: Aktualisierung der angezeigten Spielerstatistiken.
*   **UI-Rendering**: Aktualisierung der visuellen Elemente.

Events wie der Kauf eines Flugzeugs oder das Starten von Werbung werden über die UI ausgelöst und von der `game_logic` verarbeitet.

## 5. Nächste Schritte

Basierend auf dieser Analyse wird ein detaillierter Entwicklungsplan erstellt, der die einzelnen Phasen der Implementierung, die benötigten Ressourcen und potenzielle Herausforderungen aufzeigt.
