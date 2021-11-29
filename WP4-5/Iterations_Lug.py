from Classes import Flange
from Constants import material_dict
from calc import f_x_bot, f_y_bot, f_z_bot, M_y_bot


def iterate_2(fla):
    flan = fla
    w, t, d, l = flan.get_dimensions()
    material = flan.get_material()

    d_min = flan.minimum_d(loads)
    d_max = flan.maximum_d(loads)

    t_list = list()
    d_list = list()
    diameter = d_max
    while diameter > d_min:
        fl = Flange(
            width=w,
            lug_thickness=t,
            hinge_diameter=diameter,
            material=material,
            length=l
        )
        min_t = fl.minimum_t(loads, M_y_bot)
        f = Flange(
            width=w,
            lug_thickness=min_t,
            hinge_diameter=diameter,
            material=material,
            length=l
        )
        if not f.check_failure(loads, M_y_bot):
            t_list.append(min_t)
            d_list.append(diameter)
        diameter -= 0.00001

    m = 1000
    for i in range(len(t_list)):
        f = Flange(
            width=w,
            lug_thickness=t_list[i],
            hinge_diameter=d_list[i],
            material=material,
            length=l
        )
        mass = f.mass()
        ms, ty = f.margin_of_safety(loads, M_y_bot)
        if ms > 0.4 and 0 < mass < m:
            m = mass
            flan = f

    return flan, m


def second_iteration(dob_lug):
    w, t, d, l = dob_lug.get_dimensions()
    mat = dob_lug.get_material()
    f_list = list()
    m_list = list()
    while w > 0.01:
        if l < w/2:
            break
        if d > w:
            d = 0.9*w
        flan = Flange(
            width=w,
            lug_thickness=t,
            hinge_diameter=d,
            material=mat,
            length=l
        )

        fl, mass = iterate_2(flan)
        if mass > 0:
            f_list.append(fl)
            m_list.append(mass)
            w -= 0.0001
            l = (mat.get_stress() * w * t**2 / 6 - M_y_bot)*2/f_x_bot
        else:
            break
    return f_list[m_list.index(min(m_list))]


distance_to_rtgs_cg = 0.38

w_initial = 0.04445
t_initial = 0.01
d_initial = 0.034925
l_initial = 0.053975

flange = Flange(
        width=w_initial,
        lug_thickness=t_initial,
        hinge_diameter=d_initial,
        material=material_dict['Al2014T6'],
        length=l_initial
    )

loads = [f_x_bot, f_y_bot/2, f_z_bot/2]
ms, tp = flange.margin_of_safety(loads, M_y_bot)
print(f'Initial iteration has a safety factor of {ms}, and has a mass of {1000*flange.mass()} g')
for item in material_dict:
    print('\n' + item)
    print('Double Flange:')

    flange = Flange(
        width=w_initial,
        lug_thickness=t_initial,
        hinge_diameter=d_initial,
        material=material_dict[item],
        length=l_initial
    )

    loads = [f_x_bot, f_y_bot, f_z_bot]
    flange_config = second_iteration(dob_lug=flange)
    ms, tp = flange_config.margin_of_safety(loads, M_y_bot)
    print('Flange: (w, t, d, l)' + str(flange_config.get_dimensions()) +
          ' has a mass of ' + str(1000 * flange_config.mass()) + ' g')
    print(f'With a margin of safety of {ms} - Failure due to {tp}')
