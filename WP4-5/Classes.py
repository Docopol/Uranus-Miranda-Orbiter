import math

class Lug:
    def __init__(self, width, lug_thickness, hinge_diameter, material):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter
        self.m = material


    def minimum_t(self, load):
        fx, fy, fz = load

        # Failure due to tensile forces - Extracted from Bruhn
        def t_yield_z():
            area = (self.w-self.d)  # per unit thickness
            return fz / (self.m.get_stress() * area)

        def t_bearing():
            return fz / (self.m.get_bear() * self.d)

        def t_shear():
            area = 2*math.sqrt((self.w/2)**2 + (self.d/2)**2)  # conservative estimate - per unit thickness
            return fz / (self.m.get_shear() * area)

        t1 = t_yield_z()
        t2 = t_bearing()
        t3 = t_shear()

        thickness = sorted([t1, t2, t3])
        return thickness[2]


class multi_Lug:  # Assumes lug separation will be the same and lugs will be identical
    def __init__(self, lug, separation, number):
        self.l = lug
        self.n = number
        self.h = separation


class D_lug:
    def __init__(self, lug, separation):
        self.l = lug
        self.h = separation


class Material:
    def __init__(self, Youngs_Modulus, critical_stress, shear_modulus, maximum_shear, max_bearing_stress):
        self.e = Youngs_Modulus
        self.cr = critical_stress
        self.g = shear_modulus
        self.sh = maximum_shear
        self.bear = max_bearing_stress

    def get_stress(self):
        return self.cr

    def get_E(self):
        return self.E

    def get_G(self):
        return self.g

    def get_shear(self):
        return self.sh

    def get_bear(self):
        return self.bear
