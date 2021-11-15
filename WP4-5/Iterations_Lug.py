from Classes import Flange, Lug, Double_lug, Material
import numpy as np

# Loads not taking into account the moment generated
g = 9.81
rtg_mass = 97.8
number_of_rtgs = 3
accelerations = np.array([2, 6, 2])
loads = rtg_mass / number_of_rtgs * g * accelerations

# Possible materials
aluminium = Material(
    Youngs_Modulus=75*10**9,
    yield_stress=265*10**6,
    shear_modulus=24*10**9,
    maximum_shear=207*10**6,
    max_bearing_stress=1.6*265*10**6,
    density=2700
)
iron = Material(
    Youngs_Modulus=175*10**9,
    yield_stress=465*10**6,
    shear_modulus=41*10**9,
    maximum_shear=0.6*465*10**6,
    max_bearing_stress=1.5*465*10**6,
    density=7200
)
steel = Material(
    Youngs_Modulus=210*10**9,
    yield_stress=800*10**6,
    shear_modulus=77*10**9,
    maximum_shear=600*10**6,
    max_bearing_stress=185*10**6,
    density=7850
)
material_dict = {'aluminum':aluminium, 'iron':iron, 'steel':steel}
"""
Sources:
https://curioustab.com/discuss/69852/the-permissible-bearing-stress-in-steel-is/#:~:text=The%20permissible%20bearing%20stress%20in,cm2%201890%20kg%2Fcm2%2020
https://www.google.com/search?q=allowable+bearing+stress+iron&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvLo5VnrRwZI7eBvUAnnnDBd1mk55w%3A1636985183684&ei=X2mSYeiTKczSkwWivI1I&oq=allowable+bearing+stress+iron&gs_lcp=Cgdnd3Mtd2l6EAMyCAghEBYQHRAeOgcIIxCwAxAnOgUIABDLAToGCAAQFhAeSgQIQRgBUJMHWIkKYKILaAJwAHgAgAFIiAGQApIBATSYAQCgAQHIAQHAAQE&sclient=gws-wiz&ved=0ahUKEwiov4CDxZr0AhVM6aQKHSJeAwkQ4dUDCA4&uact=5
https://docshare.tips/allowable-bearing-stress-for-aluminum-alloys_58424f00b6d87f9e1d8b473c.html
https://www.google.com/search?q=maximum+shear+stress+steel&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvKys7p3IPuX1XAvpnA1pmuqUt5FKg%3A1636984953197&ei=eWiSYce1C7GCi-gPxoqx0Ak&oq=maximum+shear+stress+steel&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEMsBMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeOgcIABBHELADSgQIQRgAUMIEWKoKYPoLaAJwAngAgAF_iAGhA5IBAzQuMZgBAKABAcgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwiH1oyVxJr0AhUxwQIHHUZFDJoQ4dUDCA4&uact=5
https://www.google.com/search?q=maximum+shear+stress+iron&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvJJ31XwsRHQHeeMz_7lLYEnshcp1A%3A1636984917313&ei=VWiSYY-5Eo2-kwWQ3rv4AQ&oq=maximum+shear+stress+iron&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEBYQHjoHCCMQsAMQJzoHCAAQRxCwAzoFCAAQywFKBAhBGABQ8gZYyAlgkQtoAnACeACAAZoBiAH0ApIBAzMuMZgBAKABAcgBCcABAQ&sclient=gws-wiz&ved=0ahUKEwjPt_6DxJr0AhUN36QKHRDvDh8Q4dUDCA4&uact=5
https://www.google.com/search?q=maximum+shear+stress+aluminium&rlz=1C1CHBF_esNL918NL918&sxsrf=AOaemvL6f4sO_Uth-ciGNgZ4dQbVEi42OQ%3A1636984828892&ei=_GeSYevqNZLqkgWRuLTYDw&oq=maximum+shear+stress+a&gs_lcp=Cgdnd3Mtd2l6EAMYADIGCCMQJxATMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBOgcIIxCwAxAnOgcIABBHELADOgQIIxAnOgQIABBDOgUIABCABDoLCC4QgAQQxwEQ0QM6CwguEIAEEMcBEKMCOgsILhCABBDHARCvAToFCC4QgAQ6BQguEMsBOgsILhDHARCvARDLAUoECEEYAFCAxgRY2O8EYJH4BGgEcAJ4AIABgAGIAesPkgEEMjAuNJgBAKABAcgBCcABAQ&sclient=gws-wiz
Materials Book
"""


# First level estimation of dimensions
w_initial = int()
t_initial = int()
d_initial = int()
l_initial = int()

flange = Flange(width=w_initial,
                    lug_thickness=t_initial,
                    hinge_diameter=d_initial,
                    material=material_dict['aluminum'],
                    length=l_initial)

f1_dimensions = iterate(flange) # first iteration for one flange

clearance = int()
f2 = Lug(flange=flange, separation=clearance, number=2)

