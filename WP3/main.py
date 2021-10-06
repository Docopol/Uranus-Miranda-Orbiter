import input_parameters as i
import numpy as np


def COM(masses):
    mass_array = masses['Mass1']
    for k, v in masses.items():
        mass_array = np.vstack((mass_array, v))
    c_mass = np.average(mass_array[:, :3], axis=0, weights=mass_array[:, 3])
    return {
        "Centre of Mass": c_mass
    }


def COP(areas):
    area_array = areas['Area1']
    for k, v in areas.items():
        area_array = np.vstack((area_array, v))
    c_pressure = np.average(area_array[:, :3], axis=0, weights=area_array[:, 3])
    return {
        "Centre of Pressure": c_pressure
    }


def gravity_torque(I_x, I_y, I_z, phi, theta):
    n_sq = (i.g_param / (i.r_orbit + i.r_uranus) ** 3)
    grav_tor_x = 3 / 2 * n_sq * ((I_y - I_z) * np.sin(2 * phi))  # Torque in x direction
    grav_tor_y = 3 / 2 * n_sq * ((I_x - I_z) * np.sin(2 * theta))  # Torque in y direction
    grav_tor_z = 0  # Torque in z direction
    torque = [grav_tor_x, grav_tor_y, grav_tor_z]
    return {
        "Gravity torque x": grav_tor_x,
        "Gravity torque y": grav_tor_y,
        "Gravity torque z": grav_tor_z,
        "Gravity torque": torque
    }


masses = {"Mass1": [0, 0, 0, 1],
          "Mass2": [1, 2, 3, 4]}

areas = {"Area1": [0, 0, 0, 1],
         "Area2": [1, 2, 3, 4]}

print(masses.values())
print(COM(masses))
print(COP(areas))
