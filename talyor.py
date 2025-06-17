import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M_earth = 5.972e24  # Mass of Earth (kg)
M_moon = 7.348e22   # Mass of Moon (kg)
R_earth = 6371e3  # Radius of Earth (m)
R_moon = 1737e3   # Radius of Moon (m)
T_moon = 27.32 * 24 * 3600  # Moon's orbital period (seconds)
earth_moon_distance = 384400e3  # Average distance from Earth to Moon (m)

# Orbital radius of the Earth around the barycenter
orbital_radius_earth_barycenter = (M_moon / (M_earth + M_moon)) * earth_moon_distance  
# Orbital radius of the Moon around the barycenter
orbital_radius_moon_barycenter = earth_moon_distance - orbital_radius_earth_barycenter  
# Both bodies orbit barycenter with this angular speed...
omega_barycenter = 2 * np.pi / T_moon
omega_earth_barycenter = omega_barycenter
omega_moon_barycenter = omega_barycenter

def polar_to_cartesian(r, theta):
    """Convert polar (r, theta) coordinates to Cartesian (x, y)."""
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

# Initialize the simulation parameters    
x0 = np.array([R_earth + 400e3, 0])  # 400 km above Earth surface
v0 = np.array(polar_to_cartesian(8.3e3, 3*np.pi/16))  # Translunar Injection velocity (m/s)

# Time step and number of steps
dt = 100  # Time step in seconds (recommend 100)
steps = 5000  # Number of simulation steps (recommend 2000)
# This code simulates a spacecraft trajectory in the Earth-Moon system using the Restricted Three-Body Problem (RTBP) with moving Earth and Moon.
# The spacecraft is launched from the surface of the Earth with a specified initial velocity.
# The simulation accounts for the gravitational forces exerted by both Earth and Moon, and it checks for potential collisions with either body.
# The trajectory is computed using a Taylor series approximation method, and the results are visualized in a plot.

def earth_position(t):
    """Compute Earth's position relative to the barycenter (antiphase to Moon)."""
    x_earth = orbital_radius_earth_barycenter * np.cos(omega_barycenter * t + np.pi)
    y_earth = orbital_radius_earth_barycenter * np.sin(omega_barycenter * t + np.pi)
    return np.array([x_earth, y_earth])

def moon_position(t):
    """Compute Moon's position relative to the barycenter."""
    x_moon = orbital_radius_moon_barycenter * np.cos(omega_barycenter * t)
    y_moon = orbital_radius_moon_barycenter * np.sin(omega_barycenter * t)
    return np.array([x_moon, y_moon])

def gravitational_acceleration(pos, t):
    """Calculate gravitational acceleration due to moving Earth and Moon."""
    r_earth = pos - earth_position(t)
    r_moon = pos - moon_position(t)
    a_earth = -G * M_earth / np.linalg.norm(r_earth)**3 * r_earth
    a_moon = -G * M_moon / np.linalg.norm(r_moon)**3 * r_moon
    return a_earth + a_moon

def taylor_series_rtbp_collision(x0, v0, dt, steps):
    """Approximates spacecraft trajectory with moving Earth & Moon."""
    trajectory = [x0]
    pos = x0
    vel = v0

    for step in range(steps):
        t = step * dt
        acc = gravitational_acceleration(pos, t)
        pos = pos + vel * dt + acc * (dt**2) / 2
        vel = vel + acc * dt

        # Collision Detection
        # TODO: calculate closing speed at impact
        if np.linalg.norm(pos - earth_position(t)) < R_earth :
            print("Trajectory terminated due to collision with Earth.")
            break
        if np.linalg.norm(pos - moon_position(t)) < R_moon:
            print("Trajectory terminated due to collision with Moon.")  
            break   

        trajectory.append(pos)

    return np.array(trajectory)

# Simulating Trajectory
trajectory = taylor_series_rtbp_collision( x0, v0, dt, steps)

# Plotting results
plt.figure(figsize=(10, 8))
plt.plot(trajectory[:, 0] / 1e3, trajectory[:, 1] / 1e3, label="Spacecraft Trajectory", color="blue")
plt.plot(0 , 0, label="origin", color="red",  marker='+', markersize=10)  # Barycenter

# Plot dynamically moving Earth & Moon positions
plt.scatter(*earth_position(steps * dt) / 1e3, color="green", label="Final Earth Position", s=np.pi*(R_earth / 1e6)**2)
plt.scatter(*moon_position(steps * dt) / 1e3, color="gray", label="Final Moon Position", s=np.pi*(R_moon / 1e6)**2)

plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("RTBP Spacecraft Trajectory (Earth-Moon Barycenter Motion)")
plt.legend()
plt.grid()
plt.axis('equal')
plt.show()

# Plot Earth and Moon positions over time
"""
times = np.arange(0, steps * dt, dt)
earth_positions = np.array([10*earth_position(t) for t in times])
moon_positions = np.array([moon_position(t) for t in times])
"""

"""
plt.figure(figsize=(12, 6))
plt.plot(times / 86400, earth_positions[:, 0] / 1e3, label="Earth X (km)", color="green")
plt.plot(times / 86400, earth_positions[:, 1] / 1e3, label="Earth Y (km)", color="lime")
plt.plot(times / 86400, moon_positions[:, 0] / 1e3, label="Moon X (km)", color="gray")
plt.plot(times / 86400, moon_positions[:, 1] / 1e3, label="Moon Y (km)", color="black")
plt.xlabel("Time (days)")
plt.ylabel("Log Position (km)")
plt.title("Earth and Moon Positions vs Time (Barycenter Frame)")
plt.legend()
plt.grid()
plt.show() 
"""

# 2D plot of Earth and Moon positions (barycenter frame)
"""plt.figure(figsize=(8, 8))
plt.plot(earth_positions[:, 0] / 1e3, earth_positions[:, 1] / 1e3, label="Earth Orbit", color="green")
plt.plot(moon_positions[:, 0] / 1e3, moon_positions[:, 1] / 1e3, label="Moon Orbit", color="gray")
plt.scatter(0, 0, color="red", label="Barycenter", marker="+", s=100)
plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("Earth and Moon Orbits in Barycenter Frame")
plt.legend()
plt.axis('equal')
plt.grid()
plt.show()
"""