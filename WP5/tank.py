import materials, standards
import numpy as np

class Tank(self, radius, length, thickness1, thickness2, material):
	def __init__(self):
		self.r = radius
		self.l = length
		self.t1 = thickness1
		self.t2 = thickness2
		self.mat = material

	def InnerPressureF(self, radius, length, thickness1, thickness2, material):
		radialBurstPressureCyl = material["t_yield_stress"]*thickness1/radius
		radialBurstPressureEnd = material["t_yield_stress"]*thickness2/radius

		failurePressure = np.minimum(radialBurstPressureCyl, radialBurstPressureCyl)

		return failurePressure

	def EulerColumnBucklingF(self, radius, length, thickness1, thickness2, material):
		ICylinder = np.pi/4*(radius**4-(radius-thickness1)**4)
		areaCylinder = np.pi*radius**2
		criticalStressE = ((np.pi**2)*material["E_modulus"]*ICylinder)/(areaCylinder*length**2)

		return criticalStressE

	def ShellBuckling(self):
		continue
