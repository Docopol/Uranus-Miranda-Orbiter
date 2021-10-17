import input_parameters as ip
import main
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 13299)
To = ip.t_orbit
a_torque = []
s_torque = []
g_torque = []
m_torque = []
sum_torques = []

ae_T_x = []
ae_T_y = []
ae_T_z = []

for i in t:
    if 0 <= i <= 1/4:
        ae_torque = np.sqrt(np.square(main.torque_ae_x_var(i * To)) + np.square(main.torque_ae_y_var(i * To)) + np.square(main.torque_ae_z_var(i * To)))
        a_torque.append(ae_torque)
        ae_x = main.torque_ae_x_var(i * To)
        ae_y = main.torque_ae_y_var(i * To)
        ae_z = main.torque_ae_z_var(i * To)
        ae_T_x.append(ae_x)
        ae_T_y.append(ae_y)
        ae_T_z.append(ae_z)

        sol_torque = norm(main.solar_torque(main.cm_array_avg))
        s_torque.append(sol_torque)

        grav_torque = np.sqrt(np.square(main.torque_grav_x_var(i * To)) + np.square(main.torque_grav_y_var(i * To)) + np.square(main.torque_grav_z_var(i * To)))
        g_torque.append(grav_torque)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
    if 1/4 < i <= (1/2 + ip.frac_orbit_before_90deg_sun):
        ae_torque = norm(main.aerodynamic_torque(main.cm_array_avg, main.v_mission))
        a_torque.append(ae_torque)
        ae_x = main.aerodynamic_torque(main.cm_array_avg, main.v_mission)[0]
        ae_y = main.aerodynamic_torque(main.cm_array_avg, main.v_mission)[1]
        ae_z = main.aerodynamic_torque(main.cm_array_avg, main.v_mission)[2]
        ae_T_x.append(ae_x)
        ae_T_y.append(ae_y)
        ae_T_z.append(ae_z)

        sol_torque = np.sqrt(np.square(main.torque_s_x_var(i * To)) + np.square(main.torque_s_y_var(i * To)) + np.square(main.torque_s_z_var(i * To)))
        s_torque.append(sol_torque)

        grav_torque = norm(main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment))
        g_torque.append(grav_torque)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
    if (1/2 + ip.frac_orbit_before_90deg_sun) < i <= (1-ip.frac_orbit_before_90deg_sun):
        ae_torque = norm(main.aerodynamic_torque(main.cm_array_avg, main.v_mission))
        a_torque.append(ae_torque)
        ae_x = main.aerodynamic_torque(main.cm_array_avg, main.v_mission)[0]
        ae_y = main.aerodynamic_torque(main.cm_array_avg, main.v_mission)[1]
        ae_z = main.aerodynamic_torque(main.cm_array_avg, main.v_mission)[2]
        ae_T_x.append(ae_x)
        ae_T_y.append(ae_y)
        ae_T_z.append(ae_z)

        sol_torque = 0
        s_torque.append(sol_torque)

        grav_torque = norm(main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment))
        g_torque.append(grav_torque)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
    if (1-ip.frac_orbit_before_90deg_sun) < i <= 1:
        ae_torque = np.sqrt(np.square(main.torque_ae_x_var(i * To)) + np.square(main.torque_ae_y_var(i * To)) + np.square(main.torque_ae_z_var(i * To)))
        a_torque.append(ae_torque)
        ae_x = main.torque_ae_x_var(i * To)
        ae_y = main.torque_ae_y_var(i * To)
        ae_z = main.torque_ae_z_var(i * To)
        ae_T_x.append(ae_x)
        ae_T_y.append(ae_y)
        ae_T_z.append(ae_z)

        sol_torque = norm(main.solar_torque(main.cm_array_avg))
        s_torque.append(sol_torque)

        grav_torque = np.sqrt(np.square(main.torque_grav_x_var(i * To)) + np.square(main.torque_grav_y_var(i * To)) + np.square(main.torque_grav_z_var(i * To)))
        g_torque.append(grav_torque)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)

sum_torques = np.array(a_torque) + np.array(s_torque) + np.array(g_torque) + np.array(m_torque)


def aero_graph():
    plt.title("Aerodynamic torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, ae_x, 'r--', label='x-axis')
    plt.plot(t, ae_y, 'b--', label='y-axis')
    plt.plot(t, ae_z, 'g--', label='z-axis')
    plt.legend()
    plt.savefig("aero_graph.svg", format="svg")
    plt.show()


def solar_graph():
    plt.title("Solar torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, s_torque)
    plt.savefig("solar_graph.png")
    plt.show()


def grav_graph():
    plt.title("Gravity torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, g_torque)
    plt.savefig("grav_graph.png")
    plt.show()


def mag_graph():
    plt.title("Magnetic torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, m_torque)
    plt.savefig("mag_graph.png")
    plt.show()


def tot_graph():
    plt.title("Total torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, sum_torques)
    plt.savefig("total_graph.png")
    plt.show()


aero_graph()
solar_graph()
grav_graph()
mag_graph()
tot_graph()
