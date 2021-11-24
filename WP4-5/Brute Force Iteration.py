import numpy as np


wrange = np.linspace(...,...,100)
trange = np.linspace(...,...,100)
drange = np.linspace(...,...,100)
lrange = np.linspace(...,...,100)


for t in trange:
    w = wrange[-1]
    d = drange[-1]
    l = lrange[-1]
    fail = failfunction(t, w, d, l)
    if fail == True:
        break
    for w in wrange:
        d = drange[-1]
        l = lrange[-1]
        fail = failfunction(t, w, d, l)
        if fail == True:
            break
        for d in drange:
            l = lrange[-1]
            fail = failfunction(t, w, d, l)
            if fail == True:
                break
            for l in lrange:
                failfunction()
                if fail:
                    break
