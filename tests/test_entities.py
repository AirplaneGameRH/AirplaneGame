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


def test_flight_assignment_and_serialization() -> None:
    aircraft = Aircraft(name="B737")
    flight = Flight(flight_number="LH123", destination="BER")

    flight.assign_aircraft(aircraft)

    assert flight.flight_number == "LH123"
    assert flight.destination == "BER"
    assert flight.aircraft is aircraft
    assert flight.to_dict()["destination"] == "BER"
