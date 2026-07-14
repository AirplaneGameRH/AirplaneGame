"""
Startpunkt der Anwendung.

Dieses Modul ist zuständig für die Initialisierung des PyQt6-Fensters,
das Laden der Spielressourcen und das Starten der Hauptspiel-Logik.
"""

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedLayout,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QGraphicsBlurEffect,
    QMessageBox,
    QInputDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
)
import time
import json
import os
from datetime import datetime
from .i18n import init_translator
from .loading_screen import LoadingScreen
from .menu_screen import MenuScreen, SettingsScreen
from .core import GameLogic, AirportRenderer, AssetManager
from .ui_manager import UIManager, BackgroundWidget
from .audio_manager import BackgroundMusic
from .settings import get_settings


SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
os.makedirs(SAVE_DIR, exist_ok=True)
SAVE_SLOTS = 10


class NewGameDialog(QDialog):
    """Dialog für neues Spiel mit Name und Schwierigkeitsgrad."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neues Spiel")
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
                color: white;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                background-color: #16213e;
                color: white;
                border: 1px solid #0f3460;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #e94560;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #d63850;
            }
            QPushButton:pressed {
                background-color: #c02d42;
            }
            QDialogButtonBox QPushButton {
                min-width: 100px;
            }
        """)
        
        layout = QFormLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Spielername
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Mein Flughafen")
        self.name_edit.setText(f"Flughafen {datetime.now().strftime('%d.%m.%Y')}")
        layout.addRow("Spielname:", self.name_edit)
        
        # Schwierigkeitsgrad
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems([
            "Einfach (Startgeld: $1.000.000, günstige Kosten)",
            "Normal (Startgeld: $500.000, normale Kosten)",
            "Schwer (Startgeld: $200.000, teure Kosten)",
            "Experte (Startgeld: $50.000, sehr teure Kosten, keine Werbung)"
        ])
        self.difficulty_combo.setCurrentIndex(1)  # Normal als Standard
        layout.addRow("Schwierigkeit:", self.difficulty_combo)
        
        # Flughafen-Name
        self.airport_name_edit = QLineEdit()
        self.airport_name_edit.setPlaceholderText("Internationaler Flughafen")
        self.airport_name_edit.setText("Berlin International")
        layout.addRow("Flughafen-Name:", self.airport_name_edit)
        
        # Startflotte
        self.start_fleet_combo = QComboBox()
        self.start_fleet_combo.addItems([
            "Klein (1x Cessna 172)",
            "Mittel (1x Cessna 172, 1x Airbus A320)",
            "Groß (1x Airbus A320, 1x Boeing 737)",
            "Keine (leerer Start)"
        ])
        self.start_fleet_combo.setCurrentIndex(1)
        layout.addRow("Startflotte:", self.start_fleet_combo)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Spiel starten")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
        layout.addRow("", buttons)
    
    def get_settings(self):
        """Gibt die gewählten Einstellungen zurück."""
        diff_settings = {
            0: {"money": 1000000, "fuel_cost_mult": 0.5, "repair_cost_mult": 0.5, "ad_allowed": True},
            1: {"money": 500000, "fuel_cost_mult": 1.0, "repair_cost_mult": 1.0, "ad_allowed": True},
            2: {"money": 200000, "fuel_cost_mult": 1.5, "repair_cost_mult": 1.5, "ad_allowed": True},
            3: {"money": 50000, "fuel_cost_mult": 2.0, "repair_cost_mult": 2.0, "ad_allowed": False},
        }
        diff = diff_settings[self.difficulty_combo.currentIndex()]
        
        fleet_settings = {
            0: ["Cessna 172"],
            1: ["Cessna 172", "Airbus A320"],
            2: ["Airbus A320", "Boeing 737"],
            3: [],
        }
        
        return {
            "game_name": self.name_edit.text().strip() or "Unbenanntes Spiel",
            "airport_name": self.airport_name_edit.text().strip() or "Internationaler Flughafen",
            "difficulty": self.difficulty_combo.currentIndex(),
            "start_money": diff["money"],
            "fuel_cost_mult": diff["fuel_cost_mult"],
            "repair_cost_mult": diff["repair_cost_mult"],
            "ad_allowed": diff["ad_allowed"],
            "start_fleet": fleet_settings[self.start_fleet_combo.currentIndex()],
        }


class LoadGameDialog(QDialog):
    """Dialog zum Laden eines Spielstands aus 10 Slots."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spiel laden")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a2e;
                color: white;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
            QListWidget {
                background-color: #16213e;
                color: white;
                border: 1px solid #0f3460;
                border-radius: 4px;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #0f3460;
            }
            QListWidget::item:selected {
                background-color: #e94560;
            }
            QListWidget::item:hover {
                background-color: #1f4068;
            }
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #d63850;
            }
            QPushButton:disabled {
                background-color: #333;
                color: #888;
            }
            QDialogButtonBox QPushButton {
                min-width: 100px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titel
        title = QLabel("💾 Spielstand laden")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #e94560;")
        layout.addWidget(title)
        
        # Liste der Save-Slots
        self.save_list = QListWidget()
        self.save_list.itemDoubleClicked.connect(self.accept)
        layout.addWidget(self.save_list)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Laden")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
        self.load_button = buttons.button(QDialogButtonBox.StandardButton.Ok)
        self.load_button.setEnabled(False)
        self.save_list.itemSelectionChanged.connect(
            lambda: self.load_button.setEnabled(len(self.save_list.selectedItems()) > 0)
        )
        layout.addWidget(buttons)
        
        self.refresh_saves()
    
    def refresh_saves(self):
        """Aktualisiert die Liste der Save-Slots."""
        self.save_list.clear()
        for i in range(1, SAVE_SLOTS + 1):
            filepath = os.path.join(SAVE_DIR, f"save_slot_{i}.json")
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    game_name = data.get("game_name", f"Slot {i}")
                    airport_name = data.get("airport_name", "Unbekannt")
                    money = data.get("player", {}).get("money", 0)
                    reputation = data.get("player", {}).get("reputation", 0)
                    aircraft_count = len(data.get("aircraft", []))
                    save_time = data.get("save_time", "Unbekannt")
                    
                    # Zeit formatieren
                    try:
                        dt = datetime.fromisoformat(save_time.replace('Z', '+00:00'))
                        time_str = dt.strftime("%d.%m.%Y %H:%M")
                    except:
                        time_str = save_time
                    
                    item = QListWidgetItem()
                    item.setText(
                        f"Slot {i}: {game_name}\n"
                        f"  📍 {airport_name}  |  💰 ${money:,.0f}  |  ⭐ {reputation:.1f}  |  ✈️ {aircraft_count} Flugzeuge\n"
                        f"  💾 Gespeichert: {time_str}"
                    )
                    item.setData(Qt.ItemDataRole.UserRole, filepath)
                    self.save_list.addItem(item)
                except Exception as e:
                    item = QListWidgetItem(f"Slot {i}: Fehler beim Lesen ({e})")
                    item.setForeground(Qt.GlobalColor.red)
                    self.save_list.addItem(item)
            else:
                item = QListWidgetItem(f"Slot {i}: 📭 Leer")
                item.setForeground(Qt.GlobalColor.gray)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.save_list.addItem(item)
    
    def get_selected_save(self):
        """Gibt den Pfad des gewählten Save-Files zurück."""
        items = self.save_list.selectedItems()
        if items:
            return items[0].data(Qt.ItemDataRole.UserRole)
        return None


def main(app=None):
    """Erzeugt das Hauptfenster und gibt es zurück."""
    app = app or QApplication.instance() or QApplication([])
    
    # Lade persistente Einstellungen
    settings = get_settings()
    saved_language = settings.get("language", "de")
    
    # Erstelle Translator als globale Instanz (Google Translate, kein API-Key nötig)
    translator = init_translator(saved_language)
    
    # Lade Lautstärke-Einstellungen
    saved_master_volume = settings.get_int("master_volume", 100)
    saved_music_volume = settings.get_int("music_volume", 30)

    try:
        start_time = time.time()
        # Erstelle UIManager im Loading-Modus (ohne GameLogic/Renderer/Assets)
        window = UIManager(None, None, None, loading_mode=True)
        window.translator = translator

        loading_screen = LoadingScreen(translator)
        window.setCentralWidget(loading_screen)

        window.show()
        window.raise_()
        window.activateWindow()
        app.processEvents()

        loading_screen.set_status(translator.t("loading_assets"))
        loading_screen.set_progress(10)
        app.processEvents()
        assets = AssetManager()

        loading_screen.set_status(translator.t("initializing_renderer"))
        loading_screen.set_progress(40)
        app.processEvents()
        renderer = AirportRenderer()

        loading_screen.set_status(translator.t("starting_logic"))
        loading_screen.set_progress(70)
        app.processEvents()
        game = GameLogic()
        game.start_game()

        window.game_logic = game
        window.renderer = renderer
        window.assets = assets

        loading_screen.set_progress(100)
        loading_screen.set_status("")
        app.processEvents()

        def show_main_ui():
            elapsed = time.time() - start_time
            if elapsed < 5.0:
                return True

            timer.stop()
            window.set_fullscreen()

            # UI-Komponenten erstellen
            if window.dashboard is None:
                from .widgets import DashboardWidget, ControlPanelWidget, StatusPanelWidget
                window.dashboard = DashboardWidget()
                window.control_panel = ControlPanelWidget()
                window.status_panel = StatusPanelWidget()

            # Erstelle BackgroundWidget mit Wallpaper
            bg_widget = BackgroundWidget()

            # Inhaltsebene (Menü, Einstellungen, Game-Screen) als transparentes Overlay
            content_widget = QWidget()
            content_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)

            window.menu_screen = MenuScreen(translator, parent=window)
            window.settings_screen = SettingsScreen(translator, parent=window)
            # Wende gespeicherte Lautstärke-Einstellungen an
            window.settings_screen.master_volume = saved_master_volume
            window.settings_screen.music_volume = saved_music_volume
            window.settings_screen.master_slider.setValue(saved_master_volume)
            window.settings_screen.music_slider.setValue(saved_music_volume)

            # Menü-Buttons verbinden
            window.menu_screen.new_game_button.clicked.connect(
                lambda: start_new_game(window))
            window.menu_screen.load_game_button.clicked.connect(
                lambda: load_game(window))
            window.menu_screen.settings_button.clicked.connect(lambda: show_settings())

            def on_back() -> None:
                window.settings_screen.save_settings()
                show_menu()

            window.settings_screen.back_button.clicked.connect(on_back)

            def apply_volumes() -> None:
                master = window.settings_screen.master_volume / 100.0
                music = window.settings_screen.music_volume / 100.0
                if window.background_music is not None:
                    window.background_music.set_volume(master * music)
                window.settings_screen.apply_settings()

            window.settings_screen.master_slider.valueChanged.connect(
                lambda v: (setattr(window.settings_screen, "master_volume", v), apply_volumes())
            )
            window.settings_screen.music_slider.valueChanged.connect(
                lambda v: (setattr(window.settings_screen, "music_volume", v), apply_volumes())
            )

            window.stack = QStackedLayout()
            content_layout.addLayout(window.stack, 1)
            window.stack.addWidget(window.menu_screen)
            window.stack.addWidget(window.settings_screen)

            window.placeholder_screen = QWidget(parent=window)
            placeholder_layout = QVBoxLayout(window.placeholder_screen)
            placeholder_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            window.placeholder_label = QLabel()
            window.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            window.placeholder_label.setStyleSheet("font-size: 20px; color: white; padding: 20px;")
            placeholder_layout.addWidget(window.placeholder_label)
            window.stack.addWidget(window.placeholder_screen)

            # Game Screen mit Tower View in der Mitte und Controls unten
            window.game_screen = QWidget()
            game_layout = QVBoxLayout(window.game_screen)
            game_layout.setContentsMargins(20, 20, 20, 20)
            game_layout.setSpacing(15)

            # Obere Leiste mit Dashboard-Infos und Buttons
            top_bar = QWidget()
            top_bar.setFixedHeight(70)
            top_bar.setStyleSheet("""
                QWidget {
                    background-color: rgba(0, 0, 0, 180);
                    border-radius: 10px;
                }
            """)
            top_layout = QHBoxLayout(top_bar)
            top_layout.setContentsMargins(20, 10, 20, 10)
            top_layout.setSpacing(15)
            
            # Airport name on left
            airport_label = QLabel(f"🗼 {window.game_logic.airport.name}")
            airport_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e94560;")
            top_layout.addWidget(airport_label)
            
            top_layout.addStretch()
            
            # Dashboard kompakt in Top Bar
            window.dashboard.setMaximumHeight(50)
            top_layout.addWidget(window.dashboard, 1)
            
            top_layout.addStretch()
            
            # Save Button
            save_btn = QPushButton("💾 Speichern")
            save_btn.setMinimumWidth(120)
            save_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0096ff;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #0078cc;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
            """)
            save_btn.clicked.connect(lambda: save_game(window))
            top_layout.addWidget(save_btn)
            
            # Quit to Menu Button
            menu_btn = QPushButton("🏠 Hauptmenü")
            menu_btn.setMinimumWidth(120)
            menu_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e94560;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #d63850;
                }
                QPushButton:pressed {
                    background-color: #c02d42;
                }
            """)
            menu_btn.clicked.connect(lambda: show_menu())
            top_layout.addWidget(menu_btn)
            
            game_layout.addWidget(top_bar)

            # Mittig: Tower View (Renderer) - nimmt den meisten Platz ein
            game_layout.addWidget(window.renderer, 1)

            # Unten: Control Panel und Status Panel nebeneinander
            bottom_widget = QWidget()
            bottom_widget.setFixedHeight(180)
            bottom_widget.setStyleSheet("""
                QWidget {
                    background-color: rgba(0, 0, 0, 180);
                    border-radius: 8px;
                }
            """)
            bottom_layout = QHBoxLayout(bottom_widget)
            bottom_layout.setContentsMargins(15, 10, 15, 10)
            bottom_layout.setSpacing(15)
            
            # Control Panel (links, breiter)
            window.control_panel.setMinimumWidth(400)
            bottom_layout.addWidget(window.control_panel, 2)
            
            # Status Panel (rechts)
            window.status_panel.setMinimumWidth(300)
            bottom_layout.addWidget(window.status_panel, 1)
            
            game_layout.addWidget(bottom_widget)

            window.stack.addWidget(window.game_screen)

            # Hintergrund und Inhalt überlagern
            central = QWidget()
            grid = QGridLayout(central)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setSpacing(0)
            grid.addWidget(bg_widget, 0, 0)
            grid.addWidget(content_widget, 0, 0)

            window.bg_widget = bg_widget
            window.setCentralWidget(central)
            window.stack.setCurrentWidget(window.menu_screen)

            # Starte Hintergrundmusik
            master_vol = saved_master_volume / 100.0
            music_vol = saved_music_volume / 100.0
            window.background_music = BackgroundMusic(volume=master_vol * music_vol)
            window.background_music.play()

            # Keyboard Shortcuts
            window.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            
            # Ctrl+S für Quick Save
            from PyQt6.QtGui import QShortcut, QKeySequence
            quick_save_shortcut = QShortcut(QKeySequence(Qt.Key.Key_S | Qt.KeyboardModifier.ControlModifier), window)
            quick_save_shortcut.activated.connect(lambda: quick_save(window))
            
            # Escape für Menü
            menu_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), window)
            menu_shortcut.activated.connect(lambda: show_menu())

            def quick_save(window_obj: UIManager) -> None:
                """Schnellspeichern in Slot 1."""
                filepath = os.path.join(SAVE_DIR, "save_slot_1.json")
                save_data = {
                    "game_name": window_obj.game_logic.player.name,
                    "airport_name": window_obj.game_logic.airport.name,
                    "save_time": datetime.now().isoformat(),
                    "player": window_obj.game_logic.player.to_dict(),
                    "airport": window_obj.game_logic.airport.to_dict(),
                    "aircraft": [a.to_dict() for a in window_obj.game_logic.aircraft],
                    "flights": [f.to_dict() for f in window_obj.game_logic.flights],
                }
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(save_data, f, indent=2)
                    window_obj.status_panel.add_event("⚡ Quick Save in Slot 1 (Ctrl+S)")
                except Exception as e:
                    window_obj.status_panel.add_event(f"❌ Quick Save fehlgeschlagen: {e}")

            # Verbinde GameLogic Callbacks
            def on_state_changed(state):
                if window.dashboard:
                    window.dashboard.update_stats(
                        money=state["money"],
                        reputation=state["reputation"],
                        aircraft_count=state["aircraft_count"],
                        active_flights=state["active_flights"],
                        fuel_percent=100.0,
                    )
            
            def on_flight_completed(flight):
                if window.status_panel:
                    window.status_panel.add_event(f"✈ Flug {flight.flight_number} abgeschlossen!")
            
            def on_event(message):
                if window.status_panel:
                    window.status_panel.add_event(message)
            
            game.set_callbacks(
                on_state_changed=on_state_changed,
                on_flight_completed=on_flight_completed,
                on_event=on_event,
            )

            # Verbinde Control Panel Buttons
            connect_control_panel(window)

            # Starte Game Loop Timer
            window.game_timer = QTimer()
            window.game_timer.timeout.connect(lambda: game_loop(window))
            window.game_timer.start(100)  # 10 FPS

            return False

        def game_loop(window_obj: UIManager) -> None:
            """Hauptspielschleife - wird alle 100ms aufgerufen."""
            if window_obj.game_logic and window_obj.game_logic.running:
                window_obj.game_logic.update(0.1)
                
                # Update Renderer (Tower View)
                if window_obj.renderer:
                    window_obj.renderer.set_airport(window_obj.game_logic.airport)
                    window_obj.renderer.set_aircraft(window_obj.game_logic.aircraft)
                    window_obj.renderer.set_flights(window_obj.game_logic.flights)
                    # Renderer updated sich selbst über seinen Timer
                
                # Update Status Panel
                if window_obj.status_panel:
                    for flight in window_obj.game_logic.flights:
                        if flight.status == "in_progress":
                            window_obj.status_panel.add_flight(
                                flight.flight_number, 
                                flight.status, 
                                getattr(flight, '_progress', 0.0)
                            )

        def connect_control_panel(window_obj: UIManager) -> None:
            """Verbindet die Control Panel Buttons mit der GameLogic."""
            game = window_obj.game_logic
            
            # Flugzeug kaufen
            window_obj.control_panel.buy_aircraft_btn.clicked.connect(
                lambda: show_buy_aircraft_dialog(window_obj))
            
            # Reparieren
            window_obj.control_panel.repair_btn.clicked.connect(
                lambda: show_repair_dialog(window_obj))
            
            # Werbung
            window_obj.control_panel.advertise_btn.clicked.connect(
                lambda: start_advertising(window_obj))
            
            # Betanken
            window_obj.control_panel.refuel_btn.clicked.connect(
                lambda: show_refuel_dialog(window_obj))
            
            # Flug planen
            window_obj.control_panel.schedule_flight_btn.clicked.connect(
                lambda: show_schedule_flight_dialog(window_obj))

        def show_buy_aircraft_dialog(window_obj: UIManager) -> None:
            """Zeigt Dialog zum Flugzeugkauf."""
            game = window_obj.game_logic
            aircraft_types = game.get_available_aircraft_types()
            
            dialog = QDialog(window_obj)
            dialog.setWindowTitle("Flugzeug kaufen")
            dialog.setMinimumWidth(500)
            dialog.setStyleSheet("""
                QDialog { background-color: #1a1a2e; color: white; }
                QLabel { color: #e0e0e0; font-size: 13px; }
                QComboBox { background-color: #16213e; color: white; border: 1px solid #0f3460; 
                           border-radius: 4px; padding: 8px; font-size: 13px; }
                QComboBox::drop-down { border: none; width: 20px; }
                QPushButton { background-color: #e94560; color: white; border: none; 
                             padding: 10px 20px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #d63850; }
            """)
            
            layout = QFormLayout(dialog)
            layout.setSpacing(15)
            layout.setContentsMargins(25, 25, 25, 25)
            
            combo = QComboBox()
            for i, at in enumerate(aircraft_types):
                combo.addItem(
                    f"{at['name']} ({at['model']}) - ${at['purchase_price']:,} | "
                    f"Passagiere: {at['passenger_capacity']} | Reichweite: {at['max_fuel']} | "
                    f"Geschw.: {at['speed']} km/h",
                    i
                )
            
            layout.addRow("Flugzeugtyp:", combo)
            
            # Info Label
            info_label = QLabel("Wähle ein Flugzeug zum Kauf. Du hast ${:,.0f} verfügbar.".format(game.player.money))
            info_label.setWordWrap(True)
            info_label.setStyleSheet("color: #aaa; font-size: 12px;")
            layout.addRow("", info_label)
            
            # Update info when selection changes
            def update_info(idx):
                at = aircraft_types[idx]
                affordable = "✅ Kaufbar" if game.player.money >= at['purchase_price'] else "❌ Zu teuer"
                info_label.setText(
                    f"{at['name']} ({at['model']})\n"
                    f"Preis: ${at['purchase_price']:,} | {affordable}\n"
                    f"Passagiere: {at['passenger_capacity']} | Fracht: {at['cargo_capacity']:,} kg\n"
                    f"Max. Treibstoff: {at['max_fuel']:,} | Geschwindigkeit: {at['speed']} km/h\n"
                    f"Betriebskosten: ${at['operating_cost']:,}/Flug"
                )
            combo.currentIndexChanged.connect(update_info)
            update_info(0)
            
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Kaufen")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
            layout.addRow("", buttons)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                index = combo.currentData()
                aircraft = game.buy_aircraft(index)
                if aircraft:
                    window_obj.status_panel.add_event(f"✈ Neues Flugzeug gekauft: {aircraft.name} für ${aircraft.purchase_price:,}")
                else:
                    QMessageBox.warning(window_obj, "Kauf fehlgeschlagen", "Nicht genug Geld für dieses Flugzeug!")

        def show_repair_dialog(window_obj: UIManager) -> None:
            """Zeigt Dialog zur Reparatur."""
            game = window_obj.game_logic
            aircraft_list = game.get_aircraft_list()
            
            if not aircraft_list:
                QMessageBox.information(window_obj, "Keine Flugzeuge", "Sie besitzen keine Flugzeuge!")
                return
            
            dialog = QDialog(window_obj)
            dialog.setWindowTitle("Flugzeug reparieren")
            dialog.setMinimumWidth(450)
            dialog.setStyleSheet("""
                QDialog { background-color: #1a1a2e; color: white; }
                QLabel { color: #e0e0e0; font-size: 13px; }
                QComboBox { background-color: #16213e; color: white; border: 1px solid #0f3460; 
                           border-radius: 4px; padding: 8px; }
                QPushButton { background-color: #e94560; color: white; border: none; 
                             padding: 10px 20px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #d63850; }
            """)
            
            layout = QFormLayout(dialog)
            layout.setSpacing(15)
            layout.setContentsMargins(25, 25, 25, 25)
            
            combo = QComboBox()
            for i, a in enumerate(aircraft_list):
                damage = 100 - a.condition
                cost = damage * 100 * 1.0  # repair cost mult
                status_icon = "🟢" if a.condition > 70 else "🟡" if a.condition > 30 else "🔴"
                combo.addItem(
                    f"{status_icon} {a.name} ({a.model}) - Zustand: {a.condition:.0f}% - Reparatur: ${cost:,.0f}",
                    i
                )
            
            layout.addRow("Flugzeug:", combo)
            
            info_label = QLabel()
            info_label.setWordWrap(True)
            info_label.setStyleSheet("color: #aaa; font-size: 12px;")
            layout.addRow("", info_label)
            
            def update_repair_info(idx):
                a = aircraft_list[idx]
                damage = 100 - a.condition
                cost = damage * 100 * 1.0
                affordable = "✅" if game.player.money >= cost else "❌"
                info_label.setText(
                    f"Zustand: {a.condition:.0f}% | Wartung: {a.maintenance_level:.0f}%\n"
                    f"Reparaturkosten: ${cost:,.0f} {affordable}\n"
                    f"Verfügbares Geld: ${game.player.money:,.0f}"
                )
            combo.currentIndexChanged.connect(update_repair_info)
            update_repair_info(0)
            
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Reparieren")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
            layout.addRow("", buttons)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                index = combo.currentData()
                aircraft = aircraft_list[index]
                if game.repair_aircraft(aircraft):
                    window_obj.status_panel.add_event(f"🔧 {aircraft.name} repariert!")
                else:
                    QMessageBox.warning(window_obj, "Reparatur fehlgeschlagen", "Nicht genug Geld!")

        def start_advertising(window_obj: UIManager) -> None:
            """Startet Werbung."""
            game = window_obj.game_logic
            if not game.start_advertising(1.0, 5000):
                QMessageBox.warning(window_obj, "Werbung fehlgeschlagen", "Nicht genug Geld ($5.000 benötigt) oder Werbung läuft bereits!")
            else:
                window_obj.status_panel.add_event("📢 Werbung gestartet (1h, +50% Passagiere, $5.000)")

        def show_refuel_dialog(window_obj: UIManager) -> None:
            """Zeigt Dialog zum Betanken."""
            game = window_obj.game_logic
            aircraft_list = game.get_aircraft_list()
            
            if not aircraft_list:
                QMessageBox.information(window_obj, "Keine Flugzeuge", "Sie besitzen keine Flugzeuge!")
                return
            
            dialog = QDialog(window_obj)
            dialog.setWindowTitle("Flugzeug betanken")
            dialog.setMinimumWidth(450)
            dialog.setStyleSheet("""
                QDialog { background-color: #1a1a2e; color: white; }
                QLabel { color: #e0e0e0; font-size: 13px; }
                QComboBox { background-color: #16213e; color: white; border: 1px solid #0f3460; 
                           border-radius: 4px; padding: 8px; }
                QPushButton { background-color: #e94560; color: white; border: none; 
                             padding: 10px 20px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #d63850; }
            """)
            
            layout = QFormLayout(dialog)
            layout.setSpacing(15)
            layout.setContentsMargins(25, 25, 25, 25)
            
            combo = QComboBox()
            for i, a in enumerate(aircraft_list):
                needed = a.max_fuel - a.fuel
                cost = needed * 5
                combo.addItem(
                    f"⛽ {a.name} - Treibstoff: {a.fuel:.0f}/{a.max_fuel:.0f} - Kosten: ${cost:,.0f}",
                    i
                )
            
            layout.addRow("Flugzeug:", combo)
            
            info_label = QLabel()
            info_label.setWordWrap(True)
            info_label.setStyleSheet("color: #aaa; font-size: 12px;")
            layout.addRow("", info_label)
            
            def update_refuel_info(idx):
                a = aircraft_list[idx]
                needed = a.max_fuel - a.fuel
                cost = needed * 5
                affordable = "✅" if game.player.money >= cost else "❌"
                info_label.setText(
                    f"Aktueller Treibstoff: {a.fuel:.0f} / {a.max_fuel:.0f}\n"
                    f"Benötigt: {needed:.0f} Einheiten | Kosten: ${cost:,.0f} {affordable}\n"
                    f"Verfügbares Geld: ${game.player.money:,.0f}"
                )
            combo.currentIndexChanged.connect(update_refuel_info)
            update_refuel_info(0)
            
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Betanken")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
            layout.addRow("", buttons)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                index = combo.currentData()
                aircraft = aircraft_list[index]
                if game.refuel_aircraft(aircraft):
                    window_obj.status_panel.add_event(f"⛽ {aircraft.name} vollgetankt!")
                else:
                    QMessageBox.warning(window_obj, "Betanken fehlgeschlagen", "Nicht genug Geld!")

        def show_schedule_flight_dialog(window_obj: UIManager) -> None:
            """Zeigt Dialog zur Flugplanung."""
            game = window_obj.game_logic
            aircraft_list = game.get_aircraft_list()
            destinations = game.get_available_destinations()
            
            if not aircraft_list:
                QMessageBox.information(window_obj, "Keine Flugzeuge", "Sie besitzen keine Flugzeuge!")
                return
            
            # Nur verfügbare (geparkte) Flugzeuge
            available_aircraft = [(i, a) for i, a in enumerate(aircraft_list) if a.status == "parked"]
            if not available_aircraft:
                QMessageBox.information(window_obj, "Keine verfügbaren Flugzeuge", "Alle Flugzeuge sind in der Luft oder in Wartung!")
                return
            
            dialog = QDialog(window_obj)
            dialog.setWindowTitle("Flug planen")
            dialog.setMinimumWidth(550)
            dialog.setStyleSheet("""
                QDialog { background-color: #1a1a2e; color: white; }
                QLabel { color: #e0e0e0; font-size: 13px; }
                QComboBox { background-color: #16213e; color: white; border: 1px solid #0f3460; 
                           border-radius: 4px; padding: 8px; }
                QPushButton { background-color: #e94560; color: white; border: none; 
                             padding: 10px 20px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #d63850; }
            """)
            
            layout = QFormLayout(dialog)
            layout.setSpacing(15)
            layout.setContentsMargins(25, 25, 25, 25)
            
            dest_combo = QComboBox()
            for i, d in enumerate(destinations):
                dest_combo.addItem(
                    f"🌍 {d['name']} - {d['distance']} km - {d['base_passengers']} Pass. - ${d['ticket_price']}/Ticket",
                    i
                )
            
            ac_combo = QComboBox()
            for orig_idx, a in available_aircraft:
                ac_combo.addItem(
                    f"✈ {a.name} ({a.model}) - Kapazität: {a.passenger_capacity} - Treibstoff: {a.fuel:.0f}/{a.max_fuel:.0f}",
                    orig_idx
                )
            
            layout.addRow("Ziel:", dest_combo)
            layout.addRow("Flugzeug:", ac_combo)
            
            # Preview
            preview_label = QLabel()
            preview_label.setWordWrap(True)
            preview_label.setStyleSheet("color: #aaa; font-size: 12px; background: #16213e; padding: 10px; border-radius: 4px;")
            layout.addRow("Vorschau:", preview_label)
            
            def update_preview():
                d = destinations[dest_combo.currentData()]
                a = aircraft_list[ac_combo.currentData()]
                passengers = min(int(d['base_passengers'] * (game.player.reputation / 50.0) * game._advertising_multiplier), a.passenger_capacity)
                cargo = min(a.cargo_capacity * 0.5, d['distance'] * 10)
                revenue = passengers * d['ticket_price'] + cargo * 10
                fuel_needed = d['distance'] * 0.1
                fuel_cost = fuel_needed * 5
                profit = revenue - fuel_cost - d['distance'] * 0.1
                
                preview_label.setText(
                    f"Passagiere: {passengers}/{a.passenger_capacity} | Fracht: {cargo:.0f} kg\n"
                    f"Einnahmen: ${revenue:,.0f} | Treibstoffkosten: ${fuel_cost:,.0f} | Wartung: ${d['distance'] * 0.1:,.0f}\n"
                    f"Gewinn (geschätzt): ${profit:,.0f} | Flugzeit: ~{d['distance'] / a.speed * 10:.1f}s\n"
                    f"Benötigter Treibstoff: {fuel_needed:.0f} | Verfügbar: {a.fuel:.0f} {'✅' if a.fuel >= fuel_needed else '❌'}"
                )
            
            dest_combo.currentIndexChanged.connect(update_preview)
            ac_combo.currentIndexChanged.connect(update_preview)
            update_preview()
            
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Flug planen")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
            layout.addRow("", buttons)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                dest_idx = dest_combo.currentData()
                ac_idx = ac_combo.currentData()
                if game.schedule_flight(dest_idx, ac_idx):
                    window_obj.status_panel.add_event("📅 Flug geplant!")
                else:
                    QMessageBox.warning(window_obj, "Planung fehlgeschlagen", "Flug konnte nicht geplant werden!")

        def start_new_game(window_obj: UIManager) -> None:
            """Startet ein neues Spiel mit Dialog."""
            dialog = NewGameDialog(window_obj)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                settings = dialog.get_settings()
                
                # Neue GameLogic mit Einstellungen
                from .core import GameLogic
                window_obj.game_logic = GameLogic()
                
                # Wende Schwierigkeitsgrad an
                window_obj.game_logic.player.money = settings["start_money"]
                window_obj.game_logic.player.name = settings["game_name"]
                window_obj.game_logic.airport.name = settings["airport_name"]
                
                # Speichere Multiplikatoren für Kosten
                window_obj.game_logic._fuel_cost_multiplier = settings["fuel_cost_mult"]
                window_obj.game_logic._repair_cost_multiplier = settings["repair_cost_mult"]
                window_obj.game_logic._ad_allowed = settings["ad_allowed"]
                
                # Startflotte hinzufügen
                for fleet_item in settings["start_fleet"]:
                    for i, at in enumerate(window_obj.game_logic.available_aircraft_types):
                        if at["name"] in fleet_item:
                            aircraft = window_obj.game_logic.buy_aircraft(i)
                            if aircraft:
                                aircraft.fuel = aircraft.max_fuel
                            break
                
                window_obj.game_logic.start_game()
                
                # Reconnect callbacks
                def on_state_changed(state):
                    if window_obj.dashboard:
                        window_obj.dashboard.update_stats(
                            money=state["money"],
                            reputation=state["reputation"],
                            aircraft_count=state["aircraft_count"],
                            active_flights=state["active_flights"],
                            fuel_percent=100.0,
                        )
                def on_flight_completed(flight):
                    if window_obj.status_panel:
                        window_obj.status_panel.add_event(f"✈ Flug {flight.flight_number} abgeschlossen!")
                def on_event(message):
                    if window_obj.status_panel:
                        window_obj.status_panel.add_event(message)
                window_obj.game_logic.set_callbacks(
                    on_state_changed=on_state_changed,
                    on_flight_completed=on_flight_completed,
                    on_event=on_event,
                )
                
                # Reconnect control panel
                connect_control_panel(window_obj)
                
                # Clear status panel
                window_obj.status_panel.clear_flights()
                
                window_obj.stack.setCurrentWidget(window_obj.game_screen)
                window_obj.status_panel.add_event(f"🎮 Neues Spiel: {settings['game_name']} ({settings['airport_name']})")
                window_obj.status_panel.add_event("Willkommen! Kaufen Sie Ihr erstes Flugzeug oder planen Sie einen Flug.")

        def load_game(window_obj: UIManager) -> None:
            """Lädt einen Spielstand."""
            dialog = LoadGameDialog(window_obj)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                filepath = dialog.get_selected_save()
                if filepath and window_obj.game_logic.load_game(filepath):
                    window_obj.status_panel.add_event(f"💾 Spielstand geladen: {os.path.basename(filepath)}")
                    window_obj.stack.setCurrentWidget(window_obj.game_screen)
                else:
                    QMessageBox.warning(window_obj, "Laden fehlgeschlagen", "Spielstand konnte nicht geladen werden!")

        def save_game(window_obj: UIManager) -> None:
            """Speichert das aktuelle Spiel."""
            dialog = QDialog(window_obj)
            dialog.setWindowTitle("Spiel speichern")
            dialog.setMinimumWidth(400)
            dialog.setStyleSheet("""
                QDialog { background-color: #1a1a2e; color: white; }
                QLabel { color: #e0e0e0; font-size: 13px; }
                QComboBox { background-color: #16213e; color: white; border: 1px solid #0f3460; 
                           border-radius: 4px; padding: 8px; }
                QPushButton { background-color: #e94560; color: white; border: none; 
                             padding: 10px 20px; border-radius: 4px; font-weight: bold; }
                QPushButton:hover { background-color: #d63850; }
            """)
            
            layout = QFormLayout(dialog)
            layout.setSpacing(15)
            layout.setContentsMargins(25, 25, 25, 25)
            
            combo = QComboBox()
            for i in range(1, SAVE_SLOTS + 1):
                filepath = os.path.join(SAVE_DIR, f"save_slot_{i}.json")
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        game_name = data.get("game_name", f"Slot {i}")
                        save_time = data.get("save_time", "")
                        try:
                            dt = datetime.fromisoformat(save_time.replace('Z', '+00:00'))
                            time_str = dt.strftime("%d.%m.%Y %H:%M")
                        except:
                            time_str = save_time
                        combo.addItem(f"Slot {i}: {game_name} ({time_str})", i)
                    except:
                        combo.addItem(f"Slot {i}: [Fehlerhaft]", i)
                else:
                    combo.addItem(f"Slot {i}: 📭 Leer", i)
            
            layout.addRow("Speicherslot:", combo)
            
            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Speichern")
            buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
            layout.addRow("", buttons)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                slot = combo.currentData() + 1
                filepath = os.path.join(SAVE_DIR, f"save_slot_{slot}.json")
                # Füge Metadaten hinzu
                state = window_obj.game_logic.get_game_state()
                save_data = {
                    "game_name": window_obj.game_logic.player.name,
                    "airport_name": window_obj.game_logic.airport.name,
                    "save_time": datetime.now().isoformat(),
                    "player": window_obj.game_logic.player.to_dict(),
                    "airport": window_obj.game_logic.airport.to_dict(),
                    "aircraft": [a.to_dict() for a in window_obj.game_logic.aircraft],
                    "flights": [f.to_dict() for f in window_obj.game_logic.flights],
                }
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(save_data, f, indent=2)
                    window_obj.status_panel.add_event(f"💾 Spiel gespeichert in Slot {slot}")
                except Exception as e:
                    QMessageBox.warning(window_obj, "Speichern fehlgeschlagen", f"Fehler: {e}")

        def show_menu() -> None:
            """Zeigt das Hauptmenü an - mit Bestätigung falls im Spiel."""
            if window.stack.currentWidget() == window.game_screen:
                # Stoppe Game Timer
                if window.game_timer:
                    window.game_timer.stop()
                # Stoppe Musik
                if window.background_music:
                    window.background_music.stop()
                
                reply = QMessageBox.question(
                    window, "Zum Hauptmenü",
                    "Möchten Sie wirklich zum Hauptmenü zurückkehren?\n"
                    "Der aktuelle Spielstand wird nicht automatisch gespeichert!",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    # Resume game
                    if window.game_timer:
                        window.game_timer.start(100)
                    if window.background_music:
                        window.background_music.play()
                    return
            
            window.menu_screen.update_translations()
            window.bg_widget.setGraphicsEffect(None)
            window.stack.setCurrentWidget(window.menu_screen)

        def show_settings() -> None:
            window.settings_screen.update_translations()
            blur = QGraphicsBlurEffect()
            blur.setBlurRadius(18)
            window.bg_widget.setGraphicsEffect(blur)
            window.stack.setCurrentWidget(window.settings_screen)

        def show_placeholder(window_obj: UIManager, text: str) -> None:
            window_obj.placeholder_label.setText(text)
            window_obj.stack.setCurrentWidget(window_obj.placeholder_screen)

        timer = QTimer()
        timer.timeout.connect(show_main_ui)
        timer.start(100)

        return window
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")
        import traceback
        traceback.print_exc()
        raise