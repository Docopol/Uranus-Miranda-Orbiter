import math
import matplotlib.pyplot as plt
from Thermal_Control_Equations import Q_sun, Q_in_eclipse, Q_in_sunlight, radiating_area, Q_out


qo = Q_out(285, 119.1, 0.173)


I_sun = 30459109.914585304
d_U = 2872.463
d = 108
AU = 1.5 * 10**11

q2 = list()
q_list = list()
d_list = list()
while d <= d_U:
    I = I_sun/d**2
    q_in = Q_sun(I, 0.09, 32.9)
    q_in += Q_in_sunlight((d_U-d)*10**9, 0.09)
    q = qo - q_in
    
    d_list.append(d * 10**9 / AU)
    q_list.append(q / 1000)
    q2.append(qo / 1000)
    d += 10

plt.plot(d_list, q_list)
plt.plot(d_list, q2, 'r--')
plt.legend(['Internal Heat Generated', f'{round(qo/1000, 2)} kW'])
plt.xlabel('Distance [AU]')
plt.ylabel('Heat Generated [kW]')
plt.grid()
plt.show()
