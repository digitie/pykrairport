from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from pykrairport import Coordinate, Flight, KrairportModel


def test_response_models_are_pydantic_models() -> None:
    flight = Flight(
        provider="kac",
        airport_code="GMP",
        flight_id="KE1",
        flight_unique_id=None,
        direction="departure",
        airline_name=None,
        airline_code=None,
        departure_airport_code=None,
        arrival_airport_code=None,
        scheduled_at=None,
        estimated_at=None,
        status_korean=None,
        status_english=None,
        terminal=None,
        gate=None,
        codeshare=None,
    )

    assert isinstance(flight, BaseModel)
    assert isinstance(flight, KrairportModel)
    assert flight.provider == "kac"
    assert flight.direction == "departure"
    assert flight.to_dict()["provider"] == "kac"
    assert '"direction":"departure"' in flight.to_json()


def test_response_models_are_frozen_and_validate_fields() -> None:
    flight = Flight(
        provider="iiac",
        airport_code="ICN",
        flight_id="KE1",
        flight_unique_id=None,
        direction="arrival",
        airline_name=None,
        airline_code=None,
        departure_airport_code=None,
        arrival_airport_code=None,
        scheduled_at=None,
        estimated_at=None,
        status_korean=None,
        status_english=None,
        terminal=None,
        gate=None,
        codeshare=None,
    )

    with pytest.raises(ValidationError):
        flight.flight_id = "KE2"
    with pytest.raises(ValidationError):
        Flight(
            provider="unknown",
            airport_code="ICN",
            flight_id="KE1",
            flight_unique_id=None,
            direction="arrival",
            airline_name=None,
            airline_code=None,
            departure_airport_code=None,
            arrival_airport_code=None,
            scheduled_at=None,
            estimated_at=None,
            status_korean=None,
            status_english=None,
            terminal=None,
            gate=None,
            codeshare=None,
        )


def test_coordinate_is_a_frozen_pydantic_model_with_positional_compatibility() -> None:
    coordinate = Coordinate(37.5583, 126.791)

    assert isinstance(coordinate, BaseModel)
    assert coordinate.model_dump(mode="json") == {
        "latitude": 37.5583,
        "longitude": 126.791,
        "datum": "WGS84",
    }
    with pytest.raises(ValidationError):
        coordinate.latitude = 1
    with pytest.raises(ValidationError):
        Coordinate(latitude=91, longitude=126)
