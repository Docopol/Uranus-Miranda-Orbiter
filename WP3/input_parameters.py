# # # natural constants # # #
import numpy as np
g_param = 5.793939 * 1e6    # [km^3/s^2] Gravitational Parameter
r_uranus = 25362            # [km] Radius of Uranus
rho = 8.417 * 1e-13         # [km/m^3] Density at orbit height
P_s = 2.468 * 1e-8          # [N/m^2] Solar pressure around Uranus

# # # required parameters # # #

r_cylinder = 1.8            # [m] radius of circular cylinder
len_cylinder = 8            # [m] length of cylinder
r_orbit = 4343              # [km] Radius of circular orbit
v_orbit = np.sqrt(g_param/(r_orbit+r_uranus))             # [m/s] Orbital velocity

# # # masses # # #

masses = {"Mass1": [0, 0, 0, 1],                    # [kg] x, y, z, mass
          "Mass2": [0, 1, 0, 1]}


# # # areas # # #

areas = {"Area1": [0, 0, 0, 1],                     # [m^2] x, y, z, area
         "Area2": [0, 1, 0, 1]}

# # # Disturbance Torques # # #

n_sq = (g_param / (r_orbit + r_uranus) ** 3)        # [rad/s]parameter for Gravity torque

C_d = 2.6                                           # [-] drag coefficient for Aerodynamic torque
S = [0, 0, 0]                                       # [m^2] surface area for Aerodynamic torque

rho_r = 0.84                                        # [-] reflectivity of sail for solar radiation torque
S_eff = 28.8                                        # [m^2] effective area of of the S/C for solar radiation torque

M_d = 0.1
