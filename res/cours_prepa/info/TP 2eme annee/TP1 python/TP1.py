from random import *
from math import *
import numpy as np


def partie(n, f, g):
    coups_f = []
    coups_g = []
    for i in range(n) :
        # On copie les listes pour que les stratégies ne puissent pas tricher par effet de bord
        cf = f(i,coups_f.copy(), coups_g.copy())
        cg = g(i, coups_g.copy(), coups_f.copy())
        coups_f.append(cf)
        coups_g.append(cg)
    return coups_f, coups_g

#Liste des stratégies

def bisounours(i, moi, autre):
    return 1

def traître(i, moi, autre):
    return 0

def rancunier(i, moi, autre) :
    if i==0:
        return 1
    if autre[i-1]==0 or moi[i-1] == 0:
        return 0
    return 1

def sympa_irl(i, moi, autre):
    if i%3 == 2:
        return 0
    return 1

def miroir_méchant(i, moi, autre):
    if i==0:
        return 0
    return autre[i-1]

def miroir_gentil(i, moi, autre):
    if i==0:
        return 1
    return autre[i-1]

def mastermind(i, moi, autre):
    if i==0:
        return 0
    if i==1 or i==2:
        return 1
    if autre[0:3]==[1,1,1]:
        return 0
    return autre[i-1]



def majorité(i, moi, autre):
    a,b=0,0
    for c in autre[0:i]:
        if c==0:
            a+=1
        else:
            b+=1
    if a>b:
        return 0
    return 1

def indecis(p):
    def f(i, coups, adv):
        if random()<p:
            return 1
        return 0
    return f

def hacker(i,moi, autre):
    if i > 0:
        autre[i-1] = 1
    return 0

def score(T, C, P, D, a):
        #les deux tableaux sont donnés comme un couple, qu'on commence par éclater
    coups_f,coups_g = a
    score_f, score_g = 0,0
    for i in range(len(coups_f)):
        #On vérifie que les coups sont valides, pour détecter les stratégies qui ne suivent pas les règles du jeu. assert arrête la fonction et déclenche une exception si la condition n'est pas vérifiée.
        assert (coups_f[i]==0 or coups_f[i]==1) and (coups_g[i]==0 or coups_g[i]==1)
        f_coop = coups_f[i] == 1
        g_coop = coups_g[i] == 1
        if f_coop and g_coop:
            score_f+=C
            score_g+=C
        elif f_coop and not g_coop:
            score_f+=D
            score_g+=T
        elif g_coop and not f_coop:
            score_g+=D
            score_f+=T
        else:
            score_f += P
            score_g += P
    return score_f , score_g


def tournoi(T,C,P,D,strats,affichage):
    #Je rajoute un argument booléen affichage qui permet de préciser si on veut ou non un affichage du résultat de chaque match dans la console
    n = randint(500,1001)
    m = len(strats)
    scores = [0]*m
    for i in range(m):
        for j in range(i):
            a , b = score(T,C,P,D,partie(n, strats[i], strats[j]))
            if affichage:
                print(strats[i], " : ", a, strats[j], " : " , b)
            scores[i] += a
            scores[j] += b
    #Je renvoie le tableau des scores sous forme de np.array pour faciliter sa manipulation par les fonctions de classement
    return np.array(scores),n

strats = [bisounours, traître, sympa_irl, rancunier, miroir_méchant, miroir_gentil, mastermind, majorité, indecis(0.4)]

tournoi(5, 3, 1, 0, strats, False)



