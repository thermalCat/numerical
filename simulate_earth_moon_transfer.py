import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constants
G = 6.67430e-11
M_earth = 5.972e24
M_moon = 7.348e22
R_earth = 6371e3
R_moon = 1737e3
EARTH_MOON_DISTANCE = 384400e3  # Average distance from Earth to Moon (m)
T_moon = 27.32 * 24 * 3600
omega_moon = 2 * np.pi / T_moon
barycenter_offset = (M_moon / (M_earth + M_moon)) * EARTH_MOON_DISTANCE


def earth_position(t):
    r = -barycenter_offset
    return np.array([r * np.cos(omega_moon * t), r * np.sin(omega_moon * t)])

def moon_position(t):
    r = EARTH_MOON_DISTANCE - barycenter_offset
    return np.array([r * np.cos(omega_moon * t), r * np.sin(omega_moon * t)])

def acceleration(t, state):
    pos = state[:2]
    vel = state[2:]
    r_earth = pos - earth_position(t)
    r_moon = pos - moon_position(t)
    a_earth = -G * M_earth / np.linalg.norm(r_earth)**3 * r_earth
    a_moon = -G * M_moon / np.linalg.norm(r_moon)**3 * r_moon
    return np.concatenate((vel, a_earth + a_moon))

def simulate_transfer(x0, v0, t_max, dt, plot=True):
    state0 = np.concatenate((x0, v0))
    t_eval = np.arange(0, t_max, dt)
    sol = solve_ivp(acceleration, (0, t_max), state0, t_eval=t_eval, rtol=1e-8, atol=1e-8)

    trajectory = sol.y[:2, :].T
    t_vals = sol.t

    min_dist = float('inf')
    closest_point = closest_point = trajectory[0]

    for i, t in enumerate(t_vals):
        pos = trajectory[i]
        r_e = np.linalg.norm(pos - earth_position(t))
        r_m = np.linalg.norm(pos - moon_position(t))

        if r_e < R_earth:
            if plot:
                _plot_sim(trajectory, t_vals, t_max, collided="Earth")
            return {"outcome": "collision", "body": "Earth", "time": t}
        if r_m < R_moon:
            if plot:
                _plot_sim(trajectory, t_vals, t_max, collided="Moon")
            return {"outcome": "collision", "body": "Moon", "time": t}

        if r_m < min_dist:
            min_dist = r_m
            closest_point = pos

    if plot:
#   static graph of simulation result
#         _plot_sim(trajectory, t_vals, t_max, closest_point=closest_point)
#   animation of simulation result
        animate_trajectory(trajectory, t_vals)

    return {
        "outcome": "complete",
        "nearest_approach_km": min_dist / 1e3,
        "closest_point_km": closest_point / 1e3,
        "end_time_s": t_vals[-1]
    }

def _plot_sim(trajectory, t_vals, t_max, collided=None, closest_point=None):
    moon_positions = np.array([moon_position(t) for t in t_vals])
    earth_positions = np.array([earth_position(t) for t in t_vals])

    plt.figure(figsize=(10, 8))
    plt.plot(trajectory[:, 0] / 1e3, trajectory[:, 1] / 1e3, label="Spacecraft", c='blue')
    plt.plot(earth_positions[:, 0] / 1e3, earth_positions[:, 1] / 1e3, label="Earth", c='green')
    plt.plot(moon_positions[:, 0] / 1e3, moon_positions[:, 1] / 1e3, label="Moon", c='gray')

    if closest_point is not None:
        plt.scatter(*closest_point / 1e3, color='red', label="Closest Approach", zorder=5)

    if collided:
        plt.title(f"Trajectory terminated by collision with {collided}")
    else:
        plt.title("Simulated Earth-Moon Transfer Trajectory")

    plt.xlabel("X position (km)")
    plt.ylabel("Y position (km)")
    plt.axis('equal')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


import matplotlib.animation as animation

def animate_trajectory(trajectory, t_vals):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(np.min(trajectory[:,0]) / 1e3 - 5000, np.max(trajectory[:,0]) / 1e3 + 5000)
    ax.set_ylim(np.min(trajectory[:,1]) / 1e3 - 5000, np.max(trajectory[:,1]) / 1e3 + 5000)
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_title("Live Earth-Moon Transfer Simulation")
    ax.grid()
    
    sc_line, = ax.plot([], [], 'b-', label='Spacecraft Trajectory')
    sc_dot, = ax.plot([], [], 'bo', markersize=4)
    earth_dot, = ax.plot([], [], 'go', label='Earth')
    moon_dot, = ax.plot([], [], 'ko', label='Moon')

    ax.legend()

    def init():
        sc_line.set_data([], [])
        sc_dot.set_data([], [])
        earth_dot.set_data([], [])
        moon_dot.set_data([], [])
        return sc_line, sc_dot, earth_dot, moon_dot

    def update(frame):
        x = trajectory[:frame+1, 0] / 1e3
        y = trajectory[:frame+1, 1] / 1e3
        sc_line.set_data(x, y)
        sc_dot.set_data(x[-1], y[-1])
        earth = earth_position(t_vals[frame]) / 1e3
        moon = moon_position(t_vals[frame]) / 1e3
        earth_dot.set_data(*earth)
        moon_dot.set_data(*moon)
        return sc_line, sc_dot, earth_dot, moon_dot

    ani = animation.FuncAnimation(fig, update, frames=len(t_vals),
                                  init_func=init, blit=True, interval=20)
    plt.show()

