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


    def get_stress(self, safety_factor=1):
        return self.y/safety_factor

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


Al2014T6 = Material(        # done
    name='Al2014-T6',
    Youngs_Modulus=73.1e9,
    yield_stress=414e6,
    ultimate_stress=483e6,  # not used so not correct value
    shear_modulus=28e9,     # not used so not correct value
    maximum_shear=290e6,    # not used so not correct value
    max_bearing_stress=662e6,    # not used so not correct value
    density=2790,
    TEC=23e-6
)

Al6061T6 = Material(        # done
    name='Al6061-T6',
    Youngs_Modulus=68.9e9,
    yield_stress=255e6,
    ultimate_stress=483e6,  # not used so not correct value
    shear_modulus=28e9,     # not used so not correct value
    maximum_shear=290e6,    # not used so not correct value
    max_bearing_stress=662e6,   # not used so not correct value
    density=2710,
    TEC=24e-6
)

MgAM60 = Material(        # done
    name='Mg-Am60',
    Youngs_Modulus=45e9,
    yield_stress=130e6,
    ultimate_stress=483e6,  # not used so not correct value
    shear_modulus=28e9,     # not used so not correct value
    maximum_shear=290e6,    # not used so not correct value
    max_bearing_stress=662e6,   # not used so not correct value
    density=1800,
    TEC=26e-6
)

StA992 = Material(        # done
    name='St-A992',
    Youngs_Modulus=200e9,
    yield_stress=345e6,
    ultimate_stress=483e6,  # not used so not correct value
    shear_modulus=28e9,     # not used so not correct value
    maximum_shear=290e6,    # not used so not correct value
    max_bearing_stress=662e6,   # not used so not correct value
    density=7850,
    TEC=12e-6
)

Al7075T6 = Material( # done
    name='Al7075-T6',
    Youngs_Modulus=71.7 * 10 ** 9,
    yield_stress=503 * 10 ** 6,
    ultimate_stress=572 * 10 ** 6,
    shear_modulus=26.9 * 10 ** 9,
    maximum_shear=331 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,  # NOT FOUND
    density=2810,
    TEC=23.6 * 10 ** -6
)

# Al2024T3 = Material( # done
#     name='Al2024-T3',
#     Youngs_Modulus=73.1 * 10 ** 9,
#     yield_stress=345 * 10 ** 6,
#     ultimate_stress=483 * 10 ** 6,
#     shear_modulus=28 * 10 ** 9,
#     maximum_shear=283 * 10 ** 6,
#     max_bearing_stress=524 * 10 ** 6,
#     density=2780,
#     TEC=23.2 * 10 ** -6
# )
#
# Al2024T4 = Material( # done
#     name='Al2024-T4',
#     Youngs_Modulus=73.1 * 10 ** 9,
#     yield_stress=324 * 10 ** 6,
#     ultimate_stress=469 * 10 ** 6,
#     shear_modulus=28 * 10 ** 9,
#     maximum_shear=283 * 10 ** 6,
#     max_bearing_stress=441 * 10 ** 6,
#     density=2780,
#     TEC=23.2 * 10 ** -6
# )

St8630 = Material(
    name='St8630',
    Youngs_Modulus=187 * 10 ** 9,
    yield_stress=550 * 10 ** 6,
    ultimate_stress=620 * 10 ** 6,
    shear_modulus=72 * 10 ** 9,
    maximum_shear=1 * 10 ** 6, # ???
    max_bearing_stress=1 * 10 ** 6, # ??? I really have no idea where to find this anymore
    density=7850,
    TEC=11.2 * 10 ** -6
)
St4130 = Material(
    name='St4130',
    Youngs_Modulus=190 * 10 ** 9,
    yield_stress=460 * 10 ** 6,
    ultimate_stress=560 * 10 ** 6,
    shear_modulus=80 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,# ???
    max_bearing_stress=662 * 10 ** 6,# ???
    density=7850,
    TEC=25.2 * 10 ** -6
)
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=e1ccebe90cf94502b35c2a4745f63593

Ti6Al4V = Material(         # done
    name='Ti-6Al-4V',
    Youngs_Modulus=120e9,
    yield_stress=924e6,
    ultimate_stress=950e6,      # not used so not correct value
    shear_modulus=44e9,         # not used so not correct value
    maximum_shear=550e6,        # not used so not correct value
    max_bearing_stress=1860e6,  # not used so not correct value
    density=4430,
    TEC=9.4e-6
)
#http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MTP641

MgAZ91CT6 = Material( # done
    name='MgAZ91C-T6',
    Youngs_Modulus=44.8 * 10 ** 9,
    yield_stress=145 * 10 ** 6,
    ultimate_stress=275 * 10 ** 6,
    shear_modulus=17 * 10 ** 9,
    maximum_shear=145 * 10 ** 6,
    max_bearing_stress=360 * 10 ** 6,
    density=1810,
    TEC=26 * 10 ** -6
)
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=8c8cad8fe20544508f41b4a1300af4a1


# material_dict = {'Al2014T6': Al2014T6, 'Al7075T6': Al7075T6, 'Al2024T3': Al2024T3, 'Al2024T4': Al2024T4,
#                  'St8630': St8630, 'St4130': St4130, 'MgAZ91CT6': MgAZ91CT6, 'Ti6Al4v': Ti6Al4v}

# Standard Metric Bolt diameters  (Bolt D, Nut D, Nut height, pitch)
bolt_D_standarts = (
(1.6,3.02,0.5,0.35),
(2,3.82,1.3,0.4),
(2.5,4.82,1.7,0.45),
(3,5.32,2,0.5),
#(3.5,5.82,0.0575),
(4,6.78,2.8,0.7),
(5,7.78,3.5,0.8),
(6,9.78,4,1),
(8,12.73,5.3,1.25),
(10,15.73,6.4,1.5),
(12,17.73,7.5,1.75),
#(14,20.67,8.8),
#(16,23.67,10),
#(20,29.16,12.5),
#(24,35,15),
#(30,45,18.7),
)


magic_Ratio = 1.10266