import input_parameters as i
import numpy as np
from scipy.integrate import quad


def COM(masses):
    mass_array = np.array([0, 0, 0, 0])
    for v in masses:
        mass_array = np.vstack((mass_array, v))
    c_mass = np.average(mass_array[:, :3], axis=0, weights=mass_array[:, 3])
    c_mass[:3] += i.CG_uncertainty
    return c_mass


# def COP(areas):
#     area_array = np.array([0, 0, 0, 0])
#     for v in areas:
#         area_array = np.vstack((area_array, v))
#     c_pressure = np.average(area_array[:, :3], axis=0, weights=area_array[:, 3])
#     return c_pressure


omega = 2*np.pi/i.t_orbit
cm_array_init = COM(i.masses_init)
cm_array_fin = COM(i.masses_fin)
cm_array_avg = (cm_array_init + cm_array_fin) / 2


def gravity_torque(I_x, I_y, I_z, phi, theta):
    grav_tor_x = 3 / 2 * i.n_sq * (abs(0.99*I_y - I_z) * np.sin(2 * phi) * np.square(np.cos(theta)))  # Torque in x direction
    grav_tor_y = 3 / 2 * i.n_sq * (abs(I_x - I_z) * np.sin(2 * theta) * np.cos(phi))  # Torque in y direction
    grav_tor_z = 3 / 2 * i.n_sq * (abs(I_x - I_y) * np.sin(phi) * np.sin(2 * theta))  # Torque in z direction
    torque = np.array([grav_tor_x, grav_tor_y, grav_tor_z])
    return torque


def aerodynamic_torque(r_m, v):
    F_a = 0.5 * i.rho * i.C_d * np.square(v) * i.S
    torque = np.cross(r_m, F_a)
    return torque


def solar_torque(r_p):
    F_s = (1 + i.rho_opt) * i.P_s * i.S
    torque = np.cross(r_p, F_s)
    return torque


def magnetic_torque(D, B):
    torque = D * B

    return torque


def torque_ae_x_var(t):
    k2 = cm_array_avg[2] * 0.5 * i.C_d * i.rho * np.square(i.v_orbit) * i.S[1]

    return - k2 * np.square(np.sin(omega * t))


def torque_ae_y_var(t):
    k1 = cm_array_avg[2] * 0.5 * i.C_d * i.rho * np.square(i.v_orbit) * i.S[0]

    return k1 * np.square(np.cos(omega * t))


def torque_ae_z_var(t):
    k1 = cm_array_avg[0] * 0.5 * i.C_d * i.rho * np.square(i.v_orbit) * i.S[1]
    k2 = cm_array_avg[1] * 0.5 * i.C_d * i.rho * np.square(i.v_orbit) * i.S[0]

    return k1 * np.square(np.sin(omega * t)) - k2 * np.square(np.cos(omega * t))


def torque_s_x_var(t):
    k2 = cm_array_avg[2] * (1 + i.rho_opt) * i.P_s * i.S[1]

    return - k2 * np.cos(omega * t)


def torque_s_y_var(t):
    k1 = cm_array_avg[2] * (1 + i.rho_opt) * i.P_s * i.S[0]

    return k1 * np.sin(omega * t)


def torque_s_z_var(t):
    k1 = cm_array_avg[0] * (1 + i.rho_opt) * i.P_s * i.S[1]
    k2 = cm_array_avg[1] * (1 + i.rho_opt) * i.P_s * i.S[0]

    return k1 * np.sin(omega * t) - k2 * np.cos(omega * t)


def torque_grav_x_var(t):
    k1 = 3 / 2 * i.n_sq * abs(0.99*i.I_yy - i.I_zz) * np.square(np.cos(omega * t))

    return k1 * np.sin(2*i.phi_misalignment)


def torque_grav_y_var(t):
    k1 = 3 / 2 * i.n_sq * abs(i.I_xx - i.I_zz) * np.cos(i.phi_misalignment)

    return k1 * np.sin(2 * omega * t)


def torque_grav_z_var(t):
    k1 = 3 / 2 * i.n_sq * abs(i.I_xx - i.I_yy) * np.sin(i.phi_misalignment)

    return k1 * np.square(np.sin(omega * t))


def impulse_thrust_misalignment():
    torque = i.thrust_mainengine * i.arm_thrust_misalignment
    impulse_x = 0
    impulse_y = torque * i.burn_time_mainengine
    impulse_z = impulse_y
    impulse_array = np.array([impulse_x, impulse_y, impulse_z])
    impulse = np.sum(impulse_array)
    return impulse


def impulse_all_orbit():
    ae_T_mission = aerodynamic_torque(cm_array_avg, v_mission)
    solar_T_sending = solar_torque(cm_array_avg)

    impulse_ae_mission = ae_T_mission * i.t_orbit * 3 / 4
    impulse_ae_sending = np.array([quad(torque_ae_x_var, 0, i.t_orbit/4)[0], quad(torque_ae_y_var, 0, i.t_orbit/4)[0], quad(torque_ae_z_var, 0, i.t_orbit/4)[0]])
    impulse_ae = np.abs(impulse_ae_mission) + np.abs(impulse_ae_sending)

    impulse_solar_sending = solar_T_sending * i.t_orbit * 1 / 4
    impulse_solar_mission_day = np.array([quad(torque_s_x_var, i.t_orbit / 4, i.t_orbit / 2)[0], quad(torque_s_y_var, i.t_orbit/4, i.t_orbit/2)[0], quad(torque_s_z_var, i.t_orbit/4, i.t_orbit/2)[0]])
    impulse_solar = np.abs(impulse_solar_mission_day) + np.abs(impulse_solar_sending)

    impulse_grav_mission = gravity_torque(i.I_xx, i.I_yy, i.I_zz, i.theta_misalignment, i.phi_misalignment) * i.t_orbit * 3/4
    impulse_grav_sending = np.array([quad(torque_grav_x_var, 0, i.t_orbit/4)[0], quad(torque_grav_y_var, 0, i.t_orbit/4)[0], quad(torque_grav_z_var, 0, i.t_orbit/4)[0]])
    impulse_grav = np.abs(impulse_grav_mission) + np.abs(impulse_grav_sending)

    impulse_magnetic_mission = magnetic_torque(i.D, i.B_uranus) * i.t_orbit

    ang_impulse_rotation_sending = i.I_yy * np.pi/2 / (i.t_orbit/4)
    ang_impulse_stop_rotation = ang_impulse_rotation_sending
    ang_impulse_rotation = np.abs(ang_impulse_stop_rotation) + np.abs(ang_impulse_stop_rotation)

    sum_impulses = np.sum(impulse_ae + impulse_solar + impulse_grav + impulse_magnetic_mission)

    return {
        "Impulse due to aerodynamics during mission": impulse_ae_mission,
        "Impulse due to aerodynamics during sending": impulse_ae_sending,
        "Impulse due to solar during mission day": impulse_solar_mission_day,
        "Impulse due to solar during sending": impulse_solar_sending,
        "Impulse due to rotation to rotate for sending": ang_impulse_rotation,
        "Impulse due to gravity during mission": impulse_grav_mission,
        "Impulse due to gravity during sending": impulse_grav_sending,
        "Impulse due to magnetic field during mission": impulse_magnetic_mission,
        "Total impulse": sum_impulses
    }, sum_impulses


def propellant_mass():
    m_p = ...

    return m_p

# print(COM(i.masses_init))
print("All separate impulses per orbit:", impulse_all_orbit())
print("Total impulse per orbit:", impulse_all_orbit()[1])
print("Impulse due to thruster misalignment:", impulse_thrust_misalignment())
print("Total impulse during mission:", impulse_all_orbit()[1] * i.n_orbits + impulse_thrust_misalignment())
