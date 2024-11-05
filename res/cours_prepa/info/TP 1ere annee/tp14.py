def indice_distance_min(L,D):
    imin = 0
    for i in range(1,len(L)):
        if D[L[i]]<D[L[imin]]:
            imin = i
    return imin

def dijkstra(G,s):
    n = len(G)
    D = [float("inf")]*n
    D[s] = 0
    P = [None]*n
    L = list(range(n))
    while L != []:
        i = indice_distance_min(L,D)
        u = L.pop(i)
        for v,w in G[u]:
            d2 = D[u] + w
            if d2 < D[v]:
                D[v] = d2
                P[v] = u
    return D,P

G1 = [[(1,10), (4,5)], [(2,1),(4,2)], [(3,4)], [(2,6),(0,7)],[(1,3),(2,9),(3,2)]]

def chemin(pred,u):
	if pred[u] == None:
		return [u]
	return chemin(pred,pred[u])+[u]

#Contre-exemple avec poids négatifs, la distance et le plus court chemin de 0 à 3 ne seront pas corrects :

G2 = [[(2,2), (3,2), (1,3)], [(2,-3)], [(3,1)], []]

def indice_min_A_etoile(L,D,h,d):
    imin = 0
    for i in range(1,len(L)):
        u = L[i]
        v = L[imin]
        if D[u] + h(u,d) < D[v] + h(v,d):
            imin = i
    return imin

def A_etoile(G,s,d,h):
    n = len(G)
    D = [float("inf")]*n
    D[s] = 0
    P = [None]*n
    L = [s]
    while L != []:
        i = indice_min_A_etoile(L,D,h,d)
        u = L.pop(i)
        if u == d:
            return D[d], chemin(P,d)
        for v,w in G[u]:
            d2 = D[u] + w
            if d2 < D[v]:
                D[v] = d2
                P[v] = u
                if v not in L:
                    L.append(v)
    return "le sommet cible n'a pas été atteint"

pos = [(0, 0), (1, 2), (-3, -1), (4, -1), (2,2)]

def h(u,d):
    x1,y1 = pos[u]
    x2,y2 = pos[d]
    return ((x2 - x1)**2 +  (y2 - y1)**2)**0.5

pos = [(0, 0), (1, 2), (-3, -1), (4, -1), (2,2)]


A_etoile(G1,0,4,h)

dijkstra(G1,0)

#Pour obtenir un exemple où A* ne renvoie pas le chemin optimal, on peut placer 4 très loins des autres sommets (en position, sans changer les poids du graphe)

pos = [(0, 0), (1, 2), (-3, -1), (4, -1), (20,20)]

A_etoile(G1,0,1,h)

dijkstra(G1,0)

def element_min(L,D,d,h):
    dmin = float('inf')
    for u in L:
        du = D[u] + h(u,d)
        if du < dmin:
            umin = u
            dmin = du
    return umin

from copy import deepcopy
def A_etoile_grille(M,s,d,h):
    n,p = len(M), len(M[0])
    D = {s : 0}
    P = {s : None}
    L = {s}
    k=0
    while len(L)>0:
        k+=1
        u = element_min(L,D,d,h)
        L.remove(u)
        if u == d:
            return k, D[d], chemin(P,d)
        x,y = u
        for v in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            x2,y2 = v
            if 0<=x2<n and 0<=y2<p and M[x2][y2] != 1:
                d2 = D[u] + 1
                if v not in D or d2 < D[v]:
                    D[v] = d2
                    P[v] = u
                    L.add(v)
    return "destination inaccessible"

M = [[0,0,0,0,0],[0,0,0,0,0],[0,1,1,1,1],[0,0,0,0,0],[1,1,1,1,0],[0,0,0,0,0]]

import matplotlib.pyplot as plt


import numpy as np


def carte(n,p,q):
    #crée une carte n*p avec une proba q d'obstacles au centre, et plus faible en périphérie
    return [[np.random.binomial(1,q*(1 - 4*((i-(n-1)/2)**2 + (j-(p-1)/2)**2)/((n-1)**2+(p-1)**2))) for j in range(p)] for i in range(n)]


def tracer_progressif(M,s,d,h):
    n,p = len(M), len(M[0])
    D = {s : 0}
    P = {s : None}
    L = {s}
    N = deepcopy(M)
    plt.imshow(N)
    while len(L)>0:
        u = element_min(L,D,d,h)
        L.remove(u)
        x,y = u
        N[x][y]=-2
        for x,y in chemin(P,u):
            N[x][y] = -3
        plt.pause(0.001)
        plt.clf()
        plt.imshow(N)
        if u == d:
            plt.pause(0.001)
            return D[d], chemin(P,d)
        for x,y in chemin(P,u):
            N[x][y] = -2
        for v in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            x2,y2 = v
            if 0<=x2<n and 0<=y2<p and M[x2][y2] != 1:
                N[x2][y2]=min(-1,N[x2][y2])
                d2 = D[u] + 1
                if v not in D or d2 < D[v]:
                    D[v] = d2
                    P[v] = u
                    L.add(v)
    return "destination inaccessible"

def h0(u,d):
    #heuristique nulle, ramenant à Dijkstra
    return 0

def h1(u,d):
    #distance euclidienne
    x1,y1 = u
    x2,y2 = d
    return ((x2 - x1)**2 +  (y2 - y1)**2)**0.5

def h2(u,d):
    #distance manhattan, terminaison un peu plus rapide
    x1,y1 = u
    x2,y2 = d
    return (abs(x2 - x1) +  abs(y2 - y1))


def h3(u,d):
    #distance manhattan doublée, terminaison (en général) beaucoup plus rapide, mais le résultat n'est plus optimal
    x1,y1 = u
    x2,y2 = d
    return (abs(x2 - x1) +  abs(y2 - y1))*2

def hw(w):
    #distance manhattan multipliée par w
    def h(u,d):
        x1,y1 = u
        x2,y2 = d
        return (abs(x2 - x1) +  abs(y2 - y1))*w
    return h

n = 70
p = 70

M = carte(n,p,0.5)

tracer_progressif(M,(0,0),(n-1,p-1),hw(1.1))

# for i in range(20):
#     w = 1 + i/10
#     k,d,c = A_etoile_grille(M,(0,0),(n-1,p-1),hw(w))
#     print(w)
#     print(k,d)
#
# for h in [h0,h1,h2,h3,hw(1.1)]:
#     k,d,c = A_etoile_grille(M,(0,0),(n-1,p-1),h)
#     print(h)
#     print(k,d)



