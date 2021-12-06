import materials, standards, Forces_FBD
import numpy as np
import scipy.optimize as sco

class Tank:
	def __init__(self, radius, length, thickness1, thickness2, material, pressure):
		self.r = radius
		self.l = length
		self.t1 = thickness1
		self.t2 = thickness2
		self.mat = material
		self.p = pressure

	# def InnerPressureF(self, radius=None, length=None, thickness1=None, thickness2=None, material=None):
	# 	if(radius != None):
	# 		radialBurstPressureCyl = material["t_yield_stress"]*thickness1/radius
	# 		radialBurstPressureEnd = material["t_yield_stress"]*thickness2/radius
	# 	else:
	# 		radialBurstPressureCyl = self.mat["t_yield_stress"]*self.t1/self.r
	# 		radialBurstPressureEnd = self.mat["t_yield_stress"]*self.t2/self.r

	# 	failurePressure = np.minimum(radialBurstPressureCyl, radialBurstPressureCyl)

	# 	return failurePressure

	# def EulerColumnBucklingF(self, radius=None, length=None, thickness1=None, thickness2=None, material=None):
	# 	if(radius != None):
	# 		ICylinder = np.pi/4*(radius**4-(radius-thickness1)**4)
	# 		areaCylinder = np.pi*radius**2
	# 		criticalStressE = ((np.pi**2)*material["E_modulus"]*ICylinder)/(areaCylinder*length**2)
	# 	else:
	# 		ICylinder = np.pi/4*(self.r**4-(self.r-self.t1)**4)
	# 		areaCylinder = np.pi*self.r**2
	# 		criticalStressE = ((np.pi**2)*self.mat["E_modulus"]*ICylinder)/(areaCylinder*self.l**2)

	# 	return criticalStressE

	# def ShellBuckling(self, pressure, radius=None, length=None, thickness1=None, material=None):
	# 	if(radius != None):
	# 		k = lambda fLambda : fLambda + (12*length**4)/(np.pi**4*radius**2*thickness1**2)*(1-material["poisson_ratio"]**2)/fLambda
	# 		bestLambda = sco.minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": True}).x
	# 		Q = pressure/material["E_modulus"]*(radius/thickness1)**2
	# 		criticalStressS = (1.983-0.983*np.exp(-23.14*Q))*bestLambda*(np.pi**2*material["E_modulus"]/(12*(1-material["poisson_ratio"]**2)))*(thickness1/length)**2
	# 	else:
	# 		k = lambda fLambda : fLambda + (12*self.l**4)/(np.pi**4*self.r**2*self.t1**2)*(1-self.mat["poisson_ratio"]**2)/fLambda
	# 		bestLambda = sco.minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": True}).x
	# 		Q = pressure/self.mat["E_modulus"]*(self.r/self.t1)**2
	# 		criticalStressS = (1.983-0.983*np.exp(-23.14*Q))*bestLambda*(np.pi**2*self.mat["E_modulus"]/(12*(1-self.mat["poisson_ratio"]**2)))*(self.t1/self.l)**2

	# 	return criticalStressS

	def InnerPressureF(self, params):
		if(params.all() != None):
			radius, length, thickness1, thickness2, tYieldStress, EMod, poissonR, pressure = params
			radialBurstPressureCyl = tYieldStress*thickness1/radius
			radialBurstPressureEnd = tYieldStress*thickness2/radius
		else:
			radialBurstPressureCyl = self.mat["t_yield_stress"]*self.t1/self.r
			radialBurstPressureEnd = self.mat["t_yield_stress"]*self.t2/self.r

		failurePressure = np.minimum(radialBurstPressureCyl, radialBurstPressureCyl)

		return failurePressure

	def EulerColumnBucklingF(self, params):
		if(params.all() != None):
			radius, length, thickness1, thickness2, tYieldStress, EMod, poissonR, pressure = params
			ICylinder = np.pi/4*(radius**4-(radius-thickness1)**4)
			areaCylinder = np.pi*radius**2
			criticalStressE = ((np.pi**2)*EMod*ICylinder)/(areaCylinder*length**2)
		else:
			ICylinder = np.pi/4*(self.r**4-(self.r-self.t1)**4)
			areaCylinder = np.pi*self.r**2
			criticalStressE = ((np.pi**2)*self.mat["E_modulus"]*ICylinder)/(areaCylinder*self.l**2)
		return criticalStressE

	def ShellBuckling(self, params):
		if(params.all() != None):
			radius, length, thickness1, thickness2, tYieldStress, EMod, poissonR, pressure = params
			k = lambda fLambda : fLambda + (12*length**4)/(np.pi**4*radius**2*thickness1**2)*(1-poissonR**2)/fLambda
			bestLambda = sco.minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": False}).x[0]
			Q = pressure/EMod*(radius/thickness1)**2
			criticalStressS = (1.983-0.983*np.exp(-23.14*Q))*bestLambda*(np.pi**2*EMod/(12*(1-poissonR**2)))*(thickness1/length)**2
		else:
			k = lambda fLambda : fLambda + (12*self.l**4)/(np.pi**4*self.r**2*self.t1**2)*(1-self.mat["poisson_ratio"]**2)/fLambda
			bestLambda = sco.minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": False}).x[0]
			Q = pressure/self.mat["E_modulus"]*(self.r/self.t1)**2
			criticalStressS = (1.983-0.983*np.exp(-23.14*Q))*bestLambda*(np.pi**2*self.mat["E_modulus"]/(12*(1-self.mat["poisson_ratio"]**2)))*(self.t1/self.l)**2

		return criticalStressS


	def MassOptimization(self, initialTank):
		for material in materials.material_dict.values():
			def Mass(variables): 
				radius, length, thickness1, thickness2, tYieldStress, EMod, poissonR, pressure = variables
				massConfiguration = (4*np.pi*radius**2*thickness2+2*np.pi*radius*length)*material["density"]

				return massConfiguration

			bounds = sco.Bounds([0.4, 0.4, 5e-5, 5e-5, material["t_yield_stress"], material["E_modulus"], material["poisson_ratio"], initialTank.p], [4, 20, 1e-1, 1e-1, material["t_yield_stress"], material["E_modulus"], material["poisson_ratio"], initialTank.p])

			def ConstrainF(variables):
				return [self.InnerPressureF(variables), self.EulerColumnBucklingF(variables), self.ShellBuckling(variables)]

			cons = sco.NonlinearConstraint(ConstrainF, [0, 1e8, 1e8], [5e7, np.inf, np.inf])
			
			res = sco.minimize(Mass, [1, 1, 1e-4, 1e-4, material["t_yield_stress"], material["E_modulus"], material["poisson_ratio"], initialTank.p], method="trust-constr", jac="2-point", hess = sco.SR1(), constraints=cons, options={'verbose':1}, bounds=bounds)

			print(res.x)

			print(Mass([1, 1, 1e-3, 1e-3, material["t_yield_stress"], material["E_modulus"], material["poisson_ratio"], initialTank.p]))