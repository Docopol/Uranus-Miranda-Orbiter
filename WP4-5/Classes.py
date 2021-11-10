import math
import numpy as np


class Lug:
    def __init__(self, width, lug_thickness, hinge_diameter, material, length=0):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter
        self.m = material
        self.l = length

    def K_br(self):
        k = round(self.d/self.t)
        if k<2:
            k = 2
        elif k>10:
            k = 5*round(k/5)

        c = self.w / (2 * self.d)
        # Nested ifs for the functions and then return value


    def minimum_t(self, load):
        fx, fy, fz = load

        # Failure due to tensile forces - Extracted from Bruhn
        def t_yield_z():
            area = (self.w-self.d)  # per unit thickness
            return fz / (self.m.get_stress() * area)

        def t_bearing():
            safety_margin = 1.5
            return safety_margin * fz / (self.m.get_bear() * self.d)

        def t_shear():
            area = 2*math.sqrt((self.w/2)**2 + (self.d/2)**2)  # conservative estimate - per unit thickness
            return fz / (self.m.get_shear() * area)

        t1 = t_yield_z()
        t2 = t_bearing()
        t3 = t_shear()

        # Failure due to vertical forces - assuming bending is negligible
        t4 = (6 * self.l * fy / self.m.get_stress())**(1/3)

        thickness = sorted([t1, t2, t3, t4])
        return thickness[3]

    def minimum_d(self, load):
        fx, fy, fz = load

        # Failure due to tensile forces - Extracted from Bruhn
        def t_yield_z():
            return fz / (self.m.get_stress() * self.t) + self.w

        def t_bearing():
            safety_margin = 1.5
            return safety_margin * fz / (self.m.get_bear() * self.t)

        def t_shear():
            return math.sqrt(self.w**2 - 4*(fz/self.m.get_shear)**2)

        d1 = t_yield_z()
        d2 = t_bearing()
        d3 = t_shear()

        diameters = sorted([d1, d2, d3])
        return diameters[2]

    def mass(self):
        area = math.pi * ((self.w/2)**2 - (self.d/2)**2) + self.w * self.l
        volume = area * self.t
        return volume * self.m.get_density()


class Multi_lug:  # Assumes flange separation will be the same and flanges will be identical
    def __init__(self, lug, separation, number):
        self.l = lug
        self.n = number
        self.h = separation

    def minimum_t(self, loads):
        fx, fy, fz = load
        fx = fx/self.n
        fy = fy/self.n
        fz = fz/self.n
        return self.l.minimum_t((fx, fy, fz))

    def minimum_d(self, loads):
        fx, fy, fz = load
        fx = fx / self.n
        fy = fy / self.n
        fz = fz / self.n
        return self.l.minimum_d((fx, fy, fz))

    def mass(self):
        return self.l.mass() * self.n


class D_lug:   # A double lug
    def __init__(self, lug, separation):
        self.l = lug
        self.h = separation

    def min_t(self, loads):
        fx, fy, fz = load
        fx = fx/2
        fy = fy/2
        fz = fz/2
        return self.l.minimum_t((fx, fy, fz))

    def min_d(self, loads):
        fx, fy, fz = load
        fx = fx/2
        fy = fy/2
        fz = fz/2
        return self.l.minimum_d((fx, fy, fz))

    def mass(self):
        return self.l.mass() * 2


class Material:
    def __init__(self, Youngs_Modulus, critical_stress, shear_modulus, maximum_shear, max_bearing_stress, density):
        self.e = Youngs_Modulus
        self.cr = critical_stress
        self.g = shear_modulus
        self.sh = maximum_shear
        self.bear = max_bearing_stress
        self.d = density

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

    def get_density(self):
        return self.d


class Plate:
    def __init__(self, number_fasteners, fastener_diameter, plate_thickness):
        self.n = number_fasteners
        self.d = fastener_diameter
        self.t = plate_thickness

#Assuming the fastener diameters (D1) are the same

    def get_cg(self, coords):
        # coords format: [np.array([1, 2]), np.array([2, 3])]
        p = coords
        tot = np.array([0, 0])
        for i in coords:
            tot += i
        centre = tot / len(coords)
        return centre
