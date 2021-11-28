from Classes import Flange, Lug, Double_lug
from Constants import material_dict
import numpy as np
import matplotlib.pyplot as plt


def iterate_2(dlug):
    loading = dlug.loads(loads)

    lug = dlug.get_lugs()[0]  # Assumes both are the same
    if isinstance(lug, Lug):
        loading[1] = loading[1] / 2
        loading[2] = loading[2] / 2
        fl = lug.get_flange()
    else:
        fl = lug

    w, t, d, l = fl.get_dimensions()
    material = fl.get_material()

    d_min = fl.minimum_d(loading)
    d_max = fl.maximum_d(loading)

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
        t_list.append((diameter, fl.minimum_t(loading)))
        diameter -= 0.00001

    # Plot results
    d_list = list()
    th_list = list()
    for i in t_list:
        d_list.append(round(1000*i[0], 2))
        th_list.append(round(1000*i[1], 2))
    plt.plot(d_list, th_list)
    plt.xlabel('Diameter [mm]')
    plt.ylabel('Thickness [mm]')
    plt.legend(['Minimum thickness'])
    plt.grid()
    plt.show()

    m = 1000
    for i in range(len(th_list)):
        f = Flange(
            width=w_initial,
            lug_thickness=th_list[i] / 1000,
            hinge_diameter=d_list[i] / 1000,
            material=material,
            length=l_initial
        )
        mass = f.mass()
        if not f.check_failure(loading) and 0 < mass < m:
            m = mass
            fl = f

    return fl


def second_iteration(dob_lug):  # Check, it does not work
    # Explore variations in length and width, using the minimum thickness stablished by bending moments
    fl = iterate_2(dob_lug)

    loading = dob_lug.loads(loads)
    if isinstance(dob_lug.get_lugs()[0], Lug):
        loading[1] = loading[1] / 2
        loading[2] = loading[2] / 2

    w, t, d, l = fl.get_dimensions()
    ratio = l / w**2

    while w > 1.1*d:
        w -= 0.00001
        l = ratio * w**2
        if l < w/2:
            break
        flan = Flange(
            width=w,
            lug_thickness=t,
            hinge_diameter=d,
            material=fl.get_material(),
            length=l
        )
        if not fl.check_failure(loading) and flan.mass() > 0:
                fl = flan
    return fl


# Loads not taking into account the moment generated
g = 9.80665
rtg_mass = 108
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
clearance = 0.0516128


for item in material_dict:
    print('\n' + item)
    print('Double Lug:')

    flange = Flange(
        width=w_initial,
        lug_thickness=t_initial,
        hinge_diameter=d_initial,
        material=material_dict[item],
        length=l_initial
    )

    lug = Lug(flange=flange, separation=clearance, number=2)

    d_2 = Double_lug(
        top_lug=lug,
        bottom_lug=lug,
        separation=separation,
        dist_to_cg=distance_to_rtgs_cg
    )

    flange_config = second_iteration(dob_lug=d_2)
    loading = d_2.loads(loads)
    loading[1] = loading[1] / 2
    loading[2] = loading[2] / 2
    ms, tp = flange_config.margin_of_safety(loading)
    print('Flange: (w, t, d, l)' + str(flange_config.get_dimensions()) +
          ' has a mass of ' + str(1000*flange_config.mass()) + ' g')
    print(f'With a margin of safety of {ms} - Failure due to {tp}')

    print('\nDouble Flange:')

    d_2 = Double_lug(
        top_lug=flange,
        bottom_lug=flange,
        separation=separation,
        dist_to_cg=distance_to_rtgs_cg
    )

    flange_config = second_iteration(dob_lug=d_2)
    loading = d_2.loads(loads)
    ms, tp = flange_config.margin_of_safety(loading)
    print('Flange: (w, t, d, l)' + str(flange_config.get_dimensions()) +
          ' has a mass of ' + str(1000 * flange_config.mass()) + ' g')
    print(f'With a margin of safety of {ms} - Failure due to {tp}')
