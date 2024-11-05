#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 01:12:32 2023

@author: a.
"""
#%%

import numpy as np
import random as rd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

def grille(n) :
    M=[]
    for i in range(n) :
        L=[ ]
        for j in range(n): L.append(0)
        M.append(L)
    return M

#initialisation d'une grille avec un infecté au milieu
def init(n):
    G = grille(n)
    k,l = rd.randrange(n),rd.randrange(n)
    G[n//2][n//2] =1
    return G

#fonction qui compte le nombre de personnes dans chaque etat
def compte(G):
    L = [0,0,0,0]
    for s in G:
        for k in s:
            L[k] += 1
    return L

''' on est exposé si une des 8 cases qui nous entoure est infectée'''
#permet de savoir si un point du graphe est exposé a quelqun d'infecté
def est_exposee(G,i,j):
    n = len(G)
    if i==j==0:
        if G[0][1] == 1 or G[1][1] == 1 or G[0][1] == 1:
            return True
    elif i == 0 and j == n-1:
        if G[0][n-2] == 1 or G[1][n-2] == 1 or G[1][n-1] == 1:
            return True
    elif i == n-1 and j == 0:
        if G[n-1][1] == 1 or G[n-2][1] == 1 or G[n-2][0] == 1:
            return True
    elif i ==j==n-1:
        if G[n-1][n-2] == 1 or G[n-2][n-2] == 1 or G[n-2][n-1] == 1:
            return True
    elif i == 0 and 1<=j<=n-2:
        if G[0][j-1] == 1 or G[0][j+1] == 1 or G[1][j-1] == 1 or G[1][j]==1 or G[1][j+1]==1:
            return True
    elif i == n-1 and 1<=j<=n-2:
        if G[n-1][j-1] == 1 or G[n-1][j+1] == 1 or G[n-2][j-1] == 1 or G[n-2][j]==1 or G[n-2][j+1]==1:
            return True
    elif j == 0 and 1<=i<=n-2:
        if G[i-1][0] == 1 or G[i+1][0] == 1 or G[i-1][1] == 1 or G[i][1]==1 or G[i+1][1]==1:
            return True
    elif j == n-1 and 1<=i<=n-2:
        if G[i-1][n-1] == 1 or G[i+1][n-1] == 1 or G[i-1][n-2] == 1 or G[i][n-2]==1 or G[i+1][n-2]==1:
            return True
    else:
        if G[i-1][j-1] == 1 or G[i-1][j] == 1 or G[i-1][j+1] == 1 or G[i][j-1]==1 or G[i][j+1]==1 or G[i+1][j-1]==1 or G[i+1][j]==1 or G[i+1][j+1]==1:
            return True
    return False

def afficher(M):
    cmap = ListedColormap([ 'green', 'red', 'blue', 'black'])
    bounds = [0, 1, 2, 3, 4]
    norm = BoundaryNorm(bounds, cmap.N)
    plt.imshow(M, cmap=cmap, norm=norm)
    plt.colorbar(ticks=[0, 1, 2, 3], boundaries=bounds)
    plt.show()

def bernoulli(p):
    if rd.random() <= p:
        return 1
    return 0

#calcule la genération suivante
def suivant(G,p1,p2):
    n = len(G)
    G_suivant = grille(n)
    for i in range(n):
        for j in range(n):
            if G[i][j] == 0:
                if est_exposee(G,i,j) and bernoulli(p2) == 1:
                    G_suivant[i][j] = 1
            elif G[i][j] == 1:
                if bernoulli(p1) == 1:
                    G_suivant[i][j] = 3
                else:
                    G_suivant[i][j] = 2
            else:
                G_suivant[i][j] = G[i][j]
    return G_suivant

''' simulation de l'épidémie'''
#renvois les listes du nombre de la population dans les différents états par jour
def simulation(n,p1,p2):
    G = init(n)
    C = compte(G)
    S,I,R,M,T,POPULATION = [C[0]],[C[1]],[C[2]],[C[3]],[0],[n**2]
    i = 0


    while C[1] != 0:
        i += 1

        G = suivant(G,p1,p2)


        C = compte(G)
        S.append(C[0])
        I.append(C[1] )
        R.append(C[2])
        M.append(C[3])
        POPULATION.append(POPULATION[0] - C[3])
        T.append(i)
    L= compte(G)
    for i in range(len(L)):
        L[i] = L[i] / (n**2)
    return S,I,R,M,T,POPULATION

#calcul du seuil épidémique

def seuil(Lp2,Lxa):
    for i in range(len(Lp2)):
        if Lxa[i] >= 0.5:
            return [Lp2[i-1],Lp2[i]]


def valeur_courbe(n,m,p1):
    L,M = [0],[]
    u = 0.29
    K = simulation(n,p1,u)
    compteur = K[2] + K[3]
    M.append(compteur)
    for i in range(m+1):
        u = u + 1/(1000)
        L.append(u)
        K = simulation(n,p1,u)
        compteur = K[2] + K[3]
        if 0.8>= u >= 0.2:
            while compteur < M[-1]:
                K = simulation(n,p1,u)
                compteur = K[2] + K[3]
        M.append(compteur)
    return L,M

''' affichage de courbe pour des conditions choisies'''
p = 0.9
q = 0.1
pop = 10  #vraie population = pop**2

S,I,R,M,T,POPULATION = simulation(pop,p,q)

plt.close()
plt.plot(T,S)
plt.plot(T,I)
plt.plot(T,R)
plt.plot(T,M)
plt.title("Automate cellulaire")
plt.xlabel('Temps / jours')
plt.ylabel('Population')
plt.legend(["susceptible","infecte ","retabli","mort"])
plt.show()


def a(n):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation(n, p/100, q/100)
            if (R[-1]+M[-1]) >= 70 * popl[0] / 100:
                M_updated[p][q] = 1
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def ac(n):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation(n, p/100, q/100)
            M_updated[p][q] = max(I)*100/n
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)

def t(n):
    M_updated = [[0 for i in range(100)] for j in range(100)]  # Create a new list to store updated values
    for p in range(100):
        for q in range(100):
            print(p,q)
            S, I, R, M, T, popl = simulation(n, p/100, q/100)
            M_updated[p][q] = T[-1]
    plt.imshow(M_updated)
    plt.show()
    return (M_updated)


#%%

