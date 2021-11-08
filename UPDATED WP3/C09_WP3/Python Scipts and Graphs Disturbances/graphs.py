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

s_T_x = []
s_T_y = []
s_T_z = []

grav_T_x = []
grav_T_y = []
grav_T_z = []

mag_T_x = []
mag_T_y = []
mag_T_z = []

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
        s_x = main.solar_torque(main.cm_array_avg)[0]
        s_y = main.solar_torque(main.cm_array_avg)[1]
        s_z = main.solar_torque(main.cm_array_avg)[2]
        s_T_x.append(s_x)
        s_T_y.append(s_y)
        s_T_z.append(s_z)

        grav_torque = np.sqrt(np.square(main.torque_grav_x_var(i * To)) + np.square(main.torque_grav_y_var(i * To)) + np.square(main.torque_grav_z_var(i * To)))
        g_torque.append(grav_torque)
        g_x = main.torque_grav_x_var(i * To)
        g_y = main.torque_grav_y_var(i * To)
        g_z = main.torque_grav_z_var(i * To)
        grav_T_x.append(g_x)
        grav_T_y.append(g_y)
        grav_T_z.append(g_z)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
        mag_T_x.append(mag_torque / 3)
        mag_T_y.append(mag_torque / 3)
        mag_T_z.append(mag_torque / 3)

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
        s_x = main.torque_s_x_var(i * To)
        s_y = main.torque_s_y_var(i * To)
        s_z = main.torque_s_z_var(i * To)
        s_T_x.append(s_x)
        s_T_y.append(s_y)
        s_T_z.append(s_z)

        grav_torque = norm(main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment))
        g_torque.append(grav_torque)
        g_x = main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment)[0]
        g_y = main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment)[1]
        g_z = main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment)[2]
        grav_T_x.append(g_x)
        grav_T_y.append(g_y)
        grav_T_z.append(g_z)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
        mag_T_x.append(mag_torque / 3)
        mag_T_y.append(mag_torque / 3)
        mag_T_z.append(mag_torque / 3)

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
        s_x = 0
        s_y = 0
        s_z = 0
        s_T_x.append(s_x)
        s_T_y.append(s_y)
        s_T_z.append(s_z)

        grav_torque = norm(main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment))
        g_torque.append(grav_torque)
        g_x = main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment)[0]
        g_y = main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment)[1]
        g_z = main.gravity_torque(ip.I_xx, ip.I_yy, ip.I_zz, ip.phi_misalignment, ip.theta_misalignment)[2]
        grav_T_x.append(g_x)
        grav_T_y.append(g_y)
        grav_T_z.append(g_z)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
        mag_T_x.append(mag_torque / 3)
        mag_T_y.append(mag_torque / 3)
        mag_T_z.append(mag_torque / 3)

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
        s_x = main.solar_torque(main.cm_array_avg)[0]
        s_y = main.solar_torque(main.cm_array_avg)[1]
        s_z = main.solar_torque(main.cm_array_avg)[2]
        s_T_x.append(s_x)
        s_T_y.append(s_y)
        s_T_z.append(s_z)

        grav_torque = np.sqrt(np.square(main.torque_grav_x_var(i * To)) + np.square(main.torque_grav_y_var(i * To)) + np.square(main.torque_grav_z_var(i * To)))
        g_torque.append(grav_torque)
        g_x = main.torque_grav_x_var(i * To)
        g_y = main.torque_grav_y_var(i * To)
        g_z = main.torque_grav_z_var(i * To)
        grav_T_x.append(g_x)
        grav_T_y.append(g_y)
        grav_T_z.append(g_z)

        mag_torque = main.magnetic_torque(ip.D, ip.B_uranus)[1]
        m_torque.append(mag_torque)
        mag_T_x.append(mag_torque / 3)
        mag_T_y.append(mag_torque / 3)
        mag_T_z.append(mag_torque / 3)

sum_torques = np.array(a_torque) + np.array(s_torque) + np.array(g_torque) + np.array(m_torque)


def aero_graph():
    plt.title("Aerodynamic torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, ae_T_x, 'r', label='x-axis')
    plt.plot(t, ae_T_y, 'b', label='y-axis')
    plt.plot(t, ae_T_z, 'g', label='z-axis')
    plt.legend()
    plt.tight_layout()
    plt.savefig("aero_graph.svg", format="svg")
    plt.show()


def solar_graph():
    plt.title("Solar torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, s_T_x, 'r', label='x-axis')
    plt.plot(t, s_T_y, 'b', label='y-axis')
    plt.plot(t, s_T_z, 'g', label='z-axis')
    plt.legend()
    plt.tight_layout()
    plt.savefig("solar_graph.svg", format="svg")
    plt.show()


def grav_graph():
    plt.title("Gravity torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, grav_T_x, 'r', label='x-axis')
    plt.plot(t, grav_T_y, 'b', label='y-axis')
    plt.plot(t, grav_T_z, 'g', label='z-axis')
    plt.legend()
    plt.tight_layout()
    plt.savefig("grav_graph.svg", format="svg")
    plt.show()


def mag_graph():
    plt.title("Magnetic torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, m_torque)
    plt.tight_layout()
    plt.savefig("mag_graph.svg", format="svg")
    plt.show()

sum_T_x = np.abs(ae_T_x) + np.abs(s_T_x) + np.abs(grav_T_x) + np.abs(mag_T_x)
sum_T_y = np.abs(ae_T_y) + np.abs(s_T_y) + np.abs(grav_T_y) + np.abs(mag_T_y)
sum_T_z = np.abs(ae_T_z) + np.abs(s_T_z) + np.abs(grav_T_z) + np.abs(mag_T_z)

def tot_graph():
    plt.title("Total torque")
    plt.xlabel("t/t_orbit")
    plt.ylabel("Torque [Nm]")
    plt.plot(t, sum_torques, 'k', label='Magnitude')
    plt.plot(t, sum_T_x, 'r--', label='x-axis')
    plt.plot(t, sum_T_y, 'b--', label='y-axis')
    plt.plot(t, sum_T_z, 'g--', label='z-axis')
    plt.legend()
    plt.tight_layout()
    plt.savefig("total_graph.svg", format="svg")
    plt.show()


aero_graph()
solar_graph()
grav_graph()
mag_graph()
tot_graph()
