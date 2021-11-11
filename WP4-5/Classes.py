import math
import numpy as np


class Flange:
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

        x = self.w / (2 * self.d)
        # Polynomials are wrong, need to be changed.
        if k == 2:
            return -0.0065*x**6 + 0.099*x**5 - 0.6121*x**4 + 1.9956*x**3 - 3.8136*x**2 + 5.0505*x - 1.8379
        elif k == 3:
            return -0.0113*x**6 + 0.167*x**5 - 0.9829*x**4 + 2.9662*x**3 - 5.0921*x**2 + 5.85*x - 2.0225
        elif k == 4:
            return -0.012*x**6 + 0.1681*x**5 - 0.9298*x**4 + 2.6434*x**3 - 4.42*x**2 + 5.2851*x - 1.861
        elif k == 5:
            return -0.0053*x**6 + 0.073*x**5 - 0.4008*x**4 + 1.203*x**3 - 2.4694*x**2 + 4.0522*x - 1.5765
        elif k == 6:
            return -0.0025*x**6 + 0.0362*x**5 - 0.221*x**4 + 0.8136*x**3 - 2.1579*x**2 + 4.0147*x - 1.6038
        elif k == 7:
            return 0.0021*x**6 - 0.0227*x**5 + 0.0579*x**4 + 0.2253*x**3 - 1.6628*x**2 + 3.889*x - 1.6119
        elif k == 8:
            return 0.0087*x**6 - 0.1071*x**5 + 0.4641*x**4 - 0.6625*x**3 - 0.8352*x**2 + 3.5981*x - 1.5915
        elif k == 9:
            return 0.0029*x**6 - 0.0233*x**5 - 0.0226*x**4 + 0.7597*x**3 - 2.9987*x**2 + 5.0998*x - 1.9599
        elif k == 10:
            return -0.001*x**6 + 0.04*x**5 - 0.4264*x**4 + 2.047*x**3 - 5.0972*x**2 + 6.6263*x - 2.3538
        elif k == 15:
            return -0.0246*x**6 + 0.3572*x**5 - 2.069*x**4 + 6.1293*x**3 - 9.9355*x**2 + 8.6779*x - 2.5356
        elif k == 20:
            return -0.0092*x**6 + 0.1363*x**5 - 0.8148*x**4 + 2.5231*x**3 - 4.3542*x**2 + 4.1361*x - 1.2611
        elif k == 25:
            return -0.0092*x**6 + 0.1363*x**5 - 0.8148*x**4 + 2.5231*x**3 - 4.3542*x**2 + 4.1361*x - 1.2611
        elif k == 30:
            return -0.0076*x**6 + 0.1131*x**5 - 0.6773*x**4 + 2.0967*x**3 - 3.6146*x**2 + 3.4374*x - 1.0535


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


class Lug:  # Assumes flange separation will be the same and flanges will be identical
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


class Double_lug:   # A double lug
    def __init__(self, flange, separation):
        self.f = flange
        self.h = separation

    def min_t(self, loads):
        fx, fy, fz = load
        fx = fx/2
        fy = fy/2
        fz = fz/2
        return self.f.minimum_t((fx, fy, fz))

    def min_d(self, loads):
        fx, fy, fz = load
        fx = fx/2
        fy = fy/2
        fz = fz/2
        return self.f.minimum_d((fx, fy, fz))

    def mass(self):
        return self.f.mass() * 2


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

    # Assuming the fastener diameters (D1) are the same

    def get_cg(self, coords):  # coords format: [[x1,y1],[x2,y2]]
        copy = []
        for i in coords:
            copy.append(np.asarray(i))
        coords = copy
        return list(sum(coords) / len(coords)) # the output format: [x,y]

