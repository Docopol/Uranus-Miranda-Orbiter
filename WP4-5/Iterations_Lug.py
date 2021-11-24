from Classes import Flange, Lug, Double_lug, Material
from Constants import *
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

        # Lower bounds for thickness
        if n == 0:
            lower_bound_t_up = i.lower_bound_t(loading[n])
            print(1000*lower_bound_t_up)
        else:
            lower_bound_t_down = i.lower_bound_t(loading[n])
            print(1000*lower_bound_t_down)

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
            diameter -= 0.001*d_max
        iterations.append(t_list)
        n += 1

    ''''
    # Add lower bound thickness
    d_list = list()
    t_list = list()
    n = 0
    for i in iterations:
        for j in i:
            d_list.append(round(1000 * j[0], 2))
            if n == 0:
                t_list.append(round(1000 * lower_bound_t_up, 2))
            else:
                t_list.append(round(1000 * lower_bound_t_down, 2))
            plt.plot(d_list, t_list)
            n += 1
    '''
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
    # plt.xlabel('Diameter [mm]')
    # plt.ylabel('Thickness [mm]')
    # plt.legend(['Minimum thickness top lug', 'Minimum thickness bottom lug', 'Top lug', 'Bottom lug'])
    # plt.grid()
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
                material=material_dict['aluminum'],
                length=l_initial
            )
            mass = f.mass()
            if mass < m:
                m = f.mass()
                fl = f
        configs.append((m, fl))
        n += 1
    return configs


def second_iteration(dlug):
    # Explore variations in length and width, using the minimum thickness stablished by bending moments
    ...


# Loads not taking into account the moment generated
g = 9.80665
rtg_mass = 97.8
number_of_rtgs = 3
accelerations = np.array([2, 6, 2])
loads = rtg_mass / number_of_rtgs * g * accelerations

separation = 0.56
distance_to_rtgs_cg = 0.38

#initial values for the itteration
# Obtained from BDCB-13 -- https://www.hydrauliccylindersinc.com/product/clevis-bracket/
w_initial = 0.04445
t_initial = 0.01
d_initial = 0.034925
l_initial = 0.053975


"""
Sources: (So far only averaged values have been used)
https://curioustab.com/discuss/69852/the-permissible-bearing-stress-in-steel-is/#:~:text=The%20permissible%20bearing%20stress%20in,cm2%201890%20kg%2Fcm2%2020
https://www.google.com/search?q=allowable+bearing+stress+iron&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvLo5VnrRwZI7eBvUAnnnDBd1mk55w%3A1636985183684&ei=X2mSYeiTKczSkwWivI1I&oq=allowable+bearing+stress+iron&gs_lcp=Cgdnd3Mtd2l6EAMyCAghEBYQHRAeOgcIIxCwAxAnOgUIABDLAToGCAAQFhAeSgQIQRgBUJMHWIkKYKILaAJwAHgAgAFIiAGQApIBATSYAQCgAQHIAQHAAQE&sclient=gws-wiz&ved=0ahUKEwiov4CDxZr0AhVM6aQKHSJeAwkQ4dUDCA4&uact=5
https://docshare.tips/allowable-bearing-stress-for-aluminum-alloys_58424f00b6d87f9e1d8b473c.html
https://www.google.com/search?q=maximum+shear+stress+steel&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvKys7p3IPuX1XAvpnA1pmuqUt5FKg%3A1636984953197&ei=eWiSYce1C7GCi-gPxoqx0Ak&oq=maximum+shear+stress+steel&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEMsBMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgcIABBHELADSgQIQRgAUMIEWKoKYPoLaAJwAngAgAF_iAGhA5IBAzQuMZgBAKABAcgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwiH1oyVxJr0AhUxwQIHHUZFDJoQ4dUDCA4&uact=5
https://www.google.com/search?q=maximum+shear+stress+iron&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvJJ31XwsRHQHeeMz_7lLYEnshcp1A%3A1636984917313&ei=VWiSYY-5Eo2-kwWQ3rv4AQ&oq=maximum+shear+stress+iron&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEBYQHjoHCCMQsAMQJzoHCAAQRxCwAzoFCAAQywFKBAhBGABQ8gZYyAlgkQtoAnACeACAAZoBiAH0ApIBAzMuMZgBAKABAcgBCcABAQ&sclient=gws-wiz&ved=0ahUKEwjPt_6DxJr0AhUN36QKHRDvDh8Q4dUDCA4&uact=5
https://www.google.com/search?q=maximum+shear+stress+aluminium&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvL6f4sO_Uth-ciGNgZ4dQbVEi42OQ%3A1636984828892&ei=_GeSYevqNZLqkgWRuLTYDw&oq=maximum+shear+stress+a&gs_lcp=Cgdnd3Mtd2l6EAMYADIGCCMQJxATMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBOgcIIxCwAxAnOgcIABBHELADOgQIIxAnOgQIABBDOgUIABCABDoLCC4QgAQQxwEQ0QM6CwguEIAEEMcBEKMCOgsILhCABBDHARCvAToFCC4QgAQ6BQguEMsBOgsILhDHARCvARDLAUoECEEYAFCAxgRY2O8EYJH4BGgEcAJ4AIABgAGIAesPkgEEMjAuNJgBAKABAcgBCcABAQ&sclient=gws-wiz
Materials Book
"""


# First level estimation of dimensions

flange = Flange(
    width=w_initial,
    lug_thickness=t_initial,
    hinge_diameter=d_initial,
    material=material_dict['aluminum'],
    length=l_initial
)

clearance = 0.0516128
lug = Lug(flange=flange, separation=clearance, number=2)

d_1 = Double_lug(
    top_lug=flange,
    bottom_lug=flange,
    separation=separation,
    dist_to_cg=distance_to_rtgs_cg
)
d_2 = Double_lug(
    top_lug=lug,
    bottom_lug=lug,
    separation=separation,
    dist_to_cg=distance_to_rtgs_cg
)

top, bottom = iterate_2(dlug=d_2)
print('Top lug: (w, t, d, l)' + str(top[1].get_dimensions()) + ' has a mass of ' + str(1000*top[0]) + ' g')
print('Bottom lug: (w, t, d, l)' + str(bottom[1].get_dimensions()) + ' has a mass of ' + str(1000*bottom[0]) + ' g')
