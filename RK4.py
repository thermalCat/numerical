import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M_earth = 5.972e24  # Mass of Earth (kg)
M_moon = 7.348e22   # Mass of Moon (kg)
R_earth = 6371e3  # Radius of Earth (m)
R_moon = 1737e3   # Radius of Moon (m)
T_moon = 27.32 * 24 * 3600  # Moon's orbital period (seconds)
omega_moon = 2 * np.pi / T_moon  # Moon's angular velocity

# Compute barycenter position
barycenter_offset = (M_moon / (M_earth + M_moon)) * 384400e3

def earth_position(t):
    """Compute Earth's position relative to the barycenter."""
    x_earth = -barycenter_offset * np.cos(omega_moon * t)
    y_earth = -barycenter_offset * np.sin(omega_moon * t)
    return np.array([x_earth, y_earth])

def moon_position(t):
    """Compute Moon's position relative to the barycenter."""
    x_moon = (384400e3 - barycenter_offset) * np.cos(omega_moon * t)
    y_moon = (384400e3 - barycenter_offset) * np.sin(omega_moon * t)
    return np.array([x_moon, y_moon])

def acceleration(t, state):
    """Compute gravitational acceleration from Earth and Moon."""
    pos = state[:2]
    r_earth = pos - earth_position(t)
    r_moon = pos - moon_position(t)
    a_earth = -G * M_earth / np.linalg.norm(r_earth)**3 * r_earth
    a_moon = -G * M_moon / np.linalg.norm(r_moon)**3 * r_moon
    return np.concatenate((state[2:], a_earth + a_moon))

# Initial Conditions
x0 = np.array([0, -(R_earth + 400e3)])  # 400 km above Earth surface
v0 = np.array([9.8e3,0])  # Translunar Injection velocity
state0 = np.concatenate((x0, v0))

# Time Span
t_span = (0, 5 * 24 * 3600)  # 5 days
t_eval = np.linspace(*t_span, 1000)

# Solve ODE
solution = solve_ivp(acceleration, t_span, state0, t_eval=t_eval, method='RK45')

# Extract trajectory
trajectory = solution.y[:2].T

# Plotting
plt.figure(figsize=(10, 8))
plt.plot(trajectory[:, 0] / 1e3, trajectory[:, 1] / 1e3, label="Spacecraft Trajectory", color="blue")
plt.scatter(*earth_position(t_span[1]) / 1e3, color="green", label="Final Earth Position", s=(R_earth / 1e6)**2)
plt.scatter(*moon_position(t_span[1]) / 1e3, color="gray", label="Final Moon Position", s=(R_moon / 1e6)**2)

plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("Direct Transfer Trajectory from Earth to Moon")
plt.legend()
plt.grid()
plt.axis('equal')
plt.show()
