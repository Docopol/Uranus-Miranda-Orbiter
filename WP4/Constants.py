class Material:
    def __init__(self, name, Youngs_Modulus, yield_stress, density, TEC):
        self.n = name
        self.e = Youngs_Modulus
        self.y = yield_stress
        self.d = density
        self.t = TEC  # Thermal Expansion Coefficient


    def get_stress(self, safety_factor=1):
        return self.y/safety_factor

    def get_name(self):
        return self.n

    def get_E(self):
        return self.e

    def get_density(self):
        return self.d

    def get_TEC(self):
        return self.t


Al2014T6 = Material(        # done
    name='Al2014-T6',
    Youngs_Modulus=73.1e9,
    yield_stress=414e6,
    density=2790,
    TEC=23e-6
)

Al6061T6 = Material(        # done
    name='Al6061-T6',
    Youngs_Modulus=68.9e9,
    yield_stress=255e6,
    density=2710,
    TEC=24e-6
)

MgAM60 = Material(        # done
    name='Mg-Am60',
    Youngs_Modulus=45e9,
    yield_stress=130e6,
    density=1800,
    TEC=26e-6
)

StA992 = Material(        # done
    name='St-A992',
    Youngs_Modulus=200e9,
    yield_stress=345e6,
    density=7850,
    TEC=12e-6
)

Al7075T6 = Material( # done
    name='Al7075-T6',
    Youngs_Modulus=71.7e9,
    yield_stress=503e6,
    density=2810,
    TEC=23.6e-6
)

Al2024T3 = Material( # done
    name='Al2024-T3',
    Youngs_Modulus=73.1 * 10 ** 9,
    yield_stress=345 * 10 ** 6,
    density=2780,
    TEC=23.2 * 10 ** -6
)

# Al2024T4 = Material( # done
#     name='Al2024-T4',
#     Youngs_Modulus=73.1 * 10 ** 9,
#     yield_stress=324 * 10 ** 6,
#     density=2780,
#     TEC=23.2 * 10 ** -6
# )

St8630 = Material(
    name='St8630',
    Youngs_Modulus=187 * 10 ** 9,
    yield_stress=550 * 10 ** 6,
    density=7850,
    TEC=11.2 * 10 ** -6
)
St4130 = Material(
    name='St4130',
    Youngs_Modulus=190 * 10 ** 9,
    yield_stress=460 * 10 ** 6,
    density=7850,
    TEC=25.2 * 10 ** -6
)
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=e1ccebe90cf94502b35c2a4745f63593

Ti6Al4V = Material(         # done
    name='Ti-6Al-4V',
    Youngs_Modulus=120e9,
    yield_stress=924e6,
    density=4430,
    TEC=9.4e-6
)
#http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MTP641

MgAZ91CT6 = Material( # done
    name='MgAZ91C-T6',
    Youngs_Modulus=44.8 * 10 ** 9,
    yield_stress=145 * 10 ** 6,
    density=1810,
    TEC=26 * 10 ** -6
)
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=8c8cad8fe20544508f41b4a1300af4a1


material_dict = {'Al2014T6': Al2014T6, 'Al7075T6': Al7075T6, 'Al6061T6': Al6061T6, 'MgAM60': MgAM60,
                 'StA992': StA992, 'St8630': St8630, 'St4130': St4130, 'MgAZ91CT6': MgAZ91CT6, 'Ti6Al4V': Ti6Al4V}

# Standard Metric Bolt diameters  (Bolt D, Nut D, Nut height, pitch)
bolt_D_standarts = (
(1.6, 3.02, 0.5, 0.35),
(2, 3.82, 1.3, 0.4),
(2.5, 4.82, 1.7, 0.45),
(3, 5.32, 2, 0.5),
(3.5,5.82,0.0575),
(4, 6.78, 2.8, 0.7),
(5, 7.78, 3.5, 0.8),
(6, 9.78, 4, 1),
(8, 12.73, 5.3, 1.25),
(10, 15.73, 6.4, 1.5),
(12, 17.73, 7.5, 1.75),
(14,20.67,8.8,2),
(16,23.67,10,2),
(20,29.16,12.5,2),
(24,35,15,2.5),
(30,45,18.7,2.5)
)


hex_circ_Ratio = 1.10266