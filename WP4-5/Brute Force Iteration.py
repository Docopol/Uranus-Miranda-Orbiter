import numpy as np


mat = Al2014T6
trange = np.linspace(10*10**(-3), 0.1*10**(-3), 101)
wrange = np.linspace(500*10**(-3), 5*10**(-3), 101)
drange = np.linspace(500*10**(-3), 5*10**(-3), 101)
lrange = np.linspace(500*10**(-3), 5*10**(-3), 101)

# all_combos = np.meshgrid(trange, wrange, drange, lrange)
# options = all_combos * check_failure(mat, all_combos)
# lightest = min(mass(options))
# print(lightest)

m_i = 10000000

for t in trange:
    # w = wrange[0]
    # d = drange[-50]
    # l = lrange[-1]
    # fail = check_failure(mat, t, w, d)
    # if fail:
    #     break
    for w in wrange:
        # d = drange[-50]
        # if d >= w:
        #     continue
        # l = lrange[-1]
        # fail = check_failure(mat, t, w, d)
        # if fail:
        #     break
        for d in drange:
            if d >= w:
                continue
            # l = lrange[-1]
            # fail = check_failure(mat, t, w, d)
            # if fail:
            #     break
            for l in lrange:
                failfunction()
                if fail:
                    break
