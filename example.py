import simulate_earth_moon_transfer as st
import numpy as np

#example usage
x0 = np.array([st.R_earth + 400e3, 0])       # 400 km LEO
v0 = np.array([7.9e3, 2.5e3])                # TLI velocity
st.simulate_transfer(x0, v0, t_max=5*24*3600, dt=100)