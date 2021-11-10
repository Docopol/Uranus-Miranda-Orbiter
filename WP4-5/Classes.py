class Lug:
    def __init__(self, width, lug_thickness, hinge_diameter, material):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter
        self.m = material


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
    def __init__(self, Youngs_Modulus, critical_stress):
        self.e = Youngs_Modulus
        self.cr = critical_stress

    def get_stress(self):
        return self.cr

    def get_E(self):
        return self.E
