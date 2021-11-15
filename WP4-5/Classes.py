import math
import numpy as np


class Flange:
    def __init__(self, width, lug_thickness, hinge_diameter, material, length=0):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter
        self.m = material
        self.l = length

    def get_dimensions(self):
        return [self.w, self.t, self.d, self.l]

    def get_material(self):
        return self.m

    def K_br(self):
        k = self.t / self.d

        if k <= 0.06:
            k = 0.06
        elif k >= 0.5:
            k = 0.6
        elif k < 0.135:
            k = round(k/2*100)*2/100
        elif k < 0.25:
            k = round(k/5*100)*5/100
        else:
            k = round(k*10)/10

        x = self.w / (2 * self.d)
        if k == 0.06:
            return -0.00235*x**6 + 0.3448*x**5 - 2.0373*x**4 + 6.2116*x**3 - 10.396*x**2 + 9.3121*x - 2.7106
        elif k == 0.08:
            return -0.0196*x**6 + 0.2937*x**5 - 1.7831*x**4 + 5.6263*x**3 - 9.845*x**2 + 9.3348*x - 2.8232
        elif k == 0.1:
            return -0.0081*x**6 + 0.1355*x**5 - 0.9318*x**4 + 3.3725*x**3 - 6.8401*x**2 + 7.5535*x - 2.4513
        elif k == 0.12:
            return -0.005*x**6 + 0.0901*x**5 - 0.6644*x**4 + 2.5808*x**3 - 5.6329*x**2 + 6.7237*x - 2.2501
        elif k == 0.15:
            return 0.0032*x**6 - 0.0281*x**5 + 0.0106*x**4 + 0.6622*x**3 - 2.8503*x**2 + 4.8915*x - 1.8208
        elif k == 0.2:
            return 0.0068*x**6 - 0.087*x**5 + 0.3885*x**4 - 0.5524*x**3 - 0.8532*x**2 + 3.4179*x - 1.441
        elif k == 0.3:
            return 0.004*x**6 - 0.0555*x**5 + 0.2734*x**4 - 0.4473*x**3 - 0.6323*x**2 + 3.0505*x - 1.3112
        elif k == 0.4:
            return -0.0015*x**6 + 0.0165*x**5 - 0.088*x**4 + 0.4184*x**3 - 1.6331*x**2 + 3.579*x - 1.4127
        elif k == 0.6:
            return -0.0048*x**6 + 0.0626*x**5 - 0.343*x**4 + 1.1103*x**3 - 2.5736*x**2 + 4.1826*x - 1.5554


    def minimum_t(self, load):
        fx, fy, fz = load

        # Failure due to tensile forces - Extracted from Bruhn
        def t_yield_z():
            area = (self.w-self.d)  # per unit thickness
            return fz / (self.m.get_stress() * area)

        def t_bearing():
            safety_margin = 1.5
            return safety_margin * fz / (self.m.get_bear() * self.d)

        def t_shear():
            area = 2*math.sqrt((self.w/2)**2 + (self.d/2)**2)  # conservative estimate - per unit thickness
            return fz / (self.m.get_shear() * area)

        t1 = t_yield_z()
        t2 = t_bearing()
        t3 = t_shear()

        # Failure due to vertical forces - assuming bending is negligible
        t4 = (6 * self.l * fy / self.m.get_stress())**(1/3)

        thickness = sorted([t1, t2, t3, t4])
        return thickness[-1]

    def minimum_d(self, load):
        fx, fy, fz = load  # works both with lists and arrays

        # Failure due to tensile forces - Extracted from Bruhn
        def t_yield_z():
            return fz / (self.m.get_stress() * self.t) + self.w

        def t_bearing():
            safety_margin = 1.5
            return safety_margin * fz / (self.m.get_bear() * self.t)

        def t_shear():
            return math.sqrt(self.w**2 - 4*(fz/self.m.get_shear)**2)

        d1 = t_yield_z()
        d2 = t_bearing()
        d3 = t_shear()

        diameters = sorted([d1, d2, d3])
        return diameters[2]

    def minimum_w(self, load):
        fx, fy, fz = load

        # Failure due to bending right before the bolt
        length = self.l-self.d/2
        return math.sqrt(6*fy*length/self.t)

    def mass(self):
        area = math.pi * ((self.w/2)**2 - (self.d/2)**2) + self.w * self.l
        volume = area * self.t
        return volume * self.m.get_density()


class Lug:  # Assumes flange separation will be the same and flanges will be identical
    def __init__(self, flange, separation, number):
        self.f = flange
        self.n = number
        self.h = separation

    def get_flange(self):
        return self.f

    def minimum_t(self, loads):
        fx, fy, fz = loads
        fx = fx/self.n
        fy = fy/self.n
        fz = fz/self.n
        return self.f.minimum_t((fx, fy, fz))

    def minimum_d(self, loads):
        fx, fy, fz = loads
        fx = fx / self.n
        fy = fy / self.n
        fz = fz / self.n
        return self.f.minimum_d((fx, fy, fz))

    def mass(self):
        return self.f.mass() * self.n


class Double_lug:   # A double lug
    def __init__(self, top_lug, bottom_lug, separation, dist_to_cg):
        self.tl = top_lug
        self.bl = bottom_lug
        self.h = separation
        self.r = dist_to_cg

    def loads(self, loads):
        fx, fy, fz = loads
        fx = fx / 2
        fy = fy / 2

        fz_top = fz / 2 - 2 * fy * self.r / self.h
        fz_bot = fz / 2 + 2 * fy * self.r / self.h

        return [(fx, fy, fz_top), (fx, fy, fz_bot)]

    def min_t(self, force):
        forces = self.loads(force)
        top = self.tl.minimum_t(forces[0])
        bottom = self.bl.minimum_t(forces[1])
        return [top, bottom]

    def min_d(self, force):
        forces = self.loads(force)
        top = self.tl.minimum_d(forces[0])
        bottom = self.bl.minimum_d(forces[1])
        return [top, bottom]

    def mass(self):
        top = self.tl.mass()
        bottom = self.bl.mass()
        return [top, bottom]


class Material:
    def __init__(self, Youngs_Modulus, yield_stress, shear_modulus, maximum_shear, max_bearing_stress, density):
        self.e = Youngs_Modulus
        self.y = yield_stress
        self.g = shear_modulus
        self.sh = maximum_shear
        self.bear = max_bearing_stress
        self.d = density

    def get_stress(self):
        return self.y

    def get_E(self):
        return self.e

    def get_G(self):
        return self.g

    def get_shear(self):
        return self.sh

    def get_bear(self):
        return self.bear

    def get_density(self):
        return self.d

#test
class Plate:
    def __init__(self, number_fasteners, fastener_diameter, plate_thickness):
        self.n = number_fasteners
        self.d = fastener_diameter
        self.t = plate_thickness

    # Assuming the fastener diameters (D1) are the same

    def get_cg(self, coords):  # coords format: [[x1,y1],[x2,y2]]
        copy = []
        for i in coords:
            copy.append(np.asarray(i))
        coords = copy
        return list(sum(coords) / len(coords)) # the output format: [x,y]

    def force_cg(self, fx, fy, n):
        f_ip_x = fx / n
        f_ip_y = fy / n
        return [f_ip_x, f_ip_y]  # outputs forces acting on single (every) fastener

    def moment_cg(self, coords_cg, coords_lug, f_ip_x, f_ip_y):
        moment = 0
        for i in coords_cg:
            g = ((coords_lug[1] - i[1]) * f_ip_x) - ((coords_lug[0] - i[0]) * f_ip_y)  # positive ?
            components_moments.append(g)

        m = sum(components_moments)     # moment around cg of the plate
        return m

    def force_due_to_moment(self, coords, cg_coords, m):
        distances = []
        angles = []

        for i in coords:
            d = math.sqrt((i[0] - cg_coords[0]) ** 2 + (i[1] - cg_coords[1]) ** 2)
            a = math.atan2((i[1] - cg_coords[1]), (i[0] - cg_coords[0]))
            distances.append(d)
            angles.append(a) # * 180 / math.pi)

        force_due_moments = []

        n = 0
        while n < len(distances):
            i = distances[n]
            mx = m / i * math.cos(angles[n]) #* math.pi / 180)
            my = m / i * math.sin(angles[n]) #* math.pi / 180)
            force_due_moments.append([round(mx), round(my)])
            n += 1

        return force_due_moments  # outputs force acting on fasteners to counteract moment caused by antisymmetry

    def force_moment(self, force_due_moments, f_ip_x, f_ip_y):  # force on connector caused by moment around cg
        forces = []

        for i in force_due_moments:
            forcex = i[0] + f_ip_x
            forcey = i[1] + f_ip_y
            force = np.sqrt(forcex**2 + forcey**2)
            forces.append(force)
        return forces           # force P

    def fastener_shear_stress(self, fastener_diameter, thickness_plate, forces):
        shear_stress = []
        for i in forces:
            shear = i / (fastener_diameter * thickness_plate)
            shear_stress.append(shear)
        return max(shear_stress)

    #PULL-THROUGH CHECK (ONLY FOR ONE SYSTEM)

    def z_forces(self, fy, n):
        f_pi = fy / n
        return f_pi

    #def forces_due_moment(self, , ):
    #    ...

    def pull_through_fail(self, D_fin, D_fout, r_f, t_wall, t_lug, M_ASRG, cg_y):
        # D_fin is inner diameter of fastener (numppy array)
        # D_fout is outer

        # r_f is fastener coordinates (2D numpy array...
        # ... of the form [[x1, x2, xn], [z1, z2, zn]])
        # ^^^ (0,0) x-z axis asrg centre of mass

        g = 9.81

        # t is the thickness of s/c wall or lug plate
        n_f = len(D_fin)  # number of fasteners
        F_y = 2 * g * M_ASRG  # normal force
        Mx = 6 * g * M_ASRG * cg_y  # moment about x axis
        Mz = 2 * g * M_ASRG * cg_y  # moment about z axis
        # cg_y is distance from lug to center of mass of ASRG
        # now we calculate the normal forces caused by the moments:
        A_n = np.pi * (D_fout ** 2 - D_fin ** 2) / 4  # normal area
        F_Mx = Mx * A_n * r_f[1] / np.sum(A_n * (r_f[1] ** 2))
        F_Mz = Mz * A_n * r_f[0] / np.sum(A_n * (np.abs(r_f[0]) ** 2))
        # r_f[0] is considered always positive so we design for the highest tensile load
        # on both sides of the lug
        # total normal force:
        F_tot = F_y + F_Mx + F_Mz
        # stresses:
        sigma = F_tot / A_n  # normal stress
        A_s = np.pi * D_fin * (t_wall + t_lug)  # shear area
        tau = F_tot / A_s  # shear stress
        Y = np.sqrt((sigma ** 2) + 3 * (tau ** 2))
        # Y is the total normal stress
        # which has to be below the yield stresses of the wall and lug materials.
        return Y

class Loads:
    def __init__(self, Force_x, Force_y, Force_z, Moment_x, Moment_y, Moment_z):
        self.F_x = Force_x
        self.F_y = Force_y
        self.F_z = Force_z
        self.M_x = Moment_x
        self.M_y = Moment_y
        self.M_z = Moment_z

def Min_Fastener_Diameter_Tension (Loads, Material, n, width, height, gap):
    Sigma_yield = Material.y
    M_x_plate = Loads.F_y * gap
    F_z_max = Loads.F_z + Loads.M_y*2/width + M_x_plate*2/height
    A_total = F_z_max / Sigma_yield
    A = A_total/n
    D = math.sqrt(4*A/math.pi)
    return D
