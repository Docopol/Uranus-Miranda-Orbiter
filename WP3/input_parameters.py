import numpy as np

g_param = 5.793939 * 1e6  # [km^3/s^2] Gravitational Parameter
r_uranus = 25170  # [km] Radius of Uranus
rho = 8.417 * 1e-13  # [km/m^3] Density at orbit height
P_s = 2.468 * 1e-8  # [N/m^2] Solar pressure around Uranus

# # # required parameters # # #

m_cylinder = 157.8  # [kg] mass of structure
r_cylinder = 1.8  # [m] radius of circular cylinder
h_cylinder = 8.235  # [m] length of cylinder
r_orbit = 4343  # [km] Altitude of circular orbit
a_orbit = 2 * (r_uranus + r_orbit)  # Semi Major Axis of orbit
v_orbit = np.sqrt(g_param / (r_orbit + r_uranus)) * 1e3  # [m/s] Orbital velocity
t_orbit = 2 * np.pi * np.sqrt(np.power(a_orbit, 3, dtype="int64") / g_param)  # orbital time period
t_mission = 4*365.25*24*3600
a = 1.378  # [m] side length of octagon
s_proj = a * (1 + np.sqrt(2))  # projected side length
I = np.array([(0.345 * m_cylinder * r_cylinder ** 4) / (a * r_cylinder), 0, 0])  # [kg*m^2] Moment of Inertia along x axis

# # # masses # # #

masses_init = {"Mass of System": [0, 0, 0, 1517.24],  # [kg] x, y, z, mass
               "Mass of Fuel": [0.702, 0, 0, 180.73 * 1.2]}

masses_fin = {"Mass of System": [0, 0, 0, 1517.24],  # [kg] x, y, z, mass
              "Mass of Fuel": [0.702, 0, 0, (180.73 * (1 - 1 / 1.02) * 1.2)]}  # removing 2% residual

# # # areas # # #

areas = {"Area1": [0, 0, 0, 1],  # [m^2] x, y, z, area
         "Area2": [0, 1, 0, 1]}

# # # Disturbance Torques # # #

n_sq = (g_param / (r_orbit + r_uranus) ** 3)  # [rad/s]parameter for Gravity torque

C_d = 2.6  # [-] drag coefficient for Aerodynamic torque
S = [9.17, s_proj * h_cylinder, s_proj * h_cylinder]  # [m^2] surface area for Aerodynamic torque

rho_r = 0.84  # [-] reflectivity of sail for solar radiation torque
S_eff = 28.8  # [m^2] effective area of of the S/C for solar radiation torque

M_d = 0.1  # [A*m^2] residual magnetic dipole
B = 1e-5  # [N*m] intensity of magnetic field
