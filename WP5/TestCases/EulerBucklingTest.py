#Test case for the Euler buckling calculation of the tank

import sys

sys.path.insert(0, '../')

from materials import material_dict
from tank import Tank

testTank = Tank(1, 1, 1e-3, 1e-3, material_dict["Al2014T6"], 1e7)

print(testTank.EulerColumnBucklingF())
print(testTank.EulerColumnBucklingF(1, 1, 1e-3, 1e-3, material_dict["Al2014T6"]))