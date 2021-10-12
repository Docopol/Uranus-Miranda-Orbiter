import numpy as np
import math as m

g_param = 5.793939 * 1e6  # [km^3/s^2] Gravitational Parameter
r_uranus = 25265.0  # [km] Mission radius of Uranus = average between polar and equatorial radius
rho = 8.417 * 1e-13  # [kg/m^3] Density at orbit height
P_s = 2.468 * 1e-8  # [N/m^2] Solar pressure around Uranus

# # # Mission parameters # # #

t_mission_yr = 4  # Years in mission
t_mission = t_mission_yr * 365.25 * 24 * 3600

# # # Orbit parameters # # #

h_orbit = 4343.0  # [km] Altitude of circular orbit
a_orbit = r_uranus + h_orbit  # [km] Semi Major Axis of orbit = Radius of circular orbit
v_orbit = m.sqrt(g_param / a_orbit) * 1e3  # [m/s] Orbital velocity
t_orbit = 2 * np.pi * m.sqrt(np.power(a_orbit, 3, dtype="float64") / g_param)  # [s] orbital time period
n_sq = g_param / np.power(a_orbit, 3, dtype="float64")  # [1/s^2] parameter for Gravity torque
n_orbits = t_mission/t_orbit

# # # Magnetic parameters # # #

l_constant = 1 + np.sin((90-58.6) * np.pi/180)  # Approximation, Range: [1-2] (min at equator and max at poles)
M_earth = 7.8 * 1e15  # [A/m^2] Magnetic dipole moment Earth [SMAD]
M_uranus = 50 * M_earth  # [A/m^2] Magnetic dipole moment Uranus [Spacecraft Systems Engineering]
B_uranus = M_uranus/(np.power(a_orbit*1000, 3, dtype="float64")) * l_constant  # [A/m^2] Magnetic field Uranus [SMAD]

# # # SC parameters # # #

m_dry_SC = 1517.24  # [kg] mass of structure
r_cylinder = 1.8  # [m] radius of circular cylinder
h_cylinder = 8.235  # [m] length of cylinder
a = 1.378  # [m] side length of octagon
s_proj = a * (1 + m.sqrt(2))  # projected side length

masses_init = [[0, 0, 0, 1517.24],  # System  # [kg] x, y, z, mass
               [0.702, 0, 0, 180.73 * 1.2]]  # Fuel

masses_fin = [[0.02, 0.02, 0.02, 1517.24],  # System  # [kg] x, y, z, mass
              [0.702, 0, 0, (180.73 * (1 - 1 / 1.02) * 1.2)]]  # Fuel  # removing 2% residual

V_proptank = 182.69 * 1e-3
r_proptank = np.cbrt(V_proptank/(4/3*np.pi))
m_proptank_av = (180.73 * 1.2 + 180.73 * (1 - 1 / 1.02) * 1.2) / 2
r_to_COM = 0.702

I_xx = (0.345 * m_dry_SC * np.power(r_cylinder, 4)) / (a * r_cylinder)
I_yy = 1/4 * m_dry_SC * np.square(r_cylinder) + 1/12 * m_dry_SC * np.square(h_cylinder) + 2/5 * m_proptank_av * np.square(r_proptank) + m_proptank_av * np.square(r_to_COM)
I_zz = I_yy
I_SC = np.array([I_xx, I_yy, I_zz])  # [kg*m^2] Moment of Inertia along x axis

areas = {"Area1": [0, 0, 0, 1],  # [m^2] x, y, z, area
         "Area2": [0, 1, 0, 1]}

# # # Disturbance Torques # # #

C_d = 2.6  # [-] drag coefficient for Aerodynamic torque
S = np.array([9.17, s_proj * h_cylinder, s_proj * h_cylinder])  # [m^2] surface area for Aerodynamic torque

rho_opt = 0.84  # [-] reflectivity of sail for solar radiation torque
S_eff = 28.8  # [m^2] effective area of of the S/C for solar radiation torque

D = 0.1  # [A*m^2] residual magnetic dipole [ADSEE READER]

# # # Uncertainties # # #

theta_misalignment = np.pi/180  # 1 deg
phi_misalignment = np.pi/180  # 1 deg
CG_uncertainty = 0.02  # 2cm is uncertainty SMAD[p. 574]
angle_thrust_misalignment = 0.3 * np.pi/180  # 0.3 deg

arm_thrust_misalignment = h_cylinder/2 * np.sin(angle_thrust_misalignment)  # from geometric center in both y and z-axis

# # # ADCS # # #


# # # Other # # #

thrust_mainengine = 560  # N (WP2)
burn_time_mainengine = 1048.74  # s (WP2)

