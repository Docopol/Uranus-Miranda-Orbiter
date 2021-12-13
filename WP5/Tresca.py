import numpy as np


def tresca(sigma_x, sigma_y, tau_xy, sigma_lim):
    """Tresca function. Returns true if the elastic limit is NOT reached. (False means failure)"""
    sigma_av = (sigma_x + sigma_y) / 2      # [Pa] average normal stress
    R = np.sqrt(((sigma_x + sigma_y) / 2) ** 2 + tau_xy ** 2)       # [Pa] Mohr circle radius

    sigma1 = sigma_av + R
    sigma2 = sigma_av - R
    sigma3 = 0

    tau_max_x2 = np.abs(np.array([sigma1 - sigma2, sigma2 - sigma3, sigma1 - sigma3]))
    crit_stress = np.max(tau_max_x2)
    result = crit_stress < sigma_lim    # no fail = True | fail = False
    return result
