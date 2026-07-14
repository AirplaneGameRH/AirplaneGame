from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.entities import Aircraft, Airport, Flight, Player


def test_aircraft_defaults_and_serialization() -> None:
    aircraft = Aircraft(name="A320", fuel=1000, passenger_capacity=180)

    assert aircraft.name == "A320"
    assert aircraft.fuel == 1000
    assert aircraft.passenger_capacity == 180
    assert aircraft.status == "parked"

    payload = aircraft.to_dict()
    assert payload["name"] == "A320"
    assert payload["fuel"] == 1000


def test_aircraft_refuel_and_repair() -> None:
    aircraft = Aircraft(name="A320", fuel=500, max_fuel=1000, condition=50.0)
    
    # Test refuel
    aircraft.refuel(300)
    assert aircraft.fuel == 800
    aircraft.refuel()  # full refuel
    assert aircraft.fuel == 1000
    
    # Test repair
    aircraft.repair()
    assert aircraft.condition == 100.0
    assert aircraft.maintenance_level == 100.0
    
    # Test start_flight and land
    aircraft.start_flight("BER")
    assert aircraft.status == "in_flight"
    assert aircraft.current_flight == "BER"
    
    aircraft.land()
    assert aircraft.status == "landed"
    
    # Test maintenance
    aircraft.enter_maintenance()
    assert aircraft.status == "maintenance"


def test_airport_and_player_state() -> None:
    airport = Airport(name="MUC", gates=5, runways=2)
    player = Player(name="Player 1", money=5000, reputation=10)

    airport.add_aircraft("A320")
    player.add_aircraft("A320")

    assert airport.name == "MUC"
    assert airport.gates == 5
    assert airport.runways == 2
    assert airport.to_dict()["status"] == "open"

    assert player.name == "Player 1"
    assert player.money == 5000
    assert player.reputation == 10
    assert player.to_dict()["money"] == 5000


def test_player_money_and_fleet() -> None:
    player = Player(money=10000)
    
    player.add_money(5000)
    assert player.money == 15000
    
    player.spend_money(3000)
    assert player.money == 12000
    
    # Can't go below 0
    player.spend_money(20000)
    assert player.money == 0


def test_flight_assignment_and_serialization() -> None:
    aircraft = Aircraft(name="B737")
    flight = Flight(flight_number="LH123", destination="BER")

    flight.assign_aircraft(aircraft)

    assert flight.flight_number == "LH123"
    assert flight.destination == "BER"
    assert flight.aircraft is aircraft
    assert flight.to_dict()["destination"] == "BER"


def test_flight_lifecycle() -> None:
    aircraft = Aircraft(name="A320", fuel=1000, max_fuel=1000)
    flight = Flight(
        flight_number="LH123",
        origin="MUC",
        destination="BER",
        aircraft=aircraft,
        passengers=150,
        cargo=500,
        distance=500,
        duration=10.0,  # 10 seconds for test
    )
    
    # Start flight
    flight.start()
    assert flight.status == "in_progress"
    assert aircraft.status == "in_flight"
    
    # Update progress
    flight.update_progress(5.0)  # 50% progress
    assert flight._progress == 0.5
    
    flight.update_progress(5.0)  # 100% progress
    assert flight._progress == 1.0
    assert flight.status == "completed"
    assert aircraft.status == "landed"
    
    # Test revenue/cost calculation
    revenue = flight.calculate_revenue(ticket_price=100.0, cargo_rate=10.0)
    assert revenue == 150 * 100 + 500 * 10  # 15000 + 5000 = 20000
    
    cost = flight.calculate_operating_cost(fuel_cost_per_unit=5.0, maintenance_factor=0.1)
    assert cost > 0


def test_airport_operations() -> None:
    airport = Airport(name="BER", gates=3, runways=2, hangars=2)
    aircraft = Aircraft(name="A320")
    flight = Flight(flight_number="AB123", origin="BER", destination="MUC")
    
    airport.add_aircraft(aircraft)
    assert len(airport.aircraft) == 1
    
    airport.add_flight(flight)
    assert len(airport.flights) == 1
    
    airport.remove_aircraft(aircraft)
    assert len(airport.aircraft) == 0
    
    airport.remove_flight(flight)
    assert len(airport.flights) == 0
    
    airport.open_gate("A1")
    airport.close_gate("A1")
    airport.schedule_maintenance(aircraft)
    airport.update()
