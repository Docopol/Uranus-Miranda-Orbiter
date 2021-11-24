class Material:
    def __init__(self, name, Youngs_Modulus, yield_stress, shear_modulus, maximum_shear, max_bearing_stress, density):
        self.n = name
        self.e = Youngs_Modulus
        self.y = yield_stress
        self.g = shear_modulus
        self.sh = maximum_shear
        self.bear = max_bearing_stress
        self.d = density

    def get_stress(self):
        return self.y

    def get_name(self):
        return self.n

    def get_E(self):
        return self.e

    def get_G(self):
        return self.g

    def get_shear(self):
        return self.sh

    def get_bear(self):
        return self.bear

    def get_density(self):
        return self.d


Al2014T6 = Material(
    name='Al2014-T6',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800
)
Al7075T6 = Material(
    name='Al7075-T6',
    Youngs_Modulus=71.7 * 10 ** 9,
    yield_stress=503 * 10 ** 6,
    shear_modulus=26.9 * 10 ** 9,
    maximum_shear=331 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,  # NOT FOUND
    density=2810
)
Al2024T3 = Material(
    name='Al2024-T3',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=345 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=283 * 10 ** 6,
    max_bearing_stress=524 * 10 ** 6,
    density=2780
)
Al2024T4 = Material(
    name='Al2024T4',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=324 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=283 * 10 ** 6,
    max_bearing_stress=441 * 10 ** 6,
    density=2780
)
# Steel
St8630 = Material(
    name='St8630',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800
)
St4130 = Material(
    name='St4130',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800
)
# Titanium
Ti6Al4v = Material(
    name='Ti6Al4v',
    Youngs_Modulus=113.8 * 10 ** 9,
    yield_stress=880 * 10 ** 6,
    shear_modulus=44 * 10 ** 9,
    maximum_shear=550 * 10 ** 6,
    max_bearing_stress=1860 * 10 ** 6,
    density=4430
)
#http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MTP641

# Magnesium
MgAZ91CT6 = Material(
    name='MgAZ91C-T6',
    Youngs_Modulus=44.8 * 10 ** 9,
    yield_stress=145 * 10 ** 6,
    shear_modulus=17 * 10 ** 9,
    maximum_shear=145 * 10 ** 6,
    max_bearing_stress=360 * 10 ** 6,
    density=1810
)
"""
# more materials
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
"""


#Standart Metric Bolt diameters in mm (Bolt D, Nut D)
bolt_D_standarts = (
(1.6,3.02),
(2,3.82),
(2.5,4.82),
(3,5.32),
(3.5,5.82),
(4,6.78),
(5,7.78),
(6,9.78),
(8,12.73),
(10,15.73),
(12,17.73),
(14,20.67),
(16,23.67),
(20,29.16),
(24,35),
(30,45),
)
