#%%

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

S = [0 for i in range(45)]

I = [1,1,3,10,40,110,305,400,600,950,1300,2000,2910,4500,6000,8300,10000,35550,40000,45000,60000,79000,90000,135000,150000,200000,300000,500000,630000,800000,985000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000,1000000]
R = [0,0,0,0,0,0,0,0,0,0,2,4,5,20,40,90,150,190,350,600,1400,1800,2500,2550,2780,3000,4950,6000,10320,11120,15200,20300,35000,80000,95000,160000,260000,345000,400000,450000,590000,650000,735000,735000,735000]
M = [0,0,0,1,3,3,5,20,35,37,60,90,140,300,550,900,1400,2500,3800,4980,7000,8900,10000,13450,16000,18000,22000,25000,35000,39000,43000,55000,57000,60000,92000,100000,135000,150000,160000,180000,197000,210000,223000,240000,265000]

for i in range (len(M)):
    S[i] = 1000000 - I[i]

T = np.arange(45)
T_smooth = np.linspace(0, 44, 300)

# Smooth the curves using cubic spline interpolation
S_smooth = make_interp_spline(T, S)(T_smooth)
I_smooth = make_interp_spline(T, I)(T_smooth)
R_smooth = make_interp_spline(T, R)(T_smooth)
M_smooth = make_interp_spline(T, M)(T_smooth)

plt.close()
plt.plot(T_smooth, S_smooth)
plt.plot(T_smooth, I_smooth)
plt.plot(T_smooth, R_smooth)
plt.plot(T_smooth, M_smooth)
plt.title("Simulation")
plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(["Susceptible","Infecté","Rétabli","Mort"])
plt.show()



#%%