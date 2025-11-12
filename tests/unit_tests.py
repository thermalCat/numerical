# tests/unit_tests.py
from ..src.simulate_earth_moon_transfer import moon_position, earth_position, acceleration
import numpy as np  

T_moon = 27.321661 * 24 * 3600

def test_moon_period():
    assert np.allclose( moon_position(0), moon_position(T_moon)), "Moon position should repeat after one orbital period"

def test_earth_period():
    assert np.allclose( earth_position(0), earth_position(T_moon)), "Earth position should repeat after one lunar orbital period"

def test_positions_opposite():
    moon_pos_start = moon_position(0)
    moon_pos_half = moon_position(T_moon/2)
    assert np.allclose(moon_pos_start, -moon_pos_half), "Moon should be on opposite sides of Barycentre after half its orbital period"

def test_acceleration_magnitude():
    state = np.array([1e7, 0, 0, 0])  # position far from Earth and Moon
    acc = acceleration(0, state)
    acc_magnitude = np.linalg.norm(acc[2:])
    assert acc_magnitude < 1e-5, "Acceleration should be small when far from Earth and Moon"

def test_acceleration_direction():
    state = np.array([6371e3 + 1000, 0, 0, 0])  # position just above Earth's surface
    acc = acceleration(0, state)
    acc_vector = acc[2:]
    expected_direction = -state[:2] / np.linalg.norm(state[:2])
    acc_direction = acc_vector / np.linalg.norm(acc_vector)
    assert np.allclose(acc_direction, expected_direction), "Acceleration should point towards Earth when close to it"