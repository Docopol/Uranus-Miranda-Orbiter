def mohcircle():
    import numpy as np
    import matplotlib.pyplot as plt
    import math

    σx = float(input('σx = '))
    σy = float(input('σy = '))
    τxy = float(input('τxy = '))
    u = input('stress unit = ')
    w = float(input("Angle( in degrees) of plane's axis from x axis(+ve counter clockwise), θ = "))
    θ = math.radians(w)
    R = np.sqrt(0.25 * (σx - σy) ** 2 + (τxy) ** 2)
    σavg = (σx + σy) / 2
    ψ = np.linspace(0, 2 * np.pi, 360)
    x = σavg + R * np.cos(ψ)
    y = R * (np.sin(ψ))
    φ1 = math.degrees(0.5 * math.atan(2 * τxy / (σx - σy)))
    φ2 = φ1 + 90
    σθ1 = σavg + R * np.cos(2 * np.radians(φ1) + 2 * θ)
    σθ2 = σavg + R * np.cos(2 * np.radians(φ1) + 2 * θ + np.pi)
    τθ = R * np.sin(2 * np.radians(φ1) + 2 * θ)
    print(f'''
       Radius, R = √(0.25*(σx-σy)^2 + τxy^2) 
               = √(0.25*({σx}-{σy})^2 + {τxy}^2)  ={R} {u}

       Average Stress,(acts at the Center of Mohr's Circle) 
               = σavg = (σx + σy)/2 = ({σx} + {σy})/2 = {σavg} {u}

       Principal Stresses
       σ1 = σavg + R = {σavg} + {R} = {σavg + R} {u}
       σ2 = σavg - R = {σavg} - {R} = {σavg - R} {u}
       Angle φ1 it makes with x-axis, 
       φ1 = 0.5(atan(2*τxy/(σx - σy)) = 0.5 * atan(2*{τxy}/({σx} - {σy})) = {φ1} degrees
       Angle σ2 makes with x-axis = φ2 = φ1 + 90 = {φ2} degrees

       Maximum Shear Stress = τmax = R = {R} {u}
       It occurs at, α = φ1 + 45 = {φ1 + 45} degrees

       Stresses at a plane with axis at θ anticlockwise from x axis, 
        σθ1 = σavg + R* Cos(2φ1 + 2θ) = {σavg} + {R}* Cos({2 * φ1 + 2 * θ})
           = {σθ1}, {u}
        σθ2 = σavg + R* Cos(2φ1 + 2θ + pi) = 
            {σθ2} {u}
        τθ = R*Sin(2*φ1 + 2*θ)  = {R * np.sin(2 * np.radians(φ1) + 2 * θ)} {u}

       ''')

    plt.plot(x, y)
    plt.plot([σavg - R - 10, σavg + R + 10], [0, 0], linestyle='--', color='black')
    plt.plot([σavg, σavg], [-R - 10, R + 10], linestyle='--', color='black')
    plt.plot([σx, σy], [τxy, -τxy], [σx, σx], [0, τxy], [σy, σy], [0, -τxy], linestyle='-', color='brown')
    plt.plot([σθ1, σθ2], [τθ, -τθ], [σθ1, σθ1], [0, τθ], [σθ2, σθ2], [0, -τθ], linestyle='--', color='red')
    plt.xlabel('σ (MPa)')
    plt.ylabel('τ (MPa)')
    plt.title("Mohr's Circle")
    plt.show()

mohcircle()
v = input('Exit? y/n ')
while v == "n":
    mohcircle()
    v = input('Exit? y/n ')
exit()