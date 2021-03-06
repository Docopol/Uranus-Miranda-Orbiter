import input_parameters as ip
import numpy as np
from scipy.integrate import quad


def COM(masses):
    mass_array = np.array([0, 0, 0, 0])
    for v in masses:
        mass_array = np.vstack((mass_array, v))
    c_mass = np.average(mass_array[:, :3], axis=0, weights=mass_array[:, 3])
    c_mass[:3] += ip.CG_uncertainty
    return c_mass


# def COP(areas):
#     area_array = np.array([0, 0, 0, 0])
#     for v in areas:
#         area_array = np.vstack((area_array, v))
#     c_pressure = np.average(area_array[:, :3], axis=0, weights=area_array[:, 3])
#     return c_pressure


cm_array_init = COM(ip.masses_init)
cm_array_fin = COM(ip.masses_fin)
cm_array_avg = (cm_array_init + cm_array_fin) / 2

v_mission = np.array([ip.v_orbit, 0, 0])


# # # Base Equations External Disturbances # # #

def aerodynamic_torque(r_m, v):
    F_a = 0.5 * ip.rho * ip.C_d * np.square(v) * ip.S
    torque = np.cross(r_m, F_a)
    return torque


def solar_torque(r_p):
    F_s = (1 + ip.rho_opt) * ip.P_s_uranus * ip.S
    torque = np.cross(r_p, F_s)

    return torque


def gravity_torque(I_x, I_y, I_z, phi, theta):
    grav_tor_x = 3 / 2 * ip.n_sq * (abs(0.99*I_y - I_z) * np.sin(2 * phi) * np.square(np.cos(theta)))
    grav_tor_y = 3 / 2 * ip.n_sq * (abs(I_x - I_z) * np.sin(2 * theta) * np.cos(phi))
    grav_tor_z = 3 / 2 * ip.n_sq * (abs(I_x - I_y) * np.sin(phi) * np.sin(2 * theta))
    torque = np.array([grav_tor_x, grav_tor_y, grav_tor_z])
    return torque


def magnetic_torque(D, B):
    torque = D * B
    torque_array = np.array([1/3, 1/3, 1/3])*torque
    return torque_array, torque


# # # Variable Equations External Disturbances # # #

def torque_ae_x_var(t):
    k2 = cm_array_avg[2] * 0.5 * ip.C_d * ip.rho * np.square(ip.v_orbit) * ip.S[1]

    return - k2 * np.square(np.sin(ip.omega * t))


def torque_ae_y_var(t):
    k1 = cm_array_avg[2] * 0.5 * ip.C_d * ip.rho * np.square(ip.v_orbit) * ip.S[0]

    return k1 * np.square(np.cos(ip.omega * t))


def torque_ae_z_var(t):
    k1 = cm_array_avg[0] * 0.5 * ip.C_d * ip.rho * np.square(ip.v_orbit) * ip.S[1]
    k2 = cm_array_avg[1] * 0.5 * ip.C_d * ip.rho * np.square(ip.v_orbit) * ip.S[0]

    return k1 * np.square(np.sin(ip.omega * t)) - k2 * np.square(np.cos(ip.omega * t))


def torque_s_x_var(t):
    k2 = cm_array_avg[2] * (1 + ip.rho_opt) * ip.P_s_uranus * ip.S[1]

    return - k2 * np.cos(ip.omega * t)


def torque_s_y_var(t):
    k1 = cm_array_avg[2] * (1 + ip.rho_opt) * ip.P_s_uranus * ip.S[0]

    return k1 * np.sin(ip.omega * t)


def torque_s_z_var(t):
    k1 = cm_array_avg[0] * (1 + ip.rho_opt) * ip.P_s_uranus * ip.S[1]
    k2 = cm_array_avg[1] * (1 + ip.rho_opt) * ip.P_s_uranus * ip.S[0]

    return k1 * np.sin(ip.omega * t) - k2 * np.cos(ip.omega * t)


def torque_grav_x_var(t):
    k1 = 3 / 2 * ip.n_sq * abs(0.99*ip.I_yy - ip.I_zz) * np.sin(2*ip.phi_misalignment)

    return k1 * np.square(np.cos(ip.omega * t))


def torque_grav_y_var(t):
    k1 = 3 / 2 * ip.n_sq * abs(ip.I_xx - ip.I_zz) * np.cos(ip.phi_misalignment)

    return k1 * np.sin(2 * ip.omega * t)


def torque_grav_z_var(t):
    k1 = 3 / 2 * ip.n_sq * abs(ip.I_xx - ip.I_yy) * np.sin(ip.phi_misalignment)

    return k1 * np.square(np.sin(ip.omega * t))


# # # Base Equations Internal Disturbances # # #

def thrust_misalignment():
    torque = ip.arm_thrust_misalignment_array * ip.thrust_mainengine
    impulse_array = torque * ip.burn_time_mainengine

    return torque, impulse_array


# # # Main Function All Disturbances # # #

def impulse_all_per_orbit():

    # # # External Angular Impulses # # #

    # # Aerodynamic Angular Impulse # #
    impulse_ae_mission = aerodynamic_torque(cm_array_avg, v_mission) * (3/4*ip.t_orbit - ip.t_orbit_before_90deg_sun)
    impulse_ae_sending_x = np.abs(quad(torque_ae_x_var, -ip.t_orbit_before_90deg_sun, 0)[0]) + \
                           np.abs(quad(torque_ae_x_var, 0, ip.t_orbit/4)[0])
    impulse_ae_sending_y = np.abs(quad(torque_ae_y_var, -ip.t_orbit_before_90deg_sun, 0)[0]) + \
                           np.abs(quad(torque_ae_y_var, 0, ip.t_orbit/4)[0])
    impulse_ae_sending_z = np.abs(quad(torque_ae_z_var, -ip.t_orbit_before_90deg_sun, 0)[0]) + \
                           np.abs(quad(torque_ae_z_var, 0, ip.t_orbit/4)[0])
    impulse_ae_sending = np.array([impulse_ae_sending_x, impulse_ae_sending_y, impulse_ae_sending_z])
    impulse_ae = np.abs(impulse_ae_mission) + np.abs(impulse_ae_sending)

    # # Solar Angular Impulse # #
    impulse_solar_sending = solar_torque(cm_array_avg) * (ip.t_orbit_before_90deg_sun + ip.t_orbit/4)
    impulse_solar_mission_day_x = np.abs(quad(torque_s_x_var, ip.t_orbit/4, ip.t_orbit/2)[0]) + \
                                  np.abs(quad(torque_s_x_var, ip.t_orbit/2, ip.t_orbit/2+ip.t_orbit_before_90deg_sun)[0])
    impulse_solar_mission_day_y = np.abs(quad(torque_s_y_var, ip.t_orbit/4, ip.t_orbit/2)[0]) + \
                                  np.abs(quad(torque_s_y_var, ip.t_orbit/2, ip.t_orbit/2+ip.t_orbit_before_90deg_sun)[0])
    impulse_solar_mission_day_z = np.abs(quad(torque_s_z_var, ip.t_orbit/4, ip.t_orbit/2)[0]) + \
                                  np.abs(quad(torque_s_z_var, ip.t_orbit/2, ip.t_orbit/2+ip.t_orbit_before_90deg_sun)[0])
    impulse_solar_mission_day = np.array([impulse_solar_mission_day_x, impulse_solar_mission_day_y, impulse_solar_mission_day_z])
    impulse_solar = np.abs(impulse_solar_mission_day) + np.abs(impulse_solar_sending)

    # # Gravity Angular Impulse # #
    impulse_grav_mission = gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.theta_misalignment, ip.phi_misalignment) * \
                           (3/4*ip.t_orbit - ip.t_orbit_before_90deg_sun)
    impulse_grav_sending_x = np.abs(quad(torque_grav_x_var, -ip.t_orbit_before_90deg_sun, 0)[0]) + \
                             np.abs(quad(torque_grav_y_var, 0, ip.t_orbit/4)[0])
    impulse_grav_sending_y = np.abs(quad(torque_grav_y_var, -ip.t_orbit_before_90deg_sun, 0)[0]) + \
                             np.abs(quad(torque_grav_y_var, 0, ip.t_orbit/4)[0])
    impulse_grav_sending_z = np.abs(quad(torque_grav_z_var, -ip.t_orbit_before_90deg_sun, 0)[0]) + \
                             np.abs(quad(torque_grav_z_var, 0, ip.t_orbit/4)[0])
    impulse_grav_sending = np.array([impulse_grav_sending_x, impulse_grav_sending_y, impulse_grav_sending_z])
    impulse_grav = np.abs(impulse_grav_mission) + np.abs(impulse_grav_sending)

    impulse_magnetic_mission = magnetic_torque(ip.D, ip.B_uranus)[0] * ip.t_orbit

    # # # Repositioning Angular Momentum # # #
    impulse_rotation_sending = ip.I_yy * ip.omega
    impulse_stop_rotation = impulse_rotation_sending
    impulse_rotation = np.abs(impulse_stop_rotation) + np.abs(impulse_stop_rotation)
    # Not included in sum because rotation wheel can initialize the rotation and end it without needing the thrusters

    # # # Internal Angular Impulse # # #

    impulse_thrust_mainengine = thrust_misalignment()[1]/ip.n_orbits

    # # # Sum # # #

    sum_impulse_ext_array = impulse_ae + impulse_solar + impulse_grav + impulse_magnetic_mission
    sum_impulse_ext = np.sum(sum_impulse_ext_array)

    sum_impulse_int_array = impulse_thrust_mainengine
    sum_impulse_int = np.sum(sum_impulse_int_array)

    sum_impulse_tot_array = sum_impulse_ext_array + sum_impulse_int_array
    sum_impulse_tot = np.sum(sum_impulse_tot_array)

    return {
        "Impulse due to aerodynamics during mission": impulse_ae_mission,
        "Impulse due to aerodynamics during sending": impulse_ae_sending,
        "Impulse due to solar during mission day": impulse_solar_mission_day,
        "Impulse due to solar during sending": impulse_solar_sending,
        "Impulse due to rotation to rotate for sending": impulse_rotation,
        "Impulse due to gravity during mission": impulse_grav_mission,
        "Impulse due to gravity during sending": impulse_grav_sending,
        "Impulse due to magnetic field during mission": impulse_magnetic_mission,
        "Impulse due to thrust misalignment during mission": impulse_thrust_mainengine,
        "Total impulse (internal and external)": sum_impulse_tot_array
    }, np.array(sum_impulse_tot_array), sum_impulse_tot


def propellant_mass(thrust, mdot, impulse_array):
    t_b_array = impulse_array/(thrust * 2*ip.distance_thrusters_to_cm)
    m_p_array = mdot * t_b_array
    t_b_array_margin = ip.propmargin * t_b_array
    m_p_array_margin = ip.propmargin * m_p_array
    return m_p_array, t_b_array, m_p_array_margin, t_b_array_margin


ae_torque = aerodynamic_torque(cm_array_avg, v_mission)
s_torque = solar_torque(cm_array_avg)
grav_torque = gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.theta_misalignment, ip.phi_misalignment)
m_torque = magnetic_torque(ip.D, ip.B_uranus)
thrust_misal_torque = thrust_misalignment()[0]

m_p_tot = np.sum(propellant_mass(ip.thrust_adcs, ip.m_dot_adcs, impulse_all_per_orbit()[1])[0] * ip.n_orbits)
t_b_axis_orbit = propellant_mass(ip.thrust_adcs, ip.m_dot_adcs, impulse_all_per_orbit()[1])[1]

m_p_tot_margin = np.sum(propellant_mass(ip.thrust_adcs, ip.m_dot_adcs, impulse_all_per_orbit()[1])[2] * ip.n_orbits)
t_b_axis_orbit_margin = propellant_mass(ip.thrust_adcs, ip.m_dot_adcs, impulse_all_per_orbit()[1])[3]
V_p_margin = m_p_tot_margin/ip.propdensity

# mp_array = []
# tb_array = []
# for i in range(len(ip.ft)):
#     m_p = np.sum(propellant_mass(ip.ft[i], ip.mdot[i], impulse_all_per_orbit()[1])[0] * ip.n_orbits)
#     mp_array.append(m_p)
#     tb = propellant_mass(ip.ft[i], ip.mdot[i], impulse_all_per_orbit()[1])[1] * ip.n_orbits
#     tb_array.append(tb)
# print(mp_array)
# print(tb_array)

# print(COM(ip.masses_av))

# # Print all torques: # #
print("The torques are:")
print("Aerodynamic torque:", ae_torque, " (non-variable)")
print("Solar torque:", s_torque, " (non-variable)")
print("Gravity gradient torque:", grav_torque, " (non-variable)")
print("Magnetic torque:", m_torque, " (non-variable)")
print("Torque created by misalignment of main thruster:", thrust_misal_torque, " (non-variable)")

print("\n")
# # Print Impulses: # #
print("All separate angular impulses per orbit:", impulse_all_per_orbit()[0])
print("Total angular impulse per orbit array:", impulse_all_per_orbit()[1])
print("Total angular impulse per orbit:", impulse_all_per_orbit()[2])
print("Total angular impulse during mission:", impulse_all_per_orbit()[2] * ip.n_orbits)

print("\n")
# # Print total propellant mass and burn time per axis (of thruster pair)
print("Propellant mass for ADCS:", m_p_tot)
print("Burn time array per orbit:", t_b_axis_orbit)
print("Total propellant mass for ADCS with margin:", m_p_tot_margin)
print("Burn time array with margin per orbit:", t_b_axis_orbit_margin)
print("Total propellant volume for ADCS with margin", V_p_margin)
