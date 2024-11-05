#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 00:04:50 2023

@author: a.
"""

#%%

import random as rd
import copy

def population_ville(n,v):
    ville = [[] for _ in range(n)]
    for i in range(n):
        while len(ville[i]) < 0.7 * v:
            a = rd.randint(0, n-1)
            if a != i and a not in ville[i]:
                ville[i].append(a)
                ville[a].append(i)
    return ville


def init(n):
    etat = [0 for _ in range(n)]
    etat[rd.randrange(n)] = 1
    return etat


def compte(G):
    L = [0,0,0,0,0,0,0,0,0,0,0]
    for k in G:
        L[k] += 1
    return L



def bernoulli(p):
    if rd.random() <= p:
        return 1
    return 0


def suivant_adj(etat, ville, pr, pm):
    nouvel_etat = copy.deepcopy(etat)
    for i in range(len(ville)):
        if etat[i] == 0:
            for s in ville[i]:
                if etat[s] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    nouvel_etat[i] = 1
                    break
        elif etat[i] in [1, 2, 3, 4, 5, 6, 7]:
            if bernoulli(pm) == 1:
                nouvel_etat[i] = 10
            elif bernoulli(pr) == 1:
                nouvel_etat[i] = 9
            else:
                nouvel_etat[i] = etat[i] + 1
        elif etat[i] == 8:
            if bernoulli(pr) == 1:
                nouvel_etat[i] = 9
            elif bernoulli(pm) == 1:
                nouvel_etat[i] = 10
    return nouvel_etat


def simu_adj(n, v, pr, pm):
    ville = population_ville(n, v)
    etat = init(n)
    D = compte(etat)

    S, I, R, M, T, POPULATION = [D[0]], [D[1]], [D[9]], [D[10]], [0], [n]
    t = 0
    infectes = D[1] + D[2] + D[3] + D[4] + D[5] + D[6] + D[7] + D[8]

    while infectes > 0 and t < 50:
        t += 1
        etat = suivant_adj(etat, ville, pr, pm)
        D = compte(etat)
        infectes = D[1] + D[2] + D[3] + D[4] + D[5] + D[6] + D[7] + D[8]
        S.append(D[0])
        I.append(infectes )
        R.append(D[9])
        M.append(D[10])
        T.append(t)
        POPULATION.append(n - D[10])

    return S, I, R, M, T, POPULATION

p = 0.63
q = 0.29
pop = 10000
v = 3

import matplotlib.pyplot as plt

S, I, R, M, T, POPULATION = simu_adj(pop, v, p, q)

plt.close()
plt.plot(T, S)
plt.plot(T, I)
plt.plot(T, R)
plt.plot(T, M)
plt.title("Matrices adjacentes")
plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(["Saine", "Infecté total", "Rétabli", "Mort"])
plt.show()

def a(n, v):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simu_adj(n, v, p/100, q/100)
            if max(I) >= 50* popl[0] / 100:
                M_updated[p][q] = max(I)*100/n
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def t(n,v):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simu_adj(n, v, p/100, q/100)
            M_updated[p][q] = T[-1]
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)


#%%