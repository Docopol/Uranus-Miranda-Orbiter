from math import *

#ADCS jitter calculation

orbitingAltitude = 3520e3 #m
orbitalVelocity = 14338 #m/s
cameraResolutionPanSpecs = 1.4/500e3 #In m ground divided by orbital height

pixelGroundWidth = cameraResolutionPanSpecs*orbitingAltitude

stabilityDueToCamera = atan(pixelGroundWidth/orbitingAltitude)*orbitalVelocity/pixelGroundWidth #rad/s

#print(stabilityDueToCamera) 


##ADCS disturbances calculations

#Gravity

massSC = 2000
lengthSC = 8
radiusSC = 1.8

mu = 5.7940*10**15
orbitalRadius = orbitingAltitude + 25166e3
n2 = mu/orbitalRadius**3 
Iy = 1/2*massSC*radiusSC**2 								#Assuming S/C is a sausage of 8m x 3.6m diameter with uniform density
Iz = 1/4*massSC*radiusSC**2+1/12*massSC*lengthSC**2

perturbationGravity = (3/2*n2*(Iz-Iy)*pi/180)*sqrt(2) #s

#print(perturbationGravity)

#Aerodynamic torque

orbitalDensity = 5.432e-12
surfaceDrag = pi*radiusSC**2
cD = 1.17 #Flat frontal area
cPcG = pi/180*4 #corresponds to 1 degree misalignement of the frontal area

perturbationDrag = cPcG*1/2*orbitalDensity*orbitalVelocity**2*surfaceDrag*cD 

#print(perturbationDrag)

#Solar pressure

sailReflectivity = 0.84
solarPressure = 2.468e-8
surfaceSolar = 2*radiusSC*lengthSC
centreSolar = 1

perturbationSolar = centreSolar*(1+sailReflectivity)*solarPressure*surfaceSolar

print(perturbationSolar)

#Main camera datarate calculation

cameraImageLengthPixel = 20e3/1.4
cameraImageWidthPixel = 1 #
colourDepth = 16 #bits

imageSizeInBits = cameraImageWidthPixel*cameraImageLengthPixel*colourDepth
imageBackupSafetyFactor = 1
picturesPerSecond = orbitalVelocity/1.4*imageBackupSafetyFactor

dataRateCamera	= imageSizeInBits*picturesPerSecond #in bits/s

# print(dataRateCamera/10e6)

