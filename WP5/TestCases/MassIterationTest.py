#Test case for the mass iteration of the tank

import sys

sys.path.insert(0, '../')

from materials import material_dict
from tank import Tank

testTank = Tank(1, 1e-3, 1e-3, material_dict["Al2014T6"], 13.99, 3e6)

initialTank = Tank(1, 1e-3, 1e-3, material_dict["Al2014T6"], 13.99, 1e7)

testTank.MassOptimization(testTank)