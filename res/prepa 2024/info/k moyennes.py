import numpy as np
from random import *
from math import *
import matplotlib.pyplot as plt

def distance(p1,p2):
    return np.sqrt(sum((p1-p2)**2))

def moyenne(L):
    d = len(L[0])
    n = len(L)
    s = np.zeros(d)
    for i in range(n):
        s += L[i]
    return s/n


def indice_plus_proche(p, M):
    m = distance(p, M[0])
    im = 0
    for i in range(1,len(M)):
        d = distance(p, M[i])
        if d < m:
            m = d
            im = i
    return im

def initialisation(k, X):
    return X[:k]

#Version plus adaptée pour la partie 3 :
def initialisation(k, X):
    return [X[randint(0,len(X)-1)] for _ in range(k)]

def k_moyennes(X, k):
    n = len(X)
    d = len(X[0])
    M = initialisation(k, X)
    continuer = True
    while continuer:
        P = [[] for _ in range(k)]
        for p in X:
            i = indice_plus_proche(p,M)
            P[i].append(p)
        M2 = [moyenne(L) for L in P]
        if np.array_equal(M, M2):
            continuer = False
        else:
            M = M2
    return P,M

def generer(k, n, e):
    M = [np.array([random(), random()]) for _ in range(k)]
    X = []
    for _ in range(n):
        i = randint(0,k-1)
        m = M[i]
        theta = random()*pi
        d = np.random.normal(0,e,1)[0]
        x, y = m
        p = np.array((x + cos(theta)*d, y + sin(theta)*d))
        X.append(p)
    return X

X = generer(3,1000, 0.2)
def afficherX(X):
    Xa = [x[0] for x in X]
    Xo = [x[1] for x in X]
    scatter(Xa,Xo)
    show()



C = [".b",".y", ".r",".k",".g",".m" ]

def afficherP(P):
    for i in range(len(P)):
        La = [x[0] for x in P[i]]
        Lo = [x[1] for x in P[i]]
        plot(La,Lo,C[i])
    show()



P = k_moyennes(X,3)



img = np.array(plt.imread('buffon.jpg'))
plt.figure()
plt.imshow(img) #
plt.title('Image de depart')
plt.show()

X = []
n,p,_ = img.shape

for i in range(n):
    for j in range(p):
        X.append(img[i][j])

P,M = k_moyennes(X,16)

img2 = np.zeros((n,p,3),dtype=np.uint8)

for i in range(n):
    for j in range(p):
        m = indice_plus_proche(img[i][j], M)
        img2[i][j] = M[m]

plt.figure()
plt.imshow(img2)
plt.title('Image compressee')
plt.show()