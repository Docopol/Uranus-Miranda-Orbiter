import input_parameters as i
import numpy as np
from scipy.integrate import quad


def COM(masses):
    mass_array = [0, 0, 0, 0]
    for k, v in masses.items():
        mass_array = np.vstack((mass_array, v))
    c_mass = np.average(mass_array[:, :3], axis=0, weights=mass_array[:, 3])
    return c_mass


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


def aerodynamic_torque(r_m, S, v):
    F_a = 0.5 * i.rho * i.C_d * np.square(v) * S
    torque = np.cross(r_m, F_a)
    return torque


def solar_torque(r_p, S):
    F_s = (1 + rho) * P_s * S
    torque = np.cross(r_p, F_s)
    return {
        "Solar radiation torque": torque
    }


def magnetic_torque(M, B):
    torque = np.cross(M, B)
    return {
        "Magnetic Torque": torque
    }


def sin(x):
    return np.sin(x)


def ang_impulse(S, v, angle):
    av_sin = quad(sin, 0, angle)
    F_a = 0.5 * i.rho * i.C_d * np.square(v) * (S[0] + S[1]) * av_sin


def calculations():
    cm_array_init = COM(i.masses_init)
    cm_array_fin = COM(i.masses_fin)
    cm_array_avg = (cm_array_init + cm_array_fin)/2

    aero_torque_mission = aerodynamic_torque(cm_array_avg, i.S, v_mission)
    aero_torque_sending = aerodynamic_torque(cm_array_avg, i.S, v_sending)
    impulse_mission = aero_torque_mission * i.t_mission * 3 / 4
    impulse_sending = aero_torque_sending * i.t_mission * 1 / 4
    impulse_mission_orbit = aero_torque_mission * i.t_orbit * 3 / 4
    impulse_sending_orbit = aero_torque_sending * i.t_orbit * 1 / 4

    ang_impulse_sending = i.I[1] * np.pi/2 / i.t_orbit/4

    return {
        "Impulse total: ": impulse_mission + impulse_sending,
        "Impulse 1 orbit Total: ": impulse_mission_orbit + impulse_sending_orbit + ang_impulse_sending
    }


v_mission = np.array([i.v_orbit, 0, 0])
v_sending = np.array([0, i.v_orbit, 0])

print(COM(i.masses_init))
print(calculations())
