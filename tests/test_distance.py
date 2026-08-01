"""Tests for distance calculations."""

from fleet_sim.distance import manhattan_distance


def test_manhattan_distance() -> None:
    distance = manhattan_distance(0, 0, 7, 6)

    assert distance == 13


def test_manhattan_distance_with_negative_coordinates() -> None:
    distance = manhattan_distance(-2, -3, 4, 5)

    assert distance == 14
