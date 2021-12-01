import numpy as np
from Constants import *


def frequency_SC(E, M, A, I, L):
    k_y = E * A / L  # Longitudinal direction
    k_xz = 3 * E * I / np.power(L, 3)  # Lateral direction

    f_n1 = np.sqrt(k_y / M) / (2 * np.pi)
    f_n2 = np.sqrt(k_xz / M) / (2 * np.pi)

    f_nat = np.minimum(f_n1, f_n2)

    return f_nat, f_n1, f_n2


print(frequency_SC(73.1e9, 18119.35, 2 * np.pi * 1.8 * 0.0005, np.pi * np.power(1.8, 3) * 0.0005, 8.235))
