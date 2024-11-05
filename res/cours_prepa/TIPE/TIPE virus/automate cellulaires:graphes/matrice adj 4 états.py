#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 00:11:53 2023

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
    L = [0,0,0,0]
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
                if etat[s] == 1:
                    nouvel_etat[i] = 1
                    break
        elif etat[i] == 1:
            if bernoulli(pm) == 1:
                nouvel_etat[i] = 2
            elif bernoulli(pr) == 1:
                nouvel_etat[i] = 3
    return nouvel_etat


def simu_adj(n, v, pr, pm):
    ville = population_ville(n, v)
    etat = init(n)
    D = compte(etat)

    S, I, R, M, T, POPULATION = [D[0]], [D[1]], [D[2]], [D[3]], [0], [n]
    t = 0
    infectes = D[1]

    while not infectes == 0 and t < 50:
        t += 1
        etat = suivant_adj(etat, ville, pr, pm)
        D = compte(etat)
        infectes = D[1] 
        S.append(D[0])
        I.append(infectes)
        R.append(D[2])
        M.append(D[3])
        T.append(t)
        POPULATION.append(n - D[3])

    return S, I, R, M, T, POPULATION

p = 0.9
q = 0.9
pop = 10000
v = 3

import matplotlib.pyplot as plt

S, I, R, M, T, POPULATION = simu_adj(pop, v, p, q)

plt.close()
plt.plot(T, S)
plt.plot(T, I)
plt.plot(T, R)
plt.plot(T, M)
plt.title("Matrice adjacente")
plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(["Saine", "Infecté ", "Rétabli", "Mort"])
plt.show()

def a(n, v):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simu_adj(n, v, p/2000, q/2000)
            if (R[-1] + M[-1]) >= 85 * n / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)


#%%