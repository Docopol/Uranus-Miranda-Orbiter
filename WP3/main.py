import input_parameters as i
import numpy as np


def COM(masses):
    mass_array = [0, 0, 0, 0]
    for k, v in masses.items():
        mass_array = np.vstack((mass_array, v))
    c_mass = np.average(mass_array[:, :3], axis=0, weights=mass_array[:, 3])
    return {
        "Centre of Mass": c_mass
    }


def COP(areas):
    area_array = [0, 0, 0, 0]
    for k, v in areas.items():
        area_array = np.vstack((area_array, v))
    c_pressure = np.average(area_array[:, :3], axis=0, weights=area_array[:, 3])
    return {
        "Centre of Pressure": c_pressure
    }


def gravity_torque(I_x, I_y, I_z, phi, theta):
    grav_tor_x = 3 / 2 * i.n_sq * ((I_y - I_z) * np.sin(2 * phi))  # Torque in x direction
    grav_tor_y = 3 / 2 * i.n_sq * ((I_x - I_z) * np.sin(2 * theta))  # Torque in y direction
    grav_tor_z = 0  # Torque in z direction
    torque = [grav_tor_x, grav_tor_y, grav_tor_z]
    return {
        "Gravity torque x": grav_tor_x,
        "Gravity torque y": grav_tor_y,
        "Gravity torque z": grav_tor_z,
        "Gravity torque": torque
    }


def aerodynamic_torque(r_m, S):
    F_a = 0.5 * rho * v**2 * S * C_d
    torque = np.cross(r_m, F_a)
    return {
        "Aerodynamic torque": torque
    }


def solar_torque(r_p, S):
    F_s = (1 + rho) * P_s * S
    torque = np.cross(r_p, F_s)
    return{
        "Solar radiation torque": torque
    }


def magnetic_torque(M, B):
    torque = np.cross(M, B)
    return {
        "Magnetic Torque": torque
    }


print(COM(i.masses))
print(COP(i.areas))
