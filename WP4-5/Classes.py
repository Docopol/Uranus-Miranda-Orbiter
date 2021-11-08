class Lug:
    def __init__(self, width, lug_thickness, hinge_diameter):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter


class multi_Lug(Lug):  # Assumes lug separation will be the same and lugs will be identical
    def __init__(self, w, lug_t, diameter, separation, number):
        Lug.__init__(self, w, lug_t, diameter)
        self.n = number
        self.h = separation

