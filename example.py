import src.simulate_earth_moon_transfer as st
import numpy as np

#example usage
x0 = np.array([st.R_earth + 400e3, 0])       # 400 km Low Earth Orbit
v0 = np.array([7.9e3, 2.5e3])                # Trans Lunar Injection velocity
"""
# No plotting, just run the sim
result = st.simulate_transfer(x0, v0, t_max=5*24*3600, dt=100, mode="none")
"""

# Static plot
result = st.simulate_transfer(x0, v0, t_max=5*24*3600, dt=100, mode="static")
"""
# Animated trajectory
result = st.simulate_transfer(x0, v0, t_max=5*24*3600, dt=100, mode="animate")


# Save as MP4
result = st.simulate_transfer(x0, v0, t_max=5*24*3600, dt=100, mode="animate", save_path="transfer.mp4")

# Save as GIF
result = st.simulate_transfer(x0, v0, t_max=5*24*3600, dt=100, mode="animate", save_path="transfer.gif")
"""
