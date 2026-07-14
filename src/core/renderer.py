"""
Render-Logik für den Flughafen.

Dieses Modul ist verantwortlich für die grafische Darstellung des Flughafens
und der Flugzeuge im Tower-Livefenster.
"""

import random
import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QRadialGradient
from ..entities import Airport, Aircraft, Flight


class AirportRenderer(QWidget):
    """Render-Komponente für Flughafen und Flugzeuge - Tower View."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.airport = None
        self.aircraft_list = []
        self.flights = []
        self.setMinimumSize(800, 600)
        
        # Flughafen-Layout (zufällig generiert beim ersten Setzen)
        self._layout_generated = False
        self.runway_positions = []
        self.gate_positions = []
        self.hangar_positions = []
        self.taxiway_paths = []
        
        # Animation
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self.update)
        self._animation_timer.start(50)  # 20 FPS
        
        # Farben
        self.bg_color = QColor(25, 35, 45)
        self.runway_color = QColor(60, 60, 70)
        self.runway_marking_color = QColor(255, 255, 255)
        self.taxiway_color = QColor(50, 55, 65)
        self.gate_color = QColor(70, 130, 180)
        self.gate_occupied_color = QColor(220, 50, 50)
        self.hangar_color = QColor(100, 100, 120)
        self.grass_color = QColor(35, 60, 40)
        self.text_color = QColor(200, 220, 240)
        self.accent_color = QColor(100, 200, 150)
        
        # Flugzeug-Positionen für Animation
        self._aircraft_positions = {}  # aircraft_id -> (x, y, target_x, target_y, state)
        
        # Partikel für Starts/Landungen
        self._particles = []

    def generate_airport_layout(self, airport: Airport) -> None:
        """Generiert ein zufälliges Flughafen-Layout basierend auf den Flughafen-Eigenschaften."""
        w, h = self.width(), self.height()
        if w < 100 or h < 100:
            w, h = 800, 600
            
        # Seed basierend auf Flughafen-Name für reproduzierbare Generierung
        random.seed(hash(airport.name) % 10000)
        
        self.runway_positions = []
        self.gate_positions = []
        self.hangar_positions = []
        self.taxiway_paths = []
        
        # Startbahnen generieren (horizontal oder vertikal)
        for i in range(airport.runways):
            is_horizontal = random.choice([True, False])
            if is_horizontal:
                y = h * 0.15 + i * h * 0.6 / max(1, airport.runways - 1) if airport.runways > 1 else h * 0.5
                length = w * 0.7
                x_start = (w - length) / 2
                self.runway_positions.append({
                    'x1': x_start, 'y1': y, 'x2': x_start + length, 'y2': y,
                    'width': 40, 'horizontal': True, 'id': i
                })
            else:
                x = w * 0.15 + i * w * 0.6 / max(1, airport.runways - 1) if airport.runways > 1 else w * 0.5
                length = h * 0.7
                y_start = (h - length) / 2
                self.runway_positions.append({
                    'x1': x, 'y1': y_start, 'x2': x, 'y2': y_start + length,
                    'width': 40, 'horizontal': False, 'id': i
                })
        
        # Gates generieren (entlang der Terminal-Seite)
        terminal_side = random.choice(['left', 'right', 'top', 'bottom'])
        gate_spacing = 60
        
        if terminal_side in ['left', 'right']:
            x = 80 if terminal_side == 'left' else w - 80
            start_y = h * 0.2
            for i in range(airport.gates):
                y = start_y + i * gate_spacing
                if y > h * 0.8:
                    break
                self.gate_positions.append({
                    'x': x, 'y': y, 'width': 50, 'height': 40,
                    'occupied': False, 'aircraft_id': None, 'id': i
                })
        else:
            y = 80 if terminal_side == 'top' else h - 80
            start_x = w * 0.2
            for i in range(airport.gates):
                x = start_x + i * gate_spacing
                if x > w * 0.8:
                    break
                self.gate_positions.append({
                    'x': x, 'y': y, 'width': 50, 'height': 40,
                    'occupied': False, 'aircraft_id': None, 'id': i
                })
        
        # Hangars generieren
        for i in range(airport.hangars):
            angle = (i / max(1, airport.hangars)) * 2 * math.pi
            radius = min(w, h) * 0.35
            cx, cy = w * 0.5, h * 0.5
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            self.hangar_positions.append({
                'x': x, 'y': y, 'width': 80, 'height': 60,
                'occupied': False, 'aircraft_id': None, 'id': i
            })
        
        # Taxiways (Verbindungen zwischen Gates, Runways, Hangars)
        self._generate_taxiways(w, h)
        
        self._layout_generated = True

    def _generate_taxiways(self, w: int, h: int) -> None:
        """Generiert Rollwege zwischen Gates, Runways und Hangars."""
        # Haupt-Taxiway in der Mitte
        self.taxiway_paths.append({
            'points': [(w * 0.1, h * 0.5), (w * 0.9, h * 0.5)],
            'width': 25
        })
        self.taxiway_paths.append({
            'points': [(w * 0.5, h * 0.1), (w * 0.5, h * 0.9)],
            'width': 25
        })
        
        # Verbindungen zu Gates
        for gate in self.gate_positions:
            # Finde nächsten Punkt auf Haupt-Taxiway
            if gate['x'] < w * 0.5:
                self.taxiway_paths.append({
                    'points': [(gate['x'] + gate['width'], gate['y'] + gate['height'] / 2), 
                              (w * 0.3, gate['y'] + gate['height'] / 2),
                              (w * 0.5, h * 0.5)],
                    'width': 15
                })
            else:
                self.taxiway_paths.append({
                    'points': [(gate['x'], gate['y'] + gate['height'] / 2), 
                              (w * 0.7, gate['y'] + gate['height'] / 2),
                              (w * 0.5, h * 0.5)],
                    'width': 15
                })
        
        # Verbindungen zu Hangars
        for hangar in self.hangar_positions:
            self.taxiway_paths.append({
                'points': [(hangar['x'], hangar['y']), (w * 0.5, h * 0.5)],
                'width': 12
            })

    def set_airport(self, airport: Airport) -> None:
        """Setzt den anzuzeigenden Flughafen und generiert Layout."""
        self.airport = airport
        if not self._layout_generated or airport:
            self.generate_airport_layout(airport)
            self._layout_generated = True

    def set_aircraft(self, aircraft_list: list) -> None:
        """Setzt die Liste der anzuzeigenden Flugzeuge."""
        self.aircraft_list = aircraft_list
        # Initialisiere Positionen für neue Flugzeuge
        for aircraft in aircraft_list:
            aid = id(aircraft)
            if aid not in self._aircraft_positions:
                # Starte an einem freien Gate oder Hangar
                pos = self._find_parking_position(aircraft)
                self._aircraft_positions[aid] = {
                    'x': pos[0], 'y': pos[1],
                    'target_x': pos[0], 'target_y': pos[1],
                    'state': 'parked',  # parked, taxiing, taking_off, landing, flying
                    'progress': 0.0
                }

    def set_flights(self, flights: list) -> None:
        """Setzt die Liste der aktiven Flüge."""
        self.flights = flights

    def _find_parking_position(self, aircraft: Aircraft) -> tuple:
        """Findet eine freie Parkposition für ein Flugzeug."""
        # Erst Gates prüfen
        for gate in self.gate_positions:
            if not gate['occupied']:
                gate['occupied'] = True
                gate['aircraft_id'] = id(aircraft)
                return (gate['x'] + gate['width'] / 2, gate['y'] + gate['height'] / 2)
        
        # Dann Hangars
        for hangar in self.hangar_positions:
            if not hangar['occupied']:
                hangar['occupied'] = True
                hangar['aircraft_id'] = id(aircraft)
                return (hangar['x'] + hangar['width'] / 2, hangar['y'] + hangar['height'] / 2)
        
        # Fallback: Mitte
        return (self.width() / 2, self.height() / 2)

    def _update_aircraft_animations(self) -> None:
        """Aktualisiert Flugzeug-Animationen basierend auf Flight-Status."""
        if not self.airport:
            return
            
        w, h = self.width(), self.height()
        
        for aircraft in self.aircraft_list:
            aid = id(aircraft)
            if aid not in self._aircraft_positions:
                continue
                
            pos = self._aircraft_positions[aid]
            
            # Finde zugehörigen Flug
            flight = None
            for f in self.flights:
                if f.aircraft is aircraft:
                    flight = f
                    break
            
            if flight and flight.status == "in_progress":
                # Flugzeug ist in der Luft - bewege zum Rand (Start/Landung Animation)
                if pos['state'] in ['parked', 'taxiing']:
                    pos['state'] = 'taking_off'
                    # Finde Startbahn
                    rw = self.runway_positions[0] if self.runway_positions else None
                    if rw:
                        if rw['horizontal']:
                            pos['target_x'] = rw['x1']
                            pos['target_y'] = rw['y1']
                        else:
                            pos['target_x'] = rw['x1']
                            pos['target_y'] = rw['y1']
                
                # Animieren zur Startbahn
                if pos['state'] == 'taking_off':
                    dx = pos['target_x'] - pos['x']
                    dy = pos['target_y'] - pos['y']
                    dist = math.hypot(dx, dy)
                    if dist > 5:
                        pos['x'] += dx * 0.02
                        pos['y'] += dy * 0.02
                        # Partikel erzeugen
                        if random.random() < 0.3:
                            self._particles.append({
                                'x': pos['x'] + random.uniform(-10, 10),
                                'y': pos['y'] + random.uniform(-10, 10),
                                'vx': random.uniform(-2, 2),
                                'vy': random.uniform(-2, 2),
                                'life': 1.0,
                                'color': QColor(255, 200, 50, 200)
                            })
                    else:
                        pos['state'] = 'flying'
                        pos['progress'] = 0.0
                
                elif pos['state'] == 'flying':
                    pos['progress'] += 0.005
                    # Flugzeug fliegt aus dem Bildschirm
                    if pos['progress'] > 1.0:
                        # Simuliere Landung nach Flugdauer
                        pos['state'] = 'landing'
                        # Ziel: freie Startbahn
                        rw = self.runway_positions[0] if self.runway_positions else None
                        if rw:
                            pos['target_x'] = rw['x2'] if rw['horizontal'] else rw['x1']
                            pos['target_y'] = rw['y2'] if rw['horizontal'] else rw['y1']
                
                elif pos['state'] == 'landing':
                    dx = pos['target_x'] - pos['x']
                    dy = pos['target_y'] - pos['y']
                    dist = math.hypot(dx, dy)
                    if dist > 5:
                        pos['x'] += dx * 0.03
                        pos['y'] += dy * 0.03
                    else:
                        pos['state'] = 'taxiing'
                        # Zu freiem Gate/Hangar
                        gate_pos = self._find_parking_position(aircraft)
                        pos['target_x'] = gate_pos[0]
                        pos['target_y'] = gate_pos[1]
                
                elif pos['state'] == 'taxiing':
                    dx = pos['target_x'] - pos['x']
                    dy = pos['target_y'] - pos['y']
                    dist = math.hypot(dx, dy)
                    if dist > 3:
                        pos['x'] += dx * 0.02
                        pos['y'] += dy * 0.02
                    else:
                        pos['state'] = 'parked'
                        
            elif flight and flight.status == "scheduled":
                # Wartet auf Start - taxi zur Startbahn
                if pos['state'] == 'parked':
                    pos['state'] = 'taxiing'
                    rw = self.runway_positions[0] if self.runway_positions else None
                    if rw:
                        pos['target_x'] = rw['x1']
                        pos['target_y'] = rw['y1']
                        
            elif aircraft.status == "maintenance":
                # Im Hangar
                if pos['state'] != 'maintenance':
                    pos['state'] = 'maintenance'
                    for hangar in self.hangar_positions:
                        if hangar['aircraft_id'] == aid:
                            pos['target_x'] = hangar['x'] + hangar['width'] / 2
                            pos['target_y'] = hangar['y'] + hangar['height'] / 2
                            break
            
            # Sanfte Bewegung zum Ziel
            if pos['state'] in ['taxiing', 'maintenance'] and pos['state'] != 'flying':
                dx = pos['target_x'] - pos['x']
                dy = pos['target_y'] - pos['y']
                dist = math.hypot(dx, dy)
                if dist > 2:
                    pos['x'] += dx * 0.05
                    pos['y'] += dy * 0.05
        
        # Partikel aktualisieren
        self._particles = [p for p in self._particles if p['life'] > 0]
        for p in self._particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 0.02

    def paintEvent(self, event) -> None:
        """Zeichnet den Flughafen."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        
        # Hintergrund (Gras)
        painter.fillRect(0, 0, w, h, self.grass_color)
        
        # Farbverlauf für Tiefe
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor(30, 45, 55))
        gradient.setColorAt(1, QColor(20, 35, 45))
        painter.fillRect(0, 0, w, h, gradient)
        
        # Layout generieren falls noch nicht geschehen
        if self.airport and not self._layout_generated:
            self.generate_airport_layout(self.airport)
        
        # Animationen updaten
        self._update_aircraft_animations()
        
        # Taxiways zeichnen
        self._draw_taxiways(painter)
        
        # Startbahnen zeichnen
        self._draw_runways(painter)
        
        # Gates zeichnen
        self._draw_gates(painter)
        
        # Hangars zeichnen
        self._draw_hangars(painter)
        
        # Flugzeuge zeichnen
        self._draw_aircraft(painter)
        
        # Partikel zeichnen
        self._draw_particles(painter)
        
        # UI Overlay
        self._draw_overlay(painter)

    def _draw_taxiways(self, painter: QPainter) -> None:
        """Zeichnet Rollwege."""
        pen = QPen(self.taxiway_color)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        
        for tw in self.taxiway_paths:
            pen.setWidth(tw['width'])
            painter.setPen(pen)
            
            points = tw['points']
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            
            # Mittellinie (gelb gestrichelt)
            pen.setWidth(2)
            pen.setColor(QColor(255, 220, 50, 180))
            pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(pen)
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            pen.setStyle(Qt.PenStyle.SolidLine)

    def _draw_runways(self, painter: QPainter) -> None:
        """Zeichnet Startbahnen."""
        for rw in self.runway_positions:
            # Startbahn-Hintergrund
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(self.runway_color))
            
            if rw['horizontal']:
                rect = QRectF(rw['x1'], rw['y1'] - rw['width'] / 2, 
                             rw['x2'] - rw['x1'], rw['width'])
            else:
                rect = QRectF(rw['x1'] - rw['width'] / 2, rw['y1'],
                             rw['width'], rw['y2'] - rw['y1'])
            painter.drawRect(rect)
            
            # Startbahn-Markierungen (weiß)
            painter.setPen(QPen(self.runway_marking_color, 3))
            
            # Schwellenmarkierungen
            if rw['horizontal']:
                painter.drawLine(int(rw['x1']), int(rw['y1']), int(rw['x1'] + 30), int(rw['y1']))
                painter.drawLine(int(rw['x2']), int(rw['y2']), int(rw['x2'] - 30), int(rw['y2']))
                # Mittelstreifen
                pen = QPen(QColor(255, 255, 255, 150), 2, Qt.PenStyle.DashLine)
                painter.setPen(pen)
                painter.drawLine(int(rw['x1']), int(rw['y1']), int(rw['x2']), int(rw['y2']))
                # Nummerierung
                painter.setPen(QPen(self.text_color, 1))
                painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                painter.drawText(int(rw['x1'] + 5), int(rw['y1'] - 5), f"{rw['id'] * 2 + 9:02d}")
                painter.drawText(int(rw['x2'] - 30), int(rw['y2'] + 15), f"{(rw['id'] * 2 + 27) % 36:02d}")
            else:
                painter.drawLine(int(rw['x1']), int(rw['y1']), int(rw['x1']), int(rw['y1'] + 30))
                painter.drawLine(int(rw['x2']), int(rw['y2']), int(rw['x2']), int(rw['y2'] - 30))
                pen = QPen(QColor(255, 255, 255, 150), 2, Qt.PenStyle.DashLine)
                painter.setPen(pen)
                painter.drawLine(int(rw['x1']), int(rw['y1']), int(rw['x2']), int(rw['y2']))
                painter.setPen(QPen(self.text_color, 1))
                painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                painter.drawText(int(rw['x1'] - 15), int(rw['y1'] + 15), f"{rw['id'] * 2 + 9:02d}")
                painter.drawText(int(rw['x2'] + 5), int(rw['y2'] - 5), f"{(rw['id'] * 2 + 27) % 36:02d}")

    def _draw_gates(self, painter: QPainter) -> None:
        """Zeichnet Gates."""
        for gate in self.gate_positions:
            color = self.gate_occupied_color if gate['occupied'] else self.gate_color
            painter.setPen(QPen(color.darker(120), 2))
            painter.setBrush(QBrush(color))
            
            rect = QRectF(gate['x'], gate['y'], gate['width'], gate['height'])
            painter.drawRoundedRect(rect, 4, 4)
            
            # Gate-Nummer
            painter.setPen(QPen(self.text_color, 1))
            painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"G{gate['id'] + 1}")
            
            # Flugzeug-Indikator wenn besetzt
            if gate['occupied']:
                painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
                painter.setFont(QFont("Arial", 7))
                painter.drawText(int(gate['x'] + 2), int(gate['y'] + gate['height'] - 2), "✈")

    def _draw_hangars(self, painter: QPainter) -> None:
        """Zeichnet Hangars."""
        for hangar in self.hangar_positions:
            color = self.hangar_color.darker(130) if hangar['occupied'] else self.hangar_color
            painter.setPen(QPen(color.darker(120), 2))
            painter.setBrush(QBrush(color))
            
            rect = QRectF(hangar['x'] - hangar['width'] / 2, 
                         hangar['y'] - hangar['height'] / 2,
                         hangar['width'], hangar['height'])
            painter.drawRoundedRect(rect, 6, 6)
            
            # Hangar-Tor
            painter.setPen(QPen(color.darker(150), 3))
            painter.drawLine(
                int(hangar['x'] - hangar['width'] / 2 + 5), 
                int(hangar['y']),
                int(hangar['x'] + hangar['width'] / 2 - 5), 
                int(hangar['y'])
            )
            
            # Hangar-Nummer
            painter.setPen(QPen(self.text_color, 1))
            painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            painter.drawText(rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, f"H{hangar['id'] + 1}")

    def _draw_aircraft(self, painter: QPainter) -> None:
        """Zeichnet Flugzeuge an ihren animierten Positionen."""
        for aircraft in self.aircraft_list:
            aid = id(aircraft)
            if aid not in self._aircraft_positions:
                continue
                
            pos = self._aircraft_positions[aid]
            x, y = pos['x'], pos['y']
            
            # Flugzeug-Größe basierend auf Typ
            size = max(12, min(30, aircraft.passenger_capacity / 8))
            
            # Farbe basierend auf Status
            if aircraft.status == "in_flight" or pos['state'] == 'flying':
                color = QColor(100, 200, 255)
            elif aircraft.status == "maintenance" or pos['state'] == 'maintenance':
                color = QColor(255, 150, 50)
            elif pos['state'] in ['taking_off', 'landing']:
                color = QColor(255, 255, 100)
            else:
                color = QColor(150, 220, 150)
            
            # Flugzeug zeichnen (einfaches Dreieck)
            painter.setPen(QPen(color.darker(120), 1.5))
            painter.setBrush(QBrush(color))
            
            # Ausrichtung basierend auf Bewegungsrichtung
            angle = 0
            if pos['state'] in ['taxiing', 'taking_off', 'landing']:
                dx = pos['target_x'] - pos['x']
                dy = pos['target_y'] - pos['y']
                if abs(dx) > 0.1 or abs(dy) > 0.1:
                    angle = math.degrees(math.atan2(-dy, dx))  # -dy weil y nach unten zeigt
            
            painter.save()
            painter.translate(x, y)
            painter.rotate(angle)
            
            # Rumpf
            body = [
                QPointF(0, -size),
                QPointF(-size * 0.6, size * 0.5),
                QPointF(size * 0.6, size * 0.5),
            ]
            painter.drawPolygon(body)
            
            # Tragflächen
            wing = [
                QPointF(-size * 0.8, size * 0.1),
                QPointF(-size * 0.2, size * 0.1),
                QPointF(-size * 0.2, size * 0.4),
                QPointF(-size * 0.8, size * 0.4),
            ]
            painter.drawPolygon(wing)
            
            wing2 = [
                QPointF(size * 0.8, size * 0.1),
                QPointF(size * 0.2, size * 0.1),
                QPointF(size * 0.2, size * 0.4),
                QPointF(size * 0.8, size * 0.4),
            ]
            painter.drawPolygon(wing2)
            
            # Cockpit
            painter.setBrush(QBrush(QColor(200, 230, 255)))
            painter.drawEllipse(QRectF(-size * 0.15, -size * 0.8, size * 0.3, size * 0.3))
            
            painter.restore()
            
            # Name/Modell anzeigen
            painter.setPen(QPen(self.text_color, 1))
            painter.setFont(QFont("Arial", 7))
            painter.drawText(int(x - 30), int(y - size - 5), f"{aircraft.model}")

    def _draw_particles(self, painter: QPainter) -> None:
        """Zeichnet Partikel (Abgase, etc.)."""
        for p in self._particles:
            alpha = int(p['life'] * p['color'].alpha())
            color = QColor(p['color'].red(), p['color'].green(), p['color'].blue(), alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(color))
            size = max(1, int(4 * p['life']))
            painter.drawEllipse(QPointF(p['x'], p['y']), size, size)

    def _draw_overlay(self, painter: QPainter) -> None:
        """Zeichnet UI-Overlay mit Infos."""
        w, h = self.width(), self.height()
        
        # Halbtransparenter Balken oben
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))
        painter.drawRect(0, 0, w, 40)
        
        # Flughafen-Name
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        name = self.airport.name if self.airport else "Kein Flughafen"
        painter.drawText(15, 28, f"🗼 {name}")
        
        # Stats rechts
        if self.airport:
            stats = []
            active_flights = len([f for f in self.flights if getattr(f, 'status', '') == 'in_progress'])
            stats.append(f"Startbahnen: {self.airport.runways}")
            stats.append(f"Gates: {self.airport.gates}")
            stats.append(f"Hangars: {self.airport.hangars}")
            stats.append(f"Flugzeuge: {len(self.aircraft_list)}")
            stats.append(f"Aktiv: {active_flights}")
            
            painter.setFont(QFont("Arial", 10))
            x = w - 15
            for stat in reversed(stats):
                tw = painter.fontMetrics().horizontalAdvance(stat)
                painter.drawText(x - tw, 28, stat)
                x -= tw + 20

    def resizeEvent(self, event) -> None:
        """Neu generieren bei Größenänderung."""
        super().resizeEvent(event)
        if self.airport:
            self._layout_generated = False
            self.generate_airport_layout(self.airport)