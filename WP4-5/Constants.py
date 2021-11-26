class Material:
    def __init__(self, name, Youngs_Modulus, yield_stress, ultimate_stress, shear_modulus, maximum_shear, max_bearing_stress, density, TEC):
        self.n = name
        self.e = Youngs_Modulus
        self.y = yield_stress
        self.u = ultimate_stress
        self.g = shear_modulus
        self.sh = maximum_shear
        self.bear = max_bearing_stress
        self.d = density
        self.t = TEC # Thermal Expansion Coefficient


    def get_stress(self):
        return self.y

    def get_u_stress(self):
        return self.u

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

    def get_TEC(self):
        return self.t


Al2014T6 = Material(
    name='Al2014-T6',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    ultimate_stress=483 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800,
    TEC=24.7 * 10 ** -6
)

Al7075T6 = Material(
    name='Al7075-T6',
    Youngs_Modulus=71.7 * 10 ** 9,
    yield_stress=503 * 10 ** 6,
    ultimate_stress=572 * 10 ** 6,
    shear_modulus=26.9 * 10 ** 9,
    maximum_shear=331 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,  # NOT FOUND
    density=2810,
    TEC=25.2 * 10 ** -6
)
Al2024T3 = Material(
    name='Al2024-T3',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=345 * 10 ** 6,
    ultimate_stress=483 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=283 * 10 ** 6,
    max_bearing_stress=524 * 10 ** 6,
    density=2780,
    TEC=24.7 * 10 ** -6
)
Al2024T4 = Material(
    name='Al2024-T4',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=324 * 10 ** 6,
    ultimate_stress=469 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=283 * 10 ** 6,
    max_bearing_stress=441 * 10 ** 6,
    density=2780,
    TEC=24.7 * 10 ** -6
)
# Steel #STILL NEEDS TO BE DONE
St8630 = Material(
    name='St8630',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    ultimate_stress=572 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800,
    TEC=25.2 * 10 ** -6
)
St4130 = Material(
    name='St4130',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    ultimate_stress=572 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800,
    TEC=25.2 * 10 ** -6
)
# Titanium  STILL NEEDS TO BE DONE
Ti6Al4v = Material(
    name='Ti-6Al-4v',
    Youngs_Modulus=113.8 * 10 ** 9,
    yield_stress=880 * 10 ** 6,
    ultimate_stress=572 * 10 ** 6,
    shear_modulus=44 * 10 ** 9,
    maximum_shear=550 * 10 ** 6,
    max_bearing_stress=1860 * 10 ** 6,
    density=4430,
    TEC=25.2 * 10 ** -6
)
#http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MTP641

# Magnesium STILL NEEDS TO BE DONE
MgAZ91CT6 = Material(
    name='MgAZ91C-T6',
    Youngs_Modulus=44.8 * 10 ** 9,
    yield_stress=145 * 10 ** 6,
    ultimate_stress=572 * 10 ** 6,
    shear_modulus=17 * 10 ** 9,
    maximum_shear=145 * 10 ** 6,
    max_bearing_stress=360 * 10 ** 6,
    density=1810,
    TEC=25.2 * 10 ** -6
)

# more materials
# aluminium = Material(
#     name='aluminium',
#     Youngs_Modulus=75*10**9,
#     yield_stress=265*10**6,
#     shear_modulus=24*10**9,
#     maximum_shear=207*10**6,
#     max_bearing_stress=1.6*265*10**6,
#     density=2700
# )
# iron = Material(
#     name='iron',
#     Youngs_Modulus=175*10**9,
#     yield_stress=465*10**6,
#     shear_modulus=41*10**9,
#     maximum_shear=0.6*465*10**6,
#     max_bearing_stress=1.5*465*10**6,
#     density=7200
# )
# steel = Material(
#     name='steel',
#     Youngs_Modulus=210*10**9,
#     yield_stress=800*10**6,
#     shear_modulus=77*10**9,
#     maximum_shear=600*10**6,
#     max_bearing_stress=185*10**6,
#     density=7850
# )


material_dict = {'Al2014T6': Al2014T6, 'Al7075T6': Al7075T6, 'Al2024T3': Al2024T3, 'Al2024T4': Al2024T4,
                 'St8630': St8630, 'St4130': St4130, 'MgAZ91CT6': MgAZ91CT6}

# Standart Metric Bolt diameters in mm (Bolt D, Nut D)
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
