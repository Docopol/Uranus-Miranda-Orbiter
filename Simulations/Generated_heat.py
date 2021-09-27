import math
import matplotlib.pyplot as plt
from Thermal_Control_Equations import Q_sun, Q_in_eclipse, Q_in_sunlight, radiating_area, Q_out


def e(d):
    e = 0.05195972 / d**2 + 0.07276907
    print(e)
    if e < 0.0616:
        e = 0.0616
    elif e > 0.173:
        e = 0.173
    return e


# e max = 0.173 - 0.7AU
# e min = 0.074 - 2.5AU
# e(d) = 0.1/1.8 d + 0.117

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
    dist = d * 10**9 / AU

    if dist >= 1.3:
        #breakpoint()
        pass
    em = e(dist)
    qo = Q_out(285, 119.1, em)
    q = qo - q_in
    
    d_list.append(dist)
    q_list.append(q / 1000)
    q2.append(Q_out(285, 119.1, 0.073) / 1000)
    d += 1

plt.plot(d_list, q_list)
plt.plot(d_list, q2, 'r--')
plt.legend(['Internal Heat Generated', f'{round(qo/1000, 2)} kW'])
plt.xlabel('Distance [AU]')
plt.ylabel('Heat Generated [kW]')
plt.grid()
plt.show()
