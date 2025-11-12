import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib import animation


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
    """ Compute acceleration of spacecraft due to Earth and Moon gravity."""
    pos = state[:2]
    vel = state[2:]
    r_earth = pos - earth_position(t)
    r_moon = pos - moon_position(t)
    a_earth = -G * M_earth / np.linalg.norm(r_earth)**3 * r_earth
    a_moon = -G * M_moon / np.linalg.norm(r_moon)**3 * r_moon
    return np.concatenate((vel, a_earth + a_moon))

# --- shared drawing helper ---
def _setup_axes(trajectory, title="Trajectory"):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(np.min(trajectory[:,0]) / 1e3 - 5000,
                np.max(trajectory[:,0]) / 1e3 + 5000)
    ax.set_ylim(np.min(trajectory[:,1]) / 1e3 - 5000,
                np.max(trajectory[:,1]) / 1e3 + 5000)
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_title(title)
    ax.grid()
    return fig, ax

def _draw_static(ax, trajectory, t_vals, earth_position, moon_position,
                 collided=None, closest_point=None):
    # spacecraft path
    ax.plot(trajectory[:, 0] / 1e3, trajectory[:, 1] / 1e3,
            label="Spacecraft", c='blue')

    # Earth & Moon paths
    earth_positions = np.array([earth_position(t) for t in t_vals])
    moon_positions  = np.array([moon_position(t) for t in t_vals])
    ax.plot(earth_positions[:, 0] / 1e3, earth_positions[:, 1] / 1e3,
            label="Earth", c='green')
    ax.plot(moon_positions[:, 0] / 1e3, moon_positions[:, 1] / 1e3,
            label="Moon", c='gray')

    # closest approach marker
    if closest_point is not None:
        ax.scatter([closest_point[0] / 1e3],
                   [closest_point[1] / 1e3],
                   color='red', label="Closest Approach", zorder=5)

    if collided:
        ax.set_title(f"Trajectory terminated by collision with {collided}")

    ax.axis('equal')
    ax.legend()
    plt.tight_layout()
    plt.show()

def _animate(ax, trajectory, t_vals, earth_position, moon_position):
    sc_line, = ax.plot([], [], 'b-', label='Spacecraft Trajectory')
    sc_dot,  = ax.plot([], [], 'bo', markersize=4)
    earth_dot, = ax.plot([], [], 'go', label='Earth')
    moon_dot,  = ax.plot([], [], 'ko', label='Moon')
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
        moon  = moon_position(t_vals[frame]) / 1e3
        earth_dot.set_data(*earth)
        moon_dot.set_data(*moon)
        return sc_line, sc_dot, earth_dot, moon_dot

    ani = animation.FuncAnimation(ax.figure, update,
                                  frames=len(t_vals),
                                  init_func=init,
                                  blit=True,
                                  interval=20)
    return ani


def simulate_transfer(x0, v0, t_max, dt, mode="static", save_path=None):
    """
    Simulate an Earth–Moon transfer trajectory, detect collisions, and visualize the result.

        Initial position vector [m].
        Initial velocity vector [m/s].
        Time step for integration [s].
    mode : {"none", "static", "animate"}, optional
        Visualization mode: "none" for no plot, "static" for a static plot, "animate" for an animation (default: "static").
    save_path : str or None, optional
        If mode is "animate" and this is provided, save the animation to this file path (supports ".mp4" or ".gif").

    Returns
    -------
    dict
        Summary of the simulation outcome:
            - If a collision occurs: {"outcome": "collision", "body": <"Earth" or "Moon">, "time": <collision_time>}
            - If no collision: {
                "nearest_approach_km": <minimum distance to Moon in km>,
                "closest_point_km": <coordinates of closest approach in km>,
                "end_time_s": <final simulation time in seconds>

    Notes
    -----
    - The function integrates the equations of motion using `solve_ivp` and checks for collisions with Earth or Moon.
    - Visualization is handled according to the `mode` parameter.
    """
    
    state0 = np.concatenate((x0, v0))
    t_eval = np.arange(0, t_max, dt)
    sol = solve_ivp(acceleration, (0, t_max), state0,
                    t_eval=t_eval, rtol=1e-8, atol=1e-8)

    trajectory = sol.y[:2, :].T
    t_vals = sol.t

    # --- collision / closest approach logic ---
    min_dist = float('inf')
    closest_point = trajectory[0]

    for i, t in enumerate(t_vals):
        pos = trajectory[i]
        r_e = np.linalg.norm(pos - earth_position(t))
        r_m = np.linalg.norm(pos - moon_position(t))

        if r_e < R_earth:
            if mode == "static":
                fig, ax = _setup_axes(trajectory, "Collision with Earth")
                _draw_static(ax, trajectory, t_vals,
                             earth_position, moon_position,
                             collided="Earth")
            return {"outcome": "collision", "body": "Earth", "time": t}

        if r_m < R_moon:
            if mode == "static":
                fig, ax = _setup_axes(trajectory, "Collision with Moon")
                _draw_static(ax, trajectory, t_vals,
                             earth_position, moon_position,
                             collided="Moon")
            return {"outcome": "collision", "body": "Moon", "time": t}

        if r_m < min_dist:
            min_dist = r_m
            closest_point = pos

    # --- visualization ---
    if mode == "static":
        fig, ax = _setup_axes(trajectory, "Earth–Moon Transfer")
        _draw_static(ax, trajectory, t_vals,
                     earth_position, moon_position,
                     closest_point=closest_point)

    elif mode == "animate":
        fig, ax = _setup_axes(trajectory, "Earth–Moon Transfer (Animation)")
        ani = _animate(ax, trajectory, t_vals, earth_position, moon_position)

        if save_path:
            if save_path.endswith(".mp4"):
                ani.save(save_path, writer="ffmpeg", fps=30)
            elif save_path.endswith(".gif"):
                ani.save(save_path, writer="pillow", fps=30)
            else:
                raise ValueError("save_path must end with .mp4 or .gif")
        else:
            plt.show()

    # --- return summary ---
    return {
        "outcome": "complete",
        "nearest_approach_km": min_dist / 1e3,
        "closest_point_km": closest_point / 1e3,
        "end_time_s": t_vals[-1]
    }






