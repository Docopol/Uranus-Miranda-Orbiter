class Lug:
    def __init__(self, width, lug_thickness, hinge_diameter, material):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter
        self.m = material


class multi_Lug(Lug):  # Assumes lug separation will be the same and lugs will be identical
    def __init__(self, width, lug_thickness, hinge_diameter, material, separation, number):
        Lug.__init__(self, width, lug_thickness, hinge_diameter, material)
        self.n = number
        self.h = separation


class Material:
    def __init__(self, Youngs_Modulus, critical_stress):
        self.e = Youngs_Modulus
        self.cr = critical_stress
