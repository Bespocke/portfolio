from random import *
from math import *
from matplotlib.pyplot import *

def distance(p1,p2):
    d = len(p1)
    s = 0
    for k in range(d):
        s += (p1[k] - p2[k])**2
    return sqrt(s)

def liste_voisins(p,k,L):
    def f (p2):
        return distance(p,p2[0])
    return sorted(L,key = f)[:k]

def etiquette_maj(V):
    D = {}
    for (_,e) in V:
        if e in D:
            D[e] += 1
        else:
            D[e] = 1
    max = 0
    for e in D:
        if D[e] > max:
            e_maj = e
            max = D[e]
    return e_maj

def knn(p,k,L):
    V = liste_voisins(p,k,L)
    return etiquette_maj(V)


def fichier_vers_liste(nom):
    f = open(nom, 'r')
    L = []
    for ligne in f.readlines():
        ligne = ligne.strip()
        l = ligne.split(',')
        x,y,e = l
        L.append(((float(x),float(y)),int(e)))
    f.close()
    return L

L1 = fichier_vers_liste("L1.txt")

def afficher(L1):
    plot([x[0][0] for x in L1 if x[1] == 0], [y[0][1] for y in L1 if y[1] == 0], "+r")
    plot([x[0][0] for x in L1 if x[1] == 1], [y[0][1] for y in L1 if y[1] == 1], "xb")

d = len(L1)*80//100

L1train = L1[:d]
L1test = L1[d:]

def test(L1test, L1train, k, m):
    total_erreur = 0
    matrice_confusion = [[0 for _ in range(m)]for _ in range(m)]
    for i in range(len(L1test)):
        e_predit = knn(L1test[i][0], k, L1train)
        e_correct = L1test[i][1]
        matrice_confusion[e_correct][e_predit] += 1
        if e_predit != e_correct:
            total_erreur += 1
    return total_erreur/len(L1test), matrice_confusion

for k in range(1,41):
    print(k, test(L1test, L1train, k, 2))


L2 = fichier_vers_liste("L2.txt")
d = len(L2)*80//100

L2train = L2[:d]
L2test = L2[d:]



for k in range(1,41):
    total_erreur = 0
    for i in range(len(L1test)):
        e_predit = knn(L1test[i][0], k, L1train)
        e_correct = L1test[i][1]
        total_erreur += abs(e_predit-e_correct)
    print(k, total_erreur)


def inserer(p,p2,V):
    if V == []:
        V.append(p2)
        return
    pfin = V[-1]
    if distance(p,pfin[0]) <= distance(p,p2[0]):
        V.append(p2)
    else:
        V.pop()
        inserer(p,p2,V)
        V.append(pfin)




def liste_voisins(p,k,L):
    V = []
    for i in range(k):
        inserer(p,L[i], V)
    for i in range(k,len(L)):
        inserer(p,L[i],V)
        V.pop()
    return V

#Cette version est en O(kn), la version précédente était en O(n ln n)






