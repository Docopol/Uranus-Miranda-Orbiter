from Classes import Flange, Lug, Double_lug
from Constants import material_dict
import numpy as np
import matplotlib.pyplot as plt


def iterate_2(dlug):
    # Assume w to be fixed
    # 1. Maximize D
    # 2. Minimize t for D_max
    # 3. Find out if smaller "D"s allow for smaller "t"s
    lugs = dlug.get_lugs()
    loading = dlug.loads(loads)
    iterations = list()
    n = 0
    for i in lugs:
        w, t, d, l = i.get_dimensions()
        material = i.get_material()

        d_min = i.minimum_d(loading[n])
        d_max = i.maximum_d(loading[n])

        t_list = list()
        diameter = d_max
        while diameter > d_min:
            fl = Flange(
                width=w,
                lug_thickness=t,
                hinge_diameter=diameter,
                material=material,
                length=l
            )
            lug = Lug(
                flange=fl,
                number=2,
                separation=0.05
            )
            t_list.append((diameter, lug.minimum_t(loading[n])))
            diameter -= 0.0001*d_max
        iterations.append(t_list)
        n += 1

    # Plot results
    diameters = list()
    thicknesses = list()
    for i in iterations:
        d_list = list()
        t_list = list()
        for j in i:
            d_list.append(round(1000*j[0], 2))
            t_list.append(round(1000*j[1], 2))
        plt.plot(d_list, t_list)
        diameters.append(d_list)
        thicknesses.append(t_list)
    plt.xlabel('Diameter [mm]')
    plt.ylabel('Thickness [mm]')
    plt.legend(['Minimum thickness top lug', 'Minimum thickness bottom lug', 'Top lug', 'Bottom lug'])
    plt.grid()
    # plt.show()

    n = 0
    configs = list()
    for j in diameters:
        m = 1000
        for i in range(len(j)):
            f = Flange(
                width=w_initial,
                lug_thickness=thicknesses[n][i] / 1000,
                hinge_diameter=j[i] / 1000,
                material=material_dict['Al2014T6'],
                length=l_initial
            )
            mass = f.mass()
            if mass < m:
                m = f.mass()
                fl = f
        configs.append((m, fl))
        n += 1
    return configs  # Minimum diameters are (low, up) = (33.15mm, 42.18mm)


def second_iteration(dob_lug):  # Check, it does not work
    # Explore variations in length and width, using the minimum thickness stablished by bending moments
    top_config, bottom_config = iterate_2(dob_lug)
    top_flange = top_config[1]
    bottom_flange = bottom_config[1]

    loading = dob_lug.loads(loads)
    for i in range(len(loading)):
        tup = loading[i]
        for j in range(len(tup)):
            if j == 0:
                continue  # load on x-direction will be carried by only 1 flange
            tup[j] = tup[j]/2
        loading[i] = tup

    flanges = [top_flange, bottom_flange]

    min_w = [top_flange.min_w_2(loading[0]), bottom_flange.min_w_2(loading[1])]
    n = 0
    for item in flanges:
        w, t, d, l = item.get_dimensions()
        ratio = l / w**2
        w = min_w[n]
        l = ratio * w**2
        fl = Flange(
            width=w,
            lug_thickness=t,
            hinge_diameter=d,
            material=material_dict['Al2014T6'],
            length=l
        )
        if not fl.check_failure(loading[n]):
            flanges[n] = fl
        else:
            print(f'something went wrong on iteration {n}')
        n += 1
    return flanges


# Loads not taking into account the moment generated
g = 9.80665
rtg_mass = 97.8
number_of_rtgs = 3
accelerations = np.array([2, 6, 2])
loads = rtg_mass / number_of_rtgs * g * accelerations

separation = 0.56
distance_to_rtgs_cg = 0.38

# Initial values for the itteration
# Obtained from BDCB-13 -- https://www.hydrauliccylindersinc.com/product/clevis-bracket/
w_initial = 0.04445
t_initial = 0.01
d_initial = 0.034925
l_initial = 0.053975


lower_bound_t_up = int()
lower_bound_t_down = int()

# First level estimation of dimensions

flange = Flange(
    width=w_initial,
    lug_thickness=t_initial,
    hinge_diameter=d_initial,
    material=material_dict['Al2014T6'],
    length=l_initial
)

clearance = 0.0516128
lug = Lug(flange=flange, separation=clearance, number=2)

d_2 = Double_lug(
    top_lug=lug,
    bottom_lug=lug,
    separation=separation,
    dist_to_cg=distance_to_rtgs_cg
)

top2, bottom2 = second_iteration(dob_lug=d_2)
print('Top flange: (w, t, d, l)' + str(top2.get_dimensions()) + ' has a mass of ' + str(1000*top2.mass()) + ' g')
print('Bottom flange: (w, t, d, l)' + str(bottom2.get_dimensions()) + ' has a mass of ' + str(1000*bottom2.mass()) + ' g')
