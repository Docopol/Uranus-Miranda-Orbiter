from math import *

#ADCS jitter calculation

orbitingAltitude = 4.343e3 #m
orbitalVelocity = 14011 #m/s
cameraResolutionPanSpecs = 0.7/500e3 #In m ground divided by orbital height

pixelGroundWidth = cameraResolutionPanSpecs*orbitingAltitude

stabilityDueToCamera = atan(pixelGroundWidth/orbitingAltitude)*orbitalVelocity/pixelGroundWidth #rad/s

#print(stabilityDueToCamera) 


##ADCS disturbances calculations

#Gravity

massSC = 6000
lengthSC = 8
radiusSC = 1.8

mu = 5.7940*10**15
orbitalRadius = orbitingAltitude + 25166e3
n2 = mu/orbitalRadius**3 
Iy = 1/2*massSC*radiusSC**2 								#Assuming S/C is a sausage of 8m x 3.6m diameter with uniform density
Iz = 1/4*massSC*radiusSC**2+1/12*massSC*lengthSC**2

perturbationGravity = (3/2*n2*(Iz-Iy)*pi/180)*sqrt(2) #s

# print(perturbationGravity)

#Aerodynamic torque

orbitalDensity = 8.417e-13
surfaceDrag = pi*radiusSC**2
cD = 2.7 #Flat frontal area
cPcG = pi/180*4 #corresponds to 1 degree misalignement of the frontal area

perturbationDrag = cPcG*1/2*orbitalDensity*orbitalVelocity**2*surfaceDrag*cD 

# print(perturbationDrag)

#Solar pressure

sailReflectivity = 0.84
solarPressure = 2.468e-8
surfaceSolar = 2*radiusSC*lengthSC
centreSolar = 1

perturbationSolar = centreSolar*(1+sailReflectivity)*solarPressure*surfaceSolar

# print(perturbationSolar)

#Magnetic disturbances

residualMagneticDipole = 0.1
maxMagneticField = 1e-4

perturbationMagnetic = maxMagneticField *residualMagneticDipole

# print(perturbationMagnetic)


##Sizing of thrusters

totalInstantenousDisturbances = (perturbationGravity+perturbationDrag+perturbationSolar+perturbationMagnetic)*1.2
orbitalPeriod = 2*pi*orbitalRadius/orbitalVelocity
disturbancesPerOrbit = totalInstantenousDisturbances*orbitalPeriod
totalOrbitsToCompleteMission = 4*366*24*3600/orbitalPeriod
totalAngularImpulse = totalOrbitsToCompleteMission*disturbancesPerOrbit

thrusterForce = 4
ISPthrusters = 220
armLengthPairThrusters = 8
coupleThrusters = armLengthPairThrusters*thrusterForce

propellantMassADCS = thrusterForce*totalAngularImpulse/(ISPthrusters*9.81*coupleThrusters)

print(propellantMassADCS)

# print(totalInstantenousDisturbances)
# print(disturbancesPerOrbit)
# print(totalAngularImpulse)

#Sing of reaction wheel

timeToRotate90 = 15*60
wheelTorque = 4*Iy*pi/2/timeToRotate90**2

# print(wheelTorque)

#Main camera datarate calculation

cameraImageLengthPixel = 20e3/1.4
cameraImageWidthPixel = 1 #
colourDepth = 16 #bits

imageSizeInBits = cameraImageWidthPixel*cameraImageLengthPixel*colourDepth
imageBackupSafetyFactor = 1
picturesPerSecond = orbitalVelocity/1.4*imageBackupSafetyFactor

dataRateCamera	= imageSizeInBits*picturesPerSecond #in bits/s

# print(dataRateCamera/10e6)

