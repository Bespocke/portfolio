#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 01:10:26 2023

@author: a.
"""

import random as rd

def population_ville(n,v):
    ville = [[]for i in range(n)]
    for i in range(n):
        while len(ville[i]) < 0.7*v:
            a = rd.randint(0,n-1)
            if a != i and a not in ville[i]:
                ville[i].append(a)
                ville[a].append(i)
    return ville


def init(n):
    etat = [0 for _ in range(n)]
    for i in range(int(0.01*n)):
        etat[rd.randrange(n)] = 1
    return etat

def compte(G):
    L = [0,0,0,0]
    for k in G:
        L[k] += 1
    return L

def bernoulli(p):
    if rd.random() <= p:
        return 1
    return 0


def suivant_adj(etat,ville,p1,p2):
    nouvel_etat = [0 for _ in range(len(etat))]
    for i in range(len(ville)):
        if etat[i] == 0:
            for s in ville[i]:
                if etat[s] == 1 and bernoulli(p2) == 1:
                    nouvel_etat[i] = 1
                    break
        elif etat[i] == 1:
            if bernoulli(p1) == 1:
                nouvel_etat[i] = 3
            else:
                nouvel_etat[i] = 2
        else:
            nouvel_etat[i] = etat[i]
    return nouvel_etat

def simu_adj(n,v,p1,p2):
    ville = population_ville(n,v)
    etat = init(n)
    C = compte(etat)
    S,I,R,M,T,POPULATION = [C[0]],[C[1]],[C[2]],[C[3]],[0],[n]
    i = 0

    while C[1] != 0:
        i+=1
        etat = suivant_adj(etat,ville,p1,p2)
        C = compte(etat)
        S.append(C[0])
        I.append(C[1] + C[2]+C[3])
        R.append(C[2])
        M.append(C[3])
        T.append(i)
        POPULATION.append(POPULATION[0] - C[3])

    return S,I,R,M,T,POPULATION

p = 0.29
q = 0.63
pop = 100
v = 3

import matplotlib.pyplot as plt

S,I,R,M,T,POPULATION = simu_adj(pop,v,p,q)

plt.close()
plt.plot(T,S)
plt.plot(T,I)
plt.plot(T,R)
plt.plot(T,M)
plt.plot(T,POPULATION)
plt.legend(["saine","infecte_total ","retabli","mort",'population'])
plt.show()

def a(n, v):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simu_adj(n, v, p/100, q/100)
            if (R[-1]+M[-1]) >= 70 * popl[0] / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)