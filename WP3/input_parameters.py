import numpy as np
import math as m

g0 = 9.80665
g_param = 5.793939 * 1e6  # [km^3/s^2] Gravitational Parameter  [NASA: Uranus Fact Sheet]
r_uranus = 25265.0  # [km] Radius of Uranus = average between polar and equatorial radius  [NASA: Uranus Fact Sheet]
rho = 8.417 * 1e-13  # [kg/m^3] Density at orbit height  [WP2]
c = 299792458.0  # [m/s] speed of light
J_s_uranus = 3.69  # [W/m^2] Solar pressure around Uranus  [NASA fact sheet]
P_s_uranus = J_s_uranus/c

# # # Mission parameters # # #

t_mission_yr = 4.0  # Years in mission  [WP1]
t_mission = t_mission_yr * 365.25 * 24 * 3600

# # # Orbit parameters # # #

h_orbit = 4343.0  # [km] Altitude of circular orbit  [WP2]
a_orbit = r_uranus + h_orbit  # [km] Semi Major Axis of orbit = Radius of circular orbit

v_orbit = m.sqrt(g_param / a_orbit) * 1e3  # [m/s] Orbital velocity  [WP2]

t_orbit = 2 * np.pi * m.sqrt(np.power(a_orbit, 3, dtype="float64") / g_param)  # [s] orbital time period  [WP2]
ratio_orbit_eclipse = 1/np.pi * np.arcsin(r_uranus/a_orbit)  # Ratio of orbital period vs orbital time
t_orbit_eclipse = ratio_orbit_eclipse * t_orbit  # [s] orbital time period in eclipse  [WP2]
frac_orbit_before_90deg_sun = 0.25 - ratio_orbit_eclipse/2  # fraction of orbit before and after sun and orbit radius have 90deg angle
t_orbit_before_90deg_sun = t_orbit * frac_orbit_before_90deg_sun  # [s] time of orbit before and after sun and orbit radius have 90deg angle

n_sq = g_param / np.power(a_orbit, 3, dtype="float64")  # [1/s^2] parameter for Gravity torque  [WP2]
n_orbits = t_mission/t_orbit

# # # Magnetic parameters # # #

l_constant = 1.2  # Approximation, (1 at equator and 2 at poles) [SMAD] [Spacecraft Systems Engineering, fig 2.13b]
M_earth = 7.8 * 1e15  # [A/m^2] Magnetic dipole moment Earth [SMAD]
M_uranus = 50.0 * M_earth  # [A/m^2] Magnetic dipole moment Uranus [Book: Spacecraft Systems Engineering]
B_uranus = M_uranus/(np.power(a_orbit*1000, 3, dtype="float64")) * l_constant  # [A/m^2] Magnetic field Uranus [SMAD]

# # # SC parameters # # #

m_dry_SC = 1517.24  # [kg] mass of structure  [WP2]
r_SC = 1.8  # [m] circumcircle radius of octagon cylinder  [WP2]
h_SC = 8.235  # [m] height of SC  [WP2]
a_octagon = 1.378  # [m] side length of octagon  [WP1]
s_proj = a_octagon * (1 + m.sqrt(2))  # projected side length  [WP1]

masses_init = [[0.0, 0.0, 0.0, 1517.24],  # System  # [kg] x, y, z, mass  [WP2]
               [0.702, 0.0, 0.0, 180.73 * 1.2]]  # Fuel  [WP2]
masses_fin = [[0.0, 0.0, 0.0, 1517.24],  # System  # [kg] x, y, z, mass  [WP2]
              [0.702, 0.0, 0.0, (180.73 * (1 - 1 / 1.02) * 1.2)]]  # Fuel  # removing 2% residual  [WP2]

V_proptank = 182.69 * 1e-3  # [WP2]
r_proptank = np.cbrt(V_proptank/(4/3*np.pi))
m_proptank_av = (180.73 * 1.2 + 180.73 * (1 - 1 / 1.02) * 1.2) / 2
r_to_COM = 0.702  # [WP2]

I_xx = 1.05 * (1/3 + np.sqrt(2)/12) * m_dry_SC * np.square(r_SC) + 2/5 * m_proptank_av * np.square(r_proptank)  # [Omni calculator][Statics book]
I_yy = 1.05 * 1/12 * m_dry_SC * (3*np.square(r_SC) + np.square(h_SC)) + \
       2/5 * m_proptank_av * np.square(r_proptank) + m_proptank_av * np.square(r_to_COM)  # [Statics book]
I_zz = I_yy  # (assumption) [WP2]
I_SC = np.array([I_xx, I_yy, I_zz])  # [kg*m^2] Moment of Inertia along x axis

# # # Disturbance Torques # # #

C_d = 2.6  # [-] drag coefficient for Aerodynamic torque  [WP2]
S_x = 1.05 * 2*np.sqrt(2)*np.square(r_SC)
S_y = 1.05 * s_proj * h_SC
S_z = S_y
S = np.array([S_x, S_y, S_z])  # [m^2] surface area for Aerodynamic torque  [WP2] + 5% margin for extrusions

rho_opt = 0.84  # [-] reflectivity of sail for solar radiation torque  [WP2]

D = 0.1  # [A*m^2] residual magnetic dipole [ADSEE READER]

# # # Uncertainties and misalignments # # #

theta_misalignment = np.pi/180  # 1 deg
phi_misalignment = np.pi/180  # 1 deg
CG_uncertainty = 0.02  # 2cm is uncertainty [SMAD][p. 574]
angle_thrust_misalignment = 0.3 * np.pi/180  # 0.3 deg  [SMAD][p. 574]

arm_thrust_misalignment = h_SC/2 * np.sin(angle_thrust_misalignment)  # from geometric center in both y and z-axis
arm_thrust_misalignment_array = np.array([0, arm_thrust_misalignment, arm_thrust_misalignment])
# # # ADCS # # #

thrust_adcs = 1.5  # [N]
ISP_adcs = 239  # [s]
v_exh_adcs = ISP_adcs * g0
m_dot_adcs = thrust_adcs/v_exh_adcs
distance_thrusters_to_cm = np.array([h_SC/2, s_proj/2, s_proj/2])  # [m] simplification
propmargin = 2.00  # 100% [ESA]
propdensity = 1240

ft = np.array([1.5, 5.5, 4, 1.1, 0.1])
isp = np.array([239, 253, 229, 231, 209])
vexh = isp*g0
mdot = ft/vexh

# # # Other # # #

thrust_mainengine = 560  # [N] [WP2]
burn_time_mainengine = 1048.74  # [s] [WP2]
burn_time_mainengine_per_orbit = burn_time_mainengine/n_orbits

omega = 2*np.pi/t_orbit

