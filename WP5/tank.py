import calc, constants

class tank(self, diameter, length, thickness, material):
	self.d = diameter
	self.l = length
	self.t = thickness
	self.mat = material

	def InnerPressureFailure(self):
		radialBurstPressure = self.material["yield_stress"]
