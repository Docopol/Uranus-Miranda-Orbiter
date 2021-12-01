import materials, standards, Forces_FBD
import numpy as np
from scipy.optimize import minimize

class Tank:
	def __init__(self, radius, length, thickness1, thickness2, material):
		self.r = radius
		self.l = length
		self.t1 = thickness1
		self.t2 = thickness2
		self.mat = material

	def InnerPressureF(self, radius=None, length=None, thickness1=None, thickness2=None, material=None):
		if(radius != None):
			radialBurstPressureCyl = material["t_yield_stress"]*thickness1/radius
			radialBurstPressureEnd = material["t_yield_stress"]*thickness2/radius
		else:
			radialBurstPressureCyl = self.mat["t_yield_stress"]*self.t1/self.r
			radialBurstPressureEnd = self.mat["t_yield_stress"]*self.t2/self.r

		failurePressure = np.minimum(radialBurstPressureCyl, radialBurstPressureCyl)

		return failurePressure

	def EulerColumnBucklingF(self, radius=None, length=None, thickness1=None, thickness2=None, material=None):
		if(radius != None):
			ICylinder = np.pi/4*(radius**4-(radius-thickness1)**4)
			areaCylinder = np.pi*radius**2
			criticalStressE = ((np.pi**2)*material["E_modulus"]*ICylinder)/(areaCylinder*length**2)
		else:
			ICylinder = np.pi/4*(self.r**4-(self.r-self.t1)**4)
			areaCylinder = np.pi*self.r**2
			criticalStressE = ((np.pi**2)*self.mat["E_modulus"]*ICylinder)/(areaCylinder*self.l**2)

		return criticalStressE

	def ShellBuckling(self, pressure, radius=None, length=None, thickness1=None, material=None):
		if(radius != None):
			k = lambda fLambda : fLambda + (12*L**4)/(np.pi**4*radius**2*thickness1**2)*(1-material["poisson_ratio"]**2)/fLambda
			bestLambda = minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": True}).x
			Q = pressure/material["E_modulus"]*(radius/thickness1)**2
			criticalStressS = (1.983-0.983*np.exp**(-23.14*Q))*bestLambda*(np.pi**2*material["E_modulus"]/(12*(1-materia["poisson_ratio"]**2)))*(thickness1/length)**2
		else:
			k = lambda fLambda : fLambda + (12*L**4)/(np.pi**4*self.r**2*self.t1**2)*(1-self.mat["poisson_ratio"]**2)/fLambda
			bestLambda = minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": True}).x
			Q = pressure/self.mat["E_modulus"]*(self.r/self.t1)**2
			criticalStressS = (1.983-0.983*np.exp**(-23.14*Q))*bestLambda*(np.pi**2*self.mat["E_modulus"]/(12*(1-self.mat["poisson_ratio"]**2)))*(self.t1/self.l)**2

		return criticalStressS


