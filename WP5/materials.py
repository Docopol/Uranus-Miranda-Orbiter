Al2014T6 = {        # done
    "name": 'Al2014-T6',
    "E_modulus": 73.1e9,
    "t_yield_stress": 414e6,
    "poisson_ratio": 0.33,
    "density": 2790,
    "TEC": 23e-6
}

Al6061T6 = {        # done
    "name": 'Al6061-T6',
    "E_modulus": 68.9e9,
    "t_yield_stress": 255e6,
    "poisson_ratio": 0.33,
    "density": 2710,
    "TEC": 24e-6
}

Al2219T6 = {        # done
    "name": 'Al2219-T6',
    "E_modulus": 72e9,
    "t_yield_stress": 280e6,
    "poisson_ratio": 0.33,
    "density": 2840,
    "TEC": 22e-6
}

Al7075T6 = {        # done
    "name": 'Al7075-T6',
    "E_modulus": 71.7e9,
    "t_yield_stress": 503e6,
    "poisson_ratio": 0.33,
    "density": 2810,
    "TEC": 23.6e-6
}

# MgAM60 = {
#     "name": 'Mg-Am60',
#     "E_modulus": 45e9,
#     "t_yield_stress": 130e6,
#     "poisson_ratio": 0.35,
#     "density": 1800,
#     "TEC": 26e-6
# }

StA992 = {
    "name": 'St-A992',
    "E_modulus": 200e9,
    "t_yield_stress": 345e6,
    "poisson_ratio": 0.28,
    "density": 7850,
    "TEC": 12e-6
}

SS301 = {
    "name": 'SS-301',
    "E_modulus": 200e9,
    "t_yield_stress": 1080e6,
    "poisson_ratio": 0.28,
    "density": 7800,
    "TEC": 17e-6
}



# Al2024T3 = {
#     "name": 'Al2024-T3',
#     "E_modulus": 73.1 * 10 ** 9,
#     "t_yield_stress": 345 * 10 ** 6,
#     "poisson_ratio": 0.33,
#     "density": 2780,
#     "TEC": 23.2 * 10 ** -6
# }

# Al2024T4 = { # done
#     "name":'Al2024-T4',
#     "E_modulus":73.1 * 10 ** 9,
#     "t_yield_stress":324 * 10 ** 6,
#     "density":2780,
#     "TEC":23.2 * 10 ** -6
# }
#
# St8630 = {
#     "name": 'St8630',
#     "E_modulus": 187 * 10 ** 9,
#     "t_yield_stress": 550 * 10 ** 6,
#     "poisson_ratio": 0.28,
#     "density": 7850,
#     "TEC": 11.2 * 10 ** -6
# }
# St4130 = {
#     "name": 'St4130',
#     "E_modulus": 190 * 10 ** 9,
#     "t_yield_stress": 460 * 10 ** 6,
#     "poisson_ratio": 0.28,
#     "density": 7850,
#     "TEC": 25.2 * 10 ** -6
# }
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=e1ccebe90cf94502b35c2a4745f63593

Ti6Al4V = {
    "name": 'Ti-6Al-4V',
    "E_modulus": 120e9,
    "t_yield_stress": 924e6,
    "poisson_ratio": 0.34,
    "density": 4430,
    "TEC": 9.4e-6
}

Ti5Al25Sn = {
    "name": 'Ti-5Al-2.5Sn',
    "E_modulus": 118e9,
    "t_yield_stress": 827e6,
    "poisson_ratio": 0.34,
    "density": 4480,
    "TEC": 9.4e-6
}
#http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MTP641

# MgAZ91CT6 = {
#     "name": 'MgAZ91C-T6',
#     "E_modulus": 44.8 * 10 ** 9,
#     "t_yield_stress": 145 * 10 ** 6,
#     "poisson_ratio": 0.35,
#     "density": 1810,
#     "TEC": 26 * 10 ** -6
# }
# http://www.matweb.com/search/DataSheet.aspx?MatGUID=8c8cad8fe20544508f41b4a1300af4a1

material_dict = {'Al2014T6': Al2014T6, 'Al7075T6': Al7075T6, 'Al6061T6': Al6061T6, 'MgAM60': MgAM60,
                 'StA992': StA992, 'St8630': St8630, 'St4130': St4130, 'MgAZ91CT6': MgAZ91CT6, 'Ti6Al4V': Ti6Al4V}
