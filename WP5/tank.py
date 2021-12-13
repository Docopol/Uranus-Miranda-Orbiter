import materials, standards, Forces_FBD
import numpy as np
import scipy.optimize as sco
import scipy.constants as cts


class Tank:
	def __init__(self, radius, thickness1, thickness2, material, volume, pressure):
		self.r = radius
		self.t1 = thickness1
		self.t2 = thickness2
		self.mat = material
		self.p = pressure
		self.v = volume

		self.m = 18119.35
		self.ay = cts.g*6
		self.ax = cts.g*2

	# def InnerPressureFCase(self, params, matProp):
	# 	if(params.all() != None):
	# 		radius, thickness1, thickness2 = params
	# 		tYieldStress, EMod, poissonR, volume, pressure = matProp

	# 		radialBurstPressureCyl = tYieldStress*thickness1/radius
	# 	else:
	# 		radialBurstPressureCyl = self.mat["t_yield_stress"]*self.t1/self.r

	# 	return radialBurstPressureCyl

	# def InnerPressureFCap(self, params, matProp):
	# 	if(params.all() != None):
	# 		radius, thickness1, thickness2 = params
	# 		tYieldStress, EMod, poissonR, volume, pressure = matProp

	# 		radialBurstPressureEnd = tYieldStress*thickness2/radius
	# 	else:
	# 		radialBurstPressureEnd = self.mat["t_yield_stress"]*self.t2/self.r

	# 	return radialBurstPressureEnd

	def StressCap(self, params, matProp):
		if(params.all() != None):
			radius, thickness1, thickness2 = params
			tYieldStress, EMod, poissonR, volume, pressure = matProp
			hoopStress = pressure*radius/thickness2
			sigmaX = hoopStress

		else:
			hoopStress = self.p*self.r/self.t2
			sigmaX = hoopStress

		return sigmaX

	def StressCyl(self, params, matProp):
		if(params.all() != None):
			radius, thickness1, thickness2 = params
			tYieldStress, EMod, poissonR, volume, pressure = matProp

			hoopStress = pressure*radius/thickness1
			longitudinalStress = pressure*radius/(2*thickness1)
			compressiveStress = self.ay*self.m/(2*np.pi*radius*thickness1)
			bendingStress = 10e6 #for now has to be changed for biaxial bending at the end

			sigmaX = hoopStress
			sigmaY = np.amax(np.abs([(longitudinalStress - compressiveStress - bendingStress), (longitudinalStress - compressiveStress + bendingStress)]))

			tauXY = 15e6 #for now but has to be changed for biaxial bending at the end

		else:
			hoopStress = self.p*self.r/self.t1
			longitudinalStress = self.p*self.r/(2*self.t1)
			compressiveStress = self.ay*self.m/(2*np.pi*self.r*self.t1)
			bendingStress = 10e6 #for now has to be changed for biaxial bending at the end

			sigmaX = hoopStress
			sigmaY = np.amax(np.abs(np.array[(longitudinalStress - compressiveStress - bendingStress), (longitudinalStress - compressiveStress + bendingStress)]))

			tauXY = 15e6 #for now but has to be changed for biaxial bending at the end

		return sigmaX, sigmaY, tauXY, longitudinalStress

	def TrescaF(self, params, matProp): 	#Tresca function. Returns true if the elastic limit is NOT reached
	    sigmaX, sigmaY, tauXY, longitudinalStress = self.StressCyl(params, matProp)
	    sigma_av = (sigmaX + sigmaY) / 2      # [Pa] average normal stress
	    R = np.sqrt(sigma_av ** 2 + tauXY ** 2)       # [Pa] Mohr circle radius

	    sigma1 = sigma_av + R
	    sigma2 = sigma_av - R
	    sigma3 = 0

	    tau_max_x2 = np.abs(np.array([sigma1 - sigma2, sigma2 - sigma3, sigma1 - sigma3]))
	    actualStress = np.amax(tau_max_x2)
	    return actualStress

	def EulerColumnBuckling(self, params, matProp):
		if(params.all() != None):
			radius, thickness1, thickness2 = params
			tYieldStress, EMod, poissonR, volume, pressure = matProp

			length = (volume-4/3*np.pi*radius**3)/(np.pi*radius**2)

			ICylinder = np.pi/4*(radius**4-(radius-thickness1)**4)
			areaCylinder = np.pi*radius**2
			criticalStressE = ((np.pi**2)*EMod*ICylinder)/(areaCylinder*length**2)
		else:
			l = (self.v-4/3*np.pi*self.r**3)/(np.pi*self.r**2)

			ICylinder = np.pi/4*(self.r**4-(self.r-self.t1)**4)
			areaCylinder = np.pi*self.r**2
			criticalStressE = ((np.pi**2)*self.mat["E_modulus"]*ICylinder)/(areaCylinder*l**2)
		return criticalStressE

	def ShellBuckling(self, params, matProp):
		if(params.all() != None):
			radius, thickness1, thickness2 = params
			tYieldStress, EMod, poissonR, volume, pressure = matProp

			length = (volume-4/3*np.pi*radius**3)/(np.pi*radius**2)

			k = lambda fLambda : fLambda + (12*length**4)/(np.pi**4*radius**2*thickness1**2)*(1-poissonR**2)/fLambda
			bestLambda = sco.minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": False}).x[0]
			Q = pressure/EMod*(radius/thickness1)**2
			criticalStressS = (1.983-0.983*np.exp(-23.14*Q))*bestLambda*(np.pi**2*EMod/(12*(1-poissonR**2)))*(thickness1/length)**2
		else:
			l = (self.v-4/3*np.pi*self.r**3)/(np.pi*self.r**2)
			k = lambda fLambda : fLambda + (12*l**4)/(np.pi**4*self.r**2*self.t1**2)*(1-self.mat["poisson_ratio"]**2)/fLambda
			bestLambda = sco.minimize(k, 1, method="BFGS", options={"gtol":1e-4, "disp": False}).x[0]
			Q = pressure/self.mat["E_modulus"]*(self.r/self.t1)**2
			criticalStressS = (1.983-0.983*np.exp(-23.14*Q))*bestLambda*(np.pi**2*self.mat["E_modulus"]/(12*(1-self.mat["poisson_ratio"]**2)))*(self.t1/l)**2

		return criticalStressS

	def EulerColumnBucklingF(self, params, matProp):
		difference = self.EulerColumnBuckling(params, matProp) - self.StressCyl(params, matProp)[3]
		return difference

	def ShellBucklingF(self, params, matProp):
		difference = self.ShellBuckling(params, matProp) - self.StressCyl(params, matProp)[3]
		return difference

	def MassOptimization(self, initialTank):
		for material in materials.material_dict.values():

			matProp = np.array([material["t_yield_stress"], material["E_modulus"], material["poisson_ratio"], initialTank.v, initialTank.p])

			# InnerPressureFCase_params = lambda params: self.InnerPressureFCase(params, matProp)
			# InnerPressureFCap_params = lambda params: self.InnerPressureFCap(params, matProp)
			StressCap_params = lambda params: self.StressCap(params, matProp)-material["t_yield_stress"]
			TrescaF_params = lambda params: self.TrescaF(params, matProp)-material["t_yield_stress"]
			EulerColumnBucklingF_params = lambda params: self.EulerColumnBucklingF(params, matProp)
			ShellBuckling_params = lambda params: self.ShellBucklingF(params, matProp)

			def Mass(variables): 
				radius, thickness1, thickness2 = variables
				length = (initialTank.v-4/3*np.pi*radius**3)/(np.pi*radius**2)
				massConfiguration = (4*np.pi*radius**2*thickness2+2*np.pi*radius*length*thickness1)*material["density"]

				return massConfiguration

			bounds = sco.Bounds([0.4, 5e-5, 5e-5], [4, 1e-1, 1e-1])

			def ConstrainF(variables):
				return np.array([StressCap_params(variables), TrescaF_params(variables), EulerColumnBucklingF_params(variables), ShellBuckling_params(variables)])

			cons = sco.NonlinearConstraint(ConstrainF, [0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf])
			radiusRange = np.linspace(0.5, 1.8, 20)

			bestConf = np.array([10, 1e-1, 1e-1])

			for radiusTest in radiusRange:
				res = sco.minimize(Mass, [radiusTest, 1e-2, 1e-2], method="trust-constr", jac="2-point", hess = sco.SR1(), options={'verbose':1}, constraints=cons, bounds=bounds)
				
				if(np.all(ConstrainF(res.x)>0) and (Mass(res.x) < Mass(bestConf))):
					bestConf = res.x
					print('Update of best conf\n')

				print(f'\nParameters: {res.x}\n')
				print(f'Tresca yield: {TrescaF_params(res.x)}\nColumn buckling stress margin:{EulerColumnBucklingF_params(res.x)}\nShell buckling stress margin: {ShellBuckling_params(res.x)}\n')
				print(f'Mass : {Mass(res.x)}\n')
			
			print(f'\nMaterial: {material["name"]} \nRadius: {bestConf[0]} m\nThickness Body: {bestConf[1]} m\nThickness Cap: {bestConf[2]} m\n')
			print(f'Case pressure failure: {TrescaF_params(bestConf)/1e6} MPa\nColumn buckling stress margin:{EulerColumnBucklingF_params(bestConf)/1e6} MPa\nShell buckling stress margin: {ShellBuckling_params(bestConf)/1e6} MPa\n')		