#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 19:30:18 2022

@author: a.
"""

from scipy.integrate import odeint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate

alpha = 0.057 #contamination
beta = 0.5 #guérison
delta = 0.1 #contamination après guérison
gamma = 0.0002 #mortalité 

Nt = 1000
tmax = 30

x0 = 1
y0 = 0
z0 = 0
w0 = Nt - x0 - y0 - z0

wlist = [w0]
xlist = [x0]
ylist = [y0]
zlist = [z0]


def derivative(X, t, alpha, beta, delta, gamma):
    w, x, z = X
    
    wlist.append(w)
    xlist.append(x)
    
    zlist.append(z)
    
    dotw = -alpha * w * x + beta * x #susceptible
    dotx = alpha * w * x - beta * x - gamma * x #infecté
    #doty = beta * x #rétabli
    dotz = gamma * x #mort
    
    return np.array([dotw, dotx,  dotz])


#Résoudre avec odeint


t = np.linspace(0,tmax, Nt)

X0 = [w0, x0, z0]
res = integrate.odeint(derivative, X0, t, args = (alpha, beta, delta, gamma))
w, x, z = res.T

(2, 1000)

if len(wlist) != Nt:
    if len(wlist) < Nt:
        while len(wlist) < Nt:
            wlist.append(wlist[-1])    
            xlist.append(xlist[-1]) 
           
            zlist.append(zlist[-1])
    if len(wlist) > Nt:
        while len(wlist) > Nt:
            wlist.pop() 
            xlist.pop() 
            
            zlist.pop()

plt.figure()

plt.grid()
plt.title("Lotka-Volterra")

plt.plot(t,wlist)
plt.plot(t,xlist)

plt.plot(t,zlist)
   
#plot en nuage de points     
#plt.plot(t, w, 'xb', label = 'Susceptible', color = 'green')
#plt.plot(t, x, '+r', label = "Infectés", color = 'red')
#plt.plot(t, y, 'xb', label = 'Rétabli', color = 'blue')
#plt.plot(t, z, 'xb', label = 'Mort', color = 'black')

plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(['Susceptible', 'Infectés', 'Mort'])




plt.show()



