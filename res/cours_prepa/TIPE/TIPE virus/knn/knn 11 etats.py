#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 20:32:44 2023

@author: a.
"""
#%%

import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import copy
import random as rd
import numpy as np

def generer(n):
    return [[0] * n for _ in range(n)]

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def liste_voisins(M, p, k):
    def f(L):
        return L[0]

    a, b = p
    D = []
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] != 0 and not (a,b)==(i,j):
                p2 = (i, j)
                D.append((distance(p, p2), (i, j)))

    return sorted(D, key=f)[:int(k)]


def etiquette_maj(M, V):
    D = {}
    for (_, e) in V:
        x, y = e
        if M[x][y] not in D:
            D[M[x][y]] = 1
        else:
            D[M[x][y]] += 1
    e_maj = None
    M_max = 0
    for e in D:
        if D[e] > M_max:
            e_maj = e
            M_max = D[e]
    return e_maj

def bernoulli(pb):
    if random.random() <= pb:
        return 1
    return 0

def init(n, v, l):
    M = generer(n)
    for _ in range(v):
        continuer = True
        while continuer:
            x,y = rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
            if M[x][y] == 0:
                M[x][y] = 1
                continuer = False
    for _ in range(l):
        continuer = True
        while continuer:
            x,y = rd.randint(0,len(M)-1),rd.randint(0,len(M)-1)
            if M[x][y] == 0:
                M[x][y] = 2
                continuer = False
    return M

def propagation_epidemie(M, k, pr, pm):
    M2 = [row[:] for row in M]  # Copie temporaire de la matrice

    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] >= 2 and M[i][j]<9:  # Cellule infectée
                if bernoulli(pr) == 1:  # Probabilité de guérison
                    M2[i][j] = 10  # La cellule guérit
                elif bernoulli(pm) == 1:  # Probabilité de mourir
                    M2[i][j] = 11  # La cellule meurt
                else :
                    M2[i][j] = M[i][j] + 1
            if M[i][j] == 9:
                if bernoulli(pr) == 1:
                    M2[i][j] = 10
                else:
                    M2[i][j] = 11

    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == 1:  # Cellule saine
                voisins = liste_voisins(M, (i, j), k)
                e=etiquette_maj(M, voisins)
                if e in [2,3,4,5,6,7,8,9]:  # La majorité des voisins sont infectés
                    M2[i][j] = 2  # La cellule devient infectée

    return M2


def afficher(M):
    M = np.array(M)
    
    cmap = ListedColormap(["white", "forestgreen", "lemonchiffon", "yellow", "orange", "darkorange",
                           "orangered", "red", "firebrick", "darkred", "blue", "black"])
    bounds = np.arange(13) - 0.5
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(M, cmap=cmap, norm=norm)
    plt.colorbar(ticks=np.arange(12), boundaries=bounds)
    plt.show()

def afficher2(M):
    plt.imshow(M)
    plt.show()
    
def compte(M):
    occurences = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0
    }


    for row in M:
        for cell in row:
            if cell in occurences:
                occurences[cell] += 1

    return occurences

def simulation(n, v, l, k, pr, pm):
    M = init(n, v, l)
    D = compte(M)
    t = 0
    S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[10]], [D[11]], [t], [D[1]+D[2]]
    popi=D[1]+D[2]
    continuer = True    

    while continuer:
        t += 1
        print(t)
        M = propagation_epidemie(M, k, pr, pm)
        D = compte(M)
        infecte = D[2] + D[3] + D[4] + D[5] + D[6] + D[7] + D[8] + D[9]
        S.append(D[1])
        I.append(infecte + D[10] + D[11])
        R.append(D[10])
        Mo.append(D[11])
        T.append(t)
        popl.append(popi - D[11])
  

        if infecte == 0:

            continuer = False

    plt.close()
    plt.plot(T, S)
    plt.plot(T, I)
    plt.plot(T, R)
    plt.plot(T, Mo)
    plt.title("Voisin proche")
    plt.xlabel('Temps / jours')
    plt.ylabel('Population')
    plt.legend(["Saine", "Infecté total", "Rétabli", "Mort"])
    plt.show()
    return S, I, R, Mo, T, popl


def mouvement(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]!=0:
                dx,dy=rd.randint(-1,1),rd.randint(-1,1)
                if i+dy<=len(M)-1 and i+dy>=0 and M[i+dy][j]==0:
                    M[i+dy][j]=M[i][j]
                    M[i][j]=0
                    if j+dx<=len(M)-1 and j+dx>=0 and M[i+dy][j+dx]==0:
                        M[i+dy][j+dx]=M[i+dy][j]
                        M[i+dy][j]=0
                elif j+dx<=len(M)-1 and j+dx>=0 and M[i][j+dx]==0:
                    M[i][j+dx]=M[i][j]
                    M[i][j]=0
                    if i+dy<=len(M)-1 and i+dy>=0 and M[i+dy][j+dx]==0:
                        M[i+dy][j+dx]=M[i][j+dx]
                        M[i][j+dx]=0
    return(M)

def eliminer_mort(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j]==11:
                M[i][j]=0
    return(M)

def simulation_mouvement(n, v, l, k, pr, pm):
    M = init(n, v, l)
    D = compte(M)
    t = 0
    mort = D[11]
    S, I, R, Mo, T, popl = [D[1]], [D[2]], [D[10]], [D[11]], [t], [D[1]+D[2]]
    popi=D[1]+D[2]
    continuer = True


    while continuer:
        t += 1
        print(t)
        M = mouvement(M)
        M = propagation_epidemie(M, k, pr, pm)
        D = compte(M)
        mort+=D[11]
        M=eliminer_mort(M)
        infecte = D[2] + D[3] + D[4] + D[5] + D[6] + D[7] + D[8] + D[9]
        S.append(D[1])
        I.append(infecte + D[10] + mort)
        R.append(D[10])
        Mo.append(mort)
        T.append(t)
        popl.append(popi - mort)


        if infecte == 0:

            continuer = False

    plt.close()
    plt.plot(T, S)
    plt.plot(T, I)
    plt.plot(T, R)
    plt.plot(T, Mo)
    plt.title("Voisin proche avec mouvement")
    plt.xlabel('Temps / jours')
    plt.ylabel('Population')
    plt.legend(["Saine", "Infecté total", "Rétabli", "Mort"])
    plt.show()

    return S, I, R, Mo, T, popl

def a(n, v, l, k):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation_mouvement(n, v, l, k, p/100, q/100)
            if (R[-1]+M[-1]) >= 70 * popl[0] / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def t(n, v, l, k):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation(n, v, l, k, p/100, q/100)
            M_updated[p][q] = T[-1]
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

simulation_mouvement(60,2500,200,1,0.9,0.1)

#%%