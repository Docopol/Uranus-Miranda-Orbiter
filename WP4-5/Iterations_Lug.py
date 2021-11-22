from Classes import Flange, Lug, Double_lug, Material
import numpy as np
import matplotlib.pyplot as plt


def iterate_2(dlug):
    # Assume w to be fixed
    # 1. Maximize D
    # 2. Minimize t for D_max
    # 3. Find out if smaller "D"s allow for smaller "t"s
    lugs = dlug.get_lugs()
    iterations = list()
    for i in lugs:
        w, t, d, l = i.get_dimensions()
        material = i.get_material()

        d_min = i.minimum_d(loads)
        d_max = i.maximum_d(loads)

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
            t_list.append((diameter, lug.minimum_t(loads)))
            diameter -= 0.0001*d_max
        iterations.append(t_list)

    # Plot results
    d_list = list()
    t_list = list()
    for i in iterations:
        for j in i:
            d_list.append(round(1000*j[0], 2))
            t_list.append(round(1000*j[1], 2))
        plt.plot(d_list, t_list)
    plt.xlabel('Diameter [mm]')
    plt.ylabel('Thickness [mm]')
    plt.legend(['Top lug', 'Bottom lug'])
    plt.grid()
    plt.show()

    m = 1000
    for i in range(len(d_list)):
        f = Flange(
            width=w_initial,
            lug_thickness=t_list[i] / 1000,
            hinge_diameter=d_list[i] / 1000,
            material=material_dict['aluminum'],
            length=l_initial
        )
        mass = f.mass()
        if mass < m:
            m = f.mass()
            fl = f
    return m, fl


def iterate(dlug):
    lugs = dlug.get_lugs()
    dim_list = list()
    mass_list = list()
    for i in lugs:
        w, t, d, l = i.get_dimensions()
        material = i.get_material()

        t2 = i.minimum_t(loads)
        d2 = i.minimum_d(loads)
        w2 = i.minimum_w(loads)

        # Since flanges are assumed to be equal to each other, minimizing Lug them will minimize the lug's
        s2 = Flange(width=w,
                    lug_thickness=t2,
                    hinge_diameter=d,
                    material=material,
                    length=l)

        s3 = Flange(width=w,
                    lug_thickness=t,
                    hinge_diameter=d2,
                    material=material,
                    length=l)

        s4 = Flange(width=w2,
                    lug_thickness=t,
                    hinge_diameter=d,
                    material=material,
                    length=l)

        # Necessary for it to work for Flange and Lug classes
        is_lug = isinstance(i, Lug)
        if is_lug:
            fl = i.get_flange()
        else:
            fl = i

        flanges = [fl, s2, s3, s4]
        m_list = list()
        for j in flanges:  # error pops up here
            m_list.append(j.mass())
        sorted_m = sorted(m_list)
        best_config = flanges[m_list.index(sorted_m[0])]
        dim_list.append(best_config.get_dimensions())
        mass_list.append(best_config.mass())
    return dim_list, sorted(mass_list)


# Loads not taking into account the moment generated
g = 9.81
rtg_mass = 97.8
number_of_rtgs = 3
accelerations = np.array([2, 6, 2])
loads = rtg_mass / number_of_rtgs * g * accelerations

# Possible materials
aluminium = Material(
    name='aluminium',
    Youngs_Modulus=75*10**9,
    yield_stress=265*10**6,
    shear_modulus=24*10**9,
    maximum_shear=207*10**6,
    max_bearing_stress=1.6*265*10**6,
    density=2700
)
iron = Material(
    name='iron',
    Youngs_Modulus=175*10**9,
    yield_stress=465*10**6,
    shear_modulus=41*10**9,
    maximum_shear=0.6*465*10**6,
    max_bearing_stress=1.5*465*10**6,
    density=7200
)
steel = Material(
    name='steel',
    Youngs_Modulus=210*10**9,
    yield_stress=800*10**6,
    shear_modulus=77*10**9,
    maximum_shear=600*10**6,
    max_bearing_stress=185*10**6,
    density=7850
)
material_dict = {'aluminum': aluminium, 'iron': iron, 'steel': steel}
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
# Obtained from BDCB-13 -- https://www.hydrauliccylindersinc.com/product/clevis-bracket/
w_initial = 0.04445
t_initial = 0.01
d_initial = 0.034925
l_initial = 0.041275

flange = Flange(
    width=w_initial,
    lug_thickness=t_initial,
    hinge_diameter=d_initial,
    material=material_dict['aluminum'],
    length=l_initial
)

clearance = 0.0516128
lug = Lug(flange=flange, separation=clearance, number=2)

separation = 0.56
distance_to_rtgs_cg = 0.38
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

m, f = iterate_2(dlug=d_2)
print('(w, t, d, l)' + str(f.get_dimensions()) + ' has a mass of ' + str(m) + ' kg')
