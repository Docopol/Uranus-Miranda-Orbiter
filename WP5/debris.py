import math
import numpy as np

size_freq=[
    [50,100,150,200,250,300,350,400,450,500,550,600,650,700],
    [6,7,80,140,89,65,17,20,9,1,4,0,2,1]
]
#size_freq=np.asarray(size_freq)
tot_sum=np.sum(size_freq[1])
size_freq[1]=size_freq[1]/tot_sum

flux=[
    [50,100,150,200,250,300,350,400,450,500,550,600,650,700],
    [0]#...
]
A_Earth = 510.1 * 10**9 #m^2
