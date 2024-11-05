
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import copy
import random as rd
import math
import random
import numpy as np
#1 sain
#2 infecté jour 0
#3 infecté jour 1
#4 infecté jour 2
#5 infecté jour 3
#6 infecté jour 4
#7 infecté jour 5
#8 infecté jour 6
#9 infecté jour 7
#10 rétabli
#11 morts

#C centre commercial modèle SIRM
#T centre travail modeèle knn
#A rue modèle mouvements proches
#R centre résidentiel modèle matrices d'adjacences

def creer_pop(n,i):
    D={}
    for i in range(1,n+1):
        D[i]=(1,0)
    for j in range(i):
        r=rd.randint(0,n-1)
        D[r]=(2,0)
    return(D)

def moyenne_liste(L):
    H=[]
    for l in L:
        if l not in H:
            H.append(l)
    return(sum(H)/len(H))

def generer_grille(taille):
    return [[(0,0) for _ in range(taille)] for _ in range(taille)]

def placement_aleatoire(taille,L):
    G=generer_grille(taille)
    for l in L:
        continuer = True
        while continuer:
            x,y=rd.randint(0,len(G)-1),rd.randint(0,len(G)-1)
            if G[x][y]==(0,0):
                G[x][y]=l
                continuer = False
    return G

def afficher(M):
    n = len(M)
    M2 = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x, y = M[i][j]
            M2[i][j] = y

    cmap = ListedColormap(["white", "forestgreen", "lemonchiffon", "yellow", "orange", "darkorange",
                           "orangered", "red", "firebrick", "darkred", "blue", "black"])
    bounds = np.arange(13) - 0.5
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(M2, cmap=cmap, norm=norm)
    plt.colorbar(ticks=np.arange(12), boundaries=bounds)
    plt.show()

def bernoulli(pb):
    if random.random() <= pb:
        return 1
    return 0

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

def propagation(D,grilleR,grilleA,grilleC,grilleT,listeR,listeT,listeA,listeC,pc,pr,pm):
    for p in D:
        if not p[1]==0:
            if p[1]<8 and bernoulli(pm)==1:
                p[1]=10
            elif p[1]<8 and bernoulli(pm)==0:
                p[1]+=1

            if p[1]==8 and bernoulli(pm)==1:
                p[1]==10
            elif p[1]==8 and bernoulli(pr)==1:
                p[1]==9

    new_grilleR=placement_aleatoire(grilleR,listeR)
    new_grilleA=placement_aleatoire(grilleA,listeA)
    new_grilleC=placement_aleatoire(grilleC,listeC)
    new_grilleT=placement_aleatoire(grilleT,listeT)

    DR=compte(propagation_adjacence(new_grilleR,pr,pm))
    DA=compte(propagation_proche(new_grilleA,pm,pr))
    DT=compte(propagation_knn(new_grilleT,pr,pm))

    D = {
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

    for e in D:
        D[e]=DR[e]+DA[e]+DT[e]

    T,S,I,R,M=propagation_sirm()
    moy=moyenne_liste(I)






