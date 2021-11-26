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

    def get_bear(self, safety_factor=1):
        return self.bear/safety_factor

    def get_density(self):
        return self.d

    def get_TEC(self):
        return self.t


Al2014T6 = Material( #done
    name='Al2014-T6',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=414 * 10 ** 6,
    ultimate_stress=483 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=290 * 10 ** 6,
    max_bearing_stress=662 * 10 ** 6,
    density=2800,
    TEC=23 * 10 ** -6
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

Al2024T3 = Material( # done
    name='Al2024-T3',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=345 * 10 ** 6,
    ultimate_stress=483 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=283 * 10 ** 6,
    max_bearing_stress=524 * 10 ** 6,
    density=2780,
    TEC=23.2 * 10 ** -6
)

Al2024T4 = Material( # done
    name='Al2024-T4',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=324 * 10 ** 6,
    ultimate_stress=469 * 10 ** 6,
    shear_modulus=28 * 10 ** 9,
    maximum_shear=283 * 10 ** 6,
    max_bearing_stress=441 * 10 ** 6,
    density=2780,
    TEC=23.2 * 10 ** -6
)

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
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=8570d3599b5e439391f3c1602e31d0bd

St4130 = Material( # still NEEDS TO BE DONE
    name='St4130',
    Youngs_Modulus=205 * 10 ** 9,
    yield_stress=435 * 10 ** 6,
    ultimate_stress=670 * 10 ** 6,
    shear_modulus=80 * 10 ** 9,
    maximum_shear=1 * 10 ** 6, # ???
    max_bearing_stress=1 * 10 ** 6, # ???
    density=7850,
    TEC=1 * 10 ** -6 # ???
)
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=e1ccebe90cf94502b35c2a4745f63593

Ti6Al4v = Material( # done
    name='Ti-6Al-4v',
    Youngs_Modulus=113.8 * 10 ** 9,
    yield_stress=880 * 10 ** 6,
    ultimate_stress=950 * 10 ** 6,
    shear_modulus=44 * 10 ** 9,
    maximum_shear=550 * 10 ** 6,
    max_bearing_stress=1860 * 10 ** 6,
    density=4430,
    TEC=8.6 * 10 ** -6
)
#http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MTP641

MgAZ91CT6 = Material( # done
    name='MgAZ91C-T6',
    Youngs_Modulus=17 * 10 ** 9,
    yield_stress=150 * 10 ** 6,
    ultimate_stress=275 * 10 ** 6,
    shear_modulus=17 * 10 ** 9,
    maximum_shear=145 * 10 ** 6,
    max_bearing_stress=360 * 10 ** 6,
    density=1810,
    TEC=26 * 10 ** -6
)
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=8c8cad8fe20544508f41b4a1300af4a1

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
                 'St8630': St8630, 'St4130': St4130, 'MgAZ91CT6': MgAZ91CT6, 'Ti6Al4v': Ti6Al4v}

# Standard Metric Bolt diameters in mm (Bolt D, Nut D, Nut thickness)
bolt_D_standarts = (
(1.6,3.02,0.048),
(2,3.82,0.05),
(2.5,4.82,0.0525),
(3,5.32,0.055),
(3.5,5.82,0.0575),
(4,6.78,0.06),
(5,7.78,0.07),
(6,9.78,0.093),
(8,12.73,0.11),
(10,15.73,0.12),
(12,17.73,0.155),
#(14,20.67),
#(16,23.67),
#(20,29.16),
#(24,35),
#(30,45),
)


magic_Ratio = 1.10266