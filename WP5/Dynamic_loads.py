import numpy as np
from Constants import *


def frequency_SC(E, M, A, I, L):
    k_y = E * A / L  # Longitudinal direction

    f_nat = np.sqrt(k_y / M) / (2 * np.pi)
    f_launcher = 30

    return f_nat, f_nat > f_launcher


print(frequency_SC(73.1e9, 18119.35, 2 * np.pi * 1.8 * 0.0005, np.pi * np.power(1.8, 3) * 0.0005, 8.235))
