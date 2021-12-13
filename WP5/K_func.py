import numpy as np
import math as m


def K_t(matn, w, d):
    x = w/d
    c1 = 0.0006 * x ** 6 - 0.0099 * x ** 5 + 0.0636 * x ** 4 - 0.1779 * x ** 3 + 0.1932 * x ** 2 - 0.0412 * x + 0.9727
    c2 = -0.0045 * x ** 5 + 0.0414 * x ** 4 - 0.129 * x ** 3 + 0.1296 * x ** 2 + 0.0066 * x + 0.9568
    c3 = -0.002 * x ** 4 + 0.0217 * x ** 3 - 0.0805 * x ** 2 + 0.0519 * x + 1.02
    c4 = -0.0036 * x ** 4 + 0.044 * x ** 3 - 0.1763 * x ** 2 + 0.1694 * x + 0.981
    c5 = 0.001 * x ** 5 - 0.0134 * x ** 4 + 0.0653 * x ** 3 - 0.1165 * x ** 2 - 0.1143 * x + 1.197
    c6 = -0.083 * x + 0.7549
    c7 = 0.0059 * x ** 5 - 0.0862 * x ** 4 + 0.4716 * x ** 3 - 1.172 * x ** 2 + 1.0229 * x + 0.7781
    if matn == 'Al2014-T6':
        k = (c1 + c2 + c4 + c5) / 4
    elif matn == 'Al7075-T6' or matn == 'Al6061-T6':
        k = (c1 + c2 + c4) / 3
    elif matn == 'Al2024-T4':
        k = (c3 + c4) / 2
    elif matn == 'Al2024-T3':
        k = c4
    elif matn == 'St4130' or matn == 'St8630' or matn == 'St-A992':
        k = c1
    elif matn == 'MgAZ91C-T6' or matn == 'Mg-Am60':
        k = c7
    else:
        k = (c1 + c2 + c3 + c4 + c5 + c6 + c7) / 7

    ms = 0.15  # Margin of safety
    k += ms
    return k


def K_ty(t, w, d):
    A1 = t * (w - d * np.sqrt(1 / 2)) / 2
    A2 = t * (w - d) / 2
    A_av = 6 / (4 / A1 + 2 / A2)
    A_br = t * d
    x = A_av / A_br
    c3 = 0.0718 * x ** 3 - 0.5166 * x ** 2 + 1.5215 * x - 0.0359

    k = c3
    ms = 0.15
    k += ms
    return k


def K_bry(t, w, d):
    r = t / d

    if r <= 0.06:
        r = 0.06
    elif 0.06 < r < 0.135:
        r = round(r / 2 * 100) * 2 / 100
    elif 0.135 <= r < 0.25:
        r = round(r / 5 * 100) * 5 / 100
    elif 0.25 <= r < 0.5:
        r = round(r * 10) / 10
    else:
        r = 0.6

    x = w / (2 * d)

    if r == 0.06:
        k = -0.00235 * x ** 6 + 0.3448 * x ** 5 - 2.0373 * x ** 4 + 6.2116 * x ** 3 - 10.396 * x ** 2 + 9.3121 * x - 2.7106
    elif r == 0.08:
        k = -0.0196 * x ** 6 + 0.2937 * x ** 5 - 1.7831 * x ** 4 + 5.6263 * x ** 3 - 9.845 * x ** 2 + 9.3348 * x - 2.8232
    elif r == 0.1:
        k = -0.0081 * x ** 6 + 0.1355 * x ** 5 - 0.9318 * x ** 4 + 3.3725 * x ** 3 - 6.8401 * x ** 2 + 7.5535 * x - 2.4513
    elif r == 0.12:
        k = -0.005 * x ** 6 + 0.0901 * x ** 5 - 0.6644 * x ** 4 + 2.5808 * x ** 3 - 5.6329 * x ** 2 + 6.7237 * x - 2.2501
    elif r == 0.15:
        k = 0.0032 * x ** 6 - 0.0281 * x ** 5 + 0.0106 * x ** 4 + 0.6622 * x ** 3 - 2.8503 * x ** 2 + 4.8915 * x - 1.8208
    elif r == 0.2:
        k = 0.0068 * x ** 6 - 0.087 * x ** 5 + 0.3885 * x ** 4 - 0.5524 * x ** 3 - 0.8532 * x ** 2 + 3.4179 * x - 1.441
    elif r == 0.3:
        k = 0.004 * x ** 6 - 0.0555 * x ** 5 + 0.2734 * x ** 4 - 0.4473 * x ** 3 - 0.6323 * x ** 2 + 3.0505 * x - 1.3112
    elif r == 0.4:
        k = -0.0015 * x ** 6 + 0.0165 * x ** 5 - 0.088 * x ** 4 + 0.4184 * x ** 3 - 1.6331 * x ** 2 + 3.579 * x - 1.4127
    else:
        k = -0.0048 * x ** 6 + 0.0626 * x ** 5 - 0.343 * x ** 4 + 1.1103 * x ** 3 - 2.5736 * x ** 2 + 4.1826 * x - 1.5554

    if k < 0:
        k = 0.01

    return k