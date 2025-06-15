import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M_earth = 5.972e24  # Mass of Earth (kg)
M_moon = 7.348e22   # Mass of Moon (kg)
R_earth = 6371e3  # Radius of Earth (m)
R_moon = 1737e3   # Radius of Moon (m)
earth_pos = np.array([0, 0])  # Earth at origin
moon_pos = np.array([384400e3, 0])  # Moon's position in meters

# Initial spacecraft conditions
x0 = np.array([0, R_earth+1])  # Initial position in meters
v0 = np.array([7.998e3, 7.997e3])    # Initial velocity in m/s

def gravitational_acceleration(pos):
    """Calculate gravitational acceleration due to Earth and Moon."""
    # the 'r over r cubed' factor preserves the sign of the r vector, 
    # which 1 over r squared would lose
    r_earth = pos - earth_pos
    r_moon = pos - moon_pos
    a_earth = -G * M_earth / np.linalg.norm(r_earth)**3 * r_earth
    a_moon = -G * M_moon / np.linalg.norm(r_moon)**3 * r_moon
    return a_earth + a_moon

def taylor_series_rtbp_collision(x0, v0, dt, steps):
    """Approximates spacecraft trajectory using Taylor series with gravity & collision detection."""
    trajectory = [x0]
    pos = x0
    vel = v0
    
    for _ in range(steps):
        acc = gravitational_acceleration(pos)
        pos = pos + vel * dt + acc * (dt**2) / 2  # Taylor expansion
        vel = vel + acc * dt  # Update velocity
        
        # Collision detection
        if np.linalg.norm(pos - earth_pos) < R_earth :
            print("collision with Earth at speed: ", np.linalg.norm(vel))
            break
        if np.linalg.norm(pos - moon_pos) < R_moon:
            print("collision with Moon at speed: ", np.linalg.norm(vel))
            break
        
        trajectory.append(pos)
    
    return np.array(trajectory)

# Simulating trajectory
dt = 100  # Time step in seconds
steps = 3000  # Number of steps
trajectory = taylor_series_rtbp_collision(x0, v0, dt, steps)

# Plotting results with correct scaling
plt.figure(figsize=(12, 6))
plt.plot(trajectory[:, 0] / 1e3, trajectory[:, 1] / 1e3, label="Spacecraft Trajectory", color="blue")

# Scaling Earth and Moon correctly
plt.scatter(*earth_pos / 1e3, color="green", label="Earth", s=3.1*(R_earth / 1e6)**2)
plt.scatter(*moon_pos / 1e3, color="grey", label="Moon", s=3.1*(R_moon / 1e6)**2)

plt.xlabel("X Position (km)")
plt.ylabel("Y Position (km)")
plt.title("RTBP Spacecraft Trajectory (Correctly Scaled Earth/Moon)")
plt.legend()
plt.grid()
plt.axis('equal')  # Prevent distortion
plt.show()
