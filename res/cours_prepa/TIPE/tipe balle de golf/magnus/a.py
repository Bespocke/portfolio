#%%

import numpy as np
import sympy as sp
import sympy.vector as sv
sp.init_printing()
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 14

R0 = sv.CoordSys3D('R_0')
x = R0.x
y = R0.y

U0, R, K, Gamma = sp.symbols('U_0 R K Gamma')

# 1/ psi1 correspond à un champ uniforme
psi1 = U0*y

# verification equation de laplace
sv.divergence(sv.gradient(psi1))

# 2/ psi2 correspond à un doublet
psi2 = -K*y/(x**2+y**2)

sv.gradient(psi2)

# verification equation de laplace
sv.divergence(sv.gradient(psi2)).simplify()

# 3/ psi3 correspond à un tourbillon
psi3 = -Gamma/(2*sp.pi)*sp.log(x**2+y**2)

# verification equation de laplace
sv.divergence(sv.gradient(psi3)).simplify()

psi = psi1 + psi2.subs(K,U0*R**2) + psi3

def trace_solution(psi,R,titre): 
    # conversion fonction numpy
    F = sp.lambdify([R0.x,R0.y],psi,'numpy')
    # grille de calcul
    N = 40
    X1 = np.linspace(-3*R,3*R,N)
    Y1 = np.linspace(-2*R,2*R,N)
    X, Y = np.meshgrid(X1,Y1)
    FXY = F(X,Y)
    # filtrage
    for i in range(N):
        for j in range(N):
            if (X[i,j]**2 + Y[i,j]**2) < 0.8*R**2 : FXY[i,j] = 0.
    # tracer
    plt.figure(figsize=(10,8))
    ax = plt.gca()
    CS = ax.contour(X, Y, FXY, levels=31, cmap='coolwarm')
    ax.clabel(CS, inline=1, fontsize=10)
    plt.axis('equal')
    if titre != None : ax.set_title(titre)
    cercle = plt.Circle((0., 0.), R, color='k',zorder=10)
    ax.add_artist(cercle)
    return

rayon=1
valnum = { U0:2, R:0, Gamma:0}
psi0 = psi.subs(valnum)

trace_solution(psi0,rayon,"Ecoulement uniforme")

valnum = { U0:2, R:rayon, Gamma:0}
psi0 = psi.subs(valnum)

trace_solution(psi0,rayon,"Cylindre immobile")

valnum = { U0:2, R:rayon, Gamma:5}
psi0 = psi.subs(valnum)

trace_solution(psi0,rayon,"Cylindre en rotation")

Nabla = sv.Del()
rho0 = sp.symbols('rho_0')
p = sp.Function('p')(x,y)
u = sp.Function('u')(x,y)
v = sp.Function('v')(x,y)
U = u*R0.i + v*R0.j

# calcul de la pression
pr = rho0*U0**2/2 -rho0/2*U.dot(U)
pr = rho0*U0**2/2-rho0/2*sv.gradient(psi).dot(sv.gradient(psi))


valnum = { rho0:1, U0:2, R:rayon, Gamma:0}
pr0 = pr.subs(valnum)
trace_solution(pr0,rayon,"pression cylindre immobile")

valnum = { rho0:1, U0:2, R:rayon, Gamma:5}
pr0 = pr.subs(valnum)
trace_solution(pr0,rayon,"pression cylindre en rotation")

# %%

