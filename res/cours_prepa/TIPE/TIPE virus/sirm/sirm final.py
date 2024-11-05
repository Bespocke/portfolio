#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 00:52:59 2023

@author: a.
"""
#%%

from scipy.integrate import odeint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import uniform
from matplotlib.colors import ListedColormap, BoundaryNorm

def solve_SIRM(alpha, beta, gamma, Nt, tmax):
    x0 = 1
    y0 = 0
    z0 = 0
    w0 = Nt - x0 - y0 - z0

    wlist = [w0]
    xlist = [x0]
    ylist = [y0]
    zlist = [z0]

    def derivative(X, t, alpha, beta, gamma,):
        w, x, y, z = X
        wlist.append(w)
        xlist.append(x)
        ylist.append(y)
        zlist.append(z)

        alpha0 = uniform(alpha, alpha)
        beta0 = uniform(beta, beta)
        gamma0 = uniform(gamma, gamma)

        dotw = -alpha0 * w * x  # susceptible
        dotx = alpha0 * w * x - beta0 * x - gamma0 * x   # infecté
        doty = beta0 * x  # rétabli
        dotz = gamma0 * x  # mort

        return np.array([dotw, dotx, doty, dotz])

    t = np.linspace(0, tmax, Nt)

    X0 = [w0, x0, y0, z0]
    res = odeint(derivative, X0, t, args=(alpha, beta, gamma))
    w, x, y, z = res.T

    if len(wlist) != Nt:
        while len(wlist) < Nt:
            wlist.append(wlist[-1])
            xlist.append(xlist[-1])
            ylist.append(ylist[-1])
            zlist.append(zlist[-1])
        while len(wlist) > Nt:
            wlist.pop()
            xlist.pop()
            ylist.pop()
            zlist.pop()

    return t, wlist, xlist, ylist, zlist

alpha = 0.11 # contamination
beta = 0.6  # guérison
gamma = 0.3  # mortalité
delta = 0.3 # non immunité

Nt = 10000
tmax = 100

t, wlist, xlist, ylist, zlist = solve_SIRM(alpha, beta, gamma, Nt, tmax)

plt.figure()
plt.grid()
plt.title("SIRM")
plt.plot(t, wlist)
plt.plot(t, xlist)
plt.plot(t, ylist)
plt.plot(t, zlist)
plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(['Susceptible', 'Infectés', 'Rétabli', 'Mort'])
plt.show()

def a(Nt, tmax):
    M_updated = [[0 for i in range(50)] for j in range(50)]  # Create a new list to store updated values
    for p in range(50):
        for q in range(50):
            print(p,q)
            T, S, I, R, M = solve_SIRM(p/1000, q/10, q/10, Nt, tmax)
            if (R[-1] + M[-1]) >= 75 * Nt / 100:
                M_updated[p][q] = 1
    colors = ['yellow', 'purple']
    cmap = ListedColormap(colors)
    plt.imshow(M_updated, cmap=cmap)
    plt.show()
    return(M_updated)

def ac(Nt, tmax):
    M_updated = [[0 for i in range(50)] for j in range(50)]  # Create a new list to store updated values
    for p in range(50):
        for q in range(50):
            print(p,q)
            T, S, I, R, M = solve_SIRM(p/1000, q/10, q/10, Nt, tmax)
            M_updated[p][q] = max(I)*100/Nt
   
    plt.imshow(M_updated)
    
    plt.show()

def t(Nt, tmax):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            T, S, I, R, M = solve_SIRM(p/1000, q/100, q/100, Nt, tmax)
            t = 0
            for i in range(len(I)):
                if I[i] == max(I):
                    t = i
            M_updated[p][q] = t
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

a(1000,10)
#%%

