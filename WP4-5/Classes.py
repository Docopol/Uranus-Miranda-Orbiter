import math
import numpy as np

class Flange:
    def __init__(self, width, lug_thickness, hinge_diameter, material, length):
        self.w = width
        self.t = lug_thickness
        self.d = hinge_diameter
        self.m = material
        self.l = length

    def get_dimensions(self):
        return [self.w, self.t, self.d, self.l]

    def get_material(self):
        return self.m

    def K_bry(self):
        r = self.t / self.d

        if r < 0.06:
            r = 0.06
        elif 0.06 < r < 0.135:
            r = round(r/2*100)*2/100
        elif 0.135 <= r < 0.25:
            r = round(r/5*100)*5/100
        elif 0.25 <= r < 0.5:
            r = round(r*10)/10
        else:
            r = 0.6

        x = self.w / (2 * self.d)
        if x > 4:
            x = 4

        if r == 0.06:
            k = -0.00235*x**6 + 0.3448*x**5 - 2.0373*x**4 + 6.2116*x**3 - 10.396*x**2 + 9.3121*x - 2.7106
        elif r == 0.08:
            k = -0.0196*x**6 + 0.2937*x**5 - 1.7831*x**4 + 5.6263*x**3 - 9.845*x**2 + 9.3348*x - 2.8232
        elif r == 0.1:
            k = -0.0081*x**6 + 0.1355*x**5 - 0.9318*x**4 + 3.3725*x**3 - 6.8401*x**2 + 7.5535*x - 2.4513
        elif r == 0.12:
            k = -0.005*x**6 + 0.0901*x**5 - 0.6644*x**4 + 2.5808*x**3 - 5.6329*x**2 + 6.7237*x - 2.2501
        elif r == 0.15:
            k = 0.0032*x**6 - 0.0281*x**5 + 0.0106*x**4 + 0.6622*x**3 - 2.8503*x**2 + 4.8915*x - 1.8208
        elif r == 0.2:
            k = 0.0068*x**6 - 0.087*x**5 + 0.3885*x**4 - 0.5524*x**3 - 0.8532*x**2 + 3.4179*x - 1.441
        elif r == 0.3:
            k = 0.004*x**6 - 0.0555*x**5 + 0.2734*x**4 - 0.4473*x**3 - 0.6323*x**2 + 3.0505*x - 1.3112
        elif r == 0.4:
            k = -0.0015*x**6 + 0.0165*x**5 - 0.088*x**4 + 0.4184*x**3 - 1.6331*x**2 + 3.579*x - 1.4127
        else:
            k = -0.0048*x**6 + 0.0626*x**5 - 0.343*x**4 + 1.1103*x**3 - 2.5736*x**2 + 4.1826*x - 1.5554

        if k < 0:
            k = 0.01

        return k

    def K_t(self):
        mat = self.m.get_name()
        x = self.w / self.d
        if x > 5:
            x = 5
        c1 = 0.0006*x**6 - 0.0099*x**5 + 0.0636*x**4 - 0.1779*x**3 + 0.1932*x**2 - 0.0412*x + 0.9727
        c2 = -0.0045*x**5 + 0.0414*x**4 - 0.129*x**3 + 0.1296*x**2 + 0.0066*x + 0.9568
        c3 = -0.002*x**4 + 0.0217*x**3 - 0.0805*x**2 + 0.0519*x + 1.02
        c4 = -0.0036*x**4 + 0.044*x**3 - 0.1763*x**2 + 0.1694*x + 0.981
        c5 = 0.001*x**5 - 0.0134*x**4 + 0.0653*x**3 - 0.1165*x**2 - 0.1143*x + 1.197
        c6 = -0.083*x + 0.7549
        c7 = 0.0059*x**5 - 0.0862*x**4 + 0.4716*x**3 - 1.172*x**2 + 1.0229*x + 0.7781
        if mat == 'Al2014-T6':
            k = (c1+c2+c4+c5)/4
        elif mat == 'Al7075-T6':
            k = (c1+c2+c4)/3
        elif mat == 'Al2024-T4':
            k = (c3+c4)/2
        elif mat == 'Al2024-T3':
            k = c4
        elif mat == 'St4130' or mat == 'St8630':
            k = c1
        elif mat == 'MgAZ91C-T6':
            k = c7
        else:
            k = (c1+c2+c3+c4+c5+c6+c7)/7

        ms = 0.15
        k += ms
        return k

    def K_ty(self):
        A1 = self.t * (self.w - self.d*math.sqrt(1/2))/2
        A2 = self.t * (self.w - self.d)/2
        A_av = 6/(4/A1+2/A2)
        A_br = self.t * self.d
        x = A_av/A_br

        k = 0.0718*x**3 - 0.5166*x**2 + 1.5215*x - 0.0359

        ms = 0.15
        k += ms
        return k

    def check_failure(self, load, m_y):
        fx, fy, fz = load
        safety_factor = 1.5

        if fz/(self.t * (self.w - self.d)*self.K_t()) > self.m.get_stress(safety_factor):
            failure = True
        elif fy/((self.d * self.t)*self.K_ty()) > self.m.get_stress(safety_factor):
            failure = True
        elif fz/((self.d * self.t)*self.K_bry()) > self.m.get_stress(safety_factor):
            failure = True
        elif 6 * fy * self.l / (self.t * self.w**2) > self.m.get_stress(safety_factor):
            failure = True
        elif 6 * (fx * self.l + m_y) / (self.w * self.t**2) > self.m.get_stress(safety_factor):
            failure = True
        else:
            failure = False

        return failure

    def minimum_t(self, load, m_y):
        fx, fy, fz = load
        safety_factor = 1.5

        def t_yield():
            area = (self.w-self.d)
            k = self.K_t()
            return fz / (k * self.m.get_stress(safety_factor) * area)

        def t_bearing():
            k_bry = self.K_bry()
            return fz / (k_bry * self.m.get_stress(safety_factor) * self.d)

        def t_shear():
            k_ty = self.K_ty()
            return fy / (k_ty * self.m.get_stress(safety_factor) * self.d)

        def bending_x():
            return 6 * fy * self.l / (self.m.get_stress(safety_factor) * self.w**2)

        def bending_y():
            return math.sqrt(6 * (fx * self.l + m_y) / (self.m.get_stress(safety_factor) * self.w))

        t1 = t_yield()
        t2 = t_bearing()
        t3 = t_shear()
        t4 = bending_x()
        t5 = bending_y()

        min_t = max([t1, t2, t3, t4, t5])
        return min_t

    def minimum_d(self, load):
        fx, fy, fz = load  # works both with lists and arrays
        safety_factor = 1.5

        def d_bearing():  # Eq 3.3 from Overleaf
            k_bry = self.K_bry()
            return fz / (k_bry * self.m.get_stress(safety_factor) * self.t)

        k_ty = self.K_ty()
        d1 = fy / (k_ty * self.m.get_stress(safety_factor) * self.t)
        d2 = d_bearing()

        d_list = [d1, d2]
        return max(d_list)

    def maximum_d(self, load):
        fx, fy, fz = load  # works both with lists and arrays
        safety_factor = 1.5

        k = self.K_ty()
        d1 = self.w - abs(fz) / (k * self.m.get_stress(safety_factor) * self.t)  # Eq 3.1 from Overleaf
        return d1

    def mass(self):
        area = self.w * self.l - math.pi * self.d**2 / 8 + math.pi / 2 * (self.w**2 - self.d**2)/4
        volume = area * self.t
        return volume * self.m.get_density()

    def margin_of_safety(self, load, m_y):
        fx, fy, fz = load

        o1 = fz/(self.t * (self.w - self.d)*self.K_t())
        o2 = fy/((self.d * self.t)*self.K_ty())
        o3 = fz/((self.d * self.t)*self.K_bry())
        o4 = 6 * fy * self.l / (self.t * self.w**2)
        o5 = 6 * (fx * self.l + m_y) / (self.w * self.t**2)

        o = max([o1, o2, o3, o4, o5])
        ms = self.m.get_stress() / o - 1

        if o == o1:
            f_type = 'tension'
        elif o == o2:
            f_type = 'yield'
        elif o == o3:
            f_type = 'bearing'
        elif o == o4:
            f_type = 'bending around x'
        else:
            f_type = 'bending around y'

        return ms, f_type


class Lug:  # Assumes flange separation will be the same and flanges will be identical
    def __init__(self, flange, separation, number):
        self.f = flange
        self.n = number
        self.h = separation

    def get_flange(self):
        return self.f

    def get_material(self):
        return self.f.get_material()

    def get_dimensions(self):
        return self.f.get_dimensions()

    def minimum_t(self, loads):
        fx, fy, fz = loads
        fx = fx/self.n
        fy = fy/self.n
        fz = fz/self.n
        return self.f.minimum_t((fx, fy, fz))

    def minimum_d(self, loads):
        fx, fy, fz = loads
        fx = fx
        fy = fy / self.n
        fz = fz / self.n
        return self.f.minimum_d((fx, fy, fz))

    def maximum_d(self, loads):
        fx, fy, fz = loads
        fx = fx / self.n
        fy = fy / self.n
        fz = fz / self.n
        return self.f.maximum_d((fx, fy, fz))

    def minimum_w(self, loads):
        fx, fy, fz = loads
        fx = fx / self.n
        fy = fy / self.n
        fz = fz / self.n
        return self.f.minimum_w((fx, fy, fz))

    def mass(self):
        return self.f.mass() * self.n

    def lower_bound_t(self, loads):
        fx, fy, fz = loads
        fx = fx / self.n
        fy = fy / self.n

        material = self.f.get_material()
        w = self.f.get_dimensions()[0]
        l = self.f.get_dimensions()[-1]

        t_list = list()
        t1 = 6*fy*l / (material.get_stress() * w**2)  # From failure due to bending around x
        t_list.append(t1)
        if self.n == 2:
            t2 = 2 * fx * l / (material.get_stress() * self.h**2)
            t_list.append(t2)

        return sorted(t_list)[-1]


class Double_lug:   # A double lug
    def __init__(self, top_lug, bottom_lug, separation, dist_to_cg):
        self.tl = top_lug
        self.bl = bottom_lug
        self.h = separation
        self.r = dist_to_cg

    def get_lugs(self):
        return [self.tl, self.bl]

    def loads(self, loads):
        fx, fy, fz = loads
        fx = fx / 2
        fy = fy  # Design allows for each lug to withstand the entire vertical load
        fz = fz / 2 + 2 * fy * self.r / self.h

        return [fx, fy, fz]

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

    def min_w(self, force):
        forces = self.loads(force)
        top = self.tl.minimum_w(forces[0])
        bottom = self.bl.minimum_w(forces[1])
        return [top, bottom]

    def mass(self):
        top = self.tl.mass()
        bottom = self.bl.mass()
        return [top, bottom]

#test
class Plate:
    def __init__(self, number_fasteners, fastener_diameter, plate_thickness, plate_width, plate_height):
        self.n = number_fasteners
        self.d = fastener_diameter
        self.t = plate_thickness
        self.w = plate_width
        self.h = plate_height

    def get_mass(self, material):
        return self.w*self.h*self.t*material.d

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
        return [f_ip_x, f_ip_y]     # outputs forces acting on single (every) fastener

    def moment_cg(self, coords_cg, coords_lug, f_ip_x, f_ip_y):
        moment = 0
        for i in coords_cg:
            g = ((coords_lug[1] - i) * f_ip_x) - ((coords_lug[0] - i) * f_ip_y)  # positive ?
            moment += g
        return moment   # moment around cg of the plate

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
        return forces           # list of P forces

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

    def pull_through_fail(self,n_f, D_fin, D_fout, r_f, t_wall, t_lug, M_ASRG, cg_y):
        # D_fin is inner diameter of fastener (numppy array)
        # D_fout is outer
        # r_f is fastener coordinates (2D numpy array...
        # ... of the form [[x1, x2, xn], [z1, z2, zn]])
        # ^^^ (0,0) x-z axis asrg centre of mass
        g = 9.81
        # t is the thickness of s/c wall or lug plate
        #n_f = len(D_fin)  # number of fasteners
        F_y = 2 * g * M_ASRG /n_f  # normal force
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


class Loads:  # Javi - is this really necessary?? Well, it makes it easier for me
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
    F_z_max = Loads.F_z/n + Loads.M_y*2/width/(n/2) + M_x_plate*2/height/(n/2)
    A_total = F_z_max / Sigma_yield
    A = A_total/n
    D = math.sqrt(4*A/math.pi)
    return D
